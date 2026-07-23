"""Verify package metadata and, when requested, the bytes served by a repository.

This executable verifier is intentionally dependency-free so release workflows
can run it before installing the project. An existing version is accepted only
when its complete filename-to-SHA256 mapping equals the local wheel and sdist.
Post-publication callers must also request downloads so the served bytes, rather
than repository metadata alone, are hashed before downstream promotion.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

_DISTRIBUTION_SUFFIXES = (".whl", ".tar.gz")
_PYTHONHOSTED_SUFFIX = ".pythonhosted.org"
_MAX_METADATA_BYTES = 4 * 1024 * 1024
_DEFAULT_MAX_ARTIFACT_BYTES = 512 * 1024 * 1024


class ArtifactVerificationError(RuntimeError):
    """Raised when repository artifacts do not exactly match local artifacts."""


class _SameOriginRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, origin: tuple[str, str]) -> None:
        super().__init__()
        self._origin = origin

    def redirect_request(
        self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str
    ) -> Any:
        parsed = urllib.parse.urlsplit(newurl)
        if (parsed.scheme, parsed.netloc) != self._origin:
            raise ArtifactVerificationError("Repository metadata redirected across origins")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


class _PythonHostedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(
        self, req: Any, fp: Any, code: int, msg: str, headers: Any, newurl: str
    ) -> Any:
        if not _is_pythonhosted_url(newurl):
            raise ArtifactVerificationError("Artifact download redirected outside pythonhosted.org")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


@dataclass(frozen=True)
class RemoteArtifact:
    """Validated repository metadata for one distribution artifact."""

    filename: str
    sha256: str
    url: str


def _is_pythonhosted_url(url: str) -> bool:
    parsed = urllib.parse.urlsplit(url)
    return bool(
        parsed.scheme == "https"
        and parsed.hostname
        and parsed.hostname.endswith(_PYTHONHOSTED_SUFFIX)
    )


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _local_artifacts(dist_dir: Path) -> dict[str, Path]:
    if not dist_dir.is_dir():
        raise ArtifactVerificationError(f"Distribution directory does not exist: {dist_dir}")
    artifacts = {
        path.name: path
        for path in sorted(dist_dir.iterdir())
        if path.is_file() and path.name.endswith(_DISTRIBUTION_SUFFIXES)
    }
    wheels = [name for name in artifacts if name.endswith(".whl")]
    sdists = [name for name in artifacts if name.endswith(".tar.gz")]
    if len(wheels) != 1 or len(sdists) != 1 or len(artifacts) != 2:
        raise ArtifactVerificationError(
            f"Expected exactly one wheel and one .tar.gz sdist; found {sorted(artifacts)}"
        )
    return artifacts


def _release_url(repository_json_base: str, package: str, version: str) -> str:
    base = repository_json_base.rstrip("/")
    return (
        f"{base}/{urllib.parse.quote(package, safe='')}/{urllib.parse.quote(version, safe='')}/json"
    )


def _read_bounded(
    response: Any,
    *,
    maximum_bytes: int,
    deadline: float,
    description: str,
) -> bytes:
    content_length = response.headers.get("Content-Length")
    if content_length is not None:
        try:
            declared_size = int(content_length)
        except ValueError as exc:
            raise ArtifactVerificationError(
                f"{description} returned an invalid Content-Length"
            ) from exc
        if declared_size < 0 or declared_size > maximum_bytes:
            raise ArtifactVerificationError(
                f"{description} exceeds the {maximum_bytes}-byte size limit"
            )

    chunks: list[bytes] = []
    size = 0
    while True:
        if time.monotonic() >= deadline:
            raise ArtifactVerificationError(f"{description} exceeded its total deadline")
        chunk = response.read(min(1024 * 1024, maximum_bytes - size + 1))
        if not chunk:
            return b"".join(chunks)
        size += len(chunk)
        if size > maximum_bytes:
            raise ArtifactVerificationError(
                f"{description} exceeds the {maximum_bytes}-byte size limit"
            )
        chunks.append(chunk)


def _fetch_release(url: str, *, timeout: float = 20.0) -> dict[str, Any] | None:
    request = urllib.request.Request(
        url,
        headers={"Accept": "application/json", "User-Agent": "proxmox-sdk-release-verifier/1"},
    )
    parsed_url = urllib.parse.urlsplit(url)
    if parsed_url.scheme != "https" or not parsed_url.netloc:
        raise ArtifactVerificationError("Repository metadata URL must use HTTPS")
    opener = urllib.request.build_opener(
        _SameOriginRedirect((parsed_url.scheme, parsed_url.netloc))
    )
    try:
        with opener.open(request, timeout=timeout) as response:
            payload = _read_bounded(
                response,
                maximum_bytes=_MAX_METADATA_BYTES,
                deadline=time.monotonic() + timeout,
                description="Repository metadata response",
            )
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return None
        raise ArtifactVerificationError(
            f"Repository metadata request failed with HTTP {exc.code}: {url}"
        ) from exc
    except urllib.error.URLError as exc:
        raise ArtifactVerificationError(
            f"Repository metadata request failed: {url}: {exc}"
        ) from exc
    try:
        value = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ArtifactVerificationError(f"Repository returned malformed JSON: {url}") from exc
    if not isinstance(value, dict):
        raise ArtifactVerificationError(f"Repository metadata is not an object: {url}")
    return value


def _remote_artifacts(payload: dict[str, Any]) -> dict[str, RemoteArtifact]:
    urls = payload.get("urls")
    if not isinstance(urls, list):
        raise ArtifactVerificationError("Repository metadata has no artifact URL list")
    artifacts: dict[str, RemoteArtifact] = {}
    for item in urls:
        if not isinstance(item, dict):
            raise ArtifactVerificationError("Repository artifact metadata is not an object")
        filename = item.get("filename")
        url = item.get("url")
        digests = item.get("digests")
        sha256 = digests.get("sha256") if isinstance(digests, dict) else None
        if (
            not isinstance(filename, str)
            or Path(filename).name != filename
            or not filename.endswith(_DISTRIBUTION_SUFFIXES)
            or not isinstance(url, str)
            or not isinstance(sha256, str)
            or len(sha256) != 64
        ):
            raise ArtifactVerificationError(f"Invalid repository artifact metadata: {item!r}")
        try:
            int(sha256, 16)
        except ValueError as exc:
            raise ArtifactVerificationError(
                f"Invalid SHA256 for repository artifact {filename!r}"
            ) from exc
        if not _is_pythonhosted_url(url):
            raise ArtifactVerificationError(
                f"Repository artifact URL is outside pythonhosted.org: {url!r}"
            )
        if filename in artifacts:
            raise ArtifactVerificationError(f"Repository returned duplicate artifact {filename!r}")
        artifacts[filename] = RemoteArtifact(filename, sha256.lower(), url)
    return artifacts


def _compare_exact(local: dict[str, Path], remote: dict[str, RemoteArtifact]) -> list[str]:
    expected_names = set(local)
    remote_names = set(remote)
    errors: list[str] = []
    if expected_names != remote_names:
        missing = sorted(expected_names - remote_names)
        unexpected = sorted(remote_names - expected_names)
        errors.append(f"artifact set mismatch: missing={missing}, unexpected={unexpected}")
    for name in sorted(expected_names & remote_names):
        local_sha = _sha256(local[name])
        if local_sha != remote[name].sha256:
            errors.append(
                f"SHA256 mismatch for {name}: local={local_sha}, remote={remote[name].sha256}"
            )
    return errors


def _download(
    remote: RemoteArtifact,
    destination: Path,
    *,
    timeout: float = 60.0,
    maximum_bytes: int = _DEFAULT_MAX_ARTIFACT_BYTES,
) -> Path:
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / remote.filename
    temporary = destination / f".{remote.filename}.partial"
    request = urllib.request.Request(
        remote.url,
        headers={"User-Agent": "proxmox-sdk-release-verifier/1"},
    )
    digest = hashlib.sha256()
    deadline = time.monotonic() + timeout
    opener = urllib.request.build_opener(_PythonHostedRedirect())
    try:
        with (
            opener.open(request, timeout=timeout) as response,
            temporary.open("wb") as handle,
        ):
            if not _is_pythonhosted_url(response.geturl()):
                raise ArtifactVerificationError(
                    f"Artifact download redirected outside pythonhosted.org: {response.geturl()!r}"
                )
            content_length = response.headers.get("Content-Length")
            if content_length is not None:
                try:
                    declared_size = int(content_length)
                except ValueError as exc:
                    raise ArtifactVerificationError(
                        f"Artifact {remote.filename} returned an invalid Content-Length"
                    ) from exc
                if declared_size < 0 or declared_size > maximum_bytes:
                    raise ArtifactVerificationError(
                        f"Artifact {remote.filename} exceeds the {maximum_bytes}-byte size limit"
                    )
            size = 0
            while True:
                if time.monotonic() >= deadline:
                    raise ArtifactVerificationError(
                        f"Artifact {remote.filename} exceeded its total download deadline"
                    )
                chunk = response.read(min(1024 * 1024, maximum_bytes - size + 1))
                if not chunk:
                    break
                size += len(chunk)
                if size > maximum_bytes:
                    raise ArtifactVerificationError(
                        f"Artifact {remote.filename} exceeds the {maximum_bytes}-byte size limit"
                    )
                handle.write(chunk)
                digest.update(chunk)
    except (ArtifactVerificationError, OSError, urllib.error.URLError) as exc:
        temporary.unlink(missing_ok=True)
        if isinstance(exc, ArtifactVerificationError):
            raise
        raise ArtifactVerificationError(
            f"Failed to download repository artifact {remote.filename}: {exc}"
        ) from exc
    actual = digest.hexdigest()
    if actual != remote.sha256:
        temporary.unlink(missing_ok=True)
        raise ArtifactVerificationError(
            f"Downloaded SHA256 mismatch for {remote.filename}: "
            f"expected={remote.sha256}, actual={actual}"
        )
    temporary.replace(target)
    return target.resolve()


def _write_github_output(values: dict[str, str], output_path: Path | None) -> None:
    if output_path is None:
        return
    with output_path.open("a", encoding="utf-8") as handle:
        for key, value in values.items():
            if "\n" in value or "\r" in value:
                raise ArtifactVerificationError(f"Unsafe multiline GitHub output for {key}")
            handle.write(f"{key}={value}\n")


def verify_repository(
    *,
    repository_json_base: str,
    package: str,
    version: str,
    dist_dir: Path,
    allow_absent: bool,
    wait_seconds: float,
    download_dir: Path | None,
    request_timeout: float = 20.0,
    download_timeout: float = 60.0,
    max_artifact_bytes: int = _DEFAULT_MAX_ARTIFACT_BYTES,
) -> tuple[bool, dict[str, Path]]:
    """Return ``(upload_required, downloads)`` after fail-closed verification."""

    numeric_values = {
        "wait_seconds": wait_seconds,
        "request_timeout": request_timeout,
        "download_timeout": download_timeout,
    }
    for name, value in numeric_values.items():
        if not math.isfinite(value) or value < 0:
            raise ArtifactVerificationError(f"{name} must be a finite non-negative number")
    if request_timeout == 0 or download_timeout == 0:
        raise ArtifactVerificationError("Network timeouts must be greater than zero")
    if max_artifact_bytes <= 0:
        raise ArtifactVerificationError("max_artifact_bytes must be greater than zero")

    local = _local_artifacts(dist_dir)
    url = _release_url(repository_json_base, package, version)
    deadline = time.monotonic() + max(wait_seconds, 0.0)
    last_error: str | None = None
    while True:
        payload = _fetch_release(url, timeout=request_timeout)
        if payload is None:
            if allow_absent:
                return True, {}
            last_error = f"Repository version does not exist: {package}=={version}"
        else:
            remote = _remote_artifacts(payload)
            errors = _compare_exact(local, remote)
            if not errors:
                downloads: dict[str, Path] = {}
                if download_dir is not None:
                    downloads = {
                        name: _download(
                            artifact,
                            download_dir,
                            timeout=download_timeout,
                            maximum_bytes=max_artifact_bytes,
                        )
                        for name, artifact in sorted(remote.items())
                    }
                return False, downloads
            last_error = "; ".join(errors)
            if allow_absent:
                break
        if time.monotonic() >= deadline:
            break
        time.sleep(min(5.0, max(deadline - time.monotonic(), 0.0)))
    raise ArtifactVerificationError(last_error or "Repository artifact verification failed")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repository-json-base", required=True)
    parser.add_argument("--package", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--dist", type=Path, required=True)
    parser.add_argument("--allow-absent", action="store_true")
    parser.add_argument("--wait-seconds", type=float, default=0.0)
    parser.add_argument("--request-timeout", type=float, default=20.0)
    parser.add_argument("--download-timeout", type=float, default=60.0)
    parser.add_argument("--max-artifact-bytes", type=int, default=_DEFAULT_MAX_ARTIFACT_BYTES)
    parser.add_argument("--download-dir", type=Path)
    parser.add_argument("--github-output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run exact repository verification from CLI arguments."""

    args = _parse_args(list(sys.argv[1:] if argv is None else argv))
    upload_required, downloads = verify_repository(
        repository_json_base=args.repository_json_base,
        package=args.package,
        version=args.version,
        dist_dir=args.dist.resolve(),
        allow_absent=args.allow_absent,
        wait_seconds=args.wait_seconds,
        download_dir=args.download_dir.resolve() if args.download_dir else None,
        request_timeout=args.request_timeout,
        download_timeout=args.download_timeout,
        max_artifact_bytes=args.max_artifact_bytes,
    )
    outputs = {"upload_required": str(upload_required).lower()}
    wheels = [path for name, path in downloads.items() if name.endswith(".whl")]
    sdists = [path for name, path in downloads.items() if name.endswith(".tar.gz")]
    if wheels:
        outputs["wheel_path"] = str(wheels[0])
        outputs["wheel_filename"] = wheels[0].name
        outputs["wheel_sha256"] = _sha256(wheels[0])
        outputs["wheel_size"] = str(wheels[0].stat().st_size)
    if sdists:
        outputs["sdist_path"] = str(sdists[0])
        outputs["sdist_filename"] = sdists[0].name
        outputs["sdist_sha256"] = _sha256(sdists[0])
        outputs["sdist_size"] = str(sdists[0].stat().st_size)
    output_path = args.github_output or (
        Path(os.environ["GITHUB_OUTPUT"]) if os.environ.get("GITHUB_OUTPUT") else None
    )
    _write_github_output(outputs, output_path)
    if upload_required:
        state = "absent; upload required"
    elif downloads:
        state = "metadata and served-byte SHA256 match"
    else:
        state = "metadata filename/SHA256 match"
    print(f"Verified {args.package}=={args.version}: {state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

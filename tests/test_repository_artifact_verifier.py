"""Tests for fail-closed Python repository artifact verification."""

from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from tests import verify_repository_artifacts as verifier


def _dist(tmp_path: Path) -> Path:
    dist = tmp_path / "dist"
    dist.mkdir()
    (dist / "proxmox_sdk-1.2.3-py3-none-any.whl").write_bytes(b"wheel")
    (dist / "proxmox_sdk-1.2.3.tar.gz").write_bytes(b"sdist")
    return dist


def _payload(dist: Path, *, mutate_hash: bool = False) -> dict[str, object]:
    urls: list[dict[str, object]] = []
    for path in sorted(dist.iterdir()):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if mutate_hash and path.suffix == ".whl":
            digest = "0" * 64
        urls.append(
            {
                "filename": path.name,
                "url": f"https://files.pythonhosted.org/packages/{path.name}",
                "digests": {"sha256": digest},
            }
        )
    return {"urls": urls}


def test_absent_version_requires_upload(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    dist = _dist(tmp_path)
    monkeypatch.setattr(verifier, "_fetch_release", lambda _url, **_kwargs: None)

    upload_required, downloads = verifier.verify_repository(
        repository_json_base="https://test.pypi.org/pypi",
        package="proxmox-sdk",
        version="1.2.3",
        dist_dir=dist,
        allow_absent=True,
        wait_seconds=0,
        download_dir=None,
    )

    assert upload_required is True
    assert downloads == {}


def test_existing_version_requires_exact_hashes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dist = _dist(tmp_path)
    monkeypatch.setattr(verifier, "_fetch_release", lambda _url, **_kwargs: _payload(dist))

    upload_required, _ = verifier.verify_repository(
        repository_json_base="https://test.pypi.org/pypi",
        package="proxmox-sdk",
        version="1.2.3",
        dist_dir=dist,
        allow_absent=True,
        wait_seconds=0,
        download_dir=None,
    )

    assert upload_required is False


def test_existing_version_with_different_hash_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dist = _dist(tmp_path)
    monkeypatch.setattr(
        verifier,
        "_fetch_release",
        lambda _url, **_kwargs: _payload(dist, mutate_hash=True),
    )

    with pytest.raises(verifier.ArtifactVerificationError, match="SHA256 mismatch"):
        verifier.verify_repository(
            repository_json_base="https://test.pypi.org/pypi",
            package="proxmox-sdk",
            version="1.2.3",
            dist_dir=dist,
            allow_absent=True,
            wait_seconds=0,
            download_dir=None,
        )


def test_existing_version_with_extra_artifact_fails_closed(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dist = _dist(tmp_path)
    payload = _payload(dist)
    assert isinstance(payload["urls"], list)
    payload["urls"].append(
        {
            "filename": "proxmox_sdk-1.2.3-cp313-manylinux.whl",
            "url": "https://files.pythonhosted.org/packages/extra.whl",
            "digests": {"sha256": "1" * 64},
        }
    )
    monkeypatch.setattr(verifier, "_fetch_release", lambda _url, **_kwargs: payload)

    with pytest.raises(verifier.ArtifactVerificationError, match="artifact set mismatch"):
        verifier.verify_repository(
            repository_json_base="https://test.pypi.org/pypi",
            package="proxmox-sdk",
            version="1.2.3",
            dist_dir=dist,
            allow_absent=True,
            wait_seconds=0,
            download_dir=None,
        )


def test_remote_artifact_url_must_be_pythonhosted(tmp_path: Path) -> None:
    dist = _dist(tmp_path)
    payload = _payload(dist)
    assert isinstance(payload["urls"], list)
    payload["urls"][0]["url"] = "https://example.invalid/package.whl"

    with pytest.raises(verifier.ArtifactVerificationError, match="outside pythonhosted"):
        verifier._remote_artifacts(payload)


def test_redirect_handlers_block_cross_origin_before_following() -> None:
    with pytest.raises(verifier.ArtifactVerificationError, match="across origins"):
        verifier._SameOriginRedirect(("https", "pypi.org")).redirect_request(
            None, None, 302, "redirect", {}, "https://example.invalid/metadata"
        )
    with pytest.raises(verifier.ArtifactVerificationError, match="outside pythonhosted"):
        verifier._PythonHostedRedirect().redirect_request(
            None, None, 302, "redirect", {}, "https://example.invalid/artifact.whl"
        )


def test_download_hashes_served_bytes_and_emits_project_wheel_identity(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    dist = _dist(tmp_path)
    monkeypatch.setattr(
        verifier,
        "_fetch_release",
        lambda _url, **_kwargs: _payload(dist),
    )

    def copy_remote(
        remote: verifier.RemoteArtifact,
        destination: Path,
        **_kwargs: object,
    ) -> Path:
        destination.mkdir(exist_ok=True)
        target = destination / remote.filename
        target.write_bytes((dist / remote.filename).read_bytes())
        return target.resolve()

    monkeypatch.setattr(verifier, "_download", copy_remote)
    upload_required, downloads = verifier.verify_repository(
        repository_json_base="https://pypi.org/pypi",
        package="proxmox-sdk",
        version="1.2.3",
        dist_dir=dist,
        allow_absent=False,
        wait_seconds=0,
        download_dir=tmp_path / "downloads",
    )

    assert upload_required is False
    assert set(downloads) == {
        "proxmox_sdk-1.2.3-py3-none-any.whl",
        "proxmox_sdk-1.2.3.tar.gz",
    }
    assert verifier._sha256(downloads["proxmox_sdk-1.2.3-py3-none-any.whl"]) == (
        hashlib.sha256(b"wheel").hexdigest()
    )


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("request_timeout", 0),
        ("download_timeout", float("inf")),
        ("wait_seconds", -1),
        ("max_artifact_bytes", 0),
    ],
)
def test_network_limits_fail_closed(tmp_path: Path, field: str, value: float | int) -> None:
    arguments: dict[str, object] = {
        "repository_json_base": "https://pypi.org/pypi",
        "package": "proxmox-sdk",
        "version": "1.2.3",
        "dist_dir": _dist(tmp_path),
        "allow_absent": False,
        "wait_seconds": 0,
        "download_dir": None,
    }
    arguments[field] = value

    with pytest.raises(verifier.ArtifactVerificationError):
        verifier.verify_repository(**arguments)  # type: ignore[arg-type]

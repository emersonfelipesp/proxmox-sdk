"""Build wheel/sdist twice under one epoch and fail unless their hashes match."""

from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
_DISTRIBUTION_SUFFIXES = (".whl", ".tar.gz")
_IGNORED_NAMES = {
    ".coverage",
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tox",
    ".venv",
    "build",
    "coverage.xml",
    "dist",
    "htmlcov",
    "__pycache__",
}


class ReproducibilityError(RuntimeError):
    """Raised when a distribution cannot be reproduced byte for byte."""


def _ignore(_directory: str, names: list[str]) -> set[str]:
    return {
        name
        for name in names
        if name in _IGNORED_NAMES or name.endswith(".egg-info") or name.endswith(".pyc")
    }


def _set_tree_mtime(root: Path, timestamp: int) -> None:
    paths = sorted(root.rglob("*"), key=lambda path: len(path.parts), reverse=True)
    for path in paths:
        if not path.is_symlink():
            os.utime(path, (timestamp, timestamp), follow_symlinks=False)
    os.utime(root, (timestamp, timestamp), follow_symlinks=False)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _artifact_hashes(directory: Path) -> dict[str, str]:
    artifacts = {
        path.name: _sha256(path)
        for path in sorted(directory.iterdir())
        if path.is_file() and path.name.endswith(_DISTRIBUTION_SUFFIXES)
    }
    if len([name for name in artifacts if name.endswith(".whl")]) != 1:
        raise ReproducibilityError(f"Expected one wheel, found {sorted(artifacts)}")
    if len([name for name in artifacts if name.endswith(".tar.gz")]) != 1:
        raise ReproducibilityError(f"Expected one sdist, found {sorted(artifacts)}")
    if len(artifacts) != 2:
        raise ReproducibilityError(f"Unexpected distribution set: {sorted(artifacts)}")
    return artifacts


def _validate_archive_member(member: tarfile.TarInfo) -> None:
    path = PurePosixPath(member.name)
    if not member.name or path.is_absolute() or ".." in path.parts:
        raise ReproducibilityError(f"Unsafe sdist member path: {member.name!r}")
    if (member.issym() or member.islnk()) and (
        PurePosixPath(member.linkname).is_absolute() or ".." in PurePosixPath(member.linkname).parts
    ):
        raise ReproducibilityError(
            f"Unsafe sdist link target for {member.name!r}: {member.linkname!r}"
        )


def _normalize_sdist(path: Path, *, source_date_epoch: int) -> None:
    """Rewrite an sdist with canonical tar metadata and gzip headers."""

    temporary_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            with tarfile.open(path, mode="r:gz") as source_archive:
                members = sorted(source_archive.getmembers(), key=lambda member: member.name)
                with gzip.GzipFile(
                    filename="",
                    mode="wb",
                    fileobj=temporary,
                    compresslevel=9,
                    mtime=source_date_epoch,
                ) as compressed:
                    with tarfile.open(
                        fileobj=compressed,
                        mode="w|",
                        format=tarfile.PAX_FORMAT,
                    ) as destination_archive:
                        for member in members:
                            _validate_archive_member(member)
                            normalized = copy.copy(member)
                            normalized.gid = 0
                            normalized.gname = ""
                            normalized.mtime = source_date_epoch
                            normalized.pax_headers = {}
                            normalized.uid = 0
                            normalized.uname = ""
                            payload = (
                                source_archive.extractfile(member) if member.isfile() else None
                            )
                            destination_archive.addfile(normalized, payload)
                            if payload is not None:
                                payload.close()
        os.replace(temporary_path, path)
        temporary_path = None
    except (gzip.BadGzipFile, OSError, tarfile.TarError) as error:
        raise ReproducibilityError(f"Unable to normalize sdist {path.name}: {error}") from error
    finally:
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


def _build(source: Path, output: Path, *, source_date_epoch: int) -> None:
    environment = os.environ.copy()
    environment.update(
        {
            "LC_ALL": "C.UTF-8",
            "PYTHONHASHSEED": "0",
            "SOURCE_DATE_EPOCH": str(source_date_epoch),
            "TZ": "UTC",
        }
    )
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "build",
            "--no-isolation",
            "--outdir",
            str(output),
        ],
        cwd=source,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
        timeout=600,
    )
    if completed.returncode != 0:
        output_tail = "\n".join((completed.stdout + completed.stderr).splitlines()[-80:])
        raise ReproducibilityError(
            f"Distribution build failed with exit code {completed.returncode}:\n{output_tail}"
        )

    sdists = sorted(output.glob("*.tar.gz"))
    if len(sdists) != 1:
        raise ReproducibilityError(
            f"Expected one sdist before normalization, found {[path.name for path in sdists]}"
        )
    _normalize_sdist(sdists[0], source_date_epoch=source_date_epoch)


def build_reproducible_distributions(
    *, source_date_epoch: int, output_dir: Path, manifest_path: Path
) -> dict[str, str]:
    """Build two timestamp-perturbed source copies and retain one identical set."""

    if not 315532800 <= source_date_epoch <= 4294967295:
        raise ReproducibilityError(
            "SOURCE_DATE_EPOCH must be between 1980-01-01 and the gzip timestamp limit"
        )
    output_dir.mkdir(parents=True, exist_ok=True)
    existing = [path for path in output_dir.iterdir() if path.name.endswith(_DISTRIBUTION_SUFFIXES)]
    if existing:
        raise ReproducibilityError(
            f"Output directory already contains distributions: {[path.name for path in existing]}"
        )

    with tempfile.TemporaryDirectory(prefix="proxmox-sdk-repro-") as temporary:
        temporary_root = Path(temporary)
        hashes: list[dict[str, str]] = []
        build_dirs: list[Path] = []
        for index, offset in enumerate((101, 86401), start=1):
            source = temporary_root / f"source-{index}"
            build_output = temporary_root / f"dist-{index}"
            shutil.copytree(ROOT, source, symlinks=True, ignore=_ignore)
            _set_tree_mtime(source, source_date_epoch + offset)
            build_output.mkdir()
            _build(source, build_output, source_date_epoch=source_date_epoch)
            hashes.append(_artifact_hashes(build_output))
            build_dirs.append(build_output)

        if hashes[0] != hashes[1]:
            raise ReproducibilityError(
                "Distribution hashes differ under one SOURCE_DATE_EPOCH: "
                f"first={hashes[0]}, second={hashes[1]}"
            )
        for name in sorted(hashes[0]):
            shutil.copy2(build_dirs[0] / name, output_dir / name)

    manifest = {
        "algorithm": "sha256",
        "artifacts": hashes[0],
        "source_date_epoch": source_date_epoch,
    }
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return hashes[0]


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-date-epoch", required=True, type=int)
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Build and report a byte-for-byte reproducible wheel/sdist pair."""

    args = _parse_args(list(sys.argv[1:] if argv is None else argv))
    hashes = build_reproducible_distributions(
        source_date_epoch=args.source_date_epoch,
        output_dir=args.output_dir.resolve(),
        manifest_path=args.manifest.resolve(),
    )
    for filename, digest in sorted(hashes.items()):
        print(f"{digest}  {filename}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

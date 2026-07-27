"""Unit contracts for the deterministic distribution builder."""

from __future__ import annotations

import gzip
import hashlib
import io
import tarfile
from pathlib import Path

import pytest

from tests import build_reproducible_distributions as reproducible


def test_artifact_hashes_require_one_wheel_and_one_sdist(tmp_path: Path) -> None:
    (tmp_path / "proxmox_sdk-1.2.3-py3-none-any.whl").write_bytes(b"wheel")
    (tmp_path / "proxmox_sdk-1.2.3.tar.gz").write_bytes(b"sdist")

    assert reproducible._artifact_hashes(tmp_path) == {
        "proxmox_sdk-1.2.3-py3-none-any.whl": hashlib.sha256(b"wheel").hexdigest(),
        "proxmox_sdk-1.2.3.tar.gz": hashlib.sha256(b"sdist").hexdigest(),
    }


def test_artifact_hashes_reject_extra_wheel(tmp_path: Path) -> None:
    (tmp_path / "one.whl").write_bytes(b"one")
    (tmp_path / "two.whl").write_bytes(b"two")
    (tmp_path / "source.tar.gz").write_bytes(b"source")

    with pytest.raises(reproducible.ReproducibilityError, match="Expected one wheel"):
        reproducible._artifact_hashes(tmp_path)


def test_source_date_epoch_must_be_zip_safe(tmp_path: Path) -> None:
    with pytest.raises(reproducible.ReproducibilityError, match="1980"):
        reproducible.build_reproducible_distributions(
            source_date_epoch=1,
            output_dir=tmp_path / "dist",
            manifest_path=tmp_path / "manifest.json",
        )


def _write_sdist(path: Path, *, gzip_mtime: int, member_mtime: int, reverse_order: bool) -> None:
    entries = [("package-1.0/", b""), ("package-1.0/module.py", b"VALUE = 1\n")]
    if reverse_order:
        entries.reverse()
    with path.open("wb") as raw:
        with gzip.GzipFile(
            filename="different-name", fileobj=raw, mode="wb", mtime=gzip_mtime
        ) as gz:
            with tarfile.open(fileobj=gz, mode="w|") as archive:
                for name, content in entries:
                    member = tarfile.TarInfo(name)
                    member.mtime = member_mtime
                    if name.endswith("/"):
                        member.type = tarfile.DIRTYPE
                        member.mode = 0o755
                        archive.addfile(member)
                    else:
                        member.mode = 0o644
                        member.size = len(content)
                        archive.addfile(member, io.BytesIO(content))


def test_normalize_sdist_canonicalizes_tar_and_gzip_metadata(tmp_path: Path) -> None:
    first = tmp_path / "first.tar.gz"
    second = tmp_path / "second.tar.gz"
    _write_sdist(first, gzip_mtime=10, member_mtime=20, reverse_order=False)
    _write_sdist(second, gzip_mtime=30, member_mtime=40, reverse_order=True)

    reproducible._normalize_sdist(first, source_date_epoch=1_700_000_000)
    reproducible._normalize_sdist(second, source_date_epoch=1_700_000_000)

    assert first.read_bytes() == second.read_bytes()


def test_normalize_sdist_rejects_parent_traversal(tmp_path: Path) -> None:
    archive_path = tmp_path / "unsafe.tar.gz"
    with tarfile.open(archive_path, mode="w:gz") as archive:
        member = tarfile.TarInfo("../outside")
        member.size = 1
        archive.addfile(member, io.BytesIO(b"x"))

    with pytest.raises(reproducible.ReproducibilityError, match="Unsafe sdist member"):
        reproducible._normalize_sdist(archive_path, source_date_epoch=1_700_000_000)

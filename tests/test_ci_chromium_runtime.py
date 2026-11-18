"""Closed contracts for unprivileged, authenticated Chromium library preparation."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import xml.etree.ElementTree as ET
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ci_chromium_runtime", ROOT / "tools/prepare_ci_chromium.py"
)
assert SPEC is not None and SPEC.loader is not None
runtime = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(runtime)


@pytest.fixture(autouse=True)
def private_host_status(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    status = tmp_path / "host-status"
    status.write_bytes(b"Package: libc6\nStatus: install ok installed\nVersion: 2.36\n\n")
    monkeypatch.setattr(runtime, "HOST_STATUS", status)
    return status


@pytest.fixture
def supported(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    keyring = tmp_path / "archive.gpg"
    keyring.write_bytes(b"fixture public keyring; never used for real authentication")
    monkeypatch.setattr(runtime, "KEYRING", keyring)
    monkeypatch.setattr(runtime.os, "geteuid", lambda: 1000)
    monkeypatch.setattr(
        runtime.platform, "freedesktop_os_release", lambda: {"ID": "debian", "VERSION_ID": "12"}
    )
    monkeypatch.setattr(runtime.platform, "machine", lambda: "x86_64")
    return keyring


def test_privileged_and_unsupported_hosts_refuse_before_state_or_commands(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    runner = Mock()
    monkeypatch.setattr(runtime.subprocess, "run", runner)
    directory = tmp_path / "runtime"
    for uid, release, machine in (
        (0, {"ID": "debian", "VERSION_ID": "12"}, "x86_64"),
        (1000, {"ID": "ubuntu", "VERSION_ID": "25.04"}, "x86_64"),
        (1000, {"ID": "debian", "VERSION_ID": "13"}, "x86_64"),
        (1000, {"ID": "debian", "VERSION_ID": "12"}, "aarch64"),
    ):
        monkeypatch.setattr(runtime.os, "geteuid", lambda: uid)
        monkeypatch.setattr(runtime.platform, "freedesktop_os_release", lambda: release)
        monkeypatch.setattr(runtime.platform, "machine", lambda: machine)
        with pytest.raises(ValueError):
            runtime.acquire(directory)
    assert not directory.exists()
    runner.assert_not_called()


def test_keyring_must_be_preinstalled_regular_and_root_controlled(
    monkeypatch: pytest.MonkeyPatch,
    supported: Path,
) -> None:
    for mode, uid in ((0o100666, 0), (0o120644, 0), (0o100644, 1000)):
        monkeypatch.setattr(
            runtime,
            "KEYRING",
            SimpleNamespace(lstat=lambda: SimpleNamespace(st_mode=mode, st_uid=uid)),
        )
        with pytest.raises(ValueError, match="root controlled"):
            runtime.require_supported_host()


def test_exact_locked_distribution_and_native_dependency_set_are_required(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    registry = tmp_path / "registry"
    (registry / "lib/server/registry").mkdir(parents=True)
    native = registry / "lib/server/registry/nativeDeps.js"
    native.write_text(
        '"debian12-x64": { tools: ["fonts-liberation"], chromium: '
        + json.dumps(runtime.PACKAGES)
        + " }",
        encoding="utf-8",
    )
    manifest = registry / "browsers.json"
    rows = [{"name": name, "revision": "1208"} for name in ("chromium", "chromium-headless-shell")]
    manifest.write_text(json.dumps({"browsers": rows}), encoding="utf-8")
    package = SimpleNamespace(version="1.58.0", locate_file=lambda name: registry)
    monkeypatch.setattr(runtime.importlib.metadata, "distribution", lambda name: package)
    runtime.require_locked_playwright()
    rows[0]["revision"] = "1209"
    manifest.write_text(json.dumps({"browsers": rows}), encoding="utf-8")
    with pytest.raises(ValueError, match="identity changed"):
        runtime.require_locked_playwright()
    rows[0]["revision"] = "1208"
    manifest.write_text(json.dumps({"browsers": rows}), encoding="utf-8")
    package.version = "1.59.0"
    with pytest.raises(ValueError, match="1.58.0"):
        runtime.require_locked_playwright()
    package.version = "1.58.0"
    native.write_text('"debian12-x64": { chromium: ["libglib2.0-0"] }', encoding="utf-8")
    with pytest.raises(ValueError, match="nativeDeps"):
        runtime.require_locked_playwright()


def test_configuration_is_private_and_isolates_host_configuration(tmp_path: Path) -> None:
    directory = tmp_path / "runtime"
    configuration = runtime.private_configuration(directory)
    assert directory.stat().st_mode & 0o777 == 0o700
    assert (directory / "state/status").read_bytes() == runtime.HOST_STATUS.read_bytes()
    text = configuration.read_text()
    assert f'Dir::State::status "{directory}/state/status"' in text
    assert 'Dir::Etc::parts "parts"; Dir::Etc::main "main"' in text
    assert 'Dir::Etc::netrc "auth"; Dir::Etc::netrcparts "auth.parts"' in text
    assert 'APT::Update::Error-Mode "any"' in text
    assert "Sandbox" not in text
    with pytest.raises(FileExistsError):
        runtime.private_configuration(directory)


def test_only_authenticated_fresh_debian_sources_are_accepted(tmp_path: Path) -> None:
    directory = tmp_path / "runtime"
    text = runtime.private_configuration(directory).read_text()
    assert 'Acquire::AllowInsecureRepositories "false"' in text
    assert 'Acquire::AllowDowngradeToInsecureRepositories "false"' in text
    assert 'APT::Get::AllowUnauthenticated "false"' in text
    assert 'Acquire::Check-Valid-Until "true"' in text
    sources = (directory / "etc/sources.list").read_text()
    assert sources.count("signed-by=/usr/share/keyrings/debian-archive-keyring.gpg") == 3
    assert sources.count("https://deb.debian.org/") == 3


def test_unsafe_directory_refuses_without_creating_state(tmp_path: Path) -> None:
    for directory in (Path("relative"), tmp_path / 'bad"name', tmp_path / "bad\nname"):
        with pytest.raises(ValueError, match="APT-safe"):
            runtime.private_configuration(directory)


def test_acquisition_uses_only_download_and_data_extraction(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    directory = tmp_path / "runtime"
    monkeypatch.setattr(runtime, "require_supported_host", lambda: None)
    monkeypatch.setattr(runtime, "require_locked_playwright", lambda: None)
    calls = []

    def run(argv: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append((argv, kwargs))
        if "--download-only" in argv:
            (directory / "cache/archives/library_1_amd64.deb").write_bytes(
                b"signed-archive-fixture"
            )
        return SimpleNamespace(
            stdout="Package: libglib2.0-0\nVersion: 2.74.6-2\nArchitecture: amd64\n"
        )

    monkeypatch.setattr(runtime.subprocess, "run", run)
    runtime.acquire(directory)
    assert calls[0][0] == ["/usr/bin/apt-get", "update"]
    assert calls[1][0] == [
        "/usr/bin/apt-get",
        "--yes",
        "--download-only",
        "--reinstall",
        "--no-install-recommends",
        "install",
        *runtime.PACKAGES,
        runtime.FONT_PACKAGE,
    ]
    assert calls[3][0] == [
        "/usr/bin/dpkg-deb",
        "--extract",
        str(directory / "cache/archives/library_1_amd64.deb"),
        str(directory / "prefix"),
    ]
    inventory = json.loads((directory / "archive-inventory.json").read_text())
    assert inventory == [
        {
            "file": "library_1_amd64.deb",
            "Package": "libglib2.0-0",
            "Version": "2.74.6-2",
            "Architecture": "amd64",
            "sha256": hashlib.sha256(b"signed-archive-fixture").hexdigest(),
        }
    ]
    for _, options in calls:
        assert options["check"] is True
        assert options["env"] == {
            "PATH": "/usr/bin:/bin",
            "LANG": "C.UTF-8",
            "APT_CONFIG": str(directory / "apt.conf"),
        }


@pytest.mark.parametrize("failure_at", [0, 1])
def test_metadata_or_download_failure_never_extracts(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    failure_at: int,
) -> None:
    monkeypatch.setattr(runtime, "require_supported_host", lambda: None)
    monkeypatch.setattr(runtime, "require_locked_playwright", lambda: None)
    calls = []

    def run(argv: list[str], **kwargs: object) -> None:
        calls.append(argv)
        if len(calls) == failure_at + 1:
            raise runtime.subprocess.CalledProcessError(100, argv)

    monkeypatch.setattr(runtime.subprocess, "run", run)
    with pytest.raises(runtime.subprocess.CalledProcessError):
        runtime.acquire(tmp_path / "runtime")
    assert len(calls) == failure_at + 1
    assert all(argv[0] == "/usr/bin/apt-get" for argv in calls)


def test_empty_download_closure_refuses_instead_of_claiming_browser_readiness(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    monkeypatch.setattr(runtime, "require_supported_host", lambda: None)
    monkeypatch.setattr(runtime, "require_locked_playwright", lambda: None)
    monkeypatch.setattr(runtime.subprocess, "run", Mock())
    with pytest.raises(ValueError, match="missing or oversized"):
        runtime.acquire(tmp_path / "runtime")


@pytest.mark.parametrize("package", ["libc6", "libc-bin", "ld-linux-x86-64", "musl", "libc6-i386"])
def test_core_abi_archives_refuse_the_entire_set_before_any_extraction(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
    package: str,
) -> None:
    directory = tmp_path / "runtime"
    monkeypatch.setattr(runtime, "require_supported_host", lambda: None)
    monkeypatch.setattr(runtime, "require_locked_playwright", lambda: None)
    calls = []

    def run(argv: list[str], **kwargs: object) -> SimpleNamespace:
        calls.append(argv)
        if "--download-only" in argv:
            for name in ("a-library.deb", "z-core.deb"):
                (directory / "cache/archives" / name).write_bytes(b"authenticated-fixture")
        selected = package if "z-core.deb" in " ".join(argv) else "libglib2.0-0"
        return SimpleNamespace(stdout=f"Package: {selected}\nVersion: 2.36\nArchitecture: amd64\n")

    monkeypatch.setattr(runtime.subprocess, "run", run)
    with pytest.raises(ValueError, match="core ABI or loader"):
        runtime.acquire(directory)
    assert all("--extract" not in argv for argv in calls)
    inventory = json.loads((directory / "archive-inventory.json").read_text())
    assert [row["Package"] for row in inventory] == ["libglib2.0-0", package]


@pytest.mark.parametrize(
    "raw",
    [
        "Package: x\nVersion: 1\nArchitecture: arm64\n",
        "Package: x\nVersion: 1\nVersion: 2\nArchitecture: amd64\n",
        "Package: x\nArchitecture: amd64\n",
        "Package: /unsafe\nVersion: 1\nArchitecture: amd64\n",
        "Package: x\nVersion: bad value\nArchitecture: amd64\n",
    ],
)
def test_malformed_or_unsupported_package_identity_refuses(raw: str) -> None:
    with pytest.raises(ValueError):
        runtime.package_fields(raw)


@pytest.mark.parametrize(
    "native",
    [
        '"debian12-x64": { tools: ["xvfb"] }',
        '"ubuntu24.04-x64": { tools: ["fonts-liberation"] }',
        '"debian12-x64": { tools: ["arbitrary-font-selector"] }',
    ],
)
def test_fixed_font_must_belong_to_the_locked_debian_tools(native: str) -> None:
    with pytest.raises(ValueError, match="font package"):
        runtime.require_locked_font(native)


def test_fontconfig_has_only_the_fixed_extracted_font_directory_and_private_cache(
    tmp_path: Path,
) -> None:
    directory = tmp_path / "runtime"
    runtime.private_configuration(directory)
    root = ET.fromstring((directory / "fontconfig/fonts.conf").read_text())
    assert root.tag == "fontconfig"
    assert [element.text for element in root.findall("dir")] == [
        str(directory / "prefix/usr/share/fonts/truetype/liberation")
    ]
    assert [element.text for element in root.findall("cachedir")] == [
        str(directory / "fontconfig/cache")
    ]
    assert root.findall("include") == []
    assert (directory / "fontconfig/cache").is_dir()

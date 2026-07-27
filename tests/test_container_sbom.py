"""Contracts for deterministic image inventory and provenance metadata."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tests import generate_container_sbom as container_sbom


def _fake_run(arguments: list[str], *, timeout: int = 180) -> str:  # noqa: ARG001
    if arguments[:3] == ["docker", "image", "inspect"]:
        return json.dumps(
            [
                {
                    "Architecture": "amd64",
                    "Config": {
                        "Labels": {
                            "io.nmulti.proxmox-sdk.wheel.sha256": "a" * 64,
                            "org.opencontainers.image.revision": "b" * 40,
                            "org.opencontainers.image.version": "1.2.3",
                        }
                    },
                    "Id": "sha256:" + "c" * 64,
                    "Os": "linux",
                }
            ]
        )
    if "/sbin/apk" in arguments:
        return "ca-certificates-20260611-r0 x86_64 {ca-certificates}\n"
    return json.dumps([["proxmox-sdk", "1.2.3"]])


def test_sbom_binds_platform_image_labels_and_versions(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(container_sbom, "_run", _fake_run)

    document = container_sbom.generate_sbom(
        image="local/proxmox-sdk:test",
        platform="linux/amd64",
    )

    assert document["components"] == [
        {
            "bom-ref": "apk:ca-certificates-20260611-r0",
            "name": "ca-certificates",
            "type": "library",
            "version": "20260611-r0",
        },
        {
            "bom-ref": "pypi:proxmox-sdk@1.2.3",
            "name": "proxmox-sdk",
            "type": "library",
            "version": "1.2.3",
        },
    ]
    properties = {
        item["name"]: item["value"] for item in document["metadata"]["component"]["properties"]
    }
    assert properties == {
        "oci.image.id": "sha256:" + "c" * 64,
        "oci.image.label.io.nmulti.proxmox-sdk.wheel.sha256": "a" * 64,
        "oci.image.label.org.opencontainers.image.revision": "b" * 40,
        "oci.image.label.org.opencontainers.image.version": "1.2.3",
        "oci.image.platform": "linux/amd64",
    }


def test_sbom_rejects_platform_mismatch(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(container_sbom, "_run", _fake_run)

    with pytest.raises(container_sbom.SbomError, match="does not match"):
        container_sbom.generate_sbom(
            image="local/proxmox-sdk:test",
            platform="linux/arm64",
        )


def test_sbom_requires_revision_and_version_labels(monkeypatch: pytest.MonkeyPatch) -> None:
    def run_without_labels(arguments: list[str], *, timeout: int = 180) -> str:  # noqa: ARG001
        if arguments[:3] == ["docker", "image", "inspect"]:
            return json.dumps(
                [
                    {
                        "Architecture": "amd64",
                        "Config": {"Labels": {}},
                        "Id": "sha256:" + "c" * 64,
                        "Os": "linux",
                    }
                ]
            )
        raise AssertionError("Inventory commands must not run without provenance labels")

    monkeypatch.setattr(container_sbom, "_run", run_without_labels)

    with pytest.raises(container_sbom.SbomError, match="missing provenance labels"):
        container_sbom.generate_sbom(
            image="local/proxmox-sdk:test",
            platform="linux/amd64",
        )


def test_sbom_can_use_explicit_static_emulator(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    emulator = tmp_path / "qemu-aarch64"
    emulator.write_bytes(b"reviewed-emulator")
    calls: list[list[str]] = []

    def record_run(arguments: list[str], *, timeout: int = 180) -> str:
        calls.append(arguments)
        return _fake_run(arguments, timeout=timeout)

    monkeypatch.setattr(container_sbom, "_run", record_run)

    container_sbom.generate_sbom(
        image="local/proxmox-sdk:test",
        platform="linux/amd64",
        emulator=emulator,
    )

    inventory_calls = [arguments for arguments in calls if arguments[:2] == ["docker", "run"]]
    assert len(inventory_calls) == 2
    for arguments in inventory_calls:
        assert "--volume" in arguments
        assert f"{emulator.resolve()}:/tmp/proxmox-sdk-sbom-emulator:ro" in arguments
        assert arguments.count("/tmp/proxmox-sdk-sbom-emulator") == 1
    assert inventory_calls[0][-4:] == ["/sbin/apk", "/sbin/apk", "list", "--installed"]
    assert inventory_calls[1][-4] == "/app/.venv/bin/python"
    assert inventory_calls[1][-3] == "/app/.venv/bin/python"

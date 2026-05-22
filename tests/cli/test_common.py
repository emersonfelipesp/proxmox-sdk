"""Tests for shared CLI helpers in :mod:`proxmox_cli.commands._common`."""

from __future__ import annotations

from typing import Any

import pytest

from proxmox_sdk.proxmox_cli.commands._common import build_backend_config


@pytest.fixture
def empty_ctx(tmp_path: Any) -> dict[str, Any]:
    """Ctx object pointing at a writable config dir (no config file present)."""
    return {"config": str(tmp_path / "nonexistent.toml")}


def test_use_mock_true_forces_mock_backend(empty_ctx: dict[str, Any]) -> None:
    cfg = build_backend_config(empty_ctx, use_mock=True)
    assert cfg.backend == "mock"


def test_mock_profile_flips_to_https_when_not_use_mock(empty_ctx: dict[str, Any]) -> None:
    empty_ctx["backend"] = "mock"
    cfg = build_backend_config(empty_ctx, use_mock=False)
    assert cfg.backend == "https"


def test_service_override_pins_service(empty_ctx: dict[str, Any]) -> None:
    empty_ctx["service"] = "PMG"
    cfg = build_backend_config(empty_ctx, use_mock=False, service="PVE")
    assert cfg.service == "PVE"


def test_service_none_preserves_profile_service(empty_ctx: dict[str, Any]) -> None:
    empty_ctx["service"] = "PBS"
    cfg = build_backend_config(empty_ctx, use_mock=False)
    assert cfg.service == "PBS"


def test_cli_overrides_apply(empty_ctx: dict[str, Any]) -> None:
    empty_ctx["host"] = "pve.example.com"
    empty_ctx["user"] = "root@pam"
    cfg = build_backend_config(empty_ctx, use_mock=False)
    assert cfg.host == "pve.example.com"
    assert cfg.user == "root@pam"

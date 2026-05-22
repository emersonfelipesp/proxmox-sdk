"""Tests for shared CLI helpers in :mod:`proxmox_cli.commands._common`."""

from __future__ import annotations

from typing import Any

import pytest

from proxmox_sdk.proxmox_cli.commands._common import build_backend_config, dispatch_request
from proxmox_sdk.proxmox_cli.exceptions import ProxmoxCLIError


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


class _FakeBridge:
    """Minimal bridge stub recording the method+args it was called with."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict[str, Any]]] = []

    def _record(self, verb: str) -> Any:
        def _call(path: str, **kwargs: Any) -> dict[str, Any]:
            self.calls.append((verb, path, kwargs))
            return {"verb": verb, "path": path, **kwargs}

        return _call

    def __getattr__(self, name: str) -> Any:
        if name in {"get", "post", "put", "delete", "patch"}:
            return self._record(name)
        raise AttributeError(name)


@pytest.mark.parametrize("verb", ["get", "post", "put", "delete", "patch"])
def test_dispatch_request_routes_to_matching_method(verb: str) -> None:
    bridge = _FakeBridge()
    result = dispatch_request(bridge, verb, "/nodes", params={"a": 1})  # type: ignore[arg-type]
    assert bridge.calls == [(verb, "/nodes", {"params": {"a": 1}})]
    assert result["verb"] == verb


def test_dispatch_request_is_case_insensitive() -> None:
    bridge = _FakeBridge()
    dispatch_request(bridge, "GET", "/nodes")  # type: ignore[arg-type]
    assert bridge.calls == [("get", "/nodes", {})]


def test_dispatch_request_unsupported_method_raises_cli_error() -> None:
    bridge = _FakeBridge()
    with pytest.raises(ProxmoxCLIError) as excinfo:
        dispatch_request(bridge, "options", "/nodes")  # type: ignore[arg-type]
    assert excinfo.value.exit_code == 2
    assert "options" in excinfo.value.message
    assert bridge.calls == []

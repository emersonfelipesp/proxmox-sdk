"""Tests for :class:`proxmox_sdk.proxmox_cli.sdk_bridge.ProxmoxSDKBridge`.

Covers the factory-based dispatch in :meth:`ProxmoxSDKBridge.create` for every
supported backend: ``mock`` is constructed end-to-end; the credential-required
backends (``https``, ``local``, ``ssh_paramiko``, ``openssh``) verify that the
correct kwargs are forwarded to :func:`ProxmoxSDK.sync` without coupling the
bridge to per-backend ``if/elif`` branches.
"""

from __future__ import annotations

from typing import Any

import pytest

from proxmox_sdk.proxmox_cli.config import BackendConfig
from proxmox_sdk.proxmox_cli.sdk_bridge import (
    _DEFAULT_HTTPS_PORTS,
    ProxmoxSDKBridge,
    _default_port,
)


def test_mock_backend_creates_bridge() -> None:
    """Mock backend must succeed without any credentials."""
    config = BackendConfig(name="mock-test", backend="mock", service="PVE")
    bridge = ProxmoxSDKBridge.create(config)
    try:
        assert bridge.sdk is not None
        assert bridge.sdk._sdk._backend_name == "mock"
    finally:
        bridge.close()


@pytest.mark.parametrize(
    ("backend", "expected_port"),
    [
        ("https", 8006),
        ("ssh_paramiko", 22),
        ("openssh", 22),
        ("mock", None),
        ("local", None),
    ],
)
def test_default_port_per_backend(backend: str, expected_port: int | None) -> None:
    assert _default_port(backend, "PVE") == expected_port


@pytest.mark.parametrize(
    ("service", "expected_port"),
    [("PVE", 8006), ("PMG", 8006), ("PBS", 8007), ("PDM", 8443)],
)
def test_default_https_port_per_service(service: str, expected_port: int) -> None:
    assert _DEFAULT_HTTPS_PORTS[service] == expected_port
    assert _default_port("https", service) == expected_port


def _capture_sync_kwargs(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """Patch ``ProxmoxSDK.sync`` to record the kwargs it receives."""
    captured: dict[str, Any] = {}

    from proxmox_sdk.sdk import api as api_module

    def fake_sync(**kwargs: Any) -> Any:
        captured.update(kwargs)

        class _Stub:
            def close(self) -> None:
                pass

        return _Stub()

    monkeypatch.setattr(api_module.ProxmoxSDK, "sync", classmethod(lambda cls, **kw: fake_sync(**kw)))
    return captured


def test_https_forwards_credentials_and_default_port(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = _capture_sync_kwargs(monkeypatch)
    config = BackendConfig(
        name="prod",
        backend="https",
        host="pve.example.com",
        user="admin@pam",
        token_name="cli",
        token_value="secret",
        service="PBS",
    )
    ProxmoxSDKBridge.create(config)
    assert captured["backend"] == "https"
    assert captured["host"] == "pve.example.com"
    assert captured["user"] == "admin@pam"
    assert captured["token_name"] == "cli"
    assert captured["token_value"] == "secret"
    assert captured["port"] == 8007  # PBS default
    assert captured["service"] == "PBS"


def test_https_defaults_to_localhost_when_host_missing(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = _capture_sync_kwargs(monkeypatch)
    config = BackendConfig(name="h", backend="https", user="root@pam", password="x")
    ProxmoxSDKBridge.create(config)
    assert captured["host"] == "localhost"


@pytest.mark.parametrize("backend", ["ssh_paramiko", "openssh"])
def test_ssh_backends_default_host_user_and_port(
    monkeypatch: pytest.MonkeyPatch, backend: str
) -> None:
    captured = _capture_sync_kwargs(monkeypatch)
    config = BackendConfig(name="ssh", backend=backend)
    ProxmoxSDKBridge.create(config)
    assert captured["backend"] == backend
    assert captured["host"] == "localhost"
    assert captured["user"] == "root"
    assert captured["port"] == 22


def test_local_backend_skips_host_user(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = _capture_sync_kwargs(monkeypatch)
    config = BackendConfig(name="loc", backend="local", service="PVE")
    ProxmoxSDKBridge.create(config)
    assert captured["backend"] == "local"
    assert captured["host"] is None
    assert captured["user"] is None
    assert captured["port"] is None


def test_explicit_port_overrides_default(monkeypatch: pytest.MonkeyPatch) -> None:
    captured = _capture_sync_kwargs(monkeypatch)
    config = BackendConfig(name="p", backend="https", host="h", port=9999)
    ProxmoxSDKBridge.create(config)
    assert captured["port"] == 9999

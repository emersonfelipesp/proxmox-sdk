"""Tests for the mode-dispatch registry in :mod:`proxmox_sdk.routes.modes`."""

from __future__ import annotations

import dataclasses
from collections.abc import Iterator
from typing import Any

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from proxmox_sdk.proxmox.config import ProxmoxConfig
from proxmox_sdk.routes.modes import MODE_REGISTRARS, register_mode


def test_mock_and_real_modes_are_registered() -> None:
    assert "mock" in MODE_REGISTRARS
    assert "real" in MODE_REGISTRARS


@pytest.fixture
def restore_registry() -> Iterator[None]:
    snapshot = dict(MODE_REGISTRARS)
    yield
    MODE_REGISTRARS.clear()
    MODE_REGISTRARS.update(snapshot)


def test_register_mode_decorator_adds_to_registry(restore_registry: None) -> None:
    @register_mode("custom-test-mode")
    def _registrar(
        app: FastAPI,
        config: ProxmoxConfig,
        *,
        version_tag: str,
        openapi_document: Any,
    ) -> dict[str, Any]:
        return {"mode": "custom-test-mode", "version_tag": version_tag}

    assert MODE_REGISTRARS["custom-test-mode"] is _registrar
    result = MODE_REGISTRARS["custom-test-mode"](
        FastAPI(),
        ProxmoxConfig.from_env(),
        version_tag="9.2",
        openapi_document={},
    )
    assert result == {"mode": "custom-test-mode", "version_tag": "9.2"}


def test_real_mode_missing_url_registers_error_endpoint() -> None:
    """When real-mode config is invalid, the registrar registers /api2/json."""
    app = FastAPI()
    config = ProxmoxConfig(
        api_mode="real",
        api_url="",  # missing — triggers ValueError
        token_id=None,
        token_secret=None,
        username=None,
        password=None,
        verify_ssl=True,
        service="PVE",
        backend="https",
    )

    info = MODE_REGISTRARS["real"](
        app,
        config,
        version_tag="latest",
        openapi_document={"openapi": "3.0.0", "paths": {}},
    )
    assert info == {}

    client = TestClient(app)
    response = client.get("/api2/json")
    assert response.status_code == 200
    payload = response.json()
    assert payload["error"] == "Invalid configuration for real API mode"
    assert "PROXMOX_API_URL" in payload["detail"]


def test_unknown_mode_in_main_falls_through_silently() -> None:
    """``_register_mode_routes`` should be a no-op for unknown modes."""
    from proxmox_sdk import main as main_module

    app = FastAPI()
    config = dataclasses.replace(ProxmoxConfig.from_env(), api_mode="nonexistent-mode")
    route_info: dict[str, Any] = {}

    main_module._register_mode_routes(
        app,
        config,
        route_info,
        version_tag="latest",
        openapi_doc={"openapi": "3.0.0", "paths": {}},
    )

    assert route_info == {}

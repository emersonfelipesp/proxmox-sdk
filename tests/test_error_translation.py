"""Tests for the route error-translation decorator."""

from __future__ import annotations

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

from proxmox_sdk.exception import ProxmoxOpenAPIException
from proxmox_sdk.routes._errors import with_error_translation


@pytest.mark.asyncio
async def test_passes_through_proxmox_openapi_exception() -> None:
    """A ProxmoxOpenAPIException raised inside the body is re-raised verbatim."""

    original = ProxmoxOpenAPIException(
        message="inner message",
        detail="inner detail",
        python_exception="ValueError('boom')",
    )

    @with_error_translation(
        method="GET",
        path_template="/api2/json/version",
        message_prefix="Test op",
    )
    async def endpoint() -> None:
        raise original

    with pytest.raises(ProxmoxOpenAPIException) as exc_info:
        await endpoint()

    assert exc_info.value is original
    assert exc_info.value.message == "inner message"
    assert exc_info.value.detail == "inner detail"


@pytest.mark.asyncio
async def test_passes_through_http_exception() -> None:
    """HTTPException must reach FastAPI's error handler unchanged."""

    @with_error_translation(
        method="POST",
        path_template="/api2/json/nodes",
        message_prefix="Test op",
    )
    async def endpoint() -> None:
        raise HTTPException(status_code=409, detail="conflict")

    with pytest.raises(HTTPException) as exc_info:
        await endpoint()

    assert exc_info.value.status_code == 409
    assert exc_info.value.detail == "conflict"


@pytest.mark.asyncio
async def test_wraps_generic_exception() -> None:
    """Generic exceptions become ProxmoxOpenAPIException with python_exception set."""

    @with_error_translation(
        method="GET",
        path_template="/api2/json/foo",
        message_prefix="Proxmox API request",
    )
    async def endpoint() -> None:
        raise ValueError("kaboom")

    with pytest.raises(ProxmoxOpenAPIException) as exc_info:
        await endpoint()

    err = exc_info.value
    assert err.message == "Proxmox API request failed for GET /api2/json/foo"
    assert err.detail is None
    assert err.python_exception == "kaboom"
    assert isinstance(err.__cause__, ValueError)


@pytest.mark.asyncio
async def test_wraps_with_fixed_detail() -> None:
    """The optional `detail` argument is attached verbatim; raw text goes to python_exception."""

    @with_error_translation(
        method="DELETE",
        path_template="/api2/json/nodes/{node}",
        message_prefix="Generated Proxmox mock route",
        detail="Schema-driven mock execution raised an unexpected exception.",
    )
    async def endpoint() -> None:
        raise RuntimeError("internal state corrupt")

    with pytest.raises(ProxmoxOpenAPIException) as exc_info:
        await endpoint()

    err = exc_info.value
    assert err.message == "Generated Proxmox mock route failed for DELETE /api2/json/nodes/{node}"
    assert err.detail == "Schema-driven mock execution raised an unexpected exception."
    assert err.python_exception == "internal state corrupt"


@pytest.mark.asyncio
async def test_passes_args_and_kwargs_through() -> None:
    """The wrapped coroutine still receives positional and keyword arguments."""

    captured: dict[str, object] = {}

    @with_error_translation(
        method="GET",
        path_template="/x",
        message_prefix="Op",
    )
    async def endpoint(value: int, *, label: str) -> str:
        captured["value"] = value
        captured["label"] = label
        return f"{label}:{value}"

    result = await endpoint(7, label="answer")
    assert result == "answer:7"
    assert captured == {"value": 7, "label": "answer"}


def _build_test_app() -> FastAPI:
    app = FastAPI()

    @app.get("/raises-generic")
    @with_error_translation(
        method="GET",
        path_template="/raises-generic",
        message_prefix="Test op",
    )
    async def raises_generic() -> dict[str, str]:
        raise ValueError("boom")

    @app.get("/raises-http")
    @with_error_translation(
        method="GET",
        path_template="/raises-http",
        message_prefix="Test op",
    )
    async def raises_http() -> dict[str, str]:
        raise HTTPException(status_code=418, detail="teapot")

    @app.get("/raises-proxmox")
    @with_error_translation(
        method="GET",
        path_template="/raises-proxmox",
        message_prefix="Test op",
    )
    async def raises_proxmox() -> dict[str, str]:
        raise ProxmoxOpenAPIException(
            message="inner",
            detail="inner detail",
            python_exception="x",
        )

    return app


def test_http_exception_reaches_fastapi_handler() -> None:
    """End-to-end: HTTPException flows through to FastAPI's response."""
    client = TestClient(_build_test_app())
    response = client.get("/raises-http")
    assert response.status_code == 418
    assert response.json() == {"detail": "teapot"}


def test_generic_exception_translated_to_500() -> None:
    """End-to-end: generic exceptions wrap into ProxmoxOpenAPIException and surface as 500."""
    client = TestClient(_build_test_app(), raise_server_exceptions=False)
    response = client.get("/raises-generic")
    assert response.status_code == 500


def test_proxmox_exception_passes_through_to_500() -> None:
    """End-to-end: an inner ProxmoxOpenAPIException is not re-wrapped."""
    client = TestClient(_build_test_app(), raise_server_exceptions=False)
    response = client.get("/raises-proxmox")
    assert response.status_code == 500

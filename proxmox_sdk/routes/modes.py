"""Mode-dispatch registry for the FastAPI app factory.

``main.py`` previously had a hard-coded ``if config.is_mock_mode(): ... elif
config.is_real_mode(): ...`` ladder that imported both transport modules and
called them by hand. That violated DIP: the app factory depended on every
concrete mode.

This module inverts the dependency: each mode self-registers a registrar
function under a string key; ``main.py`` just looks up
``MODE_REGISTRARS[config.api_mode]`` and calls it. Adding a new mode no longer
requires editing ``main.py``.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any, Protocol

if TYPE_CHECKING:
    from fastapi import FastAPI

    from proxmox_sdk.proxmox.config import ProxmoxConfig


class ModeRegistrar(Protocol):
    """Signature each mode registrar must satisfy."""

    def __call__(
        self,
        app: FastAPI,
        config: ProxmoxConfig,
        *,
        version_tag: str,
        openapi_document: Any,
    ) -> dict[str, Any]: ...


MODE_REGISTRARS: dict[str, ModeRegistrar] = {}


def register_mode(name: str) -> Callable[[ModeRegistrar], ModeRegistrar]:
    """Register *func* under ``MODE_REGISTRARS[name]``.

    Decorator form so mode modules can opt in declaratively::

        @register_mode("mock")
        def register_mock(app, config, *, version_tag, openapi_document): ...
    """

    def _decorator(func: ModeRegistrar) -> ModeRegistrar:
        MODE_REGISTRARS[name] = func
        return func

    return _decorator


@register_mode("mock")
def _register_mock_mode(
    app: FastAPI,
    config: ProxmoxConfig,  # noqa: ARG001
    *,
    version_tag: str,
    openapi_document: Any,
) -> dict[str, Any]:
    """Register in-memory mock CRUD routes generated from the OpenAPI document."""
    from proxmox_sdk.mock.routes import register_generated_proxmox_mock_routes

    return register_generated_proxmox_mock_routes(
        app,
        version_tag=version_tag,
        openapi_document=openapi_document,
    )


@register_mode("real")
def _register_real_mode(
    app: FastAPI,
    config: ProxmoxConfig,
    *,
    version_tag: str,
    openapi_document: Any,
) -> dict[str, Any]:
    """Register proxy-to-real-Proxmox routes; fall back to an error endpoint."""
    try:
        config.validate_for_real_mode()
    except ValueError as config_error:
        error_message = str(config_error)

        @app.get("/api2/json")
        async def config_error_endpoint() -> dict[str, str]:
            return {
                "error": "Invalid configuration for real API mode",
                "detail": error_message,
            }

        return {}

    from proxmox_sdk.proxmox.routes import register_generated_proxmox_real_routes

    return register_generated_proxmox_real_routes(
        app,
        version_tag=version_tag,
        openapi_document=openapi_document,
        proxmox_config=config,
    )


__all__ = ["MODE_REGISTRARS", "ModeRegistrar", "register_mode"]

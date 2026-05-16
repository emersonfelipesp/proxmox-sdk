"""Standalone FastAPI app for the schema-driven Proxmox mock API."""

from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI

from proxmox_sdk import __version__
from proxmox_sdk.mock.loader import load_mock_data
from proxmox_sdk.schema import DEFAULT_PROXMOX_OPENAPI_TAG, load_proxmox_generated_openapi

# Service variants that have no generated schema yet — return a healthy stub.
_STUB_SERVICES = frozenset({"pbs", "pdm"})


def create_mock_app() -> FastAPI:
    """Build the standalone Proxmox mock API app.

    Reads PROXMOX_MOCK_SERVICE (default: "all") to select which Proxmox service
    API variant this instance represents:
      - "pve" or "all": load the generated PVE OpenAPI schema (full mock).
      - "pbs" or "pdm": return a healthy stub — schemas not yet generated.
    """
    service = os.environ.get("PROXMOX_MOCK_SERVICE", "all").lower().strip()

    if service in _STUB_SERVICES:
        return _create_stub_app(service)

    version_tag = os.environ.get("PROXMOX_MOCK_SCHEMA_VERSION", DEFAULT_PROXMOX_OPENAPI_TAG)
    openapi_doc = load_proxmox_generated_openapi(version_tag=version_tag)

    app = FastAPI(
        title=f"Proxmox Mock API ({service.upper()})",
        description="Schema-driven in-memory FastAPI mock for the generated Proxmox API.",
        version=__version__,
    )

    @app.get("/")
    async def root() -> dict[str, Any]:
        return {
            "message": "Schema-driven Proxmox mock API",
            "service": service,
            "schema_version": version_tag,
            "package_version": __version__,
        }

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ready"}

    @app.get("/version")
    async def version() -> dict[str, str]:
        return {"version": __version__}

    custom_mock_data = load_mock_data()
    if custom_mock_data:
        if openapi_doc:
            from proxmox_sdk.mock.routes import register_generated_proxmox_mock_routes

            register_generated_proxmox_mock_routes(
                app,
                version_tag=version_tag,
                openapi_document=openapi_doc,
                custom_mock_data=custom_mock_data,
            )
            return app

        _register_static_mock_routes(app, custom_mock_data)
        return app

    if openapi_doc:
        from proxmox_sdk.mock.routes import register_generated_proxmox_mock_routes

        register_generated_proxmox_mock_routes(
            app, version_tag=version_tag, openapi_document=openapi_doc
        )
        return app

    @app.get("/api2/json")
    async def no_schema() -> dict[str, str]:
        return {
            "error": "No schema loaded",
            "message": f"Run /codegen/generate to generate version '{version_tag}' or use the full API server.",
        }

    return app


def _create_stub_app(service: str) -> FastAPI:
    """Return a healthy FastAPI stub for services without a generated schema yet."""
    service_upper = service.upper()
    app = FastAPI(
        title=f"Proxmox {service_upper} Mock API (stub)",
        description=(
            f"Stub mock for Proxmox {service_upper}. "
            f"A generated OpenAPI schema for {service_upper} does not exist yet. "
            "The container is healthy and forwards health/version checks; "
            "API routes will be added when the schema is available."
        ),
        version=__version__,
    )

    @app.get("/")
    async def root() -> dict[str, Any]:
        return {
            "message": f"Proxmox {service_upper} mock stub — schema not yet generated",
            "service": service,
            "package_version": __version__,
            "schema_status": "pending",
        }

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ready"}

    @app.get("/version")
    async def version() -> dict[str, str]:
        return {"version": __version__}

    return app


def _register_static_mock_routes(app: FastAPI, mock_data: dict[str, Any]) -> None:
    """Register static mock routes from custom mock data."""

    @app.get("/api2/json/{path:path}")
    async def static_mock_get(path: str) -> dict[str, Any]:
        full_path = f"/api2/json/{path}"
        return mock_data.get(full_path, {"error": "Not found"})

    @app.post("/api2/json/{path:path}")
    async def static_mock_post(path: str) -> dict[str, Any]:
        full_path = f"/api2/json/{path}"
        return mock_data.get(full_path, {"error": "Not found"})

    @app.put("/api2/json/{path:path}")
    async def static_mock_put(path: str) -> dict[str, Any]:
        full_path = f"/api2/json/{path}"
        return mock_data.get(full_path, {"error": "Not found"})

    @app.patch("/api2/json/{path:path}")
    async def static_mock_patch(path: str) -> dict[str, Any]:
        full_path = f"/api2/json/{path}"
        return mock_data.get(full_path, {"error": "Not found"})

    @app.delete("/api2/json/{path:path}")
    async def static_mock_delete(path: str) -> dict[str, Any]:
        full_path = f"/api2/json/{path}"
        return mock_data.get(full_path, {"error": "Not found"})

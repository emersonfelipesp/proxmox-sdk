"""Standalone FastAPI app for the schema-driven Proxmox mock API."""

from __future__ import annotations

import os
from typing import Any

from fastapi import FastAPI

from proxmox_openapi import __version__
from proxmox_openapi.schema import DEFAULT_PROXMOX_OPENAPI_TAG, load_proxmox_generated_openapi


def create_mock_app() -> FastAPI:
    """Build the standalone Proxmox mock API app."""

    version_tag = os.environ.get("PROXMOX_MOCK_SCHEMA_VERSION", DEFAULT_PROXMOX_OPENAPI_TAG)
    openapi_doc = load_proxmox_generated_openapi(version_tag=version_tag)

    app = FastAPI(
        title="Proxmox Mock API",
        description="Schema-driven in-memory FastAPI mock for the generated Proxmox API.",
        version=__version__,
    )

    @app.get("/")
    async def root() -> dict[str, Any]:
        return {
            "message": "Schema-driven Proxmox mock API",
            "schema_version": version_tag,
            "package_version": __version__,
        }

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ready"}

    @app.get("/version")
    async def version() -> dict[str, str]:
        return {"version": __version__}

    if openapi_doc:
        from proxmox_openapi.mock.routes import register_generated_proxmox_mock_routes

        register_generated_proxmox_mock_routes(
            app, version_tag=version_tag, openapi_document=openapi_doc
        )
    else:

        @app.get("/api2/json")
        async def no_schema() -> dict[str, str]:
            return {
                "error": "No schema loaded",
                "message": f"Run /codegen/generate to generate version '{version_tag}' or use the full API server.",
            }

    return app

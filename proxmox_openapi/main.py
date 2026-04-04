"""Proxmox OpenAPI main module - Full API with Swagger docs."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi import __version__ as fastapi_version

from proxmox_openapi import __version__
from proxmox_openapi.routes.codegen import router as codegen_router
from proxmox_openapi.routes.mock import router as mock_router
from proxmox_openapi.routes.versions import router as versions_router


def create_app() -> FastAPI:
    """Build the Proxmox OpenAPI FastAPI application."""
    app = FastAPI(
        title="Proxmox OpenAPI",
        description=(
            "Schema-driven FastAPI package for Proxmox API: "
            "OpenAPI generation from Proxmox API Viewer, mock data, and in-memory CRUD operations."
        ),
        version=__version__,
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    @app.get("/")
    async def root() -> dict[str, str]:
        return {
            "message": "Proxmox OpenAPI",
            "version": __version__,
            "docs": "/docs",
        }

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ready"}

    @app.get("/version")
    async def version() -> dict[str, str]:
        return {
            "version": __version__,
            "fastapi": fastapi_version,
        }

    app.include_router(codegen_router, prefix="/codegen", tags=["codegen"])
    app.include_router(mock_router, prefix="/mock", tags=["mock"])
    app.include_router(versions_router, prefix="/versions", tags=["versions"])

    return app


app = create_app()

__all__ = ["app", "create_app"]

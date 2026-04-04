"""Routes for mock API endpoints."""

from __future__ import annotations

import os

from fastapi import APIRouter

from proxmox_openapi import __version__
from proxmox_openapi.schema import DEFAULT_PROXMOX_OPENAPI_TAG

router = APIRouter()


@router.get("/")
async def root():
    return {
        "message": "Proxmox OpenAPI Mock Server",
        "version": __version__,
        "docs": "/mock/docs",
    }


@router.get("/health")
async def health():
    return {"status": "ready"}


@router.get("/version")
async def version():
    return {"version": __version__}


__all__ = ["router"]

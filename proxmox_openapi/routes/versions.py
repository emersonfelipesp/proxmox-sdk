"""Routes for version management endpoints."""

from fastapi import APIRouter

from proxmox_openapi.schema import DEFAULT_PROXMOX_OPENAPI_TAG, available_proxmox_openapi_versions

router = APIRouter()


@router.get("/")
async def list_versions():
    """List available Proxmox OpenAPI versions."""
    versions = available_proxmox_openapi_versions()
    return {
        "versions": versions,
        "latest": DEFAULT_PROXMOX_OPENAPI_TAG,
        "count": len(versions),
    }


@router.get("/latest")
async def get_latest_version():
    """Get the latest version tag."""
    return {
        "version": DEFAULT_PROXMOX_OPENAPI_TAG,
    }


__all__ = ["router"]

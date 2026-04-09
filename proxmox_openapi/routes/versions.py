"""Routes for version management endpoints."""

from fastapi import APIRouter, Query

from proxmox_openapi.schema import DEFAULT_PROXMOX_OPENAPI_TAG, available_proxmox_openapi_versions

router = APIRouter()


@router.get("/")
async def list_versions(
    service: str = Query(default="PVE", description="Proxmox service type: PVE or PBS."),
) -> dict[str, object]:
    """List available Proxmox OpenAPI versions."""
    versions = available_proxmox_openapi_versions(service=service.upper())
    return {
        "service": service.upper(),
        "versions": versions,
        "latest": DEFAULT_PROXMOX_OPENAPI_TAG,
        "count": len(versions),
    }


@router.get("/latest")
async def get_latest_version() -> dict[str, str]:
    """Get the latest version tag."""
    return {
        "version": DEFAULT_PROXMOX_OPENAPI_TAG,
    }


__all__ = ["router"]

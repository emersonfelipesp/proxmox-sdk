"""Routes for codegen endpoints."""

from __future__ import annotations

import logging
import os
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import PlainTextResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from proxmox_sdk.proxmox_codegen.apidoc_parser import SERVICE_URLS
from proxmox_sdk.proxmox_codegen.pipeline import (
    LATEST_VERSION_TAG,
    generate_proxmox_codegen_bundle_async,
)
from proxmox_sdk.proxmox_codegen.security import (
    SSRFProtectionError,
    validate_source_url,
    validate_version_tag,
)
from proxmox_sdk.rate_limit import limiter

audit_logger = logging.getLogger("audit")
security = HTTPBearer(auto_error=False)


def verify_codegen_auth(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
) -> None:
    """Verify that the request is authorized to perform codegen operations."""
    api_key = os.environ.get("CODEGEN_API_KEY")
    if not api_key:
        audit_logger.warning("Unauthorized access attempt to /codegen: CODEGEN_API_KEY not set")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CODEGEN_API_KEY environment variable must be set to use codegen endpoints",
        )

    if not credentials or credentials.credentials != api_key:
        audit_logger.warning("Failed authentication attempt to /codegen")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key for codegen operations",
        )


router = APIRouter(dependencies=[Depends(verify_codegen_auth)])


_VALID_SERVICES = frozenset(SERVICE_URLS.keys())
_SERVICE_GENERATED_SUBDIRS = {"PVE": "proxmox", "PBS": "pbs"}


def _validate_service(service: str) -> str:
    """Validate and normalise a service identifier."""
    upper = service.upper()
    if upper not in _VALID_SERVICES:
        raise ValueError(f"service must be one of {sorted(_VALID_SERVICES)}, got {service!r}")
    return upper


@router.post("/generate")
@limiter.limit("1/hour")
async def generate_viewer_codegen_artifacts(
    request: Request,
    service: str = Query(
        default="PVE",
        description="Proxmox service type to generate: PVE or PBS.",
    ),
    persist: bool = Query(
        default=True,
        description="Persist generated artifacts under proxmox_sdk/generated/<service>.",
    ),
    workers: int = Query(
        default=10,
        ge=1,
        le=32,
        description="Async worker count for parallel endpoint capture.",
    ),
    retry_count: int = Query(
        default=2,
        ge=0,
        le=10,
        description="Retry attempts per endpoint for transient Playwright failures.",
    ),
    retry_backoff: float = Query(
        default=0.35,
        ge=0.0,
        le=5.0,
        description="Base exponential backoff seconds between retries.",
    ),
    checkpoint_every: int = Query(
        default=50,
        ge=1,
        le=500,
        description="Write crawl checkpoint after this many processed endpoints.",
    ),
    source_url: str | None = Query(
        default=None,
        description="Proxmox API viewer URL to crawl. Defaults to the official URL for the selected service.",
    ),
    version_tag: str = Query(
        default=LATEST_VERSION_TAG,
        description="Version tag used for generated artifacts subdirectory.",
    ),
) -> dict[str, object]:
    """Run Proxmox API Viewer to OpenAPI and Pydantic generation pipeline."""
    try:
        service = _validate_service(service)
        if source_url is not None:
            source_url = validate_source_url(source_url)
        version_tag = validate_version_tag(version_tag)
    except SSRFProtectionError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    audit_logger.info(
        "codegen_request",
        extra={
            "client_ip": request.client.host if request.client else "unknown",
            "service": service,
            "source_url": source_url,
            "version_tag": version_tag,
            "workers": workers,
        },
    )

    output_dir = None
    if persist:
        subdir = _SERVICE_GENERATED_SUBDIRS.get(service, "proxmox")
        output_dir = Path(__file__).resolve().parents[2] / "generated" / subdir

    bundle = await generate_proxmox_codegen_bundle_async(
        output_dir=output_dir,
        service=service,
        source_url=source_url,
        version_tag=version_tag,
        worker_count=workers,
        retry_count=retry_count,
        retry_backoff_seconds=retry_backoff,
        checkpoint_every=checkpoint_every,
    )

    viewer_capture = bundle.capture.get("viewer", {})
    completeness = bundle.capture.get("completeness", {})

    return {
        "message": "Generation completed",
        "source_url": bundle.source_url,
        "version_tag": bundle.version_tag,
        "generated_at": bundle.generated_at,
        "endpoint_count": bundle.endpoint_count,
        "operation_count": bundle.operation_count,
        "viewer": {
            "endpoint_count": viewer_capture.get("endpoint_count"),
            "navigation_items": viewer_capture.get("discovered_navigation_items"),
            "method_count": viewer_capture.get("method_count"),
            "duration_seconds": viewer_capture.get("duration_seconds"),
            "worker_count": viewer_capture.get("worker_count"),
            "failed_endpoint_count": viewer_capture.get("failed_endpoint_count"),
        },
        "completeness": {
            "fallback_method_count": completeness.get("fallback_method_count"),
            "missing_from_viewer": len(completeness.get("missing_from_viewer", [])),
        },
        "output_dir": str(Path(output_dir) / bundle.version_tag) if output_dir else None,
        "retry": {
            "retry_count": retry_count,
            "retry_backoff": retry_backoff,
            "checkpoint_every": checkpoint_every,
        },
    }


@router.get("/openapi")
@limiter.limit("5/hour")
async def proxmox_viewer_openapi(
    request: Request,
    service: str = Query(default="PVE", description="Proxmox service type: PVE or PBS."),
    regenerate: bool = Query(
        default=False,
        description="Regenerate from upstream viewer before returning OpenAPI output.",
    ),
    workers: int = Query(
        default=10,
        ge=1,
        le=32,
        description="Async worker count used when regeneration is requested.",
    ),
    version_tag: str = Query(
        default=LATEST_VERSION_TAG,
        description="Generated artifact version tag to load.",
    ),
) -> dict[str, object]:
    """Return generated OpenAPI schema for Proxmox API viewer endpoints."""
    from proxmox_sdk.schema import load_proxmox_generated_openapi

    try:
        service = _validate_service(service)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if regenerate:
        subdir = _SERVICE_GENERATED_SUBDIRS.get(service, "proxmox")
        output_dir = Path(__file__).resolve().parents[2] / "generated" / subdir
        bundle = await generate_proxmox_codegen_bundle_async(
            output_dir=output_dir,
            service=service,
            version_tag=version_tag,
            worker_count=workers,
        )
        return bundle.openapi

    schema = load_proxmox_generated_openapi(version_tag=version_tag, service=service)
    if schema:
        return schema

    return {
        "error": "Schema not found",
        "message": f"Run /codegen/generate?service={service} first to generate version '{version_tag}'",
    }


@router.get("/pydantic", response_class=PlainTextResponse)
@limiter.limit("5/hour")
async def proxmox_viewer_pydantic_models(
    request: Request,
    service: str = Query(default="PVE", description="Proxmox service type: PVE or PBS."),
    regenerate: bool = Query(
        default=False,
        description="Regenerate from upstream viewer before returning model source.",
    ),
    version_tag: str = Query(
        default=LATEST_VERSION_TAG,
        description="Generated artifact version tag to load.",
    ),
) -> str:
    """Return generated Pydantic v2 models source code for Proxmox API endpoints."""
    from proxmox_sdk.schema import load_pydantic_models

    try:
        service = _validate_service(service)
        version_tag = validate_version_tag(version_tag)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    if regenerate:
        subdir = _SERVICE_GENERATED_SUBDIRS.get(service, "proxmox")
        output_dir = Path(__file__).resolve().parents[2] / "generated" / subdir
        bundle = await generate_proxmox_codegen_bundle_async(
            output_dir=output_dir,
            service=service,
            version_tag=version_tag,
        )
        return bundle.pydantic_models_code

    models = load_pydantic_models(version_tag=version_tag, service=service)
    if models:
        return models

    return f"# Pydantic models for {service} version {version_tag} not found. Run /codegen/generate?service={service} first."


@router.get("/versions")
async def list_available_versions(
    service: str = Query(default="PVE", description="Proxmox service type: PVE or PBS."),
) -> dict[str, object]:
    """List available Proxmox OpenAPI versions."""
    from proxmox_sdk.schema import available_proxmox_sdk_versions

    try:
        service = _validate_service(service)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e

    versions = available_proxmox_sdk_versions(service=service)
    return {
        "service": service,
        "versions": versions,
        "latest": LATEST_VERSION_TAG,
    }


__all__ = ["router"]

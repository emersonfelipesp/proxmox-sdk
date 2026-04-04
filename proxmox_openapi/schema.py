"""Schema management for Proxmox OpenAPI."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_PROXMOX_OPENAPI_TAG = "latest"


def _generated_dir() -> Path:
    """Return the generated artifacts directory."""
    return Path(__file__).resolve().parent / "generated" / "proxmox"


def available_proxmox_openapi_versions() -> list[str]:
    """Return list of available Proxmox OpenAPI version tags."""
    generated = _generated_dir()
    if not generated.exists():
        return []

    versions = []
    for item in generated.iterdir():
        if item.is_dir() and (item / "openapi.json").exists():
            versions.append(item.name)

    return sorted(versions, key=lambda v: (0 if v == DEFAULT_PROXMOX_OPENAPI_TAG else 1, v))


def load_proxmox_generated_openapi(
    version_tag: str = DEFAULT_PROXMOX_OPENAPI_TAG,
) -> dict[str, Any] | None:
    """Load generated OpenAPI schema for a specific version tag."""
    openapi_path = _generated_dir() / version_tag / "openapi.json"
    if not openapi_path.exists():
        return None

    try:
        return json.loads(openapi_path.read_text(encoding="utf-8"))
    except Exception:
        return None


def load_pydantic_models(version_tag: str = DEFAULT_PROXMOX_OPENAPI_TAG) -> str | None:
    """Load generated Pydantic models for a specific version tag."""
    models_path = _generated_dir() / version_tag / "pydantic_models.py"
    if not models_path.exists():
        return None

    try:
        return models_path.read_text(encoding="utf-8")
    except Exception:
        return None


__all__ = [
    "DEFAULT_PROXMOX_OPENAPI_TAG",
    "available_proxmox_openapi_versions",
    "load_proxmox_generated_openapi",
    "load_pydantic_models",
]

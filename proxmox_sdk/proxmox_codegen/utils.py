"""Shared utility helpers for Proxmox code generation."""

from __future__ import annotations

import json
import keyword
import re
from datetime import UTC, datetime
from pathlib import Path


def utc_now_iso() -> str:
    """Return deterministic UTC timestamp string for generated artifacts."""

    return datetime.now(UTC).isoformat()


def ensure_parent(path: Path) -> None:
    """Ensure the parent directory exists for a file path."""

    path.parent.mkdir(parents=True, exist_ok=True)


def dump_json(path: Path, data: object) -> None:
    """Write JSON artifact with stable formatting."""

    ensure_parent(path)
    path.write_text(json.dumps(data, indent=2, sort_keys=True), encoding="utf-8")


def slugify_identifier(value: str) -> str:
    """Convert arbitrary text to a Python-safe snake_case identifier."""

    out = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip())
    out = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", out)
    out = out.strip("_").lower()
    if not out:
        return "field"
    if out[0].isdigit():
        out = f"n_{out}"
    if keyword.iskeyword(out):
        out = f"{out}_"
    return out


def pascal_case(value: str) -> str:
    """Convert input text to PascalCase identifier."""

    parts = re.split(r"[^a-zA-Z0-9]+", value)
    words = [w for w in parts if w]
    if not words:
        return "GeneratedModel"
    label = "".join(w[0].upper() + w[1:] for w in words)
    if label[0].isdigit():
        label = f"Model{label}"
    return label


def extract_path_params(path: str) -> list[str]:
    """Extract ordered path parameter names from Proxmox style path."""

    return re.findall(r"\{([^{}]+)\}", path)


def to_openapi_path(path: str) -> str:
    """Return normalized OpenAPI path (currently same placeholder syntax)."""

    if not path.startswith("/"):
        return "/" + path
    return path


__all__ = [
    "utc_now_iso",
    "ensure_parent",
    "dump_json",
    "slugify_identifier",
    "pascal_case",
    "extract_path_params",
    "to_openapi_path",
]

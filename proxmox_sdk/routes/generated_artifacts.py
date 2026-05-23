"""Load generated route metadata and lazy Pydantic model shards."""

from __future__ import annotations

import importlib.util
import json
import sys
from functools import lru_cache
from pathlib import Path
from types import ModuleType
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from proxmox_sdk.proxmox_codegen.security import validate_version_tag


def _generated_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "generated" / "proxmox"


def _tag_dir(version_tag: str) -> Path:
    return _generated_dir() / validate_version_tag(version_tag)


def _load_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def load_route_metadata(version_tag: str) -> dict[str, Any] | None:
    """Load generated runtime route metadata for *version_tag*."""

    return _load_json(_tag_dir(version_tag) / "route_metadata.json")


@lru_cache(maxsize=16)
def _load_model_index(version_tag: str) -> dict[str, Any] | None:
    return _load_json(_tag_dir(version_tag) / "model_index.json")


@lru_cache(maxsize=64)
def _load_model_module(version_tag: str, group: str) -> ModuleType | None:
    tag = validate_version_tag(version_tag)
    safe_group = "".join(ch if ch.isalnum() or ch == "_" else "_" for ch in group)
    path = _tag_dir(tag) / "models" / f"{safe_group}.py"
    module_name = f"proxmox_sdk._generated_models.{tag.replace('.', '_')}.{safe_group}"

    if not path.exists():
        path = _tag_dir(tag) / "pydantic_models.py"
        module_name = f"proxmox_sdk._generated_models.{tag.replace('.', '_')}.aggregate"

    existing = sys.modules.get(module_name)
    if existing is not None:
        return existing

    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        return None

    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    for value in module.__dict__.values():
        if (
            isinstance(value, type)
            and getattr(value, "__module__", None) == module.__name__
            and hasattr(value, "model_rebuild")
        ):
            value.model_rebuild(_types_namespace=module.__dict__)
    return module


def load_operation_model(
    version_tag: str,
    operation_id: str,
    role: str,
    *,
    group: str | None = None,
    model_name: str | None = None,
) -> type | None:
    """Return a lazy-loaded request or response model for an operation."""

    resolved_group = group
    resolved_model_name = model_name
    index = _load_model_index(version_tag)
    if index is not None:
        operation_entry = (index.get("operations") or {}).get(operation_id)
        if isinstance(operation_entry, dict):
            resolved_group = str(operation_entry.get("group") or resolved_group or "")
            key = "request_model" if role == "request" else "response_model"
            entry_model = operation_entry.get(key)
            if isinstance(entry_model, str):
                resolved_model_name = entry_model

    if not resolved_group or not resolved_model_name:
        return None

    module = _load_model_module(version_tag, resolved_group)
    if module is None:
        return None
    model = getattr(module, resolved_model_name, None)
    return model if isinstance(model, type) else None


def install_generated_openapi(app: FastAPI, openapi_document: dict[str, Any]) -> None:
    """Merge bundled generated Proxmox OpenAPI paths into FastAPI docs output."""

    documents = getattr(app.state, "_proxmox_generated_openapi_documents", None)
    if documents is None:
        documents = []
        app.state._proxmox_generated_openapi_documents = documents
    if openapi_document not in documents:
        documents.append(openapi_document)

    def custom_openapi() -> dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=app.description,
            routes=app.routes,
        )
        paths = schema.setdefault("paths", {})
        for document in app.state._proxmox_generated_openapi_documents:
            base_prefix = _server_prefix(document)
            for path_template, path_item in (document.get("paths") or {}).items():
                if not isinstance(path_template, str) or not isinstance(path_item, dict):
                    continue
                mounted_path = f"{base_prefix}{path_template}" if base_prefix else path_template
                paths[mounted_path] = path_item
        app.openapi_schema = schema
        return app.openapi_schema

    app.openapi = custom_openapi  # type: ignore[method-assign]
    app.openapi_schema = None


def _server_prefix(openapi_document: dict[str, Any]) -> str:
    servers = openapi_document.get("servers")
    if isinstance(servers, list) and servers:
        first = servers[0]
        if isinstance(first, dict) and isinstance(first.get("url"), str):
            return first["url"].rstrip("/")
    return ""


__all__ = [
    "install_generated_openapi",
    "load_operation_model",
    "load_route_metadata",
]

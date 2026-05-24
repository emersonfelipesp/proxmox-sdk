"""Generated route metadata for runtime FastAPI route registration."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any

from proxmox_sdk.proxmox_codegen.utils import (
    extract_path_params,
    pascal_case,
    slugify_identifier,
)

SUPPORTED_METHODS: frozenset[str] = frozenset({"GET", "POST", "PUT", "PATCH", "DELETE"})


def _server_prefix(openapi_document: dict[str, object]) -> str:
    servers = openapi_document.get("servers")
    if isinstance(servers, list) and servers:
        first = servers[0]
        if isinstance(first, dict) and isinstance(first.get("url"), str):
            return first["url"].rstrip("/")  # type: ignore[return-value]
    return ""


def _response_schema(operation: dict[str, object]) -> dict[str, Any] | None:
    schema = (
        operation.get("responses", {})
        .get("200", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema")
    )
    return deepcopy(schema) if isinstance(schema, dict) else None


def _request_schema(
    path_template: str,
    operation: dict[str, object],
) -> dict[str, Any] | None:
    schema = (
        operation.get("requestBody", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema")
    )
    if not isinstance(schema, dict):
        return None

    path_param_names = set(extract_path_params(path_template))
    if not path_param_names:
        return deepcopy(schema)

    filtered = deepcopy(schema)
    properties = filtered.get("properties")
    if isinstance(properties, dict):
        filtered["properties"] = {
            name: value for name, value in properties.items() if name not in path_param_names
        }
    required = filtered.get("required")
    if isinstance(required, list):
        filtered["required"] = [name for name in required if name not in path_param_names]
    return filtered


def _operation_parameters(operation: dict[str, object]) -> list[dict[str, object]]:
    parameters = operation.get("parameters")
    if not isinstance(parameters, list):
        return []
    return [p for p in parameters if isinstance(p, dict)]


def _path_parameter_name_map(operation: dict[str, object]) -> dict[str, str]:
    used_names: set[str] = {"request_body"}
    mapping: dict[str, str] = {}

    for parameter in _operation_parameters(operation):
        if parameter.get("in") != "path":
            continue
        original_name = parameter.get("name")
        if not isinstance(original_name, str):
            continue

        python_name = slugify_identifier(original_name)
        if python_name in used_names:
            candidate = f"op_{python_name}"
            suffix = 1
            while candidate in used_names:
                candidate = f"op_{python_name}_{suffix}"
                suffix += 1
            python_name = candidate

        used_names.add(python_name)
        mapping[original_name] = python_name

    return mapping


def _mounted_fastapi_path(path_template: str, operation: dict[str, object]) -> str:
    mounted = path_template
    for original, python in _path_parameter_name_map(operation).items():
        mounted = mounted.replace(f"{{{original}}}", f"{{{python}}}")
    return mounted


def _operation_id(path_template: str, method: str, operation: dict[str, object]) -> str:
    value = operation.get("operationId")
    return value if isinstance(value, str) else f"{method.lower()}_{path_template}"


def _schema_kind(schema: dict[str, Any] | None) -> str:
    resolved = _resolved_schema(schema)
    if not resolved:
        return "none"
    schema_type = resolved.get("type")
    if schema_type == "array":
        return "array"
    if schema_type == "object":
        return "object"
    if schema_type is None and isinstance(resolved.get("properties"), dict):
        return "object"
    return "scalar"


def _deep_merge(base: Any, override: Any) -> Any:
    if isinstance(base, dict) and isinstance(override, dict):
        merged = deepcopy(base)
        for key, value in override.items():
            if key in merged:
                merged[key] = _deep_merge(merged[key], value)
            else:
                merged[key] = deepcopy(value)
        return merged
    return deepcopy(override)


def _resolved_schema(schema: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(schema, dict):
        return {}
    if isinstance(schema.get("allOf"), list) and schema["allOf"]:
        merged: dict[str, Any] = {}
        for branch in schema["allOf"]:
            merged = _deep_merge(
                merged, _resolved_schema(branch if isinstance(branch, dict) else {})
            )
        return merged
    for keyword in ("oneOf", "anyOf"):
        branches = schema.get(keyword)
        if isinstance(branches, list):
            for branch in branches:
                branch_schema = _resolved_schema(branch if isinstance(branch, dict) else {})
                if branch_schema.get("type") != "null":
                    return branch_schema
    return deepcopy(schema)


def _build_direct_child_index(
    path_items: dict[str, dict[str, object]],
) -> dict[str, tuple[str, str, dict[str, Any] | None]]:
    children: dict[str, list[tuple[str, str, dict[str, Any] | None]]] = {}
    for candidate_template, candidate_item in path_items.items():
        segments = candidate_template.rsplit("/", 1)
        if len(segments) != 2:
            continue
        parent_template, suffix = segments
        if not suffix.startswith("{") or not suffix.endswith("}"):
            continue
        get_operation = candidate_item.get("get")
        if not isinstance(get_operation, dict):
            continue
        parameter_name = suffix[1:-1]
        parameter_schema = None
        for parameter in _operation_parameters(get_operation):
            if parameter.get("in") == "path" and parameter.get("name") == parameter_name:
                if isinstance(parameter.get("schema"), dict):
                    parameter_schema = deepcopy(parameter["schema"])
                break
        children.setdefault(parent_template, []).append(
            (candidate_template, parameter_name, parameter_schema)
        )
    return {
        parent: sorted(candidates, key=lambda item: item[0])[0]
        for parent, candidates in children.items()
    }


def _parent_collection_template(
    path_template: str,
    path_items: dict[str, dict[str, object]],
) -> tuple[str | None, dict[str, Any] | None]:
    segments = path_template.split("/")
    if len(segments) < 2 or not segments[-1].startswith("{") or not segments[-1].endswith("}"):
        return None, None
    parent_template = "/".join(segments[:-1])
    parent_item = path_items.get(parent_template)
    if not isinstance(parent_item, dict):
        return None, None
    parent_get = parent_item.get("get")
    if not isinstance(parent_get, dict):
        return None, None
    schema = _response_schema(parent_get)
    resolved = _resolved_schema(schema)
    if resolved.get("type") != "array":
        return None, None
    item_schema = resolved.get("items") if isinstance(resolved.get("items"), dict) else None
    return parent_template, deepcopy(item_schema) if isinstance(item_schema, dict) else None


def _model_group(path_template: str) -> str:
    parts = [part for part in path_template.split("/") if part]
    if not parts:
        return "root"
    return slugify_identifier(parts[0].strip("{}")) or "root"


def _request_model_name(
    path_template: str,
    operation: dict[str, object],
    operation_id: str,
) -> str | None:
    req_schema = _request_schema(path_template, operation)
    if not isinstance(req_schema, dict):
        return None
    properties = req_schema.get("properties")
    if not isinstance(properties, dict) or not properties:
        return None
    return f"{pascal_case(operation_id)}Request"


def _response_model_name(operation_id: str, response_schema: dict[str, Any] | None) -> str | None:
    return f"{pascal_case(operation_id)}Response" if isinstance(response_schema, dict) else None


def _parameter_metadata(operation: dict[str, object]) -> list[dict[str, object]]:
    path_name_map = _path_parameter_name_map(operation)
    used_names: set[str] = set()
    parameters: list[dict[str, object]] = []

    def unique_name(base: str) -> str:
        candidate = base
        suffix = 1
        while candidate in used_names:
            candidate = f"{base}_{suffix}"
            suffix += 1
        return candidate

    for parameter in _operation_parameters(operation):
        location = parameter.get("in")
        original_name = parameter.get("name")
        if location not in {"path", "query"} or not isinstance(original_name, str):
            continue

        python_name = (
            path_name_map[original_name]
            if location == "path" and original_name in path_name_map
            else slugify_identifier(original_name)
        )
        if python_name in used_names:
            python_name = unique_name(f"op_{python_name}")
        used_names.add(python_name)

        parameters.append(
            {
                "in": location,
                "name": original_name,
                "python_name": python_name,
                "required": bool(parameter.get("required")),
                "schema": deepcopy(parameter.get("schema"))
                if isinstance(parameter.get("schema"), dict)
                else {},
                "description": parameter.get("description")
                if isinstance(parameter.get("description"), str)
                else None,
            }
        )

    return parameters


def _source_sha256(openapi: dict[str, object]) -> str:
    payload = json.dumps(openapi, indent=2, sort_keys=True)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def generate_route_metadata(
    openapi: dict[str, object],
    *,
    version_tag: str | None = None,
    source_sha256: str | None = None,
    generated_at: str | None = None,
) -> dict[str, object]:
    """Generate runtime route metadata from a generated OpenAPI document."""

    info = openapi.get("info") if isinstance(openapi, dict) else {}
    resolved_version = (
        version_tag or (info.get("version") if isinstance(info, dict) else None) or "latest"
    )
    base_prefix = _server_prefix(openapi)
    path_items = {
        path_template: path_item
        for path_template, path_item in (openapi.get("paths") or {}).items()
        if isinstance(path_item, dict)
    }
    direct_child_index = _build_direct_child_index(path_items)
    routes: list[dict[str, object]] = []

    for path_template, path_item in sorted(path_items.items()):
        for method, operation in sorted(path_item.items()):
            method_name = method.upper()
            if method_name not in SUPPORTED_METHODS or not isinstance(operation, dict):
                continue

            same_path_get = path_items.get(path_template, {}).get("get")
            same_path_get_schema = (
                _response_schema(same_path_get) if isinstance(same_path_get, dict) else None
            )
            direct_child_template, direct_child_param, direct_child_param_schema = (
                direct_child_index.get(path_template, (None, None, None))
            )
            parent_collection_template, parent_collection_item_schema = _parent_collection_template(
                path_template,
                path_items,
            )
            operation_id = _operation_id(path_template, method_name, operation)
            response_schema = _response_schema(operation)
            group = _model_group(path_template)

            routes.append(
                {
                    "path_template": path_template,
                    "absolute_path_template": f"{base_prefix}{path_template}",
                    "mounted_path": f"{base_prefix}{_mounted_fastapi_path(path_template, operation)}",
                    "method": method_name,
                    "operation_id": operation_id,
                    "route_name": f"generated_proxmox__{method_name.lower()}__{operation_id}",
                    "summary": operation.get("summary")
                    if isinstance(operation.get("summary"), str)
                    else None,
                    "description": operation.get("description")
                    if isinstance(operation.get("description"), str)
                    else None,
                    "parameters": _parameter_metadata(operation),
                    "request_schema": _request_schema(path_template, operation),
                    "response_schema": response_schema,
                    "request_model": _request_model_name(path_template, operation, operation_id),
                    "response_model": _response_model_name(operation_id, response_schema),
                    "model_group": group,
                    "same_path_get_schema": same_path_get_schema,
                    "same_path_get_kind": _schema_kind(same_path_get_schema),
                    "direct_child_template": direct_child_template,
                    "absolute_direct_child_template": (
                        f"{base_prefix}{direct_child_template}" if direct_child_template else None
                    ),
                    "direct_child_param": direct_child_param,
                    "direct_child_param_schema": direct_child_param_schema,
                    "parent_collection_template": parent_collection_template,
                    "absolute_parent_collection_template": (
                        f"{base_prefix}{parent_collection_template}"
                        if parent_collection_template
                        else None
                    ),
                    "parent_collection_item_schema": parent_collection_item_schema,
                }
            )

    return {
        "version_tag": resolved_version,
        "schema_version": info.get("version", resolved_version)
        if isinstance(info, dict)
        else resolved_version,
        "generated_at": generated_at or "",
        "source_sha256": source_sha256 or _source_sha256(openapi),
        "base_prefix": base_prefix or "/",
        "path_count": len(path_items),
        "route_count": len(routes),
        "method_count": len(routes),
        "routes": routes,
    }


__all__ = ["SUPPORTED_METHODS", "generate_route_metadata"]

"""Normalization layer from Proxmox API Viewer captures into OpenAPI-ready operations."""

from __future__ import annotations

from copy import deepcopy

from proxmox_openapi.proxmox_codegen.models import HTTP_METHODS, NormalizedOperation
from proxmox_openapi.proxmox_codegen.utils import extract_path_params, slugify_identifier


def _is_optional(value: object) -> bool:
    """Return True when Proxmox optional marker denotes optional fields."""

    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes"}
    return False


def _to_bool(value: object) -> bool:
    """Convert common Proxmox truthy/falsy markers to bool."""

    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        v = value.strip().lower()
        if v in {"1", "true", "yes", "on"}:
            return True
        if v in {"0", "false", "no", "off", ""}:
            return False
    return bool(value)


def _normalize_schema(schema: dict[str, object] | None) -> dict[str, object] | None:  # noqa: C901
    """Normalize Proxmox method parameter/returns schema to JSON-schema compatible form."""

    if schema is None:
        return None

    obj = deepcopy(schema)
    if not isinstance(obj, dict):
        return {"type": "string", "x-proxmox-original": obj}

    additional = obj.get("additionalProperties")
    if isinstance(additional, (int, str, bool)):
        obj["additionalProperties"] = _to_bool(additional)

    if "properties" in obj and isinstance(obj["properties"], dict):
        required = []
        for name, pdef in obj["properties"].items():
            if not isinstance(pdef, dict):
                continue
            optional = pdef.get("optional")
            if not _is_optional(optional):
                required.append(name)
            if "additionalProperties" in pdef and isinstance(
                pdef["additionalProperties"], (int, str, bool)
            ):
                pdef["additionalProperties"] = _to_bool(pdef["additionalProperties"])

        if required:
            obj["required"] = sorted(set(required))

    schema_type = obj.get("type")
    if not schema_type:
        if "items" in obj:
            obj["type"] = "array"
        elif "properties" in obj:
            obj["type"] = "object"

    return obj


def _operation_id(path: str, method: str) -> str:
    path_token = path.strip("/").replace("{", "").replace("}", "") or "root"
    return slugify_identifier(f"{method.lower()}_{path_token}")


def _compose_operation_description(method_data: dict[str, object]) -> str | None:
    """Build Markdown operation description from viewer Description and Usage sections."""

    viewer_description = method_data.get("viewer_description")
    short_description = method_data.get("description")
    viewer_usage = method_data.get("viewer_usage")

    parts: list[str] = []
    if isinstance(viewer_description, str) and viewer_description.strip():
        parts.append(viewer_description.strip())
    elif isinstance(short_description, str) and short_description.strip():
        parts.append(short_description.strip())

    if isinstance(viewer_usage, str) and viewer_usage.strip():
        usage = viewer_usage.strip()
        if parts:
            parts.append(f"## Usage\n{usage}")
        else:
            parts.append(f"## Usage\n{usage}")

    if not parts:
        return None
    return "\n\n".join(parts)


def _build_path_params(path: str, parameters: dict[str, object]) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    for param in extract_path_params(path):
        pdef = {}
        if isinstance(parameters.get("properties"), dict):
            pdef = parameters["properties"].get(param, {}) or {}
        schema = _normalize_schema({"type": "object", "properties": {param: pdef}})
        base = pdef if isinstance(pdef, dict) else {}
        out.append(
            {
                "name": param,
                "in": "path",
                "required": True,
                "description": base.get("description"),
                "schema": {
                    "type": base.get("type", "string"),
                    **({"enum": base["enum"]} if "enum" in base else {}),
                    **({"pattern": base["pattern"]} if "pattern" in base else {}),
                    **({"format": base["format"]} if isinstance(base.get("format"), str) else {}),
                },
                "x-proxmox": {
                    "raw": schema,
                },
            }
        )
    return out


def _build_query_params(
    path: str,
    parameters: dict[str, object],
) -> list[dict[str, object]]:
    path_param_names = set(extract_path_params(path))
    out: list[dict[str, object]] = []
    properties = parameters.get("properties", {}) if isinstance(parameters, dict) else {}
    if not isinstance(properties, dict):
        return out

    for name, pdef in sorted(properties.items()):
        if name in path_param_names:
            continue
        if not isinstance(pdef, dict):
            continue
        out.append(
            {
                "name": name,
                "in": "query",
                "required": not _is_optional(pdef.get("optional")),
                "description": pdef.get("description"),
                "schema": {
                    "type": pdef.get("type", "string"),
                    **({"enum": pdef["enum"]} if "enum" in pdef else {}),
                    **({"pattern": pdef["pattern"]} if "pattern" in pdef else {}),
                    **({"default": pdef["default"]} if "default" in pdef else {}),
                    **({"minimum": pdef["minimum"]} if "minimum" in pdef else {}),
                    **({"maximum": pdef["maximum"]} if "maximum" in pdef else {}),
                },
                "x-proxmox": {"raw": pdef},
            }
        )
    return out


def normalize_captured_endpoints(
    endpoint_map: dict[str, dict[str, object]],
) -> list[NormalizedOperation]:
    """Convert capture endpoint map into normalized operation list."""

    operations: list[NormalizedOperation] = []

    for path in sorted(endpoint_map):
        endpoint = endpoint_map[path]
        methods = endpoint.get("methods", {}) or {}

        for method in HTTP_METHODS:
            method_data = methods.get(method)
            if not method_data:
                continue

            parameters = _normalize_schema(method_data.get("parameters") or {"type": "object"}) or {
                "type": "object"
            }
            returns = _normalize_schema(method_data.get("returns") or {"type": "object"}) or {
                "type": "object"
            }

            operations.append(
                NormalizedOperation(
                    method=method,
                    path=path,
                    operation_id=_operation_id(path=path, method=method),
                    summary=method_data.get("method_name"),
                    description=_compose_operation_description(method_data),
                    path_params=_build_path_params(path=path, parameters=parameters),
                    query_params=_build_query_params(path=path, parameters=parameters),
                    request_body_schema=(
                        parameters
                        if method in {"POST", "PUT", "DELETE"}
                        and bool(parameters.get("properties"))
                        else None
                    ),
                    response_schema=returns,
                    extra={
                        "permissions": method_data.get("permissions"),
                        "allowtoken": method_data.get("allowtoken"),
                        "protected": method_data.get("protected"),
                        "unstable": method_data.get("unstable"),
                        "raw_sections": method_data.get("raw_sections", []),
                        "source": method_data.get("source"),
                        "viewer_sections": {
                            "description": method_data.get("viewer_description"),
                            "usage": method_data.get("viewer_usage"),
                            "short_description": method_data.get("description"),
                        },
                    },
                )
            )

    return operations

"""Pydantic v2 model generator from generated OpenAPI schema."""

from __future__ import annotations

import math
from copy import deepcopy

from proxmox_sdk.proxmox_codegen.utils import (
    extract_path_params,
    pascal_case,
    slugify_identifier,
    utc_now_iso,
)


def _resolved_schema(schema: dict[str, object] | None) -> dict[str, object] | None:
    if not isinstance(schema, dict):
        return None
    one_of = schema.get("oneOf")
    if isinstance(one_of, list) and one_of:
        first = one_of[0]
        if isinstance(first, dict):
            return first
    return schema


def _number_literal(value: object) -> str | None:
    """Return a safe Python literal for a JSON Schema numeric constraint."""

    if type(value) not in {int, float}:
        return None
    if isinstance(value, float) and not math.isfinite(value):
        return None
    return repr(value)


def _integer_constraint_metadata(schema: dict[str, object]) -> list[str] | None:
    """Translate supported integer JSON Schema constraints to Pydantic metadata.

    ``None`` means the source constraint is malformed and the compatibility
    widening must fail closed instead of silently discarding it.
    """

    field_arguments: list[str] = []
    for schema_name, field_name in (
        ("minimum", "ge"),
        ("maximum", "le"),
        ("exclusiveMinimum", "gt"),
        ("exclusiveMaximum", "lt"),
        ("multipleOf", "multiple_of"),
    ):
        if schema_name not in schema:
            continue
        literal = _number_literal(schema[schema_name])
        if literal is None:
            return None
        if schema_name == "multipleOf" and schema[schema_name] <= 0:
            return None
        field_arguments.append(f"{field_name}={literal}")

    if "enum" in schema:
        enum = schema["enum"]
        if not isinstance(enum, list) or not enum or any(type(value) is not int for value in enum):
            return None
        field_arguments.append(f"json_schema_extra={{'enum': {enum!r}}}")
    metadata = [f"Field({', '.join(field_arguments)})"] if field_arguments else []
    if "enum" in schema:
        metadata.append(f"_allowed_ints({tuple(enum)!r})")
    return metadata


def _legacy_response_scalar_type(schema: dict[str, object]) -> str | None:
    """Return a strict, constraint-preserving type for a legacy response.

    Proxmox declares some values as strings because their expanded form is a
    comma-separated property string. Responses may instead contain the native
    scalar represented by the format's single ``default_key`` entry. Restrict
    this compatibility rule to integer and boolean defaults so composite disk,
    network, and other free-form strings are not widened.
    """

    format_schema = schema.get("format")
    if not isinstance(format_schema, dict):
        return None

    marked_entries = [
        value
        for value in format_schema.values()
        if isinstance(value, dict) and "default_key" in value
    ]
    if len(marked_entries) != 1:
        return None

    default_entry = marked_entries[0]
    default_key = default_entry["default_key"]
    if type(default_key) is not int or default_key != 1:
        return None
    default_type = default_entry.get("type")
    if not isinstance(default_type, str):
        return None

    if default_type == "boolean":
        # Proxmox emits native booleans and, on older endpoints, exact integer
        # flags. Keep both representations without accepting 1.0, 2, or other
        # values that Pydantic's coercive ``bool`` validator would normalize.
        return "StrictBool | Annotated[StrictInt, Field(ge=0, le=1)]"
    if default_type != "integer":
        return None

    metadata = _integer_constraint_metadata(default_entry)
    if metadata is None:
        return None
    if not metadata:
        return "StrictInt"
    return f"Annotated[StrictInt, {', '.join(metadata)}]"


def _python_type(
    schema: dict[str, object] | None, *, allow_legacy_response_scalar: bool = False
) -> str:
    schema = _resolved_schema(schema)
    if not isinstance(schema, dict):
        return "object"
    schema_type = schema.get("type")
    if schema_type == "null":
        return "None"
    if schema_type == "string":
        if allow_legacy_response_scalar:
            scalar_type = _legacy_response_scalar_type(schema)
            if scalar_type is not None:
                return f"{scalar_type} | StrictStr"
        return "StrictStr"
    if schema_type == "integer":
        return "int"
    if schema_type == "number":
        return "float"
    if schema_type == "boolean":
        return "bool"
    if schema_type == "array":
        items_schema = schema.get("items")
        item_type = _python_type(
            items_schema if isinstance(items_schema, dict) else {},
            allow_legacy_response_scalar=allow_legacy_response_scalar,
        )
        return f"list[{item_type}]"
    if schema_type == "object":
        return "dict[str, object]"
    return "object"


def _generate_object_model(
    model_name: str,
    schema: dict[str, object],
    docstring: str | None = None,
    *,
    allow_legacy_response_scalars: bool = False,
) -> str:
    properties = schema.get("properties", {}) if isinstance(schema, dict) else {}
    required = set(schema.get("required", [])) if isinstance(schema, dict) else set()

    if not properties:
        return _generate_root_model(
            model_name,
            {"type": "object"},
            docstring=docstring,
            allow_legacy_response_scalars=allow_legacy_response_scalars,
        )

    lines = [f"class {model_name}(BaseModel):"]

    # Add docstring if provided
    if docstring:
        safe_docstring = docstring.replace('"""', "").strip()
        lines.append(f'    """Model for {safe_docstring}."""')

    for prop_name, prop_schema in sorted(properties.items()):
        if not isinstance(prop_schema, dict):
            prop_schema = {}
        field_name = slugify_identifier(prop_name)
        field_type = _python_type(
            prop_schema,
            allow_legacy_response_scalar=allow_legacy_response_scalars,
        )
        is_required = prop_name in required
        default_expr = "..." if is_required else "None"
        alias_expr = f', alias="{prop_name}"' if field_name != prop_name else ""
        description = prop_schema.get("description")
        description_expr = (
            f", description={description!r}" if isinstance(description, str) and description else ""
        )

        lines.append(
            f"    {field_name}: {field_type}{'' if is_required else ' | None'} = Field({default_expr}{alias_expr}{description_expr})"
        )

    return "\n".join(lines)


def _generate_root_model(
    model_name: str,
    schema: dict[str, object],
    docstring: str | None = None,
    *,
    allow_legacy_response_scalars: bool = False,
) -> str:
    field_type = _python_type(
        schema,
        allow_legacy_response_scalar=allow_legacy_response_scalars,
    )
    description = schema.get("description")
    description_expr = (
        f", description={description!r}" if isinstance(description, str) and description else ""
    )
    lines = [
        f"class {model_name}(RootModel[{field_type}]):",
    ]

    # Add docstring if provided
    if docstring:
        safe_docstring = docstring.replace('"""', "").strip()
        lines.append(f'    """Model for {safe_docstring}."""')

    lines.append(f"    root: {field_type} = Field(...{description_expr})")

    return "\n".join(lines)


def _generate_model_from_schema(
    model_name: str,
    schema: dict[str, object],
    docstring: str | None = None,
    *,
    allow_legacy_response_scalars: bool = False,
) -> list[str]:
    schema = _resolved_schema(schema) or {}
    if (
        schema.get("type") == "array"
        and isinstance(schema.get("items"), dict)
        and schema["items"].get("type") == "object"
        and schema["items"].get("properties")
    ):
        item_model_name = f"{model_name}Item"
        description = schema.get("description")
        description_expr = (
            f", description={description!r}" if isinstance(description, str) and description else ""
        )
        item_docstring = docstring or schema["items"].get("description")
        list_docstring = docstring or schema.get("description")
        return [
            _generate_object_model(
                item_model_name,
                schema["items"],
                docstring=item_docstring,
                allow_legacy_response_scalars=allow_legacy_response_scalars,
            ),
            "\n".join(
                [
                    f"class {model_name}(RootModel[list[{item_model_name}]]):",
                    *([f'    """List of items. {list_docstring}."""'] if list_docstring else []),
                    f"    root: list[{item_model_name}] = Field(...{description_expr})",
                ]
            ),
        ]
    if schema.get("type") == "object":
        return [
            _generate_object_model(
                model_name,
                schema,
                docstring=docstring,
                allow_legacy_response_scalars=allow_legacy_response_scalars,
            )
        ]
    return [
        _generate_root_model(
            model_name,
            schema,
            docstring=docstring,
            allow_legacy_response_scalars=allow_legacy_response_scalars,
        )
    ]


def _request_schema_for_operation(
    path: str, operation: dict[str, object]
) -> dict[str, object] | None:
    """Return request-body schema excluding path parameters for runtime proxy models."""

    request_schema = (
        operation.get("requestBody", {})
        .get("content", {})
        .get("application/json", {})
        .get("schema")
    )
    if not isinstance(request_schema, dict):
        return None

    path_params = set(extract_path_params(path))
    if not path_params:
        return request_schema

    schema = deepcopy(request_schema)
    properties = schema.get("properties")
    if isinstance(properties, dict):
        schema["properties"] = {
            name: value for name, value in properties.items() if name not in path_params
        }
    required = schema.get("required")
    if isinstance(required, list):
        schema["required"] = [name for name in required if name not in path_params]
    return schema


def generate_pydantic_models_from_openapi(  # noqa: C901
    openapi: dict[str, object],
    *,
    version_tag: str | None = None,
    source_sha256: str | None = None,
    generated_at: str | None = None,
) -> str:
    """Generate a Python module with Pydantic v2 schemas for request/response payloads.

    When ``version_tag``, ``source_sha256``, and ``generated_at`` are supplied,
    they are embedded as ``GENERATED_FOR_PROXMOX_VERSION``,
    ``GENERATED_SOURCE_SHA256``, and ``GENERATED_AT`` module constants that
    ``tests/test_generated_integrity.py`` uses to detect drift.
    """

    info = openapi.get("info") if isinstance(openapi, dict) else None
    resolved_version = (
        version_tag or (info.get("version") if isinstance(info, dict) else None) or "latest"
    )
    resolved_at = generated_at or utc_now_iso()

    lines: list[str] = [
        '"""Generated Pydantic v2 schemas from Proxmox OpenAPI output.',
        "",
        "Do not edit by hand. The integrity guard below pins this artifact to the",
        "``openapi.json`` it was generated from; ``tests/test_generated_integrity.py``",
        "re-hashes the source spec on every run and fails if the two drift.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Annotated",
        "",
        "from pydantic import AfterValidator, BaseModel, ConfigDict, Field, RootModel, StrictBool, StrictInt, StrictStr",
        "",
        f'GENERATED_FOR_PROXMOX_VERSION = "{resolved_version}"',
        f'GENERATED_SOURCE_SHA256 = "{source_sha256 or ""}"',
        f'GENERATED_AT = "{resolved_at}"',
        "",
        "",
        "class ProxmoxBaseModel(BaseModel):",
        "    model_config = ConfigDict(populate_by_name=True, extra='allow')",
        "",
        "",
        "def _allowed_ints(allowed: tuple[int, ...]) -> AfterValidator:",
        "    def validate(value: int) -> int:",
        "        if value not in allowed:",
        "            raise ValueError('value is not an allowed schema member')",
        "        return value",
        "",
        "    return AfterValidator(validate)",
        "",
    ]

    seen_models: set[str] = set()

    for path, path_item in sorted((openapi.get("paths") or {}).items()):
        if not isinstance(path_item, dict):
            continue

        for method, operation in sorted(path_item.items()):
            if not isinstance(operation, dict):
                continue
            if method.upper() not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
                continue

            operation_id = operation.get("operationId") or f"{method}_{path}"
            base_name = pascal_case(operation_id)

            # Extract operation documentation
            operation_summary = operation.get("summary", "")
            operation_desc = operation.get("description", "")
            operation_doc = (
                f"{operation_summary}. {operation_desc}".strip()
                if operation_summary or operation_desc
                else None
            )

            req_schema = _request_schema_for_operation(path=path, operation=operation)
            if isinstance(req_schema, dict):
                req_model_name = f"{base_name}Request"
                if req_model_name not in seen_models:
                    req_docstring = f"{operation_doc} request" if operation_doc else None
                    model_blocks = _generate_model_from_schema(
                        req_model_name, req_schema, docstring=req_docstring
                    )
                    seen_models.add(req_model_name)
                    if len(model_blocks) > 1:
                        seen_models.add(f"{req_model_name}Item")
                    for block in model_blocks:
                        lines.append(block.replace("(BaseModel)", "(ProxmoxBaseModel)"))
                        lines.append("")

            resp_schema = (
                operation.get("responses", {})
                .get("200", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema")
            )
            if isinstance(resp_schema, dict):
                resp_model_name = f"{base_name}Response"
                if resp_model_name not in seen_models:
                    resp_docstring = f"{operation_doc} response" if operation_doc else None
                    model_blocks = _generate_model_from_schema(
                        resp_model_name,
                        resp_schema,
                        docstring=resp_docstring,
                        allow_legacy_response_scalars=True,
                    )
                    seen_models.add(resp_model_name)
                    if len(model_blocks) > 1:
                        seen_models.add(f"{resp_model_name}Item")
                    for block in model_blocks:
                        lines.append(block.replace("(BaseModel)", "(ProxmoxBaseModel)"))
                        lines.append("")

    if not seen_models:
        lines.append("class GeneratedPlaceholder(ProxmoxBaseModel):")
        lines.append("    value: str = 'no-models-generated'")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def _model_group(path: str) -> str:
    parts = [part for part in path.split("/") if part]
    if not parts:
        return "root"
    return slugify_identifier(parts[0].strip("{}")) or "root"


def _module_header(
    *,
    version_tag: str,
    source_sha256: str,
    generated_at: str,
    group: str | None = None,
) -> list[str]:
    title = (
        f'"""Generated Pydantic v2 schemas for Proxmox route group {group!r}.'
        if group
        else '"""Generated Pydantic v2 schemas from Proxmox OpenAPI output.'
    )
    return [
        title,
        "",
        "Do not edit by hand. Regenerate from the matching OpenAPI artifact.",
        '"""',
        "",
        "from __future__ import annotations",
        "",
        "from typing import Annotated",
        "",
        "from pydantic import AfterValidator, BaseModel, ConfigDict, Field, RootModel, StrictBool, StrictInt, StrictStr",
        "",
        f'GENERATED_FOR_PROXMOX_VERSION = "{version_tag}"',
        f'GENERATED_SOURCE_SHA256 = "{source_sha256}"',
        f'GENERATED_AT = "{generated_at}"',
        "",
        "",
        "class ProxmoxBaseModel(BaseModel):",
        "    model_config = ConfigDict(populate_by_name=True, extra='allow')",
        "",
        "",
        "def _allowed_ints(allowed: tuple[int, ...]) -> AfterValidator:",
        "    def validate(value: int) -> int:",
        "        if value not in allowed:",
        "            raise ValueError('value is not an allowed schema member')",
        "        return value",
        "",
        "    return AfterValidator(validate)",
        "",
    ]


def generate_pydantic_model_shards_from_openapi(  # noqa: C901
    openapi: dict[str, object],
    *,
    version_tag: str | None = None,
    source_sha256: str | None = None,
    generated_at: str | None = None,
) -> tuple[dict[str, str], dict[str, object]]:
    """Generate route-group Pydantic model shard modules and an operation index."""

    info = openapi.get("info") if isinstance(openapi, dict) else None
    resolved_version = (
        version_tag or (info.get("version") if isinstance(info, dict) else None) or "latest"
    )
    resolved_at = generated_at or utc_now_iso()
    resolved_sha = source_sha256 or ""
    shard_lines: dict[str, list[str]] = {}
    seen_models: dict[str, set[str]] = {}
    operations: dict[str, dict[str, str | None]] = {}

    for path, path_item in sorted((openapi.get("paths") or {}).items()):
        if not isinstance(path_item, dict):
            continue

        group = _model_group(path)
        lines = shard_lines.setdefault(
            group,
            _module_header(
                version_tag=resolved_version,
                source_sha256=resolved_sha,
                generated_at=resolved_at,
                group=group,
            ),
        )
        group_seen = seen_models.setdefault(group, set())

        for method, operation in sorted(path_item.items()):
            if not isinstance(operation, dict):
                continue
            if method.upper() not in {"GET", "POST", "PUT", "PATCH", "DELETE"}:
                continue

            operation_id = operation.get("operationId") or f"{method}_{path}"
            base_name = pascal_case(operation_id)
            operation_summary = operation.get("summary", "")
            operation_desc = operation.get("description", "")
            operation_doc = (
                f"{operation_summary}. {operation_desc}".strip()
                if operation_summary or operation_desc
                else None
            )
            request_model: str | None = None
            response_model: str | None = None

            req_schema = _request_schema_for_operation(path=path, operation=operation)
            if isinstance(req_schema, dict):
                req_model_name = f"{base_name}Request"
                properties = req_schema.get("properties")
                if isinstance(properties, dict) and properties:
                    request_model = req_model_name
                    if req_model_name not in group_seen:
                        req_docstring = f"{operation_doc} request" if operation_doc else None
                        model_blocks = _generate_model_from_schema(
                            req_model_name,
                            req_schema,
                            docstring=req_docstring,
                        )
                        group_seen.add(req_model_name)
                        if len(model_blocks) > 1:
                            group_seen.add(f"{req_model_name}Item")
                        for block in model_blocks:
                            lines.append(block.replace("(BaseModel)", "(ProxmoxBaseModel)"))
                            lines.append("")

            resp_schema = (
                operation.get("responses", {})
                .get("200", {})
                .get("content", {})
                .get("application/json", {})
                .get("schema")
            )
            if isinstance(resp_schema, dict):
                resp_model_name = f"{base_name}Response"
                response_model = resp_model_name
                if resp_model_name not in group_seen:
                    resp_docstring = f"{operation_doc} response" if operation_doc else None
                    model_blocks = _generate_model_from_schema(
                        resp_model_name,
                        resp_schema,
                        docstring=resp_docstring,
                        allow_legacy_response_scalars=True,
                    )
                    group_seen.add(resp_model_name)
                    if len(model_blocks) > 1:
                        group_seen.add(f"{resp_model_name}Item")
                    for block in model_blocks:
                        lines.append(block.replace("(BaseModel)", "(ProxmoxBaseModel)"))
                        lines.append("")

            operations[str(operation_id)] = {
                "group": group,
                "request_model": request_model,
                "response_model": response_model,
            }

    shards = {group: "\n".join(lines).rstrip() + "\n" for group, lines in shard_lines.items()}
    index: dict[str, object] = {
        "version_tag": resolved_version,
        "generated_at": resolved_at,
        "source_sha256": resolved_sha,
        "groups": sorted(shards),
        "operations": operations,
    }
    return shards, index


__all__ = [
    "generate_pydantic_model_shards_from_openapi",
    "generate_pydantic_models_from_openapi",
]

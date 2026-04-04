"""Real Proxmox API route registration with validation."""

from __future__ import annotations

import inspect
import sys
from copy import deepcopy
from types import ModuleType
from typing import Any

from fastapi import APIRouter, Body, FastAPI, Path, Query

from proxmox_openapi.exception import ProxmoxOpenAPIException
from proxmox_openapi.proxmox.client import ProxmoxClient
from proxmox_openapi.proxmox.config import ProxmoxConfig
from proxmox_openapi.proxmox_codegen.pydantic_generator import (
    generate_pydantic_models_from_openapi,
)
from proxmox_openapi.proxmox_codegen.utils import (
    extract_path_params,
    pascal_case,
    slugify_identifier,
)
from proxmox_openapi.schema import (
    DEFAULT_PROXMOX_OPENAPI_TAG,
    load_proxmox_generated_openapi,
)

_SUPPORTED_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE"}
_GENERATED_ROUTE_NAME_PREFIX = "generated_proxmox_real__"


def _schema_to_annotation(schema: dict[str, object] | None) -> object:
    """Convert JSON schema to Python type annotation."""
    if not isinstance(schema, dict):
        return object
    schema_type = schema.get("type")
    if schema_type == "string":
        return str
    if schema_type == "integer":
        return int
    if schema_type == "number":
        return float
    if schema_type == "boolean":
        return bool
    if schema_type == "array":
        items_schema = schema.get("items")
        return list[_schema_to_annotation(items_schema)]  # type: ignore[misc]
    if schema_type == "object" or isinstance(schema.get("properties"), dict):
        return dict[str, object]
    return object


def _load_model_module(openapi_document: dict[str, object], version_tag: str) -> ModuleType:
    """Load Pydantic models module from OpenAPI schema."""
    code = generate_pydantic_models_from_openapi(openapi_document)
    module = ModuleType(f"proxmox_openapi.proxmox.generated_{version_tag.replace('.', '_')}")
    sys.modules[module.__name__] = module
    exec(code, module.__dict__)
    for value in module.__dict__.values():
        if (
            isinstance(value, type)
            and getattr(value, "__module__", None) == module.__name__
            and hasattr(value, "model_rebuild")
        ):
            value.model_rebuild(_types_namespace=module.__dict__)
    return module


def _request_schema(path_template: str, operation: dict[str, object]) -> dict[str, object] | None:
    """Extract request schema from operation, excluding path parameters."""
    schema = (
        operation.get("requestBody", {})  # type: ignore[union-attr]
        .get("content", {})  # type: ignore[union-attr]
        .get("application/json", {})  # type: ignore[union-attr]
        .get("schema")  # type: ignore[union-attr]
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


def _response_schema(operation: dict[str, object]) -> dict[str, object] | None:
    """Extract response schema from operation."""
    schema = (
        operation.get("responses", {})  # type: ignore[union-attr]
        .get("200", {})  # type: ignore[union-attr]
        .get("content", {})  # type: ignore[union-attr]
        .get("application/json", {})  # type: ignore[union-attr]
        .get("schema")  # type: ignore[union-attr]
    )
    return deepcopy(schema) if isinstance(schema, dict) else None


def _operation_parameters(operation: dict[str, object]) -> list[dict[str, object]]:
    """Extract parameters list from operation."""
    parameters = operation.get("parameters")
    if not isinstance(parameters, list):
        return []
    return [parameter for parameter in parameters if isinstance(parameter, dict)]


def _path_parameter_name_map(operation: dict[str, object]) -> dict[str, str]:
    """Map original path parameter names to Python-safe names."""
    used_names = {"request_body"}
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
    """Convert API path template to FastAPI path format."""
    mounted = path_template
    for original, python in _path_parameter_name_map(operation).items():
        mounted = mounted.replace(f"{{{original}}}", f"{{{python}}}")
    return mounted


def _operation_id(path_template: str, method: str, operation: dict[str, object]) -> str:
    """Get or generate operation ID."""
    return operation.get("operationId") or f"{method.lower()}_{path_template}"  # type: ignore[return-value]


def _operation_request_model(
    model_module: ModuleType,
    path_template: str,
    operation: dict[str, object],
    operation_id: str,
) -> type | None:
    """Get Pydantic request model for operation."""
    request_schema = _request_schema(path_template, operation)
    if not isinstance(request_schema, dict):
        return None
    properties = request_schema.get("properties")
    if not isinstance(properties, dict) or not properties:
        return None
    return getattr(model_module, f"{pascal_case(operation_id)}Request", None)


def _operation_response_model(model_module: ModuleType, operation_id: str) -> type | None:
    """Get Pydantic response model for operation."""
    return getattr(model_module, f"{pascal_case(operation_id)}Response", None)


def _server_prefix(openapi_document: dict[str, object]) -> str:
    """Extract server URL prefix from OpenAPI document."""
    servers = openapi_document.get("servers")
    if isinstance(servers, list) and servers:
        first = servers[0]
        if isinstance(first, dict) and isinstance(first.get("url"), str):
            return first["url"].rstrip("/")  # type: ignore[return-value]
    return ""


def _normalize_body_value(request_body: Any) -> Any:
    """Normalize request body to dict."""
    if hasattr(request_body, "model_dump"):
        return request_body.model_dump(by_alias=True, exclude_none=True)
    return request_body


def _render_path(path_template: str, path_values: dict[str, Any]) -> str:
    """Render path template with actual values."""
    rendered = path_template
    for name, value in path_values.items():
        rendered = rendered.replace(f"{{{name}}}", str(value))
    return rendered


def _build_generated_endpoint(
    *,
    path_template: str,
    method: str,
    operation: dict[str, object],
    request_model: type | None,
    request_schema: dict[str, Any] | None,
    response_model: type | None,
    operation_id: str,
    proxmox_client: ProxmoxClient,
) -> object:
    """Build FastAPI endpoint that calls real Proxmox API."""
    path_param_name_map = _path_parameter_name_map(operation)
    path_param_map = {python: original for original, python in path_param_name_map.items()}
    query_param_map: dict[str, str] = {}
    signature_parameters: list[inspect.Parameter] = []
    used_names: set[str] = set()

    def _unique_name(base: str) -> str:
        candidate = base
        suffix = 1
        while candidate in used_names:
            candidate = f"{base}_{suffix}"
            suffix += 1
        return candidate

    # Add path and query parameters
    for parameter in _operation_parameters(operation):
        location = parameter.get("in")
        original_name = parameter.get("name")
        if not isinstance(original_name, str):
            continue

        schema = parameter.get("schema") if isinstance(parameter.get("schema"), dict) else {}
        description = parameter.get("description")
        required = bool(parameter.get("required"))
        python_name = (
            path_param_name_map[original_name]
            if location == "path" and original_name in path_param_name_map
            else slugify_identifier(original_name)
        )
        if python_name in used_names:
            python_name = _unique_name(f"op_{python_name}")
        annotation = _schema_to_annotation(schema)
        alias = original_name if python_name != original_name else None

        if location == "path":
            signature_parameters.append(
                inspect.Parameter(
                    python_name,
                    inspect.Parameter.KEYWORD_ONLY,
                    annotation=annotation,
                    default=Path(..., description=description),
                )
            )
            used_names.add(python_name)
        elif location == "query":
            query_param_map[python_name] = original_name
            if not required:
                annotation = annotation | None  # type: ignore[assignment]
            signature_parameters.append(
                inspect.Parameter(
                    python_name,
                    inspect.Parameter.KEYWORD_ONLY,
                    annotation=annotation,
                    default=Query(... if required else None, description=description, alias=alias),
                )
            )
            used_names.add(python_name)

    # Add request body parameter
    if request_schema is not None:
        annotation = request_model or _schema_to_annotation(request_schema)
        signature_parameters.append(
            inspect.Parameter(
                "request_body",
                inspect.Parameter.KEYWORD_ONLY,
                annotation=annotation,
                default=Body(...),
            )
        )

    async def generated_endpoint(**kwargs: Any) -> Any:
        request_body = kwargs.pop("request_body", None)
        path_values = {original: kwargs.pop(python) for python, original in path_param_map.items()}
        query_values = {
            original: kwargs.get(python)
            for python, original in query_param_map.items()
            if kwargs.get(python) is not None
        }
        body_value = _normalize_body_value(request_body)
        concrete_path = _render_path(path_template, path_values)

        try:
            # Call real Proxmox API
            result = await proxmox_client.request(
                method=method,
                path=concrete_path,
                params=query_values or None,
                json=body_value,
            )

            # Validate response if model exists
            if response_model is not None:
                try:
                    return response_model.model_validate(result)
                except Exception as error:
                    raise ProxmoxOpenAPIException(
                        message=f"Proxmox API response validation failed for {method} {path_template}",
                        detail="Response does not match generated model schema",
                        python_exception=str(error),
                    )

            return result

        except Exception as error:
            if hasattr(error, "status_code"):  # Already an HTTPException
                raise
            raise ProxmoxOpenAPIException(
                message=f"Proxmox API request failed for {method} {path_template}",
                detail=str(error),
            )

    generated_endpoint.__name__ = f"{_GENERATED_ROUTE_NAME_PREFIX}{method.lower()}__{operation_id}"
    generated_endpoint.__qualname__ = generated_endpoint.__name__
    generated_endpoint.__signature__ = inspect.Signature(  # type: ignore[attr-defined]
        parameters=signature_parameters,
        return_annotation=response_model or dict[str, object],
    )
    return generated_endpoint


def register_generated_proxmox_real_routes(
    app: FastAPI | APIRouter,
    *,
    version_tag: str = DEFAULT_PROXMOX_OPENAPI_TAG,
    openapi_document: dict[str, object] | None = None,
    proxmox_config: ProxmoxConfig,
) -> dict[str, object]:
    """Register real Proxmox API routes with validation.

    Args:
        app: FastAPI app or router
        version_tag: OpenAPI schema version tag
        openapi_document: Pre-loaded OpenAPI document (optional)
        proxmox_config: Proxmox connection configuration

    Returns:
        Registration statistics

    Raises:
        ProxmoxOpenAPIException: If schema not found or config invalid
    """
    document = openapi_document or load_proxmox_generated_openapi(version_tag=version_tag)
    if not document:
        raise ProxmoxOpenAPIException(
            message="Generated Proxmox OpenAPI schema not found",
            detail=f"Unable to load version tag '{version_tag}'",
        )

    proxmox_config.validate_for_real_mode()
    proxmox_client = ProxmoxClient(proxmox_config)

    model_module = _load_model_module(document, version_tag)
    base_prefix = _server_prefix(document)
    path_items = {
        path: item
        for path, item in (document.get("paths") or {}).items()  # type: ignore[union-attr]
        if isinstance(item, dict)
    }

    route_count = 0
    method_count = 0

    for path_template, path_item in sorted(path_items.items()):
        for method, operation in sorted(path_item.items()):
            method_name = method.upper()
            if method_name not in _SUPPORTED_METHODS or not isinstance(operation, dict):
                continue

            operation_id = _operation_id(path_template, method_name, operation)
            request_schema_val = _request_schema(path_template, operation)
            request_model = _operation_request_model(
                model_module, path_template, operation, operation_id
            )
            response_model = _operation_response_model(model_module, operation_id)

            endpoint = _build_generated_endpoint(
                path_template=path_template,
                method=method_name,
                operation=operation,
                request_model=request_model,
                request_schema=request_schema_val,
                response_model=response_model,
                operation_id=operation_id,
                proxmox_client=proxmox_client,
            )

            route_name = f"{_GENERATED_ROUTE_NAME_PREFIX}{method_name.lower()}__{operation_id}"
            app.add_api_route(
                path=f"{base_prefix}{_mounted_fastapi_path(path_template, operation)}",
                endpoint=endpoint,
                methods=[method_name],
                name=route_name,
                summary=operation.get("summary"),  # type: ignore[arg-type]
                description=operation.get("description"),  # type: ignore[arg-type]
                response_model=response_model,
                tags=["proxmox real / generated"],
            )
            route_count += 1
            method_count += 1

    app.openapi_schema = None  # type: ignore[attr-defined]

    return {
        "route_count": route_count,
        "path_count": len(path_items),
        "method_count": method_count,
        "schema_version": document.get("info", {}).get("version", version_tag),  # type: ignore[union-attr]
        "base_prefix": base_prefix or "/",
    }


__all__ = ["register_generated_proxmox_real_routes"]

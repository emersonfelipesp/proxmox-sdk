"""Real Proxmox API route registration with validation."""

from __future__ import annotations

import inspect
import logging
from typing import Any, Callable

from fastapi import APIRouter, Body, FastAPI, HTTPException, Path, Query, Request

from proxmox_sdk.exception import ProxmoxOpenAPIException
from proxmox_sdk.proxmox.client import ProxmoxClient
from proxmox_sdk.proxmox.config import ProxmoxConfig
from proxmox_sdk.proxmox_codegen.utils import slugify_identifier
from proxmox_sdk.routes._errors import with_error_translation
from proxmox_sdk.routes.generated_artifacts import (
    install_generated_openapi,
    load_operation_model,
    load_route_metadata,
)
from proxmox_sdk.routes.helpers import (
    SUPPORTED_METHODS as _SUPPORTED_METHODS,
)
from proxmox_sdk.routes.helpers import (
    load_model_module as _load_model_module_shared,
)
from proxmox_sdk.routes.helpers import (
    mounted_fastapi_path as _mounted_fastapi_path,
)
from proxmox_sdk.routes.helpers import (
    normalize_body_value as _normalize_body_value,
)
from proxmox_sdk.routes.helpers import (
    operation_id as _operation_id,
)
from proxmox_sdk.routes.helpers import (
    operation_parameters as _operation_parameters,
)
from proxmox_sdk.routes.helpers import (
    operation_request_model as _operation_request_model,
)
from proxmox_sdk.routes.helpers import (
    operation_response_model as _operation_response_model,
)
from proxmox_sdk.routes.helpers import (
    path_parameter_name_map as _path_parameter_name_map,
)
from proxmox_sdk.routes.helpers import (
    render_path as _render_path,
)
from proxmox_sdk.routes.helpers import (
    request_schema as _request_schema,
)
from proxmox_sdk.routes.helpers import (
    schema_to_annotation as _schema_to_annotation,
)
from proxmox_sdk.routes.helpers import (
    server_prefix as _server_prefix,
)
from proxmox_sdk.schema import (
    DEFAULT_PROXMOX_OPENAPI_TAG,
    load_proxmox_generated_openapi,
)

logger = logging.getLogger(__name__)

_GENERATED_ROUTE_NAME_PREFIX = "generated_proxmox_real__"


def _load_model_module(openapi_document: dict[str, object], version_tag: str) -> Any:
    """Load Pydantic models module from OpenAPI schema."""
    return _load_model_module_shared(openapi_document, version_tag, module_prefix="proxmox")


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

    @with_error_translation(
        method=method,
        path_template=path_template,
        message_prefix="Proxmox API request",
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

        result = await proxmox_client.request(
            method=method,
            path=concrete_path,
            params=query_values or None,
            json=body_value,
        )

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

    generated_endpoint.__name__ = f"{_GENERATED_ROUTE_NAME_PREFIX}{method.lower()}__{operation_id}"
    generated_endpoint.__qualname__ = generated_endpoint.__name__
    generated_endpoint.__signature__ = inspect.Signature(  # type: ignore[attr-defined]
        parameters=signature_parameters,
        return_annotation=response_model or dict[str, object],
    )
    return generated_endpoint


def _coerce_value(value: Any, schema: dict[str, Any] | None) -> Any:
    if value is None or not isinstance(schema, dict):
        return value
    schema_type = schema.get("type")
    if schema_type == "integer":
        try:
            return int(value)
        except (TypeError, ValueError):
            raise HTTPException(status_code=422, detail=f"Invalid integer value: {value!r}")
    if schema_type == "number":
        try:
            return float(value)
        except (TypeError, ValueError):
            raise HTTPException(status_code=422, detail=f"Invalid number value: {value!r}")
    if schema_type == "boolean":
        if isinstance(value, bool):
            return value
        lowered = str(value).strip().lower()
        if lowered in {"1", "true", "yes", "on"}:
            return True
        if lowered in {"0", "false", "no", "off"}:
            return False
        raise HTTPException(status_code=422, detail=f"Invalid boolean value: {value!r}")
    return value


async def _request_body_value(request: Request, request_schema: dict[str, Any] | None) -> Any:
    if request_schema is None:
        return None
    body = await request.body()
    if not body:
        return None
    try:
        return await request.json()
    except Exception:
        raise HTTPException(status_code=422, detail="Request body must be valid JSON.")


def _build_metadata_endpoint(
    *,
    route: dict[str, Any],
    proxmox_client: ProxmoxClient,
    version_tag: str,
) -> Callable[..., Any]:
    raw_parameters = route.get("parameters")
    parameters: list[Any] = raw_parameters if isinstance(raw_parameters, list) else []
    path_parameters = [p for p in parameters if isinstance(p, dict) and p.get("in") == "path"]
    query_parameters = [p for p in parameters if isinstance(p, dict) and p.get("in") == "query"]
    path_template = str(route.get("path_template") or "")
    method = str(route.get("method") or "").upper()
    operation_id = str(route.get("operation_id") or "")
    group = str(route.get("model_group") or "")
    request_schema = (
        route.get("request_schema") if isinstance(route.get("request_schema"), dict) else None
    )
    request_model_name = (
        route.get("request_model") if isinstance(route.get("request_model"), str) else None
    )
    response_model_name = (
        route.get("response_model") if isinstance(route.get("response_model"), str) else None
    )

    @with_error_translation(
        method=method,
        path_template=path_template,
        message_prefix="Proxmox API request",
    )
    async def generated_endpoint(request: Request) -> Any:
        path_values: dict[str, Any] = {}
        for parameter in path_parameters:
            python_name = str(parameter.get("python_name"))
            original_name = str(parameter.get("name"))
            if python_name not in request.path_params:
                raise HTTPException(
                    status_code=422, detail=f"Missing path parameter: {original_name}"
                )
            path_values[original_name] = _coerce_value(
                request.path_params[python_name],
                parameter.get("schema") if isinstance(parameter.get("schema"), dict) else None,
            )

        query_values: dict[str, Any] = {}
        for parameter in query_parameters:
            original_name = str(parameter.get("name"))
            raw_value = request.query_params.get(original_name)
            if raw_value is None:
                if parameter.get("required"):
                    raise HTTPException(
                        status_code=422,
                        detail=f"Missing required query parameter: {original_name}",
                    )
                continue
            query_values[original_name] = _coerce_value(
                raw_value,
                parameter.get("schema") if isinstance(parameter.get("schema"), dict) else None,
            )

        body_value = await _request_body_value(request, request_schema)
        request_model = load_operation_model(
            version_tag,
            operation_id,
            "request",
            group=group,
            model_name=request_model_name,
        )
        if request_model is not None and body_value is not None:
            body_value = request_model.model_validate(body_value)
        body_value = _normalize_body_value(body_value)

        concrete_path = _render_path(path_template, path_values)
        result = await proxmox_client.request(
            method=method,
            path=concrete_path,
            params=query_values or None,
            json=body_value,
        )

        response_model = load_operation_model(
            version_tag,
            operation_id,
            "response",
            group=group,
            model_name=response_model_name,
        )
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

    generated_endpoint.__name__ = f"{_GENERATED_ROUTE_NAME_PREFIX}{method.lower()}__{operation_id}"
    generated_endpoint.__qualname__ = generated_endpoint.__name__
    return generated_endpoint


def _add_node_version_check(
    app: FastAPI,
    document: dict[str, object],
    version_tag: str,
    proxmox_client: ProxmoxClient,
) -> None:
    """Attach the advisory Proxmox node/schema compatibility startup check."""

    _schema_info_version = str(document.get("info", {}).get("version", version_tag))
    _schema_parts = _schema_info_version.split(".")
    _version_prefix = (
        ".".join(_schema_parts[:2]) if len(_schema_parts) >= 2 else _schema_info_version
    )
    _client_ref = proxmox_client

    async def _check_node_version() -> None:
        try:
            result = await _client_ref.get("/api2/json/version")
            node_version = (result or {}).get("version", "")
            if node_version and not node_version.startswith(_version_prefix):
                logger.warning(
                    "proxmox-sdk real mode: loaded schema for '%s' but node reports "
                    "version '%s'. Update PROXMOX_MOCK_SCHEMA_VERSION if needed.",
                    version_tag,
                    node_version,
                )
            else:
                logger.info(
                    "proxmox-sdk real mode: schema '%s' compatible with node version '%s'.",
                    version_tag,
                    node_version or "(unknown)",
                )
        except Exception as exc:
            logger.debug(
                "proxmox-sdk real mode: could not verify node version at startup "
                "(schema: '%s'): %s",
                version_tag,
                exc,
            )

    app.add_event_handler("startup", _check_node_version)


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

    proxmox_client = ProxmoxClient(proxmox_config)

    metadata = load_route_metadata(version_tag)
    if metadata is not None:
        route_count = 0
        raw_routes = metadata.get("routes")
        routes: list[Any] = raw_routes if isinstance(raw_routes, list) else []
        for route in routes:
            if not isinstance(route, dict):
                continue
            method_name = str(route.get("method") or "").upper()
            if method_name not in _SUPPORTED_METHODS:
                continue

            endpoint = _build_metadata_endpoint(
                route=route,
                proxmox_client=proxmox_client,
                version_tag=version_tag,
            )
            operation_id = str(route.get("operation_id") or "")
            route_name = f"{_GENERATED_ROUTE_NAME_PREFIX}{method_name.lower()}__{operation_id}"
            app.add_api_route(
                path=str(route.get("mounted_path")),
                endpoint=endpoint,
                methods=[method_name],
                name=route_name,
                summary=route.get("summary") if isinstance(route.get("summary"), str) else None,
                description=route.get("description")
                if isinstance(route.get("description"), str)
                else None,
                tags=["proxmox real / generated"],
                include_in_schema=False,
            )
            route_count += 1

        if isinstance(app, FastAPI):
            install_generated_openapi(app, document)
            _add_node_version_check(app, document, version_tag, proxmox_client)
        app.openapi_schema = None  # type: ignore[attr-defined]
        return {
            "route_count": route_count,
            "path_count": metadata.get("path_count", 0),
            "method_count": metadata.get("method_count", route_count),
            "schema_version": metadata.get("schema_version", version_tag),
            "base_prefix": metadata.get("base_prefix", "/"),
        }

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

    if isinstance(app, FastAPI):
        _add_node_version_check(app, document, version_tag, proxmox_client)

    return {
        "route_count": route_count,
        "path_count": len(path_items),
        "method_count": method_count,
        "schema_version": document.get("info", {}).get("version", version_tag),  # type: ignore[union-attr]
        "base_prefix": base_prefix or "/",
    }


__all__ = ["register_generated_proxmox_real_routes"]

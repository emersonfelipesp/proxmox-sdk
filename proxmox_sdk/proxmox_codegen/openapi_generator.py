"""OpenAPI 3.1 generator for normalized Proxmox API operations."""

from __future__ import annotations

from collections import defaultdict

from proxmox_sdk.proxmox_codegen.models import NormalizedOperation
from proxmox_sdk.proxmox_codegen.utils import to_openapi_path


def generate_openapi_schema(
    operations: list[NormalizedOperation],
    *,
    title: str = "Proxmox VE API (Generated from API Viewer)",
    version: str = "generated",
    server_url: str = "/api2/json",
) -> dict[str, object]:
    """Generate OpenAPI 3.1 schema from normalized Proxmox operations."""

    grouped: dict[str, dict[str, object]] = defaultdict(dict)

    for operation in operations:
        path = to_openapi_path(operation.path)
        method = operation.method.lower()

        parameters = [*operation.path_params, *operation.query_params]
        request_body = None
        if operation.request_body_schema:
            request_body = {
                "required": False,
                "content": {
                    "application/json": {
                        "schema": operation.request_body_schema,
                    }
                },
            }

        response_schema = operation.response_schema or {"type": "object"}

        grouped[path][method] = {
            "operationId": operation.operation_id,
            "summary": operation.summary,
            "description": operation.description,
            "parameters": parameters,
            **({"requestBody": request_body} if request_body else {}),
            "responses": {
                "200": {
                    "description": "Successful response",
                    "content": {
                        "application/json": {
                            "schema": response_schema,
                        }
                    },
                }
            },
            "x-proxmox": operation.extra,
        }

    return {
        "openapi": "3.1.0",
        "info": {
            "title": title,
            "version": version,
            "description": "Generated from Proxmox API Viewer raw endpoint definitions.",
        },
        "servers": [{"url": server_url}],
        "paths": dict(sorted(grouped.items())),
    }

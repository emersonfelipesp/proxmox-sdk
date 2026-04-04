"""Schema helpers for generated mock routes."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from typing import Any


def schema_fingerprint(openapi_document: dict[str, object]) -> str:
    """Return a stable fingerprint for the loaded OpenAPI document."""

    payload = json.dumps(openapi_document, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def resolved_schema(schema: dict[str, Any] | None) -> dict[str, Any]:
    """Resolve the most useful inline schema representation for mock generation."""

    if not isinstance(schema, dict):
        return {}
    if isinstance(schema.get("allOf"), list) and schema["allOf"]:
        merged: dict[str, Any] = {}
        for branch in schema["allOf"]:
            branch_schema = resolved_schema(branch if isinstance(branch, dict) else {})
            merged = deep_merge(merged, branch_schema)
        return merged
    for keyword in ("oneOf", "anyOf"):
        branches = schema.get(keyword)
        if isinstance(branches, list):
            for branch in branches:
                branch_schema = resolved_schema(branch if isinstance(branch, dict) else {})
                if branch_schema.get("type") != "null":
                    return branch_schema
    return schema


def schema_kind(schema: dict[str, Any] | None) -> str:
    """Classify the resolved schema into a small set of storage kinds."""

    resolved = resolved_schema(schema)
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


def sample_value_for_schema(schema: dict[str, Any] | None, *, seed: str) -> Any:  # noqa: C901
    """Build a deterministic mock value for an inline schema."""

    schema = resolved_schema(schema)
    if not schema:
        return {}

    if "const" in schema:
        return deepcopy(schema["const"])

    if "default" in schema:
        return deepcopy(schema["default"])

    enum = schema.get("enum")
    if isinstance(enum, list) and enum:
        return deepcopy(enum[0])

    schema_type = schema.get("type")
    if schema_type == "null":
        return None
    if schema_type == "string":
        pattern = schema.get("pattern")
        if pattern == "[0-9a-fA-F]{8,64}":
            return hashlib.sha1(seed.encode("utf-8")).hexdigest()[:8]
        if schema.get("format") == "date-time":
            return "2026-01-01T00:00:00Z"
        if schema.get("format") == "date":
            return "2026-01-01"
        return seed
    if schema_type == "integer":
        digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()
        return int(digest[:6], 16) % 10_000 or 1
    if schema_type == "number":
        digest = hashlib.sha1(seed.encode("utf-8")).hexdigest()
        return float((int(digest[:6], 16) % 10_000) / 100)
    if schema_type == "boolean":
        return True
    if schema_type == "array":
        item_schema = schema.get("items") if isinstance(schema.get("items"), dict) else {}
        return [sample_value_for_schema(item_schema, seed=f"{seed}_item_0")]

    properties = schema.get("properties") if isinstance(schema.get("properties"), dict) else {}
    if properties:
        payload: dict[str, Any] = {}
        for name, property_schema in sorted(properties.items()):
            payload[name] = sample_value_for_schema(
                property_schema if isinstance(property_schema, dict) else {},
                seed=f"{seed}_{name}",
            )
        return payload

    additional_properties = schema.get("additionalProperties")
    if isinstance(additional_properties, dict):
        return {
            "key": sample_value_for_schema(additional_properties, seed=f"{seed}_value"),
        }

    return {}


def deep_merge(base: Any, override: Any) -> Any:
    """Merge dict-shaped payloads recursively and otherwise replace the value."""

    if isinstance(base, dict) and isinstance(override, dict):
        merged = deepcopy(base)
        for key, value in override.items():
            if key in merged:
                merged[key] = deep_merge(merged[key], value)
            else:
                merged[key] = deepcopy(value)
        return merged
    return deepcopy(override)


def merge_with_schema_defaults(
    schema: dict[str, Any] | None,
    *,
    seed: str,
    override: Any | None = None,
) -> Any:
    """Merge user-provided values into a deterministic schema-backed seed value."""

    seeded_value = sample_value_for_schema(schema, seed=seed)
    if override is None:
        return seeded_value
    if isinstance(seeded_value, dict) and isinstance(override, dict):
        return deep_merge(seeded_value, override)
    if isinstance(seeded_value, list) and isinstance(override, list):
        return deepcopy(override)
    if override == {} and isinstance(seeded_value, (dict, list)):
        return seeded_value
    return deepcopy(override)

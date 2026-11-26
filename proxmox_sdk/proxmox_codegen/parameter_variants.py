"""Flatten Proxmox ``allOf``/``oneOf`` parameter schemas into one object schema.

Proxmox VE 9.3 started to describe some request parameters as a common part
plus type-dependent variants. ``POST /storage`` for example is published as::

    {"allOf": [
        {"properties": {"storage": {...}}},
        {"type-property": "type",
         "type-property-schema": {"enum": ["btrfs", "dir", ...]},
         "oneOf": [{"instance-type": "btrfs", "properties": {...}}, ...]},
    ]}

Earlier releases published the same operation as one flat ``properties``
object. The request-body and query-parameter builders only read a flat
``properties`` object, so without this step those operations lose their
whole request contract.

The flattened schema keeps every property of every variant. A property is
required only when every variant requires it. The discriminator named by
``type-property`` is added as an optional enum property, because Proxmox can
derive it (for example ``resource-type`` from an HA ``sid``) and the server
remains the authority that rejects a missing value. Each property that only
some variants accept records them in ``x-proxmox-instance-types``.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any

_VARIANT_KEYWORDS = ("allOf", "oneOf", "anyOf")
_INSTANCE_TYPES_KEY = "x-proxmox-instance-types"


def _is_optional(definition: object) -> bool:
    """Return True when a Proxmox property definition is optional."""
    if not isinstance(definition, dict):
        return True
    return str(definition.get("optional", 0)).strip().lower() in {"1", "true", "yes"}


def _has_variants(schema: dict[str, Any]) -> bool:
    return any(isinstance(schema.get(keyword), list) for keyword in _VARIANT_KEYWORDS)


def _merge_properties(
    target: dict[str, Any],
    source: dict[str, Any],
    *,
    force_optional: bool,
) -> None:
    """Merge ``source`` properties into ``target``; the first definition wins."""
    for name, definition in source.items():
        if not isinstance(definition, dict):
            continue
        if name not in target:
            target[name] = deepcopy(definition)
            if force_optional:
                target[name]["optional"] = 1
        elif not _is_optional(target[name]) and _is_optional(definition):
            target[name]["optional"] = 1


def _flatten_one_of(schema: dict[str, Any], keyword: str) -> dict[str, Any]:
    """Union the variants of one ``oneOf``/``anyOf`` group."""
    variants = [v for v in schema.get(keyword, []) if isinstance(v, dict)]
    flattened = [flatten_parameter_variants(variant) for variant in variants]
    names = [set((v.get("properties") or {}).keys()) for v in flattened]
    common = set.intersection(*names) if names else set()
    properties: dict[str, Any] = {}
    applies_to: dict[str, list[str]] = {}
    for variant, flat in zip(variants, flattened, strict=True):
        variant_properties = flat.get("properties") or {}
        _merge_properties(properties, variant_properties, force_optional=False)
        instance_type = variant.get("instance-type")
        for name in variant_properties:
            if isinstance(instance_type, str):
                applies_to.setdefault(name, []).append(instance_type)
    _mark_variant_only(properties, common, applies_to)
    _add_type_property(schema, properties)
    return {"type": "object", "properties": properties}


def _mark_variant_only(
    properties: dict[str, Any],
    common: set[str],
    applies_to: dict[str, list[str]],
) -> None:
    """Make properties that only some variants accept optional and tag them."""
    for name, definition in properties.items():
        if name in common:
            continue
        definition["optional"] = 1
        if applies_to.get(name):
            definition[_INSTANCE_TYPES_KEY] = sorted(set(applies_to[name]))


def _add_type_property(schema: dict[str, Any], properties: dict[str, Any]) -> None:
    """Expose the variant discriminator as an optional enum property."""
    type_property = schema.get("type-property")
    if not isinstance(type_property, str) or not type_property or type_property in properties:
        return
    definition = schema.get("type-property-schema")
    definition = deepcopy(definition) if isinstance(definition, dict) else {"type": "string"}
    definition["optional"] = 1
    properties[type_property] = definition


def flatten_parameter_variants(schema: object) -> Any:
    """Return ``schema`` with ``allOf``/``oneOf``/``anyOf`` folded into ``properties``.

    Schemas without variant keywords are returned unchanged (same object), so
    every pre-9.3 capture keeps a byte-identical result.
    """
    if not isinstance(schema, dict) or not _has_variants(schema):
        return schema
    properties: dict[str, Any] = {}
    _merge_properties(properties, schema.get("properties") or {}, force_optional=False)
    for part in schema.get("allOf") or []:
        flat = flatten_parameter_variants(part)
        if isinstance(flat, dict):
            _merge_properties(properties, flat.get("properties") or {}, force_optional=False)
    for keyword in ("oneOf", "anyOf"):
        if isinstance(schema.get(keyword), list):
            group = _flatten_one_of(schema, keyword)
            _merge_properties(properties, group["properties"], force_optional=False)
    result = {
        key: deepcopy(value)
        for key, value in schema.items()
        if key not in (*_VARIANT_KEYWORDS, "properties", "type-property", "type-property-schema")
    }
    result["type"] = "object"
    result["properties"] = properties
    return result

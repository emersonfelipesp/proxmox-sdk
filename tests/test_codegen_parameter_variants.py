"""Proxmox VE 9.3 publishes some request parameters as allOf/oneOf variants.

These tests pin the flattening rules and the end-to-end request contract of
the operations that lost every parameter before flattening existed.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from proxmox_sdk.proxmox_codegen.models import NormalizedOperation, RawMethodCapture
from proxmox_sdk.proxmox_codegen.parameter_variants import flatten_parameter_variants

GENERATED = Path(__file__).resolve().parents[1] / "proxmox_sdk" / "generated" / "proxmox"

STORAGE_CREATE = {
    "allOf": [
        {
            "additionalProperties": 0,
            "properties": {"storage": {"type": "string", "description": "The storage identifier."}},
        },
        {
            "type-property": "type",
            "type-property-schema": {"type": "string", "enum": ["dir", "nfs"]},
            "oneOf": [
                {
                    "instance-type": "dir",
                    "additionalProperties": 0,
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string", "optional": 1},
                    },
                },
                {
                    "instance-type": "nfs",
                    "additionalProperties": 0,
                    "properties": {
                        "server": {"type": "string"},
                        "export": {"type": "string"},
                        "content": {"type": "string", "optional": 1},
                        "path": {"type": "string", "optional": 1},
                    },
                },
            ],
        },
    ]
}


def test_flat_schema_is_returned_unchanged() -> None:
    schema = {"additionalProperties": 0, "properties": {"node": {"type": "string"}}}
    assert flatten_parameter_variants(schema) is schema


def test_non_dict_is_returned_unchanged() -> None:
    assert flatten_parameter_variants(None) is None
    assert flatten_parameter_variants([1]) == [1]


def test_storage_variants_are_unioned_with_correct_optionality() -> None:
    flat = flatten_parameter_variants(STORAGE_CREATE)
    props = flat["properties"]
    assert flat["type"] == "object"
    assert set(props) == {"storage", "path", "content", "server", "export", "type"}
    assert "optional" not in props["storage"]
    # Required in dir but optional in nfs -> optional overall.
    assert props["path"]["optional"] == 1
    assert "x-proxmox-instance-types" not in props["path"]  # accepted by every variant
    # Only nfs knows these -> optional, tagged with the variant.
    assert props["server"]["optional"] == 1
    assert props["server"]["x-proxmox-instance-types"] == ["nfs"]
    # Discriminator is exposed as an optional enum.
    assert props["type"]["enum"] == ["dir", "nfs"]
    assert props["type"]["optional"] == 1
    for removed in ("allOf", "oneOf", "type-property", "type-property-schema"):
        assert removed not in flat


def test_property_required_in_every_variant_stays_required() -> None:
    schema = {
        "type-property": "resource-type",
        "type-property-schema": {"type": "string", "enum": ["ct", "vm"]},
        "oneOf": [
            {"instance-type": "ct", "properties": {"sid": {"type": "string"}}},
            {
                "instance-type": "vm",
                "properties": {
                    "sid": {"type": "string"},
                    "with-conntrack-state": {"type": "boolean", "optional": 1},
                },
            },
        ],
    }
    props = flatten_parameter_variants(schema)["properties"]
    assert "optional" not in props["sid"]
    assert "x-proxmox-instance-types" not in props["sid"]
    assert props["with-conntrack-state"]["x-proxmox-instance-types"] == ["vm"]


def test_flattening_does_not_mutate_input() -> None:
    before = json.dumps(STORAGE_CREATE, sort_keys=True)
    flatten_parameter_variants(STORAGE_CREATE)
    assert json.dumps(STORAGE_CREATE, sort_keys=True) == before


def test_normalized_operation_keeps_request_body_for_variant_schema() -> None:
    capture = RawMethodCapture(
        method="POST", path="/storage", parameters=STORAGE_CREATE, source="apidoc-fallback"
    )
    operation = NormalizedOperation.from_capture(
        path="/storage", method="POST", method_data=capture
    )
    body = operation.request_body_schema
    assert body is not None
    assert {"storage", "path", "server", "type"} <= set(body["properties"])
    assert body["required"] == ["storage"]


@pytest.mark.parametrize("tag", ["9.3", "latest"])
@pytest.mark.parametrize(
    ("path", "method", "expected"),
    [
        ("/storage", "post", {"storage", "type", "path", "server", "content"}),
        ("/storage/{storage}", "put", {"content", "disable"}),
        ("/cluster/ha/rules", "post", {"rule", "type", "resources"}),
        ("/cluster/ha/rules/{rule}", "put", {"type", "resources"}),
        ("/cluster/ha/resources/{sid}/migrate", "post", {"node", "skip-config-check"}),
    ],
)
def test_generated_9_3_variant_operations_keep_request_contract(
    tag: str, path: str, method: str, expected: set[str]
) -> None:
    schema = json.loads((GENERATED / tag / "openapi.json").read_text())
    operation = schema["paths"][path][method]
    body = operation.get("requestBody", {}).get("content", {}).get("application/json", {})
    names = set((body.get("schema") or {}).get("properties") or {})
    names |= {p["name"] for p in operation.get("parameters", []) if isinstance(p, dict)}
    missing = expected - names
    assert not missing, f"{tag} {method.upper()} {path} lost parameters {sorted(missing)}"

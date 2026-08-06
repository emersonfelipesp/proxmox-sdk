from __future__ import annotations

import importlib.util
import sys
from collections.abc import Callable
from pathlib import Path
from types import ModuleType

import pytest

from proxmox_sdk.proxmox_codegen.pydantic_generator import (
    generate_pydantic_model_shards_from_openapi,
    generate_pydantic_models_from_openapi,
)


def _composite_string(default_type: str) -> dict[str, object]:
    default_entry: dict[str, object] = {
        "type": default_type,
        "default_key": 1,
    }
    if default_type == "integer":
        default_entry["minimum"] = 16
    return {
        "type": "string",
        "format": {
            "value": default_entry,
            "option": {"type": "string", "optional": 1},
        },
    }


def _openapi_fixture() -> dict[str, object]:
    properties = {
        "agent": _composite_string("boolean"),
        "memory": _composite_string("integer"),
        "cpu": _composite_string("string"),
        "disk": _composite_string("string"),
        "freeform": {"type": "string"},
        "net": _composite_string("string"),
    }
    return {
        "info": {"version": "test"},
        "paths": {
            "/nodes/{node}/qemu/{vmid}/config": {
                "get": {
                    "operationId": "get_nodes_node_qemu_vmid_config",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {"type": "object", "properties": properties}
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "content": {
                                "application/json": {
                                    "schema": {"type": "object", "properties": properties}
                                }
                            }
                        }
                    },
                }
            }
        },
    }


def _load_generated_module(tmp_path: Path, code: str, name: str) -> ModuleType:
    module_path = tmp_path / f"{name}.py"
    module_path.write_text(code, encoding="utf-8")
    spec = importlib.util.spec_from_file_location(name, module_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


GENERATORS = [
    pytest.param(generate_pydantic_models_from_openapi, id="aggregate"),
    pytest.param(
        lambda openapi: generate_pydantic_model_shards_from_openapi(openapi)[0]["nodes"],
        id="shard",
    ),
]


@pytest.mark.parametrize("generate", GENERATORS)
def test_generated_responses_accept_only_documented_legacy_scalars(
    generate: Callable[[dict[str, object]], str],
) -> None:
    code = generate(_openapi_fixture())

    assert "agent: StrictBool | Annotated[StrictInt, Field(ge=0, le=1)] | StrictStr | None" in code
    assert "memory: Annotated[StrictInt, Field(ge=16)] | StrictStr | None" in code
    assert "cpu: StrictStr | None" in code
    assert "disk: StrictStr | None" in code
    assert "freeform: StrictStr | None" in code
    assert "net: StrictStr | None" in code


@pytest.mark.parametrize("generate", GENERATORS)
def test_generated_requests_keep_composite_strings_strict(
    generate: Callable[[dict[str, object]], str],
) -> None:
    code = generate(_openapi_fixture())
    request_block, _, response_block = code.partition("class GetNodesNodeQemuVmidConfigResponse")

    assert response_block
    assert "agent: StrictStr | None" in request_block
    assert "memory: StrictStr | None" in request_block
    assert (
        "agent: StrictBool | Annotated[StrictInt, Field(ge=0, le=1)] | StrictStr | None"
        in response_block
    )
    assert "memory: Annotated[StrictInt, Field(ge=16)] | StrictStr | None" in response_block


@pytest.mark.parametrize("generate", GENERATORS)
def test_generated_integer_scalar_preserves_range_and_enum_constraints(
    generate: Callable[[dict[str, object]], str],
) -> None:
    fixture = _openapi_fixture()
    response_schema = fixture["paths"]["/nodes/{node}/qemu/{vmid}/config"]["get"]["responses"][
        "200"
    ]["content"]["application/json"]["schema"]
    response_schema["properties"]["memory"]["format"]["value"].update(
        {"maximum": 64, "multipleOf": 16, "enum": [16, 32, 64]}
    )

    code = generate(fixture)

    assert (
        "Annotated[StrictInt, Field(ge=16, le=64, multiple_of=16, "
        "json_schema_extra={'enum': [16, 32, 64]}), "
        "_allowed_ints((16, 32, 64))] | StrictStr" in code
    )


@pytest.mark.parametrize("generate", GENERATORS)
def test_generated_integer_scalar_runtime_and_json_schema_preserve_constraints(
    generate: Callable[[dict[str, object]], str],
    tmp_path: Path,
) -> None:
    fixture = _openapi_fixture()
    value_schema = fixture["paths"]["/nodes/{node}/qemu/{vmid}/config"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]["properties"]["memory"]["format"]["value"]
    value_schema.update(
        {
            "maximum": 64,
            "exclusiveMinimum": 15,
            "exclusiveMaximum": 65,
            "multipleOf": 16,
            "enum": [16, 32, 64],
        }
    )
    module = _load_generated_module(tmp_path, generate(fixture), "generated_models")
    model = module.GetNodesNodeQemuVmidConfigResponse

    assert model.model_validate({"memory": 32}).memory == 32
    assert model.model_validate({"memory": "48"}).memory == "48"
    for rejected in (True, 15, 48, 65, 32.0):
        with pytest.raises(ValueError):
            model.model_validate({"memory": rejected})

    integer_arm = model.model_json_schema()["properties"]["memory"]["anyOf"][0]
    assert integer_arm == {
        "enum": [16, 32, 64],
        "exclusiveMaximum": 65,
        "exclusiveMinimum": 15,
        "maximum": 64,
        "minimum": 16,
        "multipleOf": 16,
        "type": "integer",
    }


@pytest.mark.parametrize(
    ("format_schema", "expected_type"),
    [
        pytest.param(None, "StrictStr", id="missing-format"),
        pytest.param([], "StrictStr", id="non-object-format"),
        pytest.param(
            {"value": {"type": "integer", "default_key": 0}},
            "StrictStr",
            id="disabled-default-key",
        ),
        pytest.param(
            {"value": {"type": "integer", "default_key": True}},
            "StrictStr",
            id="boolean-default-key",
        ),
        pytest.param(
            {"value": {"type": "integer", "default_key": 1.0}},
            "StrictStr",
            id="floating-default-key",
        ),
        pytest.param(
            {
                "first": {"type": "integer", "default_key": 1},
                "second": {"type": "boolean", "default_key": 1},
            },
            "StrictStr",
            id="ambiguous-default-key",
        ),
        pytest.param(
            {
                "first": {"type": "integer", "default_key": 1},
                "second": {"type": "integer", "default_key": True},
            },
            "StrictStr",
            id="valid-plus-boolean-default-key",
        ),
        pytest.param(
            {
                "first": {"type": "integer", "default_key": 1},
                "second": {"type": "integer", "default_key": 1.0},
            },
            "StrictStr",
            id="valid-plus-floating-default-key",
        ),
        pytest.param(
            {
                "first": {"type": "integer", "default_key": 1},
                "second": {"type": "integer", "default_key": "1"},
            },
            "StrictStr",
            id="valid-plus-string-default-key",
        ),
        pytest.param(
            {"value": {"type": "number", "default_key": 1}},
            "StrictStr",
            id="unsupported-number-default",
        ),
        pytest.param(
            {"value": {"type": "object", "default_key": 1}},
            "StrictStr",
            id="unsupported-object-default",
        ),
    ],
)
@pytest.mark.parametrize("generate", GENERATORS)
def test_malformed_or_unsupported_formats_do_not_widen_response_fields(
    generate: Callable[[dict[str, object]], str],
    format_schema: object,
    expected_type: str,
) -> None:
    fixture = _openapi_fixture()
    response_schema = fixture["paths"]["/nodes/{node}/qemu/{vmid}/config"]["get"]["responses"][
        "200"
    ]["content"]["application/json"]["schema"]
    assert isinstance(response_schema, dict)
    response_schema["properties"] = {"candidate": {"type": "string", "format": format_schema}}

    code = generate(fixture)
    _, _, response_block = code.partition("class GetNodesNodeQemuVmidConfigResponse")

    assert f"candidate: {expected_type} | None" in response_block


@pytest.mark.parametrize("generate", GENERATORS)
@pytest.mark.parametrize(
    ("constraint", "value"),
    [
        pytest.param("minimum", float("nan"), id="nan-minimum"),
        pytest.param("maximum", float("inf"), id="infinite-maximum"),
        pytest.param("exclusiveMinimum", float("-inf"), id="infinite-exclusive-minimum"),
        pytest.param("multipleOf", float("nan"), id="nan-multiple"),
        pytest.param("multipleOf", float("inf"), id="infinite-multiple"),
        pytest.param("multipleOf", 0, id="zero-multiple"),
        pytest.param("multipleOf", -1, id="negative-multiple"),
    ],
)
def test_malformed_integer_constraints_fail_closed_to_strict_string(
    generate: Callable[[dict[str, object]], str],
    constraint: str,
    value: int | float,
    tmp_path: Path,
) -> None:
    fixture = _openapi_fixture()
    response_schema = fixture["paths"]["/nodes/{node}/qemu/{vmid}/config"]["get"]["responses"][
        "200"
    ]["content"]["application/json"]["schema"]
    response_schema["properties"] = {
        "candidate": {
            "type": "string",
            "format": {
                "value": {
                    "type": "integer",
                    "default_key": 1,
                    constraint: value,
                }
            },
        }
    }

    code = generate(fixture)
    _, _, response_block = code.partition("class GetNodesNodeQemuVmidConfigResponse")
    assert "candidate: StrictStr | None" in response_block

    module = _load_generated_module(tmp_path, code, "generated_malformed_models")
    model = module.GetNodesNodeQemuVmidConfigResponse
    assert model.model_validate({"candidate": "16"}).candidate == "16"
    with pytest.raises(ValueError):
        model.model_validate({"candidate": 16})

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest
from pydantic import ValidationError

from proxmox_sdk import schema as schema_module
from proxmox_sdk.mock.loader import load_mock_data
from proxmox_sdk.routes.generated_artifacts import load_operation_model
from proxmox_sdk.schema import load_proxmox_generated_openapi

SUPPORTED_TAGS = ["latest", "9.2", "9.1.11"]


def _load_pydantic_models(tag: str) -> ModuleType:
    """Load generated ``pydantic_models.py`` by file path.

    ``importlib.import_module`` cannot resolve dotted paths whose segments
    aren't valid Python identifiers (``9.1.11``), so load directly off disk.
    """
    path = (
        Path(__file__).resolve().parent.parent
        / "proxmox_sdk"
        / "generated"
        / "proxmox"
        / tag
        / "pydantic_models.py"
    )
    spec = importlib.util.spec_from_file_location(
        f"_proxmox_pydantic_models_{tag.replace('.', '_').replace('-', '_')}",
        path,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_load_mock_data_rejects_json_array(tmp_path: Path) -> None:
    mock_file = tmp_path / "mock-data.json"
    mock_file.write_text("[]", encoding="utf-8")

    assert load_mock_data(mock_file) is None


def test_load_mock_data_rejects_yaml_scalar(tmp_path: Path) -> None:
    mock_file = tmp_path / "mock-data.yaml"
    mock_file.write_text("- item\n- item2\n", encoding="utf-8")

    assert load_mock_data(mock_file) is None


def test_load_generated_openapi_rejects_non_object(tmp_path: Path, monkeypatch) -> None:
    version_dir = tmp_path / "latest"
    version_dir.mkdir(parents=True)
    (version_dir / "openapi.json").write_text("[]", encoding="utf-8")

    monkeypatch.setattr(schema_module, "_generated_dir", lambda: tmp_path)

    assert load_proxmox_generated_openapi("latest") is None


def test_load_generated_openapi_rejects_malformed_json(tmp_path: Path, monkeypatch) -> None:
    version_dir = tmp_path / "latest"
    version_dir.mkdir(parents=True)
    (version_dir / "openapi.json").write_text("{", encoding="utf-8")

    monkeypatch.setattr(schema_module, "_generated_dir", lambda: tmp_path)

    assert load_proxmox_generated_openapi("latest") is None


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
def test_supported_tag_loads_non_empty_openapi(tag: str) -> None:
    spec = load_proxmox_generated_openapi(tag)
    assert isinstance(spec, dict), f"tag {tag!r} did not load an OpenAPI document"
    assert spec["info"]["version"] == tag
    paths = spec.get("paths") or {}
    assert len(paths) >= 400, (
        f"tag {tag!r} loaded only {len(paths)} paths; sanity floor 400 not met"
    )


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
def test_supported_tag_pydantic_models_import_cleanly(tag: str) -> None:
    module = _load_pydantic_models(tag)
    assert hasattr(module, "ProxmoxBaseModel"), (
        f"pydantic_models for tag {tag!r} did not expose ProxmoxBaseModel"
    )


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
def test_qemu_config_models_accept_legacy_response_scalars(tag: str) -> None:
    model = load_operation_model(
        tag,
        "get_nodes_node_qemu_vmid_config",
        "response",
    )
    assert model is not None

    for agent, memory, expected_agent in (
        (True, 2048, True),
        (1, "4096", 1),
        ("1", 6144, "1"),
        ("enabled=1,fstrim_cloned_disks=1", 8192, "enabled=1,fstrim_cloned_disks=1"),
    ):
        config = model.model_validate({"agent": agent, "digest": "test-digest", "memory": memory})
        assert config.agent == expected_agent
        assert config.memory == memory
        assert isinstance(config.memory, type(memory))


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
def test_qemu_config_models_keep_composite_fields_as_strings(tag: str) -> None:
    model = load_operation_model(
        tag,
        "get_nodes_node_qemu_vmid_config",
        "response",
    )
    assert model is not None

    config = model.model_validate(
        {
            "cpu": "host,flags=+aes",
            "digest": "test-digest",
            "net[n]": "virtio=52:54:00:12:34:56,bridge=vmbr0",
            "scsi[n]": "local-lvm:vm-100-disk-0,size=32G",
        }
    )
    assert config.cpu == "host,flags=+aes"
    assert config.net_n == "virtio=52:54:00:12:34:56,bridge=vmbr0"
    assert config.scsi_n == "local-lvm:vm-100-disk-0,size=32G"


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
@pytest.mark.parametrize("field", ["cpu", "net[n]", "scsi[n]"])
@pytest.mark.parametrize("value", [b"legacy-composite", bytearray(b"legacy-composite")])
def test_qemu_config_response_composite_strings_reject_bytes(
    tag: str,
    field: str,
    value: bytes | bytearray,
) -> None:
    model = load_operation_model(
        tag,
        "get_nodes_node_qemu_vmid_config",
        "response",
    )
    assert model is not None

    with pytest.raises(ValidationError) as caught:
        model.model_validate({"digest": "test-digest", field: value})

    locations = [tuple(error["loc"]) for error in caught.value.errors()]
    assert locations and all(location[0] == field for location in locations)


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
@pytest.mark.parametrize("field", ["agent", "memory"])
@pytest.mark.parametrize("value", [b"1", bytearray(b"1")])
def test_qemu_config_response_widened_string_arms_reject_bytes(
    tag: str,
    field: str,
    value: bytes | bytearray,
) -> None:
    model = load_operation_model(
        tag,
        "get_nodes_node_qemu_vmid_config",
        "response",
    )
    assert model is not None

    with pytest.raises(ValidationError) as caught:
        model.model_validate({"digest": "test-digest", field: value})

    locations = [tuple(error["loc"]) for error in caught.value.errors()]
    assert locations and all(location[0] == field for location in locations)


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
@pytest.mark.parametrize(
    "payload",
    [
        {"agent": 2},
        {"agent": 1.0},
        {"agent": {"enabled": True}},
        {"memory": True},
        {"memory": 15},
        {"memory": 4096.5},
        {"memory": {"current": 4096}},
        {"cpu": 4},
        {"net[n]": {"bridge": "vmbr0"}},
    ],
)
def test_qemu_config_models_reject_malformed_scalar_and_composite_values(
    tag: str,
    payload: dict[str, object],
) -> None:
    model = load_operation_model(
        tag,
        "get_nodes_node_qemu_vmid_config",
        "response",
    )
    assert model is not None

    with pytest.raises(ValidationError):
        model.model_validate({"digest": "test-digest", **payload})


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
@pytest.mark.parametrize(
    "operation_id",
    [
        "post_nodes_node_qemu_vmid_config",
        "put_nodes_node_qemu_vmid_config",
    ],
)
@pytest.mark.parametrize(
    "payload",
    [
        {"agent": True},
        {"agent": 1},
        {"agent": b"1"},
        {"memory": 4096},
        {"memory": b"4096"},
    ],
)
def test_qemu_config_request_models_keep_legacy_scalars_strict(
    tag: str,
    operation_id: str,
    payload: dict[str, object],
) -> None:
    model = load_operation_model(tag, operation_id, "request")
    assert model is not None

    with pytest.raises(ValidationError):
        model.model_validate(payload)


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
@pytest.mark.parametrize(
    "operation_id",
    [
        "post_nodes_node_qemu_vmid_config",
        "put_nodes_node_qemu_vmid_config",
    ],
)
def test_qemu_config_request_models_accept_composite_strings(
    tag: str,
    operation_id: str,
) -> None:
    model = load_operation_model(tag, operation_id, "request")
    assert model is not None

    config = model.model_validate({"agent": "1", "memory": "4096"})

    assert config.agent == "1"
    assert config.memory == "4096"

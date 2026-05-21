from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType

import pytest

from proxmox_sdk import schema as schema_module
from proxmox_sdk.mock.loader import load_mock_data
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

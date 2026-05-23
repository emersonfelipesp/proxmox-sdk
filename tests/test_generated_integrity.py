"""Integrity guard for the generated Pydantic schema artifacts.

For each supported schema tag, recomputes ``SHA-256(openapi.json)`` and asserts
equality with ``GENERATED_SOURCE_SHA256`` declared at the top of the matching
``proxmox_sdk/generated/proxmox/<tag>/pydantic_models.py``.

When the OpenAPI source legitimately changes, regenerate the models and bump
``GENERATED_SOURCE_SHA256`` (and ``GENERATED_AT``) to match the new source.
"""

import hashlib
import importlib.util
import json
from pathlib import Path
from types import ModuleType

import pytest

SUPPORTED_TAGS = ["latest", "9.2", "9.1.11"]


def _tag_dir(tag: str) -> Path:
    return Path(__file__).resolve().parent.parent / "proxmox_sdk" / "generated" / "proxmox" / tag


def _openapi_path(tag: str) -> Path:
    return _tag_dir(tag) / "openapi.json"


def _route_metadata_path(tag: str) -> Path:
    return _tag_dir(tag) / "route_metadata.json"


def _model_index_path(tag: str) -> Path:
    return _tag_dir(tag) / "model_index.json"


def _load_module(tag: str) -> ModuleType:
    """Load ``pydantic_models.py`` by file path so tags like ``9.1.11`` work.

    The tag is allowed to be any non-Python-identifier release string (e.g.
    ``"9.1.11"``); ``importlib.import_module`` on a dotted path containing a
    digit-leading segment would fail at the ``proxmox_sdk.generated.proxmox.9``
    step.
    """
    path = _tag_dir(tag) / "pydantic_models.py"
    spec = importlib.util.spec_from_file_location(
        f"_proxmox_pydantic_models_{tag.replace('.', '_').replace('-', '_')}",
        path,
    )
    if spec is None or spec.loader is None:
        raise ImportError(f"could not load spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
def test_generated_constants_are_strings(tag: str) -> None:
    mod = _load_module(tag)
    assert isinstance(mod.GENERATED_FOR_PROXMOX_VERSION, str)
    assert isinstance(mod.GENERATED_SOURCE_SHA256, str)
    assert isinstance(mod.GENERATED_AT, str)
    assert len(mod.GENERATED_SOURCE_SHA256) == 64


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
def test_openapi_source_matches_generated_sha256(tag: str) -> None:
    openapi_path = _openapi_path(tag)
    assert openapi_path.is_file(), f"missing source spec: {openapi_path}"
    mod = _load_module(tag)
    actual = _sha256(openapi_path)
    assert actual == mod.GENERATED_SOURCE_SHA256, (
        f"openapi.json drifted from the SHA-256 pinned in pydantic_models.py for tag {tag!r}.\n"
        "Either regenerate the artifact or update GENERATED_SOURCE_SHA256.\n"
        f"  pinned:   {mod.GENERATED_SOURCE_SHA256}\n"
        f"  computed: {actual}\n"
    )


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
def test_generated_version_matches_tag(tag: str) -> None:
    mod = _load_module(tag)
    assert mod.GENERATED_FOR_PROXMOX_VERSION == tag, (
        f"pydantic_models.py for tag {tag!r} declares "
        f"GENERATED_FOR_PROXMOX_VERSION={mod.GENERATED_FOR_PROXMOX_VERSION!r}"
    )


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
def test_route_metadata_matches_openapi(tag: str) -> None:
    openapi = json.loads(_openapi_path(tag).read_text(encoding="utf-8"))
    metadata = json.loads(_route_metadata_path(tag).read_text(encoding="utf-8"))
    expected_routes = sum(
        1
        for path_item in openapi["paths"].values()
        for method in path_item
        if method.upper() in {"GET", "POST", "PUT", "PATCH", "DELETE"}
    )

    assert metadata["source_sha256"] == _sha256(_openapi_path(tag))
    assert metadata["path_count"] == len(openapi["paths"])
    assert metadata["route_count"] == expected_routes
    assert len(metadata["routes"]) == expected_routes


@pytest.mark.parametrize("tag", SUPPORTED_TAGS)
def test_model_index_covers_route_metadata(tag: str) -> None:
    metadata = json.loads(_route_metadata_path(tag).read_text(encoding="utf-8"))
    index = json.loads(_model_index_path(tag).read_text(encoding="utf-8"))

    assert index["source_sha256"] == _sha256(_openapi_path(tag))
    indexed_operations = set(index["operations"])
    metadata_operations = {route["operation_id"] for route in metadata["routes"]}
    assert metadata_operations <= indexed_operations

    for group in index["groups"]:
        assert (_tag_dir(tag) / "models" / f"{group}.py").is_file()

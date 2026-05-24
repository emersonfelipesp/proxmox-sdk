"""HTTP smoke tests for the standalone PVE mock server (create_mock_app)."""

from __future__ import annotations

import os
import sys

import pytest
from fastapi.testclient import TestClient

from proxmox_sdk.mock.app import create_mock_app


@pytest.fixture(autouse=True)
def _use_test_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    """Isolate this file's shared mock state from the default namespace."""
    monkeypatch.setenv("PROXMOX_MOCK_STATE_NAMESPACE", "test_mock_routes")


@pytest.fixture
def client() -> TestClient:
    return TestClient(create_mock_app())


def test_root(client: TestClient) -> None:
    body = client.get("/").json()
    assert body["service"] in ("pve", "all")


def test_health(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ready"}


def test_version(client: TestClient) -> None:
    body = client.get("/version").json()
    assert "version" in body


def test_nodes_list(client: TestClient) -> None:
    r = client.get("/api2/json/nodes")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_node_detail(client: TestClient) -> None:
    nodes = client.get("/api2/json/nodes").json()
    assert nodes, "Mock seeded no nodes"
    node_name = nodes[0]["node"]
    assert client.get(f"/api2/json/nodes/{node_name}").status_code == 200


def test_unknown_path_returns_404(client: TestClient) -> None:
    assert client.get("/api2/json/__nonexistent__xyz").status_code == 404


def test_user_create_persists(client: TestClient) -> None:
    pre_count = len(client.get("/api2/json/access/users").json())
    r = client.post(
        "/api2/json/access/users",
        params={"userid": "citest@pve"},
        json={"userid": "citest@pve"},
    )
    assert r.status_code == 200
    assert len(client.get("/api2/json/access/users").json()) == pre_count + 1


def test_generated_docs_include_proxmox_paths(client: TestClient) -> None:
    body = client.get("/openapi.json").json()
    assert "/api2/json/nodes" in body["paths"]
    assert "/api2/json/access/users" in body["paths"]


def test_lazy_model_loader_imports_route_group_only(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PROXMOX_MOCK_STATE_NAMESPACE", "test_lazy_model_loader")
    monkeypatch.setenv("PROXMOX_MOCK_STORE", "dict")
    version_tag = os.environ.get("PROXMOX_MOCK_SCHEMA_VERSION", "latest")
    module_prefix = f"proxmox_sdk._generated_models.{version_tag.replace('.', '_')}"
    for module_name in list(sys.modules):
        if module_name.startswith(module_prefix):
            sys.modules.pop(module_name, None)
    from proxmox_sdk.routes import generated_artifacts

    generated_artifacts._load_model_module.cache_clear()

    assert f"{module_prefix}.aggregate" not in sys.modules

    model = generated_artifacts.load_operation_model(
        version_tag,
        "get_nodes",
        "response",
        group="nodes",
        model_name="GetNodesResponse",
    )

    assert model is not None
    assert model.__name__ == "GetNodesResponse"
    assert f"{module_prefix}.nodes" in sys.modules
    assert f"{module_prefix}.aggregate" not in sys.modules

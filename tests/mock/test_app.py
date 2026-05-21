"""HTTP smoke tests for the full create_app() server in mock mode."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from proxmox_sdk.main import create_app


@pytest.fixture(autouse=True)
def _use_test_namespace(monkeypatch: pytest.MonkeyPatch) -> None:
    """Isolate this file's shared mock state from the default namespace."""
    monkeypatch.setenv("PROXMOX_MOCK_STATE_NAMESPACE", "test_mock_app")


@pytest.fixture
def client(monkeypatch: pytest.MonkeyPatch) -> TestClient:
    monkeypatch.setenv("TESTING", "1")
    monkeypatch.setenv("PROXMOX_API_MODE", "mock")
    return TestClient(create_app())


def test_root(client: TestClient) -> None:
    body = client.get("/").json()
    assert "version" in body


def test_health(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ready"}


def test_version(client: TestClient) -> None:
    body = client.get("/version").json()
    assert "version" in body


def test_mode(client: TestClient) -> None:
    body = client.get("/mode").json()
    assert body["mode"] == "mock"


def test_versions_list(client: TestClient) -> None:
    r = client.get("/versions/")
    assert r.status_code == 200
    assert "versions" in r.json()


def test_mock_sub_router(client: TestClient) -> None:
    r = client.get("/mock/")
    assert r.status_code == 200
    assert r.json()["message"] == "Proxmox OpenAPI Mock Server"


def test_api_nodes(client: TestClient) -> None:
    r = client.get("/api2/json/nodes")
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_health_blocked_without_testing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TESTING", raising=False)
    monkeypatch.setenv("PROXMOX_API_MODE", "mock")
    no_test_client = TestClient(create_app(), raise_server_exceptions=False)
    assert no_test_client.get("/health").status_code == 404

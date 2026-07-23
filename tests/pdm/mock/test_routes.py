"""HTTP-level tests against the FastAPI PDM mock app."""

from __future__ import annotations

from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from proxmox_sdk.pdm_mock_main import create_pdm_mock_app


@pytest.fixture
def client() -> Iterator[TestClient]:
    with TestClient(create_pdm_mock_app()) as test_client:
        yield test_client


def test_health_and_root(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ready"}
    root = client.get("/").json()
    assert "Proxmox Datacenter Manager" in root["message"]


def test_version_endpoint(client: TestClient) -> None:
    body = client.get("/api2/json/version").json()
    assert "data" in body
    assert body["data"]["version"].startswith("1.0")


def test_remotes_list_returns_three(client: TestClient) -> None:
    body = client.get("/api2/json/remotes/remote").json()
    assert len(body["data"]) == 3


def test_remotes_create_get_delete_round_trip(client: TestClient) -> None:
    assert (
        client.post(
            "/api2/json/remotes/remote",
            json={"id": "pve-new", "type": "pve", "authid": "root@pam!api"},
        ).status_code
        == 200
    )
    body = client.get("/api2/json/remotes/remote/pve-new").json()
    assert body["data"]["id"] == "pve-new"
    assert client.delete("/api2/json/remotes/remote/pve-new").status_code == 200
    assert client.get("/api2/json/remotes/remote/pve-new").status_code == 404


def test_remote_update_persists_field(client: TestClient) -> None:
    client.put("/api2/json/remotes/remote/pve-cluster-a", json={"fingerprint": "ZZ"})
    body = client.get("/api2/json/remotes/remote/pve-cluster-a").json()
    assert body["data"]["fingerprint"] == "ZZ"


def test_remote_version_endpoint(client: TestClient) -> None:
    body = client.get("/api2/json/remotes/remote/pve-cluster-a/version").json()
    assert body["data"]["version"].startswith("9."), (
        f"expected a 9.x PVE version, got {body['data']['version']!r}"
    )


def test_pve_qemu_list_and_lifecycle(client: TestClient) -> None:
    body = client.get("/api2/json/pve/remotes/pve-cluster-a/qemu").json()
    assert len(body["data"]) == 10
    assert client.post("/api2/json/pve/remotes/pve-cluster-a/qemu/100/stop").status_code == 200
    # Status now reflects the mutation.
    body = client.get("/api2/json/pve/remotes/pve-cluster-a/qemu").json()
    by_id = {g["vmid"]: g for g in body["data"]}
    assert by_id[100]["status"] == "stopped"
    assert client.post("/api2/json/pve/remotes/pve-cluster-a/qemu/100/start").status_code == 200
    body = client.get("/api2/json/pve/remotes/pve-cluster-a/qemu").json()
    by_id = {g["vmid"]: g for g in body["data"]}
    assert by_id[100]["status"] == "running"


def test_pve_guest_config(client: TestClient) -> None:
    body = client.get("/api2/json/pve/remotes/pve-cluster-a/qemu/100/config").json()
    assert body["data"]["name"] == "web-prod-1"


def test_pve_resources_with_type_filter(client: TestClient) -> None:
    body = client.get("/api2/json/pve/remotes/pve-cluster-a/resources?type=qemu").json()
    assert all(e["type"] == "qemu" for e in body["data"])


def test_pbs_datastore_and_snapshots(client: TestClient) -> None:
    ds = client.get("/api2/json/pbs/remotes/pbs-main/datastore").json()
    assert {d["store"] for d in ds["data"]} == {"tank", "cold"}
    snaps = client.get("/api2/json/pbs/remotes/pbs-main/datastore/tank/snapshots?ns=prod").json()
    assert len(snaps["data"]) == 2


def test_pbs_node_rrddata(client: TestClient) -> None:
    body = client.get("/api2/json/pbs/remotes/pbs-main/rrddata").json()
    assert isinstance(body["data"], list) and body["data"]


def test_resources_endpoints(client: TestClient) -> None:
    assert len(client.get("/api2/json/resources/list").json()["data"]) > 0
    assert len(client.get("/api2/json/resources/status").json()["data"]) == 3
    assert len(client.get("/api2/json/resources/subscription").json()["data"]) == 3


def test_metrics_status_and_trigger(client: TestClient) -> None:
    assert (
        client.get("/api2/json/remotes/metric-collection/status").json()["data"]["enabled"] is True
    )
    body = client.post("/api2/json/remotes/metric-collection/trigger").json()
    assert "UPID" in body["data"]


def test_views_crud(client: TestClient) -> None:
    assert (
        client.post("/api2/json/config/views", json={"id": "dev", "name": "Dev"}).status_code == 200
    )
    body = client.get("/api2/json/config/views/dev").json()
    assert body["data"]["name"] == "Dev"
    client.put("/api2/json/config/views/dev", json={"comment": "test"})
    body = client.get("/api2/json/config/views/dev").json()
    assert body["data"]["comment"] == "test"
    assert client.delete("/api2/json/config/views/dev").status_code == 200
    assert client.get("/api2/json/config/views/dev").status_code == 404


def test_users_full_crud(client: TestClient) -> None:
    client.post("/api2/json/access/users", json={"userid": "x@pdm", "enable": True})
    assert client.get("/api2/json/access/users/x%40pdm").json()["data"]["userid"] == "x@pdm"
    client.put("/api2/json/access/users/x%40pdm", json={"comment": "updated"})
    assert client.get("/api2/json/access/users/x%40pdm").json()["data"]["comment"] == "updated"
    assert client.delete("/api2/json/access/users/x%40pdm").status_code == 200


def test_password_change_uses_user_update_endpoint(client: TestClient) -> None:
    r = client.put(
        "/api2/json/access/users/root%40pam",
        json={"password": "newpw"},
    )
    assert r.status_code == 200


def test_acl_add_then_delete(client: TestClient) -> None:
    pre = len(client.get("/api2/json/access/acl").json()["data"])
    client.put(
        "/api2/json/access/acl",
        json={"path": "/remote/pve-cluster-a", "roles": "PVEAuditor", "users": "ops@pdm"},
    )
    after = len(client.get("/api2/json/access/acl").json()["data"])
    assert after == pre + 1
    client.put(
        "/api2/json/access/acl",
        json={
            "path": "/remote/pve-cluster-a",
            "roles": "PVEAuditor",
            "users": "ops@pdm",
            "delete": 1,
        },
    )
    assert len(client.get("/api2/json/access/acl").json()["data"]) == pre


def test_tfa_add_then_delete(client: TestClient) -> None:
    r = client.post("/api2/json/access/tfa/ops%40pdm", json={"type": "totp"})
    factor_id = r.json()["data"]["id"]
    body = client.get("/api2/json/access/tfa/ops%40pdm").json()
    assert any(f["id"] == factor_id for f in body["data"])
    assert client.delete(f"/api2/json/access/tfa/ops%40pdm/{factor_id}").status_code == 200


def test_api_token_crud(client: TestClient) -> None:
    client.post("/api2/json/access/users/ops%40pdm/token/api", json={"comment": "ro"})
    body = client.get("/api2/json/access/users/ops%40pdm/token").json()
    assert any(t["tokenid"] == "api" for t in body["data"])
    assert client.delete("/api2/json/access/users/ops%40pdm/token/api").status_code == 200


def test_mock_export_seed_reset_round_trip(client: TestClient) -> None:
    snapshot = client.get("/mock/export").json()
    # Replace state with one containing exactly one remote.
    new_state = {"remotes": [{"id": "only", "type": "pve"}], "pve": {}, "pbs": {}}
    client.post("/mock/seed", json=new_state)
    assert len(client.get("/api2/json/remotes/remote").json()["data"]) == 1
    # Restore through /mock/import.
    client.request("POST", "/mock/import", json=snapshot)
    assert len(client.get("/api2/json/remotes/remote").json()["data"]) == 3
    # /mock/reset rolls back to bundled defaults.
    client.delete("/mock/reset")
    assert len(client.get("/api2/json/remotes/remote").json()["data"]) == 3

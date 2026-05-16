"""End-to-end tests driving :class:`PDMClient` against the FastAPI mock.

Uses ``httpx.ASGITransport`` so the SDK speaks to the mock app over an
in-process ASGI loop — no sockets, no ports, no flakiness.
"""

from __future__ import annotations

from typing import Any

import pytest
from fastapi.testclient import TestClient

from proxmox_sdk.pdm import PDMClient
from proxmox_sdk.pdm_mock_main import create_pdm_mock_app
from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.backends.base import AbstractBackend
from proxmox_sdk.sdk.resource import ProxmoxResource
from proxmox_sdk.sdk.services import SERVICES


class _TestClientBackend(AbstractBackend):
    """Bridge :class:`fastapi.testclient.TestClient` into the SDK transport."""

    def __init__(self, app_client: TestClient) -> None:
        self._client = app_client
        self.calls: list[tuple[str, str]] = []

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        self.calls.append((method, path))
        kwargs: dict[str, Any] = {"params": params or None}
        if data is not None:
            kwargs["json"] = data
        resp = self._client.request(method, path, **kwargs)
        if resp.status_code >= 400:
            raise AssertionError(f"{method} {path} -> {resp.status_code} {resp.text}")
        if resp.headers.get("content-type", "").startswith("application/json"):
            return resp.json()
        return resp.text

    async def close(self) -> None:
        return None


@pytest.fixture
def pdm_client() -> PDMClient:
    app = create_pdm_mock_app()
    tc = TestClient(app)
    svc = SERVICES["PDM"]
    backend = _TestClientBackend(tc)
    sdk = object.__new__(ProxmoxSDK)
    sdk._service_name = "PDM"
    sdk._service_config = svc
    sdk._backend_name = "fastapi-testclient"
    sdk._backend = backend
    sdk._root = ProxmoxResource(path=svc.api_path_prefix, backend=backend)
    return PDMClient(_sdk=sdk)


async def test_version_through_sdk(pdm_client: PDMClient) -> None:
    v = await pdm_client.version()
    assert v.version.startswith("1.0")


async def test_remotes_list_through_sdk(pdm_client: PDMClient) -> None:
    remotes = await pdm_client.remotes.list()
    assert {r.id for r in remotes} == {"pve-cluster-a", "pve-cluster-b", "pbs-main"}


async def test_pve_qemu_list_and_lifecycle(pdm_client: PDMClient) -> None:
    guests = await pdm_client.pve.qemu.list("pve-cluster-a")
    assert len(guests) == 10
    upid_stop = await pdm_client.pve.qemu.stop("pve-cluster-a", 100)
    assert "stop" in upid_stop
    guests = await pdm_client.pve.qemu.list("pve-cluster-a")
    stopped = next(g for g in guests if g.vmid == 100)
    assert stopped.status == "stopped"


async def test_pbs_snapshots_filter(pdm_client: PDMClient) -> None:
    snaps = await pdm_client.pbs.snapshots("pbs-main", "tank", namespace="prod")
    assert len(snaps) == 2
    assert all(s.namespace == "prod" for s in snaps)


async def test_global_resources_and_subscriptions(pdm_client: PDMClient) -> None:
    res = await pdm_client.resources.list()
    assert len(res) > 0
    subs = await pdm_client.subscriptions.list()
    assert len(subs) == 3


async def test_views_crud_through_sdk(pdm_client: PDMClient) -> None:
    await pdm_client.views.create(id="ops-dash", name="Operations")
    v = await pdm_client.views.get("ops-dash")
    assert v.name == "Operations"
    await pdm_client.views.update("ops-dash", comment="updated")
    v = await pdm_client.views.get("ops-dash")
    assert v.comment == "updated"
    await pdm_client.views.delete("ops-dash")


async def test_users_crud_through_sdk(pdm_client: PDMClient) -> None:
    await pdm_client.access.users.create(userid="e2e@pdm", comment="e2e")
    fetched = await pdm_client.access.users.get("e2e@pdm")
    assert fetched.userid == "e2e@pdm"
    await pdm_client.access.users.update("e2e@pdm", comment="updated")
    await pdm_client.access.users.delete("e2e@pdm")


async def test_acl_round_trip(pdm_client: PDMClient) -> None:
    before = await pdm_client.access.acl.list()
    await pdm_client.access.acl.update(
        path="/remote/pve-cluster-a", roles="PVEAuditor", users="ops@pdm"
    )
    after = await pdm_client.access.acl.list()
    assert len(after) == len(before) + 1
    await pdm_client.access.acl.delete(
        path="/remote/pve-cluster-a", roles="PVEAuditor", users="ops@pdm"
    )
    final = await pdm_client.access.acl.list()
    assert len(final) == len(before)


async def test_metrics_status_through_sdk(pdm_client: PDMClient) -> None:
    s = await pdm_client.metrics.status()
    assert s.enabled is True

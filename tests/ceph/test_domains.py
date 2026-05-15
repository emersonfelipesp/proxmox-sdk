"""Domain helper tests for the read-only Ceph facade."""

from __future__ import annotations

from typing import Any

import pytest

from proxmox_sdk.ceph import CephClient, SyncCephClient
from proxmox_sdk.ceph import models as m
from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.backends.base import AbstractBackend
from proxmox_sdk.sdk.resource import ProxmoxResource
from proxmox_sdk.sdk.services import SERVICES


class _RecordingBackend(AbstractBackend):
    """Records requested paths and replays canned responses by path."""

    def __init__(self, responses: dict[str, Any]) -> None:
        self.responses = responses
        self.calls: list[tuple[str, str, dict[str, Any] | None]] = []

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        self.calls.append((method, path, params))
        if path not in self.responses:
            raise AssertionError(f"unexpected path: {path}")
        return self.responses[path]

    async def close(self) -> None:
        return None


def _make_sdk(responses: dict[str, Any]) -> tuple[ProxmoxSDK, _RecordingBackend]:
    svc = SERVICES["PVE"]
    backend = _RecordingBackend(responses)
    sdk = object.__new__(ProxmoxSDK)
    sdk._service_config = svc
    sdk._backend_name = "recording"
    sdk._backend = backend
    sdk._root = ProxmoxResource(path=svc.api_path_prefix, backend=backend)
    return sdk, backend


async def test_cluster_status_hits_pve_ceph_path():
    sdk, backend = _make_sdk(
        {"/api2/json/cluster/ceph/status": {"data": {"health": {"status": "HEALTH_OK"}}}}
    )
    ceph = CephClient(_sdk=sdk)
    status = await ceph.status()
    assert isinstance(status, m.CephClusterStatus)
    assert status.health == {"status": "HEALTH_OK"}
    assert backend.calls[0][1] == "/api2/json/cluster/ceph/status"


async def test_cluster_flags_normalize_mapping_payloads():
    sdk, _ = _make_sdk({"/api2/json/cluster/ceph/flags": {"data": {"noout": True}}})
    ceph = CephClient(_sdk=sdk)
    flags = await ceph.cluster.flags()
    assert flags[0].name == "noout"
    assert flags[0].value is True


async def test_node_daemon_and_pool_paths():
    sdk, backend = _make_sdk(
        {
            "/api2/json/nodes/pve1/ceph/mon": {"data": [{"name": "pve1"}]},
            "/api2/json/nodes/pve1/ceph/pool": {
                "data": [{"pool_name": "rbd", "size": 3, "min_size": 2}]
            },
        }
    )
    ceph = CephClient(_sdk=sdk)
    mons = await ceph.nodes.monitors("pve1")
    pools = await ceph.nodes.pools("pve1")
    assert mons[0].daemon_type == "mon"
    assert pools[0].name == "rbd"
    assert [call[1] for call in backend.calls] == [
        "/api2/json/nodes/pve1/ceph/mon",
        "/api2/json/nodes/pve1/ceph/pool",
    ]


async def test_osd_detail_preserves_requested_id():
    sdk, _ = _make_sdk({"/api2/json/nodes/pve1/ceph/osd/7": {"data": {"up": 1, "in": 1}}})
    ceph = CephClient(_sdk=sdk)
    osd = await ceph.nodes.osd("pve1", 7)
    assert osd.osd_id == 7
    assert osd.in_cluster == 1


async def test_from_sdk_rejects_non_pve():
    pbs_sdk = ProxmoxSDK.mock(service="PBS")
    try:
        with pytest.raises(ValueError):
            CephClient.from_sdk(pbs_sdk)
    finally:
        await pbs_sdk.close()


def test_sync_client_blocks_and_returns_typed_models():
    sdk, _ = _make_sdk(
        {
            "/api2/json/cluster/ceph/status": {"data": {"health": "HEALTH_WARN"}},
            "/api2/json/nodes/pve1/ceph/osd": {"data": [{"id": 0, "up": 1}]},
        }
    )
    client = SyncCephClient(_sdk=sdk)
    try:
        assert client.status().health == "HEALTH_WARN"
        assert client.nodes.osds("pve1")[0].osd_id == 0
    finally:
        client.close()

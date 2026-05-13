"""Domain helper tests for the read-only PBS facade.

Each test wires a recording backend onto :class:`ProxmoxSDK` so we can assert
both the issued path and the parsed return value without touching network.
"""

from __future__ import annotations

from typing import Any

import pytest

from proxmox_sdk.pbs import PBSClient, SyncPBSClient
from proxmox_sdk.pbs import models as m
from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.backends.base import AbstractBackend
from proxmox_sdk.sdk.resource import ProxmoxResource
from proxmox_sdk.sdk.services import SERVICES


class _RecordingBackend(AbstractBackend):
    """Records the requested path and replays canned responses by path."""

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
    svc = SERVICES["PBS"]
    backend = _RecordingBackend(responses)
    sdk = object.__new__(ProxmoxSDK)
    sdk._service_config = svc
    sdk._backend_name = "recording"
    sdk._backend = backend
    sdk._root = ProxmoxResource(path=svc.api_path_prefix, backend=backend)
    return sdk, backend


async def test_datastores_list_hits_admin_datastore():
    sdk, backend = _make_sdk(
        {
            "/api2/json/admin/datastore": {
                "data": [
                    {"store": "tank", "total": 1000, "used": 100},
                    {"store": "cold", "total": 2000, "used": 500},
                ]
            }
        }
    )
    pbs = PBSClient(_sdk=sdk)
    stores = await pbs.datastores.list()
    assert [s.name for s in stores] == ["tank", "cold"]
    assert backend.calls[0][1] == "/api2/json/admin/datastore"


async def test_datastore_usage_hits_status_path():
    sdk, backend = _make_sdk(
        {"/api2/json/admin/datastore/tank/status": {"data": {"total": 1000, "used": 100}}}
    )
    pbs = PBSClient(_sdk=sdk)
    d = await pbs.datastores.usage("tank")
    assert d.name == "tank"
    assert d.used == 100
    assert backend.calls[0][1] == "/api2/json/admin/datastore/tank/status"


async def test_snapshot_groups_and_list():
    sdk, _ = _make_sdk(
        {
            "/api2/json/admin/datastore/tank/groups": {
                "data": [{"backup-type": "vm", "backup-id": "100"}]
            },
            "/api2/json/admin/datastore/tank/snapshots": {
                "data": [
                    {"backup-type": "vm", "backup-id": "100", "backup-time": 1700000000},
                ]
            },
        }
    )
    pbs = PBSClient(_sdk=sdk)
    groups = await pbs.snapshots.groups("tank")
    assert groups[0].backup_type == "vm"
    snaps = await pbs.snapshots.list("tank")
    assert snaps[0].backup_id == "100"


async def test_snapshots_list_filters_pass_through_as_hyphenated_params():
    sdk, backend = _make_sdk({"/api2/json/admin/datastore/tank/snapshots": {"data": []}})
    pbs = PBSClient(_sdk=sdk)
    await pbs.snapshots.list("tank", backup_type="vm", backup_id="100")
    assert backend.calls[0][2] == {"backup-type": "vm", "backup-id": "100"}


async def test_jobs_list_iterates_all_four_config_endpoints():
    sdk, backend = _make_sdk(
        {
            "/api2/json/config/verify": {"data": [{"id": "v1"}]},
            "/api2/json/config/prune": {"data": [{"id": "p1"}]},
            "/api2/json/config/sync": {"data": [{"id": "s1"}]},
            "/api2/json/config/tape-backup-job": {"data": [{"id": "t1"}]},
        }
    )
    pbs = PBSClient(_sdk=sdk)
    jobs = await pbs.jobs.list()
    assert {j.job_type for j in jobs} == {"verify", "prune", "sync", "tape"}
    paths = [c[1] for c in backend.calls]
    assert "/api2/json/config/tape-backup-job" in paths


async def test_jobs_list_rejects_gc():
    sdk, _ = _make_sdk({})
    pbs = PBSClient(_sdk=sdk)
    with pytest.raises(ValueError, match="Datastores.usage"):
        await pbs.jobs.list(job_type="gc")


async def test_node_status_path():
    sdk, backend = _make_sdk(
        {"/api2/json/nodes/localhost/status": {"data": {"uptime": 99, "cpu": 0.1}}}
    )
    pbs = PBSClient(_sdk=sdk)
    ns = await pbs.nodes.status("localhost")
    assert ns.uptime == 99
    assert backend.calls[0][1] == "/api2/json/nodes/localhost/status"


async def test_version_unwraps_data_envelope():
    sdk, _ = _make_sdk({"/api2/json/version": {"data": {"version": "3.2.7", "release": "1"}}})
    pbs = PBSClient(_sdk=sdk)
    v = await pbs.version()
    assert isinstance(v, m.PBSVersion)
    assert v.version == "3.2.7"


async def test_from_sdk_rejects_non_pbs():
    pve_sdk = ProxmoxSDK.mock(service="PVE")
    try:
        with pytest.raises(ValueError):
            PBSClient.from_sdk(pve_sdk)
    finally:
        await pve_sdk.close()


def test_sync_client_blocks_and_returns_typed_models():
    """SyncPBSClient runs coroutines on its private loop and unwraps results."""
    sdk, _ = _make_sdk(
        {
            "/api2/json/admin/datastore": {"data": [{"store": "tank"}]},
            "/api2/json/version": {"data": {"version": "3.2.7"}},
        }
    )
    client = SyncPBSClient(_sdk=sdk)
    try:
        stores = client.datastores.list()
        assert stores[0].name == "tank"
        v = client.version()
        assert v.version == "3.2.7"
    finally:
        client.close()

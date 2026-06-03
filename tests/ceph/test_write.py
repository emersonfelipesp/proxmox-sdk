"""Domain helper tests for Proxmox VE Ceph write helpers."""

from __future__ import annotations

from typing import Any

import pytest

from proxmox_sdk.ceph import CephClient, SyncCephClient
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
        self.calls.append((method, path, data if data is not None else params))
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


async def test_pool_write_helpers_hit_expected_paths_and_payloads():
    sdk, backend = _make_sdk(
        {
            "/api2/json/nodes/pve1/ceph/pool": {"data": "UPID:pool-create"},
            "/api2/json/nodes/pve1/ceph/pool/rbd": {"data": "UPID:pool-change"},
        }
    )
    ceph = CephClient(_sdk=sdk)

    created = await ceph.write.pool_create(
        "pve1",
        "rbd",
        add_storages=True,
        application="rbd",
        crush_rule="replicated_rule",
        erasure_coding="ec-profile",
        min_size=2,
        pg_autoscale_mode="on",
        pg_num=128,
        pg_num_min=32,
        size=3,
        target_size="100G",
        target_size_ratio=0.5,
    )
    changed = await ceph.write.pool_set(
        "pve1",
        "rbd",
        application="rbd",
        min_size=2,
        pg_autoscale_mode="warn",
        pg_num=256,
        size=3,
    )
    deleted = await ceph.write.pool_delete(
        "pve1",
        "rbd",
        confirm_destroy=True,
        force=True,
        remove_ecprofile=True,
        remove_storages=True,
    )

    assert created == "UPID:pool-create"
    assert changed == "UPID:pool-change"
    assert deleted == "UPID:pool-change"
    assert backend.calls == [
        (
            "POST",
            "/api2/json/nodes/pve1/ceph/pool",
            {
                "name": "rbd",
                "add_storages": True,
                "application": "rbd",
                "crush_rule": "replicated_rule",
                "erasure-coding": "ec-profile",
                "min_size": 2,
                "pg_autoscale_mode": "on",
                "pg_num": 128,
                "pg_num_min": 32,
                "size": 3,
                "target_size": "100G",
                "target_size_ratio": 0.5,
            },
        ),
        (
            "PUT",
            "/api2/json/nodes/pve1/ceph/pool/rbd",
            {
                "application": "rbd",
                "min_size": 2,
                "pg_autoscale_mode": "warn",
                "pg_num": 256,
                "size": 3,
            },
        ),
        (
            "DELETE",
            "/api2/json/nodes/pve1/ceph/pool/rbd",
            {"force": True, "remove_ecprofile": True, "remove_storages": True},
        ),
    ]


async def test_flag_helpers_use_cluster_flag_put_endpoint():
    sdk, backend = _make_sdk({"/api2/json/cluster/ceph/flags/noout": {"data": None}})
    ceph = CephClient(_sdk=sdk)

    assert await ceph.write.flag_set("noout") is None
    assert await ceph.write.flag_unset("noout") is None
    assert backend.calls == [
        ("PUT", "/api2/json/cluster/ceph/flags/noout", {"value": True}),
        ("PUT", "/api2/json/cluster/ceph/flags/noout", {"value": False}),
    ]


async def test_osd_lifecycle_helpers_hit_expected_paths_and_payloads():
    sdk, backend = _make_sdk(
        {
            "/api2/json/nodes/pve1/ceph/osd": {"data": "UPID:osd-create"},
            "/api2/json/nodes/pve1/ceph/osd/7/in": {"data": None},
            "/api2/json/nodes/pve1/ceph/osd/7/out": {"data": None},
            "/api2/json/nodes/pve1/ceph/osd/7": {"data": "UPID:osd-delete"},
        }
    )
    ceph = CephClient(_sdk=sdk)

    created = await ceph.write.osd_create(
        "pve1",
        "/dev/sdb",
        crush_device_class="ssd",
        db_dev="/dev/nvme0n1",
        db_dev_size=64.0,
        encrypted=True,
        osds_per_device=2,
        wal_dev="/dev/nvme0n2",
        wal_dev_size=8.0,
    )
    marked_in = await ceph.write.osd_in("pve1", 7)
    marked_out = await ceph.write.osd_out("pve1", 7)
    deleted = await ceph.write.osd_delete("pve1", 7, confirm_destroy=True, cleanup=True)

    assert created == "UPID:osd-create"
    assert marked_in is None
    assert marked_out is None
    assert deleted == "UPID:osd-delete"
    assert backend.calls == [
        (
            "POST",
            "/api2/json/nodes/pve1/ceph/osd",
            {
                "dev": "/dev/sdb",
                "crush-device-class": "ssd",
                "db_dev": "/dev/nvme0n1",
                "db_dev_size": 64.0,
                "encrypted": True,
                "osds-per-device": 2,
                "wal_dev": "/dev/nvme0n2",
                "wal_dev_size": 8.0,
            },
        ),
        ("POST", "/api2/json/nodes/pve1/ceph/osd/7/in", None),
        ("POST", "/api2/json/nodes/pve1/ceph/osd/7/out", None),
        ("DELETE", "/api2/json/nodes/pve1/ceph/osd/7", {"cleanup": True}),
    ]


async def test_mon_mgr_mds_lifecycle_helpers_hit_expected_paths_and_payloads():
    sdk, backend = _make_sdk(
        {
            "/api2/json/nodes/pve1/ceph/mon/pve1": {"data": "UPID:mon"},
            "/api2/json/nodes/pve1/ceph/mgr/pve1": {"data": "UPID:mgr"},
            "/api2/json/nodes/pve1/ceph/mds/fs-a": {"data": "UPID:mds"},
        }
    )
    ceph = CephClient(_sdk=sdk)

    assert await ceph.write.mon_create("pve1", "pve1", mon_address="10.0.0.10") == "UPID:mon"
    assert await ceph.write.mon_delete("pve1", "pve1", confirm_destroy=True) == "UPID:mon"
    assert await ceph.write.mgr_create("pve1", "pve1") == "UPID:mgr"
    assert await ceph.write.mgr_delete("pve1", "pve1", confirm_destroy=True) == "UPID:mgr"
    assert await ceph.write.mds_create("pve1", "fs-a", hotstandby=True) == "UPID:mds"
    assert await ceph.write.mds_delete("pve1", "fs-a", confirm_destroy=True) == "UPID:mds"
    assert backend.calls == [
        ("POST", "/api2/json/nodes/pve1/ceph/mon/pve1", {"mon-address": "10.0.0.10"}),
        ("DELETE", "/api2/json/nodes/pve1/ceph/mon/pve1", None),
        ("POST", "/api2/json/nodes/pve1/ceph/mgr/pve1", None),
        ("DELETE", "/api2/json/nodes/pve1/ceph/mgr/pve1", None),
        ("POST", "/api2/json/nodes/pve1/ceph/mds/fs-a", {"hotstandby": True}),
        ("DELETE", "/api2/json/nodes/pve1/ceph/mds/fs-a", None),
    ]


async def test_cephfs_and_service_lifecycle_helpers_hit_expected_paths_and_payloads():
    sdk, backend = _make_sdk(
        {
            "/api2/json/nodes/pve1/ceph/fs/cephfs": {"data": "UPID:fs"},
            "/api2/json/nodes/pve1/ceph/start": {"data": "UPID:start"},
            "/api2/json/nodes/pve1/ceph/stop": {"data": "UPID:stop"},
            "/api2/json/nodes/pve1/ceph/restart": {"data": "UPID:restart"},
        }
    )
    ceph = CephClient(_sdk=sdk)

    fs = await ceph.write.cephfs_create("pve1", "cephfs", add_storage=True, pg_num=128)
    started = await ceph.write.service_start("pve1", service="ceph-osd@7")
    stopped = await ceph.write.service_stop("pve1", service="ceph-osd@7")
    restarted = await ceph.write.service_restart("pve1", service="ceph-osd@7")

    assert fs == "UPID:fs"
    assert started == "UPID:start"
    assert stopped == "UPID:stop"
    assert restarted == "UPID:restart"
    assert backend.calls == [
        ("POST", "/api2/json/nodes/pve1/ceph/fs/cephfs", {"add-storage": True, "pg_num": 128}),
        ("POST", "/api2/json/nodes/pve1/ceph/start", {"service": "ceph-osd@7"}),
        ("POST", "/api2/json/nodes/pve1/ceph/stop", {"service": "ceph-osd@7"}),
        ("POST", "/api2/json/nodes/pve1/ceph/restart", {"service": "ceph-osd@7"}),
    ]


@pytest.mark.parametrize(
    ("method_name", "args"),
    [
        ("pool_delete", ("pve1", "rbd")),
        ("osd_delete", ("pve1", 7)),
        ("mon_delete", ("pve1", "pve1")),
        ("mgr_delete", ("pve1", "pve1")),
        ("mds_delete", ("pve1", "fs-a")),
    ],
)
async def test_destructive_helpers_require_confirm_destroy(method_name: str, args: tuple[Any, ...]):
    sdk, backend = _make_sdk({})
    ceph = CephClient(_sdk=sdk)

    with pytest.raises(ValueError, match="confirm_destroy=True"):
        await getattr(ceph.write, method_name)(*args)

    assert backend.calls == []


def test_sync_write_domain_blocks_and_returns_result():
    sdk, backend = _make_sdk({"/api2/json/nodes/pve1/ceph/start": {"data": "UPID:start"}})
    client = SyncCephClient(_sdk=sdk)
    try:
        assert client.write.service_start("pve1", service="ceph.target") == "UPID:start"
    finally:
        client.close()
    assert backend.calls == [
        ("POST", "/api2/json/nodes/pve1/ceph/start", {"service": "ceph.target"})
    ]

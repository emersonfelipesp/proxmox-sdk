"""Tests for the RBD provider adapter (Dashboard-backed)."""

from __future__ import annotations

import pytest

from proxmox_sdk.ceph.providers.dashboard import DashboardCephClient
from proxmox_sdk.ceph.providers.rbd import RBDClient

from .conftest import RecordingTransport

BASE = "https://ceph.example.com:8443"


def _rbd(routes: dict) -> tuple[RBDClient, RecordingTransport]:
    transport = RecordingTransport(routes)
    dashboard = DashboardCephClient(BASE, username="admin", password="secret", transport=transport)
    return RBDClient(dashboard), transport


async def test_list_and_get_image() -> None:
    routes = {
        "POST /api/auth": {"token": "t"},
        "GET /api/block/image": [
            {"pool_name": "rbd", "value": [{"name": "vm-100", "size": 10}]},
        ],
    }
    rbd, _ = _rbd(routes)
    images = await rbd.list_images("rbd")
    assert images[0].name == "vm-100"
    found = await rbd.get_image("rbd", "vm-100")
    assert found is not None and found.size == 10


async def test_create_image_builds_payload() -> None:
    routes = {"POST /api/auth": {"token": "t"}, "POST /api/block/image": {"task": "x"}}
    rbd, transport = _rbd(routes)
    await rbd.create_image("rbd", "vm-101", 1073741824, features=["layering"])
    payload = transport.calls[1]["json"]
    assert payload["pool_name"] == "rbd"
    assert payload["name"] == "vm-101"
    assert payload["size"] == 1073741824
    assert payload["features"] == ["layering"]


async def test_resize_shrink_is_gated() -> None:
    routes = {
        "POST /api/auth": {"token": "t"},
        "PUT /api/block/image/rbd%2Fvm-101": {},
    }
    rbd, _ = _rbd(routes)
    with pytest.raises(ValueError, match="shrink"):
        await rbd.resize_image("rbd", "vm-101", 512, current_size_bytes=1024)
    # Growing is allowed.
    await rbd.resize_image("rbd", "vm-101", 2048, current_size_bytes=1024)
    # Explicit allow_shrink permits shrinking.
    await rbd.resize_image("rbd", "vm-101", 512, current_size_bytes=1024, allow_shrink=True)


async def test_delete_image_requires_confirmation() -> None:
    routes = {
        "POST /api/auth": {"token": "t"},
        "DELETE /api/block/image/rbd%2Fvm-101": {},
    }
    rbd, _ = _rbd(routes)
    with pytest.raises(ValueError, match="destructive"):
        await rbd.delete_image("rbd", "vm-101")
    await rbd.delete_image("rbd", "vm-101", confirm_destroy=True)


async def test_snapshot_lifecycle() -> None:
    routes = {
        "POST /api/auth": {"token": "t"},
        "POST /api/block/image/rbd%2Fvm-101/snap": {},
        "DELETE /api/block/image/rbd%2Fvm-101/snap/snap1": {},
    }
    rbd, transport = _rbd(routes)
    await rbd.create_snapshot("rbd", "vm-101", "snap1")
    assert transport.calls[1]["json"] == {"snapshot_name": "snap1"}
    with pytest.raises(ValueError, match="destructive"):
        await rbd.delete_snapshot("rbd", "vm-101", "snap1")
    await rbd.delete_snapshot("rbd", "vm-101", "snap1", confirm_destroy=True)


async def test_capabilities_require_dashboard() -> None:
    routes = {
        "POST /api/auth": {"token": "t"},
        "GET /api/summary": {"version": "ceph version 18.2.4"},
    }
    rbd, _ = _rbd(routes)
    caps = await rbd.capabilities()
    assert caps.available is True
    assert caps.supports("rbd_image", "create") is True

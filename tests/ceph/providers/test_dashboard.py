"""Tests for the Ceph Dashboard direct provider client."""

from __future__ import annotations

import pytest

from proxmox_sdk.ceph.providers._http import HttpResponse
from proxmox_sdk.ceph.providers.dashboard import DashboardCephClient
from proxmox_sdk.sdk.exceptions import (
    AuthenticationError,
    CephCapabilityUnsupportedError,
    ResourceException,
)

from .conftest import RecordingTransport

BASE = "https://ceph.example.com:8443"


def _client(routes: dict, **kwargs) -> tuple[DashboardCephClient, RecordingTransport]:
    transport = RecordingTransport(routes)
    client = DashboardCephClient(
        BASE,
        username="admin",
        password="secret",
        transport=transport,
        **kwargs,
    )
    return client, transport


async def test_login_caches_token_and_authorizes_requests() -> None:
    routes = {
        "POST /api/auth": {"token": "jwt-abc"},
        "GET /api/health/minimal": {"health": {"status": "HEALTH_OK"}},
    }
    client, transport = _client(routes)
    health = await client.health()
    assert health.status == "HEALTH_OK"
    # First call authenticates, second carries the bearer token.
    assert transport.calls[0]["path"] == "/api/auth"
    assert transport.calls[1]["headers"]["Authorization"] == "Bearer jwt-abc"
    assert "vnd.ceph.api.v1.0+json" in transport.calls[1]["headers"]["Accept"]


async def test_login_failure_raises_authentication_error() -> None:
    routes = {"POST /api/auth": HttpResponse(status=401, text="bad creds")}
    client, _ = _client(routes)
    with pytest.raises(AuthenticationError):
        await client.health()


async def test_login_requires_credentials() -> None:
    transport = RecordingTransport({})
    client = DashboardCephClient(BASE, transport=transport)
    with pytest.raises(AuthenticationError):
        await client.login()


async def test_pools_normalizes_records() -> None:
    routes = {
        "POST /api/auth": {"token": "t"},
        "GET /api/pool": [
            {"pool_name": "rbd", "size": 3, "pg_num": 128},
            {"pool_name": "cephfs_data", "size": 2},
        ],
    }
    client, transport = _client(routes)
    pools = await client.pools()
    assert [p.pool_name for p in pools] == ["rbd", "cephfs_data"]
    assert pools[0].size == 3
    # Bool params are stringified by the real aiohttp transport, not before it.
    assert transport.calls[1]["params"] == {"stats": True}


async def test_rbd_images_flattens_per_pool_groups() -> None:
    routes = {
        "POST /api/auth": {"token": "t"},
        "GET /api/block/image": [
            {"pool_name": "rbd", "value": [{"name": "vm-100", "size": 1024}]},
            {"pool_name": "rbd2", "value": [{"name": "vm-200", "size": 2048}]},
        ],
    }
    client, transport = _client(routes)
    images = await client.rbd_images()
    assert {i.name for i in images} == {"vm-100", "vm-200"}
    # Block API negotiates the v2.0 media type.
    assert "vnd.ceph.api.v2.0+json" in transport.calls[1]["headers"]["Accept"]


async def test_pool_delete_requires_confirmation() -> None:
    routes = {"POST /api/auth": {"token": "t"}, "DELETE /api/pool/rbd": {}}
    client, _ = _client(routes)
    with pytest.raises(ValueError, match="destructive"):
        await client.pool_delete("rbd")
    # With confirmation it proceeds.
    assert await client.pool_delete("rbd", confirm_destroy=True) == {}


async def test_http_error_raises_resource_exception() -> None:
    routes = {
        "POST /api/auth": {"token": "t"},
        "GET /api/host": HttpResponse(status=500, text="boom"),
    }
    client, _ = _client(routes)
    with pytest.raises(ResourceException):
        await client.hosts()


async def test_capabilities_reports_supported_operations() -> None:
    routes = {
        "POST /api/auth": {"token": "t"},
        "GET /api/summary": {"version": "ceph version 18.2.4"},
    }
    client, _ = _client(routes)
    caps = await client.capabilities()
    assert caps.available is True
    assert caps.version == "ceph version 18.2.4"
    assert caps.supports("pool", "create") is True
    assert caps.supports("rbd_image", "delete") is True
    assert caps.supports("nonsense", "frobnicate") is True  # write fallback for unknown verbs

    # require() raises for an unsupported op.
    caps.operations["pool:create"] = False
    with pytest.raises(CephCapabilityUnsupportedError):
        client.require("pool", "create", caps)


async def test_capabilities_unavailable_when_summary_unreachable() -> None:
    routes = {
        "POST /api/auth": {"token": "t"},
        "GET /api/summary": HttpResponse(status=503, text="down"),
    }
    client, _ = _client(routes)
    caps = await client.capabilities()
    assert caps.available is False
    assert caps.supports("pool", "create") is False

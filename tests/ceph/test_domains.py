"""Unit tests for the Ceph SDK facade against the in-memory mock backend."""

from __future__ import annotations

import pytest

from proxmox_sdk.ceph import CephClient, SyncCephClient
from proxmox_sdk.ceph import models as m
from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.services import SERVICES


@pytest.mark.asyncio
async def test_client_mock_creation() -> None:
    """`CephClient.mock()` builds a working PVE-backed async client."""
    client = CephClient.mock()
    try:
        # The underlying SDK must be configured for PVE.
        assert client._sdk._service_config is SERVICES["PVE"]
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_cluster_status_returns_model() -> None:
    """`/cluster/ceph/status` returns a permissive CephClusterStatus model."""
    client = CephClient.mock()
    try:
        status = await client.status()
        assert isinstance(status, m.CephClusterStatus)
        # Permissive model accepts the empty/sparse mock payload.
        status.model_dump()
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_cluster_flags_returns_list() -> None:
    """`/cluster/ceph/flags` returns a list of CephFlag models."""
    client = CephClient.mock()
    try:
        flags = await client.cluster.flags()
        assert isinstance(flags, list)
        for flag in flags:
            assert isinstance(flag, m.CephFlag)
    finally:
        await client.close()


@pytest.mark.asyncio
async def test_node_pools_and_osds_return_lists() -> None:
    """Node-scoped pool/osd helpers return lists of permissive models."""
    client = CephClient.mock()
    try:
        pools = await client.nodes.pools("pve1")
        osds = await client.nodes.osds("pve1")
        assert isinstance(pools, list)
        assert isinstance(osds, list)
        for pool in pools:
            assert isinstance(pool, m.CephPool)
        for osd in osds:
            assert isinstance(osd, m.CephOSD)
    finally:
        await client.close()


def test_from_sdk_requires_pve() -> None:
    """`CephClient.from_sdk` refuses non-PVE SDK instances."""
    # PMG service is allowed by ProxmoxSDK but is not Ceph-capable.
    sdk = ProxmoxSDK.mock(service="PMG")
    with pytest.raises(ValueError, match="service='PVE'"):
        CephClient.from_sdk(sdk)


def test_sync_client_smoke() -> None:
    """`SyncCephClient` exposes blocking `status()` against the mock backend."""
    client = SyncCephClient(_sdk=ProxmoxSDK.mock(service="PVE"))
    try:
        status = client.status()
        assert isinstance(status, m.CephClusterStatus)
    finally:
        client.close()

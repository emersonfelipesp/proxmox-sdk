"""Typed read-only Ceph facade over :class:`ProxmoxSDK`.

Proxmox VE exposes Ceph through the PVE API, so this client shares the normal
PVE authentication, backend, retry, and mock behavior.  The facade keeps Ceph
navigation explicit and returns permissive Pydantic models from
``proxmox_sdk.ceph.models``.
"""

from __future__ import annotations

import asyncio
from typing import Any

from proxmox_sdk.ceph import models as m
from proxmox_sdk.ceph.domains.cluster import ClusterCeph
from proxmox_sdk.ceph.domains.nodes import NodeCeph
from proxmox_sdk.ceph.domains.write import CephWrite
from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.sync_adapter import BlockingDomainProxy


class CephClient:
    """Async Ceph client backed by :class:`ProxmoxSDK(service="PVE")`."""

    def __init__(
        self,
        host: str | None = None,
        *,
        user: str | None = None,
        password: str | None = None,
        token_name: str | None = None,
        token_value: str | None = None,
        otp: str | None = None,
        backend: str = "https",
        port: int | None = None,
        verify_ssl: bool = True,
        timeout: int = 30,
        connect_timeout: int | None = None,
        max_retries: int = 0,
        retry_backoff: float = 0.5,
        path_prefix: str = "",
        _sdk: ProxmoxSDK | None = None,
    ) -> None:
        self._sdk = _sdk or ProxmoxSDK(
            host=host,
            user=user,
            password=password,
            token_name=token_name,
            token_value=token_value,
            otp=otp,
            service="PVE",
            backend=backend,
            port=port,
            verify_ssl=verify_ssl,
            timeout=timeout,
            connect_timeout=connect_timeout,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            path_prefix=path_prefix,
        )
        self.cluster = ClusterCeph(self._sdk)
        self.nodes = NodeCeph(self._sdk)
        self.write = CephWrite(self._sdk)

    @classmethod
    def from_sdk(cls, sdk: ProxmoxSDK) -> CephClient:
        """Wrap an existing :class:`ProxmoxSDK` instance (service must be PVE)."""
        if sdk.service != "PVE":
            raise ValueError("CephClient requires a ProxmoxSDK instance with service='PVE'")
        return cls(_sdk=sdk)

    @classmethod
    def mock(cls, schema_version: str = "latest") -> CephClient:
        """Mock CephClient for tests, backed by the PVE mock schema."""
        return cls(_sdk=ProxmoxSDK.mock(schema_version=schema_version, service="PVE"))

    async def __aenter__(self) -> CephClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    async def close(self) -> None:
        await self._sdk.close()

    async def status(self) -> m.CephClusterStatus:
        """Return cluster-wide Ceph health/status."""
        return await self.cluster.status()


class SyncCephClient:
    """Synchronous wrapper around :class:`CephClient` for non-async callers."""

    def __init__(self, **kwargs: Any) -> None:
        self._loop = asyncio.new_event_loop()
        self._client = CephClient(**kwargs)

    def __enter__(self) -> SyncCephClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        try:
            self._loop.run_until_complete(self._client.close())
        finally:
            self._loop.close()

    def status(self) -> m.CephClusterStatus:
        return self._loop.run_until_complete(self._client.status())

    @property
    def cluster(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.cluster)

    @property
    def nodes(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.nodes)

    @property
    def write(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.write)

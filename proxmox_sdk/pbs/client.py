"""PBSClient — typed read-only PBS facade over :class:`ProxmoxSDK`.

The PBS REST service shares transport, auth, and pagination conventions with
PVE, so the heavy lifting (HTTPS session, retries, SSL, token format, cookies)
already lives in :class:`proxmox_sdk.sdk.api.ProxmoxSDK`. PBSClient adds:

* a tighter constructor (no PVE/PMG-specific knobs);
* typed read-only domain helpers (:attr:`datastores`, :attr:`snapshots`,
  :attr:`jobs`, :attr:`nodes`, :meth:`version`);
* return values parsed into the hand-coded Pydantic models in
  :mod:`proxmox_sdk.pbs.models`.

v1 exposes read paths only. Write helpers are intentionally not provided.
"""

from __future__ import annotations

from typing import Any

from proxmox_sdk.pbs import models as m
from proxmox_sdk.pbs._utils import unwrap_data
from proxmox_sdk.pbs.domains.datastores import Datastores
from proxmox_sdk.pbs.domains.jobs import Jobs
from proxmox_sdk.pbs.domains.nodes import Nodes
from proxmox_sdk.pbs.domains.snapshots import Snapshots
from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.sync_adapter import BlockingDomainProxy


class PBSClient:
    """Async PBS client. Composes :class:`ProxmoxSDK` with ``service="PBS"``."""

    def __init__(
        self,
        host: str | None = None,
        *,
        user: str | None = None,
        token_name: str | None = None,
        token_value: str | None = None,
        port: int | None = 8007,
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
            token_name=token_name,
            token_value=token_value,
            service="PBS",
            port=port,
            verify_ssl=verify_ssl,
            timeout=timeout,
            connect_timeout=connect_timeout,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            path_prefix=path_prefix,
        )
        self.datastores = Datastores(self._sdk)
        self.snapshots = Snapshots(self._sdk)
        self.jobs = Jobs(self._sdk)
        self.nodes = Nodes(self._sdk)

    @classmethod
    def from_sdk(cls, sdk: ProxmoxSDK) -> PBSClient:
        """Wrap an existing :class:`ProxmoxSDK` instance (service must be PBS)."""
        if sdk.service != "PBS":
            raise ValueError("PBSClient requires a ProxmoxSDK instance with service='PBS'")
        return cls(_sdk=sdk)

    @classmethod
    def mock(cls, schema_version: str = "latest") -> PBSClient:
        """Mock PBSClient for tests. Backed by :meth:`ProxmoxSDK.mock`.

        Note: until the PBS codegen bundle ships, mock responses fall back to
        the PVE schema surface. Most read tests should override responses
        directly rather than relying on the mock for shape correctness.
        """
        return cls(_sdk=ProxmoxSDK.mock(schema_version=schema_version, service="PBS"))

    async def __aenter__(self) -> PBSClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    async def close(self) -> None:
        await self._sdk.close()

    async def version(self) -> m.PBSVersion:
        data: Any = await self._sdk.version.get()
        return m.PBSVersion.model_validate(unwrap_data(data))


class SyncPBSClient:
    """Synchronous wrapper around :class:`PBSClient` for non-async callers."""

    def __init__(self, **kwargs: Any) -> None:
        import asyncio

        self._loop = asyncio.new_event_loop()
        self._client = PBSClient(**kwargs)

    def __enter__(self) -> SyncPBSClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        try:
            self._loop.run_until_complete(self._client.close())
        finally:
            self._loop.close()

    def version(self) -> m.PBSVersion:
        return self._loop.run_until_complete(self._client.version())

    @property
    def datastores(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.datastores)

    @property
    def snapshots(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.snapshots)

    @property
    def jobs(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.jobs)

    @property
    def nodes(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.nodes)

"""PDMClient — typed PDM facade over :class:`ProxmoxSDK`.

PDM (Proxmox Datacenter Manager) shares transport, auth, and pagination
conventions with PVE/PBS, so the heavy lifting (HTTPS session, retries, SSL,
token format, cookies) already lives in :class:`proxmox_sdk.sdk.api.ProxmoxSDK`.
PDMClient adds:

* a tighter constructor (default port 8443, PDM-specific auth);
* typed domain helpers covering all eight PDM API domains;
* return values parsed into the hand-coded Pydantic models in
  :mod:`proxmox_sdk.pdm.models`.

PDM's distinguishing trait vs PBS is that every guest/datastore operation
requires a ``remote`` argument in addition to the usual resource id, because
PDM multiplexes across registered PVE clusters and PBS instances.
"""

from __future__ import annotations

from typing import Any

from proxmox_sdk.pdm import models as m
from proxmox_sdk.pdm._normalization import require_string, validate_model
from proxmox_sdk.pdm.domains.access import AccessDomain
from proxmox_sdk.pdm.domains.metrics import MetricsDomain
from proxmox_sdk.pdm.domains.pbs import PBSDomain
from proxmox_sdk.pdm.domains.pve import PVEDomain
from proxmox_sdk.pdm.domains.remotes import RemotesDomain
from proxmox_sdk.pdm.domains.resources import GlobalResourcesDomain, SubscriptionsDomain
from proxmox_sdk.pdm.domains.views import ViewsDomain
from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.sync_adapter import BlockingDomainProxy


class PDMClient:
    """Async PDM client. Composes :class:`ProxmoxSDK` with ``service="PDM"``."""

    def __init__(
        self,
        host: str | None = None,
        *,
        user: str | None = None,
        token_name: str | None = None,
        token_value: str | None = None,
        port: int | None = 8443,
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
            service="PDM",
            port=port,
            verify_ssl=verify_ssl,
            timeout=timeout,
            connect_timeout=connect_timeout,
            max_retries=max_retries,
            retry_backoff=retry_backoff,
            path_prefix=path_prefix,
        )
        self.remotes = RemotesDomain(self._sdk)
        self.pve = PVEDomain(self._sdk)
        self.pbs = PBSDomain(self._sdk)
        self.resources = GlobalResourcesDomain(self._sdk)
        self.subscriptions = SubscriptionsDomain(self._sdk)
        self.metrics = MetricsDomain(self._sdk)
        self.access = AccessDomain(self._sdk)
        self.views = ViewsDomain(self._sdk)

    @classmethod
    def from_sdk(cls, sdk: ProxmoxSDK) -> PDMClient:
        """Wrap an existing :class:`ProxmoxSDK` instance (service must be PDM)."""
        if sdk.service != "PDM":
            raise ValueError("PDMClient requires a ProxmoxSDK instance with service='PDM'")
        return cls(_sdk=sdk)

    @classmethod
    def mock(cls, schema_version: str = "latest") -> PDMClient:
        """Mock PDMClient for tests. Backed by :meth:`ProxmoxSDK.mock`."""
        return cls(_sdk=ProxmoxSDK.mock(schema_version=schema_version, service="PDM"))

    async def __aenter__(self) -> PDMClient:
        return self

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    async def close(self) -> None:
        await self._sdk.close()

    async def version(self) -> m.PDMVersion:
        data: Any = await self._sdk.version.get()
        return validate_model(m.PDMVersion, data, operation="GET /version")

    async def ping(self) -> str:
        """Call GET /ping — lightweight PDM liveness probe."""
        data: Any = await self._sdk.ping.get()
        return require_string(data, operation="GET /ping")


class SyncPDMClient:
    """Synchronous wrapper around :class:`PDMClient` for non-async callers."""

    def __init__(self, **kwargs: Any) -> None:
        import asyncio

        self._loop = asyncio.new_event_loop()
        self._client = PDMClient(**kwargs)

    def __enter__(self) -> SyncPDMClient:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def close(self) -> None:
        try:
            self._loop.run_until_complete(self._client.close())
        finally:
            self._loop.close()

    def version(self) -> m.PDMVersion:
        return self._loop.run_until_complete(self._client.version())

    def ping(self) -> str:
        """Call GET /ping — lightweight PDM liveness probe."""
        return self._loop.run_until_complete(self._client.ping())

    @property
    def remotes(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.remotes)

    @property
    def pve(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.pve)

    @property
    def pbs(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.pbs)

    @property
    def resources(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.resources)

    @property
    def subscriptions(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.subscriptions)

    @property
    def metrics(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.metrics)

    @property
    def access(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.access)

    @property
    def views(self) -> BlockingDomainProxy:
        return BlockingDomainProxy(self._loop, self._client.views)

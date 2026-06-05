"""Direct Ceph Dashboard REST API client.

The Ceph Manager Dashboard exposes a REST API (``/api/*``) that can manage a
Ceph cluster without going through Proxmox VE.  Authentication is a JWT bearer
token obtained from ``POST /api/auth``; every request carries a versioned
``Accept`` media type (``application/vnd.ceph.api.v{n}+json``).

This client is provider-neutral and brings its own transport so it works
against Proxmox-managed *and* external/standalone Ceph clusters.  Destructive
writes require ``confirm_destroy=True`` to match
:class:`proxmox_sdk.ceph.domains.write.CephWrite`.
"""

from __future__ import annotations

from typing import Any

from proxmox_sdk.ceph.providers import models as m
from proxmox_sdk.ceph.providers._http import (
    DEFAULT_TIMEOUT,
    AsyncTransport,
    BaseHttpProvider,
    HttpResponse,
)
from proxmox_sdk.ceph.providers.capability import ProviderCapability
from proxmox_sdk.sdk.exceptions import (
    AuthenticationError,
    CephCapabilityUnsupportedError,
    ProxmoxSDKError,
)

# Endpoints whose Dashboard handlers negotiate a non-default media-type version.
_BLOCK_IMAGE_VERSION = "2.0"


def _media_type(version: str) -> str:
    return f"application/vnd.ceph.api.v{version}+json"


class DashboardCephClient(BaseHttpProvider):
    """Async client for the Ceph Manager Dashboard REST API."""

    provider = "dashboard"

    def __init__(
        self,
        base_url: str,
        *,
        username: str | None = None,
        password: str | None = None,
        token: str | None = None,
        verify_ssl: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        api_version: str = "1.0",
        transport: AsyncTransport | None = None,
    ) -> None:
        super().__init__(base_url, verify_ssl=verify_ssl, timeout=timeout, transport=transport)
        self._username = username
        self._password = password
        self._token: str | None = token
        self._api_version = api_version

    # -- auth ---------------------------------------------------------------- #
    async def login(self) -> str:
        """Authenticate and cache a JWT bearer token."""

        if not (self._username and self._password):
            raise AuthenticationError("Dashboard login requires username and password")
        response = await self._transport.request(
            "POST",
            self._url("api/auth"),
            headers={
                "Accept": _media_type(self._api_version),
                "Content-Type": "application/json",
            },
            json={"username": self._username, "password": self._password},
        )
        if response.status >= 400 or not isinstance(response.json_body, dict):
            raise AuthenticationError(f"Dashboard authentication failed (HTTP {response.status})")
        token = response.json_body.get("token")
        if not isinstance(token, str) or not token:
            raise AuthenticationError("Dashboard authentication returned no token")
        self._token = token
        return token

    async def _ensure_token(self) -> str:
        if not self._token:
            await self.login()
        assert self._token is not None  # noqa: S101 - guaranteed by login()
        return self._token

    async def logout(self) -> None:
        if not self._token:
            return
        try:
            await self._request("POST", "api/auth/logout")
        except ProxmoxSDKError:  # pragma: no cover - best-effort logout
            pass
        finally:
            self._token = None

    # -- request core -------------------------------------------------------- #
    async def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        version: str | None = None,
    ) -> HttpResponse:
        token = await self._ensure_token()
        headers = {
            "Accept": _media_type(version or self._api_version),
            "Authorization": f"Bearer {token}",
        }
        if json is not None:
            headers["Content-Type"] = "application/json"
        response = await self._transport.request(
            method, self._url(path), headers=headers, params=params, json=json
        )
        self._raise_for_status(response, context=f"dashboard {method} /{path}")
        return response

    @staticmethod
    def _require_confirm(operation: str, confirm_destroy: bool) -> None:
        if not confirm_destroy:
            raise ValueError(f"{operation} is destructive; pass confirm_destroy=True to proceed.")

    @staticmethod
    def _as_list(body: Any) -> list[dict[str, Any]]:
        if isinstance(body, list):
            return [item for item in body if isinstance(item, dict)]
        if isinstance(body, dict):
            for key in ("items", "results", "data"):
                inner = body.get(key)
                if isinstance(inner, list):
                    return [item for item in inner if isinstance(item, dict)]
        return []

    # -- reads --------------------------------------------------------------- #
    async def summary(self) -> dict[str, Any]:
        response = await self._request("GET", "api/summary")
        return response.json_body if isinstance(response.json_body, dict) else {}

    async def version(self) -> str | None:
        """Best-effort Ceph version string for capability/version display."""

        try:
            summary = await self.summary()
        except ProxmoxSDKError:
            return None
        version = summary.get("version")
        return version if isinstance(version, str) else None

    async def health(self) -> m.DashboardHealth:
        response = await self._request("GET", "api/health/minimal")
        body = response.json_body if isinstance(response.json_body, dict) else {}
        health = body.get("health", body)
        if isinstance(health, dict):
            return m.DashboardHealth.model_validate(health)
        return m.DashboardHealth(status=str(health) if health else "unknown")

    async def hosts(self) -> list[m.DashboardHost]:
        response = await self._request("GET", "api/host")
        return [m.DashboardHost.model_validate(i) for i in self._as_list(response.json_body)]

    async def osds(self) -> list[m.DashboardOSD]:
        response = await self._request("GET", "api/osd")
        return [m.DashboardOSD.model_validate(i) for i in self._as_list(response.json_body)]

    async def pools(self, *, stats: bool = True) -> list[m.DashboardPool]:
        response = await self._request("GET", "api/pool", params={"stats": stats})
        return [m.DashboardPool.model_validate(i) for i in self._as_list(response.json_body)]

    async def filesystems(self) -> list[m.DashboardFilesystem]:
        response = await self._request("GET", "api/cephfs")
        return [m.DashboardFilesystem.model_validate(i) for i in self._as_list(response.json_body)]

    async def rbd_images(self, pool_name: str | None = None) -> list[m.DashboardRBDImage]:
        params = {"pool_name": pool_name} if pool_name else None
        response = await self._request(
            "GET", "api/block/image", params=params, version=_BLOCK_IMAGE_VERSION
        )
        body = response.json_body
        images: list[dict[str, Any]] = []
        # /api/block/image groups images per pool: [{"pool_name", "value":[...]}]
        if isinstance(body, list):
            for group in body:
                if isinstance(group, dict) and isinstance(group.get("value"), list):
                    images.extend(i for i in group["value"] if isinstance(i, dict))
                elif isinstance(group, dict):
                    images.append(group)
        else:
            images = self._as_list(body)
        return [m.DashboardRBDImage.model_validate(i) for i in images]

    async def rgw_daemons(self) -> list[m.DashboardRGWDaemon]:
        response = await self._request("GET", "api/rgw/daemon")
        return [m.DashboardRGWDaemon.model_validate(i) for i in self._as_list(response.json_body)]

    async def rgw_buckets(self) -> list[m.DashboardRGWBucket]:
        response = await self._request("GET", "api/rgw/bucket", params={"stats": True})
        return [m.DashboardRGWBucket.model_validate(i) for i in self._as_list(response.json_body)]

    # -- pool writes --------------------------------------------------------- #
    async def pool_create(self, payload: dict[str, Any]) -> Any:
        response = await self._request("POST", "api/pool", json=payload)
        return response.json_body

    async def pool_edit(self, pool_name: str, payload: dict[str, Any]) -> Any:
        response = await self._request("PUT", f"api/pool/{pool_name}", json=payload)
        return response.json_body

    async def pool_delete(self, pool_name: str, *, confirm_destroy: bool = False) -> Any:
        self._require_confirm("pool_delete", confirm_destroy)
        response = await self._request("DELETE", f"api/pool/{pool_name}")
        return response.json_body

    # -- rbd writes ---------------------------------------------------------- #
    async def rbd_create(self, payload: dict[str, Any]) -> Any:
        response = await self._request(
            "POST", "api/block/image", json=payload, version=_BLOCK_IMAGE_VERSION
        )
        return response.json_body

    async def rbd_edit(self, image_spec: str, payload: dict[str, Any]) -> Any:
        response = await self._request(
            "PUT", f"api/block/image/{image_spec}", json=payload, version=_BLOCK_IMAGE_VERSION
        )
        return response.json_body

    async def rbd_delete(self, image_spec: str, *, confirm_destroy: bool = False) -> Any:
        self._require_confirm("rbd_delete", confirm_destroy)
        response = await self._request(
            "DELETE", f"api/block/image/{image_spec}", version=_BLOCK_IMAGE_VERSION
        )
        return response.json_body

    async def rbd_move_trash(self, image_spec: str, *, confirm_destroy: bool = False) -> Any:
        self._require_confirm("rbd_move_trash", confirm_destroy)
        response = await self._request(
            "POST",
            f"api/block/image/{image_spec}/move_trash",
            json={},
            version=_BLOCK_IMAGE_VERSION,
        )
        return response.json_body

    async def rbd_snapshot_create(self, image_spec: str, snapshot_name: str) -> Any:
        response = await self._request(
            "POST",
            f"api/block/image/{image_spec}/snap",
            json={"snapshot_name": snapshot_name},
            version=_BLOCK_IMAGE_VERSION,
        )
        return response.json_body

    async def rbd_snapshot_delete(
        self, image_spec: str, snapshot_name: str, *, confirm_destroy: bool = False
    ) -> Any:
        self._require_confirm("rbd_snapshot_delete", confirm_destroy)
        response = await self._request(
            "DELETE",
            f"api/block/image/{image_spec}/snap/{snapshot_name}",
            version=_BLOCK_IMAGE_VERSION,
        )
        return response.json_body

    # -- capability detection ----------------------------------------------- #
    async def capabilities(self) -> ProviderCapability:
        """Probe the Dashboard and report supported operation kinds.

        Returns ``available=False`` (never raises) when the Dashboard cannot be
        reached or authenticated, so callers can degrade gracefully.
        """

        try:
            summary = await self.summary()
        except (ProxmoxSDKError, AuthenticationError) as exc:
            return ProviderCapability(
                provider=self.provider,
                available=False,
                notes=[f"dashboard unavailable: {exc}"],
            )
        raw_version = summary.get("version")
        version = raw_version if isinstance(raw_version, str) else None
        operations = {
            "pool:create": True,
            "pool:update": True,
            "pool:set": True,
            "pool:delete": True,
            "rbd_image:create": True,
            "rbd_image:update": True,
            "rbd_image:delete": True,
            "rbd_snapshot:create": True,
            "rbd_snapshot:delete": True,
            "rgw_bucket:read": True,
            "rgw_user:read": True,
        }
        return ProviderCapability(
            provider=self.provider,
            available=True,
            version=version,
            read=True,
            write=True,
            metrics=False,
            operations=operations,
        )

    def require(self, kind: str, action: str, capability: ProviderCapability) -> None:
        """Raise :class:`CephCapabilityUnsupportedError` if unsupported."""

        if not capability.supports(kind, action):
            raise CephCapabilityUnsupportedError(f"{kind}:{action}", provider=self.provider)

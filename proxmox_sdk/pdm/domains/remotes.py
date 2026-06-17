"""``/remotes`` CRUD + per-remote version query."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import normalize_list, unwrap_data
from proxmox_sdk.pdm import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class RemotesDomain:
    """Manage registered PVE/PBS remotes and query their version.

    All operations target the ``/remotes/remote`` sub-path, which is the
    actual remote-list endpoint per the official PDM API schema.  The parent
    ``/remotes`` path returns only a sub-directory index, not the remote list.
    """

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self) -> list[m.PDMRemote]:
        """GET /remotes/remote — list all configured PVE/PBS remotes."""
        data = await self._sdk.remotes.remote.get()
        return [m.PDMRemote.model_validate(item) for item in normalize_list(data)]

    async def get(self, remote: str) -> m.PDMRemote:
        """GET /remotes/remote/{id} — fetch a single remote by id."""
        data = unwrap_data(await self._sdk.remotes.remote(remote).get())
        return m.PDMRemote.model_validate(data or {})

    async def add(
        self,
        *,
        id: str,
        type: m.RemoteType,
        nodes: list[dict[str, Any]] | None = None,
        authid: str | None = None,
        token: str | None = None,
        fingerprint: str | None = None,
        web_url: str | None = None,
    ) -> Any:
        """POST /remotes/remote — register a new remote."""
        payload: dict[str, Any] = {"id": id, "type": type}
        if nodes is not None:
            payload["nodes"] = nodes
        if authid is not None:
            payload["authid"] = authid
        if token is not None:
            payload["token"] = token
        if fingerprint is not None:
            payload["fingerprint"] = fingerprint
        if web_url is not None:
            payload["web-url"] = web_url
        return unwrap_data(await self._sdk.remotes.remote.post(**payload))

    async def update(self, remote: str, **changes: Any) -> Any:
        """PUT /remotes/remote/{id} — update a remote's configuration."""
        return unwrap_data(await self._sdk.remotes.remote(remote).put(**changes))

    async def remove(self, remote: str) -> Any:
        """DELETE /remotes/remote/{id} — deregister a remote."""
        return unwrap_data(await self._sdk.remotes.remote(remote).delete())

    async def version(self, remote: str) -> m.PDMRemoteVersion:
        """GET /remotes/remote/{id}/version — query a remote's version."""
        data = unwrap_data(await self._sdk.remotes.remote(remote).version.get())
        return m.PDMRemoteVersion.model_validate(data or {})

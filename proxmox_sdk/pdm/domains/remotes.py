"""``/remotes`` CRUD + per-remote version query."""

from __future__ import annotations

from collections.abc import Mapping
from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import unwrap_data
from proxmox_sdk.pdm import models as m
from proxmox_sdk.pdm._normalization import validate_model, validate_model_list

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK

RemoteNodeInput = str | m.PDMRemoteNode | Mapping[str, Any]


def _node_address(node: RemoteNodeInput) -> str:
    """Return the wire-format address required by the PDM OpenAPI schema."""

    if isinstance(node, str):
        address = node.strip()
    elif isinstance(node, m.PDMRemoteNode):
        address = node.hostname.strip()
    else:
        address = m.PDMRemoteNode.model_validate(node).hostname.strip()
    if not address:
        raise ValueError("PDM remote nodes require a non-empty hostname or IP address")
    return address


def _node_addresses(nodes: list[RemoteNodeInput]) -> list[str]:
    """Normalize public node inputs to the schema-required string array."""

    return [_node_address(node) for node in nodes]


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
        return validate_model_list(m.PDMRemote, data, operation="GET /remotes/remote")

    async def get(self, remote: str) -> m.PDMRemote:
        """GET /remotes/remote/{id}/config — fetch a single remote configuration."""
        data = await self._sdk.remotes.remote(remote).config.get()
        return validate_model(
            m.PDMRemote,
            data,
            operation="GET /remotes/remote/{id}/config",
        )

    async def add(
        self,
        *,
        id: str,
        type: m.RemoteType,
        nodes: list[RemoteNodeInput] | None = None,
        authid: str | None = None,
        token: str | None = None,
        fingerprint: str | None = None,
        web_url: str | None = None,
    ) -> Any:
        """POST /remotes/remote — register a new remote."""
        payload: dict[str, Any] = {"id": id, "type": type}
        if nodes is not None:
            payload["nodes"] = _node_addresses(nodes)
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
        if "nodes" in changes:
            nodes = changes["nodes"]
            if not isinstance(nodes, list):
                raise ValueError("PDM remote nodes must be provided as a list")
            changes["nodes"] = _node_addresses(nodes)
        return unwrap_data(await self._sdk.remotes.remote(remote).put(**changes))

    async def remove(self, remote: str) -> Any:
        """DELETE /remotes/remote/{id} — deregister a remote."""
        return unwrap_data(await self._sdk.remotes.remote(remote).delete())

    async def version(self, remote: str) -> m.PDMRemoteVersion:
        """GET /remotes/remote/{id}/version — query a remote's version."""
        data = await self._sdk.remotes.remote(remote).version.get()
        return validate_model(
            m.PDMRemoteVersion,
            data,
            operation="GET /remotes/remote/{id}/version",
        )

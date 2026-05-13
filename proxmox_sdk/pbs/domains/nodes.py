"""``/nodes/{node}/status`` read helper."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk.pbs import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


def _unwrap(data: Any) -> Any:
    if isinstance(data, dict) and set(data.keys()) == {"data"}:
        return data["data"]
    return data


class Nodes:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def status(self, node: str) -> m.PBSNodeStatus:
        data = _unwrap(await self._sdk.nodes(node).status.get())
        return m.PBSNodeStatus.model_validate(data or {})

"""``/nodes/{node}/status`` read helper."""

from __future__ import annotations

from typing import TYPE_CHECKING

from proxmox_sdk._response_utils import unwrap_data
from proxmox_sdk.pbs import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class Nodes:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def status(self, node: str) -> m.PBSNodeStatus:
        data = unwrap_data(await self._sdk.nodes(node).status.get())
        return m.PBSNodeStatus.model_validate(data or {})

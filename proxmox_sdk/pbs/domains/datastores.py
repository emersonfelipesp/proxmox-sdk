"""``/admin/datastore`` read helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from proxmox_sdk._response_utils import normalize_list, unwrap_data
from proxmox_sdk.pbs import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class Datastores:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self) -> list[m.PBSDatastore]:
        data = await self._sdk.admin.datastore.get()
        return [m.PBSDatastore.model_validate(item) for item in normalize_list(data)]

    async def usage(self, store: str) -> m.PBSDatastore:
        """Return a single datastore record (status + capacity)."""
        data = unwrap_data(await self._sdk.admin.datastore(store).status.get())
        return m.PBSDatastore.model_validate({"store": store, **(data or {})})

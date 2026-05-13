"""``/admin/datastore`` read helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk.pbs import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


def _unwrap(data: Any) -> Any:
    if isinstance(data, dict) and set(data.keys()) == {"data"}:
        return data["data"]
    return data


class Datastores:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self) -> list[m.PBSDatastore]:
        data = _unwrap(await self._sdk.admin.datastore.get())
        return [m.PBSDatastore.model_validate(item) for item in data or []]

    async def usage(self, store: str) -> m.PBSDatastore:
        """Return a single datastore record (status + capacity)."""
        data = _unwrap(await self._sdk.admin.datastore(store).status.get())
        return m.PBSDatastore.model_validate({"store": store, **(data or {})})

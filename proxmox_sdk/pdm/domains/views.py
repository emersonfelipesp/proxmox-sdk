"""Custom cross-remote resource view dashboards (``/config/views``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import normalize_list, unwrap_data
from proxmox_sdk.pdm import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class ViewsDomain:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self) -> list[m.PDMView]:
        data = await self._sdk.config.views.get()
        return [m.PDMView.model_validate(item) for item in normalize_list(data)]

    async def get(self, view_id: str) -> m.PDMView:
        data = unwrap_data(await self._sdk.config.views(view_id).get())
        if isinstance(data, dict):
            data.setdefault("id", view_id)
        else:
            data = {"id": view_id}
        return m.PDMView.model_validate(data)

    async def create(self, *, id: str, **fields: Any) -> Any:
        return unwrap_data(await self._sdk.config.views.post(id=id, **fields))

    async def update(self, view_id: str, **changes: Any) -> Any:
        return unwrap_data(await self._sdk.config.views(view_id).put(**changes))

    async def delete(self, view_id: str) -> Any:
        return unwrap_data(await self._sdk.config.views(view_id).delete())

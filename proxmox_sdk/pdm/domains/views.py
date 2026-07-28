"""Custom cross-remote resource view dashboards (``/config/views``)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import unwrap_data
from proxmox_sdk.pdm import models as m
from proxmox_sdk.pdm._normalization import validate_model, validate_model_list

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class ViewsDomain:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self) -> list[m.PDMView]:
        data = await self._sdk.config.views.get()
        return validate_model_list(m.PDMView, data, operation="GET /config/views")

    async def get(self, view_id: str) -> m.PDMView:
        data = await self._sdk.config.views(view_id).get()
        return validate_model(
            m.PDMView,
            data,
            operation="GET /config/views/{id}",
        )

    async def create(self, *, id: str, **fields: Any) -> Any:
        return unwrap_data(await self._sdk.config.views.post(id=id, **fields))

    async def update(self, view_id: str, **changes: Any) -> Any:
        return unwrap_data(await self._sdk.config.views(view_id).put(**changes))

    async def delete(self, view_id: str) -> Any:
        return unwrap_data(await self._sdk.config.views(view_id).delete())

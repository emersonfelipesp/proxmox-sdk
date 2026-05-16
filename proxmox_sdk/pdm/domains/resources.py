"""Global resource and subscription endpoints (cross-remote)."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import normalize_list
from proxmox_sdk.pdm import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class GlobalResourcesDomain:
    """Aggregated resource queries that span every registered remote."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self, *, type: str | None = None) -> list[m.PDMResource]:
        params: dict[str, Any] = {}
        if type is not None:
            params["type"] = type
        data = await self._sdk.resources.list.get(**params)
        return [m.PDMResource.model_validate(item) for item in normalize_list(data)]

    async def status(self) -> list[m.PDMResourceStatus]:
        data = await self._sdk.resources.status.get()
        return [m.PDMResourceStatus.model_validate(item) for item in normalize_list(data)]


class SubscriptionsDomain:
    """Fleet-wide subscription state."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self) -> list[m.PDMSubscription]:
        data = await self._sdk.resources.subscription.get()
        return [m.PDMSubscription.model_validate(item) for item in normalize_list(data)]

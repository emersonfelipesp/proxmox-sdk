"""Metric collection endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import unwrap_data
from proxmox_sdk.pdm import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class MetricsDomain:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def status(self) -> m.PDMMetricCollectionStatus:
        data = unwrap_data(await self._sdk.config.metrics.status.get())
        return m.PDMMetricCollectionStatus.model_validate(data or {})

    async def trigger(self) -> Any:
        return unwrap_data(await self._sdk.config.metrics.trigger.post())

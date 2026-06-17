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
        # GET /remotes/metric-collection/status
        # The hyphen in "metric-collection" requires call syntax (not attribute access).
        data = unwrap_data(await self._sdk.remotes("metric-collection").status.get())
        return m.PDMMetricCollectionStatus.model_validate(data or {})

    async def trigger(self) -> Any:
        # POST /remotes/metric-collection/trigger
        return unwrap_data(await self._sdk.remotes("metric-collection").trigger.post())

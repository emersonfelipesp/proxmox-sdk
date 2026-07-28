"""Metric collection endpoints."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import unwrap_data
from proxmox_sdk.pdm import models as m
from proxmox_sdk.pdm._normalization import (
    redact_optional_error,
    require_list,
    require_mapping,
    validate_model,
)

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class MetricsDomain:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def status(self) -> list[m.PDMMetricCollectionStatus]:
        # GET /remotes/metric-collection/status
        # The hyphen in "metric-collection" requires call syntax (not attribute access).
        data = await self._sdk.remotes("metric-collection").status.get()
        operation = "GET /remotes/metric-collection/status"
        statuses: list[m.PDMMetricCollectionStatus] = []
        for index, item in enumerate(require_list(data, operation=operation)):
            item_operation = f"{operation}[{index}]"
            payload, _ = redact_optional_error(
                require_mapping(item, operation=item_operation),
                operation=item_operation,
            )
            statuses.append(
                validate_model(
                    m.PDMMetricCollectionStatus,
                    payload,
                    operation=item_operation,
                )
            )
        return statuses

    async def trigger(self) -> Any:
        # POST /remotes/metric-collection/trigger
        return unwrap_data(await self._sdk.remotes("metric-collection").trigger.post())

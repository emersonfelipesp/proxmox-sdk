"""Cluster-wide Ceph read helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from proxmox_sdk._response_utils import normalize_list, unwrap_data
from proxmox_sdk.ceph import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class ClusterCeph:
    """Helpers for ``/cluster/ceph`` endpoints."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def status(self) -> m.CephClusterStatus:
        data = unwrap_data(await self._sdk("cluster/ceph/status").get())
        return m.CephClusterStatus.model_validate(data or {})

    async def metadata(self) -> m.CephClusterMetadata:
        data = unwrap_data(await self._sdk("cluster/ceph/metadata").get())
        return m.CephClusterMetadata.model_validate(data or {})

    async def flags(self) -> list[m.CephFlag]:
        data = await self._sdk("cluster/ceph/flags").get()
        return [m.CephFlag.model_validate(item) for item in normalize_list(data, dict_mode="items")]

    async def flag(self, name: str) -> m.CephFlag:
        data = unwrap_data(await self._sdk(["cluster", "ceph", "flags", name]).get())
        if isinstance(data, dict):
            payload = {"name": name, **data}
        else:
            payload = {"name": name, "value": data}
        return m.CephFlag.model_validate(payload)

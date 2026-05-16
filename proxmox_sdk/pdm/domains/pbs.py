"""PBS-via-PDM operations: datastores, snapshots, tasks, node RRD."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import normalize_list, unwrap_data
from proxmox_sdk.pdm import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class PBSDomain:
    """All PDM operations targeting registered Proxmox Backup Server remotes."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def datastores(self, remote: str) -> list[m.PDMPBSDatastore]:
        data = await self._sdk.pbs.remotes(remote).datastores.get()
        items: list[m.PDMPBSDatastore] = []
        for entry in normalize_list(data):
            payload = dict(entry)
            payload.setdefault("remote", remote)
            items.append(m.PDMPBSDatastore.model_validate(payload))
        return items

    async def datastore_rrddata(
        self,
        remote: str,
        store: str,
        *,
        timeframe: str = "hour",
        cf: str | None = None,
    ) -> list[m.PDMRRDData]:
        params: dict[str, Any] = {"timeframe": timeframe}
        if cf is not None:
            params["cf"] = cf
        data = await self._sdk.pbs.remotes(remote).datastores(store).rrddata.get(**params)
        return [m.PDMRRDData.model_validate(item) for item in normalize_list(data)]

    async def snapshots(
        self,
        remote: str,
        store: str,
        *,
        namespace: str | None = None,
    ) -> list[m.PDMPBSSnapshot]:
        params: dict[str, Any] = {}
        if namespace is not None:
            params["ns"] = namespace
        data = await self._sdk.pbs.remotes(remote).datastores(store).snapshots.get(**params)
        items: list[m.PDMPBSSnapshot] = []
        for entry in normalize_list(data):
            payload = dict(entry)
            payload.setdefault("remote", remote)
            payload.setdefault("store", store)
            if namespace is not None:
                payload.setdefault("namespace", namespace)
            items.append(m.PDMPBSSnapshot.model_validate(payload))
        return items

    async def node_rrddata(
        self,
        remote: str,
        *,
        timeframe: str = "hour",
        cf: str | None = None,
    ) -> list[m.PDMRRDData]:
        params: dict[str, Any] = {"timeframe": timeframe}
        if cf is not None:
            params["cf"] = cf
        data = await self._sdk.pbs.remotes(remote).node.rrddata.get(**params)
        return [m.PDMRRDData.model_validate(item) for item in normalize_list(data)]

    async def tasks(self, remote: str) -> list[m.PDMTask]:
        data = await self._sdk.pbs.remotes(remote).tasks.get()
        return [m.PDMTask.model_validate(item) for item in normalize_list(data)]

    async def task_status(self, remote: str, upid: str) -> m.PDMTaskStatus:
        data = unwrap_data(await self._sdk.pbs.remotes(remote).tasks(upid).status.get())
        return m.PDMTaskStatus.model_validate(data or {"upid": upid})

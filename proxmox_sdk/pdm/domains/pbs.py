"""PBS-via-PDM operations: datastores, snapshots, tasks, node RRD."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk.pdm import models as m
from proxmox_sdk.pdm._normalization import (
    require_list,
    require_mapping,
    validate_model,
    validate_model_list,
    validate_rrd_query,
)

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class PBSDomain:
    """All PDM operations targeting registered Proxmox Backup Server remotes."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def datastores(self, remote: str) -> list[m.PDMPBSDatastore]:
        # GET /pbs/remotes/{remote}/datastore  (singular — the schema uses no trailing 's')
        data = await self._sdk.pbs.remotes(remote).datastore.get()
        items: list[m.PDMPBSDatastore] = []
        operation = "GET /pbs/remotes/{remote}/datastore"
        for index, entry in enumerate(require_list(data, operation=operation)):
            payload = require_mapping(entry, operation=f"{operation}[{index}]")
            payload.setdefault("remote", remote)
            items.append(
                validate_model(
                    m.PDMPBSDatastore,
                    payload,
                    operation=f"{operation}[{index}]",
                )
            )
        return items

    async def datastore_rrddata(
        self,
        remote: str,
        store: str,
        *,
        timeframe: m.PDMRRDTimeframe = "hour",
        cf: m.PDMRRDConsolidation = "AVERAGE",
    ) -> list[m.PDMRRDData]:
        params = validate_rrd_query(timeframe, cf)
        # GET /pbs/remotes/{remote}/datastore/{datastore}/rrddata
        data = await self._sdk.pbs.remotes(remote).datastore(store).rrddata.get(**params)
        return validate_model_list(
            m.PDMRRDData,
            data,
            operation="GET /pbs/remotes/{remote}/datastore/{datastore}/rrddata",
        )

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
        # GET /pbs/remotes/{remote}/datastore/{datastore}/snapshots
        data = await self._sdk.pbs.remotes(remote).datastore(store).snapshots.get(**params)
        items: list[m.PDMPBSSnapshot] = []
        operation = "GET /pbs/remotes/{remote}/datastore/{datastore}/snapshots"
        for index, entry in enumerate(require_list(data, operation=operation)):
            payload = require_mapping(entry, operation=f"{operation}[{index}]")
            payload.setdefault("remote", remote)
            payload.setdefault("store", store)
            if namespace is not None:
                payload.setdefault("namespace", namespace)
            items.append(
                validate_model(
                    m.PDMPBSSnapshot,
                    payload,
                    operation=f"{operation}[{index}]",
                )
            )
        return items

    async def node_rrddata(
        self,
        remote: str,
        *,
        timeframe: m.PDMRRDTimeframe = "hour",
        cf: m.PDMRRDConsolidation = "AVERAGE",
    ) -> list[m.PDMRRDData]:
        params = validate_rrd_query(timeframe, cf)
        # GET /pbs/remotes/{remote}/rrddata  (no /node/ intermediate — PDM schema path)
        data = await self._sdk.pbs.remotes(remote).rrddata.get(**params)
        return validate_model_list(
            m.PDMRRDData,
            data,
            operation="GET /pbs/remotes/{remote}/rrddata",
        )

    async def tasks(self, remote: str) -> list[m.PDMTask]:
        data = await self._sdk.pbs.remotes(remote).tasks.get()
        return validate_model_list(
            m.PDMTask,
            data,
            operation="GET /pbs/remotes/{remote}/tasks",
        )

    async def task_status(self, remote: str, upid: str) -> m.PDMTaskStatus:
        data = await self._sdk.pbs.remotes(remote).tasks(upid).status.get()
        return validate_model(
            m.PDMTaskStatus,
            data,
            operation="GET /pbs/remotes/{remote}/tasks/{upid}/status",
        )

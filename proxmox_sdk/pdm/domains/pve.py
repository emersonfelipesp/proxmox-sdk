"""PVE-via-PDM operations: nodes, qemu/lxc guests, resources, tasks.

All PDM guest operations require a ``remote`` in addition to ``vmid`` — the
PDM API multiplexes across registered PVE clusters.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import normalize_list, unwrap_data
from proxmox_sdk.pdm import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class _GuestOps:
    """Shared qemu/lxc lifecycle + RRD + remote-migrate helpers."""

    _kind: str  # "qemu" or "lxc"

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    def _guest_resource(self, remote: str, vmid: int) -> Any:
        return self._sdk.pve.remotes(remote).guests(self._kind)(vmid)

    async def list(self, remote: str) -> list[m.PDMGuest]:
        data = await self._sdk.pve.remotes(remote).guests(self._kind).get()
        items: list[m.PDMGuest] = []
        for entry in normalize_list(data):
            payload = dict(entry)
            payload.setdefault("remote", remote)
            payload.setdefault("type", self._kind)
            items.append(m.PDMGuest.model_validate(payload))
        return items

    async def config(self, remote: str, vmid: int) -> m.PDMGuestConfig:
        data = unwrap_data(await self._guest_resource(remote, vmid).config.get())
        return m.PDMGuestConfig.model_validate(data or {})

    async def start(self, remote: str, vmid: int) -> Any:
        return unwrap_data(await self._guest_resource(remote, vmid).start.post())

    async def stop(self, remote: str, vmid: int) -> Any:
        return unwrap_data(await self._guest_resource(remote, vmid).stop.post())

    async def shutdown(self, remote: str, vmid: int) -> Any:
        return unwrap_data(await self._guest_resource(remote, vmid).shutdown.post())

    async def migrate(
        self,
        remote: str,
        vmid: int,
        *,
        target: str,
        online: bool | None = None,
    ) -> Any:
        kwargs: dict[str, Any] = {"target": target}
        if online is not None:
            kwargs["online"] = online
        return unwrap_data(await self._guest_resource(remote, vmid).migrate.post(**kwargs))

    async def remote_migrate(
        self,
        remote: str,
        vmid: int,
        *,
        target_remote: str,
        target_vmid: int | None = None,
        target_node: str | None = None,
        online: bool | None = None,
    ) -> Any:
        kwargs: dict[str, Any] = {"target-remote": target_remote}
        if target_vmid is not None:
            kwargs["target-vmid"] = target_vmid
        if target_node is not None:
            kwargs["target-node"] = target_node
        if online is not None:
            kwargs["online"] = online
        return unwrap_data(
            await self._guest_resource(remote, vmid)("remote-migrate").post(**kwargs)
        )

    async def rrddata(
        self,
        remote: str,
        vmid: int,
        *,
        timeframe: str = "hour",
        cf: str | None = None,
    ) -> list[m.PDMRRDData]:
        params: dict[str, Any] = {"timeframe": timeframe}
        if cf is not None:
            params["cf"] = cf
        data = await self._guest_resource(remote, vmid).rrddata.get(**params)
        return [m.PDMRRDData.model_validate(item) for item in normalize_list(data)]


class _QemuOps(_GuestOps):
    _kind = "qemu"


class _LxcOps(_GuestOps):
    _kind = "lxc"


class PVEDomain:
    """All PDM operations targeting registered Proxmox VE remotes."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk
        self.qemu = _QemuOps(sdk)
        self.lxc = _LxcOps(sdk)

    async def nodes(self, remote: str) -> list[m.PDMNode]:
        data = await self._sdk.pve.remotes(remote).nodes.get()
        items: list[m.PDMNode] = []
        for entry in normalize_list(data):
            payload = dict(entry)
            payload.setdefault("remote", remote)
            items.append(m.PDMNode.model_validate(payload))
        return items

    async def node_rrddata(
        self,
        remote: str,
        node: str,
        *,
        timeframe: str = "hour",
        cf: str | None = None,
    ) -> list[m.PDMRRDData]:
        params: dict[str, Any] = {"timeframe": timeframe}
        if cf is not None:
            params["cf"] = cf
        data = await self._sdk.pve.remotes(remote).nodes(node).rrddata.get(**params)
        return [m.PDMRRDData.model_validate(item) for item in normalize_list(data)]

    async def resources(self, remote: str, *, type: str | None = None) -> list[m.PDMResource]:
        params: dict[str, Any] = {}
        if type is not None:
            params["type"] = type
        data = await self._sdk.pve.remotes(remote).resources.get(**params)
        items: list[m.PDMResource] = []
        for entry in normalize_list(data):
            payload = dict(entry)
            payload.setdefault("remote", remote)
            items.append(m.PDMResource.model_validate(payload))
        return items

    async def tasks(self, remote: str) -> list[m.PDMTask]:
        data = await self._sdk.pve.remotes(remote).tasks.get()
        return [m.PDMTask.model_validate(item) for item in normalize_list(data)]

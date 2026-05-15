"""Node-scoped Ceph read helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk.ceph import models as m
from proxmox_sdk.ceph._utils import _normalize_list, _unwrap

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK
    from proxmox_sdk.sdk.resource import ProxmoxResource


class NodeCeph:
    """Helpers for ``/nodes/{node}/ceph`` endpoints."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    def _resource(self, node: str, *segments: str | int) -> ProxmoxResource:
        return self._sdk(["nodes", node, "ceph", *segments])

    async def _list_daemons(self, node: str, segment: str, daemon_type: str) -> list[m.CephDaemon]:
        data = await self._resource(node, segment).get()
        return [
            m.CephDaemon.model_validate({**item, "type": daemon_type})
            for item in _normalize_list(data)
            if isinstance(item, dict)
        ]

    async def index(self, node: str) -> list[dict[str, Any]]:
        return _normalize_list(await self._resource(node).get())

    async def config_db(self, node: str) -> Any:
        return _unwrap(await self._resource(node, "cfg", "db").get())

    async def config_raw(self, node: str) -> Any:
        return _unwrap(await self._resource(node, "cfg", "raw").get())

    async def config_value(self, node: str, **params: Any) -> Any:
        return _unwrap(await self._resource(node, "cfg", "value").get(**params))

    async def cmd_safety(self, node: str, **params: Any) -> Any:
        return _unwrap(await self._resource(node, "cmd-safety").get(**params))

    async def crush(self, node: str) -> Any:
        return _unwrap(await self._resource(node, "crush").get())

    async def filesystems(self, node: str) -> list[m.CephFilesystem]:
        data = await self._resource(node, "fs").get()
        return [m.CephFilesystem.model_validate(item) for item in _normalize_list(data)]

    async def monitors(self, node: str) -> list[m.CephDaemon]:
        return await self._list_daemons(node, "mon", "mon")

    async def managers(self, node: str) -> list[m.CephDaemon]:
        return await self._list_daemons(node, "mgr", "mgr")

    async def metadata_servers(self, node: str) -> list[m.CephDaemon]:
        return await self._list_daemons(node, "mds", "mds")

    async def osds(self, node: str) -> list[m.CephOSD]:
        data = await self._resource(node, "osd").get()
        return [m.CephOSD.model_validate(item) for item in _normalize_list(data)]

    async def osd(self, node: str, osdid: int | str) -> m.CephOSD:
        data = _unwrap(await self._resource(node, "osd", osdid).get())
        payload = {**(data or {}), "id": osdid} if isinstance(data, dict) else {"id": osdid}
        return m.CephOSD.model_validate(payload)

    async def osd_lv_info(self, node: str, osdid: int | str) -> Any:
        return _unwrap(await self._resource(node, "osd", osdid, "lv-info").get())

    async def osd_metadata(self, node: str, osdid: int | str) -> Any:
        return _unwrap(await self._resource(node, "osd", osdid, "metadata").get())

    async def pools(self, node: str) -> list[m.CephPool]:
        data = await self._resource(node, "pool").get()
        return [m.CephPool.model_validate(item) for item in _normalize_list(data)]

    async def pool(self, node: str, name: str) -> m.CephPool:
        data = _unwrap(await self._resource(node, "pool", name).get())
        payload = {**(data or {}), "name": name} if isinstance(data, dict) else {"name": name}
        return m.CephPool.model_validate(payload)

    async def pool_status(self, node: str, name: str) -> Any:
        return _unwrap(await self._resource(node, "pool", name, "status").get())

    async def rules(self, node: str) -> list[m.CephCrushRule]:
        data = await self._resource(node, "rules").get()
        return [m.CephCrushRule.model_validate(item) for item in _normalize_list(data)]

    async def log(self, node: str, **params: Any) -> list[m.CephLogLine]:
        data = await self._resource(node, "log").get(**params)
        return [m.CephLogLine.model_validate(item) for item in _normalize_list(data)]

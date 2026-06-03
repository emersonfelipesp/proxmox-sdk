"""Proxmox VE Ceph write helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, cast

from proxmox_sdk._response_utils import unwrap_data
from proxmox_sdk.ceph import models as m

if TYPE_CHECKING:
    from pydantic import BaseModel

    from proxmox_sdk.sdk.api import ProxmoxSDK
    from proxmox_sdk.sdk.resource import ProxmoxResource


class CephWrite:
    """Typed helpers for Proxmox VE-managed Ceph write endpoints."""

    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    def _resource(self, node: str, *segments: str | int) -> ProxmoxResource:
        return self._sdk(["nodes", node, "ceph", *segments])

    def _flag_resource(self, flag: m.CephFlagName | str) -> ProxmoxResource:
        return self._sdk(["cluster", "ceph", "flags", flag])

    @staticmethod
    def _dump(params: BaseModel) -> dict[str, Any]:
        return params.model_dump(by_alias=True, exclude_none=True)

    @staticmethod
    def _require_confirm(method: str, confirm_destroy: bool) -> None:
        if not confirm_destroy:
            raise ValueError(f"{method} is destructive; pass confirm_destroy=True to proceed.")

    # ------------------------------------------------------------------
    # Pools
    # ------------------------------------------------------------------

    async def pool_create(
        self,
        node: str,
        name: str,
        *,
        add_storages: bool | None = None,
        application: m.CephPoolApplication | str | None = None,
        crush_rule: str | None = None,
        erasure_coding: str | None = None,
        min_size: int | None = None,
        pg_autoscale_mode: m.CephPGAutoscaleMode | str | None = None,
        pg_num: int | None = None,
        pg_num_min: int | None = None,
        size: int | None = None,
        target_size: str | None = None,
        target_size_ratio: float | None = None,
    ) -> str:
        """Create a Ceph pool and return the Proxmox task UPID."""
        payload = self._dump(
            m.CephPoolCreateParams.model_validate(
                {
                    "name": name,
                    "add_storages": add_storages,
                    "application": application,
                    "crush_rule": crush_rule,
                    "erasure_coding": erasure_coding,
                    "min_size": min_size,
                    "pg_autoscale_mode": pg_autoscale_mode,
                    "pg_num": pg_num,
                    "pg_num_min": pg_num_min,
                    "size": size,
                    "target_size": target_size,
                    "target_size_ratio": target_size_ratio,
                }
            )
        )
        return cast(str, unwrap_data(await self._resource(node, "pool").post(**payload)))

    async def pool_set(
        self,
        node: str,
        name: str,
        *,
        application: m.CephPoolApplication | str | None = None,
        crush_rule: str | None = None,
        min_size: int | None = None,
        pg_autoscale_mode: m.CephPGAutoscaleMode | str | None = None,
        pg_num: int | None = None,
        pg_num_min: int | None = None,
        size: int | None = None,
        target_size: str | None = None,
        target_size_ratio: float | None = None,
    ) -> str:
        """Update a Ceph pool and return the Proxmox task UPID."""
        payload = self._dump(
            m.CephPoolSetParams(
                application=application,
                crush_rule=crush_rule,
                min_size=min_size,
                pg_autoscale_mode=pg_autoscale_mode,
                pg_num=pg_num,
                pg_num_min=pg_num_min,
                size=size,
                target_size=target_size,
                target_size_ratio=target_size_ratio,
            )
        )
        return cast(str, unwrap_data(await self._resource(node, "pool", name).put(**payload)))

    async def pool_delete(
        self,
        node: str,
        name: str,
        *,
        confirm_destroy: bool = False,
        force: bool | None = None,
        remove_ecprofile: bool | None = None,
        remove_storages: bool | None = None,
    ) -> str:
        """Destroy a Ceph pool and return the Proxmox task UPID."""
        self._require_confirm("pool_delete", confirm_destroy)
        payload = self._dump(
            m.CephPoolDeleteParams(
                force=force,
                remove_ecprofile=remove_ecprofile,
                remove_storages=remove_storages,
            )
        )
        return cast(str, unwrap_data(await self._resource(node, "pool", name).delete(**payload)))

    # ------------------------------------------------------------------
    # Cluster flags
    # ------------------------------------------------------------------

    async def flag_set(self, flag: m.CephFlagName | str) -> Any:
        """Set a cluster-wide Ceph flag."""
        return await self._flag_update(flag, value=True)

    async def flag_unset(self, flag: m.CephFlagName | str) -> Any:
        """Clear a cluster-wide Ceph flag."""
        return await self._flag_update(flag, value=False)

    async def _flag_update(self, flag: m.CephFlagName | str, *, value: bool) -> Any:
        """Set or clear a cluster-wide Ceph flag using PVE's exposed PUT endpoint."""
        payload = self._dump(m.CephFlagUpdateParams(value=value))
        return unwrap_data(await self._flag_resource(flag).put(**payload))

    # ------------------------------------------------------------------
    # OSD lifecycle
    # ------------------------------------------------------------------

    async def osd_create(
        self,
        node: str,
        dev: str,
        *,
        crush_device_class: str | None = None,
        db_dev: str | None = None,
        db_dev_size: float | None = None,
        encrypted: bool | None = None,
        osds_per_device: int | None = None,
        wal_dev: str | None = None,
        wal_dev_size: float | None = None,
    ) -> str:
        """Create one or more OSDs on a device and return the Proxmox task UPID."""
        payload = self._dump(
            m.CephOSDCreateParams.model_validate(
                {
                    "dev": dev,
                    "crush_device_class": crush_device_class,
                    "db_dev": db_dev,
                    "db_dev_size": db_dev_size,
                    "encrypted": encrypted,
                    "osds_per_device": osds_per_device,
                    "wal_dev": wal_dev,
                    "wal_dev_size": wal_dev_size,
                }
            )
        )
        return cast(str, unwrap_data(await self._resource(node, "osd").post(**payload)))

    async def osd_delete(
        self,
        node: str,
        osdid: int | str,
        *,
        confirm_destroy: bool = False,
        cleanup: bool | None = None,
    ) -> str:
        """Destroy an OSD and return the Proxmox task UPID."""
        self._require_confirm("osd_delete", confirm_destroy)
        payload = self._dump(m.CephOSDDeleteParams(cleanup=cleanup))
        return cast(str, unwrap_data(await self._resource(node, "osd", osdid).delete(**payload)))

    async def osd_in(self, node: str, osdid: int | str) -> Any:
        """Mark an OSD in."""
        return unwrap_data(await self._resource(node, "osd", osdid, "in").post())

    async def osd_out(self, node: str, osdid: int | str) -> Any:
        """Mark an OSD out."""
        return unwrap_data(await self._resource(node, "osd", osdid, "out").post())

    # ------------------------------------------------------------------
    # MON, MGR, and MDS lifecycle
    # ------------------------------------------------------------------

    async def mon_create(
        self,
        node: str,
        monid: str,
        *,
        mon_address: str | None = None,
    ) -> str:
        """Create a Ceph monitor and return the Proxmox task UPID."""
        payload = self._dump(m.CephMonCreateParams.model_validate({"mon_address": mon_address}))
        return cast(str, unwrap_data(await self._resource(node, "mon", monid).post(**payload)))

    async def mon_delete(
        self,
        node: str,
        monid: str,
        *,
        confirm_destroy: bool = False,
    ) -> str:
        """Destroy a Ceph monitor and return the Proxmox task UPID."""
        self._require_confirm("mon_delete", confirm_destroy)
        return cast(str, unwrap_data(await self._resource(node, "mon", monid).delete()))

    async def mgr_create(self, node: str, mgr_id: str) -> str:
        """Create a Ceph manager and return the Proxmox task UPID."""
        return cast(str, unwrap_data(await self._resource(node, "mgr", mgr_id).post()))

    async def mgr_delete(
        self,
        node: str,
        mgr_id: str,
        *,
        confirm_destroy: bool = False,
    ) -> str:
        """Destroy a Ceph manager and return the Proxmox task UPID."""
        self._require_confirm("mgr_delete", confirm_destroy)
        return cast(str, unwrap_data(await self._resource(node, "mgr", mgr_id).delete()))

    async def mds_create(
        self,
        node: str,
        name: str,
        *,
        hotstandby: bool | None = None,
    ) -> str:
        """Create a Ceph metadata server and return the Proxmox task UPID."""
        payload = self._dump(m.CephMDSCreateParams(hotstandby=hotstandby))
        return cast(str, unwrap_data(await self._resource(node, "mds", name).post(**payload)))

    async def mds_delete(
        self,
        node: str,
        name: str,
        *,
        confirm_destroy: bool = False,
    ) -> str:
        """Destroy a Ceph metadata server and return the Proxmox task UPID."""
        self._require_confirm("mds_delete", confirm_destroy)
        return cast(str, unwrap_data(await self._resource(node, "mds", name).delete()))

    # ------------------------------------------------------------------
    # CephFS
    # ------------------------------------------------------------------

    async def cephfs_create(
        self,
        node: str,
        name: str,
        *,
        add_storage: bool | None = None,
        pg_num: int | None = None,
    ) -> str:
        """Create a CephFS filesystem and return the Proxmox task UPID."""
        payload = self._dump(
            m.CephFSCreateParams.model_validate({"add_storage": add_storage, "pg_num": pg_num})
        )
        return cast(str, unwrap_data(await self._resource(node, "fs", name).post(**payload)))

    # ------------------------------------------------------------------
    # Service lifecycle
    # ------------------------------------------------------------------

    async def service_start(self, node: str, service: str | None = None) -> str:
        """Start Ceph services and return the Proxmox task UPID."""
        payload = self._dump(m.CephServiceParams(service=service))
        return cast(str, unwrap_data(await self._resource(node, "start").post(**payload)))

    async def service_stop(self, node: str, service: str | None = None) -> str:
        """Stop Ceph services and return the Proxmox task UPID."""
        payload = self._dump(m.CephServiceParams(service=service))
        return cast(str, unwrap_data(await self._resource(node, "stop").post(**payload)))

    async def service_restart(self, node: str, service: str | None = None) -> str:
        """Restart Ceph services and return the Proxmox task UPID."""
        payload = self._dump(m.CephServiceParams(service=service))
        return cast(str, unwrap_data(await self._resource(node, "restart").post(**payload)))

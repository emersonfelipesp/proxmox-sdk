"""RBD (RADOS Block Device) provider adapter.

RBD has no standalone HTTP API, so this adapter drives RBD operations through
the safest available provider path: the **Ceph Dashboard block API**
(``/api/block/image``).  It exposes RBD-focused typed helpers over the
underlying :class:`~proxmox_sdk.ceph.providers.dashboard.DashboardCephClient`
and applies RBD-specific safety gates (shrink, delete, protected snapshots).
"""

from __future__ import annotations

from typing import Any
from urllib.parse import quote

from proxmox_sdk.ceph.providers import models as m
from proxmox_sdk.ceph.providers.capability import ProviderCapability
from proxmox_sdk.ceph.providers.dashboard import DashboardCephClient
from proxmox_sdk.sdk.exceptions import CephCapabilityUnsupportedError


def _image_spec(pool_name: str, image_name: str, namespace: str | None = None) -> str:
    parts = [pool_name]
    if namespace:
        parts.append(namespace)
    parts.append(image_name)
    return quote("/".join(parts), safe="")


class RBDClient:
    """RBD inventory + write helpers backed by the Ceph Dashboard block API."""

    provider = "rbd"

    def __init__(self, dashboard: DashboardCephClient) -> None:
        self._dashboard = dashboard

    @staticmethod
    def _require_confirm(operation: str, confirm_destroy: bool) -> None:
        if not confirm_destroy:
            raise ValueError(f"{operation} is destructive; pass confirm_destroy=True to proceed.")

    # -- reads --------------------------------------------------------------- #
    async def list_images(self, pool_name: str | None = None) -> list[m.DashboardRBDImage]:
        return await self._dashboard.rbd_images(pool_name)

    async def get_image(self, pool_name: str, image_name: str) -> m.DashboardRBDImage | None:
        for image in await self._dashboard.rbd_images(pool_name):
            if image.name == image_name:
                return image
        return None

    # -- writes -------------------------------------------------------------- #
    async def create_image(
        self,
        pool_name: str,
        image_name: str,
        size_bytes: int,
        *,
        features: list[str] | None = None,
        namespace: str | None = None,
        data_pool: str | None = None,
        obj_size: int | None = None,
        stripe_unit: int | None = None,
        stripe_count: int | None = None,
        configuration: dict[str, Any] | None = None,
    ) -> Any:
        payload: dict[str, Any] = {
            "pool_name": pool_name,
            "name": image_name,
            "size": size_bytes,
        }
        if namespace:
            payload["namespace"] = namespace
        if features is not None:
            payload["features"] = features
        if data_pool:
            payload["data_pool"] = data_pool
        if obj_size is not None:
            payload["obj_size"] = obj_size
        if stripe_unit is not None:
            payload["stripe_unit"] = stripe_unit
        if stripe_count is not None:
            payload["stripe_count"] = stripe_count
        if configuration:
            payload["configuration"] = configuration
        return await self._dashboard.rbd_create(payload)

    async def resize_image(
        self,
        pool_name: str,
        image_name: str,
        size_bytes: int,
        *,
        namespace: str | None = None,
        current_size_bytes: int | None = None,
        allow_shrink: bool = False,
    ) -> Any:
        # Shrinking an RBD image can destroy data; gate it explicitly.
        if current_size_bytes is not None and size_bytes < current_size_bytes and not allow_shrink:
            raise ValueError("resize would shrink the image; pass allow_shrink=True to proceed.")
        spec = _image_spec(pool_name, image_name, namespace)
        return await self._dashboard.rbd_edit(spec, {"size": size_bytes})

    async def update_metadata(
        self,
        pool_name: str,
        image_name: str,
        *,
        namespace: str | None = None,
        features: list[str] | None = None,
        configuration: dict[str, Any] | None = None,
    ) -> Any:
        payload: dict[str, Any] = {}
        if features is not None:
            payload["features"] = features
        if configuration is not None:
            payload["configuration"] = configuration
        spec = _image_spec(pool_name, image_name, namespace)
        return await self._dashboard.rbd_edit(spec, payload)

    async def delete_image(
        self,
        pool_name: str,
        image_name: str,
        *,
        namespace: str | None = None,
        confirm_destroy: bool = False,
    ) -> Any:
        self._require_confirm("delete_image", confirm_destroy)
        spec = _image_spec(pool_name, image_name, namespace)
        return await self._dashboard.rbd_delete(spec, confirm_destroy=True)

    async def move_to_trash(
        self,
        pool_name: str,
        image_name: str,
        *,
        namespace: str | None = None,
        confirm_destroy: bool = False,
    ) -> Any:
        self._require_confirm("move_to_trash", confirm_destroy)
        spec = _image_spec(pool_name, image_name, namespace)
        return await self._dashboard.rbd_move_trash(spec, confirm_destroy=True)

    async def create_snapshot(
        self,
        pool_name: str,
        image_name: str,
        snapshot_name: str,
        *,
        namespace: str | None = None,
    ) -> Any:
        spec = _image_spec(pool_name, image_name, namespace)
        return await self._dashboard.rbd_snapshot_create(spec, snapshot_name)

    async def delete_snapshot(
        self,
        pool_name: str,
        image_name: str,
        snapshot_name: str,
        *,
        namespace: str | None = None,
        confirm_destroy: bool = False,
    ) -> Any:
        self._require_confirm("delete_snapshot", confirm_destroy)
        spec = _image_spec(pool_name, image_name, namespace)
        return await self._dashboard.rbd_snapshot_delete(spec, snapshot_name, confirm_destroy=True)

    # -- capability detection ----------------------------------------------- #
    async def capabilities(self) -> ProviderCapability:
        dashboard_caps = await self._dashboard.capabilities()
        if not dashboard_caps.available:
            return ProviderCapability(
                provider=self.provider,
                available=False,
                notes=["rbd requires a reachable Ceph Dashboard provider"],
            )
        return ProviderCapability(
            provider=self.provider,
            available=True,
            version=dashboard_caps.version,
            read=True,
            write=True,
            operations={
                "rbd_image:create": True,
                "rbd_image:update": True,
                "rbd_image:resize": True,
                "rbd_image:delete": True,
                "rbd_image:trash": True,
                "rbd_snapshot:create": True,
                "rbd_snapshot:delete": True,
            },
        )

    def require(self, kind: str, action: str, capability: ProviderCapability) -> None:
        if not capability.supports(kind, action):
            raise CephCapabilityUnsupportedError(f"{kind}:{action}", provider=self.provider)

"""``/admin/datastore/{store}/{groups,snapshots}`` read helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk._response_utils import normalize_list
from proxmox_sdk.pbs import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


class Snapshots:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def groups(self, store: str) -> list[m.PBSBackupGroup]:
        data = await self._sdk.admin.datastore(store).groups.get()
        return [m.PBSBackupGroup.model_validate(item) for item in normalize_list(data)]

    async def list(
        self,
        store: str,
        *,
        backup_type: m.BackupType | None = None,
        backup_id: str | None = None,
    ) -> list[m.PBSSnapshot]:
        params: dict[str, Any] = {}
        if backup_type is not None:
            params["backup-type"] = backup_type
        if backup_id is not None:
            params["backup-id"] = backup_id
        data = await self._sdk.admin.datastore(store).snapshots.get(**params)
        return [m.PBSSnapshot.model_validate(item) for item in normalize_list(data)]

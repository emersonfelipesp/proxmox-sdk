"""Read helpers for the PBS job-config endpoints.

PBS splits job config across :path:`/config/verify`, :path:`/config/prune`,
:path:`/config/sync`, and :path:`/config/tape-backup-job`. GC status is
exposed per-datastore under :path:`/admin/datastore/{store}/status` and is
not part of this helper — it is collected by ``Datastores.usage()``.

This helper normalises the four job-config endpoints into a single
:class:`~proxmox_sdk.pbs.models.PBSJob` list.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from proxmox_sdk.pbs import models as m

if TYPE_CHECKING:
    from proxmox_sdk.sdk.api import ProxmoxSDK


def _unwrap(data: Any) -> Any:
    if isinstance(data, dict) and set(data.keys()) == {"data"}:
        return data["data"]
    return data


_JOB_PATHS: dict[m.JobType, str] = {
    "verify": "config/verify",
    "prune": "config/prune",
    "sync": "config/sync",
    "tape": "config/tape-backup-job",
}


class Jobs:
    def __init__(self, sdk: ProxmoxSDK) -> None:
        self._sdk = sdk

    async def list(self, job_type: m.JobType | None = None) -> list[m.PBSJob]:
        wanted: tuple[m.JobType, ...]
        if job_type is None:
            wanted = ("verify", "prune", "sync", "tape")
        else:
            if job_type == "gc":
                raise ValueError("Use Datastores.usage(store).gc_status for GC state")
            wanted = (job_type,)
        out: list[m.PBSJob] = []
        for jt in wanted:
            resource = self._sdk(_JOB_PATHS[jt])
            data = _unwrap(await resource.get())
            for item in data or []:
                payload = dict(item)
                payload["job_type"] = jt
                out.append(m.PBSJob.model_validate(payload))
        return out

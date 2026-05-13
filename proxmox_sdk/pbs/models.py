"""Pydantic v2 response models for PBS read-only endpoints.

Hand-coded to cover the v1 surface (datastores, backup groups + snapshots,
jobs, node status, version). The codegen pipeline can later replace this
module with generated content; downstream consumers should import from
``proxmox_sdk.pbs.models`` so the swap is transparent.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class _PBSBase(BaseModel):
    """Permissive base: PBS payloads carry forward-compatible extra fields."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


# --- /version -----------------------------------------------------------------


class PBSVersion(_PBSBase):
    version: str
    release: str | None = None
    repoid: str | None = None


# --- /nodes/{node}/status -----------------------------------------------------


class PBSCPUInfo(_PBSBase):
    cpus: int | None = None
    model: str | None = None


class PBSMemoryInfo(_PBSBase):
    total: int | None = None
    used: int | None = None
    free: int | None = None


class PBSNodeStatus(_PBSBase):
    uptime: int | None = None
    cpu: float | None = None
    loadavg: list[float] | None = None
    memory: PBSMemoryInfo | None = None
    cpuinfo: PBSCPUInfo | None = None
    kversion: str | None = None
    boot_mode: dict | None = None


# --- /admin/datastore ---------------------------------------------------------


GCStatus = Literal["ok", "running", "error", "pending", "unknown"]


class PBSDatastore(_PBSBase):
    """Entry returned by ``GET /admin/datastore``."""

    name: str = Field(alias="store")
    path: str | None = None
    comment: str | None = None
    total: int | None = None
    used: int | None = None
    avail: int | None = None
    history: list[float] | None = None
    estimated_full_date: int | None = Field(default=None, alias="estimated-full-date")
    gc_status: GCStatus | None = Field(default=None, alias="gc-status")


# --- /admin/datastore/{store}/groups ------------------------------------------

BackupType = Literal["vm", "ct", "host"]


class PBSBackupGroup(_PBSBase):
    backup_type: BackupType = Field(alias="backup-type")
    backup_id: str = Field(alias="backup-id")
    last_backup: int | None = Field(default=None, alias="last-backup")
    backup_count: int | None = Field(default=None, alias="backup-count")
    files: list[str] | None = None
    owner: str | None = None
    comment: str | None = None


# --- /admin/datastore/{store}/snapshots ---------------------------------------


VerifyState = Literal["ok", "failed", "none", "pending"]


class PBSSnapshotFile(_PBSBase):
    filename: str
    size: int | None = None
    crypt_mode: str | None = Field(default=None, alias="crypt-mode")


class PBSSnapshotVerification(_PBSBase):
    state: VerifyState | None = None
    upid: str | None = None


class PBSSnapshot(_PBSBase):
    backup_type: BackupType = Field(alias="backup-type")
    backup_id: str = Field(alias="backup-id")
    backup_time: int = Field(alias="backup-time")
    size: int | None = None
    owner: str | None = None
    protected: bool | None = None
    comment: str | None = None
    files: list[PBSSnapshotFile] | None = None
    verification: PBSSnapshotVerification | None = None
    fingerprint: str | None = None


# --- /config/{verify,prune,sync,tape-backup-job} + /admin/gc ------------------


JobType = Literal["verify", "prune", "gc", "sync", "tape"]
JobRunState = Literal["ok", "error", "warning", "running", "unknown"]


class PBSJob(_PBSBase):
    """Unified read-only view across the PBS job endpoints.

    The PBS REST surface has separate config endpoints per job type; this
    model normalizes their common fields so downstream code can iterate one
    list.
    """

    job_type: JobType
    job_id: str = Field(alias="id")
    store: str | None = None
    schedule: str | None = None
    comment: str | None = None
    disable: bool | None = None
    last_run_upid: str | None = Field(default=None, alias="last-run-upid")
    last_run_state: JobRunState | None = Field(default=None, alias="last-run-state")
    last_run_endtime: int | None = Field(default=None, alias="last-run-endtime")
    next_run: int | None = Field(default=None, alias="next-run")


__all__ = [
    "BackupType",
    "GCStatus",
    "JobRunState",
    "JobType",
    "PBSBackupGroup",
    "PBSCPUInfo",
    "PBSDatastore",
    "PBSJob",
    "PBSMemoryInfo",
    "PBSNodeStatus",
    "PBSSnapshot",
    "PBSSnapshotFile",
    "PBSSnapshotVerification",
    "PBSVersion",
    "VerifyState",
]

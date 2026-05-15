"""Permissive Pydantic v2 models for Proxmox VE Ceph read endpoints."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class _CephBase(BaseModel):
    """Ceph payloads vary by Proxmox/Ceph release; preserve unknown fields."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


HealthState = Literal["HEALTH_OK", "HEALTH_WARN", "HEALTH_ERR", "unknown"]
DaemonType = Literal["mon", "mgr", "mds", "osd", "unknown"]


class CephClusterStatus(_CephBase):
    """Cluster-wide status from ``GET /cluster/ceph/status``."""

    health: str | dict[str, Any] | None = None
    fsid: str | None = None
    election_epoch: int | None = None
    quorum: list[int] | None = None
    quorum_names: list[str] | None = None
    monmap: dict[str, Any] | None = None
    osdmap: dict[str, Any] | None = None
    pgmap: dict[str, Any] | None = None
    mgrmap: dict[str, Any] | None = None
    mdsmap: dict[str, Any] | None = None
    servicemap: dict[str, Any] | None = None


class CephClusterMetadata(_CephBase):
    """Daemon metadata from ``GET /cluster/ceph/metadata``."""

    mon: dict[str, Any] | None = None
    mgr: dict[str, Any] | None = None
    mds: dict[str, Any] | None = None
    osd: dict[str, Any] | None = None


class CephFlag(_CephBase):
    """A cluster-level Ceph flag."""

    name: str | None = None
    value: bool | int | str | None = None
    enabled: bool | None = None


class CephDaemon(_CephBase):
    """Common daemon record for MON, MGR, MDS, and OSD views."""

    name: str | None = Field(default=None, validation_alias=AliasChoices("name", "id", "monid"))
    daemon_id: str | int | None = Field(
        default=None, validation_alias=AliasChoices("id", "name", "monid")
    )
    daemon_type: DaemonType | str | None = Field(default=None, alias="type")
    host: str | None = None
    status: str | None = None
    state: str | None = None
    addr: str | None = None
    version: str | None = None


class CephOSD(_CephBase):
    """OSD inventory/status record."""

    osd_id: int | str | None = Field(
        default=None, validation_alias=AliasChoices("id", "osdid", "osd")
    )
    name: str | None = None
    host: str | None = None
    status: str | None = None
    up: bool | int | None = None
    in_cluster: bool | int | None = Field(default=None, alias="in")
    reweight: float | None = None
    weight: float | None = None
    used: int | None = None
    avail: int | None = None
    total: int | None = None
    pgs: int | None = None
    device_class: str | None = None
    crush_weight: float | None = None


class CephPool(_CephBase):
    """Ceph pool record from ``/nodes/{node}/ceph/pool``."""

    name: str | None = Field(
        default=None, validation_alias=AliasChoices("pool_name", "pool-name", "name")
    )
    pool_id: int | None = Field(
        default=None, validation_alias=AliasChoices("pool", "pool_id", "pool-id")
    )
    size: int | None = None
    min_size: int | None = None
    pg_num: int | None = None
    pg_autoscale_mode: str | None = None
    crush_rule: str | int | None = None
    application: str | None = None
    bytes_used: int | None = None
    max_avail: int | None = None
    percent_used: float | None = None


class CephFilesystem(_CephBase):
    """CephFS record from ``/nodes/{node}/ceph/fs``."""

    name: str | None = None
    metadata_pool: str | None = None
    data_pools: list[str] | None = None
    standby_count_wanted: int | None = None


class CephCrushRule(_CephBase):
    """CRUSH rule record."""

    name: str | None = None
    rule_id: int | None = Field(
        default=None, validation_alias=AliasChoices("rule_id", "ruleid", "id")
    )
    type: str | None = None
    steps: list[dict[str, Any]] | None = None


class CephLogLine(_CephBase):
    """Ceph log entry."""

    t: str | int | None = None
    n: int | None = None
    msg: str | None = None
    priority: str | None = None


__all__ = [
    "CephClusterMetadata",
    "CephClusterStatus",
    "CephCrushRule",
    "CephDaemon",
    "CephFilesystem",
    "CephFlag",
    "CephLogLine",
    "CephOSD",
    "CephPool",
    "DaemonType",
    "HealthState",
]

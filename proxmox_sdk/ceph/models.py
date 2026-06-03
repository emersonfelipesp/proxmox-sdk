"""Permissive Pydantic v2 models for Proxmox VE Ceph endpoints."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class _CephBase(BaseModel):
    """Ceph payloads vary by Proxmox/Ceph release; preserve unknown fields."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


HealthState = Literal["HEALTH_OK", "HEALTH_WARN", "HEALTH_ERR", "unknown"]
DaemonType = Literal["mon", "mgr", "mds", "osd", "unknown"]
CephFlagName = Literal[
    "nobackfill",
    "nodeep-scrub",
    "nodown",
    "noin",
    "noout",
    "norebalance",
    "norecover",
    "noscrub",
    "notieragent",
    "noup",
    "pause",
]
CephPoolApplication = Literal["rbd", "cephfs", "rgw"]
CephPGAutoscaleMode = Literal["on", "off", "warn"]


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


class CephFlagUpdateParams(_CephBase):
    """Request body for ``PUT /cluster/ceph/flags/{flag}``."""

    value: bool


class CephPoolCreateParams(_CephBase):
    """Request body for ``POST /nodes/{node}/ceph/pool``."""

    name: str
    add_storages: bool | None = None
    application: CephPoolApplication | str | None = None
    crush_rule: str | None = None
    erasure_coding: str | None = Field(default=None, alias="erasure-coding")
    min_size: int | None = None
    pg_autoscale_mode: CephPGAutoscaleMode | str | None = None
    pg_num: int | None = None
    pg_num_min: int | None = None
    size: int | None = None
    target_size: str | None = None
    target_size_ratio: float | None = None


class CephPoolSetParams(_CephBase):
    """Request body for ``PUT /nodes/{node}/ceph/pool/{name}``."""

    application: CephPoolApplication | str | None = None
    crush_rule: str | None = None
    min_size: int | None = None
    pg_autoscale_mode: CephPGAutoscaleMode | str | None = None
    pg_num: int | None = None
    pg_num_min: int | None = None
    size: int | None = None
    target_size: str | None = None
    target_size_ratio: float | None = None


class CephPoolDeleteParams(_CephBase):
    """Request params for ``DELETE /nodes/{node}/ceph/pool/{name}``."""

    force: bool | None = None
    remove_ecprofile: bool | None = None
    remove_storages: bool | None = None


class CephOSDCreateParams(_CephBase):
    """Request body for ``POST /nodes/{node}/ceph/osd``."""

    dev: str
    crush_device_class: str | None = Field(default=None, alias="crush-device-class")
    db_dev: str | None = None
    db_dev_size: float | None = None
    encrypted: bool | None = None
    osds_per_device: int | None = Field(default=None, alias="osds-per-device")
    wal_dev: str | None = None
    wal_dev_size: float | None = None


class CephOSDDeleteParams(_CephBase):
    """Request params for ``DELETE /nodes/{node}/ceph/osd/{osdid}``."""

    cleanup: bool | None = None


class CephMonCreateParams(_CephBase):
    """Request body for ``POST /nodes/{node}/ceph/mon/{monid}``."""

    mon_address: str | None = Field(default=None, alias="mon-address")


class CephMDSCreateParams(_CephBase):
    """Request body for ``POST /nodes/{node}/ceph/mds/{name}``."""

    hotstandby: bool | None = None


class CephFSCreateParams(_CephBase):
    """Request body for ``POST /nodes/{node}/ceph/fs/{name}``."""

    add_storage: bool | None = Field(default=None, alias="add-storage")
    pg_num: int | None = None


class CephServiceParams(_CephBase):
    """Request body for node-scoped Ceph service lifecycle helpers."""

    service: str | None = None


__all__ = [
    "CephFSCreateParams",
    "CephFlagName",
    "CephFlagUpdateParams",
    "CephClusterMetadata",
    "CephClusterStatus",
    "CephCrushRule",
    "CephDaemon",
    "CephFilesystem",
    "CephFlag",
    "CephLogLine",
    "CephOSD",
    "CephOSDCreateParams",
    "CephOSDDeleteParams",
    "CephMDSCreateParams",
    "CephMonCreateParams",
    "CephPGAutoscaleMode",
    "CephPool",
    "CephPoolApplication",
    "CephPoolCreateParams",
    "CephPoolDeleteParams",
    "CephPoolSetParams",
    "CephServiceParams",
    "DaemonType",
    "HealthState",
]

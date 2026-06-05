"""Provider-neutral Pydantic models for direct Ceph providers.

These mirror the permissive, forward-compatible style of
:mod:`proxmox_sdk.ceph.models` (``extra="allow"``) so payloads from differing
Ceph Dashboard / RGW versions parse without loss.  Stable fields used by the
``proxbox-api`` orchestration layer are typed; everything else is preserved.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

DashboardHealthStatus = Literal["HEALTH_OK", "HEALTH_WARN", "HEALTH_ERR", "unknown"]


class _ProviderBase(BaseModel):
    """Permissive base for provider payloads (preserve unknown fields)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


# --------------------------------------------------------------------------- #
# Ceph Dashboard API
# --------------------------------------------------------------------------- #
class DashboardHealth(_ProviderBase):
    """Normalised cluster health from ``GET /api/health/minimal``."""

    status: DashboardHealthStatus | str | None = None
    checks: list[dict[str, Any]] | dict[str, Any] | None = None
    mon_status: dict[str, Any] | None = None


class DashboardHost(_ProviderBase):
    """Host record from ``GET /api/host``."""

    hostname: str | None = None
    addr: str | None = None
    labels: list[str] | None = None
    services: list[dict[str, Any]] | None = None
    status: str | None = None


class DashboardOSD(_ProviderBase):
    """OSD record from ``GET /api/osd``."""

    osd: int | None = Field(default=None, validation_alias=AliasChoices("osd", "id"))
    uuid: str | None = None
    up: bool | int | None = None
    in_cluster: bool | int | None = Field(default=None, alias="in")
    device_class: str | None = None
    host: str | dict[str, Any] | None = None


class DashboardPool(_ProviderBase):
    """Pool record from ``GET /api/pool``."""

    pool_name: str | None = Field(default=None, validation_alias=AliasChoices("pool_name", "name"))
    pool: int | None = Field(default=None, validation_alias=AliasChoices("pool", "pool_id"))
    size: int | None = None
    min_size: int | None = None
    pg_num: int | None = None
    type: str | None = None
    application_metadata: list[str] | dict[str, Any] | None = None
    crush_rule: str | int | None = None


class DashboardFilesystem(_ProviderBase):
    """CephFS record from ``GET /api/cephfs``."""

    id: int | None = None
    mdsmap: dict[str, Any] | None = None
    name: str | None = None


class DashboardRBDImage(_ProviderBase):
    """RBD image record from ``GET /api/block/image``."""

    name: str | None = None
    pool_name: str | None = Field(default=None, validation_alias=AliasChoices("pool_name", "pool"))
    namespace: str | None = None
    id: str | None = None
    size: int | None = None
    obj_size: int | None = None
    num_objs: int | None = None
    features_name: list[str] | None = None
    snapshots: list[dict[str, Any]] | None = None
    parent: dict[str, Any] | None = None
    stripe_count: int | None = None
    stripe_unit: int | None = None
    data_pool: str | None = None


class DashboardRGWDaemon(_ProviderBase):
    """RGW daemon record from ``GET /api/rgw/daemon``."""

    id: str | None = None
    version: str | None = None
    server_hostname: str | None = None
    realm_name: str | None = None
    zonegroup_name: str | None = None
    zone_name: str | None = None


class DashboardRGWBucket(_ProviderBase):
    """RGW bucket record from ``GET /api/rgw/bucket``."""

    bucket: str | None = Field(default=None, validation_alias=AliasChoices("bucket", "name"))
    owner: str | None = None
    tenant: str | None = None
    num_objects: int | None = None
    size: int | None = None
    placement_rule: str | None = None
    versioning: str | None = None


# --------------------------------------------------------------------------- #
# RGW Admin Ops API
# --------------------------------------------------------------------------- #
class RGWUser(_ProviderBase):
    """User record from ``GET /admin/user``."""

    user_id: str | None = Field(default=None, validation_alias=AliasChoices("user_id", "uid"))
    display_name: str | None = None
    email: str | None = None
    suspended: int | bool | None = None
    max_buckets: int | None = None
    tenant: str | None = None
    # keys are intentionally NOT typed here; callers must redact secret keys.


class RGWBucket(_ProviderBase):
    """Bucket record from ``GET /admin/bucket``."""

    bucket: str | None = None
    owner: str | None = None
    tenant: str | None = None
    num_objects: int | None = None
    size_kb_actual: int | None = None
    placement_rule: str | None = None
    zonegroup: str | None = None


class RGWUsage(_ProviderBase):
    """Usage summary from ``GET /admin/usage``."""

    entries: list[dict[str, Any]] | None = None
    summary: list[dict[str, Any]] | None = None


__all__ = [
    "DashboardFilesystem",
    "DashboardHealth",
    "DashboardHealthStatus",
    "DashboardHost",
    "DashboardOSD",
    "DashboardPool",
    "DashboardRBDImage",
    "DashboardRGWBucket",
    "DashboardRGWDaemon",
    "RGWBucket",
    "RGWUsage",
    "RGWUser",
]

"""Pydantic v2 response models for Proxmox Datacenter Manager (PDM) endpoints.

Hand-coded to cover the PDM API surface described in the Proxmox Datacenter
Manager 1.0 admin guide Appendix A and the upstream API viewer
(https://pdm.proxmox.com/docs/api-viewer/). The codegen pipeline can later
replace this module with generated content; downstream consumers should
import from ``proxmox_sdk.pdm.models`` so the swap is transparent.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class _PDMBase(BaseModel):
    """Permissive base: PDM payloads carry forward-compatible extra fields."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


# --- /version -----------------------------------------------------------------


class PDMVersion(_PDMBase):
    version: str
    release: str | None = None
    repoid: str | None = None


# --- Remotes ------------------------------------------------------------------

RemoteType = Literal["pve", "pbs"]


class PDMRemoteNode(_PDMBase):
    """A single node entry inside a remote configuration."""

    hostname: str
    fingerprint: str | None = None


class PDMRemote(_PDMBase):
    """Entry returned by ``GET /remotes`` describing a registered remote."""

    id: str
    type: RemoteType
    nodes: list[PDMRemoteNode] | None = None
    authid: str | None = None
    token: str | None = None
    fingerprint: str | None = None
    web_url: str | None = Field(default=None, alias="web-url")

    @field_validator("nodes", mode="before")
    @classmethod
    def normalize_node_addresses(cls, value: Any) -> Any:
        """Normalize schema-level address strings to the public node model."""

        if not isinstance(value, list):
            return value
        return [{"hostname": item} if isinstance(item, str) else item for item in value]


class PDMRemoteVersion(_PDMBase):
    version: str
    release: str | None = None
    repoid: str | None = None


# --- PVE guests ---------------------------------------------------------------

GuestType = Literal["qemu", "lxc"]
GuestStatus = Literal["running", "stopped", "paused", "suspended", "unknown"]


class PDMGuest(_PDMBase):
    """A QEMU VM or LXC container exposed via the PDM PVE domain."""

    remote: str
    vmid: int
    name: str | None = None
    type: GuestType | None = None
    status: GuestStatus | None = None
    node: str | None = None
    cpu: float | None = None
    cpus: int | None = None
    mem: int | None = None
    maxmem: int | None = None
    disk: int | None = None
    maxdisk: int | None = None
    uptime: int | None = None
    tags: str | None = None
    template: bool | None = None
    lock: str | None = None


class PDMGuestConfig(_PDMBase):
    """Free-form configuration dump for a guest (keys vary by guest type)."""

    digest: str | None = None
    name: str | None = None
    cores: int | None = None
    sockets: int | None = None
    memory: int | None = None
    ostype: str | None = None
    boot: str | None = None
    onboot: bool | None = None


class PDMNode(_PDMBase):
    """A PVE node entry surfaced via the PDM API."""

    remote: str
    node: str
    status: str | None = None
    type: str | None = None
    cpu: float | None = None
    maxcpu: int | None = None
    mem: int | None = None
    maxmem: int | None = None
    uptime: int | None = None
    level: str | None = None


class PDMTask(_PDMBase):
    """A task entry returned by PDM PVE/PBS task endpoints."""

    upid: str = Field(alias="upid")
    node: str | None = None
    type: str | None = None
    id: str | None = None
    user: str | None = None
    starttime: int | None = None
    endtime: int | None = None
    status: str | None = None
    exitstatus: str | None = None


class PDMTaskStatus(_PDMBase):
    upid: str
    node: str | None = None
    status: str | None = None
    exitstatus: str | None = None
    starttime: int | None = None
    endtime: int | None = None
    type: str | None = None


class PDMRRDData(_PDMBase):
    """Single RRD sample (shape varies by resource)."""

    time: int | None = None
    cpu: float | None = None
    mem: float | None = None
    maxmem: float | None = None
    disk: float | None = None
    maxdisk: float | None = None
    netin: float | None = None
    netout: float | None = None


# --- PBS ----------------------------------------------------------------------


class PDMPBSDatastore(_PDMBase):
    remote: str
    store: str
    total: int | None = None
    used: int | None = None
    avail: int | None = None
    comment: str | None = None


class PDMPBSSnapshot(_PDMBase):
    remote: str
    store: str
    namespace: str | None = None
    backup_type: str = Field(alias="backup-type")
    backup_id: str = Field(alias="backup-id")
    backup_time: int = Field(alias="backup-time")
    size: int | None = None
    owner: str | None = None
    protected: bool | None = None


# --- Resources / Subscriptions -----------------------------------------------


class PDMResource(_PDMBase):
    """Global resource entry across all registered remotes."""

    remote: str
    type: str
    id: str
    name: str | None = None
    node: str | None = None
    status: str | None = None
    cpu: float | None = None
    mem: int | None = None
    maxmem: int | None = None
    disk: int | None = None
    maxdisk: int | None = None


class PDMResourceStatus(_PDMBase):
    remote: str
    status: str | None = None
    error: str | None = None


class PDMSubscription(_PDMBase):
    remote: str
    status: str | None = None
    productname: str | None = None
    serverid: str | None = None
    checktime: int | None = None
    nexttime: int | None = None
    level: str | None = None
    message: str | None = None


# --- Metric collection --------------------------------------------------------


class PDMMetricCollectionStatus(_PDMBase):
    last_collection: int | None = Field(default=None, alias="last-collection")
    enabled: bool | None = None
    status: str | None = None
    error: str | None = None


# --- Access -------------------------------------------------------------------


class PDMUser(_PDMBase):
    userid: str
    comment: str | None = None
    enable: bool | None = None
    expire: int | None = None
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None


class PDMACLEntry(_PDMBase):
    path: str
    type: str
    ugid: str
    roleid: str
    propagate: bool | None = None


class PDMTFAEntry(_PDMBase):
    id: str
    type: str
    description: str | None = None
    enable: bool | None = None
    created: int | None = None


class PDMAPIToken(_PDMBase):
    tokenid: str
    comment: str | None = None
    expire: int | None = None
    privsep: bool | None = None


# --- Views --------------------------------------------------------------------


class PDMViewRule(_PDMBase):
    """An include/exclude filter rule inside a custom view."""

    type: Literal["include", "exclude"]
    pattern: str
    field: str | None = None


class PDMView(_PDMBase):
    """A custom cross-remote resource view dashboard."""

    id: str
    name: str | None = None
    comment: str | None = None
    rules: list[PDMViewRule] | None = None
    config: dict[str, Any] | None = None


__all__ = [
    "GuestStatus",
    "GuestType",
    "PDMACLEntry",
    "PDMAPIToken",
    "PDMGuest",
    "PDMGuestConfig",
    "PDMMetricCollectionStatus",
    "PDMNode",
    "PDMPBSDatastore",
    "PDMPBSSnapshot",
    "PDMRRDData",
    "PDMRemote",
    "PDMRemoteNode",
    "PDMRemoteVersion",
    "PDMResource",
    "PDMResourceStatus",
    "PDMSubscription",
    "PDMTFAEntry",
    "PDMTask",
    "PDMTaskStatus",
    "PDMUser",
    "PDMVersion",
    "PDMView",
    "PDMViewRule",
    "RemoteType",
]

"""Pydantic v2 response models for Proxmox Datacenter Manager (PDM) endpoints.

Hand-coded to cover the PDM API surface described in the Proxmox Datacenter
Manager 1.0 admin guide Appendix A and the upstream API viewer
(https://pdm.proxmox.com/docs/api-viewer/). The codegen pipeline can later
replace this module with generated content; downstream consumers should
import from ``proxmox_sdk.pdm.models`` so the swap is transparent.
"""

from __future__ import annotations

from typing import Any, Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field, field_validator


class _PDMBase(BaseModel):
    """Permissive base: PDM payloads carry forward-compatible extra fields."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)


# --- /version -----------------------------------------------------------------


class PDMVersion(_PDMBase):
    version: str
    release: str
    repoid: str


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
    release: str
    repoid: str
    console: Literal["applet", "vv", "html5", "xtermjs"] | None = None


# --- PVE guests ---------------------------------------------------------------

GuestType = Literal["qemu", "lxc"]
GuestStatus = Literal["running", "stopped", "paused", "suspended", "unknown"]
PDMGuestConfigState = Literal["pending", "active"]
PDMRRDConsolidation = Literal["MAX", "AVERAGE"]
PDMRRDTimeframe = Literal["hour", "day", "week", "month", "year", "decade"]


class PDMGuest(_PDMBase):
    """A QEMU VM or LXC container exposed via the PDM PVE domain."""

    remote: str
    vmid: int
    name: str | None = None
    type: GuestType | None = None
    status: GuestStatus | None = None
    node: str | None = None
    cpu: float | None = None
    cpus: float | None = None
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
    memory: int | str | None = None
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
    node: str
    pid: int
    pstart: int
    starttime: int
    status: Literal["running", "stopped"]
    type: str
    user: str
    id: str | None = None
    exitstatus: str | None = None
    endtime: int | None = None


class PDMRRDData(_PDMBase):
    """Single RRD sample (shape varies by resource)."""

    time: int | None = None
    cpu: float | None = Field(
        default=None,
        validation_alias=AliasChoices("cpu", "cpu-current"),
    )
    mem: float | None = Field(
        default=None,
        validation_alias=AliasChoices("mem", "mem-used"),
    )
    maxmem: float | None = Field(
        default=None,
        validation_alias=AliasChoices("maxmem", "mem-total"),
    )
    disk: float | None = None
    disk_used: float | None = Field(default=None, alias="disk-used")
    disk_available: float | None = Field(default=None, alias="disk-available")
    maxdisk: float | None = Field(
        default=None,
        validation_alias=AliasChoices("maxdisk", "disk-total"),
    )
    netin: float | None = Field(
        default=None,
        validation_alias=AliasChoices("netin", "net-in"),
    )
    netout: float | None = Field(
        default=None,
        validation_alias=AliasChoices("netout", "net-out"),
    )
    disk_read: float | None = Field(default=None, alias="disk-read")
    disk_write: float | None = Field(default=None, alias="disk-write")
    uptime: float | None = None


# --- PBS ----------------------------------------------------------------------


class PDMPBSDatastore(_PDMBase):
    remote: str
    store: str = Field(
        validation_alias=AliasChoices("store", "name"),
        serialization_alias="name",
    )
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

PDMResourceType = Literal[
    "storage",
    "qemu",
    "lxc",
    "node",
    "network",
    "pve-storage",
    "pve-qemu",
    "pve-lxc",
    "pve-node",
    "pve-network",
    "pbs-node",
    "pbs-datastore",
]


class PDMResource(_PDMBase):
    """Global resource entry across all registered remotes."""

    remote: str
    remote_error: str | None = None
    type: PDMResourceType
    id: str
    name: str | None = None
    node: str | None = None
    status: str | None = None
    cpu: float | None = None
    mem: int | None = None
    maxmem: int | None = None
    disk: int | None = None
    maxdisk: int | None = None
    maxcpu: float | None = None
    uptime: int | None = None
    vmid: int | None = None
    pool: str | None = None
    storage: str | None = None
    tags: list[str] | None = None
    template: bool | None = None
    shared: bool | None = None
    level: str | None = None
    network: str | None = None
    protocol: str | None = None
    legacy: bool | None = None
    zone_type: str | None = Field(default=None, alias="zone-type")
    cgroup_mode: int | None = Field(default=None, alias="cgroup-mode")
    usage: float | None = None
    backend_type: str | None = Field(default=None, alias="backend-type")
    backing_device: str | None = Field(default=None, alias="backing-device")
    maintenance: str | None = None


class PDMResourceStatus(_PDMBase):
    remote: str
    status: str | None = None
    error: str | None = None
    resources: list[PDMResource]


class PDMSubscription(_PDMBase):
    remote: str
    error: str | None = None
    state: Literal["none", "unknown", "mixed", "active"] | None = None
    node_status: dict[str, Any] | None = Field(default=None, alias="node-status")
    status: str | None = None
    productname: str | None = None
    serverid: str | None = None
    checktime: int | None = None
    nexttime: int | None = None
    level: str | None = None
    message: str | None = None


# --- Metric collection --------------------------------------------------------


class PDMMetricCollectionStatus(_PDMBase):
    remote: str
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
    type: Literal["user", "group"] = Field(
        validation_alias=AliasChoices("type", "ugid_type"),
        serialization_alias="ugid_type",
    )
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
    token_name: str | None = Field(default=None, alias="token-name")
    enable: bool | None = None
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
    include: list[str] | None = None
    exclude: list[str] | None = None
    include_all: bool | None = Field(default=None, alias="include-all")
    layout: str | None = None


__all__ = [
    "GuestStatus",
    "GuestType",
    "PDMACLEntry",
    "PDMAPIToken",
    "PDMGuest",
    "PDMGuestConfigState",
    "PDMGuestConfig",
    "PDMMetricCollectionStatus",
    "PDMNode",
    "PDMPBSDatastore",
    "PDMPBSSnapshot",
    "PDMRRDData",
    "PDMRRDConsolidation",
    "PDMRRDTimeframe",
    "PDMRemote",
    "PDMRemoteNode",
    "PDMRemoteVersion",
    "PDMResource",
    "PDMResourceType",
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

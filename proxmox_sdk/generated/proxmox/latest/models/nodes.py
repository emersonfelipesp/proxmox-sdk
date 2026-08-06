"""Generated Pydantic v2 schemas for Proxmox route group 'nodes'.

Do not edit by hand. Regenerate from the matching OpenAPI artifact.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, RootModel, StrictBool, StrictInt, StrictStr

GENERATED_FOR_PROXMOX_VERSION = "latest"
GENERATED_SOURCE_SHA256 = "16bd9329d954c0de7c4ac55e8dd78c10e0f1d84899c42aeac06eadf6904dd96b"
GENERATED_AT = "2026-08-06T18:55:01.885818+00:00"


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')


def _allowed_ints(allowed: tuple[int, ...]) -> AfterValidator:
    def validate(value: int) -> int:
        if value not in allowed:
            raise ValueError('value is not an allowed schema member')
        return value

    return AfterValidator(validate)

class GetNodesResponseItem(ProxmoxBaseModel):
    """Model for index. Cluster node index. response."""
    cpu: float | None = Field(None, description='CPU utilization.')
    level: StrictStr | None = Field(None, description='Support level.')
    maxcpu: int | None = Field(None, description='Number of available CPUs.')
    maxmem: int | None = Field(None, description='Number of available memory in bytes.')
    mem: int | None = Field(None, description='Used memory in bytes.')
    node: StrictStr | None = Field(None, description='The cluster node name.')
    ssl_fingerprint: StrictStr | None = Field(None, description='The SSL fingerprint for the node certificate.')
    status: StrictStr | None = Field(None, description='Node status.')
    uptime: int | None = Field(None, description='Node uptime in seconds.')

class GetNodesResponse(RootModel[list[GetNodesResponseItem]]):
    """List of items. index. Cluster node index. response."""
    root: list[GetNodesResponseItem] = Field(...)

class GetNodesNodeResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Node index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeAplinfoResponse(RootModel[list[dict[str, object]]]):
    """Model for aplinfo. Get list of appliances. response."""
    root: list[dict[str, object]] = Field(...)

class PostNodesNodeAplinfoRequest(ProxmoxBaseModel):
    """Model for apl_download. Download appliance templates. request."""
    storage: StrictStr = Field(..., description='The storage where the template will be stored')
    template: StrictStr = Field(..., description='The template which will downloaded')

class PostNodesNodeAplinfoResponse(RootModel[StrictStr]):
    """Model for apl_download. Download appliance templates. response."""
    root: StrictStr = Field(...)

class GetNodesNodeAptResponseItem(ProxmoxBaseModel):
    """Model for index. Directory index for apt (Advanced Package Tool). response."""
    id: StrictStr | None = Field(None)

class GetNodesNodeAptResponse(RootModel[list[GetNodesNodeAptResponseItem]]):
    """List of items. index. Directory index for apt (Advanced Package Tool). response."""
    root: list[GetNodesNodeAptResponseItem] = Field(...)

class GetNodesNodeAptChangelogResponse(RootModel[StrictStr]):
    """Model for changelog. Get package changelogs. response."""
    root: StrictStr = Field(...)

class GetNodesNodeAptRepositoriesResponse(ProxmoxBaseModel):
    """Model for repositories. Get APT repository information. response."""
    digest: StrictStr = Field(..., description='Common digest of all files.')
    errors: list[dict[str, object]] = Field(..., description='List of problematic repository files.')
    files: list[dict[str, object]] = Field(..., description='List of parsed repository files.')
    infos: list[dict[str, object]] = Field(..., description='Additional information/warnings for APT repositories.')
    standard_repos: list[dict[str, object]] = Field(..., alias="standard-repos", description='List of standard repositories and their configuration status')

class PostNodesNodeAptRepositoriesRequest(ProxmoxBaseModel):
    """Model for change_repository. Change the properties of a repository. Currently only allows enabling/disabling. request."""
    digest: StrictStr | None = Field(None, description='Digest to detect modifications.')
    enabled: bool | None = Field(None, description='Whether the repository should be enabled or not.')
    index: int = Field(..., description='Index within the file (starting from 0).')
    path: StrictStr = Field(..., description='Path to the containing file.')

class PostNodesNodeAptRepositoriesResponse(RootModel[None]):
    """Model for change_repository. Change the properties of a repository. Currently only allows enabling/disabling. response."""
    root: None = Field(...)

class PutNodesNodeAptRepositoriesRequest(ProxmoxBaseModel):
    """Model for add_repository. Add a standard repository to the configuration request."""
    digest: StrictStr | None = Field(None, description='Digest to detect modifications.')
    handle: StrictStr = Field(..., description='Handle that identifies a repository.')

class PutNodesNodeAptRepositoriesResponse(RootModel[None]):
    """Model for add_repository. Add a standard repository to the configuration response."""
    root: None = Field(...)

class GetNodesNodeAptUpdateResponseItem(ProxmoxBaseModel):
    """Model for list_updates. List available updates. response."""
    arch: StrictStr | None = Field(None, alias="Arch", description='Package Architecture.')
    description: StrictStr | None = Field(None, alias="Description", description='Package description.')
    notify_status: StrictStr | None = Field(None, alias="NotifyStatus", description='Version for which PVE has already sent an update notification for.')
    old_version: StrictStr | None = Field(None, alias="OldVersion", description='Old version currently installed.')
    origin: StrictStr | None = Field(None, alias="Origin", description="Package origin, e.g., 'Proxmox' or 'Debian'.")
    package: StrictStr | None = Field(None, alias="Package", description='Package name.')
    priority: StrictStr | None = Field(None, alias="Priority", description='Package priority.')
    section: StrictStr | None = Field(None, alias="Section", description='Package section.')
    title: StrictStr | None = Field(None, alias="Title", description='Package title.')
    version: StrictStr | None = Field(None, alias="Version", description='New version to be updated to.')

class GetNodesNodeAptUpdateResponse(RootModel[list[GetNodesNodeAptUpdateResponseItem]]):
    """List of items. list_updates. List available updates. response."""
    root: list[GetNodesNodeAptUpdateResponseItem] = Field(...)

class PostNodesNodeAptUpdateRequest(ProxmoxBaseModel):
    """Model for update_database. This is used to resynchronize the package index files from their sources (apt-get update). request."""
    notify: bool | None = Field(None, description='Send notification about new packages.')
    quiet: bool | None = Field(None, description='Only produces output suitable for logging, omitting progress indicators.')

class PostNodesNodeAptUpdateResponse(RootModel[StrictStr]):
    """Model for update_database. This is used to resynchronize the package index files from their sources (apt-get update). response."""
    root: StrictStr = Field(...)

class GetNodesNodeAptVersionsResponseItem(ProxmoxBaseModel):
    """Model for versions. Get package information for important Proxmox packages. response."""
    arch: StrictStr | None = Field(None, alias="Arch", description='Package Architecture.')
    current_state: StrictStr | None = Field(None, alias="CurrentState", description='Current state of the package installed on the system.')
    description: StrictStr | None = Field(None, alias="Description", description='Package description.')
    manager_version: StrictStr | None = Field(None, alias="ManagerVersion", description='Version of the currently running pve-manager API server.')
    notify_status: StrictStr | None = Field(None, alias="NotifyStatus", description='Version for which PVE has already sent an update notification for.')
    old_version: StrictStr | None = Field(None, alias="OldVersion", description='Old version currently installed.')
    origin: StrictStr | None = Field(None, alias="Origin", description="Package origin, e.g., 'Proxmox' or 'Debian'.")
    package: StrictStr | None = Field(None, alias="Package", description='Package name.')
    priority: StrictStr | None = Field(None, alias="Priority", description='Package priority.')
    running_kernel: StrictStr | None = Field(None, alias="RunningKernel", description="Kernel release, only for package 'proxmox-ve'.")
    section: StrictStr | None = Field(None, alias="Section", description='Package section.')
    title: StrictStr | None = Field(None, alias="Title", description='Package title.')
    version: StrictStr | None = Field(None, alias="Version", description='New version to be updated to.')

class GetNodesNodeAptVersionsResponse(RootModel[list[GetNodesNodeAptVersionsResponseItem]]):
    """List of items. versions. Get package information for important Proxmox packages. response."""
    root: list[GetNodesNodeAptVersionsResponseItem] = Field(...)

class GetNodesNodeCapabilitiesResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Node capabilities index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCapabilitiesQemuResponse(RootModel[list[dict[str, object]]]):
    """Model for qemu_caps_index. QEMU capabilities index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCapabilitiesQemuCpuResponseItem(ProxmoxBaseModel):
    """Model for index. List all custom and default CPU models. response."""
    abstract: bool | None = Field(None, description="True for PVE-internal abstract profiles like x86-64-v2, -v3, -v4. These do not correspond to a QEMU CPU type and cannot be used as a custom model's 'reported-model'.")
    custom: bool | None = Field(None, description='True if this is a custom CPU model.')
    name: StrictStr | None = Field(None, description="Name of the CPU model. Identifies it for subsequent API calls. Prefixed with 'custom-' for custom models.")
    vendor: StrictStr | None = Field(None, description="CPU vendor visible to the guest when this model is selected. Vendor of 'reported-model' in case of custom models.")

class GetNodesNodeCapabilitiesQemuCpuResponse(RootModel[list[GetNodesNodeCapabilitiesQemuCpuResponseItem]]):
    """List of items. index. List all custom and default CPU models. response."""
    root: list[GetNodesNodeCapabilitiesQemuCpuResponseItem] = Field(...)

class GetNodesNodeCapabilitiesQemuCpuFlagsResponseItem(ProxmoxBaseModel):
    """Model for index. List of available VM-specific CPU flags. Returns an empty list for 'aarch64' as no VM-specific flags are defined for it yet. response."""
    description: StrictStr | None = Field(None, description='Description of the CPU flag.')
    name: StrictStr | None = Field(None, description='Name of the CPU flag.')
    supported_on: list[StrictStr] | None = Field(None, alias="supported-on", description='List of nodes supporting the CPU flag with the selected acceleration type ("accel").')

class GetNodesNodeCapabilitiesQemuCpuFlagsResponse(RootModel[list[GetNodesNodeCapabilitiesQemuCpuFlagsResponseItem]]):
    """List of items. index. List of available VM-specific CPU flags. Returns an empty list for 'aarch64' as no VM-specific flags are defined for it yet. response."""
    root: list[GetNodesNodeCapabilitiesQemuCpuFlagsResponseItem] = Field(...)

class GetNodesNodeCapabilitiesQemuMachinesResponseItem(ProxmoxBaseModel):
    """Model for types. Get available QEMU/KVM machine types. response."""
    changes: StrictStr | None = Field(None, description='Notable changes of a version, currently only set for +pveX versions.')
    id: StrictStr | None = Field(None, description='Full name of machine type and version.')
    type: StrictStr | None = Field(None, description='The machine type.')
    version: StrictStr | None = Field(None, description='The machine version.')

class GetNodesNodeCapabilitiesQemuMachinesResponse(RootModel[list[GetNodesNodeCapabilitiesQemuMachinesResponseItem]]):
    """List of items. types. Get available QEMU/KVM machine types. response."""
    root: list[GetNodesNodeCapabilitiesQemuMachinesResponseItem] = Field(...)

class GetNodesNodeCapabilitiesQemuMigrationResponse(ProxmoxBaseModel):
    """Model for capabilities. Get node-specific QEMU migration capabilities of the node. Requires the 'Sys.Audit' permission on '/nodes/<node>'. response."""
    has_dbus_vmstate: bool = Field(..., alias="has-dbus-vmstate", description='Whether the host supports live-migrating additional VM state via the dbus-vmstate helper.')

class GetNodesNodeCephResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCephCfgResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCephCfgDbResponseItem(ProxmoxBaseModel):
    """Model for db. Get the Ceph configuration database. response."""
    can_update_at_runtime: bool | None = Field(None, description='Set if the value can be changed at runtime without restarting the affected daemons. Emitted as the integer 1/0 to match the existing PVE wire convention.')
    level: StrictStr | None = Field(None, description="Config level the entry is exposed at: 'basic' for operator-visible settings, 'advanced' for tuning parameters, 'dev' for developer-only knobs.")
    mask: StrictStr | None = Field(None, description="Match expression restricting the entry's scope; empty when the entry has no mask. Examples: 'host:foo', 'class:ssd'.")
    name: StrictStr | None = Field(None, description='Config key name.')
    section: StrictStr | None = Field(None, description="Ceph config section the entry applies to: 'global', a daemon type ('mon', 'osd', 'mgr', 'mds', 'client'), or a specific daemon (e.g. 'osd.0', 'mon.<name>').")
    value: StrictStr | None = Field(None, description="Configured value for the key (always serialised as a string by Ceph, regardless of the option's underlying type).")

class GetNodesNodeCephCfgDbResponse(RootModel[list[GetNodesNodeCephCfgDbResponseItem]]):
    """List of items. db. Get the Ceph configuration database. response."""
    root: list[GetNodesNodeCephCfgDbResponseItem] = Field(...)

class GetNodesNodeCephCfgRawResponse(RootModel[StrictStr]):
    """Model for raw. Get the Ceph configuration file. response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephCfgValueResponse(RootModel[dict[str, object]]):
    """Model for value. Get configured values from either ceph.conf or the mon config DB. Underscores in section and key names are normalised to hyphens in the response, regardless of how they're written in the source. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeCephCmdSafetyResponse(ProxmoxBaseModel):
    """Model for cmd_safety. Heuristical check if it is safe to perform an action. response."""
    safe: bool = Field(..., description='True if Ceph reports the requested action is safe.')
    status: StrictStr | None = Field(None, description='Human-readable status message from Ceph (typically the reason an action is not safe); absent when Ceph returned no message.')

class GetNodesNodeCephCrushResponse(RootModel[StrictStr]):
    """Model for crush. Get OSD crush map response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephFsResponseItem(ProxmoxBaseModel):
    """Model for index. Directory index. response."""
    data_pool: StrictStr | None = Field(None, description="Name of the filesystem's first data pool. A CephFS can have more than one data pool; consumers interested in the full set should read 'data_pools' instead. Kept for backwards compatibility.")
    data_pool_ids: list[int] | None = Field(None, description='Numeric ids of the data pools.')
    data_pools: list[StrictStr] | None = Field(None, description='Names of all data pools assigned to the filesystem; a CephFS can have multiple data pools (e.g. replicated metadata plus EC data, or multiple device-class-specific data pools).')
    metadata_pool: StrictStr | None = Field(None, description='Name of the metadata pool.')
    metadata_pool_id: int | None = Field(None, description='Numeric id of the metadata pool.')
    name: StrictStr | None = Field(None, description='The ceph filesystem name.')

class GetNodesNodeCephFsResponse(RootModel[list[GetNodesNodeCephFsResponseItem]]):
    """List of items. index. Directory index. response."""
    root: list[GetNodesNodeCephFsResponseItem] = Field(...)

class DeleteNodesNodeCephFsNameRequest(ProxmoxBaseModel):
    """Model for destroyfs. Destroy a Ceph filesystem. Refuses if any PVE storage entry of type 'cephfs' still references the filesystem and is not disabled. Optionally also removes the storage entries and/or the underlying metadata and data pools. request."""
    remove_pools: bool | None = Field(None, alias="remove-pools", description='Remove the metadata and data pools used by this filesystem.')
    remove_storages: bool | None = Field(None, alias="remove-storages", description='Remove pveceph-managed storages configured for this filesystem.')

class DeleteNodesNodeCephFsNameResponse(RootModel[StrictStr]):
    """Model for destroyfs. Destroy a Ceph filesystem. Refuses if any PVE storage entry of type 'cephfs' still references the filesystem and is not disabled. Optionally also removes the storage entries and/or the underlying metadata and data pools. response."""
    root: StrictStr = Field(...)

class PostNodesNodeCephFsNameRequest(ProxmoxBaseModel):
    """Model for createfs. Create a Ceph filesystem request."""
    add_storage: bool | None = Field(None, alias="add-storage", description='Configure the created CephFS as storage for this cluster.')
    pg_num: int | None = Field(None, description='Number of placement groups for the backing data pool. The metadata pool will use a quarter of this.')

class PostNodesNodeCephFsNameResponse(RootModel[StrictStr]):
    """Model for createfs. Create a Ceph filesystem response."""
    root: StrictStr = Field(...)

class PostNodesNodeCephInitRequest(ProxmoxBaseModel):
    """Model for init. Create the initial Ceph default configuration and set up symlinks. Idempotent on re-call: if a [global] section already exists in ceph.conf, the existing fsid / auth / pool defaults are preserved and most parameters are silently ignored. request."""
    cluster_network: StrictStr | None = Field(None, alias="cluster-network", description='Declare a separate cluster network, OSDs will route heartbeat, object replication and recovery traffic over it')
    disable_cephx: bool | None = Field(None, description='Disable cephx authentication.\n\nWARNING: cephx is a security feature protecting against man-in-the-middle attacks. Only consider disabling cephx if your network is private!')
    min_size: int | None = Field(None, description='Minimum number of available replicas per object to allow I/O')
    network: StrictStr | None = Field(None, description='Use specific network for all ceph related traffic')
    pg_bits: int | None = Field(None, description='Placement group bits, used to specify the default number of placement groups.\n\nDepreacted. This setting was deprecated in recent Ceph versions.')
    size: int | None = Field(None, description='Targeted number of replicas per object')

class PostNodesNodeCephInitResponse(RootModel[None]):
    """Model for init. Create the initial Ceph default configuration and set up symlinks. Idempotent on re-call: if a [global] section already exists in ceph.conf, the existing fsid / auth / pool defaults are preserved and most parameters are silently ignored. response."""
    root: None = Field(...)

class GetNodesNodeCephLogResponseItem(ProxmoxBaseModel):
    """Model for log. Read ceph log response."""
    n: int | None = Field(None, description='Log-file line number (1-based).')
    t: StrictStr | None = Field(None, description='Log line text.')

class GetNodesNodeCephLogResponse(RootModel[list[GetNodesNodeCephLogResponseItem]]):
    """List of items. log. Read ceph log response."""
    root: list[GetNodesNodeCephLogResponseItem] = Field(...)

class GetNodesNodeCephMdsResponseItem(ProxmoxBaseModel):
    """Model for index. MDS directory index. response."""
    addr: StrictStr | None = Field(None, description="Address as advertised by the MDS; Ceph-formatted (typically 'IP:PORT/NONCE').")
    ceph_version: StrictStr | None = Field(None, description='Full Ceph version string of the MDS daemon.')
    ceph_version_short: StrictStr | None = Field(None, description="Short Ceph version string of the MDS daemon (e.g. '19.2.0').")
    direxists: bool | None = Field(None, description="Set when the MDS's data directory exists on this node.")
    fs_name: StrictStr | None = Field(None, description='Name of the CephFS this MDS is bound to; absent or null for standby MDSes not currently serving a rank.')
    host: StrictStr | None = Field(None, description='Host the MDS runs on.')
    name: StrictStr | None = Field(None, description='The name (ID) for the MDS.')
    rank: int | None = Field(None, description='MDS rank within the file system; -1 for standby MDSes not currently bound to a rank.')
    service: bool | None = Field(None, description='Set if a ceph-mds@<id> systemd unit is enabled on the hosting node; absent otherwise.')
    standby_replay: bool | None = Field(None, description='If true, the standby MDS is polling the active MDS for faster recovery (hot standby).')
    state: StrictStr | None = Field(None, description="MDS state: Ceph-reported run state (e.g. 'up:active', 'up:standby', 'up:standby-replay') for daemons known to the cluster; 'stopped' or 'unknown' for configured daemons not visible to the cluster.")

class GetNodesNodeCephMdsResponse(RootModel[list[GetNodesNodeCephMdsResponseItem]]):
    """List of items. index. MDS directory index. response."""
    root: list[GetNodesNodeCephMdsResponseItem] = Field(...)

class DeleteNodesNodeCephMdsNameResponse(RootModel[StrictStr]):
    """Model for destroymds. Destroy Ceph Metadata Server response."""
    root: StrictStr = Field(...)

class PostNodesNodeCephMdsNameRequest(ProxmoxBaseModel):
    """Model for createmds. Create Ceph Metadata Server (MDS) request."""
    hotstandby: bool | None = Field(None, description='Determines whether a ceph-mds daemon should poll and replay the log of an active MDS. Faster switch on MDS failure, but needs more idle resources.')

class PostNodesNodeCephMdsNameResponse(RootModel[StrictStr]):
    """Model for createmds. Create Ceph Metadata Server (MDS) response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephMgrResponseItem(ProxmoxBaseModel):
    """Model for index. MGR directory index. response."""
    addr: StrictStr | None = Field(None, description="Address as advertised by the manager; Ceph-formatted (typically 'IP:PORT/NONCE').")
    ceph_version: StrictStr | None = Field(None, description='Full Ceph version string of the manager daemon.')
    ceph_version_short: StrictStr | None = Field(None, description="Short Ceph version string of the manager daemon (e.g. '19.2.0').")
    direxists: bool | None = Field(None, description="Set when the manager's data directory exists on this node.")
    host: StrictStr | None = Field(None, description='Host the manager runs on.')
    name: StrictStr | None = Field(None, description='The name (ID) for the MGR.')
    service: bool | None = Field(None, description='Set if a ceph-mgr@<id> systemd unit is enabled on the hosting node; absent otherwise.')
    state: StrictStr | None = Field(None, description="Manager state: 'active' or 'standby' for daemons visible to the mgr cluster, 'stopped' or 'unknown' for configured daemons not currently visible.")

class GetNodesNodeCephMgrResponse(RootModel[list[GetNodesNodeCephMgrResponseItem]]):
    """List of items. index. MGR directory index. response."""
    root: list[GetNodesNodeCephMgrResponseItem] = Field(...)

class DeleteNodesNodeCephMgrIdResponse(RootModel[StrictStr]):
    """Model for destroymgr. Destroy Ceph Manager. response."""
    root: StrictStr = Field(...)

class PostNodesNodeCephMgrIdResponse(RootModel[StrictStr]):
    """Model for createmgr. Create Ceph Manager response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephMonResponseItem(ProxmoxBaseModel):
    """Model for listmon. Get Ceph monitor list. response."""
    addr: StrictStr | None = Field(None, description="Address as advertised by the monitor; Ceph-formatted (typically 'IP:PORT/NONCE', possibly as a messenger-v2 vector depending on Ceph version and ceph.conf shape).")
    ceph_version: StrictStr | None = Field(None, description='Full Ceph version string of the monitor daemon.')
    ceph_version_short: StrictStr | None = Field(None, description="Short Ceph version string of the monitor daemon (e.g. '19.2.0').")
    direxists: bool | None = Field(None, description="Set when the monitor's data directory exists on this node.")
    host: StrictStr | None = Field(None, description='Host the monitor runs on.')
    name: StrictStr | None = Field(None, description='Monitor id (typically the hostname).')
    quorum: bool | None = Field(None, description='Set when the monitor is part of the current quorum.')
    rank: int | None = Field(None, description='Rank of the monitor within the mon map.')
    service: bool | None = Field(None, description='Set if a ceph-mon@<id> systemd unit is enabled on the hosting node; absent otherwise.')
    state: StrictStr | None = Field(None, description="Run state of the monitor: 'running' (in quorum), 'stopped' (systemd unit configured but daemon not visible to the cluster), or 'unknown' (no rados access).")

class GetNodesNodeCephMonResponse(RootModel[list[GetNodesNodeCephMonResponseItem]]):
    """List of items. listmon. Get Ceph monitor list. response."""
    root: list[GetNodesNodeCephMonResponseItem] = Field(...)

class DeleteNodesNodeCephMonMonidResponse(RootModel[StrictStr]):
    """Model for destroymon. Destroy a Ceph Monitor. Refuses to remove the last monitor of the cluster. Does not destroy any Manager on the same node; use /nodes/{node}/ceph/mgr/{id} for that. response."""
    root: StrictStr = Field(...)

class PostNodesNodeCephMonMonidRequest(ProxmoxBaseModel):
    """Model for createmon. Create a Ceph Monitor. Also auto-creates a Manager for the first monitor. request."""
    mon_address: StrictStr | None = Field(None, alias="mon-address", description='Overwrites autodetected monitor IP address(es). Must be in the public network(s) of Ceph.')

class PostNodesNodeCephMonMonidResponse(RootModel[StrictStr]):
    """Model for createmon. Create a Ceph Monitor. Also auto-creates a Manager for the first monitor. response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephOsdResponse(ProxmoxBaseModel):
    """Model for index. Get Ceph osd list/tree. response."""
    flags: StrictStr | None = Field(None, description='Comma-joined list of currently-set OSD flags; absent when no flags are set on the cluster.')
    root: dict[str, object] = Field(..., description="Top-level CRUSH bucket; recursive structure with 'children' lists holding nested buckets and OSD leaves. Per-node properties (status, weight, in, usage, latencies, etc.) vary by node type and are not statically typed here.")

class PostNodesNodeCephOsdRequest(ProxmoxBaseModel):
    """Model for createosd. Create OSD request."""
    crush_device_class: StrictStr | None = Field(None, alias="crush-device-class", description='Set the device class of the OSD in crush.')
    db_dev: StrictStr | None = Field(None, description='Block device name for block.db.')
    db_dev_size: float | None = Field(None, description='Size in GiB for block.db.')
    dev: StrictStr = Field(..., description='Block device name.')
    encrypted: bool | None = Field(None, description='Enables encryption of the OSD.')
    osds_per_device: int | None = Field(None, alias="osds-per-device", description="OSD services per physical device. Only useful for fast NVMe devices to utilize their performance better. Mutually exclusive with 'db_dev' and 'wal_dev'.")
    wal_dev: StrictStr | None = Field(None, description='Block device name for block.wal.')
    wal_dev_size: float | None = Field(None, description='Size in GiB for block.wal.')

class PostNodesNodeCephOsdResponse(RootModel[StrictStr]):
    """Model for createosd. Create OSD response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeCephOsdOsdidRequest(ProxmoxBaseModel):
    """Model for destroyosd. Destroy OSD request."""
    cleanup: bool | None = Field(None, description="If set, also destroy the underlying logical volumes via 'ceph-volume lvm zap --destroy', remove the volume group's physical volume with pvremove, and wipe any journal/block.db/block.wal partitions left over from filestore OSDs. Without this flag the LVs and partitions are left intact for inspection.")

class DeleteNodesNodeCephOsdOsdidResponse(RootModel[StrictStr]):
    """Model for destroyosd. Destroy OSD response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephOsdOsdidResponse(RootModel[list[dict[str, object]]]):
    """Model for osdindex. OSD index. response."""
    root: list[dict[str, object]] = Field(...)

class PostNodesNodeCephOsdOsdidInResponse(RootModel[None]):
    """Model for in. ceph osd in response."""
    root: None = Field(...)

class GetNodesNodeCephOsdOsdidLvInfoResponse(ProxmoxBaseModel):
    """Model for osdvolume. Get OSD volume details response."""
    creation_time: StrictStr = Field(..., description='Creation time as reported by `lvs`.')
    lv_name: StrictStr = Field(..., description='Name of the logical volume (LV).')
    lv_path: StrictStr = Field(..., description='Path to the logical volume (LV).')
    lv_size: int = Field(..., description='Size of the logical volume (LV).')
    lv_uuid: StrictStr = Field(..., description='UUID of the logical volume (LV).')
    vg_name: StrictStr = Field(..., description='Name of the volume group (VG).')

class GetNodesNodeCephOsdOsdidMetadataResponse(ProxmoxBaseModel):
    """Model for osddetails. Get OSD details response."""
    devices: list[dict[str, object]] = Field(..., description='Array containing data about devices')
    osd: dict[str, object] = Field(..., description='General information about the OSD')

class PostNodesNodeCephOsdOsdidOutResponse(RootModel[None]):
    """Model for out. ceph osd out response."""
    root: None = Field(...)

class PostNodesNodeCephOsdOsdidScrubRequest(ProxmoxBaseModel):
    """Model for scrub. Instruct the OSD to scrub. request."""
    deep: bool | None = Field(None, description='If set, instructs a deep scrub instead of a normal one.')

class PostNodesNodeCephOsdOsdidScrubResponse(RootModel[None]):
    """Model for scrub. Instruct the OSD to scrub. response."""
    root: None = Field(...)

class GetNodesNodeCephPoolResponseItem(ProxmoxBaseModel):
    """Model for lspools. List all pools and their settings (which are settable by the POST/PUT endpoints). response."""
    application_metadata: dict[str, object] | None = Field(None, description='Application tags attached to the pool (mapping of application name to its metadata object).')
    autoscale_status: dict[str, object] | None = Field(None, description='Raw pg_autoscaler status object for this pool; shape varies between Ceph releases.')
    bytes_used: int | None = Field(None, description='Bytes currently used in the pool; absent if no usage statistics are reported.')
    crush_rule: int | None = Field(None, description='Numeric id of the CRUSH rule used by this pool.')
    crush_rule_name: StrictStr | None = Field(None, description='Human-readable name of the CRUSH rule used by this pool; absent if the rule id is not in the current CRUSH map.')
    min_size: int | None = Field(None, description='Minimum number of replicas required to accept writes.')
    percent_used: float | None = Field(None, description='Percentage of pool capacity currently used; absent if no usage statistics are reported.')
    pg_autoscale_mode: StrictStr | None = Field(None, description="Placement-group autoscaler mode ('on', 'warn' or 'off').")
    pg_num: int | None = Field(None, description='Current placement-group count.')
    pg_num_final: int | None = Field(None, description='Optimal placement-group count computed by pg_autoscaler.')
    pg_num_min: int | None = Field(None, description='Minimum placement-group count the pg_autoscaler may choose.')
    pool: int | None = Field(None, description='Numeric pool id assigned by Ceph.')
    pool_name: StrictStr | None = Field(None, description='Operator-visible name of the pool.')
    size: int | None = Field(None, description='Replication factor (target number of object replicas).')
    target_size: int | None = Field(None, description='Operator-supplied target size in bytes; hints the pg_autoscaler.')
    target_size_ratio: float | None = Field(None, description='Operator-supplied target ratio of total pool capacity; hints the pg_autoscaler.')
    type: StrictStr | None = Field(None, description="Pool type: 'replicated' for n-way replication, 'erasure' for an erasure-coded pool, 'unknown' for types PVE does not yet map.")

class GetNodesNodeCephPoolResponse(RootModel[list[GetNodesNodeCephPoolResponseItem]]):
    """List of items. lspools. List all pools and their settings (which are settable by the POST/PUT endpoints). response."""
    root: list[GetNodesNodeCephPoolResponseItem] = Field(...)

class PostNodesNodeCephPoolRequest(ProxmoxBaseModel):
    """Model for createpool. Create Ceph pool request."""
    add_storages: bool | None = Field(None, description='Configure VM and CT storage using the new pool. Defaults to false for replicated pools and to true for erasure-coded pools (since EC pools are typically only useful when wired up to storage).')
    application: StrictStr | None = Field(None, description='The application of the pool.')
    crush_rule: StrictStr | None = Field(None, description='The rule to use for mapping object placement in the cluster.')
    erasure_coding: StrictStr | None = Field(None, alias="erasure-coding", description="Create an erasure coded pool for RBD with an accompaning replicated pool for metadata storage. With EC, the common ceph options 'size', 'min_size' and 'crush_rule' parameters will be applied to the metadata pool.")
    min_size: int | None = Field(None, description='Minimum number of replicas per object')
    name: StrictStr = Field(..., description='The name of the pool. It must be unique.')
    pg_autoscale_mode: StrictStr | None = Field(None, description='The automatic PG scaling mode of the pool.')
    pg_num: int | None = Field(None, description='Number of placement groups.')
    pg_num_min: int | None = Field(None, description='Minimal number of placement groups.')
    size: int | None = Field(None, description='Number of replicas per object')
    target_size: StrictStr | None = Field(None, description='The estimated target size of the pool for the PG autoscaler.')
    target_size_ratio: float | None = Field(None, description='The estimated target ratio of the pool for the PG autoscaler.')

class PostNodesNodeCephPoolResponse(RootModel[StrictStr]):
    """Model for createpool. Create Ceph pool response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeCephPoolNameRequest(ProxmoxBaseModel):
    """Model for destroypool. Destroy pool request."""
    force: bool | None = Field(None, description='If true, destroys pool even if in use')
    remove_ecprofile: bool | None = Field(None, description='Remove the erasure code profile. Defaults to true, if applicable.')
    remove_storages: bool | None = Field(None, description='Remove all pveceph-managed storages configured for this pool')

class DeleteNodesNodeCephPoolNameResponse(RootModel[StrictStr]):
    """Model for destroypool. Destroy pool response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephPoolNameResponse(RootModel[list[dict[str, object]]]):
    """Model for poolindex. Pool index. response."""
    root: list[dict[str, object]] = Field(...)

class PutNodesNodeCephPoolNameRequest(ProxmoxBaseModel):
    """Model for setpool. Change POOL settings request."""
    application: StrictStr | None = Field(None, description='The application of the pool.')
    crush_rule: StrictStr | None = Field(None, description='The rule to use for mapping object placement in the cluster.')
    min_size: int | None = Field(None, description='Minimum number of replicas per object')
    pg_autoscale_mode: StrictStr | None = Field(None, description='The automatic PG scaling mode of the pool.')
    pg_num: int | None = Field(None, description='Number of placement groups.')
    pg_num_min: int | None = Field(None, description='Minimal number of placement groups.')
    size: int | None = Field(None, description='Number of replicas per object')
    target_size: StrictStr | None = Field(None, description='The estimated target size of the pool for the PG autoscaler.')
    target_size_ratio: float | None = Field(None, description='The estimated target ratio of the pool for the PG autoscaler.')

class PutNodesNodeCephPoolNameResponse(RootModel[StrictStr]):
    """Model for setpool. Change POOL settings response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephPoolNameStatusResponse(ProxmoxBaseModel):
    """Model for getpool. Show the current pool status. response."""
    application: StrictStr | None = Field(None, description='The application of the pool.')
    application_list: list[StrictStr] | None = Field(None, description='Names of applications currently associated with the pool.')
    autoscale_status: dict[str, object] | None = Field(None, description='Raw pg_autoscaler status object for this pool; shape varies between Ceph releases.')
    crush_rule: StrictStr | None = Field(None, description='The rule to use for mapping object placement in the cluster.')
    fast_read: bool = Field(..., description='Set if the pool uses fast-read for erasure-coded reads.')
    hashpspool: bool = Field(..., description='Set if the pool hashes pool id into its CRUSH placement-seed.')
    id: int = Field(..., description='Numeric pool id assigned by Ceph.')
    min_size: int | None = Field(None, description='Minimum number of replicas per object')
    name: StrictStr = Field(..., description='The name of the pool. It must be unique.')
    nodeep_scrub: bool = Field(..., alias="nodeep-scrub", description='Set if deep-scrubbing is disabled for this pool.')
    nodelete: bool = Field(..., description='Set if pool delete is blocked.')
    nopgchange: bool = Field(..., description='Set if changing the placement-group count is blocked.')
    noscrub: bool = Field(..., description='Set if scrubbing is disabled for this pool.')
    nosizechange: bool = Field(..., description='Set if changing the replication size is blocked.')
    pg_autoscale_mode: StrictStr | None = Field(None, description='The automatic PG scaling mode of the pool.')
    pg_num: int | None = Field(None, description='Number of placement groups.')
    pg_num_min: int | None = Field(None, description='Minimal number of placement groups.')
    pgp_num: int = Field(..., description='Placement-group-for-placement count.')
    size: int | None = Field(None, description='Number of replicas per object')
    statistics: dict[str, object] | None = Field(None, description='Optional pool usage and IO statistics (only present when verbose=1 is requested).')
    target_size: StrictStr | None = Field(None, description='The estimated target size of the pool for the PG autoscaler.')
    target_size_ratio: float | None = Field(None, description='The estimated target ratio of the pool for the PG autoscaler.')
    use_gmt_hitset: bool = Field(..., description='Set if hitsets use GMT timestamps (for cache-tier pools).')
    write_fadvise_dontneed: bool = Field(..., description='Set if the pool sets the FADV_DONTNEED hint on writes.')

class PostNodesNodeCephRestartRequest(ProxmoxBaseModel):
    """Model for restart. Restart ceph services. request."""
    service: StrictStr | None = Field(None, description='Ceph service name.')

class PostNodesNodeCephRestartResponse(RootModel[StrictStr]):
    """Model for restart. Restart ceph services. response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephRulesResponseItem(ProxmoxBaseModel):
    """Model for rules. List ceph rules. response."""
    name: StrictStr | None = Field(None, description='Name of the CRUSH rule.')

class GetNodesNodeCephRulesResponse(RootModel[list[GetNodesNodeCephRulesResponseItem]]):
    """List of items. rules. List ceph rules. response."""
    root: list[GetNodesNodeCephRulesResponseItem] = Field(...)

class PostNodesNodeCephStartRequest(ProxmoxBaseModel):
    """Model for start. Start ceph services. request."""
    service: StrictStr | None = Field(None, description='Ceph service name.')

class PostNodesNodeCephStartResponse(RootModel[StrictStr]):
    """Model for start. Start ceph services. response."""
    root: StrictStr = Field(...)

class GetNodesNodeCephStatusResponse(RootModel[dict[str, object]]):
    """Model for status. Get the Ceph cluster status (raw 'ceph status' output). The response is cluster-wide and identical to /cluster/ceph/status; this node-level alias exists for operator convenience. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeCephStopRequest(ProxmoxBaseModel):
    """Model for stop. Stop ceph services. request."""
    service: StrictStr | None = Field(None, description='Ceph service name.')

class PostNodesNodeCephStopResponse(RootModel[StrictStr]):
    """Model for stop. Stop ceph services. response."""
    root: StrictStr = Field(...)

class GetNodesNodeCertificatesResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Node index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeCertificatesAcmeResponse(RootModel[list[dict[str, object]]]):
    """Model for index. ACME index. response."""
    root: list[dict[str, object]] = Field(...)

class DeleteNodesNodeCertificatesAcmeCertificateResponse(RootModel[StrictStr]):
    """Model for revoke_certificate. Revoke existing certificate from CA. response."""
    root: StrictStr = Field(...)

class PostNodesNodeCertificatesAcmeCertificateRequest(ProxmoxBaseModel):
    """Model for new_certificate. Order a new certificate from ACME-compatible CA. request."""
    force: bool | None = Field(None, description='Overwrite existing custom certificate.')

class PostNodesNodeCertificatesAcmeCertificateResponse(RootModel[StrictStr]):
    """Model for new_certificate. Order a new certificate from ACME-compatible CA. response."""
    root: StrictStr = Field(...)

class PutNodesNodeCertificatesAcmeCertificateRequest(ProxmoxBaseModel):
    """Model for renew_certificate. Renew existing certificate from CA. request."""
    force: bool | None = Field(None, description='Force renewal even if expiry is more than 30 days away.')

class PutNodesNodeCertificatesAcmeCertificateResponse(RootModel[StrictStr]):
    """Model for renew_certificate. Renew existing certificate from CA. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeCertificatesCustomRequest(ProxmoxBaseModel):
    """Model for remove_custom_cert. DELETE custom certificate chain and key. request."""
    restart: bool | None = Field(None, description='Restart pveproxy.')

class DeleteNodesNodeCertificatesCustomResponse(RootModel[None]):
    """Model for remove_custom_cert. DELETE custom certificate chain and key. response."""
    root: None = Field(...)

class PostNodesNodeCertificatesCustomRequest(ProxmoxBaseModel):
    """Model for upload_custom_cert. Upload or update custom certificate chain and key. request."""
    certificates: StrictStr = Field(..., description='PEM encoded certificate (chain).')
    force: bool | None = Field(None, description='Overwrite existing custom or ACME certificate files.')
    key: StrictStr | None = Field(None, description='PEM encoded private key.')
    restart: bool | None = Field(None, description='Restart pveproxy.')

class PostNodesNodeCertificatesCustomResponse(ProxmoxBaseModel):
    """Model for upload_custom_cert. Upload or update custom certificate chain and key. response."""
    filename: StrictStr | None = Field(None)
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    issuer: StrictStr | None = Field(None, description='Certificate issuer name.')
    notafter: int | None = Field(None, description="Certificate's notAfter timestamp (UNIX epoch).")
    notbefore: int | None = Field(None, description="Certificate's notBefore timestamp (UNIX epoch).")
    pem: StrictStr | None = Field(None, description='Certificate in PEM format')
    public_key_bits: int | None = Field(None, alias="public-key-bits", description="Certificate's public key size")
    public_key_type: StrictStr | None = Field(None, alias="public-key-type", description="Certificate's public key algorithm")
    san: list[StrictStr] | None = Field(None, description="List of Certificate's SubjectAlternativeName entries.")
    subject: StrictStr | None = Field(None, description='Certificate subject name.')

class GetNodesNodeCertificatesInfoResponseItem(ProxmoxBaseModel):
    """Model for info. Get information about node's certificates. response."""
    filename: StrictStr | None = Field(None)
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    issuer: StrictStr | None = Field(None, description='Certificate issuer name.')
    notafter: int | None = Field(None, description="Certificate's notAfter timestamp (UNIX epoch).")
    notbefore: int | None = Field(None, description="Certificate's notBefore timestamp (UNIX epoch).")
    pem: StrictStr | None = Field(None, description='Certificate in PEM format')
    public_key_bits: int | None = Field(None, alias="public-key-bits", description="Certificate's public key size")
    public_key_type: StrictStr | None = Field(None, alias="public-key-type", description="Certificate's public key algorithm")
    san: list[StrictStr] | None = Field(None, description="List of Certificate's SubjectAlternativeName entries.")
    subject: StrictStr | None = Field(None, description='Certificate subject name.')

class GetNodesNodeCertificatesInfoResponse(RootModel[list[GetNodesNodeCertificatesInfoResponseItem]]):
    """List of items. info. Get information about node's certificates. response."""
    root: list[GetNodesNodeCertificatesInfoResponseItem] = Field(...)

class GetNodesNodeConfigResponse(ProxmoxBaseModel):
    """Model for get_config. Get node configuration options. response."""
    acme: StrictStr | None = Field(None, description='Node specific ACME settings.')
    acmedomain_n: StrictStr | None = Field(None, alias="acmedomain[n]", description='ACME domain and validation plugin')
    ballooning_target: int | None = Field(None, alias="ballooning-target", description='RAM usage target for ballooning (in percent of total memory)')
    description: StrictStr | None = Field(None, description='Description for the Node. Shown in the web-interface node notes panel. This is saved as comment inside the configuration file.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    location: StrictStr | None = Field(None, description='The location of the node. Overrides the default from the datacenter config.')
    startall_onboot_delay: int | None = Field(None, alias="startall-onboot-delay", description='Initial delay in seconds, before starting all the Virtual Guests with on-boot enabled.')
    wakeonlan: StrictStr | None = Field(None, description='Node specific wake on LAN settings.')

class PutNodesNodeConfigRequest(ProxmoxBaseModel):
    """Model for set_options. Set node configuration options. request."""
    acme: StrictStr | None = Field(None, description='Node specific ACME settings.')
    acmedomain_n: StrictStr | None = Field(None, alias="acmedomain[n]", description='ACME domain and validation plugin')
    ballooning_target: int | None = Field(None, alias="ballooning-target", description='RAM usage target for ballooning (in percent of total memory)')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description='Description for the Node. Shown in the web-interface node notes panel. This is saved as comment inside the configuration file.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    location: StrictStr | None = Field(None, description='The location of the node. Overrides the default from the datacenter config.')
    startall_onboot_delay: int | None = Field(None, alias="startall-onboot-delay", description='Initial delay in seconds, before starting all the Virtual Guests with on-boot enabled.')
    wakeonlan: StrictStr | None = Field(None, description='Node specific wake on LAN settings.')

class PutNodesNodeConfigResponse(RootModel[None]):
    """Model for set_options. Set node configuration options. response."""
    root: None = Field(...)

class GetNodesNodeDisksResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Node index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeDisksDirectoryResponseItem(ProxmoxBaseModel):
    """Model for index. PVE Managed Directory storages. response."""
    device: StrictStr | None = Field(None, description='The mounted device.')
    options: StrictStr | None = Field(None, description='The mount options.')
    path: StrictStr | None = Field(None, description='The mount path.')
    type: StrictStr | None = Field(None, description='The filesystem type.')
    unitfile: StrictStr | None = Field(None, description='The path of the mount unit.')

class GetNodesNodeDisksDirectoryResponse(RootModel[list[GetNodesNodeDisksDirectoryResponseItem]]):
    """List of items. index. PVE Managed Directory storages. response."""
    root: list[GetNodesNodeDisksDirectoryResponseItem] = Field(...)

class PostNodesNodeDisksDirectoryRequest(ProxmoxBaseModel):
    """Model for create. Create a Filesystem on an unused disk. Will be mounted under '/mnt/pve/NAME'. request."""
    add_storage: bool | None = Field(None, description='Configure storage using the directory.')
    device: StrictStr = Field(..., description='The block device you want to create the filesystem on.')
    filesystem: StrictStr | None = Field(None, description='The desired filesystem.')
    name: StrictStr = Field(..., description='The storage identifier.')

class PostNodesNodeDisksDirectoryResponse(RootModel[StrictStr]):
    """Model for create. Create a Filesystem on an unused disk. Will be mounted under '/mnt/pve/NAME'. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeDisksDirectoryNameRequest(ProxmoxBaseModel):
    """Model for delete. Unmounts the storage and removes the mount unit. request."""
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disk so it can be repurposed afterwards.')

class DeleteNodesNodeDisksDirectoryNameResponse(RootModel[StrictStr]):
    """Model for delete. Unmounts the storage and removes the mount unit. response."""
    root: StrictStr = Field(...)

class PostNodesNodeDisksInitgptRequest(ProxmoxBaseModel):
    """Model for initgpt. Initialize Disk with GPT request."""
    disk: StrictStr = Field(..., description='Block device name')
    uuid: StrictStr | None = Field(None, description='UUID for the GPT table')

class PostNodesNodeDisksInitgptResponse(RootModel[StrictStr]):
    """Model for initgpt. Initialize Disk with GPT response."""
    root: StrictStr = Field(...)

class GetNodesNodeDisksListResponseItem(ProxmoxBaseModel):
    """Model for list. List local disks. response."""
    devpath: StrictStr | None = Field(None, description='The device path')
    gpt: bool | None = Field(None)
    health: StrictStr | None = Field(None)
    model: StrictStr | None = Field(None)
    mounted: bool | None = Field(None)
    osdid: int | None = Field(None)
    osdid_list: list[int] | None = Field(None, alias="osdid-list")
    parent: StrictStr | None = Field(None, description='For partitions only. The device path of the disk the partition resides on.')
    serial: StrictStr | None = Field(None)
    size: int | None = Field(None)
    used: StrictStr | None = Field(None)
    vendor: StrictStr | None = Field(None)
    wwn: StrictStr | None = Field(None)

class GetNodesNodeDisksListResponse(RootModel[list[GetNodesNodeDisksListResponseItem]]):
    """List of items. list. List local disks. response."""
    root: list[GetNodesNodeDisksListResponseItem] = Field(...)

class GetNodesNodeDisksLvmResponse(ProxmoxBaseModel):
    """Model for index. List LVM Volume Groups response."""
    children: list[dict[str, object]] = Field(...)
    leaf: bool = Field(...)

class PostNodesNodeDisksLvmRequest(ProxmoxBaseModel):
    """Model for create. Create an LVM Volume Group request."""
    add_storage: bool | None = Field(None, description='Configure storage using the Volume Group')
    device: StrictStr = Field(..., description='The block device you want to create the volume group on')
    name: StrictStr = Field(..., description='The storage identifier.')

class PostNodesNodeDisksLvmResponse(RootModel[StrictStr]):
    """Model for create. Create an LVM Volume Group response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeDisksLvmNameRequest(ProxmoxBaseModel):
    """Model for delete. Remove an LVM Volume Group. request."""
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disks so they can be repurposed afterwards.')

class DeleteNodesNodeDisksLvmNameResponse(RootModel[StrictStr]):
    """Model for delete. Remove an LVM Volume Group. response."""
    root: StrictStr = Field(...)

class GetNodesNodeDisksLvmthinResponseItem(ProxmoxBaseModel):
    """Model for index. List LVM thinpools response."""
    lv: StrictStr | None = Field(None, description='The name of the thinpool.')
    lv_size: int | None = Field(None, description='The size of the thinpool in bytes.')
    metadata_size: int | None = Field(None, description='The size of the metadata lv in bytes.')
    metadata_used: int | None = Field(None, description='The used bytes of the metadata lv.')
    used: int | None = Field(None, description='The used bytes of the thinpool.')
    vg: StrictStr | None = Field(None, description='The associated volume group.')

class GetNodesNodeDisksLvmthinResponse(RootModel[list[GetNodesNodeDisksLvmthinResponseItem]]):
    """List of items. index. List LVM thinpools response."""
    root: list[GetNodesNodeDisksLvmthinResponseItem] = Field(...)

class PostNodesNodeDisksLvmthinRequest(ProxmoxBaseModel):
    """Model for create. Create an LVM thinpool request."""
    add_storage: bool | None = Field(None, description='Configure storage using the thinpool.')
    device: StrictStr = Field(..., description='The block device you want to create the thinpool on.')
    name: StrictStr = Field(..., description='The storage identifier.')

class PostNodesNodeDisksLvmthinResponse(RootModel[StrictStr]):
    """Model for create. Create an LVM thinpool response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeDisksLvmthinNameRequest(ProxmoxBaseModel):
    """Model for delete. Remove an LVM thin pool. request."""
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disks so they can be repurposed afterwards.')
    volume_group: StrictStr = Field(..., alias="volume-group", description='The storage identifier.')

class DeleteNodesNodeDisksLvmthinNameResponse(RootModel[StrictStr]):
    """Model for delete. Remove an LVM thin pool. response."""
    root: StrictStr = Field(...)

class GetNodesNodeDisksSmartResponse(ProxmoxBaseModel):
    """Model for smart. Get SMART Health of a disk. response."""
    attributes: list[object] | None = Field(None)
    health: StrictStr = Field(...)
    text: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)

class PutNodesNodeDisksWipediskRequest(ProxmoxBaseModel):
    """Model for wipe_disk. Wipe a disk or partition. request."""
    disk: StrictStr = Field(..., description='Block device name')

class PutNodesNodeDisksWipediskResponse(RootModel[StrictStr]):
    """Model for wipe_disk. Wipe a disk or partition. response."""
    root: StrictStr = Field(...)

class GetNodesNodeDisksZfsResponseItem(ProxmoxBaseModel):
    """Model for index. List Zpools. response."""
    alloc: int | None = Field(None)
    dedup: float | None = Field(None)
    frag: int | None = Field(None)
    free: int | None = Field(None)
    health: StrictStr | None = Field(None)
    name: StrictStr | None = Field(None)
    size: int | None = Field(None)

class GetNodesNodeDisksZfsResponse(RootModel[list[GetNodesNodeDisksZfsResponseItem]]):
    """List of items. index. List Zpools. response."""
    root: list[GetNodesNodeDisksZfsResponseItem] = Field(...)

class PostNodesNodeDisksZfsRequest(ProxmoxBaseModel):
    """Model for create. Create a ZFS pool. request."""
    add_storage: bool | None = Field(None, description='Configure storage using the zpool.')
    ashift: int | None = Field(None, description='Pool sector size exponent.')
    compression: StrictStr | None = Field(None, description='The compression algorithm to use.')
    devices: StrictStr = Field(..., description='The block devices you want to create the zpool on.')
    draid_config: StrictStr | None = Field(None, alias="draid-config")
    name: StrictStr = Field(..., description='The storage identifier.')
    raidlevel: StrictStr = Field(..., description='The RAID level to use.')

class PostNodesNodeDisksZfsResponse(RootModel[StrictStr]):
    """Model for create. Create a ZFS pool. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeDisksZfsNameRequest(ProxmoxBaseModel):
    """Model for delete. Destroy a ZFS pool. request."""
    cleanup_config: bool | None = Field(None, alias="cleanup-config", description='Marks associated storage(s) as not available on this node anymore or removes them from the configuration (if configured for this node only).')
    cleanup_disks: bool | None = Field(None, alias="cleanup-disks", description='Also wipe disks so they can be repurposed afterwards.')

class DeleteNodesNodeDisksZfsNameResponse(RootModel[StrictStr]):
    """Model for delete. Destroy a ZFS pool. response."""
    root: StrictStr = Field(...)

class GetNodesNodeDisksZfsNameResponse(ProxmoxBaseModel):
    """Model for detail. Get details about a zpool. response."""
    action: StrictStr | None = Field(None, description='Information about the recommended action to fix the state.')
    children: list[dict[str, object]] = Field(..., description='The pool configuration information, including the vdevs for each section (e.g. spares, cache), may be nested.')
    errors: StrictStr = Field(..., description='Information about the errors on the zpool.')
    name: StrictStr = Field(..., description='The name of the zpool.')
    scan: StrictStr | None = Field(None, description='Information about the last/current scrub.')
    state: StrictStr = Field(..., description='The state of the zpool.')
    status: StrictStr | None = Field(None, description='Information about the state of the zpool.')

class GetNodesNodeDnsResponse(ProxmoxBaseModel):
    """Model for dns. Read DNS settings. response."""
    dns1: StrictStr | None = Field(None, description='First name server IP address.')
    dns2: StrictStr | None = Field(None, description='Second name server IP address.')
    dns3: StrictStr | None = Field(None, description='Third name server IP address.')
    search: StrictStr | None = Field(None, description='Search domain for host-name lookup.')

class PutNodesNodeDnsRequest(ProxmoxBaseModel):
    """Model for update_dns. Write DNS settings. request."""
    dns1: StrictStr | None = Field(None, description='First name server IP address.')
    dns2: StrictStr | None = Field(None, description='Second name server IP address.')
    dns3: StrictStr | None = Field(None, description='Third name server IP address.')
    search: StrictStr = Field(..., description='Search domain for host-name lookup.')

class PutNodesNodeDnsResponse(RootModel[None]):
    """Model for update_dns. Write DNS settings. response."""
    root: None = Field(...)

class PostNodesNodeExecuteRequest(ProxmoxBaseModel):
    """Model for execute. Execute multiple commands in order, root only. request."""
    commands: StrictStr = Field(..., description='JSON encoded array of commands.')

class PostNodesNodeExecuteResponse(RootModel[list[dict[str, object]]]):
    """Model for execute. Execute multiple commands in order, root only. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeFirewallResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeFirewallLogResponseItem(ProxmoxBaseModel):
    """Model for log. Read firewall log response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeFirewallLogResponse(RootModel[list[GetNodesNodeFirewallLogResponseItem]]):
    """List of items. log. Read firewall log response."""
    root: list[GetNodesNodeFirewallLogResponseItem] = Field(...)

class GetNodesNodeFirewallOptionsResponse(ProxmoxBaseModel):
    """Model for get_options. Get host firewall options. response."""
    enable: bool | None = Field(None, description='Enable host firewall rules.')
    log_level_forward: StrictStr | None = Field(None, description='Log level for forwarded traffic.')
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    log_nf_conntrack: bool | None = Field(None, description='Enable logging of conntrack information.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    nf_conntrack_allow_invalid: bool | None = Field(None, description='Allow invalid packets on connection tracking.')
    nf_conntrack_helpers: StrictStr | None = Field(None, description='Enable conntrack helpers for specific protocols. Supported protocols: amanda, ftp, irc, netbios-ns, pptp, sane, sip, snmp, tftp')
    nf_conntrack_max: int | None = Field(None, description='Maximum number of tracked connections.')
    nf_conntrack_tcp_timeout_established: int | None = Field(None, description='Conntrack established timeout.')
    nf_conntrack_tcp_timeout_syn_recv: int | None = Field(None, description='Conntrack syn recv timeout.')
    nftables: bool | None = Field(None, description='Enable nftables based firewall (tech preview)')
    nosmurfs: bool | None = Field(None, description='Enable SMURFS filter.')
    protection_synflood: bool | None = Field(None, description='Enable synflood protection')
    protection_synflood_burst: int | None = Field(None, description='Synflood protection rate burst by ip src.')
    protection_synflood_rate: int | None = Field(None, description='Synflood protection rate syn/sec by ip src.')
    smurf_log_level: StrictStr | None = Field(None, description='Log level for SMURFS filter.')
    tcp_flags_log_level: StrictStr | None = Field(None, description='Log level for illegal tcp flags filter.')
    tcpflags: bool | None = Field(None, description='Filter illegal combinations of TCP flags.')

class PutNodesNodeFirewallOptionsRequest(ProxmoxBaseModel):
    """Model for set_options. Set Firewall options. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enable host firewall rules.')
    log_level_forward: StrictStr | None = Field(None, description='Log level for forwarded traffic.')
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    log_nf_conntrack: bool | None = Field(None, description='Enable logging of conntrack information.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    nf_conntrack_allow_invalid: bool | None = Field(None, description='Allow invalid packets on connection tracking.')
    nf_conntrack_helpers: StrictStr | None = Field(None, description='Enable conntrack helpers for specific protocols. Supported protocols: amanda, ftp, irc, netbios-ns, pptp, sane, sip, snmp, tftp')
    nf_conntrack_max: int | None = Field(None, description='Maximum number of tracked connections.')
    nf_conntrack_tcp_timeout_established: int | None = Field(None, description='Conntrack established timeout.')
    nf_conntrack_tcp_timeout_syn_recv: int | None = Field(None, description='Conntrack syn recv timeout.')
    nftables: bool | None = Field(None, description='Enable nftables based firewall (tech preview)')
    nosmurfs: bool | None = Field(None, description='Enable SMURFS filter.')
    protection_synflood: bool | None = Field(None, description='Enable synflood protection')
    protection_synflood_burst: int | None = Field(None, description='Synflood protection rate burst by ip src.')
    protection_synflood_rate: int | None = Field(None, description='Synflood protection rate syn/sec by ip src.')
    smurf_log_level: StrictStr | None = Field(None, description='Log level for SMURFS filter.')
    tcp_flags_log_level: StrictStr | None = Field(None, description='Log level for illegal tcp flags filter.')
    tcpflags: bool | None = Field(None, description='Filter illegal combinations of TCP flags.')

class PutNodesNodeFirewallOptionsResponse(RootModel[None]):
    """Model for set_options. Set Firewall options. response."""
    root: None = Field(...)

class GetNodesNodeFirewallRulesResponseItem(ProxmoxBaseModel):
    """Model for get_rules. List rules. response."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr | None = Field(None, description='Rule type')

class GetNodesNodeFirewallRulesResponse(RootModel[list[GetNodesNodeFirewallRulesResponseItem]]):
    """List of items. get_rules. List rules. response."""
    root: list[GetNodesNodeFirewallRulesResponseItem] = Field(...)

class PostNodesNodeFirewallRulesRequest(ProxmoxBaseModel):
    """Model for create_rule. Create new rule. request."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr = Field(..., description='Rule type.')

class PostNodesNodeFirewallRulesResponse(RootModel[None]):
    """Model for create_rule. Create new rule. response."""
    root: None = Field(...)

class DeleteNodesNodeFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for delete_rule. Delete rule. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeFirewallRulesPosResponse(RootModel[None]):
    """Model for delete_rule. Delete rule. response."""
    root: None = Field(...)

class GetNodesNodeFirewallRulesPosResponse(ProxmoxBaseModel):
    """Model for get_rule. Get single rule data. response."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr = Field(..., description='Rule type')

class PutNodesNodeFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for update_rule. Modify rule data. request."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr | None = Field(None, description='Rule type.')

class PutNodesNodeFirewallRulesPosResponse(RootModel[None]):
    """Model for update_rule. Modify rule data. response."""
    root: None = Field(...)

class GetNodesNodeHardwareResponseItem(ProxmoxBaseModel):
    """Model for index. Index of hardware types response."""
    type: StrictStr | None = Field(None)

class GetNodesNodeHardwareResponse(RootModel[list[GetNodesNodeHardwareResponseItem]]):
    """List of items. index. Index of hardware types response."""
    root: list[GetNodesNodeHardwareResponseItem] = Field(...)

class GetNodesNodeHardwarePciResponseItem(ProxmoxBaseModel):
    """Model for pci_scan. List local PCI devices. response."""
    class_: StrictStr | None = Field(None, alias="class", description='The PCI Class of the device.')
    device: StrictStr | None = Field(None, description='The Device ID.')
    device_name: StrictStr | None = Field(None)
    id: StrictStr | None = Field(None, description='The PCI ID.')
    iommugroup: int | None = Field(None, description='The IOMMU group in which the device is in. If no IOMMU group is detected, it is set to -1.')
    mdev: bool | None = Field(None, description='If set, marks that the device is capable of creating mediated devices.')
    subsystem_device: StrictStr | None = Field(None, description='The Subsystem Device ID.')
    subsystem_device_name: StrictStr | None = Field(None)
    subsystem_vendor: StrictStr | None = Field(None, description='The Subsystem Vendor ID.')
    subsystem_vendor_name: StrictStr | None = Field(None)
    vendor: StrictStr | None = Field(None, description='The Vendor ID.')
    vendor_name: StrictStr | None = Field(None)

class GetNodesNodeHardwarePciResponse(RootModel[list[GetNodesNodeHardwarePciResponseItem]]):
    """List of items. pci_scan. List local PCI devices. response."""
    root: list[GetNodesNodeHardwarePciResponseItem] = Field(...)

class GetNodesNodeHardwarePciPciIdOrMappingResponseItem(ProxmoxBaseModel):
    """Model for pci_index. Index of available pci methods response."""
    method: StrictStr | None = Field(None)

class GetNodesNodeHardwarePciPciIdOrMappingResponse(RootModel[list[GetNodesNodeHardwarePciPciIdOrMappingResponseItem]]):
    """List of items. pci_index. Index of available pci methods response."""
    root: list[GetNodesNodeHardwarePciPciIdOrMappingResponseItem] = Field(...)

class GetNodesNodeHardwarePciPciIdOrMappingMdevResponseItem(ProxmoxBaseModel):
    """Model for mdevscan. List mediated device types for given PCI device. response."""
    available: int | None = Field(None, description='The number of still available instances of this type.')
    description: StrictStr | None = Field(None, description='Additional description of the type.')
    name: StrictStr | None = Field(None, description='A human readable name for the type.')
    type: StrictStr | None = Field(None, description='The name of the mdev type.')

class GetNodesNodeHardwarePciPciIdOrMappingMdevResponse(RootModel[list[GetNodesNodeHardwarePciPciIdOrMappingMdevResponseItem]]):
    """List of items. mdevscan. List mediated device types for given PCI device. response."""
    root: list[GetNodesNodeHardwarePciPciIdOrMappingMdevResponseItem] = Field(...)

class GetNodesNodeHardwareUsbResponseItem(ProxmoxBaseModel):
    """Model for usbscan. List local USB devices. response."""
    busnum: int | None = Field(None)
    class_: int | None = Field(None, alias="class")
    devnum: int | None = Field(None)
    level: int | None = Field(None)
    manufacturer: StrictStr | None = Field(None)
    port: int | None = Field(None)
    prodid: StrictStr | None = Field(None)
    product: StrictStr | None = Field(None)
    serial: StrictStr | None = Field(None)
    speed: StrictStr | None = Field(None)
    usbpath: StrictStr | None = Field(None)
    vendid: StrictStr | None = Field(None)

class GetNodesNodeHardwareUsbResponse(RootModel[list[GetNodesNodeHardwareUsbResponseItem]]):
    """List of items. usbscan. List local USB devices. response."""
    root: list[GetNodesNodeHardwareUsbResponseItem] = Field(...)

class GetNodesNodeHostsResponse(ProxmoxBaseModel):
    """Model for get_etc_hosts. Get the content of /etc/hosts. response."""
    data: StrictStr = Field(..., description='The content of /etc/hosts.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class PostNodesNodeHostsRequest(ProxmoxBaseModel):
    """Model for write_etc_hosts. Write /etc/hosts. request."""
    data: StrictStr = Field(..., description='The target content of /etc/hosts.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class PostNodesNodeHostsResponse(RootModel[None]):
    """Model for write_etc_hosts. Write /etc/hosts. response."""
    root: None = Field(...)

class GetNodesNodeJournalResponse(RootModel[list[StrictStr]]):
    """Model for journal. Read Journal response."""
    root: list[StrictStr] = Field(...)

class GetNodesNodeLxcResponseItem(ProxmoxBaseModel):
    """Model for vmlist. LXC container index (per node). response."""
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    disk: int | None = Field(None, description='Root disk image space-usage in bytes.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    lock: StrictStr | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk image size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    maxswap: int | None = Field(None, description='Maximum SWAP memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes.')
    name: StrictStr | None = Field(None, description='Container name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    status: StrictStr | None = Field(None, description='LXC Container status.')
    tags: StrictStr | None = Field(None, description='The current configured tags, if any.')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int | None = Field(None, description='The (unique) ID of the VM.')

class GetNodesNodeLxcResponse(RootModel[list[GetNodesNodeLxcResponseItem]]):
    """List of items. vmlist. LXC container index (per node). response."""
    root: list[GetNodesNodeLxcResponseItem] = Field(...)

class PostNodesNodeLxcRequest(ProxmoxBaseModel):
    """Model for create_vm. Create or restore a container. request."""
    arch: StrictStr | None = Field(None, description='OS architecture type.')
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    cmode: StrictStr | None = Field(None, description="Console mode. By default, the console command tries to open a connection to one of the available tty devices. By setting cmode to 'console' it tries to attach to /dev/console instead. If you set cmode to 'shell', it simply invokes a shell inside the container (no login).")
    console: bool | None = Field(None, description='Attach a console device (/dev/console) to the container.')
    cores: int | None = Field(None, description='The number of cores assigned to the container. A container can use all available cores by default.')
    cpulimit: float | None = Field(None, description="Limit of CPU usage.\n\nNOTE: If the computer has 2 CPUs, it has a total of '2' CPU time. Value '0' indicates no CPU limit.")
    cpuunits: int | None = Field(None, description='CPU weight for a container, will be clamped to [1, 10000] in cgroup v2.')
    debug: bool | None = Field(None, description='Try to be more verbose. For now this only enables debug log-level on start.')
    description: StrictStr | None = Field(None, description="Description for the Container. Shown in the web-interface CT's summary. This is saved as comment inside the configuration file.")
    dev_n: StrictStr | None = Field(None, alias="dev[n]", description='Device to pass through to the container')
    entrypoint: StrictStr | None = Field(None, description='Command to run as init, optionally with arguments; may start with an absolute path, relative path, or a binary in $PATH.')
    env: StrictStr | None = Field(None, description='The container runtime environment as NUL-separated list. Replaces any lxc.environment.runtime entries in the config.')
    features: StrictStr | None = Field(None, description='Allow containers access to advanced features.')
    force: bool | None = Field(None, description='Allow to overwrite existing container.')
    ha_managed: bool | None = Field(None, alias="ha-managed", description='Add the CT as a HA resource after it was created.')
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the containers lifetime.')
    hostname: StrictStr | None = Field(None, description='Set a host name for the container.')
    ignore_unpack_errors: bool | None = Field(None, alias="ignore-unpack-errors", description='Ignore errors when extracting the template.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the container.')
    memory: int | None = Field(None, description='Amount of RAM for the container in MB.')
    mp_n: StrictStr | None = Field(None, alias="mp[n]", description='Use volume as container mount point. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume.')
    nameserver: StrictStr | None = Field(None, description='Sets DNS server IP address for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specifies network interfaces for the container.')
    onboot: bool | None = Field(None, description='Specifies whether a container will be started during system bootup.')
    ostemplate: StrictStr = Field(..., description='The OS template or backup file.')
    ostype: StrictStr | None = Field(None, description="OS type. This is used to setup configuration inside the container, and corresponds to lxc setup scripts in /usr/share/lxc/config/<ostype>.common.conf. Value 'unmanaged' can be used to skip and OS specific setup.")
    password: StrictStr | None = Field(None, description='Sets root password inside container.')
    pool: StrictStr | None = Field(None, description='Add the VM to the specified pool.')
    protection: bool | None = Field(None, description="Sets the protection flag of the container. This will prevent the CT or CT's disk remove/update operation.")
    restore: bool | None = Field(None, description='Mark this as restore task.')
    rootfs: StrictStr | None = Field(None, description='Use volume as container root.')
    searchdomain: StrictStr | None = Field(None, description='Sets DNS search domains for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    ssh_public_keys: StrictStr | None = Field(None, alias="ssh-public-keys", description='Setup public SSH keys (one key per line, OpenSSH format).')
    start: bool | None = Field(None, description='Start the CT after its creation finished successfully.')
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    storage: StrictStr | None = Field(None, description='Default Storage.')
    swap: int | None = Field(None, description='Amount of SWAP for the container in MB.')
    tags: StrictStr | None = Field(None, description='Tags of the Container. This is only meta information.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    timezone: StrictStr | None = Field(None, description="Time zone to use in the container. If option isn't set, then nothing will be done. Can be set to 'host' to match the host time zone, or an arbitrary time zone option from /usr/share/zoneinfo/zone.tab")
    tty: int | None = Field(None, description='Specify the number of tty available to the container')
    unique: bool | None = Field(None, description='Assign a unique random ethernet address.')
    unprivileged: bool | None = Field(None, description='Makes the container run as unprivileged user. For creation, the default is 1. For restore, the default is the value from the backup. (Should not be modified manually.)')
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    vmid: int = Field(..., description='The (unique) ID of the VM.')

class PostNodesNodeLxcResponse(RootModel[StrictStr]):
    """Model for create_vm. Create or restore a container. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeLxcVmidRequest(ProxmoxBaseModel):
    """Model for destroy_vm. Destroy the container (also delete all uses files). request."""
    destroy_unreferenced_disks: bool | None = Field(None, alias="destroy-unreferenced-disks", description='If set, destroy additionally all disks with the VMID from all enabled storages which are not referenced in the config.')
    force: bool | None = Field(None, description='Force destroy, even if running.')
    purge: bool | None = Field(None, description='Remove container from all related configurations. For example, backup jobs, replication jobs or HA. Related ACLs and Firewall entries will *always* be removed.')

class DeleteNodesNodeLxcVmidResponse(RootModel[StrictStr]):
    """Model for destroy_vm. Destroy the container (also delete all uses files). response."""
    root: StrictStr = Field(...)

class GetNodesNodeLxcVmidResponseItem(ProxmoxBaseModel):
    """Model for vmdiridx. Directory index response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeLxcVmidResponse(RootModel[list[GetNodesNodeLxcVmidResponseItem]]):
    """List of items. vmdiridx. Directory index response."""
    root: list[GetNodesNodeLxcVmidResponseItem] = Field(...)

class PostNodesNodeLxcVmidCloneRequest(ProxmoxBaseModel):
    """Model for clone_vm. Create a container clone/copy request."""
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    description: StrictStr | None = Field(None, description='Description for the new CT.')
    full: bool | None = Field(None, description='Create a full copy of all disks. This is always done when you clone a normal CT. For CT templates, we try to create a linked clone by default.')
    hostname: StrictStr | None = Field(None, description='Set a hostname for the new CT.')
    newid: int = Field(..., description='VMID for the clone.')
    pool: StrictStr | None = Field(None, description='Add the new CT to the specified pool.')
    snapname: StrictStr | None = Field(None, description='The name of the snapshot.')
    storage: StrictStr | None = Field(None, description='Target storage for full clone.')
    target: StrictStr | None = Field(None, description='Target node. Only allowed if the original VM is on shared storage.')

class PostNodesNodeLxcVmidCloneResponse(RootModel[StrictStr]):
    """Model for clone_vm. Create a container clone/copy response."""
    root: StrictStr = Field(...)

class GetNodesNodeLxcVmidConfigResponse(ProxmoxBaseModel):
    """Model for vm_config. Get container configuration. response."""
    arch: StrictStr | None = Field(None, description='OS architecture type.')
    cmode: StrictStr | None = Field(None, description="Console mode. By default, the console command tries to open a connection to one of the available tty devices. By setting cmode to 'console' it tries to attach to /dev/console instead. If you set cmode to 'shell', it simply invokes a shell inside the container (no login).")
    console: bool | None = Field(None, description='Attach a console device (/dev/console) to the container.')
    cores: int | None = Field(None, description='The number of cores assigned to the container. A container can use all available cores by default.')
    cpulimit: float | None = Field(None, description="Limit of CPU usage.\n\nNOTE: If the computer has 2 CPUs, it has a total of '2' CPU time. Value '0' indicates no CPU limit.")
    cpuunits: int | None = Field(None, description='CPU weight for a container, will be clamped to [1, 10000] in cgroup v2.')
    debug: bool | None = Field(None, description='Try to be more verbose. For now this only enables debug log-level on start.')
    description: StrictStr | None = Field(None, description="Description for the Container. Shown in the web-interface CT's summary. This is saved as comment inside the configuration file.")
    dev_n: StrictStr | None = Field(None, alias="dev[n]", description='Device to pass through to the container')
    digest: StrictStr = Field(..., description='SHA1 digest of configuration file. This can be used to prevent concurrent modifications.')
    entrypoint: StrictStr | None = Field(None, description='Command to run as init, optionally with arguments; may start with an absolute path, relative path, or a binary in $PATH.')
    env: StrictStr | None = Field(None, description='The container runtime environment as NUL-separated list. Replaces any lxc.environment.runtime entries in the config.')
    features: StrictStr | None = Field(None, description='Allow containers access to advanced features.')
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the containers lifetime.')
    hostname: StrictStr | None = Field(None, description='Set a host name for the container.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the container.')
    lxc: list[list[StrictStr]] | None = Field(None, description='Array of lxc low-level configurations ([[key1, value1], [key2, value2] ...]).')
    memory: int | None = Field(None, description='Amount of RAM for the container in MB.')
    mp_n: StrictStr | None = Field(None, alias="mp[n]", description='Use volume as container mount point. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume.')
    nameserver: StrictStr | None = Field(None, description='Sets DNS server IP address for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specifies network interfaces for the container.')
    onboot: bool | None = Field(None, description='Specifies whether a container will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description="OS type. This is used to setup configuration inside the container, and corresponds to lxc setup scripts in /usr/share/lxc/config/<ostype>.common.conf. Value 'unmanaged' can be used to skip and OS specific setup.")
    protection: bool | None = Field(None, description="Sets the protection flag of the container. This will prevent the CT or CT's disk remove/update operation.")
    rootfs: StrictStr | None = Field(None, description='Use volume as container root.')
    searchdomain: StrictStr | None = Field(None, description='Sets DNS search domains for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    swap: int | None = Field(None, description='Amount of SWAP for the container in MB.')
    tags: StrictStr | None = Field(None, description='Tags of the Container. This is only meta information.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    timezone: StrictStr | None = Field(None, description="Time zone to use in the container. If option isn't set, then nothing will be done. Can be set to 'host' to match the host time zone, or an arbitrary time zone option from /usr/share/zoneinfo/zone.tab")
    tty: int | None = Field(None, description='Specify the number of tty available to the container')
    unprivileged: bool | None = Field(None, description='Makes the container run as unprivileged user. For creation, the default is 1. For restore, the default is the value from the backup. (Should not be modified manually.)')
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')

class PutNodesNodeLxcVmidConfigRequest(ProxmoxBaseModel):
    """Model for update_vm. Set container options. request."""
    arch: StrictStr | None = Field(None, description='OS architecture type.')
    cmode: StrictStr | None = Field(None, description="Console mode. By default, the console command tries to open a connection to one of the available tty devices. By setting cmode to 'console' it tries to attach to /dev/console instead. If you set cmode to 'shell', it simply invokes a shell inside the container (no login).")
    console: bool | None = Field(None, description='Attach a console device (/dev/console) to the container.')
    cores: int | None = Field(None, description='The number of cores assigned to the container. A container can use all available cores by default.')
    cpulimit: float | None = Field(None, description="Limit of CPU usage.\n\nNOTE: If the computer has 2 CPUs, it has a total of '2' CPU time. Value '0' indicates no CPU limit.")
    cpuunits: int | None = Field(None, description='CPU weight for a container, will be clamped to [1, 10000] in cgroup v2.')
    debug: bool | None = Field(None, description='Try to be more verbose. For now this only enables debug log-level on start.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description="Description for the Container. Shown in the web-interface CT's summary. This is saved as comment inside the configuration file.")
    dev_n: StrictStr | None = Field(None, alias="dev[n]", description='Device to pass through to the container')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    entrypoint: StrictStr | None = Field(None, description='Command to run as init, optionally with arguments; may start with an absolute path, relative path, or a binary in $PATH.')
    env: StrictStr | None = Field(None, description='The container runtime environment as NUL-separated list. Replaces any lxc.environment.runtime entries in the config.')
    features: StrictStr | None = Field(None, description='Allow containers access to advanced features.')
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the containers lifetime.')
    hostname: StrictStr | None = Field(None, description='Set a host name for the container.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the container.')
    memory: int | None = Field(None, description='Amount of RAM for the container in MB.')
    mp_n: StrictStr | None = Field(None, alias="mp[n]", description='Use volume as container mount point. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume.')
    nameserver: StrictStr | None = Field(None, description='Sets DNS server IP address for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specifies network interfaces for the container.')
    onboot: bool | None = Field(None, description='Specifies whether a container will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description="OS type. This is used to setup configuration inside the container, and corresponds to lxc setup scripts in /usr/share/lxc/config/<ostype>.common.conf. Value 'unmanaged' can be used to skip and OS specific setup.")
    protection: bool | None = Field(None, description="Sets the protection flag of the container. This will prevent the CT or CT's disk remove/update operation.")
    revert: StrictStr | None = Field(None, description='Revert a pending change.')
    rootfs: StrictStr | None = Field(None, description='Use volume as container root.')
    searchdomain: StrictStr | None = Field(None, description='Sets DNS search domains for a container. Create will automatically use the setting from the host if you neither set searchdomain nor nameserver.')
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    swap: int | None = Field(None, description='Amount of SWAP for the container in MB.')
    tags: StrictStr | None = Field(None, description='Tags of the Container. This is only meta information.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    timezone: StrictStr | None = Field(None, description="Time zone to use in the container. If option isn't set, then nothing will be done. Can be set to 'host' to match the host time zone, or an arbitrary time zone option from /usr/share/zoneinfo/zone.tab")
    tty: int | None = Field(None, description='Specify the number of tty available to the container')
    unprivileged: bool | None = Field(None, description='Makes the container run as unprivileged user. For creation, the default is 1. For restore, the default is the value from the backup. (Should not be modified manually.)')
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')

class PutNodesNodeLxcVmidConfigResponse(RootModel[None]):
    """Model for update_vm. Set container options. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFeatureResponse(ProxmoxBaseModel):
    """Model for vm_feature. Check if feature for virtual machine is available. response."""
    has_feature: bool = Field(..., alias="hasFeature")

class GetNodesNodeLxcVmidFirewallResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeLxcVmidFirewallAliasesResponseItem(ProxmoxBaseModel):
    """Model for get_aliases. List aliases response."""
    cidr: StrictStr | None = Field(None)
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr | None = Field(None)

class GetNodesNodeLxcVmidFirewallAliasesResponse(RootModel[list[GetNodesNodeLxcVmidFirewallAliasesResponseItem]]):
    """List of items. get_aliases. List aliases response."""
    root: list[GetNodesNodeLxcVmidFirewallAliasesResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallAliasesRequest(ProxmoxBaseModel):
    """Model for create_alias. Create IP or Network Alias. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    name: StrictStr = Field(..., description='Alias name.')

class PostNodesNodeLxcVmidFirewallAliasesResponse(RootModel[None]):
    """Model for create_alias. Create IP or Network Alias. response."""
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    """Model for remove_alias. Remove IP or Network alias. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeLxcVmidFirewallAliasesNameResponse(RootModel[None]):
    """Model for remove_alias. Remove IP or Network alias. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallAliasesNameResponse(RootModel[dict[str, object]]):
    """Model for read_alias. Read alias. response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeLxcVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    """Model for update_alias. Update IP or Network alias. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    rename: StrictStr | None = Field(None, description='Rename an existing alias.')

class PutNodesNodeLxcVmidFirewallAliasesNameResponse(RootModel[None]):
    """Model for update_alias. Update IP or Network alias. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallIpsetResponseItem(ProxmoxBaseModel):
    """Model for ipset_index. List IPSets response."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr | None = Field(None, description='IP set name.')

class GetNodesNodeLxcVmidFirewallIpsetResponse(RootModel[list[GetNodesNodeLxcVmidFirewallIpsetResponseItem]]):
    """List of items. ipset_index. List IPSets response."""
    root: list[GetNodesNodeLxcVmidFirewallIpsetResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallIpsetRequest(ProxmoxBaseModel):
    """Model for create_ipset. Create new IPSet request."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr = Field(..., description='IP set name.')
    rename: StrictStr | None = Field(None, description="Rename an existing IPSet. You can set 'rename' to the same value as 'name' to update the 'comment' of an existing IPSet.")

class PostNodesNodeLxcVmidFirewallIpsetResponse(RootModel[None]):
    """Model for create_ipset. Create new IPSet response."""
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    """Model for delete_ipset. Delete IPSet request."""
    force: bool | None = Field(None, description='Delete all members of the IPSet, if there are any.')

class DeleteNodesNodeLxcVmidFirewallIpsetNameResponse(RootModel[None]):
    """Model for delete_ipset. Delete IPSet response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallIpsetNameResponseItem(ProxmoxBaseModel):
    """Model for get_ipset. List IPSet content response."""
    cidr: StrictStr | None = Field(None)
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class GetNodesNodeLxcVmidFirewallIpsetNameResponse(RootModel[list[GetNodesNodeLxcVmidFirewallIpsetNameResponseItem]]):
    """List of items. get_ipset. List IPSet content response."""
    root: list[GetNodesNodeLxcVmidFirewallIpsetNameResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    """Model for create_ip. Add IP or Network to IPSet. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    nomatch: bool | None = Field(None)

class PostNodesNodeLxcVmidFirewallIpsetNameResponse(RootModel[None]):
    """Model for create_ip. Add IP or Network to IPSet. response."""
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    """Model for remove_ip. Remove IP or Network from IPSet. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeLxcVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    """Model for remove_ip. Remove IP or Network from IPSet. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallIpsetNameCidrResponse(RootModel[dict[str, object]]):
    """Model for read_ip. Read IP or Network settings from IPSet. response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeLxcVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    """Model for update_ip. Update IP or Network settings request."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class PutNodesNodeLxcVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    """Model for update_ip. Update IP or Network settings response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallLogResponseItem(ProxmoxBaseModel):
    """Model for log. Read firewall log response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeLxcVmidFirewallLogResponse(RootModel[list[GetNodesNodeLxcVmidFirewallLogResponseItem]]):
    """List of items. log. Read firewall log response."""
    root: list[GetNodesNodeLxcVmidFirewallLogResponseItem] = Field(...)

class GetNodesNodeLxcVmidFirewallOptionsResponse(ProxmoxBaseModel):
    """Model for get_options. Get VM firewall options. response."""
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: StrictStr | None = Field(None, description='Input policy.')
    policy_out: StrictStr | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeLxcVmidFirewallOptionsRequest(ProxmoxBaseModel):
    """Model for set_options. Set Firewall options. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: StrictStr | None = Field(None, description='Input policy.')
    policy_out: StrictStr | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeLxcVmidFirewallOptionsResponse(RootModel[None]):
    """Model for set_options. Set Firewall options. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallRefsResponseItem(ProxmoxBaseModel):
    """Model for refs. Lists possible IPSet/Alias reference which are allowed in source/dest properties. response."""
    comment: StrictStr | None = Field(None)
    name: StrictStr | None = Field(None)
    ref: StrictStr | None = Field(None)
    scope: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)

class GetNodesNodeLxcVmidFirewallRefsResponse(RootModel[list[GetNodesNodeLxcVmidFirewallRefsResponseItem]]):
    """List of items. refs. Lists possible IPSet/Alias reference which are allowed in source/dest properties. response."""
    root: list[GetNodesNodeLxcVmidFirewallRefsResponseItem] = Field(...)

class GetNodesNodeLxcVmidFirewallRulesResponseItem(ProxmoxBaseModel):
    """Model for get_rules. List rules. response."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr | None = Field(None, description='Rule type')

class GetNodesNodeLxcVmidFirewallRulesResponse(RootModel[list[GetNodesNodeLxcVmidFirewallRulesResponseItem]]):
    """List of items. get_rules. List rules. response."""
    root: list[GetNodesNodeLxcVmidFirewallRulesResponseItem] = Field(...)

class PostNodesNodeLxcVmidFirewallRulesRequest(ProxmoxBaseModel):
    """Model for create_rule. Create new rule. request."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr = Field(..., description='Rule type.')

class PostNodesNodeLxcVmidFirewallRulesResponse(RootModel[None]):
    """Model for create_rule. Create new rule. response."""
    root: None = Field(...)

class DeleteNodesNodeLxcVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for delete_rule. Delete rule. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeLxcVmidFirewallRulesPosResponse(RootModel[None]):
    """Model for delete_rule. Delete rule. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidFirewallRulesPosResponse(ProxmoxBaseModel):
    """Model for get_rule. Get single rule data. response."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr = Field(..., description='Rule type')

class PutNodesNodeLxcVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for update_rule. Modify rule data. request."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr | None = Field(None, description='Rule type.')

class PutNodesNodeLxcVmidFirewallRulesPosResponse(RootModel[None]):
    """Model for update_rule. Modify rule data. response."""
    root: None = Field(...)

class GetNodesNodeLxcVmidInterfacesResponseItem(ProxmoxBaseModel):
    """Model for ip. Get IP addresses of the specified container interface. response."""
    hardware_address: StrictStr | None = Field(None, alias="hardware-address", description='The MAC address of the interface')
    hwaddr: StrictStr | None = Field(None, description='The MAC address of the interface')
    inet: StrictStr | None = Field(None, description='The IPv4 address of the interface')
    inet6: StrictStr | None = Field(None, description='The IPv6 address of the interface')
    ip_addresses: list[dict[str, object]] | None = Field(None, alias="ip-addresses", description='The addresses of the interface')
    name: StrictStr | None = Field(None, description='The name of the interface')

class GetNodesNodeLxcVmidInterfacesResponse(RootModel[list[GetNodesNodeLxcVmidInterfacesResponseItem]]):
    """List of items. ip. Get IP addresses of the specified container interface. response."""
    root: list[GetNodesNodeLxcVmidInterfacesResponseItem] = Field(...)

class GetNodesNodeLxcVmidMigrateResponse(ProxmoxBaseModel):
    """Model for migrate_vm_precondition. Get preconditions for migration. response."""
    allowed_nodes: list[StrictStr] | None = Field(None, alias="allowed-nodes", description='List of nodes allowed for migration.')
    dependent_ha_resources: list[StrictStr] | None = Field(None, alias="dependent-ha-resources", description='HA resources, which will be migrated to the same target node as the VM, because these are in positive affinity with the VM.')
    not_allowed_nodes: dict[str, object] | None = Field(None, alias="not-allowed-nodes", description='List of not allowed nodes with additional information.')
    running: bool = Field(..., description='Determines if the container is running.')

class PostNodesNodeLxcVmidMigrateRequest(ProxmoxBaseModel):
    """Model for migrate_vm. Migrate the container to another node. Creates a new migration task. request."""
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    online: bool | None = Field(None, description='Use online/live migration.')
    restart: bool | None = Field(None, description='Use restart migration')
    target: StrictStr = Field(..., description='Target node.')
    target_storage: StrictStr | None = Field(None, alias="target-storage", description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    timeout: int | None = Field(None, description='Timeout in seconds for shutdown for restart migration')

class PostNodesNodeLxcVmidMigrateResponse(RootModel[StrictStr]):
    """Model for migrate_vm. Migrate the container to another node. Creates a new migration task. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeLxcVmidMoveVolumeRequest(ProxmoxBaseModel):
    """Model for move_volume. Move a rootfs-/mp-volume to a different storage or to a different container. request."""
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original volume after successful copy. By default the original is kept as an unused volume entry.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 " .\n\t\t    "digest. This can be used to prevent concurrent modifications.')
    storage: StrictStr | None = Field(None, description='Target Storage.')
    target_digest: StrictStr | None = Field(None, alias="target-digest", description='Prevent changes if current configuration file of the target " .\n\t\t    "container has a different SHA1 digest. This can be used to prevent " .\n\t\t    "concurrent modifications.')
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')
    target_volume: StrictStr | None = Field(None, alias="target-volume", description='The config key the volume will be moved to. Default is the source volume key.')
    volume: StrictStr = Field(..., description='Volume which will be moved.')

class PostNodesNodeLxcVmidMoveVolumeResponse(RootModel[StrictStr]):
    """Model for move_volume. Move a rootfs-/mp-volume to a different storage or to a different container. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidMtunnelRequest(ProxmoxBaseModel):
    """Model for mtunnel. Migration tunnel endpoint - only for internal use by CT migration. request."""
    bridges: StrictStr | None = Field(None, description='List of network bridges to check availability. Will be checked again for actually used bridges during migration.')
    storages: StrictStr | None = Field(None, description='List of storages to check permission and availability. Will be checked again for all actually used storages during migration.')

class PostNodesNodeLxcVmidMtunnelResponse(ProxmoxBaseModel):
    """Model for mtunnel. Migration tunnel endpoint - only for internal use by CT migration. response."""
    socket: StrictStr = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)

class GetNodesNodeLxcVmidMtunnelwebsocketResponse(ProxmoxBaseModel):
    """Model for mtunnelwebsocket. Migration tunnel endpoint for websocket upgrade - only for internal use by VM migration. response."""
    port: StrictStr | None = Field(None)
    socket: StrictStr | None = Field(None)

class GetNodesNodeLxcVmidPendingResponseItem(ProxmoxBaseModel):
    """Model for vm_pending. Get container configuration, including pending changes. response."""
    delete: int | None = Field(None, description='Indicates a pending delete request if present and not 0.')
    key: StrictStr | None = Field(None, description='Configuration option name.')
    pending: StrictStr | None = Field(None, description='Pending value.')
    value: StrictStr | None = Field(None, description='Current value.')

class GetNodesNodeLxcVmidPendingResponse(RootModel[list[GetNodesNodeLxcVmidPendingResponseItem]]):
    """List of items. vm_pending. Get container configuration, including pending changes. response."""
    root: list[GetNodesNodeLxcVmidPendingResponseItem] = Field(...)

class PostNodesNodeLxcVmidRemoteMigrateRequest(ProxmoxBaseModel):
    """Model for remote_migrate_vm. Migrate the container to another cluster. Creates a new migration task. EXPERIMENTAL feature! request."""
    bwlimit: float | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original CT and related data after successful migration. By default the original CT is kept on the source cluster in a stopped state.')
    online: bool | None = Field(None, description='Use online/live migration.')
    restart: bool | None = Field(None, description='Use restart migration')
    target_bridge: StrictStr = Field(..., alias="target-bridge", description="Mapping from source to target bridges. Providing only a single bridge ID maps all source bridges to that bridge. Providing the special value '1' will map each source bridge to itself.")
    target_endpoint: StrictStr = Field(..., alias="target-endpoint", description='Remote target endpoint')
    target_storage: StrictStr = Field(..., alias="target-storage", description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')
    timeout: int | None = Field(None, description='Timeout in seconds for shutdown for restart migration')

class PostNodesNodeLxcVmidRemoteMigrateResponse(RootModel[StrictStr]):
    """Model for remote_migrate_vm. Migrate the container to another cluster. Creates a new migration task. EXPERIMENTAL feature! response."""
    root: StrictStr = Field(..., description='the task ID.')

class PutNodesNodeLxcVmidResizeRequest(ProxmoxBaseModel):
    """Model for resize_vm. Resize a container mount point. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    disk: StrictStr = Field(..., description='The disk you want to resize.')
    size: StrictStr = Field(..., description="The new size. With the '+' sign the value is added to the actual size of the volume and without it, the value is taken as an absolute one. Shrinking disk size is not supported.")

class PutNodesNodeLxcVmidResizeResponse(RootModel[StrictStr]):
    """Model for resize_vm. Resize a container mount point. response."""
    root: StrictStr = Field(..., description='the task ID.')

class GetNodesNodeLxcVmidRrdResponse(ProxmoxBaseModel):
    """Model for rrd. Read VM RRD statistics (returns PNG) response."""
    filename: StrictStr = Field(...)

class GetNodesNodeLxcVmidRrddataResponse(RootModel[list[dict[str, object]]]):
    """Model for rrddata. Read VM RRD statistics response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeLxcVmidSnapshotResponseItem(ProxmoxBaseModel):
    """Model for list. List all snapshots. response."""
    description: StrictStr | None = Field(None, description='Snapshot description.')
    name: StrictStr | None = Field(None, description="Snapshot identifier. Value 'current' identifies the current VM.")
    parent: StrictStr | None = Field(None, description='Parent snapshot identifier.')
    snaptime: int | None = Field(None, description='Snapshot creation time')

class GetNodesNodeLxcVmidSnapshotResponse(RootModel[list[GetNodesNodeLxcVmidSnapshotResponseItem]]):
    """List of items. list. List all snapshots. response."""
    root: list[GetNodesNodeLxcVmidSnapshotResponseItem] = Field(...)

class PostNodesNodeLxcVmidSnapshotRequest(ProxmoxBaseModel):
    """Model for snapshot. Snapshot a container. request."""
    description: StrictStr | None = Field(None, description='A textual description or comment.')
    snapname: StrictStr = Field(..., description='The name of the snapshot.')

class PostNodesNodeLxcVmidSnapshotResponse(RootModel[StrictStr]):
    """Model for snapshot. Snapshot a container. response."""
    root: StrictStr = Field(..., description='the task ID.')

class DeleteNodesNodeLxcVmidSnapshotSnapnameRequest(ProxmoxBaseModel):
    """Model for delsnapshot. Delete a LXC snapshot. request."""
    force: bool | None = Field(None, description='For removal from config file, even if removing disk snapshots fails.')

class DeleteNodesNodeLxcVmidSnapshotSnapnameResponse(RootModel[StrictStr]):
    """Model for delsnapshot. Delete a LXC snapshot. response."""
    root: StrictStr = Field(..., description='the task ID.')

class GetNodesNodeLxcVmidSnapshotSnapnameResponse(RootModel[list[dict[str, object]]]):
    """Model for snapshot_cmd_idx. None response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeLxcVmidSnapshotSnapnameConfigResponse(RootModel[dict[str, object]]):
    """Model for get_snapshot_config. Get snapshot configuration response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeLxcVmidSnapshotSnapnameConfigRequest(ProxmoxBaseModel):
    """Model for update_snapshot_config. Update snapshot metadata. request."""
    description: StrictStr | None = Field(None, description='A textual description or comment.')

class PutNodesNodeLxcVmidSnapshotSnapnameConfigResponse(RootModel[None]):
    """Model for update_snapshot_config. Update snapshot metadata. response."""
    root: None = Field(...)

class PostNodesNodeLxcVmidSnapshotSnapnameRollbackRequest(ProxmoxBaseModel):
    """Model for rollback. Rollback LXC state to specified snapshot. request."""
    start: bool | None = Field(None, description='Whether the container should get started after rolling back successfully')

class PostNodesNodeLxcVmidSnapshotSnapnameRollbackResponse(RootModel[StrictStr]):
    """Model for rollback. Rollback LXC state to specified snapshot. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeLxcVmidSpiceproxyRequest(ProxmoxBaseModel):
    """Model for spiceproxy. Returns a SPICE configuration to connect to the CT. request."""
    proxy: StrictStr | None = Field(None, description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs 'spiceproxy', so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).")

class PostNodesNodeLxcVmidSpiceproxyResponse(ProxmoxBaseModel):
    """Model for spiceproxy. Returns a SPICE configuration to connect to the CT. response."""
    host: StrictStr = Field(...)
    password: StrictStr = Field(...)
    proxy: StrictStr = Field(...)
    tls_port: int = Field(..., alias="tls-port")
    type: StrictStr = Field(...)

class GetNodesNodeLxcVmidStatusResponseItem(ProxmoxBaseModel):
    """Model for vmcmdidx. Directory index response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeLxcVmidStatusResponse(RootModel[list[GetNodesNodeLxcVmidStatusResponseItem]]):
    """List of items. vmcmdidx. Directory index response."""
    root: list[GetNodesNodeLxcVmidStatusResponseItem] = Field(...)

class GetNodesNodeLxcVmidStatusCurrentResponse(ProxmoxBaseModel):
    """Model for vm_status. Get virtual machine status. response."""
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    disk: int | None = Field(None, description='Root disk image space-usage in bytes.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    ha: dict[str, object] = Field(..., description='HA manager service status.')
    lock: StrictStr | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk image size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    maxswap: int | None = Field(None, description='Maximum SWAP memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes.')
    name: StrictStr | None = Field(None, description='Container name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    status: StrictStr = Field(..., description='LXC Container status.')
    tags: StrictStr | None = Field(None, description='The current configured tags, if any.')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int = Field(..., description='The (unique) ID of the VM.')

class PostNodesNodeLxcVmidStatusRebootRequest(ProxmoxBaseModel):
    """Model for vm_reboot. Reboot the container by shutting it down, and starting it again. Applies pending changes. request."""
    timeout: int | None = Field(None, description='Wait maximal timeout seconds for the shutdown.')

class PostNodesNodeLxcVmidStatusRebootResponse(RootModel[StrictStr]):
    """Model for vm_reboot. Reboot the container by shutting it down, and starting it again. Applies pending changes. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidStatusResumeResponse(RootModel[StrictStr]):
    """Model for vm_resume. Resume the container. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidStatusShutdownRequest(ProxmoxBaseModel):
    """Model for vm_shutdown. Shutdown the container. This will trigger a clean shutdown of the container, see lxc-stop(1) for details. request."""
    force_stop: bool | None = Field(None, alias="forceStop", description='Make sure the Container stops.')
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')

class PostNodesNodeLxcVmidStatusShutdownResponse(RootModel[StrictStr]):
    """Model for vm_shutdown. Shutdown the container. This will trigger a clean shutdown of the container, see lxc-stop(1) for details. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidStatusStartRequest(ProxmoxBaseModel):
    """Model for vm_start. Start the container. request."""
    debug: bool | None = Field(None, description='If set, enables very verbose debug log-level on start.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeLxcVmidStatusStartResponse(RootModel[StrictStr]):
    """Model for vm_start. Start the container. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidStatusStopRequest(ProxmoxBaseModel):
    """Model for vm_stop. Stop the container. This will abruptly stop all processes running in the container. request."""
    overrule_shutdown: bool | None = Field(None, alias="overrule-shutdown", description="Try to abort active 'vzshutdown' tasks before stopping.")
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeLxcVmidStatusStopResponse(RootModel[StrictStr]):
    """Model for vm_stop. Stop the container. This will abruptly stop all processes running in the container. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidStatusSuspendResponse(RootModel[StrictStr]):
    """Model for vm_suspend. Suspend the container. This is experimental. response."""
    root: StrictStr = Field(...)

class PostNodesNodeLxcVmidTemplateResponse(RootModel[None]):
    """Model for template. Create a Template. response."""
    root: None = Field(...)

class PostNodesNodeLxcVmidTermproxyResponse(ProxmoxBaseModel):
    """Model for termproxy. Creates a TCP proxy connection. response."""
    port: int = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class PostNodesNodeLxcVmidVncproxyRequest(ProxmoxBaseModel):
    """Model for vncproxy. Creates a TCP VNC proxy connections. request."""
    height: int | None = Field(None, description='sets the height of the console in pixels.')
    websocket: bool | None = Field(None, description='use websocket instead of standard VNC.')
    width: int | None = Field(None, description='sets the width of the console in pixels.')

class PostNodesNodeLxcVmidVncproxyResponse(ProxmoxBaseModel):
    """Model for vncproxy. Creates a TCP VNC proxy connections. response."""
    cert: StrictStr = Field(...)
    password: StrictStr | None = Field(None, description="Password used for authentication within the VNC protocol. Consists of printable ASCII characters ('!' .. '~').")
    port: int = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class GetNodesNodeLxcVmidVncwebsocketResponse(ProxmoxBaseModel):
    """Model for vncwebsocket. Opens a websocket for VNC traffic. response."""
    port: StrictStr = Field(...)

class PostNodesNodeMigrateallRequest(ProxmoxBaseModel):
    """Model for migrateall. Migrate all VMs and Containers. request."""
    max_workers: int | None = Field(None, alias="max-workers", description="Maximal number of parallel migration job. If not set, uses'max_workers' from datacenter.cfg. One of both must be set!")
    maxworkers: int | None = Field(None, description="Maximal number of parallel migration job. If not set, uses'max_workers' from datacenter.cfg. One of both must be set!Deprecated, use 'max-workers' instead.")
    target: StrictStr = Field(..., description='Target node.')
    vms: StrictStr | None = Field(None, description='Only consider Guests with these IDs.')
    with_local_disks: bool | None = Field(None, alias="with-local-disks", description='Enable live storage migration for local disk')

class PostNodesNodeMigrateallResponse(RootModel[StrictStr]):
    """Model for migrateall. Migrate all VMs and Containers. response."""
    root: StrictStr = Field(...)

class GetNodesNodeNetstatResponse(RootModel[list[dict[str, object]]]):
    """Model for netstat. Read tap/vm network device interface counters response."""
    root: list[dict[str, object]] = Field(...)

class DeleteNodesNodeNetworkResponse(RootModel[None]):
    """Model for revert_network_changes. Revert network configuration changes. response."""
    root: None = Field(...)

class GetNodesNodeNetworkResponseItem(ProxmoxBaseModel):
    """Model for index. List available networks response."""
    active: bool | None = Field(None, description='Set to true if the interface is active.')
    address: StrictStr | None = Field(None, description='IP address.')
    address6: StrictStr | None = Field(None, description='IP address.')
    autostart: bool | None = Field(None, description='Automatically start interface on boot.')
    bond_primary: StrictStr | None = Field(None, alias="bond-primary", description='Specify the primary interface for active-backup bond.')
    bond_mode: StrictStr | None = Field(None, description='Bonding mode.')
    bond_xmit_hash_policy: StrictStr | None = Field(None, description='Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes.')
    bridge_access: int | None = Field(None, alias="bridge-access", description='The bridge port access VLAN.')
    bridge_arp_nd_suppress: bool | None = Field(None, alias="bridge-arp-nd-suppress", description='Bridge port ARP/ND suppress flag.')
    bridge_learning: bool | None = Field(None, alias="bridge-learning", description='Bridge port learning flag.')
    bridge_multicast_flood: bool | None = Field(None, alias="bridge-multicast-flood", description='Bridge port multicast flood flag.')
    bridge_unicast_flood: bool | None = Field(None, alias="bridge-unicast-flood", description='Bridge port unicast flood flag.')
    bridge_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    bridge_vids: StrictStr | None = Field(None, description="Specify the allowed VLANs. For example: '2 4 100-200'. Only used if the bridge is VLAN aware.")
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: StrictStr | None = Field(None, description='IPv4 CIDR.')
    cidr6: StrictStr | None = Field(None, description='IPv6 CIDR.')
    comments: StrictStr | None = Field(None, description='Comments')
    comments6: StrictStr | None = Field(None, description='Comments')
    exists: bool | None = Field(None, description='Set to true if the interface physically exists.')
    families: list[StrictStr] | None = Field(None, description='The network families.')
    gateway: StrictStr | None = Field(None, description='Default gateway address.')
    gateway6: StrictStr | None = Field(None, description='Default ipv6 gateway address.')
    iface: StrictStr | None = Field(None, description='Network interface name.')
    link_type: StrictStr | None = Field(None, alias="link-type", description='The link type.')
    method: StrictStr | None = Field(None, description='The network configuration method for IPv4.')
    method6: StrictStr | None = Field(None, description='The network configuration method for IPv6.')
    mtu: int | None = Field(None, description='MTU.')
    netmask: StrictStr | None = Field(None, description='Network mask.')
    netmask6: int | None = Field(None, description='Network mask.')
    options: list[StrictStr] | None = Field(None, description='A list of additional interface options for IPv4.')
    options6: list[StrictStr] | None = Field(None, description='A list of additional interface options for IPv6.')
    ovs_bonds: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    ovs_bridge: StrictStr | None = Field(None, description='The OVS bridge associated with a OVS port. This is required when you create an OVS port.')
    ovs_options: StrictStr | None = Field(None, description='OVS interface options.')
    ovs_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    ovs_tag: int | None = Field(None, description='Specify a VLan tag (used by OVSPort, OVSIntPort, OVSBond)')
    priority: int | None = Field(None, description='The order of the interface.')
    slaves: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    type: StrictStr | None = Field(None, description='Network interface type')
    uplink_id: StrictStr | None = Field(None, alias="uplink-id", description='The uplink ID.')
    vlan_id: int | None = Field(None, alias="vlan-id", description='vlan-id for a custom named vlan interface (ifupdown2 only).')
    vlan_protocol: StrictStr | None = Field(None, alias="vlan-protocol", description='The VLAN protocol.')
    vlan_raw_device: StrictStr | None = Field(None, alias="vlan-raw-device", description='Specify the raw interface for the vlan interface.')
    vxlan_id: int | None = Field(None, alias="vxlan-id", description='The VXLAN ID.')
    vxlan_local_tunnelip: StrictStr | None = Field(None, alias="vxlan-local-tunnelip", description='The VXLAN local tunnel IP.')
    vxlan_physdev: StrictStr | None = Field(None, alias="vxlan-physdev", description='The physical device for the VXLAN tunnel.')
    vxlan_svcnodeip: StrictStr | None = Field(None, alias="vxlan-svcnodeip", description='The VXLAN SVC node IP.')

class GetNodesNodeNetworkResponse(RootModel[list[GetNodesNodeNetworkResponseItem]]):
    """List of items. index. List available networks response."""
    root: list[GetNodesNodeNetworkResponseItem] = Field(...)

class PostNodesNodeNetworkRequest(ProxmoxBaseModel):
    """Model for create_network. Create network device configuration request."""
    address: StrictStr | None = Field(None, description='IP address.')
    address6: StrictStr | None = Field(None, description='IP address.')
    autostart: bool | None = Field(None, description='Automatically start interface on boot.')
    bond_primary: StrictStr | None = Field(None, alias="bond-primary", description='Specify the primary interface for active-backup bond.')
    bond_mode: StrictStr | None = Field(None, description='Bonding mode.')
    bond_xmit_hash_policy: StrictStr | None = Field(None, description='Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes.')
    bridge_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    bridge_vids: StrictStr | None = Field(None, description="Specify the allowed VLANs. For example: '2 4 100-200'. Only used if the bridge is VLAN aware.")
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: StrictStr | None = Field(None, description='IPv4 CIDR.')
    cidr6: StrictStr | None = Field(None, description='IPv6 CIDR.')
    comments: StrictStr | None = Field(None, description='Comments')
    comments6: StrictStr | None = Field(None, description='Comments')
    gateway: StrictStr | None = Field(None, description='Default gateway address.')
    gateway6: StrictStr | None = Field(None, description='Default ipv6 gateway address.')
    iface: StrictStr = Field(..., description='Network interface name.')
    mtu: int | None = Field(None, description='MTU.')
    netmask: StrictStr | None = Field(None, description='Network mask.')
    netmask6: int | None = Field(None, description='Network mask.')
    ovs_bonds: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    ovs_bridge: StrictStr | None = Field(None, description='The OVS bridge associated with a OVS port. This is required when you create an OVS port.')
    ovs_options: StrictStr | None = Field(None, description='OVS interface options.')
    ovs_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    ovs_tag: int | None = Field(None, description='Specify a VLan tag (used by OVSPort, OVSIntPort, OVSBond)')
    slaves: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    type: StrictStr = Field(..., description='Network interface type')
    vlan_id: int | None = Field(None, alias="vlan-id", description='vlan-id for a custom named vlan interface (ifupdown2 only).')
    vlan_raw_device: StrictStr | None = Field(None, alias="vlan-raw-device", description='Specify the raw interface for the vlan interface.')

class PostNodesNodeNetworkResponse(RootModel[None]):
    """Model for create_network. Create network device configuration response."""
    root: None = Field(...)

class PutNodesNodeNetworkRequest(ProxmoxBaseModel):
    """Model for reload_network_config. Reload network configuration request."""
    regenerate_frr: bool | None = Field(None, alias="regenerate-frr", description='Whether FRR config generation should get skipped or not.')

class PutNodesNodeNetworkResponse(RootModel[StrictStr]):
    """Model for reload_network_config. Reload network configuration response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeNetworkIfaceResponse(RootModel[None]):
    """Model for delete_network. Delete network device configuration response."""
    root: None = Field(...)

class GetNodesNodeNetworkIfaceResponse(ProxmoxBaseModel):
    """Model for network_config. Read network device configuration response."""
    method: StrictStr = Field(...)
    type: StrictStr = Field(...)

class PutNodesNodeNetworkIfaceRequest(ProxmoxBaseModel):
    """Model for update_network. Update network device configuration request."""
    address: StrictStr | None = Field(None, description='IP address.')
    address6: StrictStr | None = Field(None, description='IP address.')
    autostart: bool | None = Field(None, description='Automatically start interface on boot.')
    bond_primary: StrictStr | None = Field(None, alias="bond-primary", description='Specify the primary interface for active-backup bond.')
    bond_mode: StrictStr | None = Field(None, description='Bonding mode.')
    bond_xmit_hash_policy: StrictStr | None = Field(None, description='Selects the transmit hash policy to use for slave selection in balance-xor and 802.3ad modes.')
    bridge_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    bridge_vids: StrictStr | None = Field(None, description="Specify the allowed VLANs. For example: '2 4 100-200'. Only used if the bridge is VLAN aware.")
    bridge_vlan_aware: bool | None = Field(None, description='Enable bridge vlan support.')
    cidr: StrictStr | None = Field(None, description='IPv4 CIDR.')
    cidr6: StrictStr | None = Field(None, description='IPv6 CIDR.')
    comments: StrictStr | None = Field(None, description='Comments')
    comments6: StrictStr | None = Field(None, description='Comments')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    gateway: StrictStr | None = Field(None, description='Default gateway address.')
    gateway6: StrictStr | None = Field(None, description='Default ipv6 gateway address.')
    mtu: int | None = Field(None, description='MTU.')
    netmask: StrictStr | None = Field(None, description='Network mask.')
    netmask6: int | None = Field(None, description='Network mask.')
    ovs_bonds: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    ovs_bridge: StrictStr | None = Field(None, description='The OVS bridge associated with a OVS port. This is required when you create an OVS port.')
    ovs_options: StrictStr | None = Field(None, description='OVS interface options.')
    ovs_ports: StrictStr | None = Field(None, description='Specify the interfaces you want to add to your bridge.')
    ovs_tag: int | None = Field(None, description='Specify a VLan tag (used by OVSPort, OVSIntPort, OVSBond)')
    slaves: StrictStr | None = Field(None, description='Specify the interfaces used by the bonding device.')
    type: StrictStr = Field(..., description='Network interface type')
    vlan_id: int | None = Field(None, alias="vlan-id", description='vlan-id for a custom named vlan interface (ifupdown2 only).')
    vlan_raw_device: StrictStr | None = Field(None, alias="vlan-raw-device", description='Specify the raw interface for the vlan interface.')

class PutNodesNodeNetworkIfaceResponse(RootModel[None]):
    """Model for update_network. Update network device configuration response."""
    root: None = Field(...)

class GetNodesNodeQemuResponseItem(ProxmoxBaseModel):
    """Model for vmlist. Virtual machine index (per node). response."""
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    lock: StrictStr | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes. Does not take into account kernel same-page merging (KSM). Uses information from ballooning when available.')
    memhost: int | None = Field(None, description='Current memory usage on the host. Does not take into account kernel same-page merging (KSM).')
    name: StrictStr | None = Field(None, description='VM (host)name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pid: int | None = Field(None, description='PID of the QEMU process, if the VM is running.')
    pressurecpufull: float | None = Field(None, description='CPU Full pressure stall average over the last 10 seconds.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    qmpstatus: StrictStr | None = Field(None, description="VM run state from the 'query-status' QMP monitor command.")
    running_machine: StrictStr | None = Field(None, alias="running-machine", description='The currently running machine type (if running).')
    running_qemu: StrictStr | None = Field(None, alias="running-qemu", description='The QEMU version the VM is currently using (if running).')
    serial: bool | None = Field(None, description='Guest has serial device configured.')
    status: StrictStr | None = Field(None, description='QEMU process status.')
    tags: StrictStr | None = Field(None, description='The current configured tags, if any')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int | None = Field(None, description='The (unique) ID of the VM.')

class GetNodesNodeQemuResponse(RootModel[list[GetNodesNodeQemuResponseItem]]):
    """List of items. vmlist. Virtual machine index (per node). response."""
    root: list[GetNodesNodeQemuResponseItem] = Field(...)

class PostNodesNodeQemuRequest(ProxmoxBaseModel):
    """Model for create_vm. Create or restore a virtual machine. request."""
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: StrictStr | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: StrictStr | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: StrictStr | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: StrictStr | None = Field(None, description='Virtual processor architecture. Defaults to the host architecture.')
    archive: StrictStr | None = Field(None, description="The backup archive. Either the file system path to a .tar or .vma file (use '-' to pipe data from stdin) or a proxmox storage backup volume identifier.")
    args: StrictStr | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: StrictStr | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.')
    bios: StrictStr | None = Field(None, description='Select BIOS implementation.')
    boot: StrictStr | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: StrictStr | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    cdrom: StrictStr | None = Field(None, description='This is an alias for option -ide2')
    cicustom: StrictStr | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: StrictStr | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: StrictStr | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: StrictStr | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: StrictStr | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    description: StrictStr | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    efidisk0: StrictStr | None = Field(None, description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    force: bool | None = Field(None, description='Allow to overwrite existing VM.')
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    ha_managed: bool | None = Field(None, alias="ha-managed", description='Add the VM as a HA resource after it was created.')
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: StrictStr | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: StrictStr | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: StrictStr | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: StrictStr | None = Field(None, alias="ide[n]", description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    import_working_storage: StrictStr | None = Field(None, alias="import-working-storage", description="A file-based storage with 'images' content-type enabled, which is used as an intermediary extraction storage during import. Defaults to the source storage.")
    intel_tdx: StrictStr | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: StrictStr | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: StrictStr | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: StrictStr | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    live_restore: bool | None = Field(None, alias="live-restore", description='Start the VM immediately while importing or restoring in the background.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the VM.')
    machine: StrictStr | None = Field(None, description='Specify the QEMU machine.')
    memory: StrictStr | None = Field(None, description='Memory properties.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: StrictStr | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: StrictStr | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: StrictStr | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description='Specify guest operating system.')
    parallel_n: StrictStr | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    pool: StrictStr | None = Field(None, description='Add the VM to the specified pool.')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    rng0: StrictStr | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    sata_n: StrictStr | None = Field(None, alias="sata[n]", description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsi_n: StrictStr | None = Field(None, alias="scsi[n]", description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsihw: StrictStr | None = Field(None, description='SCSI controller model')
    searchdomain: StrictStr | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: StrictStr | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    smbios1: StrictStr | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: StrictStr | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: StrictStr | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    start: bool | None = Field(None, description='Start VM after it was created successfully.')
    startdate: StrictStr | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    storage: StrictStr | None = Field(None, description='Default storage.')
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: StrictStr | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: StrictStr | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    unique: bool | None = Field(None, description='Assign a unique random ethernet address.')
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: StrictStr | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: StrictStr | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: StrictStr | None = Field(None, alias="virtio[n]", description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    virtiofs_n: StrictStr | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: StrictStr | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmid: int = Field(..., description='The (unique) ID of the VM.')
    vmstatestorage: StrictStr | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: StrictStr | None = Field(None, description='Create a virtual hardware watchdog device.')

class PostNodesNodeQemuResponse(RootModel[StrictStr]):
    """Model for create_vm. Create or restore a virtual machine. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeQemuVmidRequest(ProxmoxBaseModel):
    """Model for destroy_vm. Destroy the VM and  all used/owned volumes. Removes any VM specific permissions and firewall rules request."""
    destroy_unreferenced_disks: bool | None = Field(None, alias="destroy-unreferenced-disks", description='If set, destroy additionally all disks not referenced in the config but with a matching VMID from all enabled storages.')
    purge: bool | None = Field(None, description='Remove VMID from configurations, like backup & replication jobs and HA.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class DeleteNodesNodeQemuVmidResponse(RootModel[StrictStr]):
    """Model for destroy_vm. Destroy the VM and  all used/owned volumes. Removes any VM specific permissions and firewall rules response."""
    root: StrictStr = Field(...)

class GetNodesNodeQemuVmidResponseItem(ProxmoxBaseModel):
    """Model for vmdiridx. Directory index response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeQemuVmidResponse(RootModel[list[GetNodesNodeQemuVmidResponseItem]]):
    """List of items. vmdiridx. Directory index response."""
    root: list[GetNodesNodeQemuVmidResponseItem] = Field(...)

class GetNodesNodeQemuVmidAgentResponse(RootModel[list[dict[str, object]]]):
    """Model for index. QEMU Guest Agent command index. response."""
    root: list[dict[str, object]] = Field(..., description='Returns the list of QEMU Guest Agent commands')

class PostNodesNodeQemuVmidAgentRequest(ProxmoxBaseModel):
    """Model for agent. Execute QEMU Guest Agent commands. request."""
    command: StrictStr = Field(..., description='The QGA command.')

class PostNodesNodeQemuVmidAgentResponse(RootModel[dict[str, object]]):
    """Model for agent. Execute QEMU Guest Agent commands. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentExecRequest(ProxmoxBaseModel):
    """Model for exec. Executes the given command in the vm via the guest-agent and returns an object with the pid. request."""
    command: list[StrictStr] = Field(..., description='The command as a list of program + arguments.')
    input_data: StrictStr | None = Field(None, alias="input-data", description="Data to pass as 'input-data' to the guest. Usually treated as STDIN to 'command'.")

class PostNodesNodeQemuVmidAgentExecResponse(ProxmoxBaseModel):
    """Model for exec. Executes the given command in the vm via the guest-agent and returns an object with the pid. response."""
    pid: int = Field(..., description='The PID of the process started by the guest-agent.')

class GetNodesNodeQemuVmidAgentExecStatusResponse(ProxmoxBaseModel):
    """Model for exec-status. Gets the status of the given pid started by the guest-agent response."""
    err_data: StrictStr | None = Field(None, alias="err-data", description='stderr of the process')
    err_truncated: bool | None = Field(None, alias="err-truncated", description='true if stderr was not fully captured')
    exitcode: int | None = Field(None, description='process exit code if it was normally terminated.')
    exited: bool = Field(..., description='Tells if the given command has exited yet.')
    out_data: StrictStr | None = Field(None, alias="out-data", description='stdout of the process')
    out_truncated: bool | None = Field(None, alias="out-truncated", description='true if stdout was not fully captured')
    signal: int | None = Field(None, description='signal number or exception code if the process was abnormally terminated.')

class GetNodesNodeQemuVmidAgentFileReadResponse(ProxmoxBaseModel):
    """Model for file-read. Reads the given file via guest agent. Is limited to 16777216 bytes. response."""
    content: StrictStr = Field(..., description='The content of the file, maximum 16777216')
    truncated: bool | None = Field(None, description='If set to 1, the read did not reach the end of the file.')

class PostNodesNodeQemuVmidAgentFileWriteRequest(ProxmoxBaseModel):
    """Model for file-write. Writes the given file via guest agent. request."""
    content: StrictStr = Field(..., description='The content to write into the file.')
    encode: bool | None = Field(None, description='If set, the content will be encoded as base64 (required by QEMU).Otherwise the content needs to be encoded beforehand - defaults to true.')
    file: StrictStr = Field(..., description='The path to the file.')

class PostNodesNodeQemuVmidAgentFileWriteResponse(RootModel[None]):
    """Model for file-write. Writes the given file via guest agent. response."""
    root: None = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeFreezeResponse(RootModel[dict[str, object]]):
    """Model for fsfreeze-freeze. Execute fsfreeze-freeze. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeStatusResponse(RootModel[dict[str, object]]):
    """Model for fsfreeze-status. Execute fsfreeze-status. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFsfreezeThawResponse(RootModel[dict[str, object]]):
    """Model for fsfreeze-thaw. Execute fsfreeze-thaw. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentFstrimResponse(RootModel[dict[str, object]]):
    """Model for fstrim. Execute fstrim. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetFsinfoResponse(RootModel[dict[str, object]]):
    """Model for get-fsinfo. Execute get-fsinfo. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetHostNameResponse(RootModel[dict[str, object]]):
    """Model for get-host-name. Execute get-host-name. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetMemoryBlockInfoResponse(RootModel[dict[str, object]]):
    """Model for get-memory-block-info. Execute get-memory-block-info. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetMemoryBlocksResponse(RootModel[dict[str, object]]):
    """Model for get-memory-blocks. Execute get-memory-blocks. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetOsinfoResponse(RootModel[dict[str, object]]):
    """Model for get-osinfo. Execute get-osinfo. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetTimeResponse(RootModel[dict[str, object]]):
    """Model for get-time. Execute get-time. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetTimezoneResponse(RootModel[dict[str, object]]):
    """Model for get-timezone. Execute get-timezone. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetUsersResponse(RootModel[dict[str, object]]):
    """Model for get-users. Execute get-users. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentGetVcpusResponse(RootModel[dict[str, object]]):
    """Model for get-vcpus. Execute get-vcpus. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentInfoResponse(RootModel[dict[str, object]]):
    """Model for info. Execute info. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeQemuVmidAgentNetworkGetInterfacesResponse(RootModel[dict[str, object]]):
    """Model for network-get-interfaces. Execute network-get-interfaces. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentPingResponse(RootModel[dict[str, object]]):
    """Model for ping. Execute ping. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSetUserPasswordRequest(ProxmoxBaseModel):
    """Model for set-user-password. Sets the password for the given user to the given password request."""
    crypted: bool | None = Field(None, description='set to 1 if the password has already been passed through crypt()')
    password: StrictStr = Field(..., description='The new password.')
    username: StrictStr = Field(..., description='The user to set the password for.')

class PostNodesNodeQemuVmidAgentSetUserPasswordResponse(RootModel[dict[str, object]]):
    """Model for set-user-password. Sets the password for the given user to the given password response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentShutdownResponse(RootModel[dict[str, object]]):
    """Model for shutdown. Execute shutdown. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendDiskResponse(RootModel[dict[str, object]]):
    """Model for suspend-disk. Execute suspend-disk. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendHybridResponse(RootModel[dict[str, object]]):
    """Model for suspend-hybrid. Execute suspend-hybrid. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidAgentSuspendRamResponse(RootModel[dict[str, object]]):
    """Model for suspend-ram. Execute suspend-ram. response."""
    root: dict[str, object] = Field(...)

class PostNodesNodeQemuVmidCloneRequest(ProxmoxBaseModel):
    """Model for clone_vm. Create a copy of virtual machine/template. request."""
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    description: StrictStr | None = Field(None, description='Description for the new VM.')
    format: StrictStr | None = Field(None, description='Target format for file storage. Only valid for full clone.')
    full: bool | None = Field(None, description='Create a full copy of all disks. This is always done when you clone a normal VM. For VM templates, we try to create a linked clone by default.')
    name: StrictStr | None = Field(None, description='Set a name for the new VM.')
    newid: int = Field(..., description='VMID for the clone.')
    pool: StrictStr | None = Field(None, description='Add the new VM to the specified pool.')
    snapname: StrictStr | None = Field(None, description='The name of the snapshot.')
    storage: StrictStr | None = Field(None, description='Target storage for full clone.')
    target: StrictStr | None = Field(None, description='Target node. Only allowed if the original VM is on shared storage.')

class PostNodesNodeQemuVmidCloneResponse(RootModel[StrictStr]):
    """Model for clone_vm. Create a copy of virtual machine/template. response."""
    root: StrictStr = Field(...)

class GetNodesNodeQemuVmidCloudinitResponseItem(ProxmoxBaseModel):
    """Model for cloudinit_pending. Get the cloudinit configuration with both current and pending values. response."""
    delete: int | None = Field(None, description='Indicates a pending delete request if present and not 0. ')
    key: StrictStr | None = Field(None, description='Configuration option name.')
    pending: StrictStr | None = Field(None, description='The new pending value.')
    value: StrictStr | None = Field(None, description='Value as it was used to generate the current cloudinit image.')

class GetNodesNodeQemuVmidCloudinitResponse(RootModel[list[GetNodesNodeQemuVmidCloudinitResponseItem]]):
    """List of items. cloudinit_pending. Get the cloudinit configuration with both current and pending values. response."""
    root: list[GetNodesNodeQemuVmidCloudinitResponseItem] = Field(...)

class PutNodesNodeQemuVmidCloudinitResponse(RootModel[None]):
    """Model for cloudinit_update. Regenerate and change cloudinit config drive. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidCloudinitDumpResponse(RootModel[StrictStr]):
    """Model for cloudinit_generated_config_dump. Get automatically generated cloudinit config. response."""
    root: StrictStr = Field(...)

class GetNodesNodeQemuVmidConfigResponse(ProxmoxBaseModel):
    """Model for vm_config. Get the virtual machine configuration with pending configuration changes applied. Set the 'current' parameter to get the current configuration instead. response."""
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: StrictStr | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: StrictBool | Annotated[StrictInt, Field(ge=0, le=1)] | StrictStr | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: StrictStr | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: StrictStr | None = Field(None, description='Virtual processor architecture. Defaults to the host architecture.')
    args: StrictStr | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: StrictStr | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.')
    bios: StrictStr | None = Field(None, description='Select BIOS implementation.')
    boot: StrictStr | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: StrictStr | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    cdrom: StrictStr | None = Field(None, description='This is an alias for option -ide2')
    cicustom: StrictStr | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: StrictStr | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: StrictStr | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: StrictStr | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: StrictStr | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    description: StrictStr | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    digest: StrictStr = Field(..., description='SHA1 digest of configuration file. This can be used to prevent concurrent modifications.')
    efidisk0: StrictStr | None = Field(None, description='Configure a disk for storing EFI vars.')
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: StrictStr | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: StrictStr | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: StrictStr | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: StrictStr | None = Field(None, alias="ide[n]", description='Use volume as IDE hard disk or CD-ROM (n is 0 to 3).')
    intel_tdx: StrictStr | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: StrictStr | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: StrictStr | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: StrictStr | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the VM.')
    machine: StrictStr | None = Field(None, description='Specify the QEMU machine.')
    memory: Annotated[StrictInt, Field(ge=16)] | StrictStr | None = Field(None, description='Memory properties.')
    meta: StrictStr | None = Field(None, description='Some (read-only) meta-information about this guest.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: StrictStr | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: StrictStr | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: StrictStr | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description='Specify guest operating system.')
    parallel_n: StrictStr | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    parent: StrictStr | None = Field(None, description='Parent snapshot name. This is used internally, and should not be modified.')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    rng0: StrictStr | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    running_nets_host_mtu: StrictStr | None = Field(None, alias="running-nets-host-mtu", description='List of VirtIO network devices and their effective host_mtu setting. A value of 0 means that the host_mtu parameter is to be avoided for the corresponding device. This is used internally for snapshots.')
    runningcpu: StrictStr | None = Field(None, description="Specifies the QEMU '-cpu' parameter of the running vm. This is used internally for snapshots.")
    runningmachine: StrictStr | None = Field(None, description='Specifies the QEMU machine type of the running vm. This is used internally for snapshots.')
    sata_n: StrictStr | None = Field(None, alias="sata[n]", description='Use volume as SATA hard disk or CD-ROM (n is 0 to 5).')
    scsi_n: StrictStr | None = Field(None, alias="scsi[n]", description='Use volume as SCSI hard disk or CD-ROM (n is 0 to 30).')
    scsihw: StrictStr | None = Field(None, description='SCSI controller model')
    searchdomain: StrictStr | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: StrictStr | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    smbios1: StrictStr | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    snaptime: int | None = Field(None, description='Timestamp for snapshots.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: StrictStr | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: StrictStr | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    startdate: StrictStr | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: StrictStr | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: StrictStr | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'.")
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: StrictStr | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: StrictStr | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: StrictStr | None = Field(None, alias="virtio[n]", description='Use volume as VIRTIO hard disk (n is 0 to 15).')
    virtiofs_n: StrictStr | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: StrictStr | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmstate: StrictStr | None = Field(None, description='Reference to a volume which stores the VM state. This is used internally for snapshots.')
    vmstatestorage: StrictStr | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: StrictStr | None = Field(None, description='Create a virtual hardware watchdog device.')

class PostNodesNodeQemuVmidConfigRequest(ProxmoxBaseModel):
    """Model for update_vm_async. Set virtual machine options (asynchronous API). request."""
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: StrictStr | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: StrictStr | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: StrictStr | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: StrictStr | None = Field(None, description='Virtual processor architecture. Defaults to the host architecture.')
    args: StrictStr | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: StrictStr | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    background_delay: int | None = Field(None, description="Time to wait for the task to finish. We return 'null' if the task finish within that time.")
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.')
    bios: StrictStr | None = Field(None, description='Select BIOS implementation.')
    boot: StrictStr | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: StrictStr | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    cdrom: StrictStr | None = Field(None, description='This is an alias for option -ide2')
    cicustom: StrictStr | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: StrictStr | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: StrictStr | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: StrictStr | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: StrictStr | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    efidisk0: StrictStr | None = Field(None, description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    force: bool | None = Field(None, description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called 'unused[n]', which contains the volume ID. Unlink of unused[n] always cause physical removal.")
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: StrictStr | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: StrictStr | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: StrictStr | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: StrictStr | None = Field(None, alias="ide[n]", description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    import_working_storage: StrictStr | None = Field(None, alias="import-working-storage", description="A file-based storage with 'images' content-type enabled, which is used as an intermediary extraction storage during import. Defaults to the source storage.")
    intel_tdx: StrictStr | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: StrictStr | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: StrictStr | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: StrictStr | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the VM.')
    machine: StrictStr | None = Field(None, description='Specify the QEMU machine.')
    memory: StrictStr | None = Field(None, description='Memory properties.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: StrictStr | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: StrictStr | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: StrictStr | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description='Specify guest operating system.')
    parallel_n: StrictStr | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    revert: StrictStr | None = Field(None, description='Revert a pending change.')
    rng0: StrictStr | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    sata_n: StrictStr | None = Field(None, alias="sata[n]", description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsi_n: StrictStr | None = Field(None, alias="scsi[n]", description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsihw: StrictStr | None = Field(None, description='SCSI controller model')
    searchdomain: StrictStr | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: StrictStr | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    smbios1: StrictStr | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: StrictStr | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: StrictStr | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    startdate: StrictStr | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: StrictStr | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: StrictStr | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: StrictStr | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: StrictStr | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: StrictStr | None = Field(None, alias="virtio[n]", description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    virtiofs_n: StrictStr | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: StrictStr | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmstatestorage: StrictStr | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: StrictStr | None = Field(None, description='Create a virtual hardware watchdog device.')

class PostNodesNodeQemuVmidConfigResponse(RootModel[StrictStr]):
    """Model for update_vm_async. Set virtual machine options (asynchronous API). response."""
    root: StrictStr = Field(...)

class PutNodesNodeQemuVmidConfigRequest(ProxmoxBaseModel):
    """Model for update_vm. Set virtual machine options (synchronous API) - You should consider using the POST method instead for any actions involving hotplug or storage allocation. request."""
    acpi: bool | None = Field(None, description='Enable/disable ACPI.')
    affinity: StrictStr | None = Field(None, description='List of host cores used to execute guest processes, for example: 0,5,8-11')
    agent: StrictStr | None = Field(None, description='Enable/disable communication with the QEMU Guest Agent and its properties.')
    allow_ksm: bool | None = Field(None, alias="allow-ksm", description='Allow memory pages of this guest to be merged via KSM (Kernel Samepage Merging).')
    amd_sev: StrictStr | None = Field(None, alias="amd-sev", description='Secure Encrypted Virtualization (SEV) features by AMD CPUs')
    arch: StrictStr | None = Field(None, description='Virtual processor architecture. Defaults to the host architecture.')
    args: StrictStr | None = Field(None, description='Arbitrary arguments passed to kvm.')
    audio0: StrictStr | None = Field(None, description='Configure a audio device, useful in combination with QXL/Spice.')
    autostart: bool | None = Field(None, description='Automatic restart after crash (currently ignored).')
    balloon: int | None = Field(None, description='Amount of target RAM for the VM in MiB. The balloon driver is enabled by default, unless it is explicitly disabled by setting the value to zero.')
    bios: StrictStr | None = Field(None, description='Select BIOS implementation.')
    boot: StrictStr | None = Field(None, description="Specify guest boot order. Use the 'order=' sub-property as usage with no key or 'legacy=' is deprecated.")
    bootdisk: StrictStr | None = Field(None, description="Enable booting from specified disk. Deprecated: Use 'boot: order=foo;bar' instead.")
    cdrom: StrictStr | None = Field(None, description='This is an alias for option -ide2')
    cicustom: StrictStr | None = Field(None, description='cloud-init: Specify custom files to replace the automatically generated ones at start.')
    cipassword: StrictStr | None = Field(None, description='cloud-init: Password to assign the user. Using this is generally not recommended. Use ssh keys instead. Also note that older cloud-init versions do not support hashed passwords.')
    citype: StrictStr | None = Field(None, description='Specifies the cloud-init configuration format. The default depends on the configured operating system type (`ostype`. We use the `nocloud` format for Linux, and `configdrive2` for windows.')
    ciupgrade: bool | None = Field(None, description='cloud-init: do an automatic package upgrade after the first boot.')
    ciuser: StrictStr | None = Field(None, description="cloud-init: User name to change ssh keys and password for instead of the image's configured default user.")
    cores: int | None = Field(None, description='The number of cores per socket.')
    cpu: StrictStr | None = Field(None, description='Emulated CPU type.')
    cpulimit: float | None = Field(None, description='Limit of CPU usage.')
    cpuunits: int | None = Field(None, description='CPU weight for a VM, will be clamped to [1, 10000] in cgroup v2.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    description: StrictStr | None = Field(None, description="Description for the VM. Shown in the web-interface VM's summary. This is saved as comment inside the configuration file.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    efidisk0: StrictStr | None = Field(None, description="Configure a disk for storing EFI vars. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and that the default EFI vars are copied to the volume instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    force: bool | None = Field(None, description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called 'unused[n]', which contains the volume ID. Unlink of unused[n] always cause physical removal.")
    freeze: bool | None = Field(None, description="Freeze CPU at startup (use 'c' monitor command to start execution).")
    hookscript: StrictStr | None = Field(None, description='Script that will be executed during various steps in the vms lifetime.')
    hostpci_n: StrictStr | None = Field(None, alias="hostpci[n]", description='Map host PCI devices into guest.')
    hotplug: StrictStr | None = Field(None, description="Selectively enable hotplug features. This is a comma separated list of hotplug features: 'network', 'disk', 'cpu', 'memory', 'usb' and 'cloudinit'. Use '0' to disable hotplug completely. Using '1' as value is an alias for the default `network,disk,usb`. USB hotplugging is possible for guests with machine version >= 7.1 and ostype l26 or windows > 7.")
    hugepages: StrictStr | None = Field(None, description="Enables hugepages memory.\n\nSets the size of hugepages in MiB. If the value is set to 'any' then 1 GiB hugepages will be used if possible, otherwise the size will fall back to 2 MiB.")
    ide_n: StrictStr | None = Field(None, alias="ide[n]", description="Use volume as IDE hard disk or CD-ROM (n is 0 to 3). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    intel_tdx: StrictStr | None = Field(None, alias="intel-tdx", description='Trusted Domain Extension (TDX) features by Intel CPUs')
    ipconfig_n: StrictStr | None = Field(None, alias="ipconfig[n]", description="cloud-init: Specify IP addresses and gateways for the corresponding interface.\n\nIP addresses use CIDR notation, gateways are optional but need an IP of the same type specified.\n\nThe special string 'dhcp' can be used for IP addresses to use DHCP, in which case no explicit\ngateway should be provided.\nFor IPv6 the special string 'auto' can be used to use stateless autoconfiguration. This requires\ncloud-init 19.4 or newer.\n\nIf cloud-init is enabled and neither an IPv4 nor an IPv6 address is specified, it defaults to using\ndhcp on IPv4.\n")
    ivshmem: StrictStr | None = Field(None, description='Inter-VM shared memory. Useful for direct communication between VMs, or to the host.')
    keephugepages: bool | None = Field(None, description='Use together with hugepages. If enabled, hugepages will not not be deleted after VM shutdown and can be used for subsequent starts.')
    keyboard: StrictStr | None = Field(None, description='Keyboard layout for VNC server. This option is generally not required and is often better handled from within the guest OS.')
    kvm: bool | None = Field(None, description='Enable/disable KVM hardware virtualization.')
    localtime: bool | None = Field(None, description='Set the real time clock (RTC) to local time. This is enabled by default if the `ostype` indicates a Microsoft Windows OS.')
    lock: StrictStr | None = Field(None, description='Lock/unlock the VM.')
    machine: StrictStr | None = Field(None, description='Specify the QEMU machine.')
    memory: StrictStr | None = Field(None, description='Memory properties.')
    migrate_downtime: float | None = Field(None, description='Set maximum tolerated downtime (in seconds) for migrations. Should the migration not be able to converge in the very end, because too much newly dirtied RAM needs to be transferred, the limit will be increased automatically step-by-step until migration can converge. Will be capped to 2000 seconds (maximum in QEMU).')
    migrate_speed: int | None = Field(None, description='Set maximum speed (in MB/s) for migrations. Value 0 is no limit.')
    name: StrictStr | None = Field(None, description='Set a name for the VM. Only used on the configuration web interface.')
    nameserver: StrictStr | None = Field(None, description='cloud-init: Sets DNS server IP address for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    net_n: StrictStr | None = Field(None, alias="net[n]", description='Specify network devices.')
    numa: bool | None = Field(None, description='Enable/disable NUMA.')
    numa_n: StrictStr | None = Field(None, alias="numa[n]", description='NUMA topology.')
    onboot: bool | None = Field(None, description='Specifies whether a VM will be started during system bootup.')
    ostype: StrictStr | None = Field(None, description='Specify guest operating system.')
    parallel_n: StrictStr | None = Field(None, alias="parallel[n]", description='Map host parallel devices (n is 0 to 2).')
    protection: bool | None = Field(None, description='Sets the protection flag of the VM. This will disable the remove VM and remove disk operations.')
    reboot: bool | None = Field(None, description="Allow reboot. If set to '0' the VM exit on reboot.")
    revert: StrictStr | None = Field(None, description='Revert a pending change.')
    rng0: StrictStr | None = Field(None, description='Configure a VirtIO-based Random Number Generator.')
    sata_n: StrictStr | None = Field(None, alias="sata[n]", description="Use volume as SATA hard disk or CD-ROM (n is 0 to 5). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsi_n: StrictStr | None = Field(None, alias="scsi[n]", description="Use volume as SCSI hard disk or CD-ROM (n is 0 to 30). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    scsihw: StrictStr | None = Field(None, description='SCSI controller model')
    searchdomain: StrictStr | None = Field(None, description='cloud-init: Sets DNS search domains for a container. Create will automatically use the setting from the host if neither searchdomain nor nameserver are set.')
    serial_n: StrictStr | None = Field(None, alias="serial[n]", description='Create a serial device inside the VM (n is 0 to 3)')
    shares: int | None = Field(None, description='Amount of memory shares for auto-ballooning. The larger the number is, the more memory this VM gets. Number is relative to weights of all other running VMs. Using zero disables auto-ballooning. Auto-ballooning is done by pvestatd.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    smbios1: StrictStr | None = Field(None, description='Specify SMBIOS type 1 fields.')
    smp: int | None = Field(None, description='The number of CPUs. Please use option -sockets instead.')
    sockets: int | None = Field(None, description='The number of CPU sockets.')
    spice_enhancements: StrictStr | None = Field(None, description='Configure additional enhancements for SPICE.')
    sshkeys: StrictStr | None = Field(None, description='cloud-init: Setup public SSH keys (one key per line, OpenSSH format).')
    startdate: StrictStr | None = Field(None, description="Set the initial date of the real time clock. Valid format for date are:'now' or '2006-06-17T16:01:21' or '2006-06-17'.")
    startup: StrictStr | None = Field(None, description="Startup and shutdown behavior. Order is a non-negative number defining the general startup order. Shutdown in done with reverse ordering. Additionally you can set the 'up' or 'down' delay in seconds, which specifies a delay to wait before the next VM is started or stopped.")
    tablet: bool | None = Field(None, description='Enable/disable the USB tablet device.')
    tags: StrictStr | None = Field(None, description='Tags of the VM. This is only meta information.')
    tdf: bool | None = Field(None, description='Enable/disable time drift fix.')
    template: bool | None = Field(None, description='Enable/disable Template.')
    tpmstate0: StrictStr | None = Field(None, description="Configure a Disk for storing TPM state. The format is fixed to 'raw'. Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Note that SIZE_IN_GiB is ignored here and 4 MiB will be used instead. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    unused_n: StrictStr | None = Field(None, alias="unused[n]", description='Reference to unused volumes. This is used internally, and should not be modified manually.')
    usb_n: StrictStr | None = Field(None, alias="usb[n]", description='Configure an USB device (n is 0 to 4, for machine version >= 7.1 and ostype l26 or windows > 7, n can be up to 14).')
    vcpus: int | None = Field(None, description='Number of hotplugged vcpus.')
    vga: StrictStr | None = Field(None, description='Configure the VGA hardware.')
    virtio_n: StrictStr | None = Field(None, alias="virtio[n]", description="Use volume as VIRTIO hard disk (n is 0 to 15). Use the special syntax STORAGE_ID:SIZE_IN_GiB to allocate a new volume. Use STORAGE_ID:0 and the 'import-from' parameter to import from an existing volume.")
    virtiofs_n: StrictStr | None = Field(None, alias="virtiofs[n]", description='Configuration for sharing a directory between host and guest using Virtio-fs.')
    vmgenid: StrictStr | None = Field(None, description="Set VM Generation ID. Use '1' to autogenerate on create or update, pass '0' to disable explicitly.")
    vmstatestorage: StrictStr | None = Field(None, description='Default storage for VM state volumes/files.')
    watchdog: StrictStr | None = Field(None, description='Create a virtual hardware watchdog device.')

class PutNodesNodeQemuVmidConfigResponse(RootModel[None]):
    """Model for update_vm. Set virtual machine options (synchronous API) - You should consider using the POST method instead for any actions involving hotplug or storage allocation. response."""
    root: None = Field(...)

class PostNodesNodeQemuVmidDbusVmstateRequest(ProxmoxBaseModel):
    """Model for dbus_vmstate. Control the dbus-vmstate helper for a given running VM. request."""
    action: StrictStr = Field(..., description='Action to perform on the DBus VMState helper.')

class PostNodesNodeQemuVmidDbusVmstateResponse(RootModel[None]):
    """Model for dbus_vmstate. Control the dbus-vmstate helper for a given running VM. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFeatureResponse(ProxmoxBaseModel):
    """Model for vm_feature. Check if feature for virtual machine is available. response."""
    has_feature: bool = Field(..., alias="hasFeature")
    nodes: list[StrictStr] = Field(...)

class GetNodesNodeQemuVmidFirewallResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeQemuVmidFirewallAliasesResponseItem(ProxmoxBaseModel):
    """Model for get_aliases. List aliases response."""
    cidr: StrictStr | None = Field(None)
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr | None = Field(None)

class GetNodesNodeQemuVmidFirewallAliasesResponse(RootModel[list[GetNodesNodeQemuVmidFirewallAliasesResponseItem]]):
    """List of items. get_aliases. List aliases response."""
    root: list[GetNodesNodeQemuVmidFirewallAliasesResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallAliasesRequest(ProxmoxBaseModel):
    """Model for create_alias. Create IP or Network Alias. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    name: StrictStr = Field(..., description='Alias name.')

class PostNodesNodeQemuVmidFirewallAliasesResponse(RootModel[None]):
    """Model for create_alias. Create IP or Network Alias. response."""
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    """Model for remove_alias. Remove IP or Network alias. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeQemuVmidFirewallAliasesNameResponse(RootModel[None]):
    """Model for remove_alias. Remove IP or Network alias. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallAliasesNameResponse(RootModel[dict[str, object]]):
    """Model for read_alias. Read alias. response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeQemuVmidFirewallAliasesNameRequest(ProxmoxBaseModel):
    """Model for update_alias. Update IP or Network alias. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    rename: StrictStr | None = Field(None, description='Rename an existing alias.')

class PutNodesNodeQemuVmidFirewallAliasesNameResponse(RootModel[None]):
    """Model for update_alias. Update IP or Network alias. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallIpsetResponseItem(ProxmoxBaseModel):
    """Model for ipset_index. List IPSets response."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr | None = Field(None, description='IP set name.')

class GetNodesNodeQemuVmidFirewallIpsetResponse(RootModel[list[GetNodesNodeQemuVmidFirewallIpsetResponseItem]]):
    """List of items. ipset_index. List IPSets response."""
    root: list[GetNodesNodeQemuVmidFirewallIpsetResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallIpsetRequest(ProxmoxBaseModel):
    """Model for create_ipset. Create new IPSet request."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    name: StrictStr = Field(..., description='IP set name.')
    rename: StrictStr | None = Field(None, description="Rename an existing IPSet. You can set 'rename' to the same value as 'name' to update the 'comment' of an existing IPSet.")

class PostNodesNodeQemuVmidFirewallIpsetResponse(RootModel[None]):
    """Model for create_ipset. Create new IPSet response."""
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    """Model for delete_ipset. Delete IPSet request."""
    force: bool | None = Field(None, description='Delete all members of the IPSet, if there are any.')

class DeleteNodesNodeQemuVmidFirewallIpsetNameResponse(RootModel[None]):
    """Model for delete_ipset. Delete IPSet response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallIpsetNameResponseItem(ProxmoxBaseModel):
    """Model for get_ipset. List IPSet content response."""
    cidr: StrictStr | None = Field(None)
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class GetNodesNodeQemuVmidFirewallIpsetNameResponse(RootModel[list[GetNodesNodeQemuVmidFirewallIpsetNameResponseItem]]):
    """List of items. get_ipset. List IPSet content response."""
    root: list[GetNodesNodeQemuVmidFirewallIpsetNameResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallIpsetNameRequest(ProxmoxBaseModel):
    """Model for create_ip. Add IP or Network to IPSet. request."""
    cidr: StrictStr = Field(..., description='Network/IP specification in CIDR format.')
    comment: StrictStr | None = Field(None)
    nomatch: bool | None = Field(None)

class PostNodesNodeQemuVmidFirewallIpsetNameResponse(RootModel[None]):
    """Model for create_ip. Add IP or Network to IPSet. response."""
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    """Model for remove_ip. Remove IP or Network from IPSet. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeQemuVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    """Model for remove_ip. Remove IP or Network from IPSet. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallIpsetNameCidrResponse(RootModel[dict[str, object]]):
    """Model for read_ip. Read IP or Network settings from IPSet. response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeQemuVmidFirewallIpsetNameCidrRequest(ProxmoxBaseModel):
    """Model for update_ip. Update IP or Network settings request."""
    comment: StrictStr | None = Field(None)
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    nomatch: bool | None = Field(None)

class PutNodesNodeQemuVmidFirewallIpsetNameCidrResponse(RootModel[None]):
    """Model for update_ip. Update IP or Network settings response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallLogResponseItem(ProxmoxBaseModel):
    """Model for log. Read firewall log response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeQemuVmidFirewallLogResponse(RootModel[list[GetNodesNodeQemuVmidFirewallLogResponseItem]]):
    """List of items. log. Read firewall log response."""
    root: list[GetNodesNodeQemuVmidFirewallLogResponseItem] = Field(...)

class GetNodesNodeQemuVmidFirewallOptionsResponse(ProxmoxBaseModel):
    """Model for get_options. Get VM firewall options. response."""
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: StrictStr | None = Field(None, description='Input policy.')
    policy_out: StrictStr | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeQemuVmidFirewallOptionsRequest(ProxmoxBaseModel):
    """Model for set_options. Set Firewall options. request."""
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dhcp: bool | None = Field(None, description='Enable DHCP.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    enable: bool | None = Field(None, description='Enable/disable firewall rules.')
    ipfilter: bool | None = Field(None, description="Enable default IP filters. This is equivalent to adding an empty ipfilter-net<id> ipset for every interface. Such ipsets implicitly contain sane default restrictions such as restricting IPv6 link local addresses to the one derived from the interface's MAC address. For containers the configured IP addresses will be implicitly added.")
    log_level_in: StrictStr | None = Field(None, description='Log level for incoming traffic.')
    log_level_out: StrictStr | None = Field(None, description='Log level for outgoing traffic.')
    macfilter: bool | None = Field(None, description='Enable/disable MAC address filter.')
    ndp: bool | None = Field(None, description='Enable NDP (Neighbor Discovery Protocol).')
    policy_in: StrictStr | None = Field(None, description='Input policy.')
    policy_out: StrictStr | None = Field(None, description='Output policy.')
    radv: bool | None = Field(None, description='Allow sending Router Advertisement.')

class PutNodesNodeQemuVmidFirewallOptionsResponse(RootModel[None]):
    """Model for set_options. Set Firewall options. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallRefsResponseItem(ProxmoxBaseModel):
    """Model for refs. Lists possible IPSet/Alias reference which are allowed in source/dest properties. response."""
    comment: StrictStr | None = Field(None)
    name: StrictStr | None = Field(None)
    ref: StrictStr | None = Field(None)
    scope: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)

class GetNodesNodeQemuVmidFirewallRefsResponse(RootModel[list[GetNodesNodeQemuVmidFirewallRefsResponseItem]]):
    """List of items. refs. Lists possible IPSet/Alias reference which are allowed in source/dest properties. response."""
    root: list[GetNodesNodeQemuVmidFirewallRefsResponseItem] = Field(...)

class GetNodesNodeQemuVmidFirewallRulesResponseItem(ProxmoxBaseModel):
    """Model for get_rules. List rules. response."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int | None = Field(None, description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr | None = Field(None, description='Rule type')

class GetNodesNodeQemuVmidFirewallRulesResponse(RootModel[list[GetNodesNodeQemuVmidFirewallRulesResponseItem]]):
    """List of items. get_rules. List rules. response."""
    root: list[GetNodesNodeQemuVmidFirewallRulesResponseItem] = Field(...)

class PostNodesNodeQemuVmidFirewallRulesRequest(ProxmoxBaseModel):
    """Model for create_rule. Create new rule. request."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    pos: int | None = Field(None, description='Update rule at position <pos>.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr = Field(..., description='Rule type.')

class PostNodesNodeQemuVmidFirewallRulesResponse(RootModel[None]):
    """Model for create_rule. Create new rule. response."""
    root: None = Field(...)

class DeleteNodesNodeQemuVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for delete_rule. Delete rule. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteNodesNodeQemuVmidFirewallRulesPosResponse(RootModel[None]):
    """Model for delete_rule. Delete rule. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidFirewallRulesPosResponse(ProxmoxBaseModel):
    """Model for get_rule. Get single rule data. response."""
    action: StrictStr = Field(..., description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name")
    comment: StrictStr | None = Field(None, description='Descriptive comment')
    dest: StrictStr | None = Field(None, description='Restrict packet destination address')
    dport: StrictStr | None = Field(None, description='Restrict TCP/UDP destination port')
    enable: int | None = Field(None, description='Flag to enable/disable a rule')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'")
    iface: StrictStr | None = Field(None, description='Network interface name. You have to use network configuration key names for VMs and containers')
    ipversion: int | None = Field(None, description='IP version (4 or 6) - automatically determined from source/dest addresses')
    log: StrictStr | None = Field(None, description='Log level for firewall rule')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro')
    pos: int = Field(..., description='Rule position in the ruleset')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'")
    source: StrictStr | None = Field(None, description='Restrict packet source address')
    sport: StrictStr | None = Field(None, description='Restrict TCP/UDP source port')
    type: StrictStr = Field(..., description='Rule type')

class PutNodesNodeQemuVmidFirewallRulesPosRequest(ProxmoxBaseModel):
    """Model for update_rule. Modify rule data. request."""
    action: StrictStr | None = Field(None, description="Rule action ('ACCEPT', 'DROP', 'REJECT') or security group name.")
    comment: StrictStr | None = Field(None, description='Descriptive comment.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    dest: StrictStr | None = Field(None, description="Restrict packet destination address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    dport: StrictStr | None = Field(None, description="Restrict TCP/UDP destination port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    enable: int | None = Field(None, description='Flag to enable/disable a rule.')
    icmp_type: StrictStr | None = Field(None, alias="icmp-type", description="Specify icmp-type. Only valid if proto equals 'icmp' or 'icmpv6'/'ipv6-icmp'.")
    iface: StrictStr | None = Field(None, description="Network interface name. You have to use network configuration key names for VMs and containers ('net\\d+'). Host related rules can use arbitrary strings.")
    log: StrictStr | None = Field(None, description='Log level for firewall rule.')
    macro: StrictStr | None = Field(None, description='Use predefined standard macro.')
    moveto: int | None = Field(None, description='Move rule to new position <moveto>. Other arguments are ignored.')
    proto: StrictStr | None = Field(None, description="IP protocol. You can use protocol names ('tcp'/'udp') or simple numbers, as defined in '/etc/protocols'.")
    source: StrictStr | None = Field(None, description="Restrict packet source address. This can refer to a single IP address, an IP set ('+ipsetname') or an IP alias definition. You can also specify an address range like '20.34.101.207-201.3.9.99', or a list of IP addresses and networks (entries are separated by comma). Please do not mix IPv4 and IPv6 addresses inside such lists.")
    sport: StrictStr | None = Field(None, description="Restrict TCP/UDP source port. You can use service names or simple numbers (0-65535), as defined in '/etc/services'. Port ranges can be specified with '\\d+:\\d+', for example '80:85', and you can use comma separated list to match several ports or ranges.")
    type: StrictStr | None = Field(None, description='Rule type.')

class PutNodesNodeQemuVmidFirewallRulesPosResponse(RootModel[None]):
    """Model for update_rule. Modify rule data. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidMigrateResponse(ProxmoxBaseModel):
    """Model for migrate_vm_precondition. Get preconditions for migration. response."""
    allowed_nodes: list[StrictStr] | None = Field(None, description='List of nodes allowed for migration.')
    dependent_ha_resources: list[StrictStr] | None = Field(None, alias="dependent-ha-resources", description='HA resources, which will be migrated to the same target node as the VM, because these are in positive affinity with the VM.')
    has_dbus_vmstate: bool = Field(..., alias="has-dbus-vmstate", description='Whether the VM host supports migrating additional VM state, such as conntrack entries.')
    local_disks: list[dict[str, object]] = Field(..., description='List local disks including CD-Rom, unused and not referenced disks')
    local_resources: list[StrictStr] = Field(..., description='List local resources (e.g. pci, usb) that block migration.')
    mapped_resource_info: dict[str, object] = Field(..., alias="mapped-resource-info", description="Object of mapped resources with additional information such if they're live migratable.")
    mapped_resources: list[StrictStr] = Field(..., alias="mapped-resources", description="List of mapped resources e.g. pci, usb. Deprecated, use 'mapped-resource-info' instead.")
    not_allowed_nodes: dict[str, object] | None = Field(None, description='List of not allowed nodes with additional information.')
    running: bool = Field(..., description='Determines if the VM is running.')

class PostNodesNodeQemuVmidMigrateRequest(ProxmoxBaseModel):
    """Model for migrate_vm. Migrate virtual machine. Creates a new migration task. request."""
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    force: bool | None = Field(None, description='Allow to migrate VMs which use local devices. Only root may use this option.')
    migration_network: StrictStr | None = Field(None, description='CIDR of the (sub) network that is used for migration.')
    migration_type: StrictStr | None = Field(None, description='Migration traffic is encrypted using an SSH tunnel by default. On secure, completely private networks this can be disabled to increase performance.')
    online: bool | None = Field(None, description='Use online/live migration if VM is running. Ignored if VM is stopped.')
    target: StrictStr = Field(..., description='Target node.')
    targetstorage: StrictStr | None = Field(None, description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    with_conntrack_state: bool | None = Field(None, alias="with-conntrack-state", description='Whether to migrate conntrack entries for running VMs.')
    with_local_disks: bool | None = Field(None, alias="with-local-disks", description='Enable live storage migration for local disk')

class PostNodesNodeQemuVmidMigrateResponse(RootModel[StrictStr]):
    """Model for migrate_vm. Migrate virtual machine. Creates a new migration task. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidMonitorRequest(ProxmoxBaseModel):
    """Model for monitor. Execute QEMU monitor commands. request."""
    command: StrictStr = Field(..., description='The monitor command.')

class PostNodesNodeQemuVmidMonitorResponse(RootModel[StrictStr]):
    """Model for monitor. Execute QEMU monitor commands. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidMoveDiskRequest(ProxmoxBaseModel):
    """Model for move_vm_disk. Move volume to different storage or to a different VM. request."""
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original disk after successful copy. By default the original disk is kept as unused disk.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    disk: StrictStr = Field(..., description='The disk you want to move.')
    format: StrictStr | None = Field(None, description='Target Format.')
    storage: StrictStr | None = Field(None, description='Target storage.')
    target_digest: StrictStr | None = Field(None, alias="target-digest", description='Prevent changes if the current config file of the target VM has a different SHA1 digest. This can be used to detect concurrent modifications.')
    target_disk: StrictStr | None = Field(None, alias="target-disk", description='The config key the disk will be moved to on the target VM (for example, ide0 or scsi1). Default is the source disk key.')
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')

class PostNodesNodeQemuVmidMoveDiskResponse(RootModel[StrictStr]):
    """Model for move_vm_disk. Move volume to different storage or to a different VM. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidMtunnelRequest(ProxmoxBaseModel):
    """Model for mtunnel. Migration tunnel endpoint - only for internal use by VM migration. request."""
    bridges: StrictStr | None = Field(None, description='List of network bridges to check availability. Will be checked again for actually used bridges during migration.')
    storages: StrictStr | None = Field(None, description='List of storages to check permission and availability. Will be checked again for all actually used storages during migration.')

class PostNodesNodeQemuVmidMtunnelResponse(ProxmoxBaseModel):
    """Model for mtunnel. Migration tunnel endpoint - only for internal use by VM migration. response."""
    socket: StrictStr = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)

class GetNodesNodeQemuVmidMtunnelwebsocketResponse(ProxmoxBaseModel):
    """Model for mtunnelwebsocket. Migration tunnel endpoint for websocket upgrade - only for internal use by VM migration. response."""
    port: StrictStr | None = Field(None)
    socket: StrictStr | None = Field(None)

class GetNodesNodeQemuVmidPendingResponseItem(ProxmoxBaseModel):
    """Model for vm_pending. Get the virtual machine configuration with both current and pending values. response."""
    delete: int | None = Field(None, description='Indicates a pending delete request if present and not 0. The value 2 indicates a force-delete request.')
    key: StrictStr | None = Field(None, description='Configuration option name.')
    pending: StrictStr | None = Field(None, description='Pending value.')
    value: StrictStr | None = Field(None, description='Current value.')

class GetNodesNodeQemuVmidPendingResponse(RootModel[list[GetNodesNodeQemuVmidPendingResponseItem]]):
    """List of items. vm_pending. Get the virtual machine configuration with both current and pending values. response."""
    root: list[GetNodesNodeQemuVmidPendingResponseItem] = Field(...)

class PostNodesNodeQemuVmidRemoteMigrateRequest(ProxmoxBaseModel):
    """Model for remote_migrate_vm. Migrate virtual machine to a remote cluster. Creates a new migration task. EXPERIMENTAL feature! request."""
    bwlimit: int | None = Field(None, description='Override I/O bandwidth limit (in KiB/s).')
    delete: bool | None = Field(None, description='Delete the original VM and related data after successful migration. By default the original VM is kept on the source cluster in a stopped state.')
    online: bool | None = Field(None, description='Use online/live migration if VM is running. Ignored if VM is stopped.')
    target_bridge: StrictStr = Field(..., alias="target-bridge", description="Mapping from source to target bridges. Providing only a single bridge ID maps all source bridges to that bridge. Providing the special value '1' will map each source bridge to itself.")
    target_endpoint: StrictStr = Field(..., alias="target-endpoint", description='Remote target endpoint')
    target_storage: StrictStr = Field(..., alias="target-storage", description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    target_vmid: int | None = Field(None, alias="target-vmid", description='The (unique) ID of the VM.')

class PostNodesNodeQemuVmidRemoteMigrateResponse(RootModel[StrictStr]):
    """Model for remote_migrate_vm. Migrate virtual machine to a remote cluster. Creates a new migration task. EXPERIMENTAL feature! response."""
    root: StrictStr = Field(..., description='the task ID.')

class PutNodesNodeQemuVmidResizeRequest(ProxmoxBaseModel):
    """Model for resize_vm. Extend volume size. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has different SHA1 digest. This can be used to prevent concurrent modifications.')
    disk: StrictStr = Field(..., description='The disk you want to resize.')
    size: StrictStr = Field(..., description='The new size. With the `+` sign the value is added to the actual size of the volume and without it, the value is taken as an absolute one. Shrinking disk size is not supported.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PutNodesNodeQemuVmidResizeResponse(RootModel[StrictStr]):
    """Model for resize_vm. Extend volume size. response."""
    root: StrictStr = Field(..., description='the task ID.')

class GetNodesNodeQemuVmidRrdResponse(ProxmoxBaseModel):
    """Model for rrd. Read VM RRD statistics (returns PNG) response."""
    filename: StrictStr = Field(...)

class GetNodesNodeQemuVmidRrddataResponse(RootModel[list[dict[str, object]]]):
    """Model for rrddata. Read VM RRD statistics response."""
    root: list[dict[str, object]] = Field(...)

class PutNodesNodeQemuVmidSendkeyRequest(ProxmoxBaseModel):
    """Model for vm_sendkey. Send key event to virtual machine. request."""
    key: StrictStr = Field(..., description='The key (qemu monitor encoding).')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PutNodesNodeQemuVmidSendkeyResponse(RootModel[None]):
    """Model for vm_sendkey. Send key event to virtual machine. response."""
    root: None = Field(...)

class GetNodesNodeQemuVmidSnapshotResponseItem(ProxmoxBaseModel):
    """Model for snapshot_list. List all snapshots. response."""
    description: StrictStr | None = Field(None, description='Snapshot description.')
    name: StrictStr | None = Field(None, description="Snapshot identifier. Value 'current' identifies the current VM.")
    parent: StrictStr | None = Field(None, description='Parent snapshot identifier.')
    snaptime: int | None = Field(None, description='Snapshot creation time')
    vmstate: bool | None = Field(None, description='Snapshot includes RAM.')

class GetNodesNodeQemuVmidSnapshotResponse(RootModel[list[GetNodesNodeQemuVmidSnapshotResponseItem]]):
    """List of items. snapshot_list. List all snapshots. response."""
    root: list[GetNodesNodeQemuVmidSnapshotResponseItem] = Field(...)

class PostNodesNodeQemuVmidSnapshotRequest(ProxmoxBaseModel):
    """Model for snapshot. Snapshot a VM. request."""
    description: StrictStr | None = Field(None, description='A textual description or comment.')
    snapname: StrictStr = Field(..., description='The name of the snapshot.')
    vmstate: bool | None = Field(None, description='Save the vmstate')

class PostNodesNodeQemuVmidSnapshotResponse(RootModel[StrictStr]):
    """Model for snapshot. Snapshot a VM. response."""
    root: StrictStr = Field(..., description='the task ID.')

class DeleteNodesNodeQemuVmidSnapshotSnapnameRequest(ProxmoxBaseModel):
    """Model for delsnapshot. Delete a VM snapshot. request."""
    force: bool | None = Field(None, description='For removal from config file, even if removing disk snapshots fails.')

class DeleteNodesNodeQemuVmidSnapshotSnapnameResponse(RootModel[StrictStr]):
    """Model for delsnapshot. Delete a VM snapshot. response."""
    root: StrictStr = Field(..., description='the task ID.')

class GetNodesNodeQemuVmidSnapshotSnapnameResponse(RootModel[list[dict[str, object]]]):
    """Model for snapshot_cmd_idx. None response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeQemuVmidSnapshotSnapnameConfigResponse(RootModel[dict[str, object]]):
    """Model for get_snapshot_config. Get snapshot configuration response."""
    root: dict[str, object] = Field(...)

class PutNodesNodeQemuVmidSnapshotSnapnameConfigRequest(ProxmoxBaseModel):
    """Model for update_snapshot_config. Update snapshot metadata. request."""
    description: StrictStr | None = Field(None, description='A textual description or comment.')

class PutNodesNodeQemuVmidSnapshotSnapnameConfigResponse(RootModel[None]):
    """Model for update_snapshot_config. Update snapshot metadata. response."""
    root: None = Field(...)

class PostNodesNodeQemuVmidSnapshotSnapnameRollbackRequest(ProxmoxBaseModel):
    """Model for rollback. Rollback VM state to specified snapshot. request."""
    start: bool | None = Field(None, description='Whether the VM should get started after rolling back successfully. (Note: VMs will be automatically started if the snapshot includes RAM.)')

class PostNodesNodeQemuVmidSnapshotSnapnameRollbackResponse(RootModel[StrictStr]):
    """Model for rollback. Rollback VM state to specified snapshot. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidSpiceproxyRequest(ProxmoxBaseModel):
    """Model for spiceproxy. Returns a SPICE configuration to connect to the VM. request."""
    proxy: StrictStr | None = Field(None, description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs 'spiceproxy', so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).")

class PostNodesNodeQemuVmidSpiceproxyResponse(ProxmoxBaseModel):
    """Model for spiceproxy. Returns a SPICE configuration to connect to the VM. response."""
    host: StrictStr = Field(...)
    password: StrictStr = Field(...)
    proxy: StrictStr = Field(...)
    tls_port: int = Field(..., alias="tls-port")
    type: StrictStr = Field(...)

class GetNodesNodeQemuVmidStatusResponseItem(ProxmoxBaseModel):
    """Model for vmcmdidx. Directory index response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeQemuVmidStatusResponse(RootModel[list[GetNodesNodeQemuVmidStatusResponseItem]]):
    """List of items. vmcmdidx. Directory index response."""
    root: list[GetNodesNodeQemuVmidStatusResponseItem] = Field(...)

class GetNodesNodeQemuVmidStatusCurrentResponse(ProxmoxBaseModel):
    """Model for vm_status. Get virtual machine status. response."""
    agent: bool | None = Field(None, description='QEMU Guest Agent is enabled in config.')
    clipboard: StrictStr | None = Field(None, description='Enable a specific clipboard. If not set, depending on the display type the SPICE one will be added.')
    cpu: float | None = Field(None, description='Current CPU usage.')
    cpus: float | None = Field(None, description='Maximum usable CPUs.')
    diskread: int | None = Field(None, description="The amount of bytes the guest read from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    diskwrite: int | None = Field(None, description="The amount of bytes the guest wrote from it's block devices since the guest was started. (Note: This info is not available for all storage types.)")
    ha: dict[str, object] = Field(..., description='HA manager service status.')
    lock: StrictStr | None = Field(None, description='The current config lock, if any.')
    maxdisk: int | None = Field(None, description='Root disk size in bytes.')
    maxmem: int | None = Field(None, description='Maximum memory in bytes.')
    mem: int | None = Field(None, description='Currently used memory in bytes. Does not take into account kernel same-page merging (KSM). Uses information from ballooning when available.')
    memhost: int | None = Field(None, description='Current memory usage on the host. Does not take into account kernel same-page merging (KSM).')
    name: StrictStr | None = Field(None, description='VM (host)name.')
    netin: int | None = Field(None, description='The amount of traffic in bytes that was sent to the guest over the network since it was started.')
    netout: int | None = Field(None, description='The amount of traffic in bytes that was sent from the guest over the network since it was started.')
    pid: int | None = Field(None, description='PID of the QEMU process, if the VM is running.')
    pressurecpufull: float | None = Field(None, description='CPU Full pressure stall average over the last 10 seconds.')
    pressurecpusome: float | None = Field(None, description='CPU Some pressure stall average over the last 10 seconds.')
    pressureiofull: float | None = Field(None, description='IO Full pressure stall average over the last 10 seconds.')
    pressureiosome: float | None = Field(None, description='IO Some pressure stall average over the last 10 seconds.')
    pressurememoryfull: float | None = Field(None, description='Memory Full pressure stall average over the last 10 seconds.')
    pressurememorysome: float | None = Field(None, description='Memory Some pressure stall average over the last 10 seconds.')
    qmpstatus: StrictStr | None = Field(None, description="VM run state from the 'query-status' QMP monitor command.")
    running_machine: StrictStr | None = Field(None, alias="running-machine", description='The currently running machine type (if running).')
    running_qemu: StrictStr | None = Field(None, alias="running-qemu", description='The QEMU version the VM is currently using (if running).')
    serial: bool | None = Field(None, description='Guest has serial device configured.')
    spice: bool | None = Field(None, description='QEMU VGA configuration supports spice.')
    status: StrictStr = Field(..., description='QEMU process status.')
    tags: StrictStr | None = Field(None, description='The current configured tags, if any')
    template: bool | None = Field(None, description='Determines if the guest is a template.')
    uptime: int | None = Field(None, description='Uptime in seconds.')
    vmid: int = Field(..., description='The (unique) ID of the VM.')

class PostNodesNodeQemuVmidStatusRebootRequest(ProxmoxBaseModel):
    """Model for vm_reboot. Reboot the VM by shutting it down, and starting it again. Applies pending changes. request."""
    timeout: int | None = Field(None, description='Wait maximal timeout seconds for the shutdown.')

class PostNodesNodeQemuVmidStatusRebootResponse(RootModel[StrictStr]):
    """Model for vm_reboot. Reboot the VM by shutting it down, and starting it again. Applies pending changes. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusResetRequest(ProxmoxBaseModel):
    """Model for vm_reset. Reset virtual machine. request."""
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeQemuVmidStatusResetResponse(RootModel[StrictStr]):
    """Model for vm_reset. Reset virtual machine. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusResumeRequest(ProxmoxBaseModel):
    """Model for vm_resume. Resume virtual machine. request."""
    nocheck: bool | None = Field(None)
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')

class PostNodesNodeQemuVmidStatusResumeResponse(RootModel[StrictStr]):
    """Model for vm_resume. Resume virtual machine. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusShutdownRequest(ProxmoxBaseModel):
    """Model for vm_shutdown. Shutdown virtual machine. This is similar to pressing the power button on a physical machine. This will send an ACPI event for the guest OS, which should then proceed to a clean shutdown. request."""
    force_stop: bool | None = Field(None, alias="forceStop", description='Make sure the VM stops.')
    keep_active: bool | None = Field(None, alias="keepActive", description='Do not deactivate storage volumes.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')

class PostNodesNodeQemuVmidStatusShutdownResponse(RootModel[StrictStr]):
    """Model for vm_shutdown. Shutdown virtual machine. This is similar to pressing the power button on a physical machine. This will send an ACPI event for the guest OS, which should then proceed to a clean shutdown. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusStartRequest(ProxmoxBaseModel):
    """Model for vm_start. Start virtual machine. request."""
    force_cpu: StrictStr | None = Field(None, alias="force-cpu", description="Override QEMU's -cpu argument with the given string.")
    machine: StrictStr | None = Field(None, description='Specify the QEMU machine.')
    migratedfrom: StrictStr | None = Field(None, description='The cluster node name.')
    migration_network: StrictStr | None = Field(None, description='CIDR of the (sub) network that is used for migration.')
    migration_type: StrictStr | None = Field(None, description='Migration traffic is encrypted using an SSH tunnel by default. On secure, completely private networks this can be disabled to increase performance.')
    nets_host_mtu: StrictStr | None = Field(None, alias="nets-host-mtu", description='Used for migration compat. List of VirtIO network devices and their effective host_mtu setting according to the QEMU object model on the source side of the migration. A value of 0 means that the host_mtu parameter is to be avoided for the corresponding device.')
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    stateuri: StrictStr | None = Field(None, description='Some command save/restore state from this location.')
    targetstorage: StrictStr | None = Field(None, description="Mapping from source to target storages. Providing only a single storage ID maps all source storages to that storage. Providing the special value '1' will map each source storage to itself.")
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')
    with_conntrack_state: bool | None = Field(None, alias="with-conntrack-state", description='Whether to migrate conntrack entries for running VMs.')

class PostNodesNodeQemuVmidStatusStartResponse(RootModel[StrictStr]):
    """Model for vm_start. Start virtual machine. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusStopRequest(ProxmoxBaseModel):
    """Model for vm_stop. Stop virtual machine. The qemu process will exit immediately. This is akin to pulling the power plug of a running computer and may damage the VM data. request."""
    keep_active: bool | None = Field(None, alias="keepActive", description='Do not deactivate storage volumes.')
    migratedfrom: StrictStr | None = Field(None, description='The cluster node name.')
    overrule_shutdown: bool | None = Field(None, alias="overrule-shutdown", description="Try to abort active 'qmshutdown' tasks before stopping.")
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    timeout: int | None = Field(None, description='Wait maximal timeout seconds.')

class PostNodesNodeQemuVmidStatusStopResponse(RootModel[StrictStr]):
    """Model for vm_stop. Stop virtual machine. The qemu process will exit immediately. This is akin to pulling the power plug of a running computer and may damage the VM data. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidStatusSuspendRequest(ProxmoxBaseModel):
    """Model for vm_suspend. Suspend virtual machine. request."""
    skiplock: bool | None = Field(None, description='Ignore locks - only root is allowed to use this option.')
    statestorage: StrictStr | None = Field(None, description='The storage for the VM state')
    todisk: bool | None = Field(None, description='If set, suspends the VM to disk. Will be resumed on next VM start.')

class PostNodesNodeQemuVmidStatusSuspendResponse(RootModel[StrictStr]):
    """Model for vm_suspend. Suspend virtual machine. response."""
    root: StrictStr = Field(...)

class PostNodesNodeQemuVmidTemplateRequest(ProxmoxBaseModel):
    """Model for template. Create a Template. request."""
    disk: StrictStr | None = Field(None, description='If you want to convert only 1 disk to base image.')

class PostNodesNodeQemuVmidTemplateResponse(RootModel[StrictStr]):
    """Model for template. Create a Template. response."""
    root: StrictStr = Field(..., description='the task ID.')

class PostNodesNodeQemuVmidTermproxyRequest(ProxmoxBaseModel):
    """Model for termproxy. Creates a TCP proxy connections. request."""
    serial: StrictStr | None = Field(None, description='opens a serial terminal (defaults to display)')

class PostNodesNodeQemuVmidTermproxyResponse(ProxmoxBaseModel):
    """Model for termproxy. Creates a TCP proxy connections. response."""
    port: int = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class PutNodesNodeQemuVmidUnlinkRequest(ProxmoxBaseModel):
    """Model for unlink. Unlink/delete disk images. request."""
    force: bool | None = Field(None, description="Force physical removal. Without this, we simple remove the disk from the config file and create an additional configuration entry called 'unused[n]', which contains the volume ID. Unlink of unused[n] always cause physical removal.")
    idlist: StrictStr = Field(..., description='A list of disk IDs you want to delete.')

class PutNodesNodeQemuVmidUnlinkResponse(RootModel[None]):
    """Model for unlink. Unlink/delete disk images. response."""
    root: None = Field(...)

class PostNodesNodeQemuVmidVncproxyRequest(ProxmoxBaseModel):
    """Model for vncproxy. Creates a TCP VNC proxy connections. request."""
    generate_password: bool | None = Field(None, alias="generate-password", description='Deprecated, do not use. Password is generated when required.')
    websocket: bool | None = Field(None, description='Prepare for websocket upgrade (only required when using serial terminal, otherwise upgrade is always possible).')

class PostNodesNodeQemuVmidVncproxyResponse(ProxmoxBaseModel):
    """Model for vncproxy. Creates a TCP VNC proxy connections. response."""
    cert: StrictStr = Field(...)
    password: StrictStr | None = Field(None, description="Password used for authentication within the VNC protocol. Consists of printable ASCII characters ('!' .. '~').")
    port: int = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class GetNodesNodeQemuVmidVncwebsocketResponse(ProxmoxBaseModel):
    """Model for vncwebsocket. Opens a websocket for VNC traffic. response."""
    port: StrictStr = Field(...)

class GetNodesNodeQueryOciRepoTagsResponse(RootModel[list[StrictStr]]):
    """Model for query_oci_repo_tags. List all tags for an OCI repository reference. response."""
    root: list[StrictStr] = Field(...)

class GetNodesNodeQueryUrlMetadataResponse(ProxmoxBaseModel):
    """Model for query_url_metadata. Query metadata of an URL: file size, file name and mime type. response."""
    filename: StrictStr | None = Field(None)
    mimetype: StrictStr | None = Field(None)
    size: int | None = Field(None)

class GetNodesNodeReplicationResponseItem(ProxmoxBaseModel):
    """Model for status. List status of all replication jobs on this node. response."""
    id: StrictStr | None = Field(None)

class GetNodesNodeReplicationResponse(RootModel[list[GetNodesNodeReplicationResponseItem]]):
    """List of items. status. List status of all replication jobs on this node. response."""
    root: list[GetNodesNodeReplicationResponseItem] = Field(...)

class GetNodesNodeReplicationIdResponse(RootModel[list[dict[str, object]]]):
    """Model for index. Directory index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeReplicationIdLogResponseItem(ProxmoxBaseModel):
    """Model for read_job_log. Read replication job log. response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeReplicationIdLogResponse(RootModel[list[GetNodesNodeReplicationIdLogResponseItem]]):
    """List of items. read_job_log. Read replication job log. response."""
    root: list[GetNodesNodeReplicationIdLogResponseItem] = Field(...)

class PostNodesNodeReplicationIdScheduleNowResponse(RootModel[StrictStr]):
    """Model for schedule_now. Schedule replication job to start as soon as possible. response."""
    root: StrictStr = Field(...)

class GetNodesNodeReplicationIdStatusResponse(RootModel[dict[str, object]]):
    """Model for job_status. Get replication job status. response."""
    root: dict[str, object] = Field(...)

class GetNodesNodeReportResponse(RootModel[StrictStr]):
    """Model for report. Gather various systems information about a node response."""
    root: StrictStr = Field(...)

class GetNodesNodeRrdResponse(ProxmoxBaseModel):
    """Model for rrd. Read node RRD statistics (returns PNG) response."""
    filename: StrictStr = Field(...)

class GetNodesNodeRrddataResponse(RootModel[list[dict[str, object]]]):
    """Model for rrddata. Read node RRD statistics response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeScanResponseItem(ProxmoxBaseModel):
    """Model for index. Index of available scan methods response."""
    method: StrictStr | None = Field(None)

class GetNodesNodeScanResponse(RootModel[list[GetNodesNodeScanResponseItem]]):
    """List of items. index. Index of available scan methods response."""
    root: list[GetNodesNodeScanResponseItem] = Field(...)

class GetNodesNodeScanCifsResponseItem(ProxmoxBaseModel):
    """Model for cifsscan. Scan remote CIFS server. response."""
    description: StrictStr | None = Field(None, description='Descriptive text from server.')
    share: StrictStr | None = Field(None, description='The cifs share name.')

class GetNodesNodeScanCifsResponse(RootModel[list[GetNodesNodeScanCifsResponseItem]]):
    """List of items. cifsscan. Scan remote CIFS server. response."""
    root: list[GetNodesNodeScanCifsResponseItem] = Field(...)

class GetNodesNodeScanIscsiResponseItem(ProxmoxBaseModel):
    """Model for iscsiscan. Scan remote iSCSI server. response."""
    portal: StrictStr | None = Field(None, description='The iSCSI portal name.')
    target: StrictStr | None = Field(None, description='The iSCSI target name.')

class GetNodesNodeScanIscsiResponse(RootModel[list[GetNodesNodeScanIscsiResponseItem]]):
    """List of items. iscsiscan. Scan remote iSCSI server. response."""
    root: list[GetNodesNodeScanIscsiResponseItem] = Field(...)

class GetNodesNodeScanLvmResponseItem(ProxmoxBaseModel):
    """Model for lvmscan. List local LVM volume groups. response."""
    vg: StrictStr | None = Field(None, description='The LVM logical volume group name.')

class GetNodesNodeScanLvmResponse(RootModel[list[GetNodesNodeScanLvmResponseItem]]):
    """List of items. lvmscan. List local LVM volume groups. response."""
    root: list[GetNodesNodeScanLvmResponseItem] = Field(...)

class GetNodesNodeScanLvmthinResponseItem(ProxmoxBaseModel):
    """Model for lvmthinscan. List local LVM Thin Pools. response."""
    lv: StrictStr | None = Field(None, description='The LVM Thin Pool name (LVM logical volume).')

class GetNodesNodeScanLvmthinResponse(RootModel[list[GetNodesNodeScanLvmthinResponseItem]]):
    """List of items. lvmthinscan. List local LVM Thin Pools. response."""
    root: list[GetNodesNodeScanLvmthinResponseItem] = Field(...)

class GetNodesNodeScanNfsResponseItem(ProxmoxBaseModel):
    """Model for nfsscan. Scan remote NFS server. response."""
    options: StrictStr | None = Field(None, description='NFS export options.')
    path: StrictStr | None = Field(None, description='The exported path.')

class GetNodesNodeScanNfsResponse(RootModel[list[GetNodesNodeScanNfsResponseItem]]):
    """List of items. nfsscan. Scan remote NFS server. response."""
    root: list[GetNodesNodeScanNfsResponseItem] = Field(...)

class GetNodesNodeScanPbsResponseItem(ProxmoxBaseModel):
    """Model for pbsscan. Scan remote Proxmox Backup Server. response."""
    comment: StrictStr | None = Field(None, description='Comment from server.')
    store: StrictStr | None = Field(None, description='The datastore name.')

class GetNodesNodeScanPbsResponse(RootModel[list[GetNodesNodeScanPbsResponseItem]]):
    """List of items. pbsscan. Scan remote Proxmox Backup Server. response."""
    root: list[GetNodesNodeScanPbsResponseItem] = Field(...)

class GetNodesNodeScanZfsResponseItem(ProxmoxBaseModel):
    """Model for zfsscan. Scan zfs pool list on local node. response."""
    pool: StrictStr | None = Field(None, description='ZFS pool name.')

class GetNodesNodeScanZfsResponse(RootModel[list[GetNodesNodeScanZfsResponseItem]]):
    """List of items. zfsscan. Scan zfs pool list on local node. response."""
    root: list[GetNodesNodeScanZfsResponseItem] = Field(...)

class GetNodesNodeSdnResponse(RootModel[list[dict[str, object]]]):
    """Model for sdnindex. SDN index. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeSdnFabricsFabricResponseItem(ProxmoxBaseModel):
    """Model for diridx. Directory index for SDN fabric status. response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeSdnFabricsFabricResponse(RootModel[list[GetNodesNodeSdnFabricsFabricResponseItem]]):
    """List of items. diridx. Directory index for SDN fabric status. response."""
    root: list[GetNodesNodeSdnFabricsFabricResponseItem] = Field(...)

class GetNodesNodeSdnFabricsFabricInterfacesResponseItem(ProxmoxBaseModel):
    """Model for interfaces. Get all interfaces for a fabric. response."""
    name: StrictStr | None = Field(None, description='The name of the network interface.')
    state: StrictStr | None = Field(None, description='The current state of the interface.')
    type: StrictStr | None = Field(None, description='The type of this interface in the fabric (e.g. Point-to-Point, Broadcast, ..).')

class GetNodesNodeSdnFabricsFabricInterfacesResponse(RootModel[list[GetNodesNodeSdnFabricsFabricInterfacesResponseItem]]):
    """List of items. interfaces. Get all interfaces for a fabric. response."""
    root: list[GetNodesNodeSdnFabricsFabricInterfacesResponseItem] = Field(...)

class GetNodesNodeSdnFabricsFabricNeighborsResponseItem(ProxmoxBaseModel):
    """Model for neighbors. Get all neighbors for a fabric. response."""
    neighbor: StrictStr | None = Field(None, description='The IP or hostname of the neighbor.')
    status: StrictStr | None = Field(None, description='The status of the neighbor, as returned by FRR.')
    uptime: StrictStr | None = Field(None, description='The uptime of this neighbor, as returned by FRR (e.g. 8h24m12s).')

class GetNodesNodeSdnFabricsFabricNeighborsResponse(RootModel[list[GetNodesNodeSdnFabricsFabricNeighborsResponseItem]]):
    """List of items. neighbors. Get all neighbors for a fabric. response."""
    root: list[GetNodesNodeSdnFabricsFabricNeighborsResponseItem] = Field(...)

class GetNodesNodeSdnFabricsFabricRoutesResponseItem(ProxmoxBaseModel):
    """Model for routes. Get all routes for a fabric. response."""
    route: StrictStr | None = Field(None, description='The CIDR block for this routing table entry.')
    via: list[StrictStr] | None = Field(None, description='A list of nexthops for that route.')

class GetNodesNodeSdnFabricsFabricRoutesResponse(RootModel[list[GetNodesNodeSdnFabricsFabricRoutesResponseItem]]):
    """List of items. routes. Get all routes for a fabric. response."""
    root: list[GetNodesNodeSdnFabricsFabricRoutesResponseItem] = Field(...)

class GetNodesNodeSdnVnetsVnetResponseItem(ProxmoxBaseModel):
    """Model for diridx. None response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeSdnVnetsVnetResponse(RootModel[list[GetNodesNodeSdnVnetsVnetResponseItem]]):
    """List of items. diridx. None response."""
    root: list[GetNodesNodeSdnVnetsVnetResponseItem] = Field(...)

class GetNodesNodeSdnVnetsVnetMacVrfResponseItem(ProxmoxBaseModel):
    """Model for mac-vrf. Get the MAC VRF for a VNet in an EVPN zone. response."""
    ip: StrictStr | None = Field(None, description='The IP address of the MAC VRF entry.')
    mac: StrictStr | None = Field(None, description='The MAC address of the MAC VRF entry.')
    nexthop: StrictStr | None = Field(None, description='The IP address of the nexthop.')

class GetNodesNodeSdnVnetsVnetMacVrfResponse(RootModel[list[GetNodesNodeSdnVnetsVnetMacVrfResponseItem]]):
    """List of items. mac-vrf. Get the MAC VRF for a VNet in an EVPN zone. response."""
    root: list[GetNodesNodeSdnVnetsVnetMacVrfResponseItem] = Field(..., description='All routes from the MAC VRF that this node self-originates or has learned via BGP.')

class GetNodesNodeSdnZonesResponseItem(ProxmoxBaseModel):
    """Model for index. Get status for all zones. response."""
    status: StrictStr | None = Field(None, description='Status of zone')
    zone: StrictStr | None = Field(None, description='The SDN zone object identifier.')

class GetNodesNodeSdnZonesResponse(RootModel[list[GetNodesNodeSdnZonesResponseItem]]):
    """List of items. index. Get status for all zones. response."""
    root: list[GetNodesNodeSdnZonesResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneResponseItem(ProxmoxBaseModel):
    """Model for diridx. Directory index for SDN zone status. response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeSdnZonesZoneResponse(RootModel[list[GetNodesNodeSdnZonesZoneResponseItem]]):
    """List of items. diridx. Directory index for SDN zone status. response."""
    root: list[GetNodesNodeSdnZonesZoneResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneBridgesResponseItem(ProxmoxBaseModel):
    """Model for bridges. Get a list of all bridges (vnets) that are part of a zone, as well as the ports that are members of that bridge. response."""
    name: StrictStr | None = Field(None, description='Name of the bridge.')
    ports: list[dict[str, object]] | None = Field(None, description='All ports that are members of the bridge')
    vlan_filtering: StrictStr | None = Field(None, description='Whether VLAN filtering is enabled for this bridge (= VLAN-aware).')

class GetNodesNodeSdnZonesZoneBridgesResponse(RootModel[list[GetNodesNodeSdnZonesZoneBridgesResponseItem]]):
    """List of items. bridges. Get a list of all bridges (vnets) that are part of a zone, as well as the ports that are members of that bridge. response."""
    root: list[GetNodesNodeSdnZonesZoneBridgesResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneContentResponseItem(ProxmoxBaseModel):
    """Model for index. List zone content. response."""
    status: StrictStr | None = Field(None, description='Status.')
    statusmsg: StrictStr | None = Field(None, description='Status details')
    vnet: StrictStr | None = Field(None, description='Vnet identifier.')

class GetNodesNodeSdnZonesZoneContentResponse(RootModel[list[GetNodesNodeSdnZonesZoneContentResponseItem]]):
    """List of items. index. List zone content. response."""
    root: list[GetNodesNodeSdnZonesZoneContentResponseItem] = Field(...)

class GetNodesNodeSdnZonesZoneIpVrfResponseItem(ProxmoxBaseModel):
    """Model for ip-vrf. Get the IP VRF of an EVPN zone. response."""
    ip: StrictStr | None = Field(None, description='The CIDR of the route table entry.')
    metric: int | None = Field(None, description="This route's metric.")
    nexthops: list[StrictStr] | None = Field(None, description='A list of nexthops for the route table entry.')
    protocol: StrictStr | None = Field(None, description='The protocol where this route was learned from (e.g. BGP).')

class GetNodesNodeSdnZonesZoneIpVrfResponse(RootModel[list[GetNodesNodeSdnZonesZoneIpVrfResponseItem]]):
    """List of items. ip-vrf. Get the IP VRF of an EVPN zone. response."""
    root: list[GetNodesNodeSdnZonesZoneIpVrfResponseItem] = Field(..., description='All entries in the VRF table of zone {zone} of the node.This does not include /32 routes for guests on this host,since they are handled via the respective vnet bridge directly.')

class GetNodesNodeServicesResponseItem(ProxmoxBaseModel):
    """Model for index. Service list. response."""
    active_state: StrictStr | None = Field(None, alias="active-state", description='Current state of the service process (systemd ActiveState).')
    desc: StrictStr | None = Field(None, description='Description of the service.')
    name: StrictStr | None = Field(None, description='Short identifier for the service (e.g., "pveproxy").')
    service: StrictStr | None = Field(None, description='Systemd unit name (e.g., pveproxy).')
    state: StrictStr | None = Field(None, description='Execution status of the service (systemd SubState).')
    unit_state: StrictStr | None = Field(None, alias="unit-state", description='Whether the service is enabled (systemd UnitFileState).')

class GetNodesNodeServicesResponse(RootModel[list[GetNodesNodeServicesResponseItem]]):
    """List of items. index. Service list. response."""
    root: list[GetNodesNodeServicesResponseItem] = Field(...)

class GetNodesNodeServicesServiceResponseItem(ProxmoxBaseModel):
    """Model for srvcmdidx. Directory index response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeServicesServiceResponse(RootModel[list[GetNodesNodeServicesServiceResponseItem]]):
    """List of items. srvcmdidx. Directory index response."""
    root: list[GetNodesNodeServicesServiceResponseItem] = Field(...)

class PostNodesNodeServicesServiceReloadResponse(RootModel[StrictStr]):
    """Model for service_reload. Reload service. Falls back to restart if service cannot be reloaded. response."""
    root: StrictStr = Field(...)

class PostNodesNodeServicesServiceRestartResponse(RootModel[StrictStr]):
    """Model for service_restart. Hard restart service. Use reload if you want to reduce interruptions. response."""
    root: StrictStr = Field(...)

class PostNodesNodeServicesServiceStartResponse(RootModel[StrictStr]):
    """Model for service_start. Start service. response."""
    root: StrictStr = Field(...)

class GetNodesNodeServicesServiceStateResponse(ProxmoxBaseModel):
    """Model for service_state. Read service properties response."""
    active_state: StrictStr = Field(..., alias="active-state", description='Current state of the service process (systemd ActiveState).')
    desc: StrictStr = Field(..., description='Description of the service.')
    name: StrictStr = Field(..., description='Short identifier for the service (e.g., "pveproxy").')
    service: StrictStr = Field(..., description='Systemd unit name (e.g., pveproxy).')
    state: StrictStr = Field(..., description='Execution status of the service (systemd SubState).')
    unit_state: StrictStr = Field(..., alias="unit-state", description='Whether the service is enabled (systemd UnitFileState).')

class PostNodesNodeServicesServiceStopResponse(RootModel[StrictStr]):
    """Model for service_stop. Stop service. response."""
    root: StrictStr = Field(...)

class PostNodesNodeSpiceshellRequest(ProxmoxBaseModel):
    """Model for spiceshell. Creates a SPICE shell. request."""
    cmd: StrictStr | None = Field(None, description="Run specific command or default to login (requires 'root@pam')")
    cmd_opts: StrictStr | None = Field(None, alias="cmd-opts", description='Add parameters to a command. Encoded as null terminated strings.')
    proxy: StrictStr | None = Field(None, description="SPICE proxy server. This can be used by the client to specify the proxy server. All nodes in a cluster runs 'spiceproxy', so it is up to the client to choose one. By default, we return the node where the VM is currently running. As reasonable setting is to use same node you use to connect to the API (This is window.location.hostname for the JS GUI).")

class PostNodesNodeSpiceshellResponse(ProxmoxBaseModel):
    """Model for spiceshell. Creates a SPICE shell. response."""
    host: StrictStr = Field(...)
    password: StrictStr = Field(...)
    proxy: StrictStr = Field(...)
    tls_port: int = Field(..., alias="tls-port")
    type: StrictStr = Field(...)

class PostNodesNodeStartallRequest(ProxmoxBaseModel):
    """Model for startall. Start all VMs and containers located on this node (by default only those with onboot=1). request."""
    force: bool | None = Field(None, description="Issue start command even if virtual guest have 'onboot' not set or set to off.")
    max_workers: int | None = Field(None, alias="max-workers", description="Defines the maximum number of tasks running concurrently. If not set, uses 'max_workers' from datacenter.cfg, and if that's not set, the available CPU threads, clamped to a maximum of 8, are used.")
    vms: StrictStr | None = Field(None, description='Only consider guests from this comma separated list of VMIDs.')

class PostNodesNodeStartallResponse(RootModel[StrictStr]):
    """Model for startall. Start all VMs and containers located on this node (by default only those with onboot=1). response."""
    root: StrictStr = Field(...)

class GetNodesNodeStatusResponse(ProxmoxBaseModel):
    """Model for status. Read node status response."""
    boot_info: dict[str, object] = Field(..., alias="boot-info", description='Meta-information about the boot mode.')
    cpu: float = Field(..., description='The current cpu usage.')
    cpuinfo: dict[str, object] = Field(...)
    current_kernel: dict[str, object] = Field(..., alias="current-kernel", description='Meta-information about the currently booted kernel of this node.')
    loadavg: list[StrictStr] = Field(..., description='An array of load avg for 1, 5 and 15 minutes respectively.')
    memory: dict[str, object] = Field(...)
    pveversion: StrictStr = Field(..., description='The PVE version string.')
    rootfs: dict[str, object] = Field(...)

class PostNodesNodeStatusRequest(ProxmoxBaseModel):
    """Model for node_cmd. Reboot or shutdown a node. request."""
    command: StrictStr = Field(..., description='Specify the command.')

class PostNodesNodeStatusResponse(RootModel[None]):
    """Model for node_cmd. Reboot or shutdown a node. response."""
    root: None = Field(...)

class PostNodesNodeStopallRequest(ProxmoxBaseModel):
    """Model for stopall. Stop all VMs and Containers. request."""
    force_stop: bool | None = Field(None, alias="force-stop", description='Force a hard-stop after the timeout.')
    max_workers: int | None = Field(None, alias="max-workers", description="Defines the maximum number of tasks running concurrently. If  not set, uses 'max_workers' from datacenter.cfg, and if that's not set, the available CPU threads, clamped to a maximum of 8, are used.")
    timeout: int | None = Field(None, description='Timeout for each guest shutdown task. Depending on `force-stop`, the shutdown gets then simply aborted or a hard-stop is forced.')
    vms: StrictStr | None = Field(None, description='Only consider Guests with these IDs.')

class PostNodesNodeStopallResponse(RootModel[StrictStr]):
    """Model for stopall. Stop all VMs and Containers. response."""
    root: StrictStr = Field(...)

class GetNodesNodeStorageResponseItem(ProxmoxBaseModel):
    """Model for index. Get status for all datastores. response."""
    active: bool | None = Field(None, description='Set when storage is accessible.')
    avail: int | None = Field(None, description='Available storage space in bytes.')
    content: StrictStr | None = Field(None, description='Allowed storage content types.')
    enabled: bool | None = Field(None, description='Set when storage is enabled (not disabled).')
    formats: dict[str, object] | None = Field(None, description="Lists the supported and default format. Use 'formats' instead. Only included if 'format' parameter is set.")
    select_existing: bool | None = Field(None, description="Instead of creating new volumes, one must select one that is already existing. Only included if 'format' parameter is set.")
    shared: bool | None = Field(None, description='Shared flag from storage configuration.')
    storage: StrictStr | None = Field(None, description='The storage identifier.')
    total: int | None = Field(None, description='Total storage space in bytes.')
    type: StrictStr | None = Field(None, description='Storage type.')
    used: int | None = Field(None, description='Used storage space in bytes.')
    used_fraction: float | None = Field(None, description='Used fraction (used/total).')

class GetNodesNodeStorageResponse(RootModel[list[GetNodesNodeStorageResponseItem]]):
    """List of items. index. Get status for all datastores. response."""
    root: list[GetNodesNodeStorageResponseItem] = Field(...)

class GetNodesNodeStorageStorageResponseItem(ProxmoxBaseModel):
    """Model for diridx. None response."""
    subdir: StrictStr | None = Field(None)

class GetNodesNodeStorageStorageResponse(RootModel[list[GetNodesNodeStorageStorageResponseItem]]):
    """List of items. diridx. None response."""
    root: list[GetNodesNodeStorageStorageResponseItem] = Field(...)

class GetNodesNodeStorageStorageContentResponseItem(ProxmoxBaseModel):
    """Model for index. List storage content. response."""
    approximate_size: int | None = Field(None, alias="approximate-size", description="Approximate volume size in bytes. Present instead of 'size' for storages where determining the exact size has technical limitations. Will typically be an upper bound on the actual size, but the exact semantics depend on the storage plugin.")
    ctime: int | None = Field(None, description='Creation time (seconds since the UNIX Epoch).')
    encrypted: StrictStr | None = Field(None, description="If whole backup is encrypted, value is the fingerprint or '1'  if encrypted. Only useful for the Proxmox Backup Server storage type.")
    format: StrictStr | None = Field(None, description="Format identifier ('raw', 'qcow2', 'subvol', 'iso', 'tgz' ...)")
    notes: StrictStr | None = Field(None, description='Optional notes. If they contain multiple lines, only the first one is returned here.')
    parent: StrictStr | None = Field(None, description='Volume identifier of parent (for linked cloned).')
    protected: bool | None = Field(None, description='Protection status. Currently only supported for backups.')
    size: int | None = Field(None, description='Volume size in bytes.')
    used: int | None = Field(None, description='Used space. Please note that most storage plugins do not report anything useful here.')
    verification: dict[str, object] | None = Field(None, description='Last backup verification result, only useful for PBS storages.')
    vmid: int | None = Field(None, description='Associated Owner VMID.')
    volid: StrictStr | None = Field(None, description='Volume identifier.')

class GetNodesNodeStorageStorageContentResponse(RootModel[list[GetNodesNodeStorageStorageContentResponseItem]]):
    """List of items. index. List storage content. response."""
    root: list[GetNodesNodeStorageStorageContentResponseItem] = Field(...)

class PostNodesNodeStorageStorageContentRequest(ProxmoxBaseModel):
    """Model for create. Allocate disk images. request."""
    filename: StrictStr = Field(..., description='The name of the file to create.')
    format: StrictStr | None = Field(None, description='Format of the image.')
    size: StrictStr = Field(..., description="Size in kilobyte (1024 bytes). Optional suffixes 'M' (megabyte, 1024K) and 'G' (gigabyte, 1024M)")
    vmid: int = Field(..., description='Specify owner VM')

class PostNodesNodeStorageStorageContentResponse(RootModel[StrictStr]):
    """Model for create. Allocate disk images. response."""
    root: StrictStr = Field(..., description='Volume identifier')

class DeleteNodesNodeStorageStorageContentVolumeRequest(ProxmoxBaseModel):
    """Model for delete. Delete volume request."""
    delay: int | None = Field(None, description="Time to wait for the task to finish. We return 'null' if the task finish within that time.")

class DeleteNodesNodeStorageStorageContentVolumeResponse(RootModel[StrictStr]):
    """Model for delete. Delete volume response."""
    root: StrictStr = Field(...)

class GetNodesNodeStorageStorageContentVolumeResponse(ProxmoxBaseModel):
    """Model for info. Get volume attributes response."""
    format: StrictStr = Field(..., description="Format identifier ('raw', 'qcow2', 'subvol', 'iso', 'tgz' ...)")
    notes: StrictStr | None = Field(None, description='Optional notes.')
    path: StrictStr = Field(..., description='The Path')
    protected: bool | None = Field(None, description='Protection status. Currently only supported for backups.')
    size: int = Field(..., description='Volume size in bytes.')
    used: int = Field(..., description='Used space. Please note that most storage plugins do not report anything useful here.')

class PostNodesNodeStorageStorageContentVolumeRequest(ProxmoxBaseModel):
    """Model for copy. Copy a volume. This is experimental code - do not use. request."""
    target: StrictStr = Field(..., description='Target volume identifier')
    target_node: StrictStr | None = Field(None, description='Target node. Default is local node.')

class PostNodesNodeStorageStorageContentVolumeResponse(RootModel[StrictStr]):
    """Model for copy. Copy a volume. This is experimental code - do not use. response."""
    root: StrictStr = Field(...)

class PutNodesNodeStorageStorageContentVolumeRequest(ProxmoxBaseModel):
    """Model for updateattributes. Update volume attributes request."""
    notes: StrictStr | None = Field(None, description='The new notes.')
    protected: bool | None = Field(None, description='Protection status. Currently only supported for backups.')

class PutNodesNodeStorageStorageContentVolumeResponse(RootModel[None]):
    """Model for updateattributes. Update volume attributes response."""
    root: None = Field(...)

class PostNodesNodeStorageStorageDownloadUrlRequest(ProxmoxBaseModel):
    """Model for download_url. Download templates, ISO images, OVAs and VM images by using an URL. request."""
    checksum: StrictStr | None = Field(None, description='The expected checksum of the file.')
    checksum_algorithm: StrictStr | None = Field(None, alias="checksum-algorithm", description='The algorithm to calculate the checksum of the file.')
    compression: StrictStr | None = Field(None, description='Decompress the downloaded file using the specified compression algorithm.')
    content: StrictStr = Field(..., description='Content type.')
    filename: StrictStr = Field(..., description='The name of the file to create. Caution: This will be normalized!')
    url: StrictStr = Field(..., description='The URL to download the file from.')
    verify_certificates: bool | None = Field(None, alias="verify-certificates", description='If false, no SSL/TLS certificates will be verified.')

class PostNodesNodeStorageStorageDownloadUrlResponse(RootModel[StrictStr]):
    """Model for download_url. Download templates, ISO images, OVAs and VM images by using an URL. response."""
    root: StrictStr = Field(...)

class GetNodesNodeStorageStorageFileRestoreDownloadResponse(RootModel[object]):
    """Model for download. Extract a file or directory (as zip archive) from a PBS backup. response."""
    root: object = Field(...)

class GetNodesNodeStorageStorageFileRestoreListResponseItem(ProxmoxBaseModel):
    """Model for list. List files and directories for single file restore under the given path. response."""
    filepath: StrictStr | None = Field(None, description='base64 path of the current entry')
    leaf: bool | None = Field(None, description='If this entry is a leaf in the directory graph.')
    mtime: int | None = Field(None, description='Entry last-modified time (unix timestamp).')
    size: int | None = Field(None, description='Entry file size.')
    text: StrictStr | None = Field(None, description='Entry display text.')
    type: StrictStr | None = Field(None, description='Entry type.')

class GetNodesNodeStorageStorageFileRestoreListResponse(RootModel[list[GetNodesNodeStorageStorageFileRestoreListResponseItem]]):
    """List of items. list. List files and directories for single file restore under the given path. response."""
    root: list[GetNodesNodeStorageStorageFileRestoreListResponseItem] = Field(...)

class GetNodesNodeStorageStorageIdentityResponse(ProxmoxBaseModel):
    """Model for identity. Return identity information for this storage instance. response."""
    id: StrictStr = Field(..., description='Unique identifier for this storage instance. The exact format and semantics depend on the storage plugin type.')
    type: StrictStr = Field(..., description='The type of the storage.')

class GetNodesNodeStorageStorageImportMetadataResponse(ProxmoxBaseModel):
    """Model for get_import_metadata. Get the base parameters for creating a guest which imports data from a foreign importable guest, like an ESXi VM response."""
    create_args: dict[str, object] = Field(..., alias="create-args", description='Parameters which can be used in a call to create a VM or container.')
    disks: dict[str, object] | None = Field(None, description='Recognised disk volumes as `$bus$id` => `$storeid:$path` map.')
    net: dict[str, object] | None = Field(None, description='Recognised network interfaces as `net$id` => { ...params } object.')
    source: StrictStr = Field(..., description='The type of the import-source of this guest volume.')
    type: StrictStr = Field(..., description='The type of guest this is going to produce.')
    warnings: list[dict[str, object]] | None = Field(None, description='List of known issues that can affect the import of a guest. Note that lack of warning does not imply that there cannot be any problems.')

class PostNodesNodeStorageStorageOciRegistryPullRequest(ProxmoxBaseModel):
    """Model for oci_registry_pull. Pull an OCI image from a registry. request."""
    filename: StrictStr | None = Field(None, description='Custom destination file name of the OCI image. Caution: This will be normalized!')
    reference: StrictStr = Field(..., description='The reference to the OCI image to download.')

class PostNodesNodeStorageStorageOciRegistryPullResponse(RootModel[StrictStr]):
    """Model for oci_registry_pull. Pull an OCI image from a registry. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeStorageStoragePrunebackupsRequest(ProxmoxBaseModel):
    """Model for delete. Prune backups. Only those using the standard naming scheme are considered. request."""
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    type: StrictStr | None = Field(None, description="Either 'qemu' or 'lxc'. Only consider backups for guests of this type.")
    vmid: int | None = Field(None, description='Only prune backups for this VM.')

class DeleteNodesNodeStorageStoragePrunebackupsResponse(RootModel[StrictStr]):
    """Model for delete. Prune backups. Only those using the standard naming scheme are considered. response."""
    root: StrictStr = Field(...)

class GetNodesNodeStorageStoragePrunebackupsResponseItem(ProxmoxBaseModel):
    """Model for dryrun. Get prune information for backups. NOTE: this is only a preview and might not be what a subsequent prune call does if backups are removed/added in the meantime. response."""
    ctime: int | None = Field(None, description='Creation time of the backup (seconds since the UNIX epoch).')
    mark: StrictStr | None = Field(None, description="Whether the backup would be kept or removed. Backups that are protected or don't use the standard naming scheme are not removed.")
    type: StrictStr | None = Field(None, description="One of 'qemu', 'lxc', 'openvz' or 'unknown'.")
    vmid: int | None = Field(None, description='The VM the backup belongs to.')
    volid: StrictStr | None = Field(None, description='Backup volume ID.')

class GetNodesNodeStorageStoragePrunebackupsResponse(RootModel[list[GetNodesNodeStorageStoragePrunebackupsResponseItem]]):
    """List of items. dryrun. Get prune information for backups. NOTE: this is only a preview and might not be what a subsequent prune call does if backups are removed/added in the meantime. response."""
    root: list[GetNodesNodeStorageStoragePrunebackupsResponseItem] = Field(...)

class GetNodesNodeStorageStorageRrdResponse(ProxmoxBaseModel):
    """Model for rrd. Read storage RRD statistics (returns PNG). response."""
    filename: StrictStr = Field(...)

class GetNodesNodeStorageStorageRrddataResponse(RootModel[list[dict[str, object]]]):
    """Model for rrddata. Read storage RRD statistics. response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeStorageStorageStatusResponse(ProxmoxBaseModel):
    """Model for read_status. Read storage status. response."""
    active: bool | None = Field(None, description='Set when storage is accessible.')
    avail: int | None = Field(None, description='Available storage space in bytes.')
    content: StrictStr = Field(..., description='Allowed storage content types.')
    enabled: bool | None = Field(None, description='Set when storage is enabled (not disabled).')
    shared: bool | None = Field(None, description='Shared flag from storage configuration.')
    total: int | None = Field(None, description='Total storage space in bytes.')
    type: StrictStr = Field(..., description='Storage type.')
    used: int | None = Field(None, description='Used storage space in bytes.')

class PostNodesNodeStorageStorageUploadRequest(ProxmoxBaseModel):
    """Model for upload. Upload templates, ISO images, OVAs and VM images. request."""
    checksum: StrictStr | None = Field(None, description='The expected checksum of the file.')
    checksum_algorithm: StrictStr | None = Field(None, alias="checksum-algorithm", description='The algorithm to calculate the checksum of the file.')
    content: StrictStr = Field(..., description='Content type.')
    filename: StrictStr = Field(..., description='The name of the file to create. Caution: This will be normalized!')
    tmpfilename: StrictStr | None = Field(None, description='The source file name. This parameter is usually set by the REST handler. You can only overwrite it when connecting to the trusted port on localhost.')

class PostNodesNodeStorageStorageUploadResponse(RootModel[StrictStr]):
    """Model for upload. Upload templates, ISO images, OVAs and VM images. response."""
    root: StrictStr = Field(...)

class DeleteNodesNodeSubscriptionResponse(RootModel[None]):
    """Model for delete. Delete subscription key of this node. response."""
    root: None = Field(...)

class GetNodesNodeSubscriptionResponse(ProxmoxBaseModel):
    """Model for get. Read subscription info. response."""
    checktime: int | None = Field(None, description='Timestamp of the last check done.')
    key: StrictStr | None = Field(None, description='The subscription key, if set and permitted to access.')
    level: StrictStr | None = Field(None, description='A short code for the subscription level.')
    message: StrictStr | None = Field(None, description='A more human readable status message.')
    nextduedate: StrictStr | None = Field(None, description='Next due date of the set subscription.')
    productname: StrictStr | None = Field(None, description='Human readable productname of the set subscription.')
    regdate: StrictStr | None = Field(None, description='Register date of the set subscription.')
    serverid: StrictStr | None = Field(None, description='The server ID, if permitted to access.')
    signature: StrictStr | None = Field(None, description='Signature for offline keys')
    sockets: int | None = Field(None, description='The number of sockets for this host.')
    status: StrictStr = Field(..., description='The current subscription status.')
    url: StrictStr | None = Field(None, description='URL to the web shop.')

class PostNodesNodeSubscriptionRequest(ProxmoxBaseModel):
    """Model for update. Update subscription info. request."""
    force: bool | None = Field(None, description='Always connect to server, even if local cache is still valid.')

class PostNodesNodeSubscriptionResponse(RootModel[None]):
    """Model for update. Update subscription info. response."""
    root: None = Field(...)

class PutNodesNodeSubscriptionRequest(ProxmoxBaseModel):
    """Model for set. Set subscription key. request."""
    key: StrictStr = Field(..., description='Proxmox VE subscription key')

class PutNodesNodeSubscriptionResponse(RootModel[None]):
    """Model for set. Set subscription key. response."""
    root: None = Field(...)

class PostNodesNodeSuspendallRequest(ProxmoxBaseModel):
    """Model for suspendall. Suspend all VMs. request."""
    max_workers: int | None = Field(None, alias="max-workers", description="Maximal number of parallel migration job. If not set, uses'max_workers' from datacenter.cfg, and if that's not set the available'\n                    .' CPU threads, clamped to a maximum of 8, are used.")
    vms: StrictStr | None = Field(None, description='Only consider Guests with these IDs.')

class PostNodesNodeSuspendallResponse(RootModel[StrictStr]):
    """Model for suspendall. Suspend all VMs. response."""
    root: StrictStr = Field(...)

class GetNodesNodeSyslogResponseItem(ProxmoxBaseModel):
    """Model for syslog. Read system log response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeSyslogResponse(RootModel[list[GetNodesNodeSyslogResponseItem]]):
    """List of items. syslog. Read system log response."""
    root: list[GetNodesNodeSyslogResponseItem] = Field(...)

class GetNodesNodeTasksResponseItem(ProxmoxBaseModel):
    """Model for node_tasks. Read task list for one node (finished tasks). response."""
    endtime: int | None = Field(None)
    id: StrictStr | None = Field(None)
    node: StrictStr | None = Field(None)
    pid: int | None = Field(None)
    pstart: int | None = Field(None)
    starttime: int | None = Field(None)
    status: StrictStr | None = Field(None)
    type: StrictStr | None = Field(None)
    upid: StrictStr | None = Field(None)
    user: StrictStr | None = Field(None)

class GetNodesNodeTasksResponse(RootModel[list[GetNodesNodeTasksResponseItem]]):
    """List of items. node_tasks. Read task list for one node (finished tasks). response."""
    root: list[GetNodesNodeTasksResponseItem] = Field(...)

class DeleteNodesNodeTasksUpidResponse(RootModel[None]):
    """Model for stop_task. Stop a task. response."""
    root: None = Field(...)

class GetNodesNodeTasksUpidResponse(RootModel[list[dict[str, object]]]):
    """Model for upid_index. None response."""
    root: list[dict[str, object]] = Field(...)

class GetNodesNodeTasksUpidLogResponseItem(ProxmoxBaseModel):
    """Model for read_task_log. Read task log. response."""
    n: int | None = Field(None, description='Line number')
    t: StrictStr | None = Field(None, description='Line text')

class GetNodesNodeTasksUpidLogResponse(RootModel[list[GetNodesNodeTasksUpidLogResponseItem]]):
    """List of items. read_task_log. Read task log. response."""
    root: list[GetNodesNodeTasksUpidLogResponseItem] = Field(...)

class GetNodesNodeTasksUpidStatusResponse(ProxmoxBaseModel):
    """Model for read_task_status. Read task status. response."""
    exitstatus: StrictStr | None = Field(None)
    id: StrictStr = Field(...)
    node: StrictStr = Field(...)
    pid: int = Field(...)
    pstart: int = Field(...)
    starttime: int = Field(...)
    status: StrictStr = Field(...)
    type: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class PostNodesNodeTermproxyRequest(ProxmoxBaseModel):
    """Model for termproxy. Creates a VNC Shell proxy. request."""
    cmd: StrictStr | None = Field(None, description="Run specific command or default to login (requires 'root@pam')")
    cmd_opts: StrictStr | None = Field(None, alias="cmd-opts", description='Add parameters to a command. Encoded as null terminated strings.')

class PostNodesNodeTermproxyResponse(ProxmoxBaseModel):
    """Model for termproxy. Creates a VNC Shell proxy. response."""
    port: int = Field(..., description='port used to bind termproxy to.')
    ticket: StrictStr = Field(..., description='VNC ticket used to verify websocket connection.')
    upid: StrictStr = Field(..., description='UPID for termproxy worker task.')
    user: StrictStr = Field(..., description='user/token that generated the VNC ticket in `ticket`.')

class GetNodesNodeTimeResponse(ProxmoxBaseModel):
    """Model for time. Read server time and time zone settings. response."""
    localtime: int = Field(..., description='Seconds since 1970-01-01 00:00:00 (local time)')
    time: int = Field(..., description='Seconds since 1970-01-01 00:00:00 UTC.')
    timezone: StrictStr = Field(..., description='Time zone')

class PutNodesNodeTimeRequest(ProxmoxBaseModel):
    """Model for set_timezone. Set time zone. request."""
    timezone: StrictStr = Field(..., description="Time zone. The file '/usr/share/zoneinfo/zone.tab' contains the list of valid names.")

class PutNodesNodeTimeResponse(RootModel[None]):
    """Model for set_timezone. Set time zone. response."""
    root: None = Field(...)

class GetNodesNodeVersionResponse(ProxmoxBaseModel):
    """Model for version. API version details response."""
    release: StrictStr = Field(..., description='The current installed Proxmox VE Release')
    repoid: StrictStr = Field(..., description='The short git commit hash ID from which this version was build')
    version: StrictStr = Field(..., description='The current installed pve-manager package version')

class PostNodesNodeVncshellRequest(ProxmoxBaseModel):
    """Model for vncshell. Creates a VNC Shell proxy. request."""
    cmd: StrictStr | None = Field(None, description="Run specific command or default to login (requires 'root@pam')")
    cmd_opts: StrictStr | None = Field(None, alias="cmd-opts", description='Add parameters to a command. Encoded as null terminated strings.')
    height: int | None = Field(None, description='sets the height of the console in pixels.')
    websocket: bool | None = Field(None, description='use websocket instead of standard vnc.')
    width: int | None = Field(None, description='sets the width of the console in pixels.')

class PostNodesNodeVncshellResponse(ProxmoxBaseModel):
    """Model for vncshell. Creates a VNC Shell proxy. response."""
    cert: StrictStr = Field(...)
    password: StrictStr | None = Field(None, description="Password used for authentication within the VNC protocol. Consists of printable ASCII characters ('!' .. '~').")
    port: int = Field(...)
    ticket: StrictStr = Field(...)
    upid: StrictStr = Field(...)
    user: StrictStr = Field(...)

class GetNodesNodeVncwebsocketResponse(ProxmoxBaseModel):
    """Model for vncwebsocket. Opens a websocket for VNC traffic. response."""
    port: StrictStr = Field(...)

class PostNodesNodeVzdumpRequest(ProxmoxBaseModel):
    """Model for vzdump. Create backup. request."""
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    compress: StrictStr | None = Field(None, description='Compress dump file.')
    dumpdir: StrictStr | None = Field(None, description='Store resulting files to specified directory.')
    exclude: StrictStr | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[StrictStr] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: StrictStr | None = Field(None, description='Options for backup fleecing (VM only).')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    job_id: StrictStr | None = Field(None, alias="job-id", description="The ID of the backup job. If set, the 'backup-job' metadata field of the backup notification will be set to this value. Only root@pam can set this parameter.")
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: StrictStr | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: StrictStr | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    mode: StrictStr | None = Field(None, description='Backup mode.')
    notes_template: StrictStr | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: StrictStr | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: StrictStr | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: StrictStr | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: StrictStr | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    script: StrictStr | None = Field(None, description='Use specified hook script.')
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stdout: bool | None = Field(None, description='Write tar to stdout, not to a file.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: StrictStr | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: StrictStr | None = Field(None, description='Store temporary files to specified directory.')
    vmid: StrictStr | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class PostNodesNodeVzdumpResponse(RootModel[StrictStr]):
    """Model for vzdump. Create backup. response."""
    root: StrictStr = Field(...)

class GetNodesNodeVzdumpDefaultsResponse(ProxmoxBaseModel):
    """Model for defaults. Get the currently configured vzdump defaults. response."""
    all: bool | None = Field(None, description='Backup all known guest systems on this host.')
    bwlimit: int | None = Field(None, description='Limit I/O bandwidth (in KiB/s).')
    compress: StrictStr | None = Field(None, description='Compress dump file.')
    dumpdir: StrictStr | None = Field(None, description='Store resulting files to specified directory.')
    exclude: StrictStr | None = Field(None, description='Exclude specified guest systems (assumes --all)')
    exclude_path: list[StrictStr] | None = Field(None, alias="exclude-path", description="Exclude certain files/directories (shell globs). Paths starting with '/' are anchored to the container's root, other paths match relative to each subdirectory.")
    fleecing: StrictStr | None = Field(None, description='Options for backup fleecing (VM only).')
    ionice: int | None = Field(None, description='Set IO priority when using the BFQ scheduler. For snapshot and suspend mode backups of VMs, this only affects the compressor. A value of 8 means the idle priority is used, otherwise the best-effort priority is used with the specified value.')
    lockwait: int | None = Field(None, description='Maximal time to wait for the global lock (minutes).')
    mailnotification: StrictStr | None = Field(None, description='Deprecated: use notification targets/matchers instead. Specify when to send a notification mail')
    mailto: StrictStr | None = Field(None, description='Deprecated: Use notification targets/matchers instead. Comma-separated list of email addresses or users that should receive email notifications.')
    mode: StrictStr | None = Field(None, description='Backup mode.')
    node: StrictStr | None = Field(None, description='Only run if executed on this node.')
    notes_template: StrictStr | None = Field(None, alias="notes-template", description="Template string for generating notes for the backup(s). It can contain variables which will be replaced by their values. Currently supported are {{cluster}}, {{guestname}}, {{node}}, and {{vmid}}, but more might be added in the future. Needs to be a single line, newline and backslash need to be escaped as '\\n' and '\\\\' respectively.")
    notification_mode: StrictStr | None = Field(None, alias="notification-mode", description="Determine which notification system to use. If set to 'legacy-sendmail', vzdump will consider the mailto/mailnotification parameters and send emails to the specified address(es) via the 'sendmail' command. If set to 'notification-system', a notification will be sent via PVE's notification system, and the mailto and mailnotification will be ignored. If set to 'auto' (default setting), an email will be sent if mailto is set, and the notification system will be used if not.")
    pbs_change_detection_mode: StrictStr | None = Field(None, alias="pbs-change-detection-mode", description='PBS mode used to detect file changes and switch encoding format for container backups.')
    performance: StrictStr | None = Field(None, description='Other performance-related settings.')
    pigz: int | None = Field(None, description='Use pigz instead of gzip when N>0. N=1 uses half of cores, N>1 uses N as thread count.')
    pool: StrictStr | None = Field(None, description='Backup all known guest systems included in the specified pool.')
    protected: bool | None = Field(None, description='If true, mark backup(s) as protected.')
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='Use these retention options instead of those from the storage configuration.')
    quiet: bool | None = Field(None, description='Be quiet.')
    remove: bool | None = Field(None, description="Prune older backups according to 'prune-backups'.")
    script: StrictStr | None = Field(None, description='Use specified hook script.')
    stdexcludes: bool | None = Field(None, description='Exclude temporary files and logs.')
    stop: bool | None = Field(None, description='Stop running backup jobs on this host.')
    stopwait: int | None = Field(None, description='Maximal time to wait until a guest system is stopped (minutes).')
    storage: StrictStr | None = Field(None, description='Store resulting file to this storage.')
    tmpdir: StrictStr | None = Field(None, description='Store temporary files to specified directory.')
    vmid: StrictStr | None = Field(None, description='The ID of the guest system you want to backup.')
    zstd: int | None = Field(None, description='Zstd threads. N=0 uses half of the available cores, if N is set to a value bigger than 0, N is used as thread count.')

class GetNodesNodeVzdumpExtractconfigResponse(RootModel[StrictStr]):
    """Model for extractconfig. Extract configuration from vzdump backup archive. response."""
    root: StrictStr = Field(...)

class PostNodesNodeWakeonlanResponse(RootModel[StrictStr]):
    """Model for wakeonlan. Try to wake a node via 'wake on LAN' network packet. response."""
    root: StrictStr = Field(..., description='MAC address used to assemble the WoL magic packet.')

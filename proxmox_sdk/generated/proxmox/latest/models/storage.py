"""Generated Pydantic v2 schemas for Proxmox route group 'storage'.

Do not edit by hand. Regenerate from the matching OpenAPI artifact.
"""

from __future__ import annotations

from typing import Annotated

from pydantic import AfterValidator, BaseModel, ConfigDict, Field, RootModel, StrictBool, StrictInt, StrictStr

GENERATED_FOR_PROXMOX_VERSION = "latest"
GENERATED_SOURCE_SHA256 = "83d00ff237bdfac0cb144eb603209f20654125dc40350c35447707fd330a0179"
GENERATED_AT = "2026-11-26T14:19:39.255287+00:00"


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')


def _allowed_ints(allowed: tuple[int, ...]) -> AfterValidator:
    def validate(value: int) -> int:
        if value not in allowed:
            raise ValueError('value is not an allowed schema member')
        return value

    return AfterValidator(validate)

class GetStorageResponseItem(ProxmoxBaseModel):
    """Model for index. Storage index. response."""
    storage: StrictStr | None = Field(None)

class GetStorageResponse(RootModel[list[GetStorageResponseItem]]):
    """List of items. index. Storage index. response."""
    root: list[GetStorageResponseItem] = Field(...)

class PostStorageRequest(ProxmoxBaseModel):
    """Model for create. Create a new storage. request."""
    base: StrictStr | None = Field(None, description='Volume ID of the base volume (automatically activated).')
    blocksize: StrictStr | None = Field(None, description='ZFS block size.')
    bwlimit: StrictStr | None = Field(None, description='Set I/O bandwidth limit for various operations (in KiB/s).')
    comstar_hg: StrictStr | None = Field(None, description='Host group for COMSTAR views.')
    comstar_tg: StrictStr | None = Field(None, description='Target group for COMSTAR views.')
    content: StrictStr | None = Field(None, description="Allowed content types.\n\nNOTE: the value 'rootdir' is used for Containers, and value 'images' for VMs. A storage can instead be restricted to some of their volume types: 'vm-vol' for the disks of VMs, 'vm-state' for the saved states of VMs, and 'ct-vol' for the volumes of Containers.\n")
    content_dirs: StrictStr | None = Field(None, alias="content-dirs", description='Overrides for default content type directories.')
    create_base_path: bool | None = Field(None, alias="create-base-path", description="Create the base directory if it doesn't exist.")
    create_subdirs: bool | None = Field(None, alias="create-subdirs", description='Populate the base directory with the default structure.')
    data_pool: StrictStr | None = Field(None, alias="data-pool", description='Data pool name for erasure-coded images.')
    datastore: StrictStr | None = Field(None, description='Proxmox Backup Server datastore name.')
    disable: bool | None = Field(None, description='Flag to disable the storage.')
    domain: StrictStr | None = Field(None, description='The name of the user domain (workgroup) to use.')
    encryption_key: StrictStr | None = Field(None, alias="encryption-key", description="Encryption key. Use 'autogen' to generate one automatically without passphrase.")
    export: StrictStr | None = Field(None, description='Path exported by the NFS server (e.g., /srv/nfs).')
    fast_io_fail_tmo: int | None = Field(None, alias="fast-io-fail-tmo", description='Seconds before I/O through a reconnecting path fails. -1 disables this timeout; I/O can remain queued while paths reconnect.')
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    format: StrictStr | None = Field(None, description='Default image format.')
    fs_name: StrictStr | None = Field(None, alias="fs-name", description='The name or identifier of the filesystem.')
    fuse: bool | None = Field(None, description='Mount the filesystem through FUSE.')
    is_mountpoint: StrictStr | None = Field(None, description='Assume the given path is an externally managed mountpoint and consider the storage offline if it is not mounted. Using a boolean (yes/no) value serves as a shortcut to using the target path in this field.')
    iscsiprovider: StrictStr | None = Field(None, description='The iSCSI target implementation used on the remote machine.')
    keyring: StrictStr | None = Field(None, description='Client keyring contents (for external clusters).')
    krbd: bool | None = Field(None, description='Always access rbd through krbd kernel module.')
    lio_tpg: StrictStr | None = Field(None, description='Target portal group for Linux LIO targets.')
    managed_multipath: bool | None = Field(None, alias="managed-multipath", description="Manage multipath access to the storage's LUNs and include them in the cluster-wide path-health monitoring.")
    master_pubkey: StrictStr | None = Field(None, alias="master-pubkey", description='Base64-encoded, PEM-formatted public RSA key. Used to encrypt a copy of the encryption-key which will be added to each encrypted backup.')
    max_protected_backups: int | None = Field(None, alias="max-protected-backups", description="Maximal number of protected backups per guest. Use '-1' for unlimited.")
    mkdir: bool | None = Field(None, description="Create the directory if it doesn't exist and populate it with default sub-dirs. NOTE: Deprecated, use the 'create-base-path' and 'create-subdirs' options instead.")
    monhost: StrictStr | None = Field(None, description='IP addresses of monitors (for external clusters).')
    mountpoint: StrictStr | None = Field(None, description='Path to the directory where the storage is mounted.')
    namespace: StrictStr | None = Field(None, description='The namespace used for grouping, isolation, or partitioning purposes.')
    nocow: bool | None = Field(None, description='Set the NOCOW flag on files. Disables data checksumming and causes data errors to be unrecoverable from while allowing direct I/O. Only use this if data does not need to be any more safe than on a single ext4 formatted disk with no underlying raid system.')
    nodes: StrictStr | None = Field(None, description='List of nodes for which the storage configuration applies.')
    nowritecache: bool | None = Field(None, description='Disable write caching on the iSCSI target.')
    on_volume_remove: StrictStr | None = Field(None, alias="on-volume-remove", description='Optional actions when removing LVs.')
    options: StrictStr | None = Field(None, description="Comma-separated list of mount options. See 'man nfs', 'man mount.cifs', or 'man mount.ceph' for more information.")
    password: StrictStr | None = Field(None, description='The password used for authentication.')
    path: StrictStr | None = Field(None, description='Path of the storage in the local file system, for example its base directory or mount point.')
    pool: StrictStr | None = Field(None, description='Name of the pool that stores images.')
    port: int | None = Field(None, description="Use this port to connect to the storage instead of the default one (for example, with PBS or ESXi). For NFS and CIFS, use the 'options' option to configure the port via the mount options.")
    portal: StrictStr | None = Field(None, description='iSCSI portal (IP or hostname, optionally with port).')
    portals: StrictStr | None = Field(None, description='TCP portals of the NVMe subsystem, as IPv4 or bracketed IPv6 addresses with an optional port (default 4420).')
    preallocation: StrictStr | None = Field(None, description="Preallocation mode for raw and qcow2 images. Using 'metadata' on raw images results in preallocation=off.")
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='The retention options with shorter intervals are processed first with --keep-last being the very first one. Each option covers a specific period of time. We say that backups within this period are covered by this option. The next option does not take care of already covered backups and only considers older backups.')
    saferemove: bool | None = Field(None, description='Zero-out data when removing LVs.')
    saferemove_stepsize: int | None = Field(None, alias="saferemove-stepsize", description='Wipe step size in MiB. It will be capped to the maximum supported by the storage.')
    saferemove_throughput: StrictStr | None = Field(None, description='Wipe throughput in bytes per second (optional suffix: k, m, or g).')
    server: StrictStr | None = Field(None, description='IP address or hostname of the server.')
    share: StrictStr | None = Field(None, description='The name of the share to use.')
    shared: bool | None = Field(None, description="Indicate that this is a single storage with the same contents on all nodes (or all listed in the 'nodes' option). It will not make the contents of a local storage automatically accessible to other nodes, it just marks an already shared storage as such!")
    skip_cert_verification: bool | None = Field(None, alias="skip-cert-verification", description='Disable TLS certificate verification, only enable on fully trusted networks!')
    smbversion: StrictStr | None = Field(None, description="SMB protocol version. 'default' if not set, negotiates the highest SMB2+ version supported by both the client and server.")
    snapshot_as_volume_chain: bool | None = Field(None, alias="snapshot-as-volume-chain", description='Enable support for creating storage-vendor agnostic snapshot through volume backing-chains.')
    sparse: bool | None = Field(None, description='Use sparse (thin-provisioned) volumes.')
    storage: StrictStr = Field(..., description='The storage identifier.')
    subdir: StrictStr | None = Field(None, description='Subdir to mount.')
    subsysnqn: StrictStr | None = Field(None, description='The NQN of the NVMe subsystem.')
    tagged_only: bool | None = Field(None, description="Only list logical volumes tagged with 'pve-vm-ID'.")
    target: StrictStr | None = Field(None, description='iSCSI target name (an iSCSI Qualified Name - IQN).')
    thinpool: StrictStr | None = Field(None, description='Name of the LVM thin pool logical volume.')
    type: StrictStr | None = Field(None, description='Storage type.')
    username: StrictStr | None = Field(None, description="The username for authentication. For RBD and CephFS, the Ceph client ID without the 'client.' prefix.")
    vgname: StrictStr | None = Field(None, description='LVM volume group name.')
    zfs_base_path: StrictStr | None = Field(None, alias="zfs-base-path", description="Base path where to look for the created ZFS block devices. Set automatically during creation if not specified. Usually '/dev/zvol'.")

class PostStorageResponse(ProxmoxBaseModel):
    """Model for create. Create a new storage. response."""
    config: dict[str, object] | None = Field(None, description='Partial, possibly server generated, configuration properties.')
    storage: StrictStr = Field(..., description='The ID of the created storage.')
    type: StrictStr = Field(..., description='The type of the created storage.')

class DeleteStorageStorageRequest(ProxmoxBaseModel):
    """Model for delete. Delete storage configuration. request."""
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')

class DeleteStorageStorageResponse(RootModel[None]):
    """Model for delete. Delete storage configuration. response."""
    root: None = Field(...)

class GetStorageStorageResponse(RootModel[dict[str, object]]):
    """Model for read. Read storage configuration. response."""
    root: dict[str, object] = Field(...)

class PutStorageStorageRequest(ProxmoxBaseModel):
    """Model for update. Update storage configuration. request."""
    blocksize: StrictStr | None = Field(None, description='ZFS block size.')
    bwlimit: StrictStr | None = Field(None, description='Set I/O bandwidth limit for various operations (in KiB/s).')
    comstar_hg: StrictStr | None = Field(None, description='Host group for COMSTAR views.')
    comstar_tg: StrictStr | None = Field(None, description='Target group for COMSTAR views.')
    content: StrictStr | None = Field(None, description="Allowed content types.\n\nNOTE: the value 'rootdir' is used for Containers, and value 'images' for VMs. A storage can instead be restricted to some of their volume types: 'vm-vol' for the disks of VMs, 'vm-state' for the saved states of VMs, and 'ct-vol' for the volumes of Containers.\n")
    content_dirs: StrictStr | None = Field(None, alias="content-dirs", description='Overrides for default content type directories.')
    create_base_path: bool | None = Field(None, alias="create-base-path", description="Create the base directory if it doesn't exist.")
    create_subdirs: bool | None = Field(None, alias="create-subdirs", description='Populate the base directory with the default structure.')
    data_pool: StrictStr | None = Field(None, alias="data-pool", description='Data pool name for erasure-coded images.')
    delete: StrictStr | None = Field(None, description='A list of settings you want to delete.')
    digest: StrictStr | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the storage.')
    domain: StrictStr | None = Field(None, description='The name of the user domain (workgroup) to use.')
    encryption_key: StrictStr | None = Field(None, alias="encryption-key", description="Encryption key. Use 'autogen' to generate one automatically without passphrase.")
    fast_io_fail_tmo: int | None = Field(None, alias="fast-io-fail-tmo", description='Seconds before I/O through a reconnecting path fails. -1 disables this timeout; I/O can remain queued while paths reconnect.')
    fingerprint: StrictStr | None = Field(None, description='Certificate SHA 256 fingerprint.')
    format: StrictStr | None = Field(None, description='Default image format.')
    fs_name: StrictStr | None = Field(None, alias="fs-name", description='The name or identifier of the filesystem.')
    fuse: bool | None = Field(None, description='Mount the filesystem through FUSE.')
    is_mountpoint: StrictStr | None = Field(None, description='Assume the given path is an externally managed mountpoint and consider the storage offline if it is not mounted. Using a boolean (yes/no) value serves as a shortcut to using the target path in this field.')
    keyring: StrictStr | None = Field(None, description='Client keyring contents (for external clusters).')
    krbd: bool | None = Field(None, description='Always access rbd through krbd kernel module.')
    lio_tpg: StrictStr | None = Field(None, description='Target portal group for Linux LIO targets.')
    managed_multipath: bool | None = Field(None, alias="managed-multipath", description="Manage multipath access to the storage's LUNs and include them in the cluster-wide path-health monitoring.")
    master_pubkey: StrictStr | None = Field(None, alias="master-pubkey", description='Base64-encoded, PEM-formatted public RSA key. Used to encrypt a copy of the encryption-key which will be added to each encrypted backup.')
    max_protected_backups: int | None = Field(None, alias="max-protected-backups", description="Maximal number of protected backups per guest. Use '-1' for unlimited.")
    mkdir: bool | None = Field(None, description="Create the directory if it doesn't exist and populate it with default sub-dirs. NOTE: Deprecated, use the 'create-base-path' and 'create-subdirs' options instead.")
    monhost: StrictStr | None = Field(None, description='IP addresses of monitors (for external clusters).')
    mountpoint: StrictStr | None = Field(None, description='Path to the directory where the storage is mounted.')
    namespace: StrictStr | None = Field(None, description='The namespace used for grouping, isolation, or partitioning purposes.')
    nocow: bool | None = Field(None, description='Set the NOCOW flag on files. Disables data checksumming and causes data errors to be unrecoverable from while allowing direct I/O. Only use this if data does not need to be any more safe than on a single ext4 formatted disk with no underlying raid system.')
    nodes: StrictStr | None = Field(None, description='List of nodes for which the storage configuration applies.')
    nowritecache: bool | None = Field(None, description='Disable write caching on the iSCSI target.')
    on_volume_remove: StrictStr | None = Field(None, alias="on-volume-remove", description='Optional actions when removing LVs.')
    options: StrictStr | None = Field(None, description="Comma-separated list of mount options. See 'man nfs', 'man mount.cifs', or 'man mount.ceph' for more information.")
    password: StrictStr | None = Field(None, description='The password used for authentication.')
    pool: StrictStr | None = Field(None, description='Name of the pool that stores images.')
    port: int | None = Field(None, description="Use this port to connect to the storage instead of the default one (for example, with PBS or ESXi). For NFS and CIFS, use the 'options' option to configure the port via the mount options.")
    portals: StrictStr | None = Field(None, description='TCP portals of the NVMe subsystem, as IPv4 or bracketed IPv6 addresses with an optional port (default 4420).')
    preallocation: StrictStr | None = Field(None, description="Preallocation mode for raw and qcow2 images. Using 'metadata' on raw images results in preallocation=off.")
    prune_backups: StrictStr | None = Field(None, alias="prune-backups", description='The retention options with shorter intervals are processed first with --keep-last being the very first one. Each option covers a specific period of time. We say that backups within this period are covered by this option. The next option does not take care of already covered backups and only considers older backups.')
    saferemove: bool | None = Field(None, description='Zero-out data when removing LVs.')
    saferemove_stepsize: int | None = Field(None, alias="saferemove-stepsize", description='Wipe step size in MiB. It will be capped to the maximum supported by the storage.')
    saferemove_throughput: StrictStr | None = Field(None, description='Wipe throughput in bytes per second (optional suffix: k, m, or g).')
    shared: bool | None = Field(None, description="Indicate that this is a single storage with the same contents on all nodes (or all listed in the 'nodes' option). It will not make the contents of a local storage automatically accessible to other nodes, it just marks an already shared storage as such!")
    skip_cert_verification: bool | None = Field(None, alias="skip-cert-verification", description='Disable TLS certificate verification, only enable on fully trusted networks!')
    smbversion: StrictStr | None = Field(None, description="SMB protocol version. 'default' if not set, negotiates the highest SMB2+ version supported by both the client and server.")
    snapshot_as_volume_chain: bool | None = Field(None, alias="snapshot-as-volume-chain", description='Enable support for creating storage-vendor agnostic snapshot through volume backing-chains.')
    sparse: bool | None = Field(None, description='Use sparse (thin-provisioned) volumes.')
    subdir: StrictStr | None = Field(None, description='Subdir to mount.')
    tagged_only: bool | None = Field(None, description="Only list logical volumes tagged with 'pve-vm-ID'.")
    type: StrictStr | None = Field(None, description='Storage type.')
    username: StrictStr | None = Field(None, description="The username for authentication. For RBD and CephFS, the Ceph client ID without the 'client.' prefix.")
    zfs_base_path: StrictStr | None = Field(None, alias="zfs-base-path", description="Base path where to look for the created ZFS block devices. Set automatically during creation if not specified. Usually '/dev/zvol'.")

class PutStorageStorageResponse(ProxmoxBaseModel):
    """Model for update. Update storage configuration. response."""
    config: dict[str, object] | None = Field(None, description='Partial, possibly server generated, configuration properties.')
    storage: StrictStr = Field(..., description='The ID of the created storage.')
    type: StrictStr = Field(..., description='The type of the created storage.')

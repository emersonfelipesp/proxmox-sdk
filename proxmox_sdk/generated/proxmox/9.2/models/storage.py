"""Generated Pydantic v2 schemas for Proxmox route group 'storage'.

Do not edit by hand. Regenerate from the matching OpenAPI artifact.
"""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, RootModel

GENERATED_FOR_PROXMOX_VERSION = "9.2"
GENERATED_SOURCE_SHA256 = "db7e80b8646db731814601617206e3835b5b572def655f18a27e0b22b6f31297"
GENERATED_AT = "2026-05-23T21:58:59.250679+00:00"


class ProxmoxBaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra='allow')

class GetStorageResponseItem(ProxmoxBaseModel):
    """Model for index. Storage index. response."""
    storage: str | None = Field(None)

class GetStorageResponse(RootModel[list[GetStorageResponseItem]]):
    """List of items. index. Storage index. response."""
    root: list[GetStorageResponseItem] = Field(...)

class PostStorageRequest(ProxmoxBaseModel):
    """Model for create. Create a new storage. request."""
    authsupported: str | None = Field(None, description='Authsupported.')
    base: str | None = Field(None, description='Base volume. This volume is automatically activated.')
    blocksize: str | None = Field(None, description='ZFS block size')
    bwlimit: str | None = Field(None, description='Set I/O bandwidth limit for various operations (in KiB/s).')
    comstar_hg: str | None = Field(None, description='host group for comstar views')
    comstar_tg: str | None = Field(None, description='target group for comstar views')
    content: str | None = Field(None, description="Allowed content types.\n\nNOTE: the value 'rootdir' is used for Containers, and value 'images' for VMs.\n")
    content_dirs: str | None = Field(None, alias="content-dirs", description='Overrides for default content type directories.')
    create_base_path: bool | None = Field(None, alias="create-base-path", description="Create the base directory if it doesn't exist.")
    create_subdirs: bool | None = Field(None, alias="create-subdirs", description='Populate the directory with the default structure.')
    data_pool: str | None = Field(None, alias="data-pool", description='Data Pool (for erasure coding only)')
    datastore: str | None = Field(None, description='Proxmox Backup Server datastore name.')
    disable: bool | None = Field(None, description='Flag to disable the storage.')
    domain: str | None = Field(None, description='CIFS domain.')
    encryption_key: str | None = Field(None, alias="encryption-key", description="Encryption key. Use 'autogen' to generate one automatically without passphrase.")
    export: str | None = Field(None, description='NFS export path.')
    fingerprint: str | None = Field(None, description='Certificate SHA 256 fingerprint.')
    format: str | None = Field(None, description='Default image format.')
    fs_name: str | None = Field(None, alias="fs-name", description='The Ceph filesystem name.')
    fuse: bool | None = Field(None, description='Mount CephFS through FUSE.')
    is_mountpoint: str | None = Field(None, description='Assume the given path is an externally managed mountpoint and consider the storage offline if it is not mounted. Using a boolean (yes/no) value serves as a shortcut to using the target path in this field.')
    iscsiprovider: str | None = Field(None, description='iscsi provider')
    keyring: str | None = Field(None, description='Client keyring contents (for external clusters).')
    krbd: bool | None = Field(None, description='Always access rbd through krbd kernel module.')
    lio_tpg: str | None = Field(None, description='target portal group for Linux LIO targets')
    master_pubkey: str | None = Field(None, alias="master-pubkey", description='Base64-encoded, PEM-formatted public RSA key. Used to encrypt a copy of the encryption-key which will be added to each encrypted backup.')
    max_protected_backups: int | None = Field(None, alias="max-protected-backups", description="Maximal number of protected backups per guest. Use '-1' for unlimited.")
    mkdir: bool | None = Field(None, description="Create the directory if it doesn't exist and populate it with default sub-dirs. NOTE: Deprecated, use the 'create-base-path' and 'create-subdirs' options instead.")
    monhost: str | None = Field(None, description='IP addresses of monitors (for external clusters).')
    mountpoint: str | None = Field(None, description='mount point')
    namespace: str | None = Field(None, description='Namespace.')
    nocow: bool | None = Field(None, description='Set the NOCOW flag on files. Disables data checksumming and causes data errors to be unrecoverable from while allowing direct I/O. Only use this if data does not need to be any more safe than on a single ext4 formatted disk with no underlying raid system.')
    nodes: str | None = Field(None, description='List of nodes for which the storage configuration applies.')
    nowritecache: bool | None = Field(None, description='disable write caching on the target')
    options: str | None = Field(None, description="NFS/CIFS mount options (see 'man nfs' or 'man mount.cifs')")
    password: str | None = Field(None, description='Password for accessing the share/datastore.')
    path: str | None = Field(None, description='File system path.')
    pool: str | None = Field(None, description='Pool.')
    port: int | None = Field(None, description="Use this port to connect to the storage instead of the default one (for example, with PBS or ESXi). For NFS and CIFS, use the 'options' option to configure the port via the mount options.")
    portal: str | None = Field(None, description='iSCSI portal (IP or DNS name with optional port).')
    preallocation: str | None = Field(None, description="Preallocation mode for raw and qcow2 images. Using 'metadata' on raw images results in preallocation=off.")
    prune_backups: str | None = Field(None, alias="prune-backups", description='The retention options with shorter intervals are processed first with --keep-last being the very first one. Each option covers a specific period of time. We say that backups within this period are covered by this option. The next option does not take care of already covered backups and only considers older backups.')
    saferemove: bool | None = Field(None, description='Zero-out data when removing LVs.')
    saferemove_stepsize: int | None = Field(None, alias="saferemove-stepsize", description='Wipe step size in MiB. It will be capped to the maximum supported by the storage.')
    saferemove_throughput: str | None = Field(None, description='Wipe throughput (cstream -t parameter value).')
    server: str | None = Field(None, description='Server IP or DNS name.')
    share: str | None = Field(None, description='CIFS share.')
    shared: bool | None = Field(None, description="Indicate that this is a single storage with the same contents on all nodes (or all listed in the 'nodes' option). It will not make the contents of a local storage automatically accessible to other nodes, it just marks an already shared storage as such!")
    skip_cert_verification: bool | None = Field(None, alias="skip-cert-verification", description='Disable TLS certificate verification, only enable on fully trusted networks!')
    smbversion: str | None = Field(None, description="SMB protocol version. 'default' if not set, negotiates the highest SMB2+ version supported by both the client and server.")
    snapshot_as_volume_chain: bool | None = Field(None, alias="snapshot-as-volume-chain", description='Enable support for creating storage-vendor agnostic snapshot through volume backing-chains.')
    sparse: bool | None = Field(None, description='use sparse volumes')
    storage: str = Field(..., description='The storage identifier.')
    subdir: str | None = Field(None, description='Subdir to mount.')
    tagged_only: bool | None = Field(None, description="Only list logical volumes tagged with 'pve-vm-ID'.")
    target: str | None = Field(None, description='iSCSI target.')
    thinpool: str | None = Field(None, description='LVM thin pool LV name.')
    type: str = Field(..., description='Storage type.')
    username: str | None = Field(None, description='RBD Id.')
    vgname: str | None = Field(None, description='Volume group name.')
    zfs_base_path: str | None = Field(None, alias="zfs-base-path", description="Base path where to look for the created ZFS block devices. Set automatically during creation if not specified. Usually '/dev/zvol'.")

class PostStorageResponse(ProxmoxBaseModel):
    """Model for create. Create a new storage. response."""
    config: dict[str, object] | None = Field(None, description='Partial, possibly server generated, configuration properties.')
    storage: str = Field(..., description='The ID of the created storage.')
    type: str = Field(..., description='The type of the created storage.')

class DeleteStorageStorageResponse(RootModel[None]):
    """Model for delete. Delete storage configuration. response."""
    root: None = Field(...)

class GetStorageStorageResponse(RootModel[dict[str, object]]):
    """Model for read. Read storage configuration. response."""
    root: dict[str, object] = Field(...)

class PutStorageStorageRequest(ProxmoxBaseModel):
    """Model for update. Update storage configuration. request."""
    blocksize: str | None = Field(None, description='ZFS block size')
    bwlimit: str | None = Field(None, description='Set I/O bandwidth limit for various operations (in KiB/s).')
    comstar_hg: str | None = Field(None, description='host group for comstar views')
    comstar_tg: str | None = Field(None, description='target group for comstar views')
    content: str | None = Field(None, description="Allowed content types.\n\nNOTE: the value 'rootdir' is used for Containers, and value 'images' for VMs.\n")
    content_dirs: str | None = Field(None, alias="content-dirs", description='Overrides for default content type directories.')
    create_base_path: bool | None = Field(None, alias="create-base-path", description="Create the base directory if it doesn't exist.")
    create_subdirs: bool | None = Field(None, alias="create-subdirs", description='Populate the directory with the default structure.')
    data_pool: str | None = Field(None, alias="data-pool", description='Data Pool (for erasure coding only)')
    delete: str | None = Field(None, description='A list of settings you want to delete.')
    digest: str | None = Field(None, description='Prevent changes if current configuration file has a different digest. This can be used to prevent concurrent modifications.')
    disable: bool | None = Field(None, description='Flag to disable the storage.')
    domain: str | None = Field(None, description='CIFS domain.')
    encryption_key: str | None = Field(None, alias="encryption-key", description="Encryption key. Use 'autogen' to generate one automatically without passphrase.")
    fingerprint: str | None = Field(None, description='Certificate SHA 256 fingerprint.')
    format: str | None = Field(None, description='Default image format.')
    fs_name: str | None = Field(None, alias="fs-name", description='The Ceph filesystem name.')
    fuse: bool | None = Field(None, description='Mount CephFS through FUSE.')
    is_mountpoint: str | None = Field(None, description='Assume the given path is an externally managed mountpoint and consider the storage offline if it is not mounted. Using a boolean (yes/no) value serves as a shortcut to using the target path in this field.')
    keyring: str | None = Field(None, description='Client keyring contents (for external clusters).')
    krbd: bool | None = Field(None, description='Always access rbd through krbd kernel module.')
    lio_tpg: str | None = Field(None, description='target portal group for Linux LIO targets')
    master_pubkey: str | None = Field(None, alias="master-pubkey", description='Base64-encoded, PEM-formatted public RSA key. Used to encrypt a copy of the encryption-key which will be added to each encrypted backup.')
    max_protected_backups: int | None = Field(None, alias="max-protected-backups", description="Maximal number of protected backups per guest. Use '-1' for unlimited.")
    mkdir: bool | None = Field(None, description="Create the directory if it doesn't exist and populate it with default sub-dirs. NOTE: Deprecated, use the 'create-base-path' and 'create-subdirs' options instead.")
    monhost: str | None = Field(None, description='IP addresses of monitors (for external clusters).')
    mountpoint: str | None = Field(None, description='mount point')
    namespace: str | None = Field(None, description='Namespace.')
    nocow: bool | None = Field(None, description='Set the NOCOW flag on files. Disables data checksumming and causes data errors to be unrecoverable from while allowing direct I/O. Only use this if data does not need to be any more safe than on a single ext4 formatted disk with no underlying raid system.')
    nodes: str | None = Field(None, description='List of nodes for which the storage configuration applies.')
    nowritecache: bool | None = Field(None, description='disable write caching on the target')
    options: str | None = Field(None, description="NFS/CIFS mount options (see 'man nfs' or 'man mount.cifs')")
    password: str | None = Field(None, description='Password for accessing the share/datastore.')
    pool: str | None = Field(None, description='Pool.')
    port: int | None = Field(None, description="Use this port to connect to the storage instead of the default one (for example, with PBS or ESXi). For NFS and CIFS, use the 'options' option to configure the port via the mount options.")
    preallocation: str | None = Field(None, description="Preallocation mode for raw and qcow2 images. Using 'metadata' on raw images results in preallocation=off.")
    prune_backups: str | None = Field(None, alias="prune-backups", description='The retention options with shorter intervals are processed first with --keep-last being the very first one. Each option covers a specific period of time. We say that backups within this period are covered by this option. The next option does not take care of already covered backups and only considers older backups.')
    saferemove: bool | None = Field(None, description='Zero-out data when removing LVs.')
    saferemove_stepsize: int | None = Field(None, alias="saferemove-stepsize", description='Wipe step size in MiB. It will be capped to the maximum supported by the storage.')
    saferemove_throughput: str | None = Field(None, description='Wipe throughput (cstream -t parameter value).')
    server: str | None = Field(None, description='Server IP or DNS name.')
    shared: bool | None = Field(None, description="Indicate that this is a single storage with the same contents on all nodes (or all listed in the 'nodes' option). It will not make the contents of a local storage automatically accessible to other nodes, it just marks an already shared storage as such!")
    skip_cert_verification: bool | None = Field(None, alias="skip-cert-verification", description='Disable TLS certificate verification, only enable on fully trusted networks!')
    smbversion: str | None = Field(None, description="SMB protocol version. 'default' if not set, negotiates the highest SMB2+ version supported by both the client and server.")
    snapshot_as_volume_chain: bool | None = Field(None, alias="snapshot-as-volume-chain", description='Enable support for creating storage-vendor agnostic snapshot through volume backing-chains.')
    sparse: bool | None = Field(None, description='use sparse volumes')
    subdir: str | None = Field(None, description='Subdir to mount.')
    tagged_only: bool | None = Field(None, description="Only list logical volumes tagged with 'pve-vm-ID'.")
    username: str | None = Field(None, description='RBD Id.')
    zfs_base_path: str | None = Field(None, alias="zfs-base-path", description="Base path where to look for the created ZFS block devices. Set automatically during creation if not specified. Usually '/dev/zvol'.")

class PutStorageStorageResponse(ProxmoxBaseModel):
    """Model for update. Update storage configuration. response."""
    config: dict[str, object] | None = Field(None, description='Partial, possibly server generated, configuration properties.')
    storage: str = Field(..., description='The ID of the created storage.')
    type: str = Field(..., description='The type of the created storage.')

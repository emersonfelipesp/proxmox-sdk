"""Read-only Ceph domain helpers."""

from proxmox_sdk.ceph.domains.cluster import ClusterCeph
from proxmox_sdk.ceph.domains.nodes import NodeCeph

__all__ = ["ClusterCeph", "NodeCeph"]

"""Ceph SDK facade for Proxmox VE clusters.

Ceph management in Proxmox VE is exposed under the PVE API surface
(``/cluster/ceph`` and ``/nodes/{node}/ceph``).  This package therefore
composes the existing :class:`proxmox_sdk.sdk.api.ProxmoxSDK` transport with
``service="PVE"`` and adds typed helpers for inventory, status collection, and
explicit Proxmox-managed Ceph write operations.

Destructive write helpers require ``confirm_destroy=True`` so callers must opt
in before removing pools or daemons.
"""

from proxmox_sdk.ceph.client import CephClient, SyncCephClient
from proxmox_sdk.ceph.domains import CephWrite, ClusterCeph, NodeCeph

__all__ = ["CephClient", "CephWrite", "ClusterCeph", "NodeCeph", "SyncCephClient"]

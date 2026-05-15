"""Ceph SDK facade for Proxmox VE clusters.

Ceph management in Proxmox VE is exposed under the PVE API surface
(``/cluster/ceph`` and ``/nodes/{node}/ceph``).  This package therefore
composes the existing :class:`proxmox_sdk.sdk.api.ProxmoxSDK` transport with
``service="PVE"`` and adds typed read-only helpers for inventory and status
collection.

v1 intentionally exports read helpers only. Mutating Ceph operations such as
creating pools, starting daemons, deleting OSDs, or changing flags remain out
of this facade until the NetBox workflow needs explicit write support.
"""

from proxmox_sdk.ceph.client import CephClient, SyncCephClient

__all__ = ["CephClient", "SyncCephClient"]

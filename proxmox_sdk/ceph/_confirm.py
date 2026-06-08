"""Shared destructive-operation confirmation gate for Ceph clients."""

from __future__ import annotations


def require_confirm(operation: str, confirm_destroy: bool) -> None:
    """Raise ``ValueError`` unless a destructive operation is explicitly confirmed.

    Centralises the ``confirm_destroy=True`` gate shared by the Proxmox VE
    :class:`~proxmox_sdk.ceph.domains.write.CephWrite` domain and the direct
    provider clients (Dashboard / RGW / RBD) so the wording and exception type
    live in exactly one place.
    """
    if not confirm_destroy:
        raise ValueError(f"{operation} is destructive; pass confirm_destroy=True to proceed.")

"""Proxmox Datacenter Manager (PDM) SDK — typed client facade.

Composes the existing :class:`~proxmox_sdk.sdk.api.ProxmoxSDK` transport
(``service="PDM"``) with typed domain helpers and hand-coded Pydantic v2
response models for the PDM REST API.

Quick start::

    from proxmox_sdk.pdm import PDMClient

    async with PDMClient(
        host="pdm.example.com",
        user="root@pam",
        token_name="api",
        token_value="...",
    ) as pdm:
        remotes = await pdm.remotes.list()
        guests = await pdm.pve.qemu.list(remote="pve-a")

Sync usage::

    from proxmox_sdk.pdm import SyncPDMClient

    with SyncPDMClient(host=..., user=..., token_name=..., token_value=...) as pdm:
        version = pdm.version()

See :class:`~proxmox_sdk.pdm.client.PDMClient` for the full API.
"""

from proxmox_sdk.pdm.client import PDMClient, SyncPDMClient
from proxmox_sdk.pdm.errors import PDMResponseContractError

__all__ = ["PDMClient", "PDMResponseContractError", "SyncPDMClient"]

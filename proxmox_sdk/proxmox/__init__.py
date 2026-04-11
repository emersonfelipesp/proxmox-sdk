"""Real Proxmox API client implementation."""

from __future__ import annotations

from proxmox_sdk.proxmox.client import ProxmoxClient
from proxmox_sdk.proxmox.config import ProxmoxConfig

__all__ = ["ProxmoxClient", "ProxmoxConfig"]

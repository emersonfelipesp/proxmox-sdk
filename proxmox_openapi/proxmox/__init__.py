"""Real Proxmox API client implementation."""

from __future__ import annotations

from proxmox_openapi.proxmox.client import ProxmoxClient
from proxmox_openapi.proxmox.config import ProxmoxConfig

__all__ = ["ProxmoxClient", "ProxmoxConfig"]

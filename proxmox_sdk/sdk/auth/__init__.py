"""Authentication strategies for the Proxmox SDK HTTPS backend."""

from proxmox_sdk.sdk.auth.ticket import TicketAuth
from proxmox_sdk.sdk.auth.token import TokenAuth

__all__ = ["TicketAuth", "TokenAuth"]

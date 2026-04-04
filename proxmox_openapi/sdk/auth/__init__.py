"""Authentication strategies for the Proxmox SDK HTTPS backend."""

from proxmox_openapi.sdk.auth.ticket import TicketAuth
from proxmox_openapi.sdk.auth.token import TokenAuth

__all__ = ["TicketAuth", "TokenAuth"]

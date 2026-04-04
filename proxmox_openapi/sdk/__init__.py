"""Proxmox OpenAPI SDK — standalone Python SDK for the Proxmox API."""

from proxmox_openapi.sdk.api import ProxmoxSDK
from proxmox_openapi.sdk.exceptions import (
    AuthenticationError,
    BackendNotAvailableError,
    ProxmoxSDKError,
    ResourceException,
)
from proxmox_openapi.sdk.sync import SyncProxmoxSDK
from proxmox_openapi.sdk.tools.files import Files
from proxmox_openapi.sdk.tools.tasks import Tasks

__all__ = [
    "ProxmoxSDK",
    "SyncProxmoxSDK",
    "ResourceException",
    "AuthenticationError",
    "BackendNotAvailableError",
    "ProxmoxSDKError",
    "Tasks",
    "Files",
]

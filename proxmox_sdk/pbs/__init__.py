"""Proxmox Backup Server (PBS) SDK — read-only client facade.

Composes the existing `ProxmoxSDK(service="PBS", ...)` transport
(`proxmox_sdk.sdk.api.ProxmoxSDK`) with typed read-only domain helpers and
hand-coded Pydantic v2 response models for the PBS REST API.

v1 ships the read paths only (datastores, backup groups + snapshots, jobs
status, node status, version). Write helpers (POST/PUT/DELETE) are
intentionally not exported.

A full codegen bundle at ``proxmox_sdk/generated/pbs/latest/`` (retargeting
the existing crawler at ``https://pbs.proxmox.com/docs/api-viewer/``) is
planned as a follow-up so the typed surface can grow without hand-writing
each endpoint.
"""

from proxmox_sdk.pbs.client import PBSClient, SyncPBSClient

__all__ = ["PBSClient", "SyncPBSClient"]

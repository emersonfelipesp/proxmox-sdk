"""Direct (non-Proxmox) Ceph provider clients for Ceph v2.

These clients talk to Ceph services directly rather than through the Proxmox VE
API, so they support Proxmox-managed *and* external/standalone clusters:

- :class:`DashboardCephClient` — Ceph Manager Dashboard REST API.
- :class:`RGWAdminClient` — RGW Admin Ops API (S3 SigV2 signed).
- :class:`RBDClient` — RBD operations via the Dashboard block API.

Each client exposes an async ``capabilities()`` returning a
:class:`ProviderCapability`, and raises
:class:`~proxmox_sdk.sdk.exceptions.CephCapabilityUnsupportedError` for
operations the configured provider/version cannot service.
"""

from proxmox_sdk.ceph.providers._http import (
    AiohttpTransport,
    AsyncTransport,
    BaseHttpProvider,
    HttpResponse,
    JSONValue,
)
from proxmox_sdk.ceph.providers.capability import ProviderCapability
from proxmox_sdk.ceph.providers.dashboard import DashboardCephClient
from proxmox_sdk.ceph.providers.rbd import RBDClient
from proxmox_sdk.ceph.providers.rgw import RGWAdminClient
from proxmox_sdk.sdk.exceptions import CephCapabilityUnsupportedError

__all__ = [
    "AiohttpTransport",
    "AsyncTransport",
    "BaseHttpProvider",
    "CephCapabilityUnsupportedError",
    "DashboardCephClient",
    "HttpResponse",
    "JSONValue",
    "ProviderCapability",
    "RBDClient",
    "RGWAdminClient",
]

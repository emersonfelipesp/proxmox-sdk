"""In-memory FastAPI mock for the Proxmox Datacenter Manager (PDM) API.

The mock is hand-coded because the PDM codegen pipeline is a future
deliverable (see closed issue #29). It mirrors every PDM SDK code path
(`proxmox_sdk.pdm`) so E2E tests can run without a live PDM instance.

Public entry points:

* :func:`register_generated_pdm_mock_routes` — attach mock routes to an
  existing :class:`fastapi.FastAPI` app and return its mutable state.
* :func:`get_default_pdm_seed` — realistic default fixture data.
"""

from proxmox_sdk.pdm.mock.routes import (
    PDMMockState,
    register_generated_pdm_mock_routes,
)
from proxmox_sdk.pdm.mock.seed_data import get_default_pdm_seed

__all__ = [
    "PDMMockState",
    "get_default_pdm_seed",
    "register_generated_pdm_mock_routes",
]

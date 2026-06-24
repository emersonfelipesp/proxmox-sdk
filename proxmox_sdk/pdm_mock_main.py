"""Standalone PDM mock API entrypoint.

Exposes the PDM mock as a FastAPI app on (by default) ``0.0.0.0:8443``.
Configured via environment variables:

================================  =================================================
Variable                          Purpose
================================  =================================================
``PROXMOX_PDM_MOCK_HOST``         Bind host (default ``0.0.0.0``).
``PROXMOX_PDM_MOCK_PORT``         Bind port (default ``8443``).
``PROXMOX_PDM_MOCK_SEED_FILE``    JSON file to use as initial state.
``PROXMOX_PDM_MOCK_SCHEMA_VERSION`` Reserved for the future PDM codegen pipeline.
================================  =================================================
"""

from __future__ import annotations

import os
from typing import Any

import uvicorn
from fastapi import FastAPI

from proxmox_sdk import __version__
from proxmox_sdk.pdm.mock.routes import (
    PDMMockState,
    load_seed_from_file,
    register_generated_pdm_mock_routes,
)


def _instrument_app(app: FastAPI) -> FastAPI:
    from proxmox_sdk import telemetry

    return telemetry.instrument_fastapi_app(app)


def create_pdm_mock_app(
    *,
    state: PDMMockState | None = None,
    seed: dict[str, Any] | None = None,
) -> FastAPI:
    """Build the standalone PDM mock API app.

    Pass ``state`` to share state with another process/app instance, or
    pass ``seed`` to bootstrap from a custom fixture dict. If neither is
    given, the bundled default seed (3 remotes, 16 VMs, 5 CTs, 2 datastores,
    50+ snapshots, 3 users, 5 ACL entries, 2 views) is used.
    """
    version_tag = os.environ.get("PROXMOX_PDM_MOCK_SCHEMA_VERSION", "1.0")

    if seed is None and state is None:
        seed_file = os.environ.get("PROXMOX_PDM_MOCK_SEED_FILE")
        if seed_file:
            seed = load_seed_from_file(seed_file)

    app = FastAPI(
        title="Proxmox Datacenter Manager (PDM) Mock API",
        description=(
            "In-memory FastAPI mock for the PDM REST API. Mirrors every PDM SDK "
            "code path so E2E tests can run without a live PDM instance."
        ),
        version=__version__,
    )

    mock_state = register_generated_pdm_mock_routes(app, state=state, seed=seed)

    @app.get("/")
    async def root() -> dict[str, Any]:
        return {
            "message": "Proxmox Datacenter Manager mock API",
            "schema_version": version_tag,
            "package_version": __version__,
        }

    @app.get("/health")
    async def health() -> dict[str, str]:
        return {"status": "ready"}

    # Expose the state on the app so test fixtures can inspect / mutate it
    # without going through HTTP.
    app.state.pdm_mock_state = mock_state
    return _instrument_app(app)


app = create_pdm_mock_app()


def run() -> None:
    """Console-script entrypoint for the PDM mock API."""
    uvicorn.run(
        "proxmox_sdk.pdm_mock_main:app",
        host=os.environ.get("PROXMOX_PDM_MOCK_HOST", "0.0.0.0"),
        port=int(os.environ.get("PROXMOX_PDM_MOCK_PORT", "8443")),
    )


__all__ = ["app", "create_pdm_mock_app", "run"]

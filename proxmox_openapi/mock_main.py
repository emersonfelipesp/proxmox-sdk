"""Standalone mock API entrypoint."""

from __future__ import annotations

import os

import uvicorn

from proxmox_openapi.mock.app import create_mock_app

app = create_mock_app()


def run() -> None:
    """Console-script entrypoint for the standalone mock API."""
    uvicorn.run(
        "proxmox_openapi.mock_main:app",
        host=os.environ.get("HOST", "0.0.0.0"),
        port=int(os.environ.get("PORT", "8000")),
    )


__all__ = ["app", "run"]

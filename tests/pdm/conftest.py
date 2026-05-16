"""Shared fixtures for PDM tests.

The ``_RecordingBackend`` mirrors the pattern used in ``tests/pbs/`` so each
test can wire canned responses by path and assert the exact requests issued
against the SDK transport.
"""

from __future__ import annotations

from typing import Any

from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.backends.base import AbstractBackend
from proxmox_sdk.sdk.resource import ProxmoxResource
from proxmox_sdk.sdk.services import SERVICES


class RecordingBackend(AbstractBackend):
    """Records (method, path, params, data) and replays canned responses by path."""

    def __init__(self, responses: dict[str, Any]) -> None:
        self.responses = responses
        self.calls: list[tuple[str, str, dict[str, Any] | None, dict[str, Any] | None]] = []

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        self.calls.append((method, path, params, data))
        if path not in self.responses:
            raise AssertionError(f"unexpected path: {path}")
        return self.responses[path]

    async def close(self) -> None:
        return None


def make_pdm_sdk(responses: dict[str, Any]) -> tuple[ProxmoxSDK, RecordingBackend]:
    svc = SERVICES["PDM"]
    backend = RecordingBackend(responses)
    sdk = object.__new__(ProxmoxSDK)
    sdk._service_name = "PDM"
    sdk._service_config = svc
    sdk._backend_name = "recording"
    sdk._backend = backend
    sdk._root = ProxmoxResource(path=svc.api_path_prefix, backend=backend)
    return sdk, backend

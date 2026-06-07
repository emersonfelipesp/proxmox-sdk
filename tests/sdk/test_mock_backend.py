"""Regression tests for the direct SDK MockBackend."""

from __future__ import annotations

import asyncio
import uuid

import pytest

from proxmox_sdk.sdk.backends.mock import MockBackend
from proxmox_sdk.sdk.exceptions import ResourceException
from proxmox_sdk.sdk.services import SERVICES


def test_delete_tombstone_prevents_get_resurrection(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PROXMOX_MOCK_STORE", "dict")
    monkeypatch.setenv("PROXMOX_MOCK_STATE_NAMESPACE", f"test_sdk_mock_backend_{uuid.uuid4().hex}")

    async def _run() -> None:
        backend = MockBackend(api_path_prefix=SERVICES["PVE"].api_path_prefix)
        path = "/api2/json/access/users/psk001@pve"

        seeded = await backend.request("GET", path)
        assert isinstance(seeded, dict)

        await backend.request("DELETE", path)

        with pytest.raises(ResourceException) as exc_info:
            await backend.request("GET", path)

        assert exc_info.value.status_code == 404
        assert exc_info.value.status_message == "Not Found"
        assert exc_info.value.content == "Mock resource not found."
        assert backend._store is not None
        assert backend._store.get_object(path) is None

    asyncio.run(_run())

"""Client-level behaviour: version, sync wrapper, service guard, mock factory."""

from __future__ import annotations

import pytest

from proxmox_sdk.pdm import PDMClient, SyncPDMClient
from proxmox_sdk.pdm import models as m
from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.services import SERVICES

from .conftest import make_pdm_sdk


def test_pdm_service_registered_with_expected_defaults():
    svc = SERVICES["PDM"]
    assert svc.default_port == 8443
    assert svc.auth_cookie_name == "PDMAuthCookie"
    assert "https" in svc.supported_backends
    assert "mock" in svc.supported_backends


async def test_version_unwraps_data_envelope():
    sdk, _ = make_pdm_sdk({"/api2/json/version": {"data": {"version": "1.0.4", "release": "1"}}})
    pdm = PDMClient(_sdk=sdk)
    v = await pdm.version()
    assert isinstance(v, m.PDMVersion)
    assert v.version == "1.0.4"


async def test_from_sdk_rejects_non_pdm():
    pve_sdk = ProxmoxSDK.mock(service="PVE")
    try:
        with pytest.raises(ValueError):
            PDMClient.from_sdk(pve_sdk)
    finally:
        await pve_sdk.close()


async def test_from_sdk_accepts_pdm():
    sdk, _ = make_pdm_sdk({"/api2/json/version": {"data": {"version": "1.0"}}})
    pdm = PDMClient.from_sdk(sdk)
    v = await pdm.version()
    assert v.version == "1.0"


def test_sync_client_blocks_and_returns_typed_models():
    sdk, _ = make_pdm_sdk(
        {
            "/api2/json/version": {"data": {"version": "1.0.4"}},
            "/api2/json/remotes/remote": {"data": [{"id": "pve-a", "type": "pve"}]},
        }
    )
    client = SyncPDMClient(_sdk=sdk)
    try:
        v = client.version()
        assert v.version == "1.0.4"
        remotes = client.remotes.list()
        assert remotes[0].id == "pve-a"
    finally:
        client.close()

"""Live Proxmox API smoke tests.

These tests hit a real Proxmox node and are excluded from CI by default
(see ``markers`` in ``pyproject.toml`` and ``pytest -m live`` to opt in).

Required environment variables:

- ``PROXMOX_API_URL`` (e.g. ``https://10.0.30.91:8006``)
- ``PROXMOX_API_TOKEN_ID`` (e.g. ``root@pam!proxbox``)
- ``PROXMOX_API_TOKEN_SECRET``
"""

from __future__ import annotations

import os
from urllib.parse import urlsplit

import pytest

pytestmark = pytest.mark.live


@pytest.fixture
async def sdk():
    url = os.getenv("PROXMOX_API_URL")
    token_id = os.getenv("PROXMOX_API_TOKEN_ID")
    token_secret = os.getenv("PROXMOX_API_TOKEN_SECRET")
    if not (url and token_id and token_secret):
        pytest.skip(
            "PROXMOX_API_URL / PROXMOX_API_TOKEN_ID / PROXMOX_API_TOKEN_SECRET not set",
        )

    from proxmox_sdk.sdk import ProxmoxSDK
    from proxmox_sdk.sdk.auth.token import parse_token_id

    user, token_name = parse_token_id(token_id)
    parsed = urlsplit(url)
    host = parsed.hostname or url
    port = parsed.port

    instance = ProxmoxSDK(
        host=host,
        user=user,
        token_name=token_name,
        token_value=token_secret,
        service="PVE",
        backend="https",
        port=port,
        verify_ssl=False,
    )
    try:
        yield instance
    finally:
        await instance.close()


async def test_live_version_is_9_1(sdk) -> None:
    info = await sdk.version.get()
    version = (info or {}).get("version") or ""
    assert version.startswith("9.1"), f"expected Proxmox 9.1.x on live node, got {version!r}"

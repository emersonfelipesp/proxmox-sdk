"""Verify the auth/backend protocol split (ISP/LSP fix in S2).

After the split:

- ``TokenAuth`` satisfies :class:`AuthStrategy` (headers + cookies) but **not**
  :class:`EnsurableAuthStrategy` — it has no ``ensure_ready`` method.
- ``TicketAuth`` satisfies both protocols (it implements ``ensure_ready``).
- Only :class:`HttpsBackend` satisfies :class:`TicketCapableBackend`; other
  backends (mock, local pvesh, SSH) do not — instead of raising
  ``RuntimeError`` from :meth:`AbstractBackend.get_tokens` they simply lack
  the method.
"""

from __future__ import annotations

import asyncio

import pytest

from proxmox_sdk.sdk.auth.base import AuthStrategy, EnsurableAuthStrategy
from proxmox_sdk.sdk.auth.ticket import TicketAuth
from proxmox_sdk.sdk.auth.token import TokenAuth
from proxmox_sdk.sdk.backends.base import TicketCapableBackend
from proxmox_sdk.sdk.services import SERVICES


def test_token_auth_is_authstrategy_but_not_ensurable() -> None:
    auth = TokenAuth(
        user="root@pam",
        token_name="cli",
        token_value="secret",
        service_config=SERVICES["PVE"],
    )
    assert isinstance(auth, AuthStrategy)
    assert not isinstance(auth, EnsurableAuthStrategy)
    assert not hasattr(auth, "ensure_ready")


def test_ticket_auth_is_both_authstrategy_and_ensurable() -> None:
    auth = TicketAuth(
        username="root@pam",
        password="x",
        service_config=SERVICES["PVE"],
    )
    assert isinstance(auth, AuthStrategy)
    assert isinstance(auth, EnsurableAuthStrategy)


def test_mock_backend_is_not_ticket_capable() -> None:
    from proxmox_sdk.sdk.backends.mock import MockBackend

    backend = MockBackend(api_path_prefix=SERVICES["PVE"].api_path_prefix)
    assert not isinstance(backend, TicketCapableBackend)
    assert not hasattr(backend, "get_tokens")


def test_https_backend_is_ticket_capable() -> None:
    from proxmox_sdk.sdk.backends.https import HttpsBackend

    auth = TokenAuth(
        user="root@pam",
        token_name="cli",
        token_value="secret",
        service_config=SERVICES["PVE"],
    )
    backend = HttpsBackend(
        host="pve.example.com",
        service_config=SERVICES["PVE"],
        auth=auth,
    )
    assert isinstance(backend, TicketCapableBackend)


def test_proxmoxsdk_get_tokens_rejects_non_ticket_backend() -> None:
    from proxmox_sdk.sdk.api import ProxmoxSDK

    async def _run() -> None:
        sdk = ProxmoxSDK(backend="mock", service="PVE")
        try:
            with pytest.raises(RuntimeError, match="HTTPS backend"):
                await sdk.get_tokens()
        finally:
            await sdk.close()

    asyncio.run(_run())

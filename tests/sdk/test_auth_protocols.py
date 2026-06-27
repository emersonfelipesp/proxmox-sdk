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
from unittest.mock import AsyncMock, patch

import pytest

from proxmox_sdk.sdk.auth.base import AuthStrategy, EnsurableAuthStrategy
from proxmox_sdk.sdk.auth.ticket import TicketAuth
from proxmox_sdk.sdk.auth.token import TokenAuth
from proxmox_sdk.sdk.backends.base import TicketCapableBackend
from proxmox_sdk.sdk.exceptions import AuthenticationError, ResourceException
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


def test_https_backend_ticket_url_includes_api_path_prefix() -> None:
    """Regression: the password/ticket endpoint must be built under the
    service API prefix (``/api2/json/access/ticket``), not a bare
    ``/access/ticket`` — the latter returns HTTP 500 "no such file" on a
    real Proxmox node, surfacing as a JSONDecodeError during auth.
    """
    from proxmox_sdk.sdk.backends.https import HttpsBackend

    auth = TicketAuth(
        username="root@pam",
        password="secret",
        service_config=SERVICES["PVE"],
    )
    backend = HttpsBackend(
        host="pve.example.com",
        service_config=SERVICES["PVE"],
        auth=auth,
    )
    assert backend._ticket_url == "https://pve.example.com:8006/api2/json/access/ticket"


def test_https_backend_ticket_url_respects_reverse_proxy_prefix() -> None:
    """A reverse-proxy path prefix must sit in front of the API prefix:
    ``/proxmox/api2/json/access/ticket``.
    """
    from proxmox_sdk.sdk.backends.https import HttpsBackend

    auth = TicketAuth(
        username="root@pam",
        password="secret",
        service_config=SERVICES["PVE"],
    )
    backend = HttpsBackend(
        host="pve.example.com",
        service_config=SERVICES["PVE"],
        auth=auth,
        path_prefix="/proxmox",
    )
    assert backend._ticket_url == "https://pve.example.com:8006/proxmox/api2/json/access/ticket"


async def test_https_backend_sends_unquoted_proxmox_cookie() -> None:
    """Regression: aiohttp quotes cookie values containing special chars
    (``: @ = / +``) by default, but Proxmox rejects a *quoted* ``PVEAuthCookie``
    and 401s every authenticated request. The backend's session must use a
    ``quote_cookie=False`` jar so the ticket is sent verbatim.
    """
    from yarl import URL

    from proxmox_sdk.sdk.backends.https import HttpsBackend

    auth = TicketAuth(
        username="root@pam",
        password="secret",
        service_config=SERVICES["PVE"],
    )
    backend = HttpsBackend(
        host="pve.example.com",
        service_config=SERVICES["PVE"],
        auth=auth,
    )
    try:
        session = await backend._ensure_session()
        # A ticket exercising every character class Proxmox emits.
        ticket = "PVE:root@pam:6630ABCD::abcDEF123+/=ghIJ=="
        session.cookie_jar.update_cookies(
            {"PVEAuthCookie": ticket}, response_url=URL("https://pve.example.com")
        )
        rendered = (
            session.cookie_jar.filter_cookies(URL("https://pve.example.com/api2/json/nodes"))
            .output(header="", sep="")
            .strip()
        )
        assert rendered == f"PVEAuthCookie={ticket}"
        assert '"' not in rendered
    finally:
        await backend.close()


def test_ticket_auth_get_auth_tokens_requires_authenticated_state() -> None:
    auth = TicketAuth(
        username="root@pam",
        password="x",
        service_config=SERVICES["PVE"],
    )

    with pytest.raises(AuthenticationError):
        auth.get_auth_tokens()


def test_https_backend_get_tokens_requires_authenticated_state() -> None:
    from proxmox_sdk.sdk.backends.https import HttpsBackend

    async def _run() -> None:
        auth = TicketAuth(
            username="root@pam",
            password="x",
            service_config=SERVICES["PVE"],
        )
        backend = HttpsBackend(
            host="pve.example.com",
            service_config=SERVICES["PVE"],
            auth=auth,
            verify_ssl=False,
        )
        try:
            with (
                patch.object(backend, "_ensure_session", new_callable=AsyncMock) as ensure_session,
                patch.object(backend, "_ensure_authenticated", new_callable=AsyncMock),
            ):
                ensure_session.return_value = AsyncMock()

                with pytest.raises(AuthenticationError):
                    await backend.get_tokens()
        finally:
            await backend.close()

    asyncio.run(_run())


def test_resource_exception_exposes_typed_errors_dict() -> None:
    err = ResourceException(
        status_code=422,
        status_message="x",
        errors={"field": "required"},
    )

    assert isinstance(err.errors, dict)
    assert err.errors == {"field": "required"}


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

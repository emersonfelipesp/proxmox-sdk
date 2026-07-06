"""Regression tests for caller-supplied ("bring your own") aiohttp sessions.

``ProxmoxSDK(..., session=...)`` / ``HttpsBackend(..., session=...)`` let a
caller pass an existing :class:`aiohttp.ClientSession`. Two properties must hold:

1. The backend reuses the session verbatim and never closes it — its lifecycle
   belongs to the caller.
2. Password/ticket auth still works. This is subtle: an external session's
   cookie jar auto-stores the ``PVEAuthCookie`` from the ticket POST and
   re-quotes it on send, and a *quoted* ``PVEAuthCookie`` is rejected by Proxmox
   with 401. The backend therefore drops the auth cookie from the jar and sends
   it verbatim via an explicit ``Cookie`` header. A jar-stored cookie otherwise
   overrides the header (verified against a loopback server), so the purge is
   required — the header alone is not enough.
"""

from __future__ import annotations

import aiohttp
import pytest
from aiohttp import web
from yarl import URL

from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.auth.ticket import TicketAuth
from proxmox_sdk.sdk.backends.https import HttpsBackend
from proxmox_sdk.sdk.services import SERVICES

TICKET = "PVE:root@pam:6630ABCD::abcDEF123+/=ghIJ=="


def _make_backend(session: aiohttp.ClientSession | None = None) -> HttpsBackend:
    return HttpsBackend(
        host="pve.example.com",
        service_config=SERVICES["PVE"],
        auth=TicketAuth(
            username="root@pam",
            password="secret",
            service_config=SERVICES["PVE"],
        ),
        session=session,
    )


async def test_backend_reuses_external_session() -> None:
    """An external session is returned verbatim by _ensure_session()."""
    async with aiohttp.ClientSession() as external:
        backend = _make_backend(session=external)
        assert backend._session_external is True
        first = await backend._ensure_session()
        second = await backend._ensure_session()
        assert first is external
        assert second is external
        await backend.close()  # must not close the caller's session
        assert external.closed is False


async def test_backend_creates_and_owns_internal_session() -> None:
    """Without an external session the backend builds and closes its own."""
    backend = _make_backend(session=None)
    assert backend._session_external is False
    created = await backend._ensure_session()
    assert created.closed is False
    await backend.close()
    assert created.closed is True


async def test_close_is_noop_for_external_session() -> None:
    async with aiohttp.ClientSession() as external:
        backend = _make_backend(session=external)
        await backend._ensure_session()
        await backend.close()
        assert external.closed is False
        # The reference is retained so the backend stays usable.
        assert backend._session is external


async def test_purge_jar_auth_cookie_removes_only_auth_cookie() -> None:
    """Purging drops PVEAuthCookie but leaves unrelated caller cookies intact."""
    async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as external:
        external.cookie_jar.update_cookies(
            {"PVEAuthCookie": TICKET, "other": "keep-me"},
            response_url=URL("https://pve.example.com"),
        )
        backend = _make_backend(session=external)
        backend._purge_jar_auth_cookie(external)
        remaining = {c.key for c in external.cookie_jar}
        assert "PVEAuthCookie" not in remaining
        assert "other" in remaining


async def test_external_session_ticket_auth_sends_unquoted_cookie(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """End-to-end: a caller session whose jar stores the ticket must still send
    the ``PVEAuthCookie`` **unquoted** on authenticated requests.

    Uses a plain-HTTP loopback (URL builder patched to http) so the real aiohttp
    session, cookie jar, ticket POST, purge, and header path all execute. The
    caller session uses an ``unsafe=True`` jar so it stores the loopback IP
    cookie, reproducing the real-hostname behaviour where the jar would
    otherwise re-quote and clobber the header.
    """
    captured: dict[str, str] = {}

    async def handle_ticket(request: web.Request) -> web.Response:
        resp = web.json_response({"data": {"ticket": TICKET, "CSRFPreventionToken": "csrf:xyz"}})
        resp.set_cookie("PVEAuthCookie", TICKET)  # jar auto-stores this
        return resp

    async def handle_nodes(request: web.Request) -> web.Response:
        captured["cookie"] = request.headers.get("Cookie", "<none>")
        return web.json_response({"data": [{"node": "pve1"}]})

    app = web.Application()
    app.router.add_post("/api2/json/access/ticket", handle_ticket)
    app.router.add_get("/api2/json/nodes", handle_nodes)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]  # type: ignore[union-attr]

    monkeypatch.setattr(
        "proxmox_sdk.sdk.backends.https._build_base_url",
        lambda host, prt, path_prefix="": f"http://{host}:{prt}",
    )

    try:
        external = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True))
        async with ProxmoxSDK(
            host="127.0.0.1",
            user="root@pam",
            password="secret",
            port=port,
            verify_ssl=False,
            session=external,
        ) as proxmox:
            nodes = await proxmox.nodes.get()

        assert nodes == [{"node": "pve1"}]  # auth succeeded end-to-end
        assert captured["cookie"] == f"PVEAuthCookie={TICKET}"
        assert '"' not in captured["cookie"]  # NOT quoted
        # The SDK context exit must not close the caller-owned session.
        assert external.closed is False
    finally:
        await external.close()
        await runner.cleanup()

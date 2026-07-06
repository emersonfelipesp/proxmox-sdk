"""Regression tests for the v0.0.13 review fixes.

Covers:
- negative retry-setting validation on the HTTPS backend
- idempotent close on the synchronous SDK
- SSRF guard on download checksum auto-discovery
- typed AuthenticationError on a non-JSON ticket response
"""

from __future__ import annotations

import aiohttp
import pytest
from aiohttp import web

from proxmox_sdk.sdk.auth.ticket import TicketAuth
from proxmox_sdk.sdk.backends.https import HttpsBackend
from proxmox_sdk.sdk.exceptions import AuthenticationError
from proxmox_sdk.sdk.services import SERVICES
from proxmox_sdk.sdk.sync import SyncProxmoxSDK
from proxmox_sdk.sdk.tools.files import Files, _is_safe_probe_url


def _ticket_auth() -> TicketAuth:
    return TicketAuth(username="root@pam", password="secret", service_config=SERVICES["PVE"])


# --------------------------------------------------------------------------
# Negative retry settings must fail fast (previously tripped a later assertion)
# --------------------------------------------------------------------------
@pytest.mark.parametrize("kwargs", [{"max_retries": -1}, {"retry_backoff": -0.5}])
def test_https_backend_rejects_negative_retry_settings(kwargs: dict[str, float]) -> None:
    with pytest.raises(ValueError):
        HttpsBackend(
            host="pve.example.com",
            service_config=SERVICES["PVE"],
            auth=_ticket_auth(),
            **kwargs,
        )


def test_https_backend_accepts_zero_retries() -> None:
    backend = HttpsBackend(
        host="pve.example.com",
        service_config=SERVICES["PVE"],
        auth=_ticket_auth(),
        max_retries=0,
    )
    assert backend._max_retries == 0


# --------------------------------------------------------------------------
# Sync SDK close must be idempotent
# --------------------------------------------------------------------------
def test_sync_sdk_close_is_idempotent() -> None:
    sdk = SyncProxmoxSDK(backend="mock")
    sdk.close()
    sdk.close()  # second call must be a no-op, not raise on a closed loop


# --------------------------------------------------------------------------
# SSRF guard on checksum auto-discovery
# --------------------------------------------------------------------------
@pytest.mark.parametrize(
    "url",
    [
        "http://169.254.169.254/latest/meta-data/foo.iso",  # cloud metadata
        "http://127.0.0.1/x.iso",
        "https://localhost/x.iso",
        "http://10.0.0.5/x.iso",
        "http://192.168.1.1/x.iso",
        "http://172.16.5.5/x.iso",
        "http://[::1]/x.iso",
        "http://[::ffff:169.254.169.254]/x.iso",  # IPv4-mapped link-local
        "ftp://example.com/x.iso",  # non-HTTP scheme
        "file:///etc/passwd",
    ],
)
def test_unsafe_probe_urls_blocked(url: str) -> None:
    assert _is_safe_probe_url(url) is False


@pytest.mark.parametrize(
    "url",
    [
        "https://cdn.example.com/debian.iso",
        "http://mirror.example.org/ubuntu.iso",
        "https://8.8.8.8/x.iso",  # public IP literal
    ],
)
def test_safe_probe_urls_allowed(url: str) -> None:
    assert _is_safe_probe_url(url) is True


async def test_discover_checksum_skips_unsafe_url() -> None:
    """The guard must short-circuit before any outbound request is attempted."""
    files = Files.__new__(Files)  # bypass constructor; unsafe path uses no state
    result = await files._discover_checksum("http://169.254.169.254/meta.iso")
    assert result is None


# --------------------------------------------------------------------------
# Non-JSON ticket response -> typed AuthenticationError (not a raw decode error)
# --------------------------------------------------------------------------
async def test_ticket_auth_non_json_response_raises_auth_error() -> None:
    async def handle_ticket(request: web.Request) -> web.Response:
        return web.Response(
            status=502,
            text="<html><body>502 Bad Gateway</body></html>",
            content_type="text/html",
        )

    app = web.Application()
    app.router.add_post("/api2/json/access/ticket", handle_ticket)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]  # type: ignore[union-attr]

    try:
        auth = _ticket_auth()
        async with aiohttp.ClientSession() as session:
            with pytest.raises(AuthenticationError):
                await auth.authenticate(session, f"http://127.0.0.1:{port}/api2/json/access/ticket")
    finally:
        await runner.cleanup()

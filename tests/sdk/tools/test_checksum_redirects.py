"""Redirect-refusal tests for SDK-host checksum discovery probes."""

from __future__ import annotations

import ipaddress
import socket
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Literal

import aiohttp
import pytest
from aiohttp import web
from aiohttp.abc import AbstractResolver, ResolveResult

from proxmox_sdk.sdk.exceptions import ProxmoxRedirectError
from proxmox_sdk.sdk.tools.files import (
    _fetch_hash_from_sums,
    _fetch_single_hash,
    _is_safe_probe_url,
)


class _PublicOriginResolver(AbstractResolver):
    """Resolve the synthetic public hostname to the loopback test server."""

    async def resolve(
        self,
        host: str,
        port: int = 0,
        family: socket.AddressFamily = socket.AF_INET,
    ) -> list[ResolveResult]:
        return [
            ResolveResult(
                hostname=host,
                host="127.0.0.1",
                port=port,
                family=family,
                proto=0,
                flags=0,
            )
        ]

    async def close(self) -> None:
        return None


@asynccontextmanager
async def _run_server(
    app: web.Application,
    *,
    host: str = "127.0.0.1",
) -> AsyncIterator[int]:
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]  # type: ignore[union-attr]
    try:
        yield port
    finally:
        await runner.cleanup()


_FALLBACK_PRIVATE_ADDRESS = "10.255.255.254"


def _private_interface_address() -> str:
    """Return a private, non-loopback IPv4 address to use as a redirect target.

    Prefer the host's own default-route interface when it is private, so the
    catch-all target server bound on ``0.0.0.0`` is genuinely reachable there.
    A host whose default interface carries a public address falls back to a
    documented RFC 1918 literal; the redirect must be refused before any
    connection is attempted, so reachability of the fallback is irrelevant,
    and the short client timeout in the test turns a regression into a fast
    failure rather than a hang.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as probe:
        probe.connect(("192.0.2.1", 9))
        address = probe.getsockname()[0]
    parsed = ipaddress.ip_address(address)
    if parsed.is_private and not parsed.is_loopback:
        return address
    return _FALLBACK_PRIVATE_ADDRESS


@pytest.mark.asyncio
@pytest.mark.parametrize("strategy", ["sibling", "sums"])
@pytest.mark.parametrize("destination", ["loopback", "private"])
async def test_public_checksum_probe_refuses_internal_redirect(
    strategy: Literal["sibling", "sums"],
    destination: Literal["loopback", "private"],
) -> None:
    target_requests = 0
    origin_requests = 0

    async def capture_target(_request: web.Request) -> web.Response:
        nonlocal target_requests
        target_requests += 1
        return web.Response(text="target contacted")

    target_app = web.Application()
    target_app.router.add_route("*", "/{tail:.*}", capture_target)

    async with _run_server(target_app, host="0.0.0.0") as target_port:
        destination_host = (
            "127.0.0.1" if destination == "loopback" else _private_interface_address()
        )
        redirect_url = f"http://{destination_host}:{target_port}/capture"

        async def redirect_probe(_request: web.Request) -> web.Response:
            nonlocal origin_requests
            origin_requests += 1
            return web.Response(
                status=302,
                body=b"redirect body must not be parsed as a checksum",
                headers={"Location": redirect_url},
            )

        origin_app = web.Application()
        origin_app.router.add_route("*", "/{tail:.*}", redirect_probe)

        async with _run_server(origin_app) as origin_port:
            public_url = f"http://cdn.example.com:{origin_port}/image.iso.sha256"
            assert _is_safe_probe_url(public_url) is True
            connector = aiohttp.TCPConnector(resolver=_PublicOriginResolver())
            timeout = aiohttp.ClientTimeout(total=5)
            async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
                with pytest.raises(ProxmoxRedirectError) as exc_info:
                    if strategy == "sibling":
                        await _fetch_single_hash(session, public_url)
                    else:
                        await _fetch_hash_from_sums(session, public_url, "image.iso")

    assert exc_info.value.status == 302
    assert exc_info.value.location_host == destination_host
    assert origin_requests == 1
    assert target_requests == 0

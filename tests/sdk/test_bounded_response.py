"""Contracts for pre-materialization SDK response limits."""

from __future__ import annotations

import gzip
import io
from collections.abc import AsyncIterator
from typing import Any

import pytest
from aiohttp import web

from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.backends.https import HttpsBackend
from proxmox_sdk.sdk.exceptions import (
    AuthenticationError,
    BackendNotAvailableError,
    ResponseTooLargeError,
    UnsupportedResponseEncodingError,
)
from proxmox_sdk.sdk.resource import ProxmoxResource


class _Chunks:
    def __init__(self, chunks: list[bytes]) -> None:
        self.chunks = chunks
        self.consumed = 0

    async def iter_chunked(self, _size: int) -> AsyncIterator[bytes]:
        for chunk in self.chunks:
            self.consumed += 1
            yield chunk


class _Response:
    def __init__(
        self,
        chunks: list[bytes],
        *,
        content_length: int | None = None,
        status: int = 200,
        content_encoding: str = "identity",
    ) -> None:
        self.content = _Chunks(chunks)
        self.content_length = content_length
        self.status = status
        self.reason = "OK" if status < 400 else "Bad Request"
        self.headers = {"content-encoding": content_encoding}


class _UnboundedBackend:
    async def request(self, *_args: object, **_kwargs: object) -> object:
        return {}

    async def close(self) -> None:
        return None


class _BoundedBackend(_UnboundedBackend):
    def __init__(self) -> None:
        self.call: tuple[str, str, int, dict[str, Any] | None] | None = None

    async def request_bounded(
        self,
        method: str,
        path: str,
        *,
        max_response_bytes: int,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> object:
        assert data is None
        self.call = (method, path, max_response_bytes, params)
        return {"ok": True}


@pytest.mark.asyncio
async def test_exact_limit_json_response_succeeds() -> None:
    response = _Response([b'{"data":[1]}'], content_length=12)

    result = await HttpsBackend._read_bounded_json(object(), response, 12)

    assert result == {"data": [1]}
    assert response.content.consumed == 1


@pytest.mark.asyncio
async def test_declared_oversize_fails_before_body_iteration() -> None:
    response = _Response([b"secret-response"], content_length=15)

    with pytest.raises(ResponseTooLargeError, match="8-byte limit") as exc_info:
        await HttpsBackend._read_bounded_json(object(), response, 8)

    assert response.content.consumed == 0
    assert "secret-response" not in str(exc_info.value)


@pytest.mark.asyncio
async def test_chunked_oversize_stops_before_later_chunks() -> None:
    response = _Response([b"1234", b"56789", b"never-read"])

    with pytest.raises(ResponseTooLargeError):
        await HttpsBackend._read_bounded_json(object(), response, 8)

    assert response.content.consumed == 2


@pytest.mark.asyncio
async def test_compressed_response_is_rejected_before_iteration() -> None:
    response = _Response(
        [b"compressed-secret"],
        content_length=17,
        content_encoding="gzip",
    )

    with pytest.raises(UnsupportedResponseEncodingError, match="identity"):
        await HttpsBackend._read_bounded_json(object(), response, 64)

    assert response.content.consumed == 0


@pytest.mark.asyncio
async def test_real_transport_disables_decompression_and_requests_identity(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured: dict[str, str] = {}

    async def handle_version(request: web.Request) -> web.Response:
        captured["accept_encoding"] = request.headers.get("Accept-Encoding", "")
        body = gzip.compress(b'{"data":"' + b"x" * 4096 + b'"}')
        return web.Response(body=body, headers={"Content-Encoding": "gzip"})

    app = web.Application()
    app.router.add_get("/api2/json/version", handle_version)
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
        async with ProxmoxSDK(
            host="127.0.0.1",
            user="monitoring@pve",
            token_name="metrics",
            token_value="secret",
            port=port,
            verify_ssl=False,
        ) as proxmox:
            with pytest.raises(UnsupportedResponseEncodingError):
                await proxmox.version.get_bounded(64)
    finally:
        await runner.cleanup()

    assert captured["accept_encoding"] == "identity"


@pytest.mark.asyncio
async def test_password_auth_rejects_compressed_ticket_before_bounded_get(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    dispatched = False

    async def handle_ticket(_request: web.Request) -> web.Response:
        ticket = b'{"data":{"ticket":"PVE:user@pam:ticket","CSRFPreventionToken":"csrf"}}'
        return web.Response(body=gzip.compress(ticket), headers={"Content-Encoding": "gzip"})

    async def handle_version(_request: web.Request) -> web.Response:
        nonlocal dispatched
        dispatched = True
        return web.json_response({"data": {"version": "9.0"}})

    app = web.Application()
    app.router.add_post("/api2/json/access/ticket", handle_ticket)
    app.router.add_get("/api2/json/version", handle_version)
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
        async with ProxmoxSDK(
            host="127.0.0.1",
            user="user@pam",
            password="secret",
            port=port,
            verify_ssl=False,
        ) as proxmox:
            with pytest.raises(AuthenticationError, match="encoding is unsupported"):
                await proxmox.version.get_bounded(1024)
    finally:
        await runner.cleanup()

    assert dispatched is False


def test_unbounded_request_preserves_session_decompression_default() -> None:
    backend = object.__new__(HttpsBackend)
    backend._ssl = True
    backend._timeout = None
    backend._proxy = None
    common = ("GET", "https://pve.test/version", {}, {}, None, None)

    unbounded = backend._request_options(*common, None)
    bounded = backend._request_options(*common, 1024)

    assert "auto_decompress" not in unbounded
    assert bounded["auto_decompress"] is False


@pytest.mark.asyncio
async def test_bounded_backend_rejects_upload_before_dispatch() -> None:
    with pytest.raises(ValueError, match="GET requests only"):
        await HttpsBackend.request_bounded(
            object(),
            "POST",
            "/api2/json/upload",
            max_response_bytes=64,
            data={"file": io.BytesIO(b"payload")},
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_limit", [float("nan"), float("inf"), 1.5, True, 0, -1])
async def test_backend_rejects_invalid_limits_before_authentication(
    invalid_limit: object,
) -> None:
    with pytest.raises(ValueError, match="positive integer"):
        await HttpsBackend.request_bounded(
            object(),
            "GET",
            "/api2/json/version",
            max_response_bytes=invalid_limit,  # type: ignore[arg-type]
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("invalid_limit", [0, -1, True, 1.5])
async def test_resource_rejects_invalid_limits_before_dispatch(
    invalid_limit: object,
) -> None:
    backend = _BoundedBackend()
    resource = ProxmoxResource("/api2/json/cluster/metrics/export", backend)

    with pytest.raises(ValueError, match="positive integer"):
        await resource.get_bounded(invalid_limit)  # type: ignore[arg-type]

    assert backend.call is None


@pytest.mark.asyncio
async def test_resource_dispatches_bound_and_filtered_parameters() -> None:
    backend = _BoundedBackend()
    resource = ProxmoxResource("/api2/json/cluster/metrics/export", backend)

    result = await resource.get_bounded(4096, history=True, start_time=None)

    assert result == {"ok": True}
    assert backend.call == (
        "GET",
        "/api2/json/cluster/metrics/export",
        4096,
        {"history": True},
    )


@pytest.mark.asyncio
async def test_resource_rejects_backend_without_bounded_capability() -> None:
    resource = ProxmoxResource("/api2/json/cluster/metrics/export", _UnboundedBackend())

    with pytest.raises(BackendNotAvailableError, match="bounded responses"):
        await resource.get_bounded(4096)

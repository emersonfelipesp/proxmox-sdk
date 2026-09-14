"""Contracts for pre-materialization SDK response limits."""

from __future__ import annotations

import gzip
import io
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import aiohttp
import pytest
from aiohttp import web
from yarl import URL

from proxmox_sdk.sdk.api import ProxmoxSDK
from proxmox_sdk.sdk.backends.https import HttpsBackend
from proxmox_sdk.sdk.exceptions import (
    AuthenticationError,
    BackendNotAvailableError,
    ProxmoxRedirectError,
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


class _UnreadableResponse:
    def __init__(self, status: int, location: str | None = None) -> None:
        self.status = status
        self.reason = "redirect body must not be read"
        self.headers = {"Location": location} if location else {}

    async def json(self, **_kwargs: object) -> object:
        raise AssertionError("redirect JSON body was read")

    async def text(self) -> str:
        raise AssertionError("redirect text body was read")


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


@asynccontextmanager
async def _run_server(app: web.Application) -> AsyncIterator[tuple[str, int]]:
    host = "127.0.0.1"
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]  # type: ignore[union-attr]
    try:
        yield host, port
    finally:
        await runner.cleanup()


def _catch_all_app(captured: list[dict[str, Any]]) -> web.Application:
    async def capture(request: web.Request) -> web.Response:
        captured.append(
            {
                "method": request.method,
                "path": request.path,
                "authorization": request.headers.get("Authorization"),
                "cookie": request.cookies.get("PVEAuthCookie"),
                "csrf": request.headers.get("CSRFPreventionToken"),
                "body": await request.read(),
            }
        )
        return web.json_response({"data": {"captured": True}})

    app = web.Application()
    app.router.add_route("*", "/{tail:.*}", capture)
    return app


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


def test_request_options_disable_redirects_and_preserve_decompression_defaults() -> None:
    backend = object.__new__(HttpsBackend)
    backend._ssl = True
    backend._timeout = None
    backend._proxy = None
    common = ("GET", "https://pve.test/version", {}, {}, None, None)

    unbounded = backend._request_options(*common, None)
    bounded = backend._request_options(*common, 1024)

    assert unbounded["allow_redirects"] is False
    assert bounded["allow_redirects"] is False
    assert "auto_decompress" not in unbounded
    assert bounded["auto_decompress"] is False


@pytest.mark.asyncio
async def test_304_not_modified_is_rejected_as_redirect() -> None:
    response = _UnreadableResponse(304)

    with pytest.raises(ProxmoxRedirectError) as exc_info:
        await HttpsBackend._handle_response(  # type: ignore[arg-type]
            object(),
            response,
            "GET",
            "/api2/json/version",
        )

    assert exc_info.value.status == 304


@pytest.mark.asyncio
async def test_redirect_response_body_is_never_consumed() -> None:
    response = _UnreadableResponse(308, "https://target.example/capture")

    with pytest.raises(ProxmoxRedirectError) as exc_info:
        await HttpsBackend._handle_response(  # type: ignore[arg-type]
            object(),
            response,
            "POST",
            "/api2/json/nodes",
        )

    assert exc_info.value.status == 308
    assert exc_info.value.location_host == "target.example"


@pytest.mark.asyncio
async def test_bounded_cross_origin_redirect_does_not_forward_secrets(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    origin_headers: dict[str, str | None] = {}
    target_requests: list[dict[str, str | None]] = []

    async def handle_target(request: web.Request) -> web.Response:
        target_requests.append(
            {
                "cookie": request.cookies.get("PVEAuthCookie"),
                "csrf": request.headers.get("CSRFPreventionToken"),
            }
        )
        return web.json_response({"data": {"version": "stolen"}})

    target_app = web.Application()
    target_app.router.add_route("*", "/{tail:.*}", handle_target)

    async with _run_server(target_app) as (target_host, target_port):
        redirect_url = f"http://{target_host}:{target_port}/capture?ticket=redirect-secret"

        async def handle_origin(request: web.Request) -> web.Response:
            origin_headers["cookie"] = request.cookies.get("PVEAuthCookie")
            origin_headers["csrf"] = request.headers.get("CSRFPreventionToken")
            return web.Response(status=302, headers={"Location": redirect_url})

        origin_app = web.Application()
        origin_app.router.add_get("/api2/json/version", handle_origin)

        async with _run_server(origin_app) as (origin_host, origin_port):
            monkeypatch.setattr(
                "proxmox_sdk.sdk.backends.https._build_base_url",
                lambda host, prt, path_prefix="": f"http://{host}:{prt}",
            )
            jar = aiohttp.CookieJar(unsafe=True)
            async with aiohttp.ClientSession(
                cookie_jar=jar,
                headers={"CSRFPreventionToken": "csrf-secret"},
            ) as session:
                jar.update_cookies(
                    {"PVEAuthCookie": "auth-ticket"},
                    response_url=URL(f"http://{origin_host}:{origin_port}"),
                )
                async with ProxmoxSDK(
                    host=origin_host,
                    user="monitoring@pve",
                    token_name="metrics",
                    token_value="secret",
                    port=origin_port,
                    verify_ssl=False,
                    session=session,
                ) as proxmox:
                    with pytest.raises(ProxmoxRedirectError) as exc_info:
                        await proxmox.version.get_bounded(1024)

    assert exc_info.value.status == 302
    assert exc_info.value.location_host == target_host
    assert "redirect-secret" not in str(exc_info.value)
    assert origin_headers == {"cookie": "auth-ticket", "csrf": "csrf-secret"}
    assert target_requests == []


@pytest.mark.asyncio
async def test_bounded_same_origin_redirect_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    redirected_requests = 0

    async def handle_origin(_request: web.Request) -> web.Response:
        return web.Response(
            status=301,
            headers={"Location": "/api2/json/redirected"},
        )

    async def handle_redirected(_request: web.Request) -> web.Response:
        nonlocal redirected_requests
        redirected_requests += 1
        return web.json_response({"data": {"version": "redirected"}})

    app = web.Application()
    app.router.add_get("/api2/json/version", handle_origin)
    app.router.add_get("/api2/json/redirected", handle_redirected)

    async with _run_server(app) as (host, port):
        monkeypatch.setattr(
            "proxmox_sdk.sdk.backends.https._build_base_url",
            lambda hostname, prt, path_prefix="": f"http://{hostname}:{prt}",
        )
        async with ProxmoxSDK(
            host=host,
            user="monitoring@pve",
            token_name="metrics",
            token_value="secret",
            port=port,
            verify_ssl=False,
        ) as proxmox:
            with pytest.raises(ProxmoxRedirectError) as exc_info:
                await proxmox.version.get_bounded(1024)

    assert exc_info.value.status == 301
    assert exc_info.value.location_host is None
    assert redirected_requests == 0


@pytest.mark.asyncio
async def test_redirect_is_not_retried(monkeypatch: pytest.MonkeyPatch) -> None:
    request_count = 0

    async def handle_origin(_request: web.Request) -> web.Response:
        nonlocal request_count
        request_count += 1
        return web.Response(status=307, headers={"Location": "/api2/json/version"})

    app = web.Application()
    app.router.add_get("/api2/json/version", handle_origin)

    async with _run_server(app) as (host, port):
        monkeypatch.setattr(
            "proxmox_sdk.sdk.backends.https._build_base_url",
            lambda hostname, prt, path_prefix="": f"http://{hostname}:{prt}",
        )
        async with ProxmoxSDK(
            host=host,
            user="monitoring@pve",
            token_name="metrics",
            token_value="secret",
            port=port,
            verify_ssl=False,
            max_retries=3,
            retry_backoff=0,
        ) as proxmox:
            with pytest.raises(ProxmoxRedirectError) as exc_info:
                await proxmox.version.get_bounded(1024)

    assert exc_info.value.status == 307
    assert request_count == 1


@pytest.mark.asyncio
async def test_unbounded_token_request_refuses_cross_origin_307_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    origin_requests: list[dict[str, Any]] = []
    target_requests: list[dict[str, Any]] = []

    async with _run_server(_catch_all_app(target_requests)) as (target_host, target_port):
        redirect_url = f"http://{target_host}:{target_port}/capture"

        async def handle_origin(request: web.Request) -> web.Response:
            origin_requests.append(
                {
                    "authorization": request.headers.get("Authorization"),
                }
            )
            return web.Response(status=307, headers={"Location": redirect_url})

        origin_app = web.Application()
        origin_app.router.add_get("/api2/json/nodes", handle_origin)

        async with _run_server(origin_app) as (origin_host, origin_port):
            monkeypatch.setattr(
                "proxmox_sdk.sdk.backends.https._build_base_url",
                lambda host, prt, path_prefix="": f"http://{host}:{prt}",
            )
            async with ProxmoxSDK(
                host=origin_host,
                user="monitoring@pve",
                token_name="metrics",
                token_value="token-secret",
                port=origin_port,
                verify_ssl=False,
                max_retries=3,
                retry_backoff=0,
            ) as proxmox:
                with pytest.raises(ProxmoxRedirectError) as exc_info:
                    await proxmox.nodes.get()

    assert exc_info.value.status == 307
    assert len(origin_requests) == 1
    assert origin_requests[0]["authorization"] == (
        "PVEAPIToken=monitoring@pve!metrics=token-secret"
    )
    assert target_requests == []


@pytest.mark.asyncio
async def test_unbounded_ticket_request_refuses_cross_origin_308_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ticket_requests = 0
    origin_requests: list[dict[str, Any]] = []
    target_requests: list[dict[str, Any]] = []

    async with _run_server(_catch_all_app(target_requests)) as (target_host, target_port):
        redirect_url = f"http://{target_host}:{target_port}/capture"

        async def handle_ticket(request: web.Request) -> web.Response:
            nonlocal ticket_requests
            ticket_requests += 1
            form = await request.post()
            assert form["password"] == "ticket-secret"
            return web.json_response(
                {
                    "data": {
                        "ticket": "PVE:user@pam:auth-ticket",
                        "CSRFPreventionToken": "csrf-secret",
                    }
                }
            )

        async def handle_origin(request: web.Request) -> web.Response:
            origin_requests.append(
                {
                    "cookie": request.cookies.get("PVEAuthCookie"),
                    "csrf": request.headers.get("CSRFPreventionToken"),
                    "body": await request.json(),
                }
            )
            return web.Response(status=308, headers={"Location": redirect_url})

        origin_app = web.Application()
        origin_app.router.add_post("/api2/json/access/ticket", handle_ticket)
        origin_app.router.add_post("/api2/json/nodes", handle_origin)

        async with _run_server(origin_app) as (origin_host, origin_port):
            monkeypatch.setattr(
                "proxmox_sdk.sdk.backends.https._build_base_url",
                lambda host, prt, path_prefix="": f"http://{host}:{prt}",
            )
            async with ProxmoxSDK(
                host=origin_host,
                user="user@pam",
                password="ticket-secret",
                port=origin_port,
                verify_ssl=False,
                max_retries=3,
                retry_backoff=0,
            ) as proxmox:
                with pytest.raises(ProxmoxRedirectError) as exc_info:
                    await proxmox.nodes.post(password="request-body-secret")

    assert exc_info.value.status == 308
    assert ticket_requests == 1
    assert len(origin_requests) == 1
    assert origin_requests[0] == {
        "cookie": "PVE:user@pam:auth-ticket",
        "csrf": "csrf-secret",
        "body": {"password": "request-body-secret"},
    }
    assert target_requests == []


@pytest.mark.asyncio
async def test_multipart_upload_refuses_cross_origin_308_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    origin_requests: list[dict[str, Any]] = []
    target_requests: list[dict[str, Any]] = []

    async with _run_server(_catch_all_app(target_requests)) as (target_host, target_port):
        redirect_url = f"http://{target_host}:{target_port}/capture"

        async def handle_origin(request: web.Request) -> web.Response:
            origin_requests.append(
                {
                    "authorization": request.headers.get("Authorization"),
                    "body": await request.read(),
                }
            )
            return web.Response(status=308, headers={"Location": redirect_url})

        origin_app = web.Application()
        origin_app.router.add_post(
            "/api2/json/nodes/pve/storage/local/upload",
            handle_origin,
        )

        async with _run_server(origin_app) as (origin_host, origin_port):
            monkeypatch.setattr(
                "proxmox_sdk.sdk.backends.https._build_base_url",
                lambda host, prt, path_prefix="": f"http://{host}:{prt}",
            )
            async with ProxmoxSDK(
                host=origin_host,
                user="monitoring@pve",
                token_name="metrics",
                token_value="upload-token-secret",
                port=origin_port,
                verify_ssl=False,
                max_retries=3,
                retry_backoff=0,
            ) as proxmox:
                with pytest.raises(ProxmoxRedirectError) as exc_info:
                    await (
                        proxmox.nodes("pve")
                        .storage("local")
                        .upload.post(
                            content="iso",
                            filename=io.BytesIO(b"multipart-body-secret"),
                        )
                    )

    assert exc_info.value.status == 308
    assert len(origin_requests) == 1
    assert origin_requests[0]["authorization"] == (
        "PVEAPIToken=monitoring@pve!metrics=upload-token-secret"
    )
    assert b"multipart-body-secret" in origin_requests[0]["body"]
    assert target_requests == []


@pytest.mark.asyncio
async def test_ticket_authentication_redirect_is_refused(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    ticket_requests = 0
    target_requests = 0

    async def handle_target(_request: web.Request) -> web.Response:
        nonlocal target_requests
        target_requests += 1
        return web.json_response({"data": {"ticket": "stolen", "CSRFPreventionToken": "stolen"}})

    target_app = web.Application()
    target_app.router.add_route("*", "/{tail:.*}", handle_target)

    async with _run_server(target_app) as (target_host, target_port):
        redirect_url = f"http://{target_host}:{target_port}/capture?ticket=redirect-secret"

        async def handle_ticket(_request: web.Request) -> web.Response:
            nonlocal ticket_requests
            ticket_requests += 1
            return web.Response(status=307, headers={"Location": redirect_url})

        origin_app = web.Application()
        origin_app.router.add_post("/api2/json/access/ticket", handle_ticket)

        async with _run_server(origin_app) as (origin_host, origin_port):
            monkeypatch.setattr(
                "proxmox_sdk.sdk.backends.https._build_base_url",
                lambda host, prt, path_prefix="": f"http://{host}:{prt}",
            )
            async with ProxmoxSDK(
                host=origin_host,
                user="user@pam",
                password="secret",
                port=origin_port,
                verify_ssl=False,
            ) as proxmox:
                with pytest.raises(ProxmoxRedirectError) as exc_info:
                    await proxmox.version.get_bounded(1024)

    assert exc_info.value.status == 307
    assert exc_info.value.location_host == target_host
    assert "redirect-secret" not in str(exc_info.value)
    assert ticket_requests == 1
    assert target_requests == 0


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

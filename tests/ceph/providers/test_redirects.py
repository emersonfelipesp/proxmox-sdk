"""Live redirect-refusal tests for direct Ceph provider transports."""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import pytest
from aiohttp import web

from proxmox_sdk.ceph.providers.dashboard import DashboardCephClient
from proxmox_sdk.ceph.providers.rbd import RBDClient
from proxmox_sdk.ceph.providers.rgw import RGWAdminClient
from proxmox_sdk.sdk.exceptions import ProxmoxRedirectError


@asynccontextmanager
async def _run_server(app: web.Application) -> AsyncIterator[str]:
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", 0)
    await site.start()
    port = site._server.sockets[0].getsockname()[1]  # type: ignore[union-attr]
    try:
        yield f"http://127.0.0.1:{port}"
    finally:
        await runner.cleanup()


def _target_app(captured: list[dict[str, Any]]) -> web.Application:
    async def capture(request: web.Request) -> web.Response:
        captured.append(
            {
                "method": request.method,
                "path": request.path,
                "authorization": request.headers.get("Authorization"),
                "body": await request.read(),
            }
        )
        return web.json_response({"captured": True})

    app = web.Application()
    app.router.add_route("*", "/{tail:.*}", capture)
    return app


async def test_dashboard_login_redirect_does_not_forward_credentials() -> None:
    target_requests: list[dict[str, Any]] = []
    origin_requests = 0

    async with _run_server(_target_app(target_requests)) as target_url:

        async def redirect_login(request: web.Request) -> web.Response:
            nonlocal origin_requests
            origin_requests += 1
            assert await request.json() == {"username": "admin", "password": "login-secret"}
            return web.Response(status=307, headers={"Location": f"{target_url}/capture"})

        origin_app = web.Application()
        origin_app.router.add_post("/api/auth", redirect_login)

        async with _run_server(origin_app) as origin_url:
            client = DashboardCephClient(
                origin_url,
                username="admin",
                password="login-secret",
                verify_ssl=False,
            )
            try:
                with pytest.raises(ProxmoxRedirectError, match="307"):
                    await client.login()
            finally:
                await client.close()

    assert origin_requests == 1
    assert target_requests == []


async def test_rbd_redirect_does_not_forward_dashboard_bearer_token() -> None:
    target_requests: list[dict[str, Any]] = []
    origin_requests = 0

    async with _run_server(_target_app(target_requests)) as target_url:

        async def redirect_rbd(request: web.Request) -> web.Response:
            nonlocal origin_requests
            origin_requests += 1
            assert request.headers["Authorization"] == "Bearer dashboard-secret"
            return web.Response(status=307, headers={"Location": f"{target_url}/capture"})

        origin_app = web.Application()
        origin_app.router.add_get("/api/block/image", redirect_rbd)

        async with _run_server(origin_app) as origin_url:
            dashboard = DashboardCephClient(
                origin_url,
                token="dashboard-secret",
                verify_ssl=False,
            )
            client = RBDClient(dashboard)
            try:
                with pytest.raises(ProxmoxRedirectError, match="307"):
                    await client.list_images("rbd")
            finally:
                await dashboard.close()

    assert origin_requests == 1
    assert target_requests == []


async def test_rgw_redirect_does_not_forward_authorization_header() -> None:
    target_requests: list[dict[str, Any]] = []
    origin_requests = 0

    async with _run_server(_target_app(target_requests)) as target_url:

        async def redirect_rgw(request: web.Request) -> web.Response:
            nonlocal origin_requests
            origin_requests += 1
            assert request.headers["Authorization"].startswith("AWS access-key:")
            return web.Response(status=307, headers={"Location": f"{target_url}/capture"})

        origin_app = web.Application()
        origin_app.router.add_get("/admin/user", redirect_rgw)

        async with _run_server(origin_app) as origin_url:
            client = RGWAdminClient(
                origin_url,
                access_key="access-key",
                secret_key="rgw-secret",
                verify_ssl=False,
            )
            try:
                with pytest.raises(ProxmoxRedirectError, match="307"):
                    await client.get_user("alice")
            finally:
                await client.close()

    assert origin_requests == 1
    assert target_requests == []

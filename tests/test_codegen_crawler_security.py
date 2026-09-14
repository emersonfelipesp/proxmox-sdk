from __future__ import annotations

import asyncio
import importlib.util
import json
import os
import ssl
from collections.abc import Iterator
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any

import pytest

from proxmox_sdk.proxmox_codegen.crawler import (
    _extract_navigation,
    _guard_web_socket,
    _run_playwright_crawler,
    _should_abort,
    _should_reject_web_socket,
    crawl_proxmox_api_viewer,
    crawl_proxmox_api_viewer_async,
)
from proxmox_sdk.sdk.exceptions import ProxmoxRedirectError


class _FakeResponse:
    def __init__(self, status: int, location: str | None) -> None:
        self.status = status
        self.headers = {"Location": location} if location is not None else {}


class _FakeRequest:
    def __init__(
        self,
        url: str,
        *,
        redirected_from: _FakeRequest | None = None,
        response: _FakeResponse | None = None,
        resource_type: str = "document",
    ) -> None:
        self.url = url
        self.redirected_from = redirected_from
        self._response = response
        self.resource_type = resource_type

    def response(self) -> _FakeResponse | None:
        return self._response


def test_browser_request_guard_aborts_redirect_and_recovers_metadata() -> None:
    prior_request = _FakeRequest(
        "https://source.example/viewer/",
        response=_FakeResponse(
            307,
            "http://169.254.169.254/latest/meta-data?secret=hidden",
        ),
    )
    redirected_request = _FakeRequest(
        "http://169.254.169.254/latest/meta-data?secret=hidden",
        redirected_from=prior_request,
    )

    decision = _should_abort(redirected_request, ("https", "source.example", 443))

    assert decision.abort is True
    assert decision.reason == "redirect"
    assert decision.status == 307
    assert decision.location == "http://169.254.169.254/latest/meta-data?secret=hidden"


def test_browser_request_guard_aborts_cross_origin_subresource() -> None:
    request = _FakeRequest("https://assets.example/apidoc.js", resource_type="script")

    decision = _should_abort(request, ("https", "source.example", 443))

    assert decision.abort is True
    assert decision.reason == "cross-origin"
    assert decision.status is None
    assert decision.location is None


def test_browser_request_guard_allows_same_origin_request() -> None:
    request = _FakeRequest("https://SOURCE.example:443/apidoc.js")

    decision = _should_abort(request, ("https", "source.example", 443))

    assert decision.abort is False
    assert decision.reason is None


@pytest.mark.parametrize("url", ["ws://source.example/socket", "wss://source.example/socket"])
def test_browser_web_socket_policy_rejects_every_socket(url: str) -> None:
    assert _should_reject_web_socket(url) is True


def test_late_redirect_error_is_not_hidden_by_locator_failure() -> None:
    redirect_errors: list[ProxmoxRedirectError] = []
    endpoints: dict[str, object] = {}

    class FailingItem:
        def get_attribute(self, name: str) -> str | None:
            redirect_errors.append(ProxmoxRedirectError(302, "https://target.example/private"))
            raise RuntimeError(f"locator failed while reading {name}")

        def text_content(self) -> str:
            raise AssertionError("redirect errors must propagate before fallback text extraction")

    class FakeLocator:
        def locator(self, selector: str) -> FakeLocator:
            assert selector == "a"
            return self

        def all(self) -> list[FailingItem]:
            return [FailingItem()]

    class FakePage:
        def locator(self, selector: str) -> FakeLocator:
            assert selector == "nav"
            return FakeLocator()

    with pytest.raises(ProxmoxRedirectError) as error:
        _extract_navigation(FakePage(), endpoints, [], redirect_errors)

    assert error.value.status == 302
    assert error.value.location_host == "target.example"
    assert isinstance(error.value.__cause__, RuntimeError)
    assert endpoints == {}


def test_browser_guards_are_wired_before_page_creation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    events: list[str] = []
    handlers: dict[str, Any] = {}

    class EmptyLocator:
        def locator(self, selector: str) -> EmptyLocator:
            assert selector == "a"
            return self

        def all(self) -> list[object]:
            return []

    class FakePage:
        def goto(self, url: str, **kwargs: object) -> None:
            assert url == "https://source.example/api-viewer/"

        def wait_for_selector(self, selector: str, **kwargs: object) -> None:
            assert selector == "nav"

        def locator(self, selector: str) -> EmptyLocator:
            assert selector == "nav"
            return EmptyLocator()

    class FakeContext:
        def route(self, pattern: str, handler: Any) -> None:
            events.append("route")
            handlers["request"] = handler
            assert pattern == "**/*"

        def route_web_socket(self, pattern: str, handler: Any) -> None:
            events.append("route_web_socket")
            handlers["web_socket"] = handler
            assert pattern == "**/*"

        def new_page(self) -> FakePage:
            events.append("new_page")
            return FakePage()

    class FakeBrowser:
        def new_context(self, **kwargs: object) -> FakeContext:
            return FakeContext()

        def close(self) -> None:
            pass

    class FakeChromium:
        def launch(self, *, headless: bool) -> FakeBrowser:
            assert headless is True
            return FakeBrowser()

    class FakePlaywright:
        chromium = FakeChromium()

    class FakePlaywrightManager:
        def __enter__(self) -> FakePlaywright:
            return FakePlaywright()

        def __exit__(self, *args: object) -> None:
            pass

    monkeypatch.setattr(
        "playwright.sync_api.sync_playwright",
        lambda: FakePlaywrightManager(),
    )

    capture = _run_playwright_crawler(
        "https://source.example/api-viewer/",
        allow_insecure_ssl=False,
    )

    assert events == ["route", "route_web_socket", "new_page"]
    assert handlers["request"].__name__ == "guard_request"
    assert handlers["web_socket"] is _guard_web_socket
    assert capture["discovered_navigation_items"] == 0


@contextmanager
def _serve_http(
    handler: type[BaseHTTPRequestHandler],
    *,
    tls_context: ssl.SSLContext | None = None,
) -> Iterator[ThreadingHTTPServer]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    if tls_context is not None:
        server.socket = tls_context.wrap_socket(server.socket, server_side=True)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def _chromium_available() -> bool:
    playwright_spec = importlib.util.find_spec("playwright")
    if playwright_spec is None or playwright_spec.origin is None:
        return False
    package_dir = Path(playwright_spec.origin).parent
    manifest_path = package_dir / "driver" / "package" / "browsers.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    chromium = next(
        browser for browser in manifest["browsers"] if browser["name"] == "chromium-headless-shell"
    )
    configured_root = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if configured_root == "0":
        browser_root = package_dir / "driver" / "package" / ".local-browsers"
    else:
        browser_root = (
            Path(configured_root) if configured_root else Path.home() / ".cache/ms-playwright"
        )
    browser_dir = browser_root / f"chromium_headless_shell-{chromium['revision']}"
    return browser_dir.is_dir()


def _ephemeral_localhost_certificate(directory: Path) -> tuple[Path, Path]:
    """Write a throwaway self-signed certificate for 127.0.0.1 into ``directory``.

    Generating the pair per test run keeps private-key material out of the
    repository; the certificate is only ever trusted by the crawl under test,
    which runs with ``allow_insecure_ssl=True``.
    """
    import datetime
    import ipaddress

    from cryptography import x509
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import ec
    from cryptography.x509.oid import NameOID

    key = ec.generate_private_key(ec.SECP256R1())
    name = x509.Name([x509.NameAttribute(NameOID.COMMON_NAME, "localhost")])
    now = datetime.datetime.now(datetime.UTC)
    certificate = (
        x509.CertificateBuilder()
        .subject_name(name)
        .issuer_name(name)
        .public_key(key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - datetime.timedelta(minutes=1))
        .not_valid_after(now + datetime.timedelta(hours=1))
        .add_extension(
            x509.SubjectAlternativeName(
                [x509.DNSName("localhost"), x509.IPAddress(ipaddress.ip_address("127.0.0.1"))]
            ),
            critical=False,
        )
        .sign(key, hashes.SHA256())
    )
    cert_path = directory / "localhost-cert.pem"
    key_path = directory / "localhost-key.pem"
    cert_path.write_bytes(certificate.public_bytes(serialization.Encoding.PEM))
    key_path.write_bytes(
        key.private_bytes(
            serialization.Encoding.PEM,
            serialization.PrivateFormat.PKCS8,
            serialization.NoEncryption(),
        )
    )
    return cert_path, key_path


@pytest.mark.skipif(
    not _chromium_available(),
    reason="Playwright Chromium executable is not installed",
)
def test_browser_crawler_refuses_https_to_http_redirect_before_target_request(
    tmp_path: Path,
) -> None:
    origin_requests = 0
    target_requests = 0

    class TargetHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            nonlocal target_requests
            target_requests += 1
            self.send_response(200)
            self.end_headers()

        def log_message(self, format: str, *args: object) -> None:
            pass

    with _serve_http(TargetHandler) as target_server:
        target_port = int(target_server.server_address[1])
        target_url = f"http://127.0.0.1:{target_port}/redirect-target"

        class RedirectHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                nonlocal origin_requests
                origin_requests += 1
                self.send_response(302)
                self.send_header("Location", target_url)
                self.end_headers()

            def log_message(self, format: str, *args: object) -> None:
                pass

        cert_path, key_path = _ephemeral_localhost_certificate(tmp_path)
        tls_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        tls_context.load_cert_chain(cert_path, key_path)
        with _serve_http(RedirectHandler, tls_context=tls_context) as origin_server:
            origin_port = int(origin_server.server_address[1])
            origin_url = f"https://127.0.0.1:{origin_port}/api-viewer/"

            with pytest.raises(ProxmoxRedirectError) as async_error:
                asyncio.run(
                    crawl_proxmox_api_viewer_async(
                        origin_url,
                        allow_insecure_ssl=True,
                    )
                )
            with pytest.raises(ProxmoxRedirectError) as sync_error:
                crawl_proxmox_api_viewer(origin_url, allow_insecure_ssl=True)

    assert async_error.value.status == 302
    assert async_error.value.location_host == "127.0.0.1"
    assert sync_error.value.status == 302
    assert sync_error.value.location_host == "127.0.0.1"
    assert origin_requests == 2
    assert target_requests == 0


@pytest.mark.skipif(
    not _chromium_available(),
    reason="Playwright Chromium executable is not installed",
)
def test_browser_crawler_refuses_cross_origin_web_socket_before_upgrade() -> None:
    upgrade_requests = 0

    class WebSocketHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            nonlocal upgrade_requests
            upgrade_requests += 1
            self.send_response(400)
            self.end_headers()

        def log_message(self, format: str, *args: object) -> None:
            pass

    with _serve_http(WebSocketHandler) as web_socket_server:
        web_socket_port = int(web_socket_server.server_address[1])
        web_socket_url = f"ws://127.0.0.1:{web_socket_port}/socket"

        class ViewerHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                body = (
                    "<!doctype html><nav><a href='/nodes'>Nodes</a></nav>"
                    f"<script>window.socket = new WebSocket({json.dumps(web_socket_url)});</script>"
                ).encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args: object) -> None:
                pass

        with _serve_http(ViewerHandler) as viewer_server:
            viewer_port = int(viewer_server.server_address[1])
            viewer_url = f"http://127.0.0.1:{viewer_port}/api-viewer/"
            capture = crawl_proxmox_api_viewer(viewer_url)

    assert capture["discovered_navigation_items"] == 1
    assert upgrade_requests == 0


@pytest.mark.skipif(
    not _chromium_available(),
    reason="Playwright Chromium executable is not installed",
)
def test_delayed_page_script_redirect_propagates_from_sync_and_async_crawlers() -> None:
    late_redirect_requests = 0
    target_requests = 0

    class TargetHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            nonlocal target_requests
            target_requests += 1
            self.send_response(200)
            self.end_headers()

        def log_message(self, format: str, *args: object) -> None:
            pass

    with _serve_http(TargetHandler) as target_server:
        target_port = int(target_server.server_address[1])
        target_url = f"http://127.0.0.1:{target_port}/redirect-target"

        class ViewerHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                nonlocal late_redirect_requests
                if self.path == "/late-redirect":
                    late_redirect_requests += 1
                    self.send_response(302)
                    self.send_header("Location", target_url)
                    self.end_headers()
                    return
                links = "".join(
                    f"<a href='/nodes/{index}'>Node {index}</a>" for index in range(1000)
                )
                body = (
                    "<!doctype html><nav>"
                    f"{links}</nav><script>setTimeout(() => {{ "
                    "window.location.href = '/late-redirect'; }, 550);</script>"
                ).encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args: object) -> None:
                pass

        with _serve_http(ViewerHandler) as viewer_server:
            viewer_port = int(viewer_server.server_address[1])
            viewer_url = f"http://127.0.0.1:{viewer_port}/api-viewer/"

            with pytest.raises(ProxmoxRedirectError) as async_error:
                asyncio.run(crawl_proxmox_api_viewer_async(viewer_url))
            with pytest.raises(ProxmoxRedirectError) as sync_error:
                crawl_proxmox_api_viewer(viewer_url)

    assert async_error.value.status == 302
    assert async_error.value.location_host == "127.0.0.1"
    assert sync_error.value.status == 302
    assert sync_error.value.location_host == "127.0.0.1"
    assert late_redirect_requests == 2
    assert target_requests == 0

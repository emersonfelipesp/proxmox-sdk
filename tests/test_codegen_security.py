from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
from http.client import HTTPResponse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from urllib.request import Request

import pytest

from proxmox_sdk.proxmox_codegen.apidoc_parser import fetch_apidoc_js
from proxmox_sdk.proxmox_codegen.security import (
    SSRFProtectionError,
    validate_source_url,
    validate_version_tag,
)
from proxmox_sdk.sdk.exceptions import ProxmoxRedirectError


@contextmanager
def _serve_http(
    handler: type[BaseHTTPRequestHandler],
) -> Iterator[ThreadingHTTPServer]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield server
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


@pytest.mark.parametrize("prepared_request", [False, True], ids=["url", "request"])
def test_apidoc_downloader_refuses_redirect_at_opener_level(
    monkeypatch: pytest.MonkeyPatch,
    prepared_request: bool,
) -> None:
    target_requests = 0
    origin_requests = 0

    class TargetHandler(BaseHTTPRequestHandler):
        def do_GET(self) -> None:
            nonlocal target_requests
            target_requests += 1
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"const apiSchema = [];")

        def log_message(self, format: str, *args: object) -> None:
            pass

    with _serve_http(TargetHandler) as target_server:
        target_port = int(target_server.server_address[1])
        target_url = f"http://127.0.0.1:{target_port}/target?secret=hidden"

        class RedirectHandler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:
                nonlocal origin_requests
                origin_requests += 1
                body = b"redirect body must not be read"
                self.send_response(302)
                self.send_header("Location", target_url)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args: object) -> None:
                pass

        with _serve_http(RedirectHandler) as origin_server:
            origin_port = int(origin_server.server_address[1])
            origin_url = f"http://127.0.0.1:{origin_port}/apidoc.js"
            url: str | Request = Request(origin_url) if prepared_request else origin_url

            def fail_if_read(
                self: HTTPResponse,
                amt: int | None = None,
                decode_content: bool | None = None,
                cache_content: bool = False,
            ) -> bytes:
                del self, amt, decode_content, cache_content
                raise AssertionError("the redirect response body was read")

            monkeypatch.setattr(HTTPResponse, "read", fail_if_read)
            with pytest.raises(ProxmoxRedirectError) as exc_info:
                fetch_apidoc_js(url)

    assert exc_info.value.status == 302
    assert exc_info.value.location_host == "127.0.0.1"
    assert "secret=hidden" not in str(exc_info.value)
    assert origin_requests == 1
    assert target_requests == 0


class TestSSRFProtection:
    def test_valid_urls(self):
        assert (
            validate_source_url("https://pve.proxmox.com/pve-docs/apidoc.html")
            == "https://pve.proxmox.com/pve-docs/apidoc.html"
        )
        assert (
            validate_source_url("https://pmg.proxmox.com/pmg-docs/api-viewer/index.html")
            == "https://pmg.proxmox.com/pmg-docs/api-viewer/index.html"
        )

    def test_http_blocked_by_default(self):
        with pytest.raises(SSRFProtectionError, match="Invalid URL scheme"):
            validate_source_url("http://pve.proxmox.com/pve-docs/apidoc.html")

    def test_http_allowed_explicitly(self):
        assert (
            validate_source_url("http://pve.proxmox.com/pve-docs/apidoc.html", allow_http=True)
            == "http://pve.proxmox.com/pve-docs/apidoc.html"
        )

    def test_localhost_blocked(self):
        with pytest.raises(
            SSRFProtectionError, match="SSRF attempt blocked: URL targets localhost"
        ):
            validate_source_url("https://localhost/api")
        with pytest.raises(
            SSRFProtectionError, match="SSRF attempt blocked: URL targets private IP range"
        ):
            validate_source_url("https://127.0.0.1/api")
        with pytest.raises(
            SSRFProtectionError, match="SSRF attempt blocked: URL targets private IP range"
        ):
            validate_source_url("https://0.0.0.0/api")

    def test_private_ips_blocked(self):
        with pytest.raises(SSRFProtectionError, match="private IP range"):
            validate_source_url("https://10.0.0.5/api")
        with pytest.raises(SSRFProtectionError, match="private IP range"):
            validate_source_url("https://192.168.1.1/api")
        with pytest.raises(SSRFProtectionError, match="private IP range"):
            validate_source_url("https://172.16.0.5/api")
        with pytest.raises(SSRFProtectionError, match="private IP range"):
            validate_source_url("https://169.254.169.254/metadata")  # AWS metadata

    def test_ipv6_blocked(self):
        with pytest.raises(SSRFProtectionError, match="private IPv6 range"):
            validate_source_url("https://[::1]/api")
        with pytest.raises(SSRFProtectionError, match="private IPv6 range"):
            validate_source_url("https://[fe80::1]/api")

    def test_invalid_scheme(self):
        with pytest.raises(SSRFProtectionError, match="Invalid URL scheme"):
            validate_source_url("file:///etc/passwd")
        with pytest.raises(SSRFProtectionError, match="Invalid URL scheme"):
            validate_source_url("gopher://127.0.0.1:6379/_INFO")

    def test_empty_url(self):
        with pytest.raises(SSRFProtectionError, match="URL must be a non-empty string"):
            validate_source_url("")
        with pytest.raises(SSRFProtectionError, match="URL must be a non-empty string"):
            validate_source_url("   ")

    def test_invalid_url_format(self):
        with pytest.raises(SSRFProtectionError):
            validate_source_url("https://[invalid-ipv6]/api")

    def test_non_allowlisted_domain_blocked_by_default(self):
        """Fix 1: Non-Proxmox domains must be rejected unless allow_any_domain=True."""
        with pytest.raises(SSRFProtectionError, match="not in the allowed domains list"):
            validate_source_url("https://evil.com/api")
        with pytest.raises(SSRFProtectionError, match="not in the allowed domains list"):
            validate_source_url("https://example.com/api")

    def test_non_allowlisted_domain_allowed_with_flag(self):
        """Fix 1: allow_any_domain=True permits non-Proxmox domains."""
        result = validate_source_url("https://example.com/api", allow_any_domain=True)
        assert result == "https://example.com/api"

    def test_ipv4_mapped_ipv6_blocked(self):
        """Fix 2: ::ffff:127.0.0.1 must be blocked (IPv4-mapped loopback)."""
        with pytest.raises(SSRFProtectionError, match="IPv6-mapped"):
            validate_source_url("https://[::ffff:127.0.0.1]/api")

    def test_ipv4_mapped_ipv6_private_ranges(self):
        """Fix 2: IPv4-mapped IPv6 private addresses must all be blocked."""
        with pytest.raises(SSRFProtectionError, match="IPv6-mapped"):
            validate_source_url("https://[::ffff:10.0.0.1]/api")
        with pytest.raises(SSRFProtectionError, match="IPv6-mapped"):
            validate_source_url("https://[::ffff:192.168.1.1]/api")
        with pytest.raises(SSRFProtectionError, match="IPv6-mapped"):
            validate_source_url("https://[::ffff:169.254.169.254]/api")

    def test_ipv4_mapped_ipv6_public_allowed(self):
        """Fix 2: IPv4-mapped IPv6 with a public IP passes the IP check."""
        # Public IP embedded in IPv6 — passes IP check, but needs allow_any_domain
        # since it's not a hostname in the Proxmox allowlist.
        result = validate_source_url("https://[::ffff:8.8.8.8]/api", allow_any_domain=True)
        assert result == "https://[::ffff:8.8.8.8]/api"


class TestVersionTagValidation:
    def test_valid_tags(self):
        assert validate_version_tag("v1.0") == "v1.0"
        assert validate_version_tag("latest") == "latest"
        assert validate_version_tag("my-custom_tag.1") == "my-custom_tag.1"
        assert validate_version_tag("  v2.0  ") == "v2.0"

    def test_path_traversal_blocked(self):
        with pytest.raises(ValueError, match="must not contain parent directory references"):
            validate_version_tag("../v1.0")
        with pytest.raises(ValueError, match="must not contain parent directory references"):
            validate_version_tag("v1.0/..")
        with pytest.raises(ValueError, match="must not contain path separators"):
            validate_version_tag("v1.0/test")
        with pytest.raises(ValueError, match="must not contain path separators"):
            validate_version_tag("v1.0\\test")

    def test_invalid_characters_blocked(self):
        with pytest.raises(ValueError, match="must only contain alphanumeric characters"):
            validate_version_tag("v1.0!")
        with pytest.raises(ValueError, match="must only contain alphanumeric characters"):
            validate_version_tag("v1.0@test")
        with pytest.raises(ValueError, match="must only contain alphanumeric characters"):
            validate_version_tag("v1.0 test")

    def test_empty_tag(self):
        with pytest.raises(ValueError, match="must be a non-empty string"):
            validate_version_tag("")
        with pytest.raises(ValueError, match="must be a non-empty string"):
            validate_version_tag("   ")

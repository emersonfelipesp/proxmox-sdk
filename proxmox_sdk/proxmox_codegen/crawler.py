"""Crawler for Proxmox API Viewer using Playwright."""

from __future__ import annotations

import asyncio
import importlib.util
import logging
from collections import deque
from dataclasses import dataclass
from typing import Any, Literal
from urllib.parse import urlsplit

from proxmox_sdk.sdk.exceptions import ProxmoxRedirectError

_playwright_sync_api_available: bool | None = None

_logger = logging.getLogger(__name__)

_Origin = tuple[str, str, int | None]


@dataclass(frozen=True, slots=True)
class RedirectDecision:
    """Describe whether the browser request guard must abort a request."""

    abort: bool
    reason: Literal["redirect", "cross-origin"] | None = None
    status: int | None = None
    location: str | None = None


def _check_playwright_sync_api_available() -> bool:
    """Check if playwright sync API is available."""
    global _playwright_sync_api_available
    if _playwright_sync_api_available is None:
        _playwright_sync_api_available = importlib.util.find_spec("playwright.sync_api") is not None
    return _playwright_sync_api_available


def _url_origin(url: str) -> _Origin | None:
    """Return a normalized scheme, host, and effective port tuple."""
    try:
        parsed = urlsplit(url)
        port = parsed.port
    except ValueError:
        return None
    if not parsed.scheme or not parsed.hostname:
        return None
    if port is None:
        port = {"http": 80, "https": 443}.get(parsed.scheme.lower())
    return parsed.scheme.lower(), parsed.hostname.lower(), port


def _redirect_metadata(redirected_from: Any) -> tuple[int, str | None]:
    """Read redirect status and Location metadata without reading its body."""
    try:
        response = redirected_from.response()
    except Exception:  # noqa: BLE001 - Playwright metadata may be unavailable.
        return 300, None
    if response is None:
        return 300, None
    try:
        status = int(response.status)
    except Exception:  # noqa: BLE001 - retain the generic redirect status.
        status = 300
    try:
        location = response.headers.get("location") or response.headers.get("Location")
    except Exception:  # noqa: BLE001 - Location is optional metadata.
        location = None
    return status, location


def _should_abort(request_like: Any, source_origin: _Origin) -> RedirectDecision:
    """Apply the browser no-redirect and same-origin request policy."""
    redirected_from = request_like.redirected_from
    if redirected_from is not None:
        status, location = _redirect_metadata(redirected_from)
        return RedirectDecision(
            abort=True,
            reason="redirect",
            status=status,
            location=location,
        )
    if _url_origin(request_like.url) != source_origin:
        return RedirectDecision(abort=True, reason="cross-origin")
    return RedirectDecision(abort=False)


def _should_reject_web_socket(_url: str) -> bool:
    """Return whether a browser WebSocket must be refused before connection."""
    return True


def _guard_web_socket(web_socket: Any, pending: deque[Any]) -> None:
    """Queue a refusal without entering sync Playwright from its dispatcher."""
    if _should_reject_web_socket(web_socket.url):
        pending.append(web_socket)


def _drain_web_socket_refusals(pending: deque[Any]) -> None:
    """Close every unconnected socket on the owning synchronous caller stack."""
    first_error = None
    for _ in range(len(pending)):
        web_socket = pending.popleft()
        try:
            web_socket.close(code=1008, reason="WebSockets are refused")
        except Exception as error:
            if first_error is None:
                first_error = error
    if first_error is not None:
        raise first_error


def _fulfill_without_redirect(route: Any, redirect_errors: list[ProxmoxRedirectError]) -> None:
    """Inspect the first response before the browser can follow any redirect."""
    response = route.fetch(max_redirects=0, max_retries=0, timeout=30000)
    try:
        if 300 <= response.status < 400:
            location = response.headers.get("location") or response.headers.get("Location")
            redirect_errors.append(ProxmoxRedirectError(response.status, location))
            route.abort("blockedbyclient")
            return
        route.fulfill(response=response)
    finally:
        response.dispose()


def _guard_request(
    route: Any,
    request: Any,
    source_origin: _Origin,
    redirect_errors: list[ProxmoxRedirectError],
) -> None:
    """Reject forbidden request origins before making any network fetch."""
    decision = _should_abort(request, source_origin)
    if not decision.abort:
        _fulfill_without_redirect(route, redirect_errors)
        return
    if decision.reason == "redirect":
        redirect_errors.append(ProxmoxRedirectError(decision.status or 300, decision.location))
    route.abort("blockedbyclient")


def _close_browser(browser: Any, pending: deque[Any]) -> None:
    """Drain refusals before cleanup and retain no handles after browser closure."""
    try:
        _drain_web_socket_refusals(pending)
    finally:
        try:
            browser.close()
        finally:
            # Routes arriving while the browser closes are never connected and
            # are disposed with that browser, rather than retained across crawls.
            pending.clear()


def _raise_redirect_error(
    redirect_errors: list[ProxmoxRedirectError],
    cause: Exception | None = None,
) -> None:
    """Raise the first browser redirect error, preserving an extraction cause."""
    if not redirect_errors:
        return
    if cause is None:
        raise redirect_errors[0]
    raise redirect_errors[0] from cause


def _extract_navigation(
    page: Any,
    endpoints: dict[str, object],
    failed_endpoints: list[str],
    redirect_errors: list[ProxmoxRedirectError],
) -> int:
    """Extract rendered navigation without hiding a concurrent redirect error."""
    try:
        items = page.locator("nav").locator("a").all()
    except Exception as enumeration_error:
        _raise_redirect_error(redirect_errors, enumeration_error)
        raise

    for item in items:
        try:
            href = item.get_attribute("href")
            if href:
                endpoints[href] = {
                    "path": href,
                    "text": item.text_content(),
                    "methods": {},
                }
        except Exception as item_error:
            _raise_redirect_error(redirect_errors, item_error)
            try:
                failed_endpoints.append(item.text_content() or "")
            except Exception as label_error:
                _raise_redirect_error(redirect_errors, label_error)
                raise

    _raise_redirect_error(redirect_errors)
    return len(items)


def _empty_capture() -> dict[str, object]:
    """Return an empty browser-capture result."""
    return {
        "endpoints": {},
        "discovered_navigation_items": 0,
        "method_count": 0,
        "failed_endpoint_count": 0,
        "duration_seconds": 0.0,
    }


def _run_playwright_crawler(
    url: str,
    *,
    allow_insecure_ssl: bool,
) -> dict[str, object]:
    """Run the synchronous Playwright crawl."""
    from playwright.sync_api import sync_playwright

    source_origin = _url_origin(url)
    if source_origin is None:
        raise ValueError(f"Crawler source URL has no valid origin: {url!r}")

    endpoints: dict[str, object] = {}
    failed_endpoints: list[str] = []
    discovered_navigation_items = 0
    redirect_errors: list[ProxmoxRedirectError] = []
    pending_web_sockets: deque[Any] = deque()

    def guard_request(route: Any, request: Any) -> None:
        _guard_request(route, request, source_origin, redirect_errors)

    def guard_web_socket(web_socket: Any) -> None:
        _guard_web_socket(web_socket, pending_web_sockets)

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            context = browser.new_context(
                ignore_https_errors=allow_insecure_ssl,
                service_workers="block",
            )
            context.route("**/*", guard_request)
            context.route_web_socket("**/*", guard_web_socket)
            page = context.new_page()
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
            except Exception as goto_error:
                if redirect_errors:
                    raise redirect_errors[0] from goto_error
                _logger.warning(
                    "Playwright goto failed for %s (%s); apidoc.js fallback will cover the schema.",
                    url,
                    goto_error,
                )
                return _empty_capture()
            finally:
                _drain_web_socket_refusals(pending_web_sockets)
            if redirect_errors:
                raise redirect_errors[0]
            try:
                page.wait_for_selector("nav", timeout=10000)
            except Exception as selector_error:
                if redirect_errors:
                    raise redirect_errors[0] from selector_error
                _logger.warning(
                    "Proxmox API viewer at %s did not expose a <nav> selector (%s); "
                    "apidoc.js fallback will cover the schema.",
                    url,
                    selector_error,
                )
                return _empty_capture()
            finally:
                _drain_web_socket_refusals(pending_web_sockets)
            if redirect_errors:
                raise redirect_errors[0]

            discovered_navigation_items = _extract_navigation(
                page,
                endpoints,
                failed_endpoints,
                redirect_errors,
            )
        finally:
            _close_browser(browser, pending_web_sockets)

    _raise_redirect_error(redirect_errors)
    return {
        "endpoints": endpoints,
        "discovered_navigation_items": discovered_navigation_items,
        "method_count": len(endpoints),
        "failed_endpoint_count": len(failed_endpoints),
        "duration_seconds": 0.0,
    }


async def crawl_proxmox_api_viewer_async(
    url: str,
    worker_count: int = 10,
    retry_count: int = 2,
    retry_backoff_seconds: float = 0.35,
    checkpoint_path: str | None = None,
    checkpoint_every: int = 50,
    allow_insecure_ssl: bool = False,
) -> dict[str, object]:
    """Crawl Proxmox API viewer to capture endpoint definitions."""
    if not _check_playwright_sync_api_available():
        return _empty_capture()
    return await asyncio.to_thread(
        _run_playwright_crawler,
        url,
        allow_insecure_ssl=allow_insecure_ssl,
    )


def crawl_proxmox_api_viewer(
    url: str,
    worker_count: int = 10,
    retry_count: int = 2,
    retry_backoff_seconds: float = 0.35,
    checkpoint_path: str | None = None,
    checkpoint_every: int = 50,
    allow_insecure_ssl: bool = False,
) -> dict[str, object]:
    """Synchronously crawl Proxmox API viewer to capture endpoint definitions."""
    return asyncio.run(
        crawl_proxmox_api_viewer_async(
            url=url,
            worker_count=worker_count,
            retry_count=retry_count,
            retry_backoff_seconds=retry_backoff_seconds,
            checkpoint_path=checkpoint_path,
            checkpoint_every=checkpoint_every,
            allow_insecure_ssl=allow_insecure_ssl,
        )
    )


__all__ = ["crawl_proxmox_api_viewer", "crawl_proxmox_api_viewer_async"]

"""Shared async HTTP plumbing for direct Ceph provider clients.

The Ceph Dashboard API and the RGW Admin Ops API are standalone HTTP
services that are *not* reachable through the Proxmox VE API surface, so the
direct-provider clients cannot reuse :class:`proxmox_sdk.sdk.api.ProxmoxSDK`.
They each own their own transport instead.

The transport is expressed as a small :class:`AsyncTransport` protocol so the
default ``aiohttp``-backed implementation can be swapped for a recording
transport in tests without a live server or event-loop juggling.
"""

from __future__ import annotations

import ssl
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Protocol, Self, runtime_checkable

from proxmox_sdk.sdk.exceptions import (
    ProxmoxConnectionError,
    ResourceException,
)

if TYPE_CHECKING:
    import aiohttp

DEFAULT_TIMEOUT = 30

#: Any JSON value a provider endpoint may return. Using a union (rather than
#: ``Any``) keeps call sites honest: callers must narrow the result before
#: treating it as a specific shape.
JSONValue = dict[str, Any] | list[Any] | str | int | float | bool | None


@dataclass(slots=True)
class HttpResponse:
    """Normalised HTTP response returned by every transport."""

    status: int
    headers: dict[str, str] = field(default_factory=dict)
    json_body: Any = None
    text: str = ""


@runtime_checkable
class AsyncTransport(Protocol):
    """Minimal async HTTP transport contract used by provider clients."""

    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        data: Any | None = None,
    ) -> HttpResponse: ...

    async def close(self) -> None: ...


class AiohttpTransport:
    """Default transport backed by a lazily-created ``aiohttp`` session."""

    def __init__(self, *, verify_ssl: bool = True, timeout: int = DEFAULT_TIMEOUT) -> None:
        self._verify_ssl = verify_ssl
        self._timeout = timeout
        self._session: aiohttp.ClientSession | None = None
        # Build the SSL context once; create_default_context() parses the system
        # CA bundle, so rebuilding it per request is wasted work on hot paths.
        self._ssl: ssl.SSLContext | bool = self._build_ssl_context()

    def _build_ssl_context(self) -> ssl.SSLContext | bool:
        if self._verify_ssl:
            return True
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    async def _ensure_session(self) -> aiohttp.ClientSession:
        import aiohttp

        if self._session is None or self._session.closed:
            timeout = aiohttp.ClientTimeout(total=self._timeout)
            self._session = aiohttp.ClientSession(timeout=timeout)
        return self._session

    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        data: Any | None = None,
    ) -> HttpResponse:
        import aiohttp

        session = await self._ensure_session()
        ssl_param = self._ssl
        try:
            async with session.request(
                method,
                url,
                headers=headers,
                params=_clean_params(params),
                json=json,
                data=data,
                ssl=ssl_param,
            ) as response:
                text = await response.text()
                body: Any = None
                if text:
                    try:
                        body = await response.json(content_type=None)
                    except (ValueError, aiohttp.ContentTypeError):
                        body = None
                return HttpResponse(
                    status=response.status,
                    headers={k: v for k, v in response.headers.items()},
                    json_body=body,
                    text=text,
                )
        except aiohttp.ClientError as exc:  # pragma: no cover - network failure path
            raise ProxmoxConnectionError(str(exc)) from exc

    async def close(self) -> None:
        if self._session is not None and not self._session.closed:
            await self._session.close()
        self._session = None


def _clean_params(params: dict[str, Any] | None) -> dict[str, Any] | None:
    """Drop ``None`` values and lower-case bools to Ceph-friendly strings."""

    if not params:
        return None
    cleaned: dict[str, Any] = {}
    for key, value in params.items():
        if value is None:
            continue
        if isinstance(value, bool):
            cleaned[key] = "true" if value else "false"
        else:
            cleaned[key] = value
    return cleaned or None


class BaseHttpProvider:
    """Common base for HTTP-backed provider clients.

    Owns the transport, builds absolute URLs from a base URL, and exposes the
    async context-manager protocol so callers can ``async with`` the client and
    have its session closed deterministically.
    """

    #: Provider name used in capability errors; overridden by subclasses.
    provider: str = "ceph"

    def __init__(
        self,
        base_url: str,
        *,
        verify_ssl: bool = True,
        timeout: int = DEFAULT_TIMEOUT,
        transport: AsyncTransport | None = None,
    ) -> None:
        if not base_url:
            raise ValueError("base_url is required")
        self._base_url = base_url.rstrip("/")
        self._verify_ssl = verify_ssl
        self._timeout = timeout
        self._transport: AsyncTransport
        if transport is None:
            self._transport = AiohttpTransport(verify_ssl=verify_ssl, timeout=timeout)
            self._owns_transport = True
        else:
            # An injected transport is owned by the caller (and may be shared
            # across provider clients), so this provider must not close it.
            self._transport = transport
            self._owns_transport = False

    def _url(self, path: str) -> str:
        return f"{self._base_url}/{path.lstrip('/')}"

    @staticmethod
    def _raise_for_status(response: HttpResponse, *, context: str = "") -> None:
        if response.status >= 400:
            detail = response.text or ""
            label = f"{context}: " if context else ""
            raise ResourceException(
                status_code=response.status,
                status_message=f"{label}provider request failed",
                content=detail,
            )

    async def close(self) -> None:
        # Only close transports we created; an injected transport is owned by
        # the caller and may be shared across provider clients.
        if self._owns_transport:
            await self._transport.close()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *_exc: object) -> None:
        await self.close()

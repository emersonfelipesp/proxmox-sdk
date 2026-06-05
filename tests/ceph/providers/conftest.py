"""Shared recording transport for direct Ceph provider client tests."""

from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit

import pytest

from proxmox_sdk.ceph.providers._http import HttpResponse


class RecordingTransport:
    """In-memory :class:`AsyncTransport` keyed by ``"METHOD /path"``.

    ``routes`` maps ``"GET /api/host"`` (method + URL path) to either an
    :class:`HttpResponse` or a plain object used as the JSON body (status 200).
    Every call is appended to ``calls`` for assertions.
    """

    def __init__(self, routes: dict[str, Any] | None = None) -> None:
        self.routes = routes or {}
        self.calls: list[dict[str, Any]] = []
        self.closed = False

    def _response(self, method: str, path: str) -> HttpResponse:
        key = f"{method} {path}"
        if key not in self.routes:
            raise AssertionError(f"unexpected request: {key} (known: {sorted(self.routes)})")
        value = self.routes[key]
        if isinstance(value, HttpResponse):
            return value
        return HttpResponse(status=200, json_body=value)

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
        path = urlsplit(url).path
        self.calls.append(
            {
                "method": method,
                "url": url,
                "path": path,
                "headers": headers or {},
                "params": params,
                "json": json,
            }
        )
        return self._response(method, path)

    async def close(self) -> None:
        self.closed = True


@pytest.fixture
def recording_transport() -> RecordingTransport:
    return RecordingTransport()

"""Abstract authentication strategy protocols for the Proxmox SDK."""

from __future__ import annotations

import ssl
from typing import Protocol, runtime_checkable

import aiohttp


@runtime_checkable
class AuthStrategy(Protocol):
    """Minimal protocol every SDK authentication handler must satisfy.

    Auth strategies attach credentials to outgoing requests via headers
    and/or cookies. Strategies that also need an async preparation step
    (initial login, ticket renewal) implement :class:`EnsurableAuthStrategy`.

    Concrete implementations:

    - :class:`~proxmox_sdk.sdk.auth.token.TokenAuth` — stateless API token auth.
      Implements only this protocol.
    - :class:`~proxmox_sdk.sdk.auth.ticket.TicketAuth` — stateful ticket/password
      auth with renewal. Implements :class:`EnsurableAuthStrategy`.
    """

    def build_headers(self, method: str) -> dict[str, str]:
        """Return HTTP headers required for this auth strategy."""
        ...

    def build_cookies(self) -> dict[str, str]:
        """Return cookies required for this auth strategy."""
        ...


@runtime_checkable
class EnsurableAuthStrategy(AuthStrategy, Protocol):
    """Auth strategy with a pre-request async preparation step.

    Stateful strategies (ticket/password auth) implement this so the
    backend can perform initial authentication or renewal before each
    request. Stateless strategies (token auth) should implement only
    :class:`AuthStrategy` so they are not forced to depend on aiohttp.
    """

    async def ensure_ready(
        self,
        session: aiohttp.ClientSession,
        ticket_url: str,
        *,
        ssl: "ssl.SSLContext | bool | None" = None,
        proxy: str | None = None,
    ) -> None:
        """Ensure authentication state is valid before a request is sent.

        Args:
            session: Active aiohttp session to use for auth requests.
            ticket_url: Full URL for the ``POST /access/ticket`` endpoint.
            ssl: SSL context or bool passed through to aiohttp.
            proxy: HTTP proxy URL forwarded to auth requests.
        """
        ...


__all__ = ["AuthStrategy", "EnsurableAuthStrategy"]

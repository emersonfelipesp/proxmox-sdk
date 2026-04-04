"""Abstract backend protocol for the Proxmox SDK."""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class AbstractBackend(Protocol):
    """Protocol that all SDK backends must implement.

    Backends are responsible for executing API calls — they know how to reach
    the Proxmox service (HTTPS, SSH, local pvesh, or in-memory mock) and
    how to authenticate.  The ``ProxmoxResource`` navigation layer calls
    ``request()`` and never interacts with the transport directly.
    """

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
    ) -> Any:
        """Execute a Proxmox API call.

        Args:
            method: HTTP verb — GET, POST, PUT, PATCH, DELETE.
            path: Full API path including prefix, e.g. ``/api2/json/nodes``.
            params: Query parameters (used by GET/DELETE).
            data: Request body (used by POST/PUT/PATCH).

        Returns:
            Unwrapped response data (Proxmox ``data`` field extracted).

        Raises:
            ResourceException: API returned HTTP >= 400.
            AuthenticationError: Authentication failed.
        """
        ...

    async def close(self) -> None:
        """Release held resources (sessions, connections, threads)."""
        ...


__all__ = ["AbstractBackend"]

"""Synchronous wrapper for the Proxmox SDK."""

from __future__ import annotations

import asyncio
from typing import Any

from proxmox_openapi.sdk.resource import ProxmoxResource


class SyncProxmoxResource:
    """Synchronous wrapper around a :class:`ProxmoxResource`.

    HTTP methods block until complete.  Navigation attributes return
    additional :class:`SyncProxmoxResource` instances.

    Usage::

        with ProxmoxSDK.sync(host=..., user=..., password=...) as proxmox:
            nodes = proxmox.nodes.get()
            proxmox.nodes("pve1").qemu.post(vmid=100, name="test")
    """

    __slots__ = ("_resource", "_loop")

    def __init__(self, resource: ProxmoxResource, loop: asyncio.AbstractEventLoop) -> None:
        object.__setattr__(self, "_resource", resource)
        object.__setattr__(self, "_loop", loop)

    # ------------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------------

    def __getattr__(self, item: str) -> SyncProxmoxResource:
        sub = getattr(self._resource, item)  # returns ProxmoxResource
        return SyncProxmoxResource(sub, self._loop)

    def __call__(self, resource_id: str | int | list | tuple | None = None) -> SyncProxmoxResource:
        return SyncProxmoxResource(self._resource(resource_id), self._loop)

    def __repr__(self) -> str:
        return f"SyncProxmoxResource({self._resource!r})"

    # ------------------------------------------------------------------
    # HTTP methods (blocking)
    # ------------------------------------------------------------------

    def get(self, *path_args: str, **params: Any) -> Any:
        """Blocking HTTP GET."""
        return self._loop.run_until_complete(self._resource.get(*path_args, **params))

    def post(self, *path_args: str, **data: Any) -> Any:
        """Blocking HTTP POST."""
        return self._loop.run_until_complete(self._resource.post(*path_args, **data))

    def put(self, *path_args: str, **data: Any) -> Any:
        """Blocking HTTP PUT."""
        return self._loop.run_until_complete(self._resource.put(*path_args, **data))

    def patch(self, *path_args: str, **data: Any) -> Any:
        """Blocking HTTP PATCH."""
        return self._loop.run_until_complete(self._resource.patch(*path_args, **data))

    def delete(self, *path_args: str, **params: Any) -> Any:
        """Blocking HTTP DELETE."""
        return self._loop.run_until_complete(self._resource.delete(*path_args, **params))

    def create(self, *path_args: str, **data: Any) -> Any:
        """Alias for :meth:`post`."""
        return self.post(*path_args, **data)

    def set(self, *path_args: str, **data: Any) -> Any:
        """Alias for :meth:`put`."""
        return self.put(*path_args, **data)


class SyncProxmoxSDK:
    """Synchronous Proxmox SDK — blocks for every API call.

    Useful for scripts and contexts where ``async/await`` is not available.
    Uses a dedicated event loop that lives for the lifetime of this object.

    Usage::

        # Context manager (recommended)
        with ProxmoxSDK.sync(host="pve.example.com", user="admin@pam", password="s") as proxmox:
            nodes = proxmox.nodes.get()

        # Manual lifecycle
        proxmox = SyncProxmoxSDK(host=..., user=..., password=...)
        nodes = proxmox.nodes.get()
        proxmox.close()

    All keyword arguments are forwarded to :class:`ProxmoxSDK`.
    """

    def __init__(self, **kwargs: Any) -> None:
        self._loop = asyncio.new_event_loop()
        from proxmox_openapi.sdk.api import ProxmoxSDK

        self._sdk = ProxmoxSDK(**kwargs)
        self._root = SyncProxmoxResource(self._sdk._root, self._loop)

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    def __enter__(self) -> SyncProxmoxResource:
        return self._root

    def __exit__(self, *_: object) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Direct navigation (use without context manager)
    # ------------------------------------------------------------------

    def __getattr__(self, item: str) -> SyncProxmoxResource:
        if item.startswith("_"):
            raise AttributeError(item)
        return getattr(self._root, item)

    def __call__(self, resource_id: str | int | list | tuple | None = None) -> SyncProxmoxResource:
        return self._root(resource_id)

    # ------------------------------------------------------------------
    # Token access
    # ------------------------------------------------------------------

    def get_tokens(self) -> tuple[str, str]:
        """Return (ticket, csrf_token). Only available for HTTPS + password auth."""
        return self._loop.run_until_complete(self._sdk.get_tokens())

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def close(self) -> None:
        """Close the backend and the event loop."""
        self._loop.run_until_complete(self._sdk.close())
        self._loop.close()


__all__ = ["SyncProxmoxSDK", "SyncProxmoxResource"]

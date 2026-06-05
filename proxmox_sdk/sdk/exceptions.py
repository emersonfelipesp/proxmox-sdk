"""SDK exceptions for proxmox-sdk."""

from __future__ import annotations

from typing import Any


class ProxmoxSDKError(Exception):
    """Base exception for all SDK errors."""


class ResourceException(ProxmoxSDKError):
    """Raised when the Proxmox API returns HTTP >= 400."""

    def __init__(
        self,
        status_code: int,
        status_message: str,
        content: str = "",
        errors: dict[str, Any] | None = None,
        exit_code: int | None = None,
    ) -> None:
        self.status_code = status_code
        self.status_message = status_message
        self.content = content
        self.errors: dict[str, Any] | None = errors
        self.exit_code = exit_code
        super().__init__(f"HTTP {status_code} {status_message}: {content}")


class AuthenticationError(ProxmoxSDKError):
    """Raised when Proxmox authentication fails."""


class BackendNotAvailableError(ProxmoxSDKError):
    """Raised when a required optional backend dependency is not installed."""


class CephCapabilityUnsupportedError(ProxmoxSDKError):
    """Raised when a Ceph provider cannot service a requested operation.

    Used by the direct-provider clients (Dashboard API, RGW Admin Ops, RBD)
    to signal that the configured provider/version does not expose the
    requested capability, so higher layers can surface an actionable
    "unsupported" reason instead of failing opaquely.
    """

    def __init__(self, capability: str, *, provider: str = "", detail: str = "") -> None:
        self.capability = capability
        self.provider = provider
        self.detail = detail
        location = f"{provider} provider" if provider else "provider"
        message = f"{location} does not support capability '{capability}'"
        if detail:
            message = f"{message}: {detail}"
        super().__init__(message)


class ProxmoxTimeoutError(ResourceException):
    """Request timed out waiting for the Proxmox API to respond."""

    def __init__(self, content: str = "") -> None:
        super().__init__(status_code=504, status_message="Gateway Timeout", content=content)


class ProxmoxConnectionError(ResourceException):
    """Transport-level failure: DNS resolution, connection refused, or SSL error."""

    def __init__(self, content: str = "") -> None:
        super().__init__(status_code=503, status_message="Service Unavailable", content=content)


__all__ = [
    "ProxmoxSDKError",
    "ResourceException",
    "AuthenticationError",
    "BackendNotAvailableError",
    "CephCapabilityUnsupportedError",
    "ProxmoxTimeoutError",
    "ProxmoxConnectionError",
]

"""Configuration for Proxmox API connections."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ProxmoxConfig:
    """Configuration for Proxmox API client.

    Supports both the FastAPI server layer and the standalone SDK.

    Environment variables (original, unchanged):
        PROXMOX_API_MODE: "mock" or "real" (default: "mock")
        PROXMOX_API_URL: Proxmox API base URL (e.g., "https://pve.example.com:8006")
        PROXMOX_API_TOKEN_ID: API token ID (e.g., "user@pam!mytoken")
        PROXMOX_API_TOKEN_SECRET: API token secret value
        PROXMOX_API_USERNAME: Username for password auth (alternative to token)
        PROXMOX_API_PASSWORD: Password for password auth (alternative to token)
        PROXMOX_API_VERIFY_SSL: Verify SSL certificates ("true" or "false", default: "true")

    Additional environment variables (SDK layer):
        PROXMOX_API_SERVICE: Service type — PVE, PMG, PBS (default: "PVE")
        PROXMOX_API_BACKEND: Transport backend (default: "https")
        PROXMOX_API_TIMEOUT: Request timeout in seconds (default: "5")
        PROXMOX_API_PATH_PREFIX: Reverse-proxy path prefix (default: "")
        PROXMOX_API_OTP: OTP/TOTP code for 2FA (default: None)
        PROXMOX_API_OTPTYPE: OTP type — "totp" (default: "totp")
    """

    # ---- Original fields (unchanged) ----
    api_mode: str
    api_url: str | None
    token_id: str | None
    token_secret: str | None
    username: str | None
    password: str | None
    verify_ssl: bool

    # ---- SDK fields (new, all have defaults) ----
    service: str = "PVE"
    backend: str = "https"
    timeout: int = 5
    port: int | None = None
    path_prefix: str = ""
    otp: str | None = None
    otptype: str = "totp"
    cert: str | None = None
    proxies: dict[str, str] | None = field(default=None, hash=False, compare=False)

    @classmethod
    def from_env(cls) -> ProxmoxConfig:
        """Load configuration from environment variables."""
        api_mode = os.environ.get("PROXMOX_API_MODE", "mock").lower()
        api_url = os.environ.get("PROXMOX_API_URL")
        token_id = os.environ.get("PROXMOX_API_TOKEN_ID")
        token_secret = os.environ.get("PROXMOX_API_TOKEN_SECRET")
        username = os.environ.get("PROXMOX_API_USERNAME")
        password = os.environ.get("PROXMOX_API_PASSWORD")
        verify_ssl_str = os.environ.get("PROXMOX_API_VERIFY_SSL", "true").lower()
        verify_ssl = verify_ssl_str in ("true", "1", "yes")

        service = os.environ.get("PROXMOX_API_SERVICE", "PVE").upper()
        backend = os.environ.get("PROXMOX_API_BACKEND", "https").lower()
        timeout = int(os.environ.get("PROXMOX_API_TIMEOUT", "5"))
        path_prefix = os.environ.get("PROXMOX_API_PATH_PREFIX", "")
        otp = os.environ.get("PROXMOX_API_OTP") or None
        otptype = os.environ.get("PROXMOX_API_OTPTYPE", "totp")

        return cls(
            api_mode=api_mode,
            api_url=api_url,
            token_id=token_id,
            token_secret=token_secret,
            username=username,
            password=password,
            verify_ssl=verify_ssl,
            service=service,
            backend=backend,
            timeout=timeout,
            path_prefix=path_prefix,
            otp=otp,
            otptype=otptype,
        )

    def validate_for_real_mode(self) -> None:
        """Validate that configuration is sufficient for real API mode.

        Raises:
            ValueError: If required configuration is missing.
        """
        if not self.api_url:
            raise ValueError("PROXMOX_API_URL is required for real API mode")

        if not ((self.token_id and self.token_secret) or (self.username and self.password)):
            raise ValueError(
                "Either (PROXMOX_API_TOKEN_ID + PROXMOX_API_TOKEN_SECRET) "
                "or (PROXMOX_API_USERNAME + PROXMOX_API_PASSWORD) is required for authentication"
            )

    def is_real_mode(self) -> bool:
        """Check if running in real API mode."""
        return self.api_mode == "real"

    def is_mock_mode(self) -> bool:
        """Check if running in mock API mode."""
        return self.api_mode == "mock"

    def to_sdk_kwargs(self) -> dict[str, Any]:
        """Convert to ``ProxmoxSDK`` constructor keyword arguments.

        Useful when bridging the FastAPI configuration to the SDK::

            config = ProxmoxConfig.from_env()
            proxmox = ProxmoxSDK(**config.to_sdk_kwargs())
        """
        from urllib.parse import urlsplit

        kwargs: dict[str, Any] = {
            "service": self.service,
            "backend": self.backend if self.api_mode != "mock" else "mock",
            "verify_ssl": self.verify_ssl,
            "timeout": self.timeout,
            "path_prefix": self.path_prefix,
            "otptype": self.otptype,
        }

        if self.cert:
            kwargs["cert"] = self.cert
        if self.proxies:
            kwargs["proxies"] = self.proxies
        if self.otp:
            kwargs["otp"] = self.otp

        if self.api_mode == "mock":
            return kwargs

        # Real mode — extract host and credentials
        parsed = urlsplit(str(self.api_url or ""))
        kwargs["host"] = parsed.netloc or parsed.path

        if self.token_id and self.token_secret:
            parts = self.token_id.rsplit("!", 1)
            kwargs["user"] = parts[0] if len(parts) == 2 else self.token_id
            kwargs["token_name"] = parts[1] if len(parts) == 2 else ""
            kwargs["token_value"] = self.token_secret
        else:
            kwargs["user"] = self.username
            kwargs["password"] = self.password

        return kwargs


__all__ = ["ProxmoxConfig"]

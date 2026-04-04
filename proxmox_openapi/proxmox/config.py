"""Configuration for Proxmox API connections."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ProxmoxConfig:
    """Configuration for Proxmox API client.

    Environment variables:
        PROXMOX_API_MODE: "mock" or "real" (default: "mock")
        PROXMOX_API_URL: Proxmox API base URL (e.g., "https://pve.example.com:8006")
        PROXMOX_API_TOKEN_ID: API token ID (e.g., "user@pam!mytoken")
        PROXMOX_API_TOKEN_SECRET: API token secret value
        PROXMOX_API_USERNAME: Username for password auth (alternative to token)
        PROXMOX_API_PASSWORD: Password for password auth (alternative to token)
        PROXMOX_API_VERIFY_SSL: Verify SSL certificates ("true" or "false", default: "true")
    """

    api_mode: str
    api_url: str | None
    token_id: str | None
    token_secret: str | None
    username: str | None
    password: str | None
    verify_ssl: bool

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

        return cls(
            api_mode=api_mode,
            api_url=api_url,
            token_id=token_id,
            token_secret=token_secret,
            username=username,
            password=password,
            verify_ssl=verify_ssl,
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


__all__ = ["ProxmoxConfig"]

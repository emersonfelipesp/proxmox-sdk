"""Proxmox API client using aiohttp."""

from __future__ import annotations

import logging
import ssl
from typing import Any
from urllib.parse import urljoin

import aiohttp
from fastapi import HTTPException

from proxmox_openapi.proxmox.config import ProxmoxConfig

logger = logging.getLogger(__name__)


class ProxmoxClient:
    """Async HTTP client for Proxmox VE API.

    Supports both API token and username/password authentication.
    """

    def __init__(self, config: ProxmoxConfig) -> None:
        """Initialize Proxmox client.

        Args:
            config: Proxmox connection configuration
        """
        self.config = config
        config.validate_for_real_mode()

        self._session: aiohttp.ClientSession | None = None
        self._auth_ticket: str | None = None
        self._csrf_token: str | None = None

    async def _ensure_session(self) -> aiohttp.ClientSession:
        """Ensure aiohttp session is created and configured."""
        if self._session is None or self._session.closed:
            # SSL context configuration
            ssl_context: ssl.SSLContext | bool
            if self.config.verify_ssl:
                ssl_context = ssl.create_default_context()
            else:
                ssl_context = False

            # Create session with connector
            connector = aiohttp.TCPConnector(ssl=ssl_context)
            self._session = aiohttp.ClientSession(connector=connector)

        return self._session

    async def _authenticate_with_password(self) -> None:
        """Authenticate using username and password to get ticket."""
        if not self.config.username or not self.config.password:
            raise ValueError("Username and password required for password authentication")

        session = await self._ensure_session()
        auth_url = urljoin(str(self.config.api_url), "/api2/json/access/ticket")

        try:
            async with session.post(
                auth_url,
                data={
                    "username": self.config.username,
                    "password": self.config.password,
                },
            ) as response:
                if response.status != 200:
                    error_text = await response.text()
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Proxmox authentication failed: {error_text}",
                    )

                data = await response.json()
                ticket_data = data.get("data", {})
                self._auth_ticket = ticket_data.get("ticket")
                self._csrf_token = ticket_data.get("CSRFPreventionToken")

                if not self._auth_ticket:
                    raise HTTPException(
                        status_code=500,
                        detail="Proxmox authentication succeeded but no ticket returned",
                    )

        except aiohttp.ClientError as error:
            logger.exception("Proxmox authentication request failed")
            raise HTTPException(
                status_code=503,
                detail=f"Failed to connect to Proxmox API: {error}",
            )

    def _build_headers(self, method: str) -> dict[str, str]:
        """Build request headers with authentication.

        Args:
            method: HTTP method (for CSRF token requirement)

        Returns:
            Headers dictionary with authentication
        """
        headers: dict[str, str] = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }

        # API token authentication
        if self.config.token_id and self.config.token_secret:
            headers["Authorization"] = (
                f"PVEAPIToken={self.config.token_id}={self.config.token_secret}"
            )
        # Ticket authentication (requires CSRF for modifying methods)
        elif self._auth_ticket:
            headers["Cookie"] = f"PVEAuthCookie={self._auth_ticket}"
            if method.upper() in ("POST", "PUT", "PATCH", "DELETE") and self._csrf_token:
                headers["CSRFPreventionToken"] = self._csrf_token

        return headers

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Make HTTP request to Proxmox API.

        Args:
            method: HTTP method
            path: API path (e.g., "/api2/json/nodes")
            params: Query parameters
            json: JSON request body

        Returns:
            Parsed JSON response data

        Raises:
            HTTPException: On API errors or connection failures
        """
        # Authenticate with password if needed (and not using token auth)
        if (
            not self.config.token_id
            and self.config.username
            and self.config.password
            and not self._auth_ticket
        ):
            await self._authenticate_with_password()

        session = await self._ensure_session()
        headers = self._build_headers(method)

        # Build full URL
        url = urljoin(str(self.config.api_url), path)

        try:
            async with session.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json,
            ) as response:
                # Read response body
                try:
                    response_data = await response.json()
                except aiohttp.ContentTypeError:
                    response_data = {"data": await response.text()}

                # Handle non-2xx responses
                if not (200 <= response.status < 300):
                    error_detail = response_data.get("errors") or response_data
                    raise HTTPException(
                        status_code=response.status,
                        detail=f"Proxmox API error: {error_detail}",
                    )

                # Extract data from Proxmox response format
                return response_data.get("data", response_data)

        except aiohttp.ClientError as error:
            logger.exception("Proxmox API request failed: %s %s", method, path)
            raise HTTPException(
                status_code=503,
                detail=f"Failed to connect to Proxmox API: {error}",
            )

    async def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make GET request to Proxmox API."""
        return await self.request("GET", path, params=params)

    async def post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Make POST request to Proxmox API."""
        return await self.request("POST", path, params=params, json=json)

    async def put(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Make PUT request to Proxmox API."""
        return await self.request("PUT", path, params=params, json=json)

    async def patch(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Make PATCH request to Proxmox API."""
        return await self.request("PATCH", path, params=params, json=json)

    async def delete(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Make DELETE request to Proxmox API."""
        return await self.request("DELETE", path, params=params)

    async def close(self) -> None:
        """Close the HTTP session."""
        if self._session and not self._session.closed:
            await self._session.close()

    async def __aenter__(self) -> ProxmoxClient:
        """Async context manager entry."""
        return self

    async def __aexit__(self, *args: object) -> None:
        """Async context manager exit."""
        await self.close()


__all__ = ["ProxmoxClient"]

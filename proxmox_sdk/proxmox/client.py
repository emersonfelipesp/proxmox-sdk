"""FastAPI adapter — thin wrapper over the SDK HTTPS backend."""

from __future__ import annotations

import logging
from typing import Any

from fastapi import HTTPException

from proxmox_sdk.proxmox.config import ProxmoxConfig
from proxmox_sdk.sdk.exceptions import AuthenticationError, ResourceException
from proxmox_sdk.sdk.services import SERVICES

logger = logging.getLogger(__name__)


class ProxmoxClient:
    """Async HTTP client for the Proxmox VE API (FastAPI layer adapter).

    Delegates all transport logic to the SDK's :class:`HttpsBackend`.
    Translates SDK exceptions into :class:`fastapi.HTTPException` so that
    ``proxmox/routes.py`` continues to work without changes.

    Supports both API token and username/password authentication.
    """

    def __init__(self, config: ProxmoxConfig) -> None:
        config.validate_for_real_mode()
        self._config = config
        self._backend = self._build_backend(config)

    @staticmethod
    def _build_backend(config: ProxmoxConfig) -> Any:
        """Build an SDK HttpsBackend from the ProxmoxConfig."""
        from proxmox_sdk.sdk.backends.https import HttpsBackend

        service_name = getattr(config, "service", "PVE").upper()
        service_config = SERVICES.get(service_name, SERVICES["PVE"])
        return HttpsBackend.from_config(config, service_config)

    async def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        """Make an HTTP request to the Proxmox API.

        Args:
            method: HTTP method.
            path: API path (e.g., ``/api2/json/nodes``).
            params: Query parameters.
            json: JSON request body (``data`` in SDK terminology).

        Returns:
            Parsed JSON response data.

        Raises:
            HTTPException: On API errors or connection failures.
        """
        try:
            return await self._backend.request(method, path, params=params, data=json)
        except AuthenticationError as exc:
            raise HTTPException(status_code=401, detail=str(exc)) from exc
        except ResourceException as exc:
            raise HTTPException(
                status_code=exc.status_code, detail=exc.content or str(exc)
            ) from exc
        except Exception as exc:
            logger.exception("Unexpected Proxmox API error: %s %s", method, path)
            raise HTTPException(status_code=503, detail=str(exc)) from exc

    # Convenience wrappers used by routes.py implicitly via `request`

    async def get(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self.request("GET", path, params=params)

    async def post(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        return await self.request("POST", path, params=params, json=json)

    async def put(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        return await self.request("PUT", path, params=params, json=json)

    async def patch(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
    ) -> Any:
        return await self.request("PATCH", path, params=params, json=json)

    async def delete(self, path: str, *, params: dict[str, Any] | None = None) -> Any:
        return await self.request("DELETE", path, params=params)

    async def close(self) -> None:
        """Close the underlying session."""
        await self._backend.close()

    async def __aenter__(self) -> ProxmoxClient:
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()


__all__ = ["ProxmoxClient"]

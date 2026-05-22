"""Bridge between ProxmoxSDK and CLI for ergonomic command operations."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from proxmox_sdk.sdk.resource import ProxmoxResource
    from proxmox_sdk.sdk.sync import SyncProxmoxSDK

from .config import BackendConfig
from .exceptions import BackendError

logger = logging.getLogger(__name__)

_DEFAULT_HTTPS_PORTS = {"PVE": 8006, "PMG": 8006, "PBS": 8007, "PDM": 8443}
_SSH_BACKENDS = frozenset({"ssh_paramiko", "openssh"})
_HOST_REQUIRED_BACKENDS = frozenset({"https", "ssh_paramiko", "openssh"})


def _default_port(backend: str, service: str) -> int | None:
    """Return the conventional default port for *backend* / *service*."""
    if backend in _SSH_BACKENDS:
        return 22
    if backend == "https":
        return _DEFAULT_HTTPS_PORTS.get(service, 8006)
    return None


class ProxmoxSDKBridge:
    """Wrapper around ProxmoxSDK to provide CLI-friendly operations."""

    def __init__(self, sdk: SyncProxmoxSDK) -> None:
        """Initialize SDKBridge.

        Args:
            sdk: Initialized SyncProxmoxSDK instance
        """
        self.sdk = sdk
        self._current_resource: ProxmoxResource | None = None

    @staticmethod
    def create(config: BackendConfig) -> ProxmoxSDKBridge:
        """Create a bridge with SDK initialized from config.

        Backend dispatch lives in :class:`~proxmox_sdk.sdk.backends.factory.BackendFactory`
        (which ``ProxmoxSDK.__init__`` already consults). Adding a new backend
        only requires registering it in the factory — no edit to this method.

        Args:
            config: BackendConfig with connection details

        Returns:
            ProxmoxSDKBridge instance

        Raises:
            BackendError: If SDK initialization fails
        """
        try:
            from proxmox_sdk.sdk.api import ProxmoxSDK

            sdk = ProxmoxSDK.sync(
                backend=config.backend,
                service=config.service,
                host=config.host
                or ("localhost" if config.backend in _HOST_REQUIRED_BACKENDS else None),
                user=config.user or ("root" if config.backend in _SSH_BACKENDS else None),
                password=config.password,
                token_name=config.token_name,
                token_value=config.token_value,
                port=config.port or _default_port(config.backend, config.service),
                verify_ssl=config.verify_ssl,
                timeout=config.timeout,
                connect_timeout=config.connect_timeout,
                proxies=config.proxies,
                max_retries=config.max_retries,
                retry_backoff=config.retry_backoff,
            )
            return ProxmoxSDKBridge(sdk)
        except Exception as e:
            raise BackendError(f"Failed to initialize SDK: {e}", backend=config.backend)

    def navigate_path(self, path: str) -> ProxmoxResource:
        """Navigate to a resource using API path.

        Args:
            path: API path (e.g., "/nodes/pve1/qemu/100")

        Returns:
            ProxmoxResource at that path

        Raises:
            BackendError: If navigation fails
        """
        try:
            from .utils import extract_path_components

            components = extract_path_components(path)
            resource = self.sdk

            for component in components:
                # Try as attribute first, then as callable
                try:
                    resource = getattr(resource, component)
                except AttributeError:
                    # Try with parentheses (for parameterized paths)
                    parent_resource = resource
                    try:
                        resource = getattr(parent_resource, component.split("(")[0])
                        if "(" in component:
                            # Extract parameter and call
                            param = component.split("(")[1].rstrip(")")
                            resource = resource(param)
                    except (AttributeError, TypeError):
                        raise BackendError(
                            f"Cannot navigate to component: {component}",
                            backend=self.sdk._backend,  # type: ignore
                        )

            self._current_resource = resource
            return resource
        except BackendError:
            raise
        except Exception as e:
            raise BackendError(f"Cannot navigate path {path}: {e}", backend=self.sdk._backend)  # type: ignore

    def get(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Execute GET request.

        Args:
            path: API path
            params: Optional query parameters

        Returns:
            API response

        Raises:
            BackendError: If request fails
        """
        try:
            resource = self.navigate_path(path)
            return resource.get(**(params or {}))
        except BackendError:
            raise
        except Exception as e:
            raise BackendError(f"GET request failed: {e}", backend=self.sdk._backend)  # type: ignore

    def post(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Execute POST request.

        Args:
            path: API path
            params: Optional request parameters

        Returns:
            API response

        Raises:
            BackendError: If request fails
        """
        try:
            resource = self.navigate_path(path)
            return resource.post(**(params or {}))
        except BackendError:
            raise
        except Exception as e:
            raise BackendError(f"POST request failed: {e}", backend=self.sdk._backend)  # type: ignore

    def put(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Execute PUT request.

        Args:
            path: API path
            params: Optional request parameters

        Returns:
            API response

        Raises:
            BackendError: If request fails
        """
        try:
            resource = self.navigate_path(path)
            return resource.put(**(params or {}))
        except BackendError:
            raise
        except Exception as e:
            raise BackendError(f"PUT request failed: {e}", backend=self.sdk._backend)  # type: ignore

    def delete(
        self,
        path: str,
        params: dict[str, Any] | None = None,
    ) -> Any:
        """Execute DELETE request.

        Args:
            path: API path
            params: Optional query parameters

        Returns:
            API response

        Raises:
            BackendError: If request fails
        """
        try:
            resource = self.navigate_path(path)
            return resource.delete(**(params or {}))
        except BackendError:
            raise
        except Exception as e:
            raise BackendError(f"DELETE request failed: {e}", backend=self.sdk._backend)  # type: ignore

    def list_children(self, path: str) -> Any:
        """List child resources at path.

        Args:
            path: API path

        Returns:
            List of child resources

        Raises:
            BackendError: If request fails
        """
        # ls is typically a GET on the path
        return self.get(path)

    def close(self) -> None:
        """Close SDK connections if needed."""
        # SDK close if applicable
        if hasattr(self.sdk, "close"):
            self.sdk.close()

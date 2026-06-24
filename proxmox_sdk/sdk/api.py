"""ProxmoxSDK — main entry point for the Proxmox OpenAPI SDK."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal, cast

if TYPE_CHECKING:
    from proxmox_sdk.proxmox.config import ProxmoxConfig
    from proxmox_sdk.sdk.sync import SyncProxmoxSDK

from proxmox_sdk.sdk.auth.token import parse_token_id
from proxmox_sdk.sdk.backends.base import AbstractBackend, TicketCapableBackend
from proxmox_sdk.sdk.backends.factory import BackendBuildSpec, BackendFactory
from proxmox_sdk.sdk.resource import ProxmoxResource
from proxmox_sdk.sdk.services import SERVICES, ServiceConfig

ServiceName = Literal["PVE", "PMG", "PBS", "PDM"]


def _normalize_service_name(service: Any) -> ServiceName:
    service_upper = str(service).upper()
    if service_upper not in SERVICES:
        raise ValueError(f"Unknown service '{service}'. Supported: {list(SERVICES.keys())}")
    return cast(ServiceName, service_upper)


class ProxmoxSDK:
    """Async Python SDK for the Proxmox API.

    Provides dynamic, attribute-based navigation of the Proxmox REST API
    over multiple transport backends (HTTPS, SSH, local pvesh, or in-memory
    mock).  No FastAPI server required.

    Quick start (async context manager)::

        async with ProxmoxSDK(
            host="pve.example.com",
            user="admin@pam",
            password="secret",
            verify_ssl=False,
        ) as proxmox:
            nodes = await proxmox.nodes.get()
            vms   = await proxmox.nodes("pve1").qemu.get()

    Token auth::

        proxmox = ProxmoxSDK(
            host="pve.example.com",
            user="monitoring@pve",
            token_name="api-read",
            token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        )

    Mock mode (no real Proxmox)::

        async with ProxmoxSDK.mock() as proxmox:
            nodes = await proxmox.nodes.get()

    SSH backend::

        proxmox = ProxmoxSDK(
            host="pve.example.com",
            user="root",
            password="secret",
            backend="ssh_paramiko",
        )

    Local backend (on Proxmox host)::

        proxmox = ProxmoxSDK(backend="local", service="PVE")

    Sync usage::

        proxmox = ProxmoxSDK.sync(host=..., user=..., password=...)
        nodes = proxmox.nodes.get()
    """

    def __init__(
        self,
        host: str | None = None,
        *,
        _backend: AbstractBackend | None = None,
        user: str | None = None,
        password: str | None = None,
        token_name: str | None = None,
        token_value: str | None = None,
        otp: str | None = None,
        otptype: str = "totp",
        service: ServiceName = "PVE",
        backend: str = "https",
        port: int | None = None,
        path_prefix: str = "",
        verify_ssl: bool = True,
        cert: str | None = None,
        timeout: int = 5,
        connect_timeout: int | None = None,
        proxies: dict[str, str] | None = None,
        max_retries: int = 0,
        retry_backoff: float = 0.5,
        sudo: bool = False,
        private_key_file: str | None = None,
        identity_file: str | None = None,
        forward_ssh_agent: bool = False,
        config_file: str | None = None,
        otel_enabled: bool | None = None,
    ) -> None:
        service_upper = _normalize_service_name(service)
        svc: ServiceConfig = SERVICES[service_upper]

        if _backend is not None:
            # Caller-supplied backend — skip factory entirely (e.g. for testing).
            self._service_name = service_upper
            self._service_config = svc
            self._backend_name = "custom"
            self._backend = self._install_backend(_backend, otel_enabled=otel_enabled)
            self._root = ProxmoxResource(path=svc.api_path_prefix, backend=self._backend)
            return

        if backend not in svc.supported_backends:
            raise ValueError(
                f"Backend '{backend}' is not supported for service '{service_upper}'. "
                f"Supported backends: {list(svc.supported_backends)}"
            )

        self._service_name = service_upper
        self._service_config = svc
        self._backend_name = backend
        built_backend = BackendFactory().create(
            BackendBuildSpec(
                backend=backend,
                service_config=svc,
                host=host,
                user=user,
                password=password,
                token_name=token_name,
                token_value=token_value,
                otp=otp,
                otptype=otptype,
                port=port,
                path_prefix=path_prefix,
                verify_ssl=verify_ssl,
                cert=cert,
                timeout=timeout,
                connect_timeout=connect_timeout,
                proxies=proxies,
                max_retries=max_retries,
                retry_backoff=retry_backoff,
                sudo=sudo,
                private_key_file=private_key_file,
                identity_file=identity_file,
                forward_ssh_agent=forward_ssh_agent,
                config_file=config_file,
            )
        )
        self._backend = self._install_backend(built_backend, otel_enabled=otel_enabled)
        self._root: ProxmoxResource = ProxmoxResource(
            path=svc.api_path_prefix,
            backend=self._backend,
        )

    def _install_backend(
        self,
        backend: AbstractBackend,
        *,
        otel_enabled: bool | None = None,
    ) -> AbstractBackend:
        """Wrap *backend* with tracing when telemetry is explicitly enabled."""
        from proxmox_sdk import telemetry

        if not telemetry.is_enabled(otel_enabled):
            return backend
        return telemetry.TracingBackend(
            backend,
            backend_name=self._backend_name,
            service_name=self._service_name,
            otel_enabled=otel_enabled,
        )

    @property
    def service(self) -> str:
        """Return the Proxmox service name this SDK instance targets."""
        return self._service_name

    @property
    def backend_name(self) -> str:
        """Return the configured transport backend name."""
        return self._backend_name

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> ProxmoxResource:
        """Return the root ProxmoxResource for API navigation."""
        return self._root

    async def __aexit__(self, *_: object) -> None:
        await self.close()

    # ------------------------------------------------------------------
    # Direct navigation (use without context manager)
    # ------------------------------------------------------------------

    def __getattr__(self, item: str) -> ProxmoxResource:
        """Delegate attribute access to the root resource.

        Allows usage without the context manager::

            proxmox = ProxmoxSDK(...)
            nodes = await proxmox.nodes.get()
            await proxmox.close()
        """
        if item.startswith("_"):
            raise AttributeError(item)
        return getattr(self._root, item)

    def __call__(self, resource_id: str | int | list | tuple | None = None) -> ProxmoxResource:
        """Delegate call to the root resource."""
        return self._root(resource_id)

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def close(self) -> None:
        """Release all backend resources (sessions, connections)."""
        await self._backend.close()

    # ------------------------------------------------------------------
    # Token access
    # ------------------------------------------------------------------

    async def get_tokens(self) -> tuple[str, str]:
        """Return (ticket, csrf_token) for HTTPS password-auth backends.

        Useful when you need to pass Proxmox auth tokens to another system.

        Raises:
            RuntimeError: If the active backend does not support tickets
                (e.g. mock, local pvesh, or SSH backends).
        """
        if not isinstance(self._backend, TicketCapableBackend):
            raise RuntimeError(
                "get_tokens() is only available for the HTTPS backend with password auth"
            )
        return await self._backend.get_tokens()

    # ------------------------------------------------------------------
    # Class-method constructors
    # ------------------------------------------------------------------

    @classmethod
    def mock(
        cls,
        schema_version: str = "latest",
        service: ServiceName = "PVE",
        *,
        otel_enabled: bool | None = None,
    ) -> ProxmoxSDK:
        """Create a ProxmoxSDK instance backed by the in-memory mock.

        No real Proxmox host required.  Useful for tests and development.

        Example::

            async with ProxmoxSDK.mock() as proxmox:
                nodes = await proxmox.nodes.get()
        """
        instance = object.__new__(cls)

        from proxmox_sdk.sdk.backends.mock import MockBackend

        service_upper = _normalize_service_name(service)
        svc = SERVICES[service_upper]
        backend = MockBackend(
            schema_version=schema_version,
            api_path_prefix=svc.api_path_prefix,
            service=service_upper,
        )
        instance._service_name = service_upper
        instance._service_config = svc
        instance._backend_name = "mock"
        instance._backend = instance._install_backend(backend, otel_enabled=otel_enabled)
        instance._root = ProxmoxResource(path=svc.api_path_prefix, backend=instance._backend)
        return instance

    @classmethod
    def from_config(cls, config: ProxmoxConfig) -> ProxmoxSDK:
        """Create a ProxmoxSDK instance from a ProxmoxConfig dataclass.

        Args:
            config: A :class:`~proxmox_sdk.proxmox.config.ProxmoxConfig` instance.

        Example::

            config = ProxmoxConfig.from_env()
            proxmox = ProxmoxSDK.from_config(config)
        """
        service = _normalize_service_name(getattr(config, "service", "PVE"))
        backend_name = getattr(config, "backend", "https")

        if backend_name == "mock" or getattr(config, "api_mode", "real") == "mock":
            schema_version = getattr(config, "schema_version", "latest")
            return cls.mock(
                schema_version=schema_version,
                service=service,
                otel_enabled=getattr(config, "otel_enabled", None),
            )

        # Extract credentials from ProxmoxConfig
        token_id: str | None = config.token_id
        token_secret: str | None = config.token_secret
        token_name: str | None = None
        token_value: str | None = None

        if token_id and token_secret:
            user, token_name = parse_token_id(token_id)
            token_value = token_secret
        else:
            user = config.username

        # Extract host from api_url
        from urllib.parse import urlsplit

        parsed = urlsplit(str(config.api_url or ""))
        host = parsed.netloc or parsed.path or "localhost"

        return cls(
            host=host,
            user=user,
            password=config.password,
            token_name=token_name,
            token_value=token_value,
            service=service,
            backend=backend_name,
            verify_ssl=config.verify_ssl,
            cert=getattr(config, "cert", None),
            timeout=getattr(config, "timeout", 5),
            connect_timeout=getattr(config, "connect_timeout", None),
            proxies=getattr(config, "proxies", None),
            max_retries=getattr(config, "max_retries", 0),
            retry_backoff=getattr(config, "retry_backoff", 0.5),
            path_prefix=getattr(config, "path_prefix", ""),
            port=getattr(config, "port", None),
            otp=getattr(config, "otp", None),
            otptype=getattr(config, "otptype", "totp"),
            otel_enabled=getattr(config, "otel_enabled", None),
        )

    @classmethod
    def sync(cls, **kwargs: Any) -> "SyncProxmoxSDK":
        """Create a synchronous wrapper for environments without async/await.

        Example::

            with ProxmoxSDK.sync(
                host="pve.example.com",
                user="admin@pam",
                password="secret",
            ) as proxmox:
                nodes = proxmox.nodes.get()
        """
        from proxmox_sdk.sdk.sync import SyncProxmoxSDK

        return SyncProxmoxSDK(**kwargs)

    @classmethod
    def sync_mock(
        cls,
        schema_version: str = "latest",
        service: ServiceName = "PVE",
        *,
        otel_enabled: bool | None = None,
    ) -> "SyncProxmoxSDK":
        """Create a synchronous mock SDK instance.

        No real Proxmox host required.  Useful for tests and development.
        All API calls block synchronously (no `async/await` needed).

        Args:
            schema_version: Proxmox schema version tag (default: "latest").
            service: Service type (default: "PVE").

        Returns:
            A SyncProxmoxSDK instance ready for blocking API calls.

        Example::

            with ProxmoxSDK.sync_mock() as proxmox:
                nodes = proxmox.nodes.get()
                vms = proxmox.nodes("pve").qemu.get()
        """
        from proxmox_sdk.sdk.sync import SyncProxmoxSDK

        instance = object.__new__(SyncProxmoxSDK)
        import asyncio

        instance._loop = asyncio.new_event_loop()
        instance._sdk = cls.mock(
            schema_version=schema_version,
            service=service,
            otel_enabled=otel_enabled,
        )
        from proxmox_sdk.sdk.sync import SyncProxmoxResource

        instance._root = SyncProxmoxResource(instance._sdk._root, instance._loop)
        return instance


__all__ = ["ProxmoxSDK"]

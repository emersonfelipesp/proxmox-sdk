"""Backend factory for :class:`proxmox_sdk.sdk.api.ProxmoxSDK`."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from proxmox_sdk.sdk.backends.base import AbstractBackend
from proxmox_sdk.sdk.services import ServiceConfig


@dataclass(frozen=True, kw_only=True)
class BackendConfig:
    """Constructor inputs needed to build one concrete SDK backend."""

    backend: str
    service_config: ServiceConfig
    host: str | None = None
    user: str | None = None
    password: str | None = None
    token_name: str | None = None
    token_value: str | None = None
    otp: str | None = None
    otptype: str = "totp"
    port: int | None = None
    path_prefix: str = ""
    verify_ssl: bool = True
    cert: str | None = None
    timeout: int = 5
    connect_timeout: int | None = None
    proxies: dict[str, str] | None = None
    max_retries: int = 0
    retry_backoff: float = 0.5
    sudo: bool = False
    private_key_file: str | None = None
    identity_file: str | None = None
    forward_ssh_agent: bool = False
    config_file: str | None = None


class BackendFactory:
    """Create concrete backends without coupling ``ProxmoxSDK`` to transport details."""

    def create(self, config: BackendConfig) -> AbstractBackend:
        creators: dict[str, Callable[[BackendConfig], AbstractBackend]] = {
            "mock": self._mock,
            "local": self._local,
            "https": self._https,
            "ssh_paramiko": self._ssh_paramiko,
            "openssh": self._openssh,
        }
        try:
            creator = creators[config.backend]
        except KeyError as exc:
            supported = ", ".join(sorted(creators))
            raise ValueError(f"Unknown backend '{config.backend}'. Supported: {supported}") from exc
        return creator(config)

    @staticmethod
    def _mock(config: BackendConfig) -> AbstractBackend:
        from proxmox_sdk.sdk.backends.mock import MockBackend

        return MockBackend(api_path_prefix=config.service_config.api_path_prefix)

    @staticmethod
    def _local(config: BackendConfig) -> AbstractBackend:
        from proxmox_sdk.sdk.backends.local import LocalBackend

        return LocalBackend(service_config=config.service_config, sudo=config.sudo)

    @staticmethod
    def _https(config: BackendConfig) -> AbstractBackend:
        from proxmox_sdk.sdk.auth.ticket import TicketAuth
        from proxmox_sdk.sdk.auth.token import TokenAuth
        from proxmox_sdk.sdk.backends.https import HttpsBackend

        if not config.host:
            raise ValueError("'host' is required for the HTTPS backend")

        if config.token_name and config.token_value:
            auth = TokenAuth(
                user=config.user or "",
                token_name=config.token_name,
                token_value=config.token_value,
                service_config=config.service_config,
            )
        elif config.user and config.password:
            auth = TicketAuth(
                username=config.user,
                password=config.password,
                service_config=config.service_config,
                otp=config.otp,
                otptype=config.otptype,
            )
        else:
            raise ValueError(
                "HTTPS backend requires either (user + password) "
                "or (user + token_name + token_value)"
            )

        return HttpsBackend(
            host=config.host,
            service_config=config.service_config,
            auth=auth,
            port=config.port,
            path_prefix=config.path_prefix,
            verify_ssl=config.verify_ssl,
            cert=config.cert,
            timeout=config.timeout,
            connect_timeout=config.connect_timeout,
            proxies=config.proxies,
            max_retries=config.max_retries,
            retry_backoff=config.retry_backoff,
        )

    @staticmethod
    def _ssh_paramiko(config: BackendConfig) -> AbstractBackend:
        from proxmox_sdk.sdk.backends.ssh_paramiko import SshParamikoBackend

        if not config.host:
            raise ValueError("'host' is required for the ssh_paramiko backend")
        if not config.user:
            raise ValueError("'user' is required for the ssh_paramiko backend")

        return SshParamikoBackend(
            host=config.host,
            user=config.user,
            service_config=config.service_config,
            password=config.password,
            private_key_file=config.private_key_file,
            port=config.port or 22,
            sudo=config.sudo,
        )

    @staticmethod
    def _openssh(config: BackendConfig) -> AbstractBackend:
        from proxmox_sdk.sdk.backends.openssh import OpenSshBackend

        if not config.host:
            raise ValueError("'host' is required for the openssh backend")
        if not config.user:
            raise ValueError("'user' is required for the openssh backend")

        return OpenSshBackend(
            host=config.host,
            user=config.user,
            service_config=config.service_config,
            password=config.password,
            identity_file=config.identity_file,
            forward_ssh_agent=config.forward_ssh_agent,
            config_file=config.config_file,
            port=config.port or 22,
            sudo=config.sudo,
        )


__all__ = ["BackendConfig", "BackendFactory"]

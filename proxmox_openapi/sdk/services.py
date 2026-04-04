"""Proxmox service definitions and metadata registry."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ServiceConfig:
    """Configuration metadata for a Proxmox service type."""

    supported_backends: tuple[str, ...]
    supported_auth_methods: tuple[str, ...]
    default_port: int
    token_separator: str
    auth_cookie_name: str
    api_path_prefix: str
    cli_name: str | None
    cli_extra_options: tuple[str, ...]


SERVICES: dict[str, ServiceConfig] = {
    "PVE": ServiceConfig(
        supported_backends=("https", "ssh_paramiko", "openssh", "local", "mock"),
        supported_auth_methods=("password", "token"),
        default_port=8006,
        token_separator="=",
        auth_cookie_name="PVEAuthCookie",
        api_path_prefix="/api2/json",
        cli_name="pvesh",
        cli_extra_options=("--output-format", "json"),
    ),
    "PMG": ServiceConfig(
        supported_backends=("https", "ssh_paramiko", "openssh", "local", "mock"),
        supported_auth_methods=("password",),
        default_port=8006,
        token_separator="=",
        auth_cookie_name="PMGAuthCookie",
        api_path_prefix="/api2/json",
        cli_name="pmgsh",
        cli_extra_options=("--output-format", "json"),
    ),
    "PBS": ServiceConfig(
        supported_backends=("https", "mock"),
        supported_auth_methods=("password", "token"),
        default_port=8007,
        token_separator=":",
        auth_cookie_name="PBSAuthCookie",
        api_path_prefix="/api2/json",
        cli_name=None,
        cli_extra_options=(),
    ),
}


__all__ = ["SERVICES", "ServiceConfig"]

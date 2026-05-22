"""Shared helpers for CLI command implementations."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

if TYPE_CHECKING:
    from proxmox_sdk.proxmox_cli.config import BackendConfig

from proxmox_sdk.proxmox_cli.config import ConfigManager
from proxmox_sdk.proxmox_cli.exceptions import ProxmoxCLIError
from proxmox_sdk.proxmox_cli.output import (
    OutputFormatter,
    get_context_options,
    resolve_output_format,
)
from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge
from proxmox_sdk.sdk.services import SERVICES

ServiceName = Literal["PVE", "PDM", "PBS", "PMG"]

# Fields that can be overridden from the CLI context object.
_OVERRIDE_KEYS = ("backend", "host", "user", "password", "token_value", "port", "service")


def apply_cli_overrides(backend_cfg: BackendConfig, ctx_obj: dict[str, Any]) -> None:
    """Apply CLI global-flag overrides to *backend_cfg* in-place."""
    for key in _OVERRIDE_KEYS:
        if ctx_obj.get(key):
            setattr(backend_cfg, key, ctx_obj[key])


def prepare_command(
    ctx_obj: dict[str, Any] | None = None,
) -> tuple[ConfigManager, ProxmoxSDKBridge]:
    """Load config, apply CLI overrides, and create an SDK bridge.

    Returns:
        A ``(config_mgr, bridge)`` tuple.  The caller is responsible for
        calling ``bridge.close()`` when done.
    """
    if ctx_obj is None:
        ctx_obj = get_context_options()
    config_mgr = ConfigManager()
    config_mgr.load_config(ctx_obj.get("config"))
    backend_cfg = config_mgr.get_profile()
    apply_cli_overrides(backend_cfg, ctx_obj)
    bridge = ProxmoxSDKBridge.create(backend_cfg)
    return config_mgr, bridge


def create_formatter(
    config_mgr: ConfigManager,
    output: str | None,
    *,
    json_output: bool = False,
    yaml_output: bool = False,
    markdown_output: bool = False,
    ctx_obj: dict[str, Any] | None = None,
) -> OutputFormatter:
    """Build an :class:`OutputFormatter` from CLI context and format flags."""
    if ctx_obj is None:
        ctx_obj = get_context_options()
    fmt = resolve_output_format(
        output,
        json_output=json_output,
        yaml_output=yaml_output,
        markdown_output=markdown_output,
        fallback=ctx_obj.get("output_format", "human"),
    )
    return OutputFormatter(format=fmt, colors=config_mgr.global_config.colors)


def ensure_service(bridge: ProxmoxSDKBridge, service: ServiceName) -> None:
    """Raise ``ProxmoxCLIError`` unless *bridge* is bound to *service*.

    Centralized service guard for CLI command groups that only make sense
    against a specific Proxmox service (e.g. Ceph against PVE, PDM commands
    against PDM). A ``None`` service config is treated as a match (legacy
    backends that predate per-service routing).
    """
    inner = getattr(bridge.sdk, "_sdk", bridge.sdk)
    current = getattr(inner, "_service_config", None)
    expected = SERVICES[service]
    if current is None or current is expected:
        return
    detected = next((name for name, cfg in SERVICES.items() if cfg is current), "unknown")
    raise ProxmoxCLIError(
        f"{service} commands require service={service}; current service is {detected}.",
        exit_code=2,
    )

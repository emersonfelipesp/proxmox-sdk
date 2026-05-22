"""Shared helpers for PDM CLI command modules."""

from __future__ import annotations

from typing import Any

import typer

from proxmox_sdk.proxmox_cli.config import BackendConfig, ConfigManager
from proxmox_sdk.proxmox_cli.decorators import cli_error_handler
from proxmox_sdk.proxmox_cli.output import get_context_options
from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge

from .._common import (
    apply_cli_overrides,
    create_formatter,
    dispatch_request,
    ensure_service,
    prepare_command,
)


def _build_pdm_backend_config(ctx_obj: dict[str, Any], *, use_mock: bool) -> BackendConfig:
    config_mgr = ConfigManager()
    config_mgr.load_config(ctx_obj.get("config"))
    backend_cfg = config_mgr.get_profile()
    apply_cli_overrides(backend_cfg, ctx_obj)
    if use_mock:
        backend_cfg.backend = "mock"
    elif backend_cfg.backend == "mock":
        backend_cfg.backend = "https"
    backend_cfg.service = "PDM"
    return backend_cfg


def _prepare_pdm_bridge() -> tuple[Any, ProxmoxSDKBridge]:
    """Force service=PDM in the context and prepare an SDK bridge."""
    ctx_obj = dict(get_context_options())
    ctx_obj["service"] = "PDM"
    return prepare_command(ctx_obj)


def _format_options(
    output: str | None,
    json_output: bool,
    yaml_output: bool,
    markdown_output: bool,
) -> dict[str, Any]:
    return {
        "output": output,
        "json_output": json_output,
        "yaml_output": yaml_output,
        "markdown_output": markdown_output,
    }


@cli_error_handler
def _run_request(
    method: str,
    path: str,
    *,
    params: dict[str, Any] | None,
    output: str | None,
    json_output: bool,
    yaml_output: bool,
    markdown_output: bool,
) -> None:
    config_mgr, bridge = _prepare_pdm_bridge()
    try:
        ensure_service(bridge, "PDM")
        ctx_obj = get_context_options()
        formatter = create_formatter(
            config_mgr,
            output,
            json_output=json_output,
            yaml_output=yaml_output,
            markdown_output=markdown_output,
            ctx_obj=ctx_obj,
        )
        result = dispatch_request(bridge, method, path, params=params)
        formatter.print_output(result)
    finally:
        bridge.close()


def _fmt_opt() -> tuple[Any, Any, Any, Any]:
    return (
        typer.Option(None, "--output", "-o", help="Output format."),
        typer.Option(False, "--json", help="Shortcut for --output json"),
        typer.Option(False, "--yaml", help="Shortcut for --output yaml"),
        typer.Option(False, "--markdown", help="Shortcut for --output markdown"),
    )

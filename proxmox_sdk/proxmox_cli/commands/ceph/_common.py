"""Shared helpers for Ceph CLI command modules."""

from __future__ import annotations

from typing import Any, Optional

from proxmox_sdk.proxmox_cli.decorators import cli_error_handler
from proxmox_sdk.proxmox_cli.output import get_context_options

from .._common import create_formatter, ensure_service, prepare_command


@cli_error_handler
def _run_get(
    path: str,
    *,
    params: dict[str, Any] | None,
    output: Optional[str],
    json_output: bool,
    yaml_output: bool,
    markdown_output: bool,
) -> None:
    ctx_obj = get_context_options()
    config_mgr, bridge = prepare_command(ctx_obj)
    try:
        ensure_service(bridge, "PVE")
        formatter = create_formatter(
            config_mgr,
            output,
            json_output=json_output,
            yaml_output=yaml_output,
            markdown_output=markdown_output,
            ctx_obj=ctx_obj,
        )
        result = bridge.get(path, params=params)
        formatter.print_output(result)
    finally:
        bridge.close()

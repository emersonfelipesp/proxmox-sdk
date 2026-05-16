"""PBS top-level subcommand group: launches the PBS module TUI.

The PDM remote-aware PBS commands live under ``proxmox pdm pbs ...`` in
``commands/pdm.py``. This module adds a top-level ``proxmox pbs tui`` so the
PBS Textual TUI has its own dedicated entry point while still supporting
in-app view switching back to PVE/Ceph/PDM.
"""

from __future__ import annotations

import logging
from typing import Any, Optional

import typer

from proxmox_sdk.proxmox_cli.app import app
from proxmox_sdk.proxmox_cli.config import BackendConfig, ConfigManager
from proxmox_sdk.proxmox_cli.exceptions import ProxmoxCLIError
from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge
from proxmox_sdk.proxmox_cli.tui_runner import launch_tui

from ._common import apply_cli_overrides

logger = logging.getLogger(__name__)

pbs_app = typer.Typer(
    name="pbs",
    help="Proxmox Backup Server tools (TUI entry point).",
    no_args_is_help=True,
)
app.add_typer(pbs_app, name="pbs")


def _build_backend_config(ctx_obj: dict[str, Any], *, use_mock: bool) -> BackendConfig:
    config_mgr = ConfigManager()
    config_mgr.load_config(ctx_obj.get("config"))
    backend_cfg = config_mgr.get_profile()
    apply_cli_overrides(backend_cfg, ctx_obj)
    if use_mock:
        backend_cfg.backend = "mock"
    elif backend_cfg.backend == "mock":
        backend_cfg.backend = "https"
    return backend_cfg


@pbs_app.command("tui")
def tui(
    ctx: typer.Context,
    mode: Optional[str] = typer.Argument(
        None, help="Optional mode. Use 'mock' to run against the in-memory mock backend."
    ),
    path: str = typer.Option(
        "/admin/datastore",
        "--path",
        "-p",
        help="Initial API path to load (must be a PBS path).",
    ),
) -> None:
    """Launch the PBS Textual TUI."""
    bridge: ProxmoxSDKBridge | None = None
    try:
        ctx_obj = ctx.obj or {}
        use_mock = mode == "mock"
        backend_cfg = _build_backend_config(ctx_obj, use_mock=use_mock)
        bridge = ProxmoxSDKBridge.create(backend_cfg)
        launch_tui(
            bridge=bridge,
            mode="mock" if use_mock else "production",
            initial_path=path,
            initial_module="pbs",
        )
    except ProxmoxCLIError as exc:
        typer.echo(f"Error: {exc.message}", err=True)
        raise typer.Exit(code=exc.exit_code)
    except Exception as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=1)
    finally:
        if bridge is not None:
            bridge.close()


__all__ = ["pbs_app", "tui"]

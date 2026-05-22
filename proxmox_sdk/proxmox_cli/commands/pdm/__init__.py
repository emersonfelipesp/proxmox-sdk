"""PDM subcommand group: full CLI surface for Proxmox Datacenter Manager.

Mirrors the SDK domain layout in :mod:`proxmox_sdk.pdm` so every PDM SDK
operation has a matching CLI command. The command tree is::

    proxmox pdm remote   list | add | remove | update | version
    proxmox pdm pve qemu list | config | start | stop | shutdown | migrate
                          | remote-migrate | rrddata
    proxmox pdm pve lxc  list | config | start | stop | shutdown | migrate
                          | remote-migrate | rrddata
    proxmox pdm pve node list | rrddata
    proxmox pdm pve      resources | tasks
    proxmox pdm pbs datastore list | rrddata
    proxmox pdm pbs snapshot list
    proxmox pdm pbs node rrddata
    proxmox pdm pbs tasks list | status
    proxmox pdm resources list | status
    proxmox pdm subscriptions
    proxmox pdm metrics  status | trigger
    proxmox pdm access user list | create | update | delete | passwd
    proxmox pdm access acl  list | update | delete
    proxmox pdm access tfa  list | add | delete
    proxmox pdm views    list | get | create | update | delete
    proxmox pdm tui
"""

from __future__ import annotations

from typing import Optional

import typer

from proxmox_sdk.proxmox_cli.app import app
from proxmox_sdk.proxmox_cli.decorators import cli_error_handler
from proxmox_sdk.proxmox_cli.exceptions import ProxmoxCLIError
from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge

from ._bridge import _build_pdm_backend_config, _format_options, _run_request
from .access import access_app
from .metrics import metrics_app
from .pbs import pbs_app
from .pve import pve_app
from .remotes import remote_app
from .resources import resources_app, views_app

# ---------------------------------------------------------------------------
# App tree
# ---------------------------------------------------------------------------

pdm_app = typer.Typer(
    name="pdm",
    help="Proxmox Datacenter Manager (PDM) commands.",
    no_args_is_help=True,
)
app.add_typer(pdm_app, name="pdm")

pdm_app.add_typer(remote_app, name="remote")
pdm_app.add_typer(pve_app, name="pve")
pdm_app.add_typer(pbs_app, name="pbs")
pdm_app.add_typer(resources_app, name="resources")
pdm_app.add_typer(metrics_app, name="metrics")
pdm_app.add_typer(access_app, name="access")
pdm_app.add_typer(views_app, name="views")


@pdm_app.command("subscriptions")
def subscriptions(
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Show fleet-wide subscription status."""
    _run_request(
        "GET",
        "/resources/subscription",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


# ---------------------------------------------------------------------------
# TUI launcher (delegates to dedicated TUI module added in Phase 3)
# ---------------------------------------------------------------------------


@pdm_app.command("tui")
@cli_error_handler
def tui(
    ctx: typer.Context,
    mode: Optional[str] = typer.Argument(
        None, help="Optional mode. Use 'mock' to run against the in-memory mock backend."
    ),
) -> None:
    """Launch the PDM Textual TUI."""
    bridge: ProxmoxSDKBridge | None = None
    try:
        ctx_obj = ctx.obj or {}
        use_mock = mode == "mock"
        backend_cfg = _build_pdm_backend_config(ctx_obj, use_mock=use_mock)
        bridge = ProxmoxSDKBridge.create(backend_cfg)
        # Lazy-import so missing Textual surfaces a friendly error instead of
        # an import traceback.
        try:
            from proxmox_sdk.proxmox_cli.tui.runner import run_module_tui
        except ImportError:
            raise ProxmoxCLIError(
                "PDM TUI is not installed. Install with: pip install 'proxmox-sdk[cli]'",
                exit_code=1,
            )
        run_module_tui(
            bridge=bridge,
            mode="mock" if use_mock else "production",
            initial_module="pdm",
        )
    finally:
        if bridge is not None:
            bridge.close()


__all__ = ["pdm_app"]

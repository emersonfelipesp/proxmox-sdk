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

import logging
from typing import Any, Optional

import typer

from proxmox_sdk.proxmox_cli.app import app
from proxmox_sdk.proxmox_cli.config import BackendConfig, ConfigManager
from proxmox_sdk.proxmox_cli.decorators import cli_error_handler
from proxmox_sdk.proxmox_cli.exceptions import ProxmoxCLIError
from proxmox_sdk.proxmox_cli.output import get_context_options
from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge

from ._common import (
    apply_cli_overrides,
    create_formatter,
    dispatch_request,
    ensure_service,
    prepare_command,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# App tree
# ---------------------------------------------------------------------------

pdm_app = typer.Typer(
    name="pdm",
    help="Proxmox Datacenter Manager (PDM) commands.",
    no_args_is_help=True,
)
app.add_typer(pdm_app, name="pdm")

remote_app = typer.Typer(name="remote", help="Manage PDM remotes.", no_args_is_help=True)
pve_app = typer.Typer(
    name="pve", help="PDM operations on registered PVE remotes.", no_args_is_help=True
)
pve_qemu_app = typer.Typer(name="qemu", help="QEMU VMs on a PVE remote.", no_args_is_help=True)
pve_lxc_app = typer.Typer(name="lxc", help="LXC containers on a PVE remote.", no_args_is_help=True)
pve_node_app = typer.Typer(name="node", help="PVE nodes on a remote.", no_args_is_help=True)
pbs_app = typer.Typer(
    name="pbs", help="PDM operations on registered PBS remotes.", no_args_is_help=True
)
pbs_datastore_app = typer.Typer(name="datastore", help="PBS datastores.", no_args_is_help=True)
pbs_snapshot_app = typer.Typer(name="snapshot", help="PBS snapshots.", no_args_is_help=True)
pbs_node_app = typer.Typer(name="node", help="PBS node operations.", no_args_is_help=True)
pbs_tasks_app = typer.Typer(name="tasks", help="PBS tasks.", no_args_is_help=True)
resources_app = typer.Typer(
    name="resources", help="Global cross-remote resources.", no_args_is_help=True
)
metrics_app = typer.Typer(name="metrics", help="Metric collection.", no_args_is_help=True)
access_app = typer.Typer(name="access", help="Users, ACL, TFA.", no_args_is_help=True)
access_user_app = typer.Typer(name="user", help="User accounts.", no_args_is_help=True)
access_acl_app = typer.Typer(name="acl", help="Access control entries.", no_args_is_help=True)
access_tfa_app = typer.Typer(name="tfa", help="Two-factor auth.", no_args_is_help=True)
views_app = typer.Typer(name="views", help="Custom cross-remote dashboards.", no_args_is_help=True)

pdm_app.add_typer(remote_app, name="remote")
pdm_app.add_typer(pve_app, name="pve")
pve_app.add_typer(pve_qemu_app, name="qemu")
pve_app.add_typer(pve_lxc_app, name="lxc")
pve_app.add_typer(pve_node_app, name="node")
pdm_app.add_typer(pbs_app, name="pbs")
pbs_app.add_typer(pbs_datastore_app, name="datastore")
pbs_app.add_typer(pbs_snapshot_app, name="snapshot")
pbs_app.add_typer(pbs_node_app, name="node")
pbs_app.add_typer(pbs_tasks_app, name="tasks")
pdm_app.add_typer(resources_app, name="resources")
pdm_app.add_typer(metrics_app, name="metrics")
pdm_app.add_typer(access_app, name="access")
access_app.add_typer(access_user_app, name="user")
access_app.add_typer(access_acl_app, name="acl")
access_app.add_typer(access_tfa_app, name="tfa")
pdm_app.add_typer(views_app, name="views")


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


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


# ---------------------------------------------------------------------------
# Remote commands
# ---------------------------------------------------------------------------


@remote_app.command("list")
def remote_list(
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List registered PDM remotes."""
    _run_request(
        "GET",
        "/remotes",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@remote_app.command("version")
def remote_version(
    remote: str = typer.Argument(..., help="Remote id."),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Query the version of a registered remote."""
    _run_request(
        "GET",
        f"/remotes/{remote}/version",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@remote_app.command("add")
def remote_add(
    id: str = typer.Argument(..., help="Remote id."),
    type: str = typer.Option(..., "--type", "-t", help="Remote type (pve or pbs)."),
    authid: Optional[str] = typer.Option(None, "--authid"),
    token: Optional[str] = typer.Option(None, "--token"),
    fingerprint: Optional[str] = typer.Option(None, "--fingerprint"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Register a new PVE or PBS remote with PDM."""
    params: dict[str, Any] = {"id": id, "type": type}
    if authid is not None:
        params["authid"] = authid
    if token is not None:
        params["token"] = token
    if fingerprint is not None:
        params["fingerprint"] = fingerprint
    _run_request(
        "POST",
        "/remotes",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@remote_app.command("update")
def remote_update(
    remote: str = typer.Argument(..., help="Remote id."),
    token: Optional[str] = typer.Option(None, "--token"),
    fingerprint: Optional[str] = typer.Option(None, "--fingerprint"),
    authid: Optional[str] = typer.Option(None, "--authid"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Update a registered remote."""
    params: dict[str, Any] = {}
    if token is not None:
        params["token"] = token
    if fingerprint is not None:
        params["fingerprint"] = fingerprint
    if authid is not None:
        params["authid"] = authid
    _run_request(
        "PUT",
        f"/remotes/{remote}",
        params=params or None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@remote_app.command("remove")
def remote_remove(
    remote: str = typer.Argument(..., help="Remote id."),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Unregister a remote."""
    _run_request(
        "DELETE",
        f"/remotes/{remote}",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


# ---------------------------------------------------------------------------
# PVE guest commands (qemu + lxc share the same shape)
# ---------------------------------------------------------------------------


def _register_guest_commands(group: typer.Typer, kind: str) -> None:
    """Wire start/stop/shutdown/etc. onto a qemu or lxc Typer group."""

    @group.command("list")
    def _list(
        remote: str = typer.Argument(..., help="Remote id."),
        output: Optional[str] = typer.Option(None, "--output", "-o"),
        json_output: bool = typer.Option(False, "--json"),
        yaml_output: bool = typer.Option(False, "--yaml"),
        markdown_output: bool = typer.Option(False, "--markdown"),
    ) -> None:
        """List guests on the remote."""
        _run_request(
            "GET",
            f"/pve/remotes/{remote}/guests/{kind}",
            params=None,
            **_format_options(output, json_output, yaml_output, markdown_output),
        )

    @group.command("config")
    def _config(
        remote: str = typer.Argument(...),
        vmid: int = typer.Argument(...),
        output: Optional[str] = typer.Option(None, "--output", "-o"),
        json_output: bool = typer.Option(False, "--json"),
        yaml_output: bool = typer.Option(False, "--yaml"),
        markdown_output: bool = typer.Option(False, "--markdown"),
    ) -> None:
        """Show a guest configuration."""
        _run_request(
            "GET",
            f"/pve/remotes/{remote}/guests/{kind}/{vmid}/config",
            params=None,
            **_format_options(output, json_output, yaml_output, markdown_output),
        )

    @group.command("start")
    def _start(
        remote: str = typer.Argument(...),
        vmid: int = typer.Argument(...),
        output: Optional[str] = typer.Option(None, "--output", "-o"),
        json_output: bool = typer.Option(False, "--json"),
        yaml_output: bool = typer.Option(False, "--yaml"),
        markdown_output: bool = typer.Option(False, "--markdown"),
    ) -> None:
        """Start the guest."""
        _run_request(
            "POST",
            f"/pve/remotes/{remote}/guests/{kind}/{vmid}/start",
            params=None,
            **_format_options(output, json_output, yaml_output, markdown_output),
        )

    @group.command("stop")
    def _stop(
        remote: str = typer.Argument(...),
        vmid: int = typer.Argument(...),
        output: Optional[str] = typer.Option(None, "--output", "-o"),
        json_output: bool = typer.Option(False, "--json"),
        yaml_output: bool = typer.Option(False, "--yaml"),
        markdown_output: bool = typer.Option(False, "--markdown"),
    ) -> None:
        """Force-stop the guest."""
        _run_request(
            "POST",
            f"/pve/remotes/{remote}/guests/{kind}/{vmid}/stop",
            params=None,
            **_format_options(output, json_output, yaml_output, markdown_output),
        )

    @group.command("shutdown")
    def _shutdown(
        remote: str = typer.Argument(...),
        vmid: int = typer.Argument(...),
        output: Optional[str] = typer.Option(None, "--output", "-o"),
        json_output: bool = typer.Option(False, "--json"),
        yaml_output: bool = typer.Option(False, "--yaml"),
        markdown_output: bool = typer.Option(False, "--markdown"),
    ) -> None:
        """Gracefully shut down the guest."""
        _run_request(
            "POST",
            f"/pve/remotes/{remote}/guests/{kind}/{vmid}/shutdown",
            params=None,
            **_format_options(output, json_output, yaml_output, markdown_output),
        )

    @group.command("migrate")
    def _migrate(
        remote: str = typer.Argument(...),
        vmid: int = typer.Argument(...),
        target: str = typer.Option(..., "--target", help="Target node name."),
        online: bool = typer.Option(False, "--online"),
        output: Optional[str] = typer.Option(None, "--output", "-o"),
        json_output: bool = typer.Option(False, "--json"),
        yaml_output: bool = typer.Option(False, "--yaml"),
        markdown_output: bool = typer.Option(False, "--markdown"),
    ) -> None:
        """Migrate the guest within the same cluster."""
        params: dict[str, Any] = {"target": target}
        if online:
            params["online"] = True
        _run_request(
            "POST",
            f"/pve/remotes/{remote}/guests/{kind}/{vmid}/migrate",
            params=params,
            **_format_options(output, json_output, yaml_output, markdown_output),
        )

    @group.command("remote-migrate")
    def _remote_migrate(
        remote: str = typer.Argument(...),
        vmid: int = typer.Argument(...),
        target_remote: str = typer.Option(..., "--target-remote"),
        target_vmid: Optional[int] = typer.Option(None, "--target-vmid"),
        target_node: Optional[str] = typer.Option(None, "--target-node"),
        online: bool = typer.Option(False, "--online"),
        output: Optional[str] = typer.Option(None, "--output", "-o"),
        json_output: bool = typer.Option(False, "--json"),
        yaml_output: bool = typer.Option(False, "--yaml"),
        markdown_output: bool = typer.Option(False, "--markdown"),
    ) -> None:
        """Migrate the guest to another registered PDM cluster."""
        params: dict[str, Any] = {"target-remote": target_remote}
        if target_vmid is not None:
            params["target-vmid"] = target_vmid
        if target_node is not None:
            params["target-node"] = target_node
        if online:
            params["online"] = True
        _run_request(
            "POST",
            f"/pve/remotes/{remote}/guests/{kind}/{vmid}/remote-migrate",
            params=params,
            **_format_options(output, json_output, yaml_output, markdown_output),
        )

    @group.command("rrddata")
    def _rrddata(
        remote: str = typer.Argument(...),
        vmid: int = typer.Argument(...),
        timeframe: str = typer.Option("hour", "--timeframe"),
        cf: Optional[str] = typer.Option(None, "--cf"),
        output: Optional[str] = typer.Option(None, "--output", "-o"),
        json_output: bool = typer.Option(False, "--json"),
        yaml_output: bool = typer.Option(False, "--yaml"),
        markdown_output: bool = typer.Option(False, "--markdown"),
    ) -> None:
        """Fetch RRD samples for the guest."""
        params: dict[str, Any] = {"timeframe": timeframe}
        if cf is not None:
            params["cf"] = cf
        _run_request(
            "GET",
            f"/pve/remotes/{remote}/guests/{kind}/{vmid}/rrddata",
            params=params,
            **_format_options(output, json_output, yaml_output, markdown_output),
        )


_register_guest_commands(pve_qemu_app, "qemu")
_register_guest_commands(pve_lxc_app, "lxc")


# ---------------------------------------------------------------------------
# PVE nodes + cluster
# ---------------------------------------------------------------------------


@pve_node_app.command("list")
def pve_node_list(
    remote: str = typer.Argument(..., help="Remote id."),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List PVE nodes on a remote."""
    _run_request(
        "GET",
        f"/pve/remotes/{remote}/nodes",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@pve_node_app.command("rrddata")
def pve_node_rrddata(
    remote: str = typer.Argument(...),
    node: str = typer.Argument(...),
    timeframe: str = typer.Option("hour", "--timeframe"),
    cf: Optional[str] = typer.Option(None, "--cf"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Fetch RRD samples for a node."""
    params: dict[str, Any] = {"timeframe": timeframe}
    if cf is not None:
        params["cf"] = cf
    _run_request(
        "GET",
        f"/pve/remotes/{remote}/nodes/{node}/rrddata",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@pve_app.command("resources")
def pve_resources(
    remote: str = typer.Argument(...),
    type: Optional[str] = typer.Option(None, "--type"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Query resources on a PVE remote."""
    params: dict[str, Any] = {}
    if type is not None:
        params["type"] = type
    _run_request(
        "GET",
        f"/pve/remotes/{remote}/resources",
        params=params or None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@pve_app.command("tasks")
def pve_tasks(
    remote: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List tasks on a PVE remote."""
    _run_request(
        "GET",
        f"/pve/remotes/{remote}/tasks",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


# ---------------------------------------------------------------------------
# PBS commands
# ---------------------------------------------------------------------------


@pbs_datastore_app.command("list")
def pbs_datastore_list(
    remote: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List PBS datastores on a remote."""
    _run_request(
        "GET",
        f"/pbs/remotes/{remote}/datastores",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@pbs_datastore_app.command("rrddata")
def pbs_datastore_rrddata(
    remote: str = typer.Argument(...),
    store: str = typer.Argument(...),
    timeframe: str = typer.Option("hour", "--timeframe"),
    cf: Optional[str] = typer.Option(None, "--cf"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Fetch RRD samples for a PBS datastore."""
    params: dict[str, Any] = {"timeframe": timeframe}
    if cf is not None:
        params["cf"] = cf
    _run_request(
        "GET",
        f"/pbs/remotes/{remote}/datastores/{store}/rrddata",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@pbs_snapshot_app.command("list")
def pbs_snapshot_list(
    remote: str = typer.Argument(...),
    store: str = typer.Argument(...),
    namespace: Optional[str] = typer.Option(None, "--namespace", "--ns"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List snapshots in a PBS datastore."""
    params: dict[str, Any] = {}
    if namespace is not None:
        params["ns"] = namespace
    _run_request(
        "GET",
        f"/pbs/remotes/{remote}/datastores/{store}/snapshots",
        params=params or None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@pbs_node_app.command("rrddata")
def pbs_node_rrddata(
    remote: str = typer.Argument(...),
    timeframe: str = typer.Option("hour", "--timeframe"),
    cf: Optional[str] = typer.Option(None, "--cf"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Fetch RRD samples for the PBS node."""
    params: dict[str, Any] = {"timeframe": timeframe}
    if cf is not None:
        params["cf"] = cf
    _run_request(
        "GET",
        f"/pbs/remotes/{remote}/node/rrddata",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@pbs_tasks_app.command("list")
def pbs_tasks_list(
    remote: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List tasks on a PBS remote."""
    _run_request(
        "GET",
        f"/pbs/remotes/{remote}/tasks",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@pbs_tasks_app.command("status")
def pbs_tasks_status(
    remote: str = typer.Argument(...),
    upid: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Show the status of a PBS task."""
    _run_request(
        "GET",
        f"/pbs/remotes/{remote}/tasks/{upid}/status",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


# ---------------------------------------------------------------------------
# Global resources / subscriptions / metrics
# ---------------------------------------------------------------------------


@resources_app.command("list")
def resources_list(
    type: Optional[str] = typer.Option(None, "--type"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List global resources across every remote."""
    params: dict[str, Any] = {}
    if type is not None:
        params["type"] = type
    _run_request(
        "GET",
        "/resources/list",
        params=params or None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@resources_app.command("status")
def resources_status(
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Show per-remote connectivity status."""
    _run_request(
        "GET",
        "/resources/status",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


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


@metrics_app.command("status")
def metrics_status(
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Show metric collection status."""
    _run_request(
        "GET",
        "/config/metrics/status",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@metrics_app.command("trigger")
def metrics_trigger(
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Manually trigger metric collection."""
    _run_request(
        "POST",
        "/config/metrics/trigger",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


# ---------------------------------------------------------------------------
# Access (users / acl / tfa)
# ---------------------------------------------------------------------------


@access_user_app.command("list")
def user_list(
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List PDM users."""
    _run_request(
        "GET",
        "/access/users",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_user_app.command("create")
def user_create(
    userid: str = typer.Argument(..., help="user@realm"),
    comment: Optional[str] = typer.Option(None, "--comment"),
    email: Optional[str] = typer.Option(None, "--email"),
    enable: Optional[bool] = typer.Option(None, "--enable/--disable"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Create a PDM user."""
    params: dict[str, Any] = {"userid": userid}
    if comment is not None:
        params["comment"] = comment
    if email is not None:
        params["email"] = email
    if enable is not None:
        params["enable"] = enable
    _run_request(
        "POST",
        "/access/users",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_user_app.command("update")
def user_update(
    userid: str = typer.Argument(...),
    comment: Optional[str] = typer.Option(None, "--comment"),
    email: Optional[str] = typer.Option(None, "--email"),
    enable: Optional[bool] = typer.Option(None, "--enable/--disable"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Update a PDM user."""
    params: dict[str, Any] = {}
    if comment is not None:
        params["comment"] = comment
    if email is not None:
        params["email"] = email
    if enable is not None:
        params["enable"] = enable
    _run_request(
        "PUT",
        f"/access/users/{userid}",
        params=params or None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_user_app.command("delete")
def user_delete(
    userid: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Delete a PDM user."""
    _run_request(
        "DELETE",
        f"/access/users/{userid}",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_user_app.command("passwd")
def user_passwd(
    userid: str = typer.Argument(...),
    password: str = typer.Option(..., "--password", prompt=True, hide_input=True),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Change the password of a PDM user."""
    _run_request(
        "PUT",
        "/access/password",
        params={"userid": userid, "password": password},
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_acl_app.command("list")
def acl_list(
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List ACL entries."""
    _run_request(
        "GET",
        "/access/acl",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_acl_app.command("update")
def acl_update(
    path: str = typer.Option(..., "--path"),
    roles: str = typer.Option(..., "--roles"),
    users: Optional[str] = typer.Option(None, "--users"),
    groups: Optional[str] = typer.Option(None, "--groups"),
    propagate: Optional[bool] = typer.Option(None, "--propagate/--no-propagate"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Add or update an ACL entry."""
    params: dict[str, Any] = {"path": path, "roles": roles}
    if users is not None:
        params["users"] = users
    if groups is not None:
        params["groups"] = groups
    if propagate is not None:
        params["propagate"] = propagate
    _run_request(
        "PUT",
        "/access/acl",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_acl_app.command("delete")
def acl_delete(
    path: str = typer.Option(..., "--path"),
    roles: str = typer.Option(..., "--roles"),
    users: Optional[str] = typer.Option(None, "--users"),
    groups: Optional[str] = typer.Option(None, "--groups"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Remove an ACL entry."""
    params: dict[str, Any] = {"path": path, "roles": roles, "delete": 1}
    if users is not None:
        params["users"] = users
    if groups is not None:
        params["groups"] = groups
    _run_request(
        "PUT",
        "/access/acl",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_tfa_app.command("list")
def tfa_list(
    userid: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List TFA factors for a user."""
    _run_request(
        "GET",
        f"/access/tfa/{userid}",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_tfa_app.command("add")
def tfa_add(
    userid: str = typer.Argument(...),
    type: str = typer.Option(..., "--type", help="totp, webauthn, recovery, …"),
    description: Optional[str] = typer.Option(None, "--description"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Add a TFA factor to a user."""
    params: dict[str, Any] = {"type": type}
    if description is not None:
        params["description"] = description
    _run_request(
        "POST",
        f"/access/tfa/{userid}",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@access_tfa_app.command("delete")
def tfa_delete(
    userid: str = typer.Argument(...),
    tfa_id: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Remove a TFA factor."""
    _run_request(
        "DELETE",
        f"/access/tfa/{userid}/{tfa_id}",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


# ---------------------------------------------------------------------------
# Views
# ---------------------------------------------------------------------------


@views_app.command("list")
def views_list(
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """List custom views."""
    _run_request(
        "GET",
        "/config/views",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@views_app.command("get")
def views_get(
    view_id: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Show a custom view."""
    _run_request(
        "GET",
        f"/config/views/{view_id}",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@views_app.command("create")
def views_create(
    id: str = typer.Argument(...),
    name: Optional[str] = typer.Option(None, "--name"),
    comment: Optional[str] = typer.Option(None, "--comment"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Create a custom view."""
    params: dict[str, Any] = {"id": id}
    if name is not None:
        params["name"] = name
    if comment is not None:
        params["comment"] = comment
    _run_request(
        "POST",
        "/config/views",
        params=params,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@views_app.command("update")
def views_update(
    view_id: str = typer.Argument(...),
    name: Optional[str] = typer.Option(None, "--name"),
    comment: Optional[str] = typer.Option(None, "--comment"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Update a custom view."""
    params: dict[str, Any] = {}
    if name is not None:
        params["name"] = name
    if comment is not None:
        params["comment"] = comment
    _run_request(
        "PUT",
        f"/config/views/{view_id}",
        params=params or None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@views_app.command("delete")
def views_delete(
    view_id: str = typer.Argument(...),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Delete a custom view."""
    _run_request(
        "DELETE",
        f"/config/views/{view_id}",
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

"""PDM commands for registered PVE remotes."""

from __future__ import annotations

from typing import Any, Optional

import typer

from ._bridge import _format_options, _run_request

pve_app = typer.Typer(
    name="pve", help="PDM operations on registered PVE remotes.", no_args_is_help=True
)
pve_qemu_app = typer.Typer(name="qemu", help="QEMU VMs on a PVE remote.", no_args_is_help=True)
pve_lxc_app = typer.Typer(name="lxc", help="LXC containers on a PVE remote.", no_args_is_help=True)
pve_node_app = typer.Typer(name="node", help="PVE nodes on a remote.", no_args_is_help=True)

pve_app.add_typer(pve_qemu_app, name="qemu")
pve_app.add_typer(pve_lxc_app, name="lxc")
pve_app.add_typer(pve_node_app, name="node")


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

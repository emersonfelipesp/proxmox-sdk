"""PDM commands for registered PBS remotes."""

from __future__ import annotations

from typing import Any, Optional

import typer

from ._bridge import PDMRRDConsolidation, PDMRRDTimeframe, _format_options, _run_request

pbs_app = typer.Typer(
    name="pbs", help="PDM operations on registered PBS remotes.", no_args_is_help=True
)
pbs_datastore_app = typer.Typer(name="datastore", help="PBS datastores.", no_args_is_help=True)
pbs_snapshot_app = typer.Typer(name="snapshot", help="PBS snapshots.", no_args_is_help=True)
pbs_node_app = typer.Typer(name="node", help="PBS node operations.", no_args_is_help=True)
pbs_tasks_app = typer.Typer(name="tasks", help="PBS tasks.", no_args_is_help=True)

pbs_app.add_typer(pbs_datastore_app, name="datastore")
pbs_app.add_typer(pbs_snapshot_app, name="snapshot")
pbs_app.add_typer(pbs_node_app, name="node")
pbs_app.add_typer(pbs_tasks_app, name="tasks")


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
        f"/pbs/remotes/{remote}/datastore",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@pbs_datastore_app.command("rrddata")
def pbs_datastore_rrddata(
    remote: str = typer.Argument(...),
    store: str = typer.Argument(...),
    timeframe: PDMRRDTimeframe = typer.Option(PDMRRDTimeframe.HOUR, "--timeframe"),
    cf: PDMRRDConsolidation = typer.Option(PDMRRDConsolidation.AVERAGE, "--cf"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Fetch RRD samples for a PBS datastore."""
    params: dict[str, Any] = {"timeframe": timeframe.value, "cf": cf.value}
    _run_request(
        "GET",
        f"/pbs/remotes/{remote}/datastore/{store}/rrddata",
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
        f"/pbs/remotes/{remote}/datastore/{store}/snapshots",
        params=params or None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )


@pbs_node_app.command("rrddata")
def pbs_node_rrddata(
    remote: str = typer.Argument(...),
    timeframe: PDMRRDTimeframe = typer.Option(PDMRRDTimeframe.HOUR, "--timeframe"),
    cf: PDMRRDConsolidation = typer.Option(PDMRRDConsolidation.AVERAGE, "--cf"),
    output: Optional[str] = typer.Option(None, "--output", "-o"),
    json_output: bool = typer.Option(False, "--json"),
    yaml_output: bool = typer.Option(False, "--yaml"),
    markdown_output: bool = typer.Option(False, "--markdown"),
) -> None:
    """Fetch RRD samples for the PBS node."""
    params: dict[str, Any] = {"timeframe": timeframe.value, "cf": cf.value}
    _run_request(
        "GET",
        f"/pbs/remotes/{remote}/rrddata",
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

"""PDM metric collection commands."""

from __future__ import annotations

from typing import Optional

import typer

from ._bridge import _format_options, _run_request

metrics_app = typer.Typer(name="metrics", help="Metric collection.", no_args_is_help=True)


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
        "/remotes/metric-collection/status",
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
        "/remotes/metric-collection/trigger",
        params=None,
        **_format_options(output, json_output, yaml_output, markdown_output),
    )

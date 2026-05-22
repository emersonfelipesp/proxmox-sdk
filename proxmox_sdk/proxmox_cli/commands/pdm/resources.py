"""PDM global resource and view commands."""

from __future__ import annotations

from typing import Any, Optional

import typer

from ._bridge import _format_options, _run_request

resources_app = typer.Typer(
    name="resources", help="Global cross-remote resources.", no_args_is_help=True
)
views_app = typer.Typer(name="views", help="Custom cross-remote dashboards.", no_args_is_help=True)


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

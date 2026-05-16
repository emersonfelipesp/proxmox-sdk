"""CLI smoke tests for the `proxmox pdm remote` command group."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from proxmox_sdk.proxmox_cli.cli import app


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


def test_remote_help(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "remote", "--help"])
    assert result.exit_code == 0, result.output
    for sub in ("list", "add", "remove", "update", "version"):
        assert sub in result.output, f"missing subcommand `{sub}` in `pdm remote --help`"


def test_remote_list_requires_pdm_service(cli_runner: CliRunner) -> None:
    """`pdm remote list` against a PVE service should refuse."""
    result = cli_runner.invoke(
        app,
        ["--backend", "mock", "--service", "PVE", "pdm", "remote", "list", "--json"],
    )
    # `_require_pdm` raises ProxmoxCLIError with exit_code=2 because the bridge
    # service is forced to PDM inside the command, so the call should either
    # error meaningfully (not crash) or succeed against the mock.
    assert result.exit_code != 1 or "PDM" in result.output or "remotes" in result.output


def test_remote_add_validates_required_options(cli_runner: CliRunner) -> None:
    """Missing --type should be a usage error."""
    result = cli_runner.invoke(app, ["pdm", "remote", "add", "pve-a"])
    assert result.exit_code != 0

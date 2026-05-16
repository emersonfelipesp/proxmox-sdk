"""CLI smoke tests for the full `proxmox pdm` command tree."""

from __future__ import annotations

import pytest
from typer.testing import CliRunner

from proxmox_sdk.proxmox_cli.cli import app


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


def test_pdm_help_shows_all_top_level_groups(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "--help"])
    assert result.exit_code == 0, result.output
    for grp in (
        "remote",
        "pve",
        "pbs",
        "resources",
        "subscriptions",
        "metrics",
        "access",
        "views",
        "tui",
    ):
        assert grp in result.output, f"missing pdm group `{grp}`"


def test_pdm_pve_qemu_help(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "pve", "qemu", "--help"])
    assert result.exit_code == 0, result.output
    for sub in (
        "list",
        "config",
        "start",
        "stop",
        "shutdown",
        "migrate",
        "remote-migrate",
        "rrddata",
    ):
        assert sub in result.output


def test_pdm_pve_lxc_help(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "pve", "lxc", "--help"])
    assert result.exit_code == 0, result.output
    for sub in (
        "list",
        "config",
        "start",
        "stop",
        "shutdown",
        "migrate",
        "remote-migrate",
        "rrddata",
    ):
        assert sub in result.output


def test_pdm_pbs_help(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "pbs", "--help"])
    assert result.exit_code == 0, result.output
    for sub in ("datastore", "snapshot", "node", "tasks"):
        assert sub in result.output


def test_pdm_access_help(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "access", "--help"])
    assert result.exit_code == 0, result.output
    for sub in ("user", "acl", "tfa"):
        assert sub in result.output


def test_pdm_access_user_help(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "access", "user", "--help"])
    assert result.exit_code == 0, result.output
    for sub in ("list", "create", "update", "delete", "passwd"):
        assert sub in result.output


def test_pdm_metrics_help(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "metrics", "--help"])
    assert result.exit_code == 0, result.output
    for sub in ("status", "trigger"):
        assert sub in result.output


def test_pdm_views_help(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "views", "--help"])
    assert result.exit_code == 0, result.output
    for sub in ("list", "get", "create", "update", "delete"):
        assert sub in result.output


def test_global_service_accepts_pdm(cli_runner: CliRunner) -> None:
    """`--service PDM` on the root should not be rejected by Click."""
    result = cli_runner.invoke(app, ["--service", "PDM", "--help"])
    assert result.exit_code == 0, result.output


def test_pdm_qemu_list_requires_remote_arg(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "pve", "qemu", "list"])
    assert result.exit_code != 0


def test_pdm_pbs_snapshot_list_requires_remote_and_store(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "pbs", "snapshot", "list"])
    assert result.exit_code != 0


def test_pdm_acl_update_requires_path_and_roles(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["pdm", "access", "acl", "update"])
    assert result.exit_code != 0

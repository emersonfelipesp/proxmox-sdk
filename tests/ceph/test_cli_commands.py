"""Smoke tests for the `proxmox ceph` Typer subcommand group."""

from __future__ import annotations

import json

import pytest
from typer.testing import CliRunner

from proxmox_sdk.proxmox_cli.cli import app


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


def test_ceph_help(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["ceph", "--help"])
    assert result.exit_code == 0, result.output
    out = result.output
    for sub in (
        "status",
        "metadata",
        "flags",
        "flag",
        "monitors",
        "managers",
        "mds",
        "osds",
        "osd",
        "pools",
        "pool",
        "fs",
        "rules",
        "log",
        "tui",
    ):
        assert sub in out, f"missing subcommand `{sub}` in `ceph --help` output"


def test_ceph_status_mock_json(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["--backend", "mock", "ceph", "status", "--json"])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.stdout)
    assert isinstance(payload, (dict, list))


def test_ceph_flags_mock(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["--backend", "mock", "ceph", "flags", "--json"])
    assert result.exit_code == 0, result.output


def test_ceph_osds_mock_requires_node(cli_runner: CliRunner) -> None:
    # Missing node argument should be a usage error.
    result = cli_runner.invoke(app, ["--backend", "mock", "ceph", "osds"])
    assert result.exit_code != 0


def test_ceph_osds_mock(cli_runner: CliRunner) -> None:
    result = cli_runner.invoke(app, ["--backend", "mock", "ceph", "osds", "pve1", "--json"])
    assert result.exit_code == 0, result.output


def test_ceph_rejects_non_pve(cli_runner: CliRunner) -> None:
    # PMG service has no Ceph endpoints; CLI should reject the call.
    result = cli_runner.invoke(app, ["--backend", "mock", "--service", "PMG", "ceph", "status"])
    assert result.exit_code == 2
    assert "PVE" in result.output

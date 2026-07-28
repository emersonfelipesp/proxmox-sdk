"""CLI smoke tests for the full `proxmox pdm` command tree."""

from __future__ import annotations

from typing import Any

import pytest
from typer.testing import CliRunner

from proxmox_sdk.proxmox_cli.cli import app
from proxmox_sdk.proxmox_cli.commands.pdm import access as access_commands
from proxmox_sdk.proxmox_cli.commands.pdm import metrics as metrics_commands
from proxmox_sdk.proxmox_cli.commands.pdm import pbs as pbs_commands
from proxmox_sdk.proxmox_cli.commands.pdm import pve as pve_commands
from proxmox_sdk.proxmox_cli.commands.pdm import remotes as remote_commands
from proxmox_sdk.proxmox_cli.commands.pdm import resources as resource_commands


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


@pytest.fixture
def captured_requests(
    monkeypatch: pytest.MonkeyPatch,
) -> list[tuple[str, str, dict[str, Any] | None]]:
    """Capture PDM CLI transport requests without contacting a backend."""

    captured: list[tuple[str, str, dict[str, Any] | None]] = []

    def record_request(
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None,
        **_: Any,
    ) -> None:
        captured.append((method, path, params))

    for module in (
        access_commands,
        metrics_commands,
        pbs_commands,
        pve_commands,
        remote_commands,
        resource_commands,
    ):
        monkeypatch.setattr(module, "_run_request", record_request)
    return captured


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


@pytest.mark.parametrize(
    "arguments",
    [
        ["pve", "qemu", "config", "pve-a", "100", "--state", "invalid"],
        ["pve", "qemu", "rrddata", "pve-a", "100", "--cf", "LAST"],
        ["pbs", "node", "rrddata", "pbs-a", "--timeframe", "forever"],
        ["pve", "resources", "pve-a", "--type", "guest"],
        ["resources", "list", "--type", "guest"],
    ],
)
def test_pdm_schema_enum_options_reject_invalid_values(
    cli_runner: CliRunner,
    arguments: list[str],
) -> None:
    result = cli_runner.invoke(app, ["pdm", *arguments])
    assert result.exit_code != 0


@pytest.mark.parametrize(
    ("arguments", "expected"),
    [
        (["remote", "list"], ("GET", "/remotes/remote", None)),
        (
            ["remote", "version", "pve-a"],
            ("GET", "/remotes/remote/pve-a/version", None),
        ),
        (
            ["remote", "add", "pve-a", "--type", "pve"],
            ("POST", "/remotes/remote", {"id": "pve-a", "type": "pve"}),
        ),
        (
            ["remote", "update", "pve-a", "--authid", "root@pam!pdm"],
            ("PUT", "/remotes/remote/pve-a", {"authid": "root@pam!pdm"}),
        ),
        (["remote", "remove", "pve-a"], ("DELETE", "/remotes/remote/pve-a", None)),
        (["pve", "qemu", "list", "pve-a"], ("GET", "/pve/remotes/pve-a/qemu", None)),
        (
            ["pve", "qemu", "config", "pve-a", "100"],
            ("GET", "/pve/remotes/pve-a/qemu/100/config", {"state": "pending"}),
        ),
        (
            ["pve", "qemu", "start", "pve-a", "100"],
            ("POST", "/pve/remotes/pve-a/qemu/100/start", None),
        ),
        (
            ["pve", "qemu", "stop", "pve-a", "100"],
            ("POST", "/pve/remotes/pve-a/qemu/100/stop", None),
        ),
        (
            ["pve", "qemu", "shutdown", "pve-a", "100"],
            ("POST", "/pve/remotes/pve-a/qemu/100/shutdown", None),
        ),
        (
            ["pve", "qemu", "migrate", "pve-a", "100", "--target", "node-b"],
            ("POST", "/pve/remotes/pve-a/qemu/100/migrate", {"target": "node-b"}),
        ),
        (
            [
                "pve",
                "qemu",
                "remote-migrate",
                "pve-a",
                "100",
                "--target-remote",
                "pve-b",
            ],
            (
                "POST",
                "/pve/remotes/pve-a/qemu/100/remote-migrate",
                {"target-remote": "pve-b"},
            ),
        ),
        (
            ["pve", "qemu", "rrddata", "pve-a", "100"],
            (
                "GET",
                "/pve/remotes/pve-a/qemu/100/rrddata",
                {"timeframe": "hour", "cf": "AVERAGE"},
            ),
        ),
        (["pve", "lxc", "list", "pve-a"], ("GET", "/pve/remotes/pve-a/lxc", None)),
        (
            ["pve", "resources", "pve-a", "--type", "vm"],
            ("GET", "/pve/remotes/pve-a/resources", {"kind": "vm"}),
        ),
        (
            ["pbs", "datastore", "list", "pbs-a"],
            ("GET", "/pbs/remotes/pbs-a/datastore", None),
        ),
        (
            ["pbs", "datastore", "rrddata", "pbs-a", "tank"],
            (
                "GET",
                "/pbs/remotes/pbs-a/datastore/tank/rrddata",
                {"timeframe": "hour", "cf": "AVERAGE"},
            ),
        ),
        (
            ["pbs", "snapshot", "list", "pbs-a", "tank", "--namespace", "prod"],
            ("GET", "/pbs/remotes/pbs-a/datastore/tank/snapshots", {"ns": "prod"}),
        ),
        (
            ["pbs", "node", "rrddata", "pbs-a"],
            (
                "GET",
                "/pbs/remotes/pbs-a/rrddata",
                {"timeframe": "hour", "cf": "AVERAGE"},
            ),
        ),
        (
            ["resources", "list", "--type", "vm"],
            ("GET", "/resources/list", {"resource-type": "qemu"}),
        ),
        (
            ["metrics", "status"],
            ("GET", "/remotes/metric-collection/status", None),
        ),
        (
            ["metrics", "trigger"],
            ("POST", "/remotes/metric-collection/trigger", None),
        ),
        (
            ["access", "user", "passwd", "alice@pdm", "--password", "secret"],
            (
                "PUT",
                "/access/users/alice@pdm",
                {"userid": "alice@pdm", "password": "secret"},
            ),
        ),
    ],
)
def test_pdm_commands_use_captured_schema_paths(
    cli_runner: CliRunner,
    captured_requests: list[tuple[str, str, dict[str, Any] | None]],
    arguments: list[str],
    expected: tuple[str, str, dict[str, Any] | None],
) -> None:
    result = cli_runner.invoke(app, ["pdm", *arguments])

    assert result.exit_code == 0, result.output
    assert captured_requests == [expected]

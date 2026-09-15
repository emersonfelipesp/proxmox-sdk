"""Unit and end-to-end tests for live-credential snapshotting before proxmox_sdk.main import."""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from proxmox_sdk.proxmox.config import ProxmoxConfig
from tests.conftest import (
    MASKED_SENTINEL,
    live_suite_selected,
    resolve_live_credentials,
    snapshot_live_credentials,
)

_ORIGINAL_SECRET = "original-secret-value"
_REPO_ROOT = Path(__file__).resolve().parents[1]
_REPO_CONFTEST = Path(__file__).resolve().parent / "conftest.py"


# ---------------------------------------------------------------------------
# live_suite_selected unit tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("markexpr", "expected"),
    [
        ("live", True),
        ("not live", False),
        ("", False),
        ("live and not slow", True),
        ("(live)", True),
        ("(live) and not slow", True),
        ("ceph or (live)", True),
        ("(not live)", False),
        ("live_ceph", False),
        ("not live_ceph", False),
    ],
)
def test_live_suite_selected_markexpr(markexpr: str, expected: bool) -> None:
    assert live_suite_selected(markexpr, ()) is expected


@pytest.mark.parametrize(
    ("arg", "expected"),
    [
        ("tests/live", True),
        ("tests/live/test_version.py", True),
        ("tests/mock", False),
    ],
)
def test_live_suite_selected_path_args(arg: str, expected: bool) -> None:
    assert live_suite_selected("", (arg,)) is expected


# ---------------------------------------------------------------------------
# resolve_live_credentials unit tests
# ---------------------------------------------------------------------------


def test_resolve_replacement_current_non_masked_wins() -> None:
    current = {
        "PROXMOX_API_URL": "https://new.example.com:8006",
        "PROXMOX_API_TOKEN_ID": "root@pam!new",
        "PROXMOX_API_TOKEN_SECRET": "rotated-secret",
    }
    snapshot = {
        "PROXMOX_API_URL": "https://old.example.com:8006",
        "PROXMOX_API_TOKEN_ID": "root@pam!old",
        "PROXMOX_API_TOKEN_SECRET": "original-secret",
    }
    assert resolve_live_credentials(current, snapshot) == current


def test_resolve_deletion_absent_key_not_returned() -> None:
    current = {
        "PROXMOX_API_URL": "https://pve.example.com:8006",
        "PROXMOX_API_TOKEN_ID": "root@pam!test",
    }
    snapshot = {
        "PROXMOX_API_URL": "https://pve.example.com:8006",
        "PROXMOX_API_TOKEN_ID": "root@pam!test",
        "PROXMOX_API_TOKEN_SECRET": "original-secret",
    }
    assert resolve_live_credentials(current, snapshot) == current


def test_resolve_partial_only_masked_secret_recovered() -> None:
    current = {
        "PROXMOX_API_URL": "https://pve.example.com:8006",
        "PROXMOX_API_TOKEN_ID": "root@pam!test",
        "PROXMOX_API_TOKEN_SECRET": MASKED_SENTINEL,
    }
    snapshot = {
        "PROXMOX_API_URL": "https://stale.example.com:8006",
        "PROXMOX_API_TOKEN_ID": "root@pam!stale",
        "PROXMOX_API_TOKEN_SECRET": "original-secret",
    }
    assert resolve_live_credentials(current, snapshot) == {
        "PROXMOX_API_URL": "https://pve.example.com:8006",
        "PROXMOX_API_TOKEN_ID": "root@pam!test",
        "PROXMOX_API_TOKEN_SECRET": "original-secret",
    }


def test_resolve_masked_secret_recovery() -> None:
    current = {"PROXMOX_API_TOKEN_SECRET": MASKED_SENTINEL}
    snapshot = {"PROXMOX_API_TOKEN_SECRET": "original-secret"}
    assert resolve_live_credentials(current, snapshot) == {
        "PROXMOX_API_TOKEN_SECRET": "original-secret",
    }


def test_resolve_deliberate_sentinel_url_not_recovered() -> None:
    current = {"PROXMOX_API_URL": MASKED_SENTINEL}
    snapshot = {"PROXMOX_API_URL": "https://stale.example.com:8006"}
    assert resolve_live_credentials(current, snapshot) == {
        "PROXMOX_API_URL": MASKED_SENTINEL,
    }


def test_resolve_deliberate_sentinel_token_id_not_recovered() -> None:
    current = {"PROXMOX_API_TOKEN_ID": MASKED_SENTINEL}
    snapshot = {"PROXMOX_API_TOKEN_ID": "root@pam!stale"}
    assert resolve_live_credentials(current, snapshot) == {
        "PROXMOX_API_TOKEN_ID": MASKED_SENTINEL,
    }


def test_snapshot_live_credentials_preserves_secret_after_config_clear(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("PROXMOX_API_MODE", "mock")
    monkeypatch.setenv("PROXMOX_API_URL", "https://pve.example.com:8006")
    monkeypatch.setenv("PROXMOX_API_TOKEN_ID", "root@pam!test")
    monkeypatch.setenv("PROXMOX_API_TOKEN_SECRET", _ORIGINAL_SECRET)

    snapshot = snapshot_live_credentials(os.environ)

    ProxmoxConfig.from_env()

    assert os.environ["PROXMOX_API_TOKEN_SECRET"] == MASKED_SENTINEL
    assert snapshot["PROXMOX_API_TOKEN_SECRET"] == _ORIGINAL_SECRET
    assert resolve_live_credentials(os.environ, snapshot) == {
        "PROXMOX_API_URL": "https://pve.example.com:8006",
        "PROXMOX_API_TOKEN_ID": "root@pam!test",
        "PROXMOX_API_TOKEN_SECRET": _ORIGINAL_SECRET,
    }


# ---------------------------------------------------------------------------
# pytester end-to-end: real hook / stash / fixture path
# ---------------------------------------------------------------------------


def _write_pytester_project(pytester: pytest.Pytester, *, live_marker: bool) -> None:
    pytester.makeini("[pytest]\nmarkers = live: live integration tests\n")
    pytester.syspathinsert(str(_REPO_ROOT))
    pytester.makeconftest(_REPO_CONFTEST.read_text(encoding="utf-8"))
    if live_marker:
        probe_source = """
import os

import pytest
from conftest import _LIVE_CREDENTIALS_KEY, live_credentials


@pytest.mark.live
def test_live_probe(request) -> None:
    creds = live_credentials(request.config)
    stash = request.config.stash[_LIVE_CREDENTIALS_KEY]
    assert creds["PROXMOX_API_TOKEN_SECRET"] == "fake-secret"
    assert os.environ["PROXMOX_API_TOKEN_SECRET"] == "********"
    assert stash["PROXMOX_API_TOKEN_SECRET"] == "fake-secret"
"""
    else:
        probe_source = """
import os

from conftest import _LIVE_CREDENTIALS_KEY, live_credentials


def test_live_probe(request) -> None:
    creds = live_credentials(request.config)
    stash = request.config.stash[_LIVE_CREDENTIALS_KEY]
    assert creds["PROXMOX_API_TOKEN_SECRET"] == "********"
    assert os.environ["PROXMOX_API_TOKEN_SECRET"] == "********"
    assert stash == {}
"""
    pytester.makepyfile(
        test_a_import_main="""
import proxmox_sdk.main


def test_import_main() -> None:
    pass
""",
        test_z_live_probe=probe_source,
    )


def _run_pytester_subprocess(
    pytester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
    *extra_args: str,
) -> pytest.RunResult:
    monkeypatch.setenv("PROXMOX_API_MODE", "mock")
    monkeypatch.setenv("PROXMOX_API_URL", "https://pve.example.invalid:8006")
    monkeypatch.setenv("PROXMOX_API_TOKEN_ID", "root@pam!fake")
    monkeypatch.setenv("PROXMOX_API_TOKEN_SECRET", "fake-secret")
    return pytester.runpytest_subprocess("-p", "no:cacheprovider", *extra_args)


def test_live_credentials_pytester_non_live_run(
    pytester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_pytester_project(pytester, live_marker=False)
    result = _run_pytester_subprocess(pytester, monkeypatch)
    result.assert_outcomes(passed=2)


@pytest.mark.parametrize("markexpr", ["live", "(live)", "(live) and not slow"])
def test_live_credentials_pytester_e2e_serial(
    pytester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
    markexpr: str,
) -> None:
    _write_pytester_project(pytester, live_marker=True)
    result = _run_pytester_subprocess(pytester, monkeypatch, "-m", markexpr)
    result.assert_outcomes(passed=1)


def test_live_credentials_pytester_e2e_xdist(
    pytester: pytest.Pytester,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _write_pytester_project(pytester, live_marker=True)
    result = _run_pytester_subprocess(pytester, monkeypatch, "-m", "(live)", "-n", "2")
    result.assert_outcomes(passed=1)

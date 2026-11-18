"""Exercise the native event checkout with closed local Git transport fixtures."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any

import pytest
import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / ".gitea/workflows/ci.yml"
SOURCE_URL = "https://git.nmulti.cloud/emersonfelipesp/proxmox-sdk.git"
SETUP_UV_URL = "https://github.com/astral-sh/setup-uv.git"
SETUP_UV_SHA = "11f9893b081a58869d3b5fccaea48c9e9e46f990"
JOBS = ("static", "syntax", "schema-tests", "docs-package")


def _checkout(job: str = "static") -> dict[str, Any]:
    workflow = yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)
    return workflow["jobs"][job]["steps"][0]


def _git(directory: Path, *arguments: str) -> str:
    result = subprocess.run(
        ["git", *arguments],
        cwd=directory,
        capture_output=True,
        text=True,
        check=True,
        timeout=10,
    )
    return result.stdout.strip()


@pytest.fixture
def source_repository(tmp_path: Path) -> tuple[Path, str, str]:
    source = tmp_path / "source"
    source.mkdir()
    _git(source, "init", "--initial-branch=main")
    (source / ".gitignore").write_text(".tmp/\n")
    for value in ("parent", "event"):
        (source / "payload.txt").write_text(value)
        _git(source, "add", "payload.txt", ".gitignore")
        _git(
            source,
            "-c",
            "user.name=Checkout Fixture",
            "-c",
            "user.email=checkout@example.invalid",
            "commit",
            "-m",
            value,
        )
    head = _git(source, "rev-parse", "HEAD")
    parent = _git(source, "rev-parse", "HEAD^")
    _git(source, "update-ref", "refs/pull/7/head", head)
    return source, parent, head


def _run_checkout(
    workspace: Path,
    source: Path,
    sha: str,
    ref: str = "refs/heads/main",
    job: str = "static",
) -> subprocess.CompletedProcess[str]:
    workspace.mkdir(exist_ok=True)
    # Only the closed fixture redirects the fixed production URL to a local repository.
    # No workflow input, global configuration, hook, or production source is changed.
    environment = {
        **os.environ,
        "GITHUB_WORKSPACE": str(workspace),
        "SOURCE_SHA": sha,
        "SOURCE_REF": ref,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_ASKPASS": "/bin/false",
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": f"url.{source.as_uri()}.insteadOf",
        "GIT_CONFIG_VALUE_0": SOURCE_URL,
    }
    return subprocess.run(
        ["bash", "-c", _checkout(job)["run"]],
        cwd=workspace,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )


@pytest.mark.parametrize("job", JOBS)
def test_checkout_is_first_and_binds_the_event_without_remote_actions(job: str) -> None:
    step = _checkout(job)
    assert step["name"] == "Checkout exact event source"
    assert "uses" not in step
    assert step["env"] == {
        "SOURCE_SHA": "${{ github.event.pull_request.head.sha || github.sha }}",
        "SOURCE_REF": "${{ github.ref }}",
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_ASKPASS": "/bin/false",
    }
    assert f"git remote add origin {SOURCE_URL}" in step["run"]
    assert "credential.helper= -c http.extraHeader= fetch" in step["run"]


@pytest.mark.parametrize("job", JOBS)
@pytest.mark.parametrize("ref", ["refs/heads/main", "refs/pull/7/head"])
def test_checkout_retains_exact_detached_source_and_complete_ref_history(
    tmp_path: Path,
    source_repository: tuple[Path, str, str],
    job: str,
    ref: str,
) -> None:
    source, parent, head = source_repository
    workspace = tmp_path / "workspace"
    result = _run_checkout(workspace, source, head, ref, job)
    assert result.returncode == 0, result.stderr
    assert _git(workspace, "rev-parse", "HEAD") == head
    assert _git(workspace, "log", "--format=%H").splitlines() == [head, parent]
    assert _git(workspace, "rev-parse", "--is-shallow-repository") == "false"
    assert _git(workspace, "config", "--local", "--get", "remote.origin.url") == SOURCE_URL
    assert (workspace / ".git/HEAD").read_text().strip() == head


def test_moved_event_ref_fails_before_any_source_is_checked_out(
    tmp_path: Path, source_repository: tuple[Path, str, str]
) -> None:
    source, parent, _head = source_repository
    workspace = tmp_path / "workspace"
    result = _run_checkout(workspace, source, parent)
    assert result.returncode != 0
    assert not (workspace / "payload.txt").exists()


@pytest.mark.parametrize(
    "sha,ref",
    [
        ("", "refs/heads/main"),
        ("--help", "refs/heads/main"),
        ("0" * 40, "--upload-pack=unexpected"),
        ("0" * 40, "refs/heads/invalid:ref"),
    ],
)
def test_invalid_event_identity_is_refused_before_repository_initialization(
    tmp_path: Path, source_repository: tuple[Path, str, str], sha: str, ref: str
) -> None:
    source, _parent, _head = source_repository
    workspace = tmp_path / "workspace"
    result = _run_checkout(workspace, source, sha, ref)
    assert result.returncode != 0
    assert not (workspace / ".git").exists()


def test_missing_remote_ref_is_an_explicit_transport_failure_without_fallback(
    tmp_path: Path, source_repository: tuple[Path, str, str]
) -> None:
    source, _parent, head = source_repository
    workspace = tmp_path / "workspace"
    result = _run_checkout(workspace, source, head, "refs/heads/missing")
    assert result.returncode != 0
    assert "couldn't find remote ref" in result.stderr
    assert not (workspace / "payload.txt").exists()


def test_preexisting_repository_is_preserved_and_refused(
    tmp_path: Path, source_repository: tuple[Path, str, str]
) -> None:
    source, _parent, head = source_repository
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    _git(workspace, "init")
    marker = workspace / "caller-owned.txt"
    marker.write_text("preserve")
    result = _run_checkout(workspace, source, head)
    assert result.returncode != 0
    assert marker.read_text() == "preserve"
    assert not (workspace / "payload.txt").exists()


def _setup_acquisition(job: str = "static") -> dict[str, Any]:
    workflow = yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)
    return workflow["jobs"][job]["steps"][1]


def _run_setup_acquisition(
    workspace: Path, source: Path, sha: str, job: str = "static"
) -> subprocess.CompletedProcess[str]:
    environment = {
        **os.environ,
        "GITHUB_WORKSPACE": str(workspace),
        "SETUP_UV_SHA": sha,
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_ASKPASS": "/bin/false",
        "GIT_CONFIG_COUNT": "1",
        "GIT_CONFIG_KEY_0": f"url.{source.as_uri()}.insteadOf",
        "GIT_CONFIG_VALUE_0": SETUP_UV_URL,
    }
    return subprocess.run(
        ["bash", "-c", _setup_acquisition(job)["run"]],
        cwd=workspace,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
        timeout=10,
    )


@pytest.mark.parametrize("job", JOBS)
def test_local_action_preserves_the_reviewed_pin_and_every_original_input(job: str) -> None:
    workflow = yaml.load(WORKFLOW.read_text(), Loader=yaml.BaseLoader)
    acquisition, setup = workflow["jobs"][job]["steps"][1:3]
    assert acquisition["name"] == "Acquire the pinned setup-uv action privately"
    assert acquisition["env"]["SETUP_UV_SHA"] == SETUP_UV_SHA
    assert {"if", "continue-on-error"}.isdisjoint(acquisition)
    assert f"remote add origin {SETUP_UV_URL}" in acquisition["run"]
    assert setup["uses"] == "./.tmp/setup-uv"
    assert setup["with"] == {
        "version": "0.11.28",
        "enable-cache": "true",
        "python-version": "3.12.13",
        "no-project": "false",
    }


@pytest.mark.parametrize("job", JOBS)
def test_action_acquisition_is_pinned_detached_and_ignored_by_the_source_repository(
    tmp_path: Path, source_repository: tuple[Path, str, str], job: str
) -> None:
    source, _parent, head = source_repository
    workspace = tmp_path / "workspace"
    assert _run_checkout(workspace, source, head).returncode == 0
    result = _run_setup_acquisition(workspace, source, head, job)
    assert result.returncode == 0, result.stderr
    action = workspace / ".tmp/setup-uv"
    assert _git(action, "rev-parse", "HEAD") == head
    assert (action / ".git/HEAD").read_text().strip() == head
    assert _git(workspace, "status", "--porcelain") == ""
    assert _git(workspace, "check-ignore", ".tmp/setup-uv/payload.txt")


def test_unavailable_action_pin_fails_without_a_fallback(
    tmp_path: Path, source_repository: tuple[Path, str, str]
) -> None:
    source, _parent, head = source_repository
    workspace = tmp_path / "workspace"
    assert _run_checkout(workspace, source, head).returncode == 0
    result = _run_setup_acquisition(workspace, source, "0" * 40)
    assert result.returncode != 0
    assert not (workspace / ".tmp/setup-uv/payload.txt").exists()
    assert not (workspace / ".tmp/setup-uv/action.yml").exists()


def test_existing_action_directory_is_preserved_and_refused(
    tmp_path: Path, source_repository: tuple[Path, str, str]
) -> None:
    source, _parent, head = source_repository
    workspace = tmp_path / "workspace"
    assert _run_checkout(workspace, source, head).returncode == 0
    action = workspace / ".tmp/setup-uv"
    action.mkdir(parents=True)
    marker = action / "caller-owned.txt"
    marker.write_text("preserve")
    result = _run_setup_acquisition(workspace, source, head)
    assert result.returncode != 0
    assert marker.read_text() == "preserve"
    assert not (action / ".git").exists()

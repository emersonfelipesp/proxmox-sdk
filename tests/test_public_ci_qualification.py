"""Contracts for complete public quality and bounded publication suppression."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
QUALITY_JOBS = ("lint", "syntax", "package", "test", "docs")
RESULT_FIELDS = {
    "lint": "LINT_RESULT",
    "syntax": "SYNTAX_RESULT",
    "package": "PACKAGE_RESULT",
    "test": "TEST_RESULT",
    "docs": "DOCS_RESULT",
    "docker-images": "DOCKER_RESULT",
}


def _workflow(name: str) -> dict[str, Any]:
    value = yaml.load((ROOT / ".github/workflows" / name).read_text(), Loader=yaml.BaseLoader)
    assert isinstance(value, dict)
    return value


def _summary_code() -> str:
    command = _workflow("ci.yml")["jobs"]["ci-summary"]["steps"][0]["run"]
    assert command.startswith("python3 -I -S - <<'PY'\n")
    assert command.endswith("\nPY\n")
    return command.split("\n", 1)[1].rsplit("\nPY", 1)[0]


def _summary_result(
    event: str = "pull_request",
    ref: str = "refs/heads/main",
    qualification: str = "",
    docker: str = "skipped",
    changes: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    results = {name: "success" for name in QUALITY_JOBS}
    results["docker-images"] = docker
    results.update(changes or {})
    environment = {field: results[name] for name, field in RESULT_FIELDS.items()}
    environment.update(EVENT_NAME=event, EVENT_REF=ref, QUALIFICATION_ONLY=qualification)
    return subprocess.run(
        [sys.executable, "-I", "-S", "-c", _summary_code()],
        env=environment,
        capture_output=True,
        text=True,
        timeout=10,
        check=False,
    )


def test_only_the_public_browser_matrix_moves_to_a_supported_host() -> None:
    jobs = _workflow("ci.yml")["jobs"]
    assert jobs["test"]["runs-on"] == "ubuntu-24.04"
    assert jobs["test"]["strategy"]["matrix"]["proxmox_schema"] == ["latest", "9.2", "9.1.11"]
    assert jobs["test"]["strategy"]["fail-fast"] == "false"
    assert jobs["lint"]["runs-on"] == "ubuntu-latest"
    assert jobs["syntax"]["runs-on"] == "ubuntu-latest"


def test_locked_real_browser_is_required_before_the_unchanged_complete_command() -> None:
    steps = _workflow("ci.yml")["jobs"]["test"]["steps"]
    install = next(
        index
        for index, step in enumerate(steps)
        if step.get("name") == "Install locked Chromium on the ephemeral hosted runner"
    )
    regression = next(
        index
        for index, step in enumerate(steps)
        if str(step.get("name", "")).startswith("Run mocked schema-driven tests")
    )
    assert install < regression
    assert {"if", "continue-on-error"}.isdisjoint(steps[install])
    assert "uv run --locked playwright install chromium --with-deps" in steps[install]["run"]
    assert (
        "chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell"
        in steps[install]["run"]
    )
    assert (
        steps[regression]["run"]
        == "uv run --locked pytest -n 4 --cov=proxmox_sdk --cov-report=term-missing --cov-report=xml tests"
    )


def test_browser_install_exports_its_private_path_to_the_original_test_step() -> None:
    steps = _workflow("ci.yml")["jobs"]["test"]["steps"]
    install = next(
        step
        for step in steps
        if step.get("name") == "Install locked Chromium on the ephemeral hosted runner"
    )
    assert install["env"]["PLAYWRIGHT_BROWSERS_PATH"] == "${{ runner.temp }}/proxmox-playwright"
    assert '"$PLAYWRIGHT_BROWSERS_PATH" >> "$GITHUB_ENV"' in install["run"]


def test_read_only_docs_reuses_original_quality_commands_without_the_writer() -> None:
    workflow = _workflow("ci.yml")
    quality = workflow["jobs"]["docs"]
    legacy = _workflow("docs.yml")["jobs"]["deploy"]
    commands = [step["run"] for step in quality["steps"] if "run" in step]
    original = [step["run"] for step in legacy["steps"] if "run" in step]
    assert commands == original[:3]
    assert original[-1] == "uv run --locked mkdocs gh-deploy --force --clean --verbose"


def test_docs_quality_has_only_read_permission_and_no_publication_step() -> None:
    workflow = _workflow("ci.yml")
    quality = workflow["jobs"]["docs"]
    assert workflow["permissions"] == {"contents": "read"}
    assert "permissions" not in quality
    assert "gh-deploy" not in str(quality)
    assert "secrets." not in str(quality)


def test_only_the_existing_writer_entry_points_have_the_optional_guard() -> None:
    docker = _workflow("ci.yml")["jobs"]["docker-images"]
    legacy = _workflow("docs.yml")["jobs"]["deploy"]
    assert docker["if"] == (
        "github.event_name == 'push' && (github.ref == 'refs/heads/main' || github.ref == 'refs/heads/testing')"
        " && vars.CI_QUALIFICATION_ONLY != 'true'"
    )
    assert legacy["if"] == "vars.CI_QUALIFICATION_ONLY != 'true'"
    assert docker["needs"] == ["lint", "syntax", "package", "test"]
    assert docker["with"] == {"source_ref": "${{ github.sha }}", "mode": "publish"}
    assert set(docker["secrets"]) == {"DOCKERHUB_USERNAME", "DOCKERHUB_TOKEN"}
    assert docker["uses"] == "./.github/workflows/docker-hub-publish.yml"


def test_complete_summary_always_observes_all_quality_and_publication_jobs() -> None:
    summary = _workflow("ci.yml")["jobs"]["ci-summary"]
    assert summary["if"] == "${{ always() }}"
    assert set(summary["needs"]) == {*QUALITY_JOBS, "docker-images"}
    assert "secrets." not in str(summary)
    assert "environment" not in summary


@pytest.mark.parametrize(
    "event,ref,qualification,docker",
    [
        ("push", "refs/heads/main", "", "success"),
        ("push", "refs/heads/testing", "false", "success"),
        ("push", "refs/heads/main", "true", "skipped"),
        ("push", "refs/heads/testing", "true", "skipped"),
        ("push", "refs/heads/main", "TRUE", "skipped"),
        ("pull_request", "refs/pull/1/merge", "", "skipped"),
        ("workflow_dispatch", "refs/heads/main", "", "skipped"),
        ("push", "refs/heads/feature", "", "skipped"),
    ],
)
def test_summary_accepts_only_the_intended_event_and_writer_disposition(
    event: str,
    ref: str,
    qualification: str,
    docker: str,
) -> None:
    result = _summary_result(event, ref, qualification, docker)
    assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("job", QUALITY_JOBS)
@pytest.mark.parametrize("state", ["failure", "cancelled", "skipped", ""])
def test_summary_refuses_any_incomplete_quality_job(job: str, state: str) -> None:
    result = _summary_result(changes={job: state})
    assert result.returncode != 0
    assert job in result.stderr


@pytest.mark.parametrize(
    "event,qualification,docker",
    [
        ("push", "", "skipped"),
        ("push", "false", "failure"),
        ("push", "true", "success"),
        ("pull_request", "", "success"),
        ("workflow_dispatch", "", "success"),
        ("push", "true", "cancelled"),
    ],
)
def test_summary_refuses_missing_or_unexpected_publication(
    event: str,
    qualification: str,
    docker: str,
) -> None:
    result = _summary_result(event=event, qualification=qualification, docker=docker)
    assert result.returncode != 0
    assert "publication disposition" in result.stderr

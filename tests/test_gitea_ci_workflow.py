"""Contracts for the secret-free Gitea pull-request quality gate."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_PATH = ROOT / ".gitea" / "workflows" / "ci.yml"
FULL_SHA_ACTION = re.compile(r"^[^\s@]+@[0-9a-f]{40}$")
GITEA_UPLOAD_ARTIFACT = "actions/upload-artifact@a8a3f3ad30e3422c9c7b888a15615d19a852ae32"
GITEA_SETUP_UV = "./.tmp/setup-uv"


def _workflow() -> dict[str, Any]:
    value = yaml.load(WORKFLOW_PATH.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    assert isinstance(value, dict)
    return value


def _commands(job: dict[str, Any]) -> str:
    return "\n".join(str(step["run"]) for step in job.get("steps", []) if "run" in step)


def test_gitea_ci_has_bounded_read_only_review_triggers() -> None:
    workflow = _workflow()

    assert workflow["name"] == "Gitea CI"
    assert workflow["permissions"] == {"contents": "read"}
    assert workflow["on"]["push"]["branches"] == ["main", "testing"]
    assert workflow["on"]["pull_request"]["branches"] == ["main", "testing"]
    assert workflow["on"]["pull_request"]["types"] == [
        "opened",
        "synchronize",
        "reopened",
    ]
    assert "workflow_dispatch" in workflow["on"]
    assert workflow["concurrency"] == {
        "group": "gitea-ci-${{ github.ref }}",
        "cancel-in-progress": "${{ github.event_name == 'pull_request' }}",
    }


def test_every_job_uses_the_untrusted_runner_and_explicit_timeout() -> None:
    jobs = _workflow()["jobs"]

    assert set(jobs) == {"static", "syntax", "schema-tests", "docs-package"}
    for job in jobs.values():
        assert job["runs-on"] == "ci-untrusted-python312"
        assert int(job["timeout-minutes"]) > 0
        assert "environment" not in job
        assert "permissions" not in job


def test_third_party_actions_are_pinned_to_reviewed_commits() -> None:
    for job_name, job in _workflow()["jobs"].items():
        for step in job["steps"]:
            action = step.get("uses")
            if action is not None and action != GITEA_SETUP_UV:
                assert FULL_SHA_ACTION.fullmatch(action), f"{job_name}: {action}"


def test_setup_uv_uses_gitea_compatible_boolean_inputs() -> None:
    setup_steps = [
        step
        for job in _workflow()["jobs"].values()
        for step in job["steps"]
        if step.get("name") == "Set up locked Python tooling"
    ]

    assert len(setup_steps) == 4
    for step in setup_steps:
        assert step["uses"] == GITEA_SETUP_UV
        assert step["with"]["no-project"] == "false"


def test_static_and_syntax_jobs_preserve_github_ci_policy() -> None:
    jobs = _workflow()["jobs"]
    static = _commands(jobs["static"])
    syntax = _commands(jobs["syntax"])

    for command in (
        "uv lock --check",
        "uv sync --locked --group dev",
        "ruff check .",
        "ruff format --check .",
        "ty check proxmox_sdk tests",
        "pyright proxmox_sdk",
        ".github/workflows/*.yml",
        ".gitea/workflows/*.yml",
        "sha256sum --check --strict",
    ):
        assert command in static

    for command in (
        "uv lock --check",
        "uv sync --locked --extra test --group dev",
        "python -m compileall proxmox_sdk tests",
        "import proxmox_sdk.main",
        "import proxmox_sdk.mock_main",
        "import proxmox_sdk.pdm_mock_main",
        "from proxmox_sdk.sdk import ProxmoxSDK",
        "from proxmox_sdk.sdk.sync import SyncProxmoxSDK",
        "from proxmox_sdk.proxmox_cli.cli import cli",
    ):
        assert command in syntax


def test_schema_matrix_runs_the_complete_covered_suite() -> None:
    job = _workflow()["jobs"]["schema-tests"]
    commands = _commands(job)
    artifact_steps = [
        step for step in job["steps"] if step.get("name") == "Retain schema coverage evidence"
    ]

    assert job["strategy"]["fail-fast"] == "false"
    assert job["strategy"]["matrix"]["proxmox_schema"] == [
        "latest",
        "9.2",
        "9.1.11",
    ]
    assert job["env"]["PROXMOX_MOCK_SCHEMA_VERSION"] == ("${{ matrix.proxmox_schema }}")
    assert (
        "${{ github.run_id }}_${{ github.run_attempt }}"
        in job["env"]["PROXMOX_MOCK_STATE_NAMESPACE"]
    )
    assert "uv sync --locked --extra test --group dev" in commands
    assert "pytest -n 4" in commands
    assert "--cov=proxmox_sdk" in commands
    assert "--cov-branch" in commands
    assert "--cov-report=xml tests" in commands
    assert len(artifact_steps) == 1
    assert artifact_steps[0]["uses"] == GITEA_UPLOAD_ARTIFACT


def test_docs_and_package_job_validates_the_installed_artifact() -> None:
    commands = _commands(_workflow()["jobs"]["docs-package"])

    for command in (
        "uv lock --check",
        "uv sync --locked --extra docs --group dev",
        "mkdocs build --strict",
        "python -m build --no-isolation",
        "python -m twine check dist/*",
        "tests/verify_wheel_contract.py dist/*.whl",
    ):
        assert command in commands


def _browser_steps() -> tuple[list[dict[str, Any]], int, int]:
    steps = _workflow()["jobs"]["schema-tests"]["steps"]
    preparation = next(
        index
        for index, step in enumerate(steps)
        if step.get("name") == "Prepare job-private Chromium and authenticated Debian libraries"
    )
    regression = next(
        index
        for index, step in enumerate(steps)
        if step.get("name") == "Run complete schema-driven regression suite"
    )
    return steps, preparation, regression


def test_schema_browser_preparation_is_mandatory_before_unchanged_regression() -> None:
    steps, preparation, regression = _browser_steps()
    assert preparation < regression
    assert "if" not in steps[preparation]
    assert "continue-on-error" not in steps[preparation]
    assert steps[regression]["run"] == (
        "uv run --locked pytest -n 4 --cov=proxmox_sdk --cov-branch "
        "--cov-report=term-missing --cov-report=xml tests"
    )
    artifact = next(step for step in steps if step.get("name") == "Retain schema coverage evidence")
    assert artifact["with"]["path"].splitlines() == [
        "coverage.xml",
        "${{ env.PROXMOX_CHROMIUM_RUNTIME }}/archive-inventory.json",
    ]


def test_schema_browser_preparation_uses_private_paths_and_exact_browser() -> None:
    steps, preparation, _regression = _browser_steps()
    command = steps[preparation]["run"]
    assert 'mktemp -d "${RUNNER_TEMP:?}/proxmox-chromium.XXXXXX"' in command
    assert 'tools/prepare_ci_chromium.py "$runtime/runtime"' in command
    assert "playwright install chromium\n" in command
    assert (
        "chromium_headless_shell-1208/chrome-headless-shell-linux64/chrome-headless-shell"
        in command
    )
    assert '>> "$GITHUB_ENV"' in command
    assert "--with-deps" not in command
    assert "sudo" not in command
    assert "--no-sandbox" not in command


def test_private_fontconfig_state_is_confined_to_the_original_regression_step() -> None:
    steps, preparation, regression = _browser_steps()
    assert steps[regression]["env"] == {
        "FONTCONFIG_FILE": "${{ env.PROXMOX_CHROMIUM_RUNTIME }}/fontconfig/fonts.conf",
        "FONTCONFIG_PATH": "${{ env.PROXMOX_CHROMIUM_RUNTIME }}/fontconfig",
    }
    assert "FONTCONFIG_" not in steps[preparation]["run"]
    assert "FONTCONFIG_FILE" not in _workflow()["jobs"]["schema-tests"]["env"]


def test_pull_request_workflow_contains_no_publish_or_deploy_authority() -> None:
    text = WORKFLOW_PATH.read_text(encoding="utf-8").lower()

    for forbidden in (
        "secrets.",
        "gitea_package_token",
        "pypi_token",
        "dockerhub_token",
        "twine upload",
        "docker push",
        "git push",
        "gh release",
        "environment:",
    ):
        assert forbidden not in text

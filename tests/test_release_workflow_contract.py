"""Semantic contracts for release workflows and the container supply chain."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
GITHUB_WORKFLOWS = ROOT / ".github" / "workflows"
GITEA_WORKFLOWS = ROOT / ".gitea" / "workflows"
FULL_SHA_ACTION = re.compile(r"^[^\s@]+@[0-9a-f]{40}$")


def _workflow(path: Path) -> dict[str, Any]:
    value = yaml.load(path.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)
    assert isinstance(value, dict)
    return value


def _github(name: str) -> dict[str, Any]:
    return _workflow(GITHUB_WORKFLOWS / name)


def _gitea(name: str) -> dict[str, Any]:
    return _workflow(GITEA_WORKFLOWS / name)


def _uses(job: dict[str, Any]) -> list[str]:
    return [step["uses"] for step in job.get("steps", []) if "uses" in step]


def test_release_triggers_and_manual_modes_are_fail_closed() -> None:
    release = _github("publish-testpypi.yml")
    assert release["on"]["push"]["tags"] == ["v*rc*"]
    assert release["on"]["release"]["types"] == ["published"]
    assert release["concurrency"]["cancel-in-progress"] == "false"

    docker = _github("docker-hub-publish.yml")
    assert set(docker["on"]["workflow_dispatch"]["inputs"]) == {"source_ref"}
    context_text = str(docker["jobs"]["resolve-publish-source"]["steps"])
    assert "Manual Docker runs cannot publish" in context_text
    assert "full lowercase commit SHA" in context_text
    assert "Reusable publishers must build the exact triggering event SHA" in context_text


def test_credentialed_jobs_are_protected_and_artifact_only() -> None:
    jobs: list[tuple[dict[str, Any], str, str]] = [
        (_github("publish-testpypi.yml"), "publish-testpypi", "testpypi"),
        (_github("publish-testpypi.yml"), "publish-pypi", "pypi"),
        (
            _github("publish-testpypi.yml"),
            "stage-service-images",
            "dockerhub-candidate",
        ),
        (
            _github("publish-testpypi.yml"),
            "promote-all-docker-images",
            "dockerhub-release",
        ),
        (_github("docker-hub-publish.yml"), "stage-images", "dockerhub-candidate"),
        (
            _github("docker-hub-publish.yml"),
            "promote-development",
            "dockerhub-development",
        ),
    ]
    for workflow, job_name, environment in jobs:
        job = workflow["jobs"][job_name]
        assert job["environment"] == environment
        assert not any(action.startswith("actions/checkout@") for action in _uses(job))

    release_text = (GITHUB_WORKFLOWS / "publish-testpypi.yml").read_text(encoding="utf-8")
    assert "TEST_PYPI_USERNAME" not in release_text
    assert "PYPI_USERNAME" not in release_text
    assert "pypa/gh-action-pypi-publish@ed0c53931b1dc9bd32cbe73a98c7f6766f8a527e" in (release_text)
    assert "secrets: inherit" not in release_text
    assert "secrets: inherit" not in (GITHUB_WORKFLOWS / "ci.yml").read_text(encoding="utf-8")

    mirror = _gitea("mirror-github.yml")
    mirror_job = mirror["jobs"]["mirror"]
    assert "env" not in mirror_job
    install_step, mirror_step = mirror_job["steps"]
    assert "env" not in install_step
    assert "GH_MIRROR_TOKEN" in str(mirror_step["env"])


def test_distribution_build_is_reproducible_and_serialized() -> None:
    release_text = (GITHUB_WORKFLOWS / "publish-testpypi.yml").read_text(encoding="utf-8")
    gitea_text = (GITEA_WORKFLOWS / "publish-package.yml").read_text(encoding="utf-8")
    for text in (release_text, gitea_text):
        assert "SOURCE_DATE_EPOCH" in text
        assert "build_reproducible_distributions.py" in text
        assert "distribution-manifest.json" in text
    assert "cancel-in-progress: false" in release_text


def test_public_promotion_waits_for_served_pypi_bytes_and_all_candidates() -> None:
    release = _github("publish-testpypi.yml")
    jobs = release["jobs"]
    assert jobs["publish-docker"]["needs"] == ["prepare-release", "verify-pypi-artifacts"]
    assert jobs["publish-docker"]["with"]["mode"] == "stage"
    assert jobs["build-service-images"]["needs"] == [
        "prepare-release",
        "verify-pypi-artifacts",
    ]
    promotion_needs = set(jobs["promote-all-docker-images"]["needs"])
    assert promotion_needs == {
        "prepare-release",
        "verify-pypi-artifacts",
        "publish-docker",
        "stage-service-images",
        "smoke-service-candidates",
    }
    assert "docker buildx imagetools create" in str(jobs["promote-all-docker-images"]["steps"])
    assert "Validate candidate provenance fan-in" in str(jobs["promote-all-docker-images"]["steps"])
    assert jobs["promote-all-docker-images"]["concurrency"] == {
        "group": "proxmox-sdk-stable-docker-promotion",
        "cancel-in-progress": "false",
    }
    assert "releases/latest" in str(jobs["promote-all-docker-images"]["steps"])

    docker = _github("docker-hub-publish.yml")
    assert docker["on"]["workflow_call"]["outputs"]["raw_digest"]
    assert "candidate-" in str(docker["jobs"]["stage-images"]["steps"])
    assert docker["jobs"]["promote-development"]["needs"] == [
        "resolve-publish-source",
        "stage-images",
        "smoke-candidates",
    ]


def test_repository_publication_hashes_served_bytes_and_binds_project_wheel() -> None:
    release_text = (GITHUB_WORKFLOWS / "publish-testpypi.yml").read_text(encoding="utf-8")
    assert "--skip-existing" not in release_text
    assert '--download-dir "$RUNNER_TEMP/proxmox-sdk-pypi"' in release_text
    assert "pypi-wheel-${{ needs.prepare-release.outputs.version }}" in release_text
    assert "PROXMOX_SDK_WHEEL_SHA256=" in release_text
    assert "PROXMOX_SDK_WHEEL=" in release_text
    assert "Wait for PyPI package" not in release_text
    assert "pip install --dry-run" not in release_text

    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    assert "COPY dist/ /tmp/proxmox-sdk-dist/" in dockerfile
    assert "printf '%s  %s\\n' \"${PROXMOX_SDK_WHEEL_SHA256}\"" in dockerfile
    assert '"/tmp/proxmox-sdk-dist/${PROXMOX_SDK_WHEEL}"' in dockerfile
    assert "sha256sum -c -" in dockerfile
    assert "sha256sum --check" not in dockerfile
    assert '"proxmox-sdk==${PROXMOX_SDK_VERSION}"' not in dockerfile


def test_gitea_package_of_record_and_rc_gates_are_repository_visible() -> None:
    gitea = _gitea("publish-package.yml")
    assert gitea["on"]["push"]["tags"] == ["v*"]
    assert set(gitea["jobs"]) == {"prepare-package"}
    prepare = gitea["jobs"]["prepare-package"]
    assert prepare["runs-on"] == "ci-untrusted-python312"
    assert gitea["permissions"] == {"contents": "read", "packages": "none"}
    gitea_text = (GITEA_WORKFLOWS / "publish-package.yml").read_text(encoding="utf-8")
    secret_names = set(re.findall(r"secrets\.([A-Z0-9_]+)", gitea_text))
    assert secret_names == set()
    for forbidden in (
        "release-publisher",
        "TWINE_USERNAME",
        "TWINE_PASSWORD",
        "GITEA_PACKAGE_TOKEN",
        "packages: write",
        "pypa/gh-action-pypi-publish",
        "twine upload",
    ):
        assert forbidden not in gitea_text
    assert "Prerelease publication is restricted to rc versions" in gitea_text
    assert "local or development segments" in gitea_text
    assert "github.server_url" in gitea_text
    assert "https://git.nmulti.cloud" in gitea_text
    assert "actions/setup-python@" not in gitea_text
    assert 'python-version: "3.13.14"' in gitea_text
    assert "uv run --locked python - <<'PY'" in gitea_text
    assert "jq --arg" not in gitea_text
    assert "actions/upload-artifact@c6a3b2bd78b3985e4b2f15397fec357f0fd808de" in gitea_text
    meta = next(
        step for step in prepare["steps"] if step.get("name") == "Validate tag and package metadata"
    )
    assert meta["env"]["RELEASE_RUN_ID"] == "${{ github.run_id }}"
    assert meta["env"]["RELEASE_RUN_ATTEMPT"] == "${{ github.run_attempt }}"
    assert 're.fullmatch(r"[1-9][0-9]*", run_id)' in meta["run"]
    assert 're.fullmatch(r"[1-9][0-9]*", run_attempt)' in meta["run"]
    upload = next(
        step for step in prepare["steps"] if step.get("name") == "Upload attested package candidate"
    )
    assert upload["with"]["name"] == "${{ steps.meta.outputs.artifact_name }}"
    assert upload["with"]["path"] == "release-artifacts/proxmox-sdk-gitea-candidate.tar"
    assert "PROXMOX_SDK_CANDIDATE_SHA256=" in gitea_text
    assert 'workflow_path=".gitea/workflows/publish-package.yml"' in gitea_text
    assert "workflow_sha256=sha256" in gitea_text
    assert 'provenance_path = pathlib.Path("release-artifacts/gitea-provenance.json")' in gitea_text
    assert "distribution_manifest_sha256=distribution_manifest_sha256" in gitea_text
    assert "manifest.update(\n              source_sha=" in gitea_text

    verifier_unit = (ROOT / "tools" / "proxmox-sdk-gitea-verify@.service").read_text(
        encoding="utf-8"
    )
    publisher_unit = (ROOT / "tools" / "proxmox-sdk-gitea-publisher@.service").read_text(
        encoding="utf-8"
    )
    assert "registry.json" not in verifier_unit
    assert "gitea-read.json" not in publisher_unit
    assert "policy.json" not in publisher_unit
    assert "gitea_package_publisher.py verify" in verifier_unit
    assert "gitea_package_publisher.py seal" in verifier_unit
    assert "gitea_package_publisher.py publish" in publisher_unit
    assert "/opt/proxmox-sdk-publisher/bin/nms" in (
        ROOT / "tools" / "gitea_package_publisher.py"
    ).read_text(encoding="utf-8")
    for unit in (verifier_unit, publisher_unit):
        assert "uv " not in unit
        assert "pip " not in unit
        assert "twine" not in unit.lower()

    release_text = (GITHUB_WORKFLOWS / "publish-testpypi.yml").read_text(encoding="utf-8")
    assert 'tags: ["v*rc*"]' in release_text
    assert "The tag trigger is restricted to PEP 440 rc versions" in release_text
    assert "needs.prepare-release.outputs.is_final == 'true'" in release_text


def test_no_gitea_workflow_or_runner_receives_package_credentials() -> None:
    forbidden = (
        "release-publisher",
        "TWINE_PASSWORD",
        "TWINE_USERNAME",
        "GITEA_PACKAGE_TOKEN",
        "GITEA_PACKAGE_USERNAME",
        ".pypirc",
        "packages: write",
    )
    for path in GITEA_WORKFLOWS.glob("*.yml"):
        text = path.read_text(encoding="utf-8")
        for value in forbidden:
            assert value not in text, f"{value!r} must not appear in {path.name}"


def test_current_python_base_and_direct_apk_inputs_are_pinned() -> None:
    dockerfile = (ROOT / "Dockerfile").read_text(encoding="utf-8")
    reviewed = (
        "python:3.13.14-alpine3.24@"
        "sha256:399babc8b49529dabfd9c922f2b5eea81d611e4512e3ed250d75bd2e7683f4b0"
    )
    assert dockerfile.count(reviewed) == 3
    for package in (
        "build-base=0.5-r4",
        "curl=8.21.0-r0",
        "nginx=1.30.4-r1",
        "supervisor=4.3.0-r1",
        "ca-certificates=20260611-r0",
        "nss-tools=3.124-r0",
        "openssl=3.5.7-r0",
    ):
        assert package in dockerfile
    all_workflow_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [*GITHUB_WORKFLOWS.glob("*.yml"), *GITEA_WORKFLOWS.glob("*.yml")]
    )
    assert "3.13.3" not in all_workflow_text
    assert 'python-version: "3.13.14"' in all_workflow_text


def test_container_helper_images_and_artifacts_are_identity_bound() -> None:
    paths = (
        GITHUB_WORKFLOWS / "docker-hub-publish.yml",
        GITHUB_WORKFLOWS / "publish-testpypi.yml",
        GITHUB_WORKFLOWS / "release-docker-verify.yml",
    )
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    assert (
        "docker.io/tonistiigi/binfmt@"
        "sha256:400a4873b838d1b89194d982c45e5fb3cda4593fbfd7e08a02e76b03b21166f0"
    ) in text
    assert (
        "docker.io/moby/buildkit:buildx-stable-1@"
        "sha256:2f5adac4ecd194d9f8c10b7b5d7bceb5186853db1b26e5abd3a657af0b7e26ec"
    ) in text
    assert "tonistiigi/binfmt:latest" not in text
    assert "image_id" in text
    assert "archive_sha256" in text
    assert "sbom_sha256" in text
    assert "registry_manifest_digest" in text
    assert "io.nmulti.proxmox-sdk.wheel.sha256" in text
    assert "overwrite: true" in text
    assert (
        "dist-${{ steps.meta.outputs.source_sha }}-${{ github.run_id }}-${{ github.run_attempt }}"
    ) in text
    assert "CANDIDATE_RUN_TOKEN: ${{ github.run_id }}-${{ github.run_attempt }}" in text
    assert 'test "$arch_digest" = "$pushed_digest"' in text
    assert ".run_id == $run_id and .run_attempt == $run_attempt" in text


def test_both_architectures_and_all_services_receive_runtime_smoke_tests() -> None:
    docker = _github("docker-hub-publish.yml")
    assert docker["jobs"]["build-image"]["strategy"]["matrix"]["arch"] == [
        "amd64",
        "arm64",
    ]
    assert docker["jobs"]["smoke-candidates"]["strategy"]["matrix"]["variant"] == [
        "raw",
        "nginx",
        "granian",
    ]
    assert "generate_container_sbom.py" in str(docker["jobs"]["build-image"]["steps"])

    release = _github("publish-testpypi.yml")
    service_matrix = release["jobs"]["build-service-images"]["strategy"]["matrix"]
    assert service_matrix["service"] == ["all", "pve", "pbs", "pdm"]
    assert service_matrix["arch"] == ["amd64", "arm64"]

    post = _github("release-docker-verify.yml")
    post_matrix = post["jobs"]["verify-image"]["strategy"]["matrix"]
    assert post_matrix["identity"] == ["raw", "nginx", "granian", "all", "pve", "pbs", "pdm"]
    assert post_matrix["arch"] == ["amd64", "arm64"]


def test_network_calls_and_tests_have_explicit_bounds() -> None:
    verifier = (ROOT / "tests" / "verify_repository_artifacts.py").read_text(encoding="utf-8")
    assert "--request-timeout" in verifier
    assert "--download-timeout" in verifier
    assert "--max-artifact-bytes" in verifier
    assert "total download deadline" in verifier

    post_text = (GITHUB_WORKFLOWS / "release-docker-verify.yml").read_text(encoding="utf-8")
    assert "timeout 30s gh api" in post_text
    assert "timeout 120s docker pull" in post_text

    missing: list[str] = []
    paths = [*GITHUB_WORKFLOWS.glob("*.yml"), GITEA_WORKFLOWS / "ci.yml"]
    for path in sorted(paths):
        workflow = _workflow(path)
        for job_name, job in workflow["jobs"].items():
            if "runs-on" in job and "timeout-minutes" not in job:
                missing.append(f"{path.name}:{job_name}")
    assert missing == []


def test_release_evidence_is_a_hard_publication_gate() -> None:
    release = _github("publish-testpypi.yml")
    prepare_steps = str(release["jobs"]["prepare-release"]["steps"])
    assert "verify_release_evidence.py" in prepare_steps
    assert "Validate final public release and package-record evidence" in prepare_steps
    assert "--distribution-manifest" in prepare_steps
    template = (ROOT / ".github" / "RELEASE_EVIDENCE_TEMPLATE.md").read_text(encoding="utf-8")
    assert "Package-of-record manifest SHA256: `<sha256>`" in template
    for item in ("REQ", "ARCH", "IMPL", "STATIC", "TEST", "COVERAGE", "DEFECTS", "OPS"):
        assert f"**{item}**" in template


def test_third_party_actions_are_pinned_to_full_commit_shas() -> None:
    unpinned: list[str] = []
    paths = [
        *GITHUB_WORKFLOWS.glob("*.yml"),
        GITEA_WORKFLOWS / "ci.yml",
        GITEA_WORKFLOWS / "publish-package.yml",
    ]
    for path in sorted(paths):
        workflow = _workflow(path)
        for job_name, job in workflow["jobs"].items():
            for action in _uses(job):
                if not action.startswith("./") and not FULL_SHA_ACTION.fullmatch(action):
                    unpinned.append(f"{path.name}:{job_name}:{action}")
    assert unpinned == []


def test_ci_lints_github_and_gitea_workflows() -> None:
    ci_text = (GITHUB_WORKFLOWS / "ci.yml").read_text(encoding="utf-8")
    assert ".github/workflows/*.yml" in ci_text
    assert ".gitea/workflows/*.yml" in ci_text


def test_permissions_are_read_only_and_tag_terminology_is_truthful() -> None:
    for name in (
        "ci.yml",
        "docker-hub-publish.yml",
        "publish-testpypi.yml",
        "release-docker-verify.yml",
    ):
        assert _github(name)["permissions"] == {"contents": "read"}
    assert _gitea("ci.yml")["permissions"] == {"contents": "read"}
    assert _gitea("publish-package.yml")["permissions"] == {
        "contents": "read",
        "packages": "none",
    }
    assert _gitea("mirror-github.yml")["permissions"] == {"contents": "read"}

    schema = _github("schema-update.yml")
    assert schema["permissions"] == {"contents": "read"}
    assert schema["jobs"]["open-pr"]["permissions"] == {
        "contents": "write",
        "pull-requests": "write",
    }

    checked_paths = [
        ROOT / "README.md",
        ROOT / "docs" / "development.md",
        ROOT / "CLAUDE.md",
        ROOT / "AGENTS.md",
        ROOT / ".github" / "CLAUDE.md",
        ROOT / ".github" / "AGENTS.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in checked_paths)
    assert "immutable SHA tag" not in text
    assert "commit traceability tag" in text

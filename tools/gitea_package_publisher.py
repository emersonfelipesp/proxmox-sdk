"""Verify, seal, and publish a proxmox-sdk Gitea package candidate.

The host mode obtains read-only Gitea evidence through an immutable ``nms git``
installation.  The Actions mode validates an anonymously fetched exact tag.
Both modes independently rebuild twice and seal a byte-for-byte match before a
separate process receives package credentials.  The Actions publisher lane also
rebuilds and compares the exact source before its credentialed step.  The
Actions token is read only from an environment variable by the final
publication command and is never printed or passed as a command argument.
"""

from __future__ import annotations

import argparse
import base64
import binascii
import copy
import fnmatch
import gzip
import hashlib
import html.parser
import http.client
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import tomllib
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from datetime import UTC, datetime
from email.message import Message
from email.parser import BytesParser
from pathlib import Path, PurePosixPath
from typing import Any, Protocol

EXPECTED_SERVER = "https://git.nmulti.cloud"
EXPECTED_OWNER = "emersonfelipesp"
EXPECTED_REPOSITORY = "proxmox-sdk"
EXPECTED_FULL_NAME = f"{EXPECTED_OWNER}/{EXPECTED_REPOSITORY}"
EXPECTED_PACKAGE = "proxmox-sdk"
EXPECTED_WORKFLOW_NAME = "Build Gitea package candidate"
EXPECTED_WORKFLOW_PATH = ".gitea/workflows/publish-package.yml"
EXPECTED_WORKFLOW_ID = "publish-package.yml"
EXPECTED_JOB_NAME = "build and attest package candidate"
EXPECTED_RUNNER_LABEL = "ci-untrusted-python312"
EXPECTED_TAG_PROTECTION = "v*"
NMS_EXECUTABLE = Path("/opt/proxmox-sdk-publisher/bin/nms")
BUILD_PYTHON = Path("/opt/proxmox-sdk-publisher/bin/python")
EXPECTED_BUILD_TOOLS = {
    "build": "1.5.0",
    "packaging": "26.0",
    "pyproject-hooks": "1.2.0",
    "setuptools": "83.0.0",
    "wheel": "0.47.0",
}
EXPECTED_PYTHON_VERSION = "3.13.14"
PAYLOAD_NAME = "proxmox-sdk-gitea-candidate.tar"
SEAL_MANIFEST_NAME = "seal-manifest.json"
MAX_CONTROL_BYTES = 4 * 1024 * 1024
MAX_HANDOFF_BYTES = 64 * 1024
MAX_DISTRIBUTION_BYTES = 512 * 1024 * 1024
MAX_PAYLOAD_BYTES = 1024 * 1024 * 1024
MAX_TOKEN_BYTES = 4096
HEX40 = re.compile(r"[0-9a-f]{40}")
HEX64 = re.compile(r"[0-9a-f]{64}")
SAFE_VERSION = re.compile(
    r"(?P<release>[0-9]+(?:\.[0-9]+)*)"
    r"(?:(?:[-_.]?)(?P<pre>a|b|rc)(?P<pre_n>[0-9]+))?"
    r"(?:(?:[-_.]?post)(?P<post_n>[0-9]+))?",
    re.IGNORECASE,
)
DIST_SUFFIXES = (".whl", ".tar.gz")
INSTALLABLE_SUFFIXES = (
    ".zip",
    ".whl",
    ".tar.gz",
    ".tgz",
    ".tar",
    ".tar.bz2",
    ".tbz",
    ".tar.xz",
    ".txz",
    ".tlz",
    ".tar.lz",
    ".tar.lzma",
)


class PublisherError(RuntimeError):
    """A fail-closed publisher policy or integrity failure."""


class GiteaReader(Protocol):
    """Read-only evidence source used before package credentials are opened."""

    def get_json(self, path: str) -> Any: ...

    def get_bytes(self, path: str) -> bytes: ...


class PackageRegistry(Protocol):
    """Credentialed package registry operations."""

    def inspect(self, package: str, version: str) -> dict[str, str]: ...

    def upload(self, artifact: Path, metadata: Mapping[str, str]) -> None: ...


class SourceRebuilder(Protocol):
    """Trusted host build boundary for byte-comparing the tagged source."""

    def rebuild(
        self,
        client: GiteaReader,
        *,
        source_sha: str,
        source_date_epoch: int,
        work: Path,
    ) -> Mapping[str, Path]: ...


@dataclass(frozen=True)
class RegistryCredential:
    username: str
    token: str


@dataclass(frozen=True)
class PublisherPolicy:
    """Root-owned non-secret release policy installed before tag creation."""

    tag_protection_id: int
    whitelist_usernames: tuple[str, ...]
    whitelist_teams: tuple[str, ...]


@dataclass(frozen=True)
class VerifiedCandidate:
    artifact_name: str
    candidate_sha256: str
    distributions: Mapping[str, Path]
    metadata: Mapping[str, Mapping[str, str]]
    run_attempt: int
    run_id: int
    source_sha: str
    tag: str
    version: str
    distribution_manifest_sha256: str
    gitea_provenance_sha256: str
    distribution_manifest: Path
    gitea_provenance: Path


@dataclass(frozen=True)
class RegistryArtifact:
    """An exact registry artifact identity."""

    name: str
    size: int
    sha256: str


@dataclass(frozen=True)
class RegistryState:
    """The bounded package-version state returned by Gitea."""

    version_exists: bool
    repository: str | None
    artifacts: tuple[RegistryArtifact, ...]

    def artifact_map(self) -> dict[str, RegistryArtifact]:
        return {artifact.name: artifact for artifact in self.artifacts}


def _object(value: Any, description: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise PublisherError(f"{description} is not a JSON object")
    return value


def _list(value: Any, description: str) -> list[Any]:
    if not isinstance(value, list):
        raise PublisherError(f"{description} is not a JSON list")
    return value


def _require_equal(actual: Any, expected: Any, description: str) -> None:
    if actual != expected:
        raise PublisherError(f"Unexpected {description}")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_package_token(token: str) -> str:
    if not isinstance(token, str) or not token or len(token) > MAX_TOKEN_BYTES:
        raise PublisherError("PACKAGE_WRITE_TOKEN has an invalid length")
    if any(not 0x21 <= ord(character) <= 0x7E for character in token):
        raise PublisherError("PACKAGE_WRITE_TOKEN must contain printable ASCII without spaces")
    return token


def _canonical_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower()


def _canonical_version(value: str) -> str | None:
    match = SAFE_VERSION.fullmatch(value)
    if match is None:
        return None
    result = match.group("release")
    if match.group("pre"):
        result += f"{match.group('pre').lower()}{int(match.group('pre_n'))}"
    if match.group("post_n"):
        result += f".post{int(match.group('post_n'))}"
    return result


def _belongs_to_release(filename: str, package: str, version: str) -> bool:
    lowered = filename.lower()
    suffix = next((item for item in INSTALLABLE_SUFFIXES if lowered.endswith(item)), None)
    if suffix is None:
        return False
    stem = filename[: -len(suffix)]
    for index, character in enumerate(stem):
        if character not in "-_." or index == 0 or index == len(stem) - 1:
            continue
        if _canonical_name(stem[:index]) != _canonical_name(package):
            continue
        candidate = stem[index + 1 :]
        if suffix == ".whl":
            candidate = candidate.split("-", 1)[0]
        if _canonical_version(candidate) == version:
            return True
    return False


def _decode_content(payload: Any, description: str) -> bytes:
    item = _object(payload, description)
    _require_equal(item.get("encoding"), "base64", f"{description} encoding")
    content = item.get("content")
    if not isinstance(content, str):
        raise PublisherError(f"{description} has no base64 content")
    try:
        decoded = base64.b64decode(content, validate=False)
    except (ValueError, binascii.Error) as exc:
        raise PublisherError(f"{description} has malformed base64 content") from exc
    if len(decoded) > MAX_CONTROL_BYTES:
        raise PublisherError(f"{description} exceeds the control-file size limit")
    return decoded


def _server_time(value: Any, description: str) -> datetime:
    if not isinstance(value, str):
        raise PublisherError(f"{description} has no server timestamp")
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise PublisherError(f"{description} has an invalid server timestamp") from exc
    if parsed.tzinfo is None:
        raise PublisherError(f"{description} server timestamp has no timezone")
    return parsed.astimezone(UTC)


def _workflow_job_block(text: str, job_name: str) -> str:
    marker = f"  {job_name}:"
    lines = text.splitlines(keepends=True)
    starts = [index for index, line in enumerate(lines) if line.rstrip() == marker]
    if len(starts) != 1:
        raise PublisherError(f"Workflow does not contain exactly one {job_name} job")
    start = starts[0]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if re.fullmatch(r"  [A-Za-z0-9_-]+:\s*", lines[index]):
            end = index
            break
    return "".join(lines[start:end])


def _validate_workflow_secret_scope(text: str) -> None:
    prepare = _workflow_job_block(text, "prepare-package")
    verify = _workflow_job_block(text, "verify-and-seal")
    publish = _workflow_job_block(text, "publish-candidate")
    secret_names = re.findall(r"secrets\s*\.\s*([A-Za-z_][A-Za-z0-9_]*)", text)
    if re.search(r"secrets\s*\[", text) or secret_names != ["PACKAGE_WRITE_TOKEN"]:
        raise PublisherError("Workflow package secret set or cardinality is invalid")
    publish_marker = "      - name: Publish sealed package and verify served bytes"
    if publish.count(publish_marker) != 1:
        raise PublisherError("Workflow does not contain one credentialed publish step")
    before_publish, publish_and_later = publish.split(publish_marker, 1)
    publish_step = publish_and_later.split("\n      - name:", 1)[0]
    secret_reference = "${{ secrets.PACKAGE_WRITE_TOKEN }}"
    if (
        secret_reference in prepare
        or secret_reference in verify
        or secret_reference in before_publish
    ):
        raise PublisherError("Workflow exposes the package secret before the publish step")
    if publish_step.count(secret_reference) != 1:
        raise PublisherError("Publish step does not contain the exact package secret")


def _validate_workflow_publisher_rebuild(publish: str) -> None:
    source_marker = "      - name: Fetch exact tag source anonymously for independent rebuild"
    rebuild_marker = "      - name: Independently rebuild and compare exact tag distributions"
    publish_marker = "      - name: Publish sealed package and verify served bytes"
    required = (
        "EVENT_SOURCE_SHA: ${{ github.sha }}",
        "EVENT_TAG: ${{ github.ref_name }}",
        'git init "$TOOL_ROOT"',
        "fetch --force --no-tags --depth 1 origin",
        '"+refs/tags/${EVENT_TAG}:refs/tags/${EVENT_TAG}"',
        'checkout --detach "$EVENT_SOURCE_SHA"',
        'rev-parse HEAD)" = "$EVENT_SOURCE_SHA"',
        'rev-parse "refs/tags/${EVENT_TAG}^{commit}"',
        "tests/build_reproducible_distributions.py",
        "filecmp.cmp",
    )
    if "actions/checkout@" in publish or any(item not in publish for item in required):
        raise PublisherError("Publisher workflow is missing its independent rebuild control")
    if publish.count(source_marker) != 1:
        raise PublisherError("Publisher workflow does not contain one anonymous source fetch")
    source_and_later = publish.split(source_marker, 1)[1]
    source_step = source_and_later.split("\n      - name:", 1)[0]
    canonical_remote = (
        'git -C "$TOOL_ROOT" remote add origin \\\n'
        "            https://git.nmulti.cloud/emersonfelipesp/proxmox-sdk.git"
    )
    if (
        canonical_remote not in source_step
        or source_step.count("https://git.nmulti.cloud/emersonfelipesp/proxmox-sdk.git") != 1
    ):
        raise PublisherError("Publisher source fetch does not use the canonical public origin")
    forbidden_source_credentials = (
        "github.server_url",
        "github.token",
        "GITHUB_TOKEN",
        "GIT_ASKPASS",
        "secrets.",
    )
    if any(item in source_step for item in forbidden_source_credentials):
        raise PublisherError("Publisher source fetch must not receive credentials")
    if (
        publish.count(rebuild_marker) != 1
        or publish.index(source_marker) > publish.index(rebuild_marker)
        or publish.index(rebuild_marker) > publish.index(publish_marker)
    ):
        raise PublisherError("Publisher rebuild must precede the credentialed step")


def _validate_workflow_source(source: bytes, expected_sha256: str) -> None:
    if hashlib.sha256(source).hexdigest() != expected_sha256:
        raise PublisherError("Workflow source digest does not match the attestation")
    try:
        text = source.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PublisherError("Workflow source is not UTF-8") from exc
    prepare = _workflow_job_block(text, "prepare-package")
    verify = _workflow_job_block(text, "verify-and-seal")
    publish = _workflow_job_block(text, "publish-candidate")
    required = (
        f"name: {EXPECTED_WORKFLOW_NAME}",
        "packages: none",
        "actions/upload-artifact@c6a3b2bd78b3985e4b2f15397fec357f0fd808de",
        "actions/download-artifact@ad191675b41f6a5b46da9a048cb6893812da158b",
        "verify-and-seal:",
        "publish-candidate:",
    )
    if any(item not in text for item in required):
        raise PublisherError("Workflow source is missing a required credential-free control")
    if "runs-on: ci-untrusted-python312" not in prepare:
        raise PublisherError("Candidate workflow job requires the untrusted runner")
    if "runs-on: release-builder" not in verify or "runs-on: ci-untrusted-" in verify:
        raise PublisherError("Verifier workflow job requires the release builder runner")
    if "runs-on: release-publisher" not in publish or "runs-on: ci-untrusted-" in publish:
        raise PublisherError("Credentialed workflow job requires the release publisher runner")
    forbidden = (
        "TWINE_PASSWORD",
        "TWINE_USERNAME",
        "GITEA_PACKAGE_TOKEN",
        "packages: write",
    )
    if any(item in text for item in forbidden):
        raise PublisherError("Workflow source contains a forbidden publisher credential path")
    _validate_workflow_publisher_rebuild(publish)
    _validate_workflow_secret_scope(text)


def _validate_repository_and_run(client: GiteaReader, run_id: int) -> dict[str, Any]:
    prefix = f"/repos/{EXPECTED_FULL_NAME}"
    repository = _object(client.get_json(prefix), "repository response")
    _require_equal(repository.get("full_name"), EXPECTED_FULL_NAME, "repository owner/name")
    _require_equal(
        repository.get("clone_url"),
        f"{EXPECTED_SERVER}/{EXPECTED_FULL_NAME}.git",
        "repository clone URL",
    )

    run = _object(client.get_json(f"{prefix}/actions/runs/{run_id}"), "workflow run")
    _require_equal(run.get("id"), run_id, "workflow run ID")
    _require_equal(run.get("event"), "push", "workflow event")
    _require_equal(run.get("status"), "completed", "workflow status")
    _require_equal(run.get("conclusion"), "success", "workflow conclusion")
    run_repository = _object(run.get("repository"), "workflow repository")
    _require_equal(run_repository.get("full_name"), EXPECTED_FULL_NAME, "run repository")
    head_repository = run.get("head_repository")
    if head_repository is not None:
        _require_equal(
            _object(head_repository, "workflow head repository").get("full_name"),
            EXPECTED_FULL_NAME,
            "head repository",
        )
    source_sha = run.get("head_sha")
    path = run.get("path")
    attempt = run.get("run_attempt")
    if not isinstance(source_sha, str) or HEX40.fullmatch(source_sha) is None:
        raise PublisherError("Workflow source SHA is not a full lowercase commit digest")
    if not isinstance(path, str):
        raise PublisherError("Workflow run has no source-qualified workflow path")
    path_match = re.fullmatch(
        re.escape(EXPECTED_WORKFLOW_ID) + r"@refs/tags/(v[0-9][0-9A-Za-z._-]{0,127})",
        path,
    )
    if path_match is None:
        raise PublisherError("Workflow run is not the exact workflow at a safe v* tag")
    tag = path_match.group(1)
    if run.get("head_branch") not in {None, ""}:
        raise PublisherError("Tag workflow unexpectedly reports a branch head")
    if not isinstance(attempt, int) or attempt < 0:
        raise PublisherError("Workflow run attempt is invalid")
    workflow = _object(
        client.get_json(f"{prefix}/actions/workflows/{EXPECTED_WORKFLOW_ID}"),
        "workflow identity",
    )
    _require_equal(workflow.get("id"), EXPECTED_WORKFLOW_ID, "workflow ID")
    _require_equal(workflow.get("name"), EXPECTED_WORKFLOW_NAME, "workflow name")
    _require_equal(workflow.get("path"), EXPECTED_WORKFLOW_PATH, "workflow file path")
    _require_equal(workflow.get("state"), "active", "workflow state")
    run["_release_tag"] = tag
    return run


def _validate_successful_job(client: GiteaReader, run: Mapping[str, Any]) -> tuple[str, str, int]:
    run_id = int(run["id"])
    prefix = f"/repos/{EXPECTED_FULL_NAME}"
    response = _object(client.get_json(f"{prefix}/actions/runs/{run_id}/jobs"), "job list")
    jobs = [
        _object(item, "workflow job")
        for item in _list(response.get("jobs"), "workflow jobs")
        if isinstance(item, dict) and item.get("name") == EXPECTED_JOB_NAME
    ]
    if len(jobs) != 1:
        raise PublisherError("Workflow run does not contain exactly one expected builder job")
    job = jobs[0]
    job_attempt = job.get("run_attempt")
    if not isinstance(job_attempt, int) or job_attempt < 1:
        raise PublisherError("Builder job run attempt is invalid")
    if run["run_attempt"] not in {0, job_attempt}:
        raise PublisherError("Builder job run attempt does not match the workflow run")
    checks = {
        "job run ID": (job.get("run_id"), run_id),
        "job source SHA": (job.get("head_sha"), run["head_sha"]),
        "job branch marker": (job.get("head_branch"), run.get("head_branch")),
        "job status": (job.get("status"), "completed"),
        "job conclusion": (job.get("conclusion"), "success"),
    }
    for description, (actual, expected) in checks.items():
        _require_equal(actual, expected, description)
    labels = job.get("labels")
    if not isinstance(labels, list) or EXPECTED_RUNNER_LABEL not in labels:
        raise PublisherError("Builder job did not run on the untrusted release label")
    if "release-publisher" in labels:
        raise PublisherError("Builder job targeted a forbidden publisher runner")
    job_id = job.get("id")
    runner_id = job.get("runner_id")
    if not isinstance(job_id, int) or job_id < 1 or not isinstance(runner_id, int) or runner_id < 1:
        raise PublisherError("Builder job has no concrete job/runner identity")

    raw_log = client.get_bytes(f"{prefix}/actions/jobs/{job_id}/logs")
    if len(raw_log) > 128 * 1024 * 1024:
        raise PublisherError("Builder job log exceeds the size limit")
    try:
        log = raw_log.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise PublisherError("Builder job log is not UTF-8") from exc
    timestamp = r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9:.]+Z "
    artifact_values = re.findall(
        rf"^{timestamp}PROXMOX_SDK_ARTIFACT_NAME=(\S+)$", log, re.MULTILINE
    )
    digest_values = re.findall(
        rf"^{timestamp}PROXMOX_SDK_CANDIDATE_SHA256=([0-9a-f]{{64}})$",
        log,
        re.MULTILINE,
    )
    if len(artifact_values) != 1 or len(digest_values) != 1:
        raise PublisherError("Builder log lacks one unambiguous candidate identity")
    return artifact_values[0], digest_values[0], job_attempt


def _validate_tag_and_source(
    client: GiteaReader, run: Mapping[str, Any], policy: PublisherPolicy
) -> tuple[str, bytes, int]:
    prefix = f"/repos/{EXPECTED_FULL_NAME}"
    tag = str(run["_release_tag"])
    source_sha = str(run["head_sha"])
    version = tag.removeprefix("v")
    if _canonical_version(version) != version:
        raise PublisherError("Tag version is not canonical or is outside the release policy")

    tag_response = _object(client.get_json(f"{prefix}/tags/{tag}"), "tag response")
    _require_equal(tag_response.get("name"), tag, "tag name")
    tag_object_sha = tag_response.get("id")
    if not isinstance(tag_object_sha, str) or HEX40.fullmatch(tag_object_sha) is None:
        raise PublisherError("Tag does not expose an annotated tag object SHA")
    tag_commit = _object(tag_response.get("commit"), "tag commit")
    _require_equal(tag_commit.get("sha"), source_sha, "tag commit SHA")

    annotated = _object(client.get_json(f"{prefix}/git/tags/{tag_object_sha}"), "annotated tag")
    _require_equal(annotated.get("tag"), tag, "annotated tag name")
    _require_equal(annotated.get("sha"), tag_object_sha, "annotated tag object SHA")
    target = _object(annotated.get("object"), "annotated tag target")
    _require_equal(target.get("type"), "commit", "annotated tag target type")
    _require_equal(target.get("sha"), source_sha, "annotated tag target SHA")

    protections = _list(client.get_json(f"{prefix}/tag_protections"), "tag protections")
    exact_rules = [
        _object(item, "tag protection")
        for item in protections
        if isinstance(item, dict)
        and item.get("id") == policy.tag_protection_id
        and item.get("name_pattern") == EXPECTED_TAG_PROTECTION
    ]
    if len(exact_rules) != 1 or not fnmatch.fnmatchcase(tag, EXPECTED_TAG_PROTECTION):
        raise PublisherError("Tag is not covered by the pinned protected v* rule")
    rule = exact_rules[0]
    usernames = rule.get("whitelist_usernames", [])
    teams = rule.get("whitelist_teams", [])
    if sorted(usernames) != sorted(policy.whitelist_usernames) or sorted(teams) != sorted(
        policy.whitelist_teams
    ):
        raise PublisherError("Protected v* rule allowlists differ from host policy")
    run_started = _server_time(run.get("started_at"), "workflow run")
    if _server_time(rule.get("created_at"), "tag protection") > run_started:
        raise PublisherError("Protected v* rule was created after the workflow began")
    if _server_time(rule.get("updated_at"), "tag protection") > run_started:
        raise PublisherError("Protected v* rule changed after the workflow began")

    comparison = _object(
        client.get_json(f"{prefix}/compare/main...{source_sha}"), "main comparison"
    )
    comparison_commits = _list(comparison.get("commits"), "main comparison commits")
    if comparison.get("total_commits") != 0 or comparison_commits:
        raise PublisherError("Tagged commit is not an ancestor of main")

    pyproject = _decode_content(
        client.get_json(f"{prefix}/contents/pyproject.toml?ref={source_sha}"),
        "pyproject.toml",
    )
    try:
        project = tomllib.loads(pyproject.decode("utf-8"))["project"]
    except (KeyError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise PublisherError("Tagged pyproject.toml has invalid project metadata") from exc
    _require_equal(project.get("name"), EXPECTED_PACKAGE, "tagged package name")
    _require_equal(project.get("version"), version, "tagged package version")
    commit = _object(client.get_json(f"{prefix}/commits/{source_sha}"), "source commit")
    commit_details = _object(commit.get("commit"), "source commit details")
    committer = _object(commit_details.get("committer"), "source commit committer")
    source_date_epoch = int(_server_time(committer.get("date"), "source commit").timestamp())
    if not 315532800 <= source_date_epoch <= 4294967295:
        raise PublisherError("Source commit timestamp is outside the reproducible-build range")
    return version, pyproject, source_date_epoch


def _copy_bounded(source: Any, destination: Path, maximum: int, description: str) -> None:
    size = 0
    with destination.open("wb") as handle:
        while True:
            chunk = source.read(min(1024 * 1024, maximum - size + 1))
            if not chunk:
                return
            size += len(chunk)
            if size > maximum:
                raise PublisherError(f"{description} exceeds its size limit")
            handle.write(chunk)


def _unwrap_candidate(artifact_zip: Path, work: Path, expected_digest: str) -> Path:
    try:
        outer_size = artifact_zip.stat().st_size
    except OSError as exc:
        raise PublisherError("Candidate artifact archive is not readable") from exc
    if outer_size <= 0 or outer_size > MAX_PAYLOAD_BYTES:
        raise PublisherError("Candidate artifact archive has an invalid size")
    try:
        with zipfile.ZipFile(artifact_zip) as archive:
            members = [item for item in archive.infolist() if not item.is_dir()]
            if len(members) != 1:
                raise PublisherError("Actions artifact must contain exactly one payload")
            member = members[0]
            path = PurePosixPath(member.filename)
            if path.name != PAYLOAD_NAME or path.is_absolute() or ".." in path.parts:
                raise PublisherError("Actions artifact contains an unexpected payload path")
            if member.flag_bits & 0x1:
                raise PublisherError("Actions artifact payload must not be encrypted")
            if member.file_size <= 0 or member.file_size > MAX_PAYLOAD_BYTES:
                raise PublisherError("Actions artifact payload has an invalid size")
            payload = work / PAYLOAD_NAME
            with archive.open(member) as source:
                _copy_bounded(source, payload, MAX_PAYLOAD_BYTES, "candidate payload")
    except (OSError, zipfile.BadZipFile) as exc:
        raise PublisherError("Candidate artifact is not a valid ZIP archive") from exc
    if _sha256(payload) != expected_digest:
        raise PublisherError("Candidate payload digest does not match the exact successful job log")
    return payload


def _extract_candidate(payload: Path, work: Path) -> dict[str, Path]:
    destination = work / "candidate"
    destination.mkdir(mode=0o700)
    try:
        with tarfile.open(payload, mode="r:") as archive:
            members = archive.getmembers()
            names = [member.name for member in members]
            if len(names) != len(set(names)):
                raise PublisherError("Candidate payload contains duplicate paths")
            control = {
                "release-artifacts/distribution-manifest.json",
                "release-artifacts/gitea-provenance.json",
                "release-artifacts/SHA256SUMS",
            }
            distribution_names: set[str] = set()
            for name in names:
                path = PurePosixPath(name)
                if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
                    raise PublisherError("Candidate payload contains an unsafe member path")
                if name.startswith("dist/"):
                    if len(path.parts) != 2 or path.name != path.parts[1]:
                        raise PublisherError("Candidate distribution path is not a safe basename")
                    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]*", path.name) is None:
                        raise PublisherError("Candidate distribution filename is unsafe")
                    if name.endswith(DIST_SUFFIXES):
                        distribution_names.add(name)
            expected = control | distribution_names
            if len(distribution_names) != 2 or set(names) != expected:
                raise PublisherError("Candidate payload does not contain the closed five-file set")
            extracted: dict[str, Path] = {}
            for member in members:
                if not member.isfile():
                    raise PublisherError("Candidate payload contains a non-regular entry")
                maximum = (
                    MAX_DISTRIBUTION_BYTES if member.name.startswith("dist/") else MAX_CONTROL_BYTES
                )
                if member.size < 0 or member.size > maximum:
                    raise PublisherError(f"Candidate member exceeds its size limit: {member.name}")
                target = destination.joinpath(*PurePosixPath(member.name).parts)
                try:
                    target.resolve().relative_to(destination.resolve())
                except ValueError as exc:
                    raise PublisherError("Candidate member escapes the extraction root") from exc
                target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                source = archive.extractfile(member)
                if source is None:
                    raise PublisherError(f"Candidate member cannot be read: {member.name}")
                with source:
                    _copy_bounded(source, target, maximum, member.name)
                extracted[member.name] = target
            return extracted
    except (OSError, tarfile.TarError) as exc:
        raise PublisherError("Candidate payload is not a valid uncompressed tar archive") from exc


def _distribution_metadata(path: Path) -> dict[str, str]:
    try:
        if path.name.endswith(".whl"):
            with zipfile.ZipFile(path) as archive:
                names = [
                    name for name in archive.namelist() if name.endswith(".dist-info/METADATA")
                ]
                if len(names) != 1:
                    raise PublisherError(f"Wheel has no unique METADATA file: {path.name}")
                info = archive.getinfo(names[0])
                if info.file_size > MAX_CONTROL_BYTES:
                    raise PublisherError(f"Wheel METADATA exceeds its size limit: {path.name}")
                raw = archive.read(info)
            filetype = "bdist_wheel"
            pyversion = "py3"
        else:
            with tarfile.open(path, mode="r:gz") as archive:
                members = [
                    member
                    for member in archive.getmembers()
                    if member.isfile() and PurePosixPath(member.name).name == "PKG-INFO"
                ]
                if len(members) != 1 or members[0].size > MAX_CONTROL_BYTES:
                    raise PublisherError(f"Sdist has no bounded, unique PKG-INFO: {path.name}")
                source = archive.extractfile(members[0])
                if source is None:
                    raise PublisherError(f"Sdist PKG-INFO cannot be read: {path.name}")
                with source:
                    raw = source.read(MAX_CONTROL_BYTES + 1)
            if len(raw) > MAX_CONTROL_BYTES:
                raise PublisherError(f"Sdist PKG-INFO exceeds its size limit: {path.name}")
            filetype = "sdist"
            pyversion = "source"
    except (OSError, tarfile.TarError, zipfile.BadZipFile) as exc:
        raise PublisherError(f"Distribution metadata cannot be read: {path.name}") from exc
    message: Message = BytesParser().parsebytes(raw)
    values = {
        "name": message.get("Name", ""),
        "version": message.get("Version", ""),
        "metadata_version": message.get("Metadata-Version", ""),
        "summary": message.get("Summary", ""),
        "requires_python": message.get("Requires-Python", ""),
        "license": message.get("License", ""),
        "author": message.get("Author", ""),
        "home_page": message.get("Home-page", ""),
        "filetype": filetype,
        "pyversion": pyversion,
    }
    return values


def _set_tree_mtime(root: Path, timestamp: int) -> None:
    paths = sorted(root.rglob("*"), key=lambda path: len(path.parts), reverse=True)
    for path in paths:
        if not path.is_symlink():
            os.utime(path, (timestamp, timestamp), follow_symlinks=False)
    os.utime(root, (timestamp, timestamp), follow_symlinks=False)


def _normalize_sdist(path: Path, source_date_epoch: int) -> None:
    temporary = path.with_suffix(path.suffix + ".normalized")
    try:
        with tarfile.open(path, mode="r:gz") as source_archive, temporary.open("wb") as raw:
            with gzip.GzipFile(
                filename="", mode="wb", fileobj=raw, compresslevel=9, mtime=source_date_epoch
            ) as compressed:
                with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.PAX_FORMAT) as out:
                    for member in sorted(source_archive.getmembers(), key=lambda item: item.name):
                        member_path = PurePosixPath(member.name)
                        if member_path.is_absolute() or ".." in member_path.parts:
                            raise PublisherError("Trusted rebuild produced an unsafe sdist path")
                        normalized = copy.copy(member)
                        normalized.uid = 0
                        normalized.gid = 0
                        normalized.uname = ""
                        normalized.gname = ""
                        normalized.mtime = source_date_epoch
                        normalized.pax_headers = {}
                        payload = source_archive.extractfile(member) if member.isfile() else None
                        out.addfile(normalized, payload)
                        if payload is not None:
                            payload.close()
        os.replace(temporary, path)
    except (OSError, tarfile.TarError, gzip.BadGzipFile) as exc:
        raise PublisherError("Trusted rebuild could not normalize its sdist") from exc
    finally:
        temporary.unlink(missing_ok=True)


def _safe_extract_source(archive_bytes: bytes, destination: Path) -> Path:
    if not archive_bytes or len(archive_bytes) > 128 * 1024 * 1024:
        raise PublisherError("Tagged source archive has an invalid compressed size")
    destination.mkdir(mode=0o700)
    total = 0
    roots: set[str] = set()
    try:
        with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:gz") as archive:
            members = archive.getmembers()
            if not members or len(members) > 100_000:
                raise PublisherError("Tagged source archive has an invalid member count")
            for member in members:
                path = PurePosixPath(member.name)
                if path.is_absolute() or len(path.parts) < 1 or ".." in path.parts:
                    raise PublisherError("Tagged source archive contains an unsafe path")
                roots.add(path.parts[0])
                if not (member.isdir() or member.isfile()):
                    raise PublisherError("Tagged source archive contains a link or special entry")
                total += member.size
                if member.size < 0 or total > MAX_PAYLOAD_BYTES:
                    raise PublisherError("Tagged source archive exceeds its extracted size limit")
                target = destination.joinpath(*path.parts)
                try:
                    target.resolve().relative_to(destination.resolve())
                except ValueError as exc:
                    raise PublisherError(
                        "Tagged source member escapes the extraction root"
                    ) from exc
                if member.isdir():
                    target.mkdir(mode=0o700, parents=True, exist_ok=True)
                    continue
                target.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
                source = archive.extractfile(member)
                if source is None:
                    raise PublisherError("Tagged source member cannot be read")
                with source:
                    _copy_bounded(source, target, MAX_DISTRIBUTION_BYTES, member.name)
    except (OSError, tarfile.TarError, gzip.BadGzipFile) as exc:
        raise PublisherError("Tagged source archive is malformed") from exc
    if len(roots) != 1:
        raise PublisherError("Tagged source archive does not have one repository root")
    root = destination / next(iter(roots))
    if not (root / "pyproject.toml").is_file():
        raise PublisherError("Tagged source archive lacks pyproject.toml")
    return root


class TrustedSourceRebuilder:
    """Rebuild in a preinstalled, root-owned, version-pinned Python environment."""

    def __init__(self, interpreter: Path = BUILD_PYTHON) -> None:
        self._interpreter = interpreter

    def _environment(self, source_date_epoch: int) -> dict[str, str]:
        return {
            "LC_ALL": "C.UTF-8",
            "PATH": "/usr/bin:/bin",
            "PYTHONHASHSEED": "0",
            "PYTHONNOUSERSITE": "1",
            "SOURCE_DATE_EPOCH": str(source_date_epoch),
            "TZ": "UTC",
        }

    def _check_environment(self, environment: Mapping[str, str]) -> None:
        if not self._interpreter.is_absolute():
            raise PublisherError("Trusted build interpreter path must be absolute")
        script = (
            "import importlib.metadata as m,json,platform;"
            "print(json.dumps({'python':platform.python_version(),"
            "'tools':{n:m.version(n) for n in "
            "('build','packaging','pyproject-hooks','setuptools','wheel')}},sort_keys=True))"
        )
        completed = subprocess.run(
            [str(self._interpreter), "-I", "-c", script],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
            env=dict(environment),
            cwd="/",
        )
        if completed.returncode != 0:
            raise PublisherError("Immutable trusted build environment is unavailable")
        try:
            versions = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise PublisherError("Trusted build environment identity is malformed") from exc
        if versions != {"python": EXPECTED_PYTHON_VERSION, "tools": EXPECTED_BUILD_TOOLS}:
            raise PublisherError("Trusted build environment versions differ from policy")

    def rebuild(
        self,
        client: GiteaReader,
        *,
        source_sha: str,
        source_date_epoch: int,
        work: Path,
    ) -> Mapping[str, Path]:
        environment = self._environment(source_date_epoch)
        self._check_environment(environment)
        archive_bytes = client.get_bytes(f"/repos/{EXPECTED_FULL_NAME}/archive/{source_sha}.tar.gz")
        first_source = _safe_extract_source(archive_bytes, work / "trusted-source-1")
        second_source = _safe_extract_source(archive_bytes, work / "trusted-source-2")
        outputs: list[Path] = []
        hashes: list[dict[str, str]] = []
        for index, source in enumerate((first_source, second_source), start=1):
            _set_tree_mtime(source, source_date_epoch + (101 if index == 1 else 86401))
            output = work / f"trusted-dist-{index}"
            output.mkdir(mode=0o700)
            completed = subprocess.run(
                [
                    str(self._interpreter),
                    "-I",
                    "-m",
                    "build",
                    "--no-isolation",
                    "--outdir",
                    str(output),
                ],
                cwd=source,
                env=environment,
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=600,
            )
            if completed.returncode != 0:
                raise PublisherError("Independent trusted source rebuild failed")
            sdists = list(output.glob("*.tar.gz"))
            if len(sdists) != 1:
                raise PublisherError("Independent rebuild produced an invalid sdist set")
            _normalize_sdist(sdists[0], source_date_epoch)
            result = {
                path.name: _sha256(path)
                for path in output.iterdir()
                if path.is_file() and path.name.endswith(DIST_SUFFIXES)
            }
            if len(result) != 2:
                raise PublisherError("Independent rebuild produced an invalid distribution set")
            hashes.append(result)
            outputs.append(output)
        if hashes[0] != hashes[1]:
            raise PublisherError("Independent trusted rebuild is not byte reproducible")
        return {name: outputs[0] / name for name in hashes[0]}


def _git_output(source_root: Path, *arguments: str) -> str:
    try:
        completed = subprocess.run(
            ["git", "-C", str(source_root), *arguments],
            check=False,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PublisherError("Anonymous source checkout could not be inspected") from exc
    if completed.returncode != 0:
        raise PublisherError("Anonymous source checkout failed a Git identity check")
    return completed.stdout.strip()


def _git_bytes(source_root: Path, *arguments: str) -> bytes:
    try:
        completed = subprocess.run(
            ["git", "-C", str(source_root), *arguments],
            check=False,
            capture_output=True,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PublisherError("Anonymous source content could not be inspected") from exc
    if completed.returncode != 0:
        raise PublisherError("Anonymous source content failed a Git identity check")
    return completed.stdout


def _git_is_ancestor(source_root: Path, ancestor: str, descendant: str) -> None:
    try:
        completed = subprocess.run(
            ["git", "-C", str(source_root), "merge-base", "--is-ancestor", ancestor, descendant],
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=60,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise PublisherError("Canonical main ancestry could not be checked") from exc
    if completed.returncode != 0:
        raise PublisherError("Tagged commit is not an ancestor of canonical main")


def validate_actions_source(
    *, source_root: Path, source_sha: str, tag: str
) -> tuple[str, int, bytes]:
    """Validate an anonymously fetched exact tag and return its release identity."""

    if HEX40.fullmatch(source_sha) is None:
        raise PublisherError("Actions source SHA is not a full lowercase commit digest")
    version = tag.removeprefix("v")
    if tag != f"v{version}" or _canonical_version(version) != version:
        raise PublisherError("Actions tag version is not canonical or safe")
    if source_root.is_symlink() or not source_root.is_dir():
        raise PublisherError("Anonymous source checkout is unavailable or unsafe")
    expected_origin = f"{EXPECTED_SERVER}/{EXPECTED_FULL_NAME}.git"
    _require_equal(
        _git_output(source_root, "remote", "get-url", "origin"), expected_origin, "origin"
    )
    _require_equal(_git_output(source_root, "rev-parse", "HEAD"), source_sha, "checkout SHA")
    _require_equal(_git_output(source_root, "cat-file", "-t", tag), "tag", "tag object type")
    _require_equal(
        _git_output(source_root, "rev-parse", f"{tag}^{{commit}}"),
        source_sha,
        "tag commit SHA",
    )
    _git_is_ancestor(source_root, source_sha, "refs/remotes/origin/main")
    pyproject_bytes = _git_bytes(source_root, "show", f"{source_sha}:pyproject.toml")
    try:
        project = tomllib.loads(pyproject_bytes.decode("utf-8"))["project"]
    except (KeyError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        raise PublisherError("Tagged pyproject.toml has invalid project metadata") from exc
    _require_equal(project.get("name"), EXPECTED_PACKAGE, "tagged package name")
    _require_equal(project.get("version"), version, "tagged package version")
    timestamp = _git_output(source_root, "show", "-s", "--format=%ct", source_sha)
    if not timestamp.isascii() or not timestamp.isdigit():
        raise PublisherError("Source commit timestamp is invalid")
    source_date_epoch = int(timestamp)
    if not 315532800 <= source_date_epoch <= 4294967295:
        raise PublisherError("Source commit timestamp is outside the reproducible-build range")
    workflow = _git_bytes(source_root, "show", f"{source_sha}:{EXPECTED_WORKFLOW_PATH}")
    return version, source_date_epoch, workflow


class ActionsSourceRebuilder(TrustedSourceRebuilder):
    """Rebuild an anonymous checkout twice from independent Git worktrees."""

    def __init__(self, source_root: Path, interpreter: Path) -> None:
        super().__init__(interpreter)
        self._source_root = source_root

    def _add_worktree(self, destination: Path, source_sha: str) -> None:
        try:
            completed = subprocess.run(
                [
                    "git",
                    "-C",
                    str(self._source_root),
                    "worktree",
                    "add",
                    "--detach",
                    str(destination),
                    source_sha,
                ],
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise PublisherError("Independent source worktree could not be created") from exc
        if completed.returncode != 0:
            raise PublisherError("Independent source worktree could not be created")

    def _build_worktree(
        self,
        source: Path,
        output: Path,
        environment: Mapping[str, str],
        source_date_epoch: int,
    ) -> dict[str, str]:
        _set_tree_mtime(source, source_date_epoch)
        output.mkdir(mode=0o700)
        try:
            completed = subprocess.run(
                [
                    str(self._interpreter),
                    "-I",
                    "-m",
                    "build",
                    "--no-isolation",
                    "--outdir",
                    str(output),
                ],
                cwd=source,
                env=dict(environment),
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=600,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise PublisherError("Independent Actions source rebuild failed") from exc
        if completed.returncode != 0:
            raise PublisherError("Independent Actions source rebuild failed")
        sdists = list(output.glob("*.tar.gz"))
        if len(sdists) != 1:
            raise PublisherError("Independent Actions rebuild produced an invalid sdist set")
        _normalize_sdist(sdists[0], source_date_epoch)
        hashes = {
            path.name: _sha256(path)
            for path in output.iterdir()
            if path.is_file() and path.name.endswith(DIST_SUFFIXES)
        }
        if len(hashes) != 2:
            raise PublisherError("Independent Actions rebuild produced an invalid distribution set")
        return hashes

    def _remove_worktree(self, source: Path) -> None:
        subprocess.run(
            ["git", "-C", str(self._source_root), "worktree", "remove", "--force", str(source)],
            check=False,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=60,
        )

    def rebuild(
        self,
        client: GiteaReader,
        *,
        source_sha: str,
        source_date_epoch: int,
        work: Path,
    ) -> Mapping[str, Path]:
        del client
        environment = self._environment(source_date_epoch)
        self._check_environment(environment)
        hashes: list[dict[str, str]] = []
        outputs: list[Path] = []
        for index in (1, 2):
            source = work / f"actions-source-{index}"
            output = work / f"actions-dist-{index}"
            self._add_worktree(source, source_sha)
            try:
                hashes.append(self._build_worktree(source, output, environment, source_date_epoch))
                outputs.append(output)
            finally:
                self._remove_worktree(source)
        if hashes[0] != hashes[1]:
            raise PublisherError("Independent Actions worktree builds are not byte reproducible")
        return {name: outputs[0] / name for name in hashes[0]}


def verify_candidate(
    client: GiteaReader,
    *,
    policy: PublisherPolicy,
    rebuilder: SourceRebuilder,
    run_id: int,
    artifact_zip: Path,
    work: Path,
) -> VerifiedCandidate:
    """Validate all remote control-plane and local byte evidence without publish credentials."""

    if run_id < 1:
        raise PublisherError("Run ID must be a positive integer")
    work.mkdir(mode=0o700, parents=True, exist_ok=True)
    run = _validate_repository_and_run(client, run_id)
    artifact_name, candidate_sha256, run_attempt = _validate_successful_job(client, run)
    version, _pyproject, source_date_epoch = _validate_tag_and_source(client, run, policy)
    source_sha = str(run["head_sha"])
    expected_artifact_name = f"gitea-dist-{source_sha}-{run_id}-{run_attempt}"
    _require_equal(artifact_name, expected_artifact_name, "Actions artifact name")

    payload = _unwrap_candidate(artifact_zip, work, candidate_sha256)
    extracted = _extract_candidate(payload, work)
    manifest_path = extracted["release-artifacts/distribution-manifest.json"]
    try:
        manifest = _object(
            json.loads(manifest_path.read_text(encoding="utf-8")),
            "distribution manifest",
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PublisherError("Distribution manifest is malformed") from exc

    expected_manifest = {
        "algorithm": "sha256",
        "source_date_epoch": source_date_epoch,
        "source_sha": source_sha,
        "version": version,
    }
    if set(manifest) != {*expected_manifest, "artifacts"}:
        raise PublisherError("Canonical distribution manifest field set is invalid")
    for key, expected in expected_manifest.items():
        _require_equal(manifest.get(key), expected, f"manifest {key}")

    provenance_path = extracted["release-artifacts/gitea-provenance.json"]
    try:
        provenance = _object(
            json.loads(provenance_path.read_text(encoding="utf-8")),
            "Gitea provenance",
        )
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PublisherError("Gitea provenance is malformed") from exc
    expected_provenance = {
        "schema_version": 1,
        "artifact_name": artifact_name,
        "distribution_manifest_sha256": _sha256(manifest_path),
        "event": "push",
        "ref": f"refs/tags/v{version}",
        "repository": EXPECTED_FULL_NAME,
        "run_attempt": run_attempt,
        "run_id": run_id,
        "server_url": EXPECTED_SERVER,
        "source_sha": source_sha,
        "tag": f"v{version}",
        "version": version,
        "workflow_name": EXPECTED_WORKFLOW_NAME,
        "workflow_path": EXPECTED_WORKFLOW_PATH,
    }
    if set(provenance) != {*expected_provenance, "workflow_sha256"}:
        raise PublisherError("Gitea provenance field set is invalid")
    for key, expected in expected_provenance.items():
        _require_equal(provenance.get(key), expected, f"provenance {key}")
    workflow_sha256 = provenance.get("workflow_sha256")
    if not isinstance(workflow_sha256, str) or HEX64.fullmatch(workflow_sha256) is None:
        raise PublisherError("Manifest workflow SHA256 is invalid")
    prefix = f"/repos/{EXPECTED_FULL_NAME}"
    workflow_source = _decode_content(
        client.get_json(f"{prefix}/contents/{EXPECTED_WORKFLOW_PATH}?ref={source_sha}"),
        "workflow source",
    )
    _validate_workflow_source(workflow_source, workflow_sha256)

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict) or len(artifacts) != 2:
        raise PublisherError("Distribution manifest must name exactly two artifacts")
    distributions = {
        PurePosixPath(name).name: path
        for name, path in extracted.items()
        if name.startswith("dist/")
    }
    if set(artifacts) != set(distributions):
        raise PublisherError("Distribution manifest artifact set does not match the payload")
    if (
        sum(name.endswith(".whl") for name in distributions) != 1
        or sum(name.endswith(".tar.gz") for name in distributions) != 1
    ):
        raise PublisherError("Candidate must contain exactly one wheel and one sdist")
    for name, path in distributions.items():
        digest = artifacts.get(name)
        if not isinstance(digest, str) or HEX64.fullmatch(digest) is None:
            raise PublisherError(f"Manifest SHA256 is invalid for {name}")
        if _sha256(path) != digest:
            raise PublisherError(f"Distribution SHA256 mismatch for {name}")
        if not _belongs_to_release(name, EXPECTED_PACKAGE, version):
            raise PublisherError(f"Distribution filename is not bound to this release: {name}")

    rebuilt = rebuilder.rebuild(
        client,
        source_sha=source_sha,
        source_date_epoch=source_date_epoch,
        work=work,
    )
    if set(rebuilt) != set(distributions):
        raise PublisherError("Independent rebuild distribution set differs from candidate")
    for name, path in rebuilt.items():
        if _sha256(path) != _sha256(distributions[name]):
            raise PublisherError(
                f"Candidate bytes differ from independent trusted source rebuild: {name}"
            )

    expected_checksums = "".join(f"{artifacts[name]}  dist/{name}\n" for name in sorted(artifacts))
    try:
        checksums = extracted["release-artifacts/SHA256SUMS"].read_text(encoding="ascii")
    except (OSError, UnicodeDecodeError) as exc:
        raise PublisherError("SHA256SUMS is not valid ASCII") from exc
    _require_equal(checksums, expected_checksums, "SHA256SUMS content")

    metadata = {name: _distribution_metadata(path) for name, path in distributions.items()}
    for name, values in metadata.items():
        if _canonical_name(values["name"]) != _canonical_name(EXPECTED_PACKAGE):
            raise PublisherError(f"Distribution metadata name mismatch for {name}")
        _require_equal(values["version"], version, f"distribution metadata version for {name}")
        if not values["metadata_version"]:
            raise PublisherError(f"Distribution metadata version is missing for {name}")

    return VerifiedCandidate(
        artifact_name=artifact_name,
        candidate_sha256=candidate_sha256,
        distributions=distributions,
        metadata=metadata,
        run_attempt=run_attempt,
        run_id=run_id,
        source_sha=source_sha,
        tag=str(run["_release_tag"]),
        version=version,
        distribution_manifest_sha256=_sha256(manifest_path),
        gitea_provenance_sha256=_sha256(provenance_path),
        distribution_manifest=manifest_path,
        gitea_provenance=provenance_path,
    )


def _load_candidate_document(path: Path, description: str) -> dict[str, Any]:
    try:
        return _object(json.loads(path.read_text(encoding="utf-8")), description)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PublisherError(f"{description} is malformed") from exc


def _validate_actions_attestation(
    *,
    extracted: Mapping[str, Path],
    artifact_name: str,
    run_id: int,
    run_attempt: int,
    source_sha: str,
    source_date_epoch: int,
    version: str,
    workflow_source: bytes,
) -> tuple[dict[str, Any], Path, Path]:
    manifest_path = extracted["release-artifacts/distribution-manifest.json"]
    manifest = _load_candidate_document(manifest_path, "distribution manifest")
    expected_manifest = {
        "algorithm": "sha256",
        "source_date_epoch": source_date_epoch,
        "source_sha": source_sha,
        "version": version,
    }
    if set(manifest) != {*expected_manifest, "artifacts"}:
        raise PublisherError("Canonical distribution manifest field set is invalid")
    for key, expected in expected_manifest.items():
        _require_equal(manifest.get(key), expected, f"manifest {key}")

    provenance_path = extracted["release-artifacts/gitea-provenance.json"]
    provenance = _load_candidate_document(provenance_path, "Gitea provenance")
    expected_provenance = {
        "schema_version": 1,
        "artifact_name": artifact_name,
        "distribution_manifest_sha256": _sha256(manifest_path),
        "event": "push",
        "ref": f"refs/tags/v{version}",
        "repository": EXPECTED_FULL_NAME,
        "run_attempt": run_attempt,
        "run_id": run_id,
        "server_url": EXPECTED_SERVER,
        "source_sha": source_sha,
        "tag": f"v{version}",
        "version": version,
        "workflow_name": EXPECTED_WORKFLOW_NAME,
        "workflow_path": EXPECTED_WORKFLOW_PATH,
    }
    if set(provenance) != {*expected_provenance, "workflow_sha256"}:
        raise PublisherError("Gitea provenance field set is invalid")
    for key, expected in expected_provenance.items():
        _require_equal(provenance.get(key), expected, f"provenance {key}")
    workflow_sha256 = provenance.get("workflow_sha256")
    if not isinstance(workflow_sha256, str) or HEX64.fullmatch(workflow_sha256) is None:
        raise PublisherError("Manifest workflow SHA256 is invalid")
    _validate_workflow_source(workflow_source, workflow_sha256)
    return manifest, manifest_path, provenance_path


def _validate_candidate_distributions(
    *, extracted: Mapping[str, Path], manifest: Mapping[str, Any], version: str
) -> dict[str, Path]:
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, dict) or len(artifacts) != 2:
        raise PublisherError("Distribution manifest must name exactly two artifacts")
    distributions = {
        PurePosixPath(name).name: path
        for name, path in extracted.items()
        if name.startswith("dist/")
    }
    if set(artifacts) != set(distributions):
        raise PublisherError("Distribution manifest artifact set does not match the payload")
    if sum(name.endswith(".whl") for name in distributions) != 1:
        raise PublisherError("Candidate must contain exactly one wheel")
    if sum(name.endswith(".tar.gz") for name in distributions) != 1:
        raise PublisherError("Candidate must contain exactly one sdist")
    for name, path in distributions.items():
        _validate_distribution_digest(name, path, artifacts.get(name), version)
    _validate_candidate_checksums(extracted, artifacts)
    return distributions


def _validate_distribution_digest(name: str, path: Path, digest: Any, version: str) -> None:
    if not isinstance(digest, str) or HEX64.fullmatch(digest) is None:
        raise PublisherError(f"Manifest SHA256 is invalid for {name}")
    if _sha256(path) != digest:
        raise PublisherError(f"Distribution SHA256 mismatch for {name}")
    if not _belongs_to_release(name, EXPECTED_PACKAGE, version):
        raise PublisherError(f"Distribution filename is not bound to this release: {name}")


def _validate_candidate_checksums(
    extracted: Mapping[str, Path], artifacts: Mapping[str, Any]
) -> None:
    expected_checksums = "".join(f"{artifacts[name]}  dist/{name}\n" for name in sorted(artifacts))
    try:
        checksums = extracted["release-artifacts/SHA256SUMS"].read_text(encoding="ascii")
    except (OSError, UnicodeDecodeError) as exc:
        raise PublisherError("SHA256SUMS is not valid ASCII") from exc
    _require_equal(checksums, expected_checksums, "SHA256SUMS content")


def _validate_rebuilt_distributions(
    distributions: Mapping[str, Path], rebuilt: Mapping[str, Path]
) -> None:
    if set(rebuilt) != set(distributions):
        raise PublisherError("Independent rebuild distribution set differs from candidate")
    for name, path in rebuilt.items():
        if _sha256(path) != _sha256(distributions[name]):
            raise PublisherError(
                f"Candidate bytes differ from independent trusted source rebuild: {name}"
            )


def _validated_distribution_metadata(
    distributions: Mapping[str, Path], version: str
) -> dict[str, dict[str, str]]:
    metadata = {name: _distribution_metadata(path) for name, path in distributions.items()}
    for name, values in metadata.items():
        if _canonical_name(values["name"]) != _canonical_name(EXPECTED_PACKAGE):
            raise PublisherError(f"Distribution metadata name mismatch for {name}")
        _require_equal(values["version"], version, f"distribution metadata version for {name}")
        if not values["metadata_version"]:
            raise PublisherError(f"Distribution metadata version is missing for {name}")
    return metadata


def _validate_candidate_tar(path: Path, expected_sha256: str) -> str:
    try:
        details = path.lstat()
    except OSError as exc:
        raise PublisherError("Actions candidate payload is unavailable") from exc
    if path.is_symlink() or not stat.S_ISREG(details.st_mode):
        raise PublisherError("Actions candidate payload must be a regular non-symlink file")
    if not 0 < details.st_size <= MAX_PAYLOAD_BYTES:
        raise PublisherError("Actions candidate payload has an invalid size")
    actual = _sha256(path)
    if HEX64.fullmatch(expected_sha256) is None or actual != expected_sha256:
        raise PublisherError("Actions candidate payload digest does not match the builder output")
    return actual


class _UnusedGiteaReader:
    def get_json(self, path: str) -> Any:
        raise PublisherError(f"Unexpected Actions Gitea JSON read: {path}")

    def get_bytes(self, path: str) -> bytes:
        raise PublisherError(f"Unexpected Actions Gitea byte read: {path}")


def verify_actions_candidate(
    *,
    source_root: Path,
    interpreter: Path,
    candidate_tar: Path,
    expected_candidate_sha256: str,
    run_id: int,
    run_attempt: int,
    source_sha: str,
    tag: str,
    repository: str,
    server_url: str,
    work: Path,
) -> VerifiedCandidate:
    """Verify Actions event evidence and rebuild twice without package credentials."""

    if run_id < 1 or run_attempt < 1:
        raise PublisherError("Actions run identity must contain positive integers")
    _require_equal(repository, EXPECTED_FULL_NAME, "Actions repository identity")
    _require_equal(server_url, EXPECTED_SERVER, "Actions canonical server URL")
    version, source_date_epoch, workflow_source = validate_actions_source(
        source_root=source_root,
        source_sha=source_sha,
        tag=tag,
    )
    artifact_name = f"gitea-dist-{source_sha}-{run_id}-{run_attempt}"
    candidate_sha256 = _validate_candidate_tar(candidate_tar, expected_candidate_sha256)
    work.mkdir(mode=0o700, parents=True, exist_ok=False)
    extracted = _extract_candidate(candidate_tar, work)
    manifest, manifest_path, provenance_path = _validate_actions_attestation(
        extracted=extracted,
        artifact_name=artifact_name,
        run_id=run_id,
        run_attempt=run_attempt,
        source_sha=source_sha,
        source_date_epoch=source_date_epoch,
        version=version,
        workflow_source=workflow_source,
    )
    distributions = _validate_candidate_distributions(
        extracted=extracted,
        manifest=manifest,
        version=version,
    )
    rebuilt = ActionsSourceRebuilder(source_root, interpreter).rebuild(
        _UnusedGiteaReader(),
        source_sha=source_sha,
        source_date_epoch=source_date_epoch,
        work=work,
    )
    _validate_rebuilt_distributions(distributions, rebuilt)
    metadata = _validated_distribution_metadata(distributions, version)
    return VerifiedCandidate(
        artifact_name=artifact_name,
        candidate_sha256=candidate_sha256,
        distributions=distributions,
        metadata=metadata,
        run_attempt=run_attempt,
        run_id=run_id,
        source_sha=source_sha,
        tag=tag,
        version=version,
        distribution_manifest_sha256=_sha256(manifest_path),
        gitea_provenance_sha256=_sha256(provenance_path),
        distribution_manifest=manifest_path,
        gitea_provenance=provenance_path,
    )


def _load_registry_credential_payload(path: Path) -> dict[str, Any]:
    try:
        details = path.lstat()
    except OSError as exc:
        raise PublisherError("Package credential is unavailable") from exc
    if stat.S_ISLNK(details.st_mode) or not stat.S_ISREG(details.st_mode):
        raise PublisherError("Package credential must be a regular, non-symlink file")
    if stat.S_IMODE(details.st_mode) & 0o077:
        raise PublisherError("Package credential must not be group/world accessible")
    if details.st_uid not in {0, os.geteuid()} or details.st_size > 16 * 1024:
        raise PublisherError("Package credential ownership or size is invalid")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PublisherError("Package credential file is malformed") from exc
    if not isinstance(payload, dict) or set(payload) != {"username", "token"}:
        raise PublisherError("Package credential must contain only username and token")
    return payload


def load_registry_credential(path: Path) -> RegistryCredential:
    """Open the host-only package credential after provenance verification."""

    payload = _load_registry_credential_payload(path)
    username = payload["username"]
    token = payload["token"]
    if not isinstance(username, str) or not isinstance(token, str):
        raise PublisherError("Package credential values must be strings")
    if not username or len(username) > 255:
        raise PublisherError("Package credential values have invalid lengths")
    if any(ord(character) < 0x20 or ord(character) == 0x7F for character in username):
        raise PublisherError("Package credential values contain control characters")
    return RegistryCredential(username=username, token=_validate_package_token(token))


def load_publisher_policy(path: Path) -> PublisherPolicy:
    """Load the root-owned, non-secret policy pinned before release."""

    try:
        details = path.lstat()
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PublisherError("Publisher policy file is unavailable or malformed") from exc
    if stat.S_ISLNK(details.st_mode) or not stat.S_ISREG(details.st_mode):
        raise PublisherError("Publisher policy must be a regular, non-symlink file")
    if stat.S_IMODE(details.st_mode) & 0o022 or details.st_uid != 0:
        raise PublisherError("Publisher policy must be root-owned and not group/world writable")
    if not isinstance(payload, dict) or set(payload) != {
        "tag_protection_id",
        "whitelist_usernames",
        "whitelist_teams",
    }:
        raise PublisherError("Publisher policy field set is invalid")
    protection_id = payload["tag_protection_id"]
    usernames = payload["whitelist_usernames"]
    teams = payload["whitelist_teams"]
    if not isinstance(protection_id, int) or protection_id < 1:
        raise PublisherError("Publisher policy tag protection ID is invalid")
    if not isinstance(usernames, list) or not isinstance(teams, list):
        raise PublisherError("Publisher policy allowlists must be lists")
    if any(not isinstance(value, str) or not value for value in [*usernames, *teams]):
        raise PublisherError("Publisher policy allowlist entry is invalid")
    if len(set(usernames)) != len(usernames) or len(set(teams)) != len(teams):
        raise PublisherError("Publisher policy allowlists contain duplicates")
    if EXPECTED_OWNER not in usernames:
        raise PublisherError("Publisher policy must explicitly authorize the repository owner")
    return PublisherPolicy(protection_id, tuple(usernames), tuple(teams))


class NmsGitReader:
    """Read exact Gitea evidence through the workspace-approved nms git surface."""

    def __init__(self, credential_file: Path) -> None:
        self._credential_file = credential_file

    def _get(self, path: str) -> bytes:
        if not path.startswith(f"/repos/{EXPECTED_FULL_NAME}/") and path != (
            f"/repos/{EXPECTED_FULL_NAME}"
        ):
            raise PublisherError("Refusing an out-of-policy Gitea API path")
        if any(character in path for character in "\r\n\0"):
            raise PublisherError("Refusing an unsafe Gitea API path")
        with tempfile.TemporaryDirectory(prefix="proxmox-sdk-gitea-read-") as temporary:
            output = Path(temporary) / "response"
            command = [
                str(NMS_EXECUTABLE),
                "git",
                "api",
                "GET",
                path,
                "--direct",
                "--credential-file",
                str(self._credential_file),
                "--output",
                str(output),
            ]
            result = subprocess.run(
                command,
                check=False,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                timeout=120,
            )
            if result.returncode != 0:
                raise PublisherError("Read-only Gitea evidence request failed")
            try:
                payload = output.read_bytes()
            except OSError as exc:
                raise PublisherError("Read-only Gitea evidence response is unavailable") from exc
        return payload

    def get_json(self, path: str) -> Any:
        try:
            return json.loads(self._get(path))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PublisherError("Gitea evidence response is not valid JSON") from exc

    def get_bytes(self, path: str) -> bytes:
        return self._get(path)


class _Links(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.values: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            value = dict(attrs).get("href")
            if value:
                self.values.append(value)


class _SameOriginRedirect(urllib.request.HTTPRedirectHandler):
    def __init__(self, origin: tuple[str, str]) -> None:
        super().__init__()
        self._origin = origin

    def redirect_request(  # ty: ignore[invalid-method-override]
        self, request: Any, fp: Any, code: int, message: str, headers: Any, new_url: str
    ) -> Any:
        parsed = urllib.parse.urlsplit(new_url)
        if (parsed.scheme, parsed.netloc) != self._origin:
            raise PublisherError("Package registry redirected across origins")
        return super().redirect_request(request, fp, code, message, headers, new_url)


class GiteaPackageRegistry:
    """Minimal, bounded legacy PyPI client with no dynamically resolved dependencies."""

    def __init__(self, credential: RegistryCredential) -> None:
        self._base = f"{EXPECTED_SERVER}/api/packages/{EXPECTED_OWNER}/pypi"
        parsed = urllib.parse.urlsplit(self._base)
        self._origin = (parsed.scheme, parsed.netloc)
        encoded = base64.b64encode(
            f"{credential.username}:{credential.token}".encode("utf-8")
        ).decode("ascii")
        self._authorization = f"Basic {encoded}"
        self._opener = urllib.request.build_opener(_SameOriginRedirect(self._origin))

    def _request(self, request: urllib.request.Request, maximum: int) -> bytes:
        request.add_header("Authorization", self._authorization)
        request.add_header("User-Agent", "proxmox-sdk-host-publisher/1")
        try:
            with self._opener.open(request, timeout=60) as response:
                final = urllib.parse.urlsplit(response.geturl())
                if (final.scheme, final.netloc) != self._origin:
                    raise PublisherError("Package registry response crossed origins")
                payload = response.read(maximum + 1)
        except urllib.error.HTTPError:
            raise
        except (OSError, urllib.error.URLError) as exc:
            raise PublisherError("Package registry request failed") from exc
        if len(payload) > maximum:
            raise PublisherError("Package registry response exceeds its size limit")
        return payload

    def inspect(self, package: str, version: str) -> dict[str, str]:
        url = f"{self._base}/simple/{urllib.parse.quote(_canonical_name(package), safe='')}/"
        try:
            raw = self._request(urllib.request.Request(url), MAX_CONTROL_BYTES)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return {}
            raise PublisherError("Package registry index request failed") from exc
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise PublisherError("Package registry index is not UTF-8") from exc
        links = _Links()
        links.feed(text)
        result: dict[str, str] = {}
        for href in links.values:
            resolved = urllib.parse.urljoin(url, href)
            parsed = urllib.parse.urlsplit(resolved)
            if (parsed.scheme, parsed.netloc) != self._origin:
                raise PublisherError("Package registry index contains a cross-origin link")
            filename = PurePosixPath(urllib.parse.unquote(parsed.path)).name
            if not _belongs_to_release(filename, package, version):
                continue
            request = urllib.request.Request(resolved)
            payload = self._request(request, MAX_DISTRIBUTION_BYTES)
            if filename in result:
                raise PublisherError("Package registry returned a duplicate release artifact")
            result[filename] = hashlib.sha256(payload).hexdigest()
        return result

    def upload(self, artifact: Path, metadata: Mapping[str, str]) -> None:
        boundary = f"proxmox-sdk-{os.urandom(24).hex()}"
        fields = {
            ":action": "file_upload",
            "protocol_version": "1",
            "name": metadata["name"],
            "version": metadata["version"],
            "metadata_version": metadata["metadata_version"],
            "summary": metadata["summary"],
            "requires_python": metadata["requires_python"],
            "license": metadata["license"],
            "author": metadata["author"],
            "home_page": metadata["home_page"],
            "filetype": metadata["filetype"],
            "pyversion": metadata["pyversion"],
            "sha256_digest": _sha256(artifact),
        }
        chunks: list[bytes] = []
        for key, value in fields.items():
            chunks.extend(
                (
                    f"--{boundary}\r\n".encode(),
                    f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode(),
                    value.encode("utf-8"),
                    b"\r\n",
                )
            )
        chunks.extend(
            (
                f"--{boundary}\r\n".encode(),
                (
                    'Content-Disposition: form-data; name="content"; '
                    f'filename="{artifact.name}"\r\n'
                ).encode(),
                b"Content-Type: application/octet-stream\r\n\r\n",
                artifact.read_bytes(),
                b"\r\n",
                f"--{boundary}--\r\n".encode(),
            )
        )
        request = urllib.request.Request(
            self._base + "/",
            data=b"".join(chunks),
            method="POST",
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        try:
            self._request(request, MAX_CONTROL_BYTES)
        except urllib.error.HTTPError as exc:
            raise PublisherError("Package registry upload failed") from exc


class RegistryHttpConnection(Protocol):
    sock: Any

    def request(
        self, method: str, url: str, body: bytes | None, headers: Mapping[str, str]
    ) -> None: ...

    def getresponse(self) -> Any: ...

    def putrequest(self, method: str, url: str) -> None: ...

    def putheader(self, header: str, *values: str) -> None: ...

    def endheaders(self) -> None: ...

    def send(self, data: bytes) -> None: ...

    def close(self) -> None: ...


def _multipart_prefix(boundary: str, fields: Mapping[str, str], artifact_name: str) -> bytes:
    if re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]*", artifact_name) is None:
        raise PublisherError("Upload artifact filename is unsafe")
    chunks: list[bytes] = []
    for key, value in fields.items():
        if re.fullmatch(r"[:A-Za-z_][A-Za-z0-9_:.-]*", key) is None:
            raise PublisherError("Upload metadata field name is unsafe")
        chunks.extend(
            (
                f"--{boundary}\r\n".encode(),
                f'Content-Disposition: form-data; name="{key}"\r\n\r\n'.encode(),
                value.encode("utf-8"),
                b"\r\n",
            )
        )
    chunks.extend(
        (
            f"--{boundary}\r\n".encode(),
            (
                f'Content-Disposition: form-data; name="content"; filename="{artifact_name}"\r\n'
            ).encode(),
            b"Content-Type: application/octet-stream\r\n\r\n",
        )
    )
    prefix = b"".join(chunks)
    if len(prefix) > MAX_CONTROL_BYTES:
        raise PublisherError("Upload metadata exceeds its size limit")
    return prefix


class BoundedRegistryClient:
    """A no-redirect registry client with request, body, and wall-clock bounds."""

    def __init__(
        self,
        *,
        server_url: str,
        token: str,
        deadline_seconds: float = 180.0,
        request_timeout: float = 15.0,
        connection_factory: Callable[[str, float], RegistryHttpConnection] | None = None,
        clock: Callable[[], float] = time.monotonic,
    ) -> None:
        _validate_package_token(token)
        parsed = urllib.parse.urlsplit(server_url)
        if (
            parsed.scheme != "https"
            or not parsed.netloc
            or parsed.username is not None
            or parsed.password is not None
            or parsed.query
            or parsed.fragment
            or parsed.path not in {"", "/"}
        ):
            raise PublisherError("Registry server URL must be a credential-free HTTPS origin")
        if not 0 < deadline_seconds <= 600 or not 0 < request_timeout <= 60:
            raise PublisherError("Registry timeout bounds are invalid")
        self.origin = f"{parsed.scheme}://{parsed.netloc}"
        self._host = parsed.netloc
        self._token = token
        self._clock = clock
        self._deadline = clock() + deadline_seconds
        self._request_timeout = request_timeout
        self._connection_factory = connection_factory or (
            lambda host, timeout: http.client.HTTPSConnection(host, timeout=timeout)
        )

    def remaining(self) -> float:
        remaining = self._deadline - self._clock()
        if remaining <= 0:
            raise PublisherError("Registry operation exceeded its deadline")
        return remaining

    @staticmethod
    def _response_socket(response: Any, connection: RegistryHttpConnection) -> Any:
        if connection.sock is not None:
            return connection.sock
        stream = getattr(response, "fp", None)
        raw_stream = getattr(stream, "raw", None)
        response_socket = getattr(raw_stream, "_sock", None)
        if response_socket is None:
            raise PublisherError("Registry response did not expose a bounded socket")
        return response_socket

    def _read_bounded(
        self, response: Any, connection: RegistryHttpConnection, maximum: int
    ) -> bytes:
        length_value = response.getheader("Content-Length")
        if length_value is not None:
            try:
                content_length = int(length_value)
            except ValueError as exc:
                raise PublisherError("Registry returned an invalid Content-Length") from exc
            if content_length < 0 or content_length > maximum:
                raise PublisherError("Registry response exceeds the allowed size")
        result = bytearray()
        response_socket = self._response_socket(response, connection)
        while True:
            remaining = self.remaining()
            response_socket.settimeout(min(self._request_timeout, remaining))
            chunk = response.read(min(64 * 1024, maximum + 1 - len(result)))
            if not chunk:
                break
            result.extend(chunk)
            if len(result) > maximum:
                raise PublisherError("Registry response exceeds the allowed size")
        self.remaining()
        return bytes(result)

    def request_bytes(
        self,
        *,
        method: str,
        path: str,
        maximum: int,
        allow_not_found: bool = False,
    ) -> bytes | None:
        if not path.startswith("/") or any(character in path for character in "\r\n"):
            raise PublisherError("Registry request path is invalid")
        connection = self._connection_factory(
            self._host,
            min(self._request_timeout, self.remaining()),
        )
        try:
            connection.request(
                method,
                path,
                b"" if method == "POST" else None,
                {
                    "Authorization": f"token {self._token}",
                    "Accept": "application/json",
                    "User-Agent": "proxmox-sdk-actions-publisher/1",
                },
            )
            response = connection.getresponse()
            status = int(response.status)
            if status == 404 and allow_not_found:
                return None
            if 300 <= status < 400:
                raise PublisherError("Registry redirect was refused")
            if not 200 <= status < 300:
                raise PublisherError(f"Registry request failed with HTTP {status}")
            return self._read_bounded(response, connection, maximum)
        except PublisherError:
            raise
        except ValueError:
            raise PublisherError("Registry request headers are invalid") from None
        except (TimeoutError, http.client.HTTPException, OSError) as exc:
            raise PublisherError("Registry request failed or timed out") from exc
        finally:
            connection.close()

    def request_json(self, *, path: str, allow_not_found: bool = False) -> Any | None:
        payload = self.request_bytes(
            method="GET",
            path=path,
            maximum=MAX_CONTROL_BYTES,
            allow_not_found=allow_not_found,
        )
        if payload is None:
            return None
        try:
            return json.loads(payload)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise PublisherError("Registry response is not valid bounded JSON") from exc

    def post_empty(self, *, path: str) -> None:
        self.request_bytes(method="POST", path=path, maximum=MAX_CONTROL_BYTES)

    def _send_bounded(self, connection: RegistryHttpConnection, payload: bytes) -> None:
        if connection.sock is None:
            raise PublisherError("Registry connection did not expose a bounded socket")
        connection.sock.settimeout(min(self._request_timeout, self.remaining()))
        connection.send(payload)
        self.remaining()

    def upload_distribution(
        self,
        *,
        path: str,
        username: str,
        artifact: Path,
        fields: Mapping[str, str],
    ) -> None:
        if not path.startswith("/") or any(character in path for character in "\r\n"):
            raise PublisherError("Registry upload path is invalid")
        details = artifact.lstat()
        if artifact.is_symlink() or not stat.S_ISREG(details.st_mode):
            raise PublisherError("Upload artifact must be a regular file")
        if not 0 < details.st_size <= MAX_DISTRIBUTION_BYTES:
            raise PublisherError("Upload artifact size is outside policy")
        boundary = f"proxmox-sdk-{os.urandom(24).hex()}"
        prefix = _multipart_prefix(boundary, fields, artifact.name)
        suffix = f"\r\n--{boundary}--\r\n".encode()
        authorization = base64.b64encode(f"{username}:{self._token}".encode("ascii")).decode(
            "ascii"
        )
        headers = {
            "Accept": "application/json",
            "Authorization": f"Basic {authorization}",
            "Content-Length": str(len(prefix) + details.st_size + len(suffix)),
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "User-Agent": "proxmox-sdk-actions-publisher/1",
        }
        connection = self._connection_factory(
            self._host,
            min(self._request_timeout, self.remaining()),
        )
        try:
            connection.putrequest("POST", path)
            for key, value in headers.items():
                connection.putheader(key, value)
            connection.endheaders()
            self._send_bounded(connection, prefix)
            with artifact.open("rb") as handle:
                for chunk in iter(lambda: handle.read(64 * 1024), b""):
                    self._send_bounded(connection, chunk)
            self._send_bounded(connection, suffix)
            response = connection.getresponse()
            status = int(response.status)
            if 300 <= status < 400:
                raise PublisherError("Registry redirect was refused")
            if not 200 <= status < 300:
                raise PublisherError(f"Registry upload failed with HTTP {status}")
            self._read_bounded(response, connection, MAX_CONTROL_BYTES)
        except PublisherError:
            raise
        except ValueError:
            raise PublisherError("Registry request headers are invalid") from None
        except (TimeoutError, http.client.HTTPException, OSError) as exc:
            raise PublisherError("Registry upload failed or timed out") from exc
        finally:
            connection.close()


def _registry_quote(value: str) -> str:
    if not value or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", value) is None:
        raise PublisherError("Registry identity contains unsupported characters")
    return urllib.parse.quote(value, safe="")


def _repository_identity(payload: Any) -> str | None:
    package = _object(payload, "registry package metadata")
    repository = package.get("repository")
    if repository is None:
        return None
    value = _object(repository, "registry repository association").get("full_name")
    if not isinstance(value, str) or value.count("/") != 1:
        raise PublisherError("Registry repository association is incomplete")
    return value


def _candidate_registry_artifacts(candidate: VerifiedCandidate) -> tuple[RegistryArtifact, ...]:
    records: list[RegistryArtifact] = []
    for name, path in sorted(candidate.distributions.items()):
        try:
            details = path.lstat()
        except OSError as exc:
            raise PublisherError("Sealed distribution is unavailable") from exc
        if path.is_symlink() or not stat.S_ISREG(details.st_mode):
            raise PublisherError("Sealed distribution is not a regular file")
        if not 0 < details.st_size <= MAX_DISTRIBUTION_BYTES:
            raise PublisherError("Sealed distribution size is outside policy")
        records.append(RegistryArtifact(name, details.st_size, _sha256(path)))
    if len(records) != 2:
        raise PublisherError("Sealed candidate must contain exactly two distributions")
    return tuple(records)


def _distribution_upload_fields(artifact: Path, metadata: Mapping[str, str]) -> dict[str, str]:
    return {
        ":action": "file_upload",
        "protocol_version": "1",
        "name": metadata["name"],
        "version": metadata["version"],
        "metadata_version": metadata["metadata_version"],
        "summary": metadata["summary"],
        "requires_python": metadata["requires_python"],
        "license": metadata["license"],
        "author": metadata["author"],
        "home_page": metadata["home_page"],
        "filetype": metadata["filetype"],
        "pyversion": metadata["pyversion"],
        "sha256_digest": _sha256(artifact),
    }


class ActionsGiteaRegistry:
    """An exact-state view of Gitea package metadata and served files."""

    def __init__(
        self, client: BoundedRegistryClient, owner: str, repository: str, username: str
    ) -> None:
        self.client = client
        self.owner = _registry_quote(owner)
        self.repository = _registry_quote(repository)
        self.username = _registry_quote(username)

    @property
    def expected_repository(self) -> str:
        return f"{urllib.parse.unquote(self.owner)}/{urllib.parse.unquote(self.repository)}"

    def _package_path(self, candidate: VerifiedCandidate) -> str:
        return (
            f"/api/v1/packages/{self.owner}/pypi/"
            f"{_registry_quote(EXPECTED_PACKAGE)}/{_registry_quote(candidate.version)}"
        )

    def _download_exact(self, candidate: VerifiedCandidate, expected: RegistryArtifact) -> None:
        path = (
            f"/api/packages/{self.owner}/pypi/files/{_registry_quote(EXPECTED_PACKAGE)}/"
            f"{_registry_quote(candidate.version)}/{_registry_quote(expected.name)}"
        )
        content = self.client.request_bytes(method="GET", path=path, maximum=expected.size)
        if content is None:
            raise PublisherError("Registry artifact download unexpectedly disappeared")
        actual = RegistryArtifact(expected.name, len(content), hashlib.sha256(content).hexdigest())
        if actual != expected:
            raise PublisherError("Registry artifact bytes do not match their API provenance")

    def _version_repository(
        self, candidate: VerifiedCandidate, package_payload: Any | None
    ) -> str | None:
        if package_payload is None:
            latest = (
                f"/api/v1/packages/{self.owner}/pypi/{_registry_quote(EXPECTED_PACKAGE)}/-/latest"
            )
            latest_payload = self.client.request_json(path=latest, allow_not_found=True)
            return _repository_identity(latest_payload) if latest_payload is not None else None
        package = _object(package_payload, "registry package metadata")
        identity = (
            str(package.get("type", "")),
            _canonical_name(str(package.get("name", ""))),
            str(package.get("version", "")),
        )
        if identity != ("pypi", _canonical_name(EXPECTED_PACKAGE), candidate.version):
            raise PublisherError("Registry package metadata identity mismatch")
        return _repository_identity(package)

    def _file_record(
        self,
        row: Any,
        expected: Mapping[str, RegistryArtifact],
        seen: set[str],
        candidate: VerifiedCandidate,
    ) -> RegistryArtifact:
        item = _object(row, "registry file inventory entry")
        name, size, digest = item.get("name"), item.get("size"), item.get("sha256")
        if (
            not isinstance(name, str)
            or re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._+-]*", name) is None
            or name in seen
            or isinstance(size, bool)
            or not isinstance(size, int)
            or not 0 <= size <= MAX_DISTRIBUTION_BYTES
            or not isinstance(digest, str)
            or HEX64.fullmatch(digest.lower()) is None
        ):
            raise PublisherError("Registry file inventory identity is invalid")
        seen.add(name)
        record = RegistryArtifact(name, size, digest.lower())
        if expected.get(name) == record:
            self._download_exact(candidate, record)
        return record

    def inspect(self, candidate: VerifiedCandidate) -> RegistryState:
        package_path = self._package_path(candidate)
        package_payload = self.client.request_json(path=package_path, allow_not_found=True)
        version_exists = package_payload is not None
        repository = self._version_repository(candidate, package_payload)
        files_payload = self.client.request_json(path=f"{package_path}/files", allow_not_found=True)
        if files_payload is None:
            if version_exists:
                raise PublisherError("Registry package version exists without a file inventory")
            return RegistryState(False, repository, ())
        if not version_exists or not isinstance(files_payload, list):
            raise PublisherError("Registry file inventory is inconsistent")
        expected = {record.name: record for record in _candidate_registry_artifacts(candidate)}
        records: list[RegistryArtifact] = []
        seen: set[str] = set()
        for row in files_payload:
            records.append(self._file_record(row, expected, seen, candidate))
        return RegistryState(True, repository, tuple(sorted(records, key=lambda item: item.name)))

    def link(self) -> None:
        path = (
            f"/api/v1/packages/{self.owner}/pypi/{_registry_quote(EXPECTED_PACKAGE)}"
            f"/-/link/{self.repository}"
        )
        self.client.post_empty(path=path)

    def upload(self, candidate: VerifiedCandidate, artifact: Path) -> None:
        expected = candidate.distributions.get(artifact.name)
        if expected is None or expected.resolve() != artifact.resolve():
            raise PublisherError("Upload artifact is not part of the sealed candidate")
        path = f"/api/packages/{self.owner}/pypi/"
        fields = _distribution_upload_fields(artifact, candidate.metadata[artifact.name])
        self.client.upload_distribution(
            path=path,
            username=urllib.parse.unquote(self.username),
            artifact=artifact,
            fields=fields,
        )


def classify_registry_state(state: RegistryState, candidate: VerifiedCandidate) -> str:
    """Accept absent, exact, or byte-exact resumable subset states."""

    local = {record.name: record for record in _candidate_registry_artifacts(candidate)}
    remote = state.artifact_map()
    if not state.version_exists:
        if remote:
            raise PublisherError("Registry version state is inconsistent")
        return "absent"
    if set(remote) - set(local):
        raise PublisherError("Registry version contains unexpected extra artifacts")
    if any(remote[name] != local[name] for name in remote):
        raise PublisherError("Registry artifact size or digest mismatch")
    return "exact" if set(remote) == set(local) else "partial"


def _require_repository_association(state: RegistryState, expected: str) -> None:
    if state.repository is not None and state.repository != expected:
        raise PublisherError("Package is associated with a different repository")


def _inspect_actions_registry(
    candidate: VerifiedCandidate, registry: ActionsGiteaRegistry
) -> tuple[RegistryState, str]:
    state = registry.inspect(candidate)
    _require_repository_association(state, registry.expected_repository)
    return state, classify_registry_state(state, candidate)


def _ensure_actions_repository(
    candidate: VerifiedCandidate,
    registry: ActionsGiteaRegistry,
    state: RegistryState,
) -> RegistryState:
    if state.repository == registry.expected_repository or not state.version_exists:
        return state
    try:
        registry.link()
    except Exception:
        pass
    recovered, _ = _inspect_actions_registry(candidate, registry)
    if recovered.repository != registry.expected_repository:
        raise PublisherError("Repository association did not reach an exact state")
    return recovered


def _upload_actions_artifact(
    *,
    candidate: VerifiedCandidate,
    registry: ActionsGiteaRegistry,
    artifact: Path,
    revalidate_seal: Callable[[], None],
) -> RegistryState:
    revalidate_seal()
    try:
        registry.upload(candidate, artifact)
    except Exception:
        revalidate_seal()
        recovered, _ = _inspect_actions_registry(candidate, registry)
        if artifact.name not in recovered.artifact_map():
            raise PublisherError("Registry upload made no exact recoverable progress") from None
        return _ensure_actions_repository(candidate, registry, recovered)
    revalidate_seal()
    state, _ = _inspect_actions_registry(candidate, registry)
    if state.artifact_map().get(artifact.name) not in _candidate_registry_artifacts(candidate):
        raise PublisherError("Registry upload did not preserve the uploaded artifact")
    return _ensure_actions_repository(candidate, registry, state)


def reconcile_actions_publication(
    *,
    candidate: VerifiedCandidate,
    registry: ActionsGiteaRegistry,
    revalidate_seal: Callable[[], None],
) -> tuple[str, RegistryState]:
    """Resume exact subsets one file at a time and require an exact final GET."""

    revalidate_seal()
    state, initial = _inspect_actions_registry(candidate, registry)
    state = _ensure_actions_repository(candidate, registry, state)
    for record in _candidate_registry_artifacts(candidate):
        if record.name in state.artifact_map():
            continue
        state = _upload_actions_artifact(
            candidate=candidate,
            registry=registry,
            artifact=candidate.distributions[record.name],
            revalidate_seal=revalidate_seal,
        )
    revalidate_seal()
    final_state, classification = _inspect_actions_registry(candidate, registry)
    if final_state.repository != registry.expected_repository:
        raise PublisherError("Package repository association is missing")
    if classification != "exact":
        raise PublisherError("Final registry state is not exact")
    result = "already exact" if initial == "exact" else "published exact"
    return result, final_state


def publish_verified_candidate(
    candidate: VerifiedCandidate, registry: PackageRegistry
) -> tuple[str, RegistryState]:
    """Idempotently upload missing files and require exact served bytes."""

    expected = {name: _sha256(path) for name, path in candidate.distributions.items()}
    remote = registry.inspect(EXPECTED_PACKAGE, candidate.version)
    unexpected = set(remote) - set(expected)
    mismatched = {name for name in set(remote) & set(expected) if remote[name] != expected[name]}
    if unexpected or mismatched:
        raise PublisherError("Existing registry release has unexpected or mismatched bytes")
    for name in sorted(set(expected) - set(remote)):
        registry.upload(candidate.distributions[name], candidate.metadata[name])
    served = registry.inspect(EXPECTED_PACKAGE, candidate.version)
    if served != expected:
        raise PublisherError("Served package bytes do not exactly match the verified candidate")
    artifacts = tuple(
        RegistryArtifact(name, candidate.distributions[name].stat().st_size, digest)
        for name, digest in sorted(served.items())
    )
    result = "already exact" if remote == expected else "published exact"
    return result, RegistryState(True, None, artifacts)


def _canonical_json_bytes(value: Mapping[str, Any]) -> bytes:
    return (json.dumps(value, separators=(",", ":"), sort_keys=True) + "\n").encode("utf-8")


def _write_seal_manifest(candidate: VerifiedCandidate, staging: Path) -> str:
    files = {
        path.relative_to(staging).as_posix(): _sha256(path)
        for path in staging.rglob("*")
        if path.is_file()
    }
    manifest = {
        "schema_version": 1,
        "files": dict(sorted(files.items())),
        "run_attempt": candidate.run_attempt,
        "run_id": candidate.run_id,
        "source_sha": candidate.source_sha,
        "tag": candidate.tag,
        "version": candidate.version,
    }
    path = staging / SEAL_MANIFEST_NAME
    path.write_bytes(_canonical_json_bytes(manifest))
    path.chmod(0o600)
    return _sha256(path)


def write_verified_staging(candidate: VerifiedCandidate, staging: Path) -> str:
    """Write a closed handoff and return its canonical seal-manifest digest."""

    staging.mkdir(mode=0o700, parents=False)
    dist = staging / "dist"
    dist.mkdir(mode=0o700)
    files: dict[str, str] = {}
    for name, source in sorted(candidate.distributions.items()):
        target = dist / name
        shutil.copyfile(source, target)
        target.chmod(0o600)
        files[f"dist/{name}"] = _sha256(target)
    controls = {
        "distribution-manifest.json": candidate.distribution_manifest,
        "gitea-provenance.json": candidate.gitea_provenance,
    }
    for name, source in controls.items():
        target = staging / name
        shutil.copyfile(source, target)
        target.chmod(0o600)
        files[name] = _sha256(target)
    handoff = {
        "schema_version": 1,
        "artifact_name": candidate.artifact_name,
        "candidate_sha256": candidate.candidate_sha256,
        "distribution_manifest_sha256": candidate.distribution_manifest_sha256,
        "gitea_provenance_sha256": candidate.gitea_provenance_sha256,
        "file_sha256": files,
        "metadata": candidate.metadata,
        "run_attempt": candidate.run_attempt,
        "run_id": candidate.run_id,
        "source_sha": candidate.source_sha,
        "tag": candidate.tag,
        "version": candidate.version,
    }
    handoff_path = staging / "handoff.json"
    handoff_path.write_text(json.dumps(handoff, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    handoff_path.chmod(0o600)
    return _write_seal_manifest(candidate, staging)


def _load_handoff_json(directory: Path) -> dict[str, Any]:
    try:
        path = directory / "handoff.json"
        details = path.lstat()
        if path.is_symlink() or not stat.S_ISREG(details.st_mode):
            raise PublisherError("Verified handoff is not a regular file")
        if not 0 < details.st_size <= MAX_HANDOFF_BYTES:
            raise PublisherError("Verified handoff exceeds its size limit")
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PublisherError("Verified handoff is unavailable or malformed") from exc
    handoff = _object(value, "verified handoff")
    required = {
        "schema_version",
        "artifact_name",
        "candidate_sha256",
        "distribution_manifest_sha256",
        "gitea_provenance_sha256",
        "file_sha256",
        "metadata",
        "run_attempt",
        "run_id",
        "source_sha",
        "tag",
        "version",
    }
    if set(handoff) != required or handoff.get("schema_version") != 1:
        raise PublisherError("Verified handoff field set is invalid")
    return handoff


def _validate_actions_seal_directories(sealed: Path) -> None:
    directories = {
        path.relative_to(sealed).as_posix() for path in sealed.rglob("*") if path.is_dir()
    }
    if directories != {"dist"}:
        raise PublisherError("Actions seal does not contain its exact directory set")


def _validate_handoff_files(directory: Path, handoff: Mapping[str, Any]) -> dict[str, Path]:
    hashes = handoff.get("file_sha256")
    if not isinstance(hashes, dict):
        raise PublisherError("Verified handoff file map is invalid")
    relative_files = {
        path.relative_to(directory).as_posix() for path in directory.rglob("*") if path.is_file()
    }
    if relative_files != {*hashes, "handoff.json", SEAL_MANIFEST_NAME}:
        raise PublisherError("Verified handoff does not contain its exact closed file set")
    result = _rehash_handoff_files(directory, hashes)
    distribution_names = {
        name for name in result if name.startswith("dist/") and len(PurePosixPath(name).parts) == 2
    }
    if len(distribution_names) != 2 or set(result) != {
        *distribution_names,
        "distribution-manifest.json",
        "gitea-provenance.json",
    }:
        raise PublisherError("Verified handoff has an invalid distribution/control set")
    return result


def _rehash_handoff_files(directory: Path, hashes: Mapping[Any, Any]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for name, digest in hashes.items():
        path = PurePosixPath(str(name))
        if path.is_absolute() or ".." in path.parts or not isinstance(digest, str):
            raise PublisherError("Verified handoff contains an unsafe file identity")
        target = directory.joinpath(*path.parts)
        if HEX64.fullmatch(digest) is None or _sha256(target) != digest:
            raise PublisherError("Verified handoff file digest mismatch")
        result[str(name)] = target
    return result


def _load_seal_manifest(sealed: Path) -> tuple[dict[str, Any], bytes]:
    path = sealed / SEAL_MANIFEST_NAME
    try:
        details = path.lstat()
        if path.is_symlink() or not stat.S_ISREG(details.st_mode):
            raise PublisherError("Actions seal manifest is not a regular file")
        if not 0 < details.st_size <= MAX_HANDOFF_BYTES:
            raise PublisherError("Actions seal manifest exceeds its size limit")
        raw = path.read_bytes()
        manifest = _object(json.loads(raw), "Actions seal manifest")
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise PublisherError("Actions seal manifest is unavailable or malformed") from exc
    if raw != _canonical_json_bytes(manifest):
        raise PublisherError("Actions seal manifest is not canonical JSON")
    return manifest, raw


def _validate_seal_manifest_files(sealed: Path, manifest: Mapping[str, Any]) -> None:
    hashes = manifest.get("files")
    if not isinstance(hashes, dict):
        raise PublisherError("Actions seal manifest file map is invalid")
    relative_files = {
        path.relative_to(sealed).as_posix() for path in sealed.rglob("*") if path.is_file()
    }
    if relative_files != {*hashes, SEAL_MANIFEST_NAME}:
        raise PublisherError("Actions seal manifest does not cover the exact file set")
    for name, digest in hashes.items():
        relative = PurePosixPath(str(name))
        if relative.is_absolute() or ".." in relative.parts or not isinstance(digest, str):
            raise PublisherError("Actions seal manifest contains an unsafe file identity")
        target = sealed.joinpath(*relative.parts)
        if HEX64.fullmatch(digest) is None or _sha256(target) != digest:
            raise PublisherError("Actions seal manifest file digest mismatch")


def verify_actions_seal_manifest(
    sealed: Path,
    *,
    expected_sha256: str,
    source_sha: str,
    run_id: int,
    run_attempt: int,
    tag: str,
    version: str,
) -> str:
    """Verify the externally carried digest and all canonical seal identities."""

    manifest, raw = _load_seal_manifest(sealed)
    actual_sha256 = hashlib.sha256(raw).hexdigest()
    if HEX64.fullmatch(expected_sha256) is None or actual_sha256 != expected_sha256:
        raise PublisherError("Actions seal manifest digest does not match verifier output")
    expected = {
        "schema_version": 1,
        "run_attempt": run_attempt,
        "run_id": run_id,
        "source_sha": source_sha,
        "tag": tag,
        "version": version,
    }
    if set(manifest) != {*expected, "files"}:
        raise PublisherError("Actions seal manifest field set is invalid")
    for key, value in expected.items():
        _require_equal(manifest.get(key), value, f"seal manifest {key}")
    _validate_seal_manifest_files(sealed, manifest)
    return actual_sha256


def seal_verified_staging(staging: Path, sealed: Path) -> None:
    """As root, validate and atomically convert staging into immutable handoff bytes."""

    if os.geteuid() != 0:
        raise PublisherError("Only root may seal a verified handoff")
    try:
        if not stat.S_ISDIR(staging.lstat().st_mode):
            raise PublisherError("Verified staging is not a real directory")
        if any(path.is_symlink() for path in staging.rglob("*")):
            raise PublisherError("Verified staging contains a symlink")
    except OSError as exc:
        raise PublisherError("Verified staging cannot be inspected safely") from exc
    handoff = _load_handoff_json(staging)
    _validate_handoff_files(staging, handoff)
    sealed.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    if sealed.exists():
        raise PublisherError("A sealed handoff already exists for this run")
    temporary = Path(tempfile.mkdtemp(prefix=f".{sealed.name}.", dir=sealed.parent))
    try:
        shutil.copytree(staging, temporary / "payload", dirs_exist_ok=False)
        payload = temporary / "payload"
        for path in payload.rglob("*"):
            if path.is_symlink():
                raise PublisherError("Verified handoff contains a symlink")
            os.chown(path, 0, 0)
            path.chmod(0o500 if path.is_dir() else 0o400)
        os.replace(payload, sealed)
        os.chown(sealed, 0, 0)
        sealed.chmod(0o500)
    finally:
        shutil.rmtree(temporary, ignore_errors=True)


def _candidate_from_handoff(sealed: Path) -> VerifiedCandidate:
    handoff = _load_handoff_json(sealed)
    files = _validate_handoff_files(sealed, handoff)
    metadata = handoff.get("metadata")
    if not isinstance(metadata, dict):
        raise PublisherError("Verified handoff metadata is invalid")
    distributions = {
        PurePosixPath(name).name: path for name, path in files.items() if name.startswith("dist/")
    }
    if set(metadata) != set(distributions):
        raise PublisherError("Verified handoff metadata set differs from distributions")
    checked_metadata: dict[str, dict[str, str]] = {}
    for name, value in metadata.items():
        if not isinstance(value, dict) or any(
            not isinstance(key, str) or not isinstance(item, str) for key, item in value.items()
        ):
            raise PublisherError("Verified handoff distribution metadata is invalid")
        checked_metadata[str(name)] = {str(key): str(item) for key, item in value.items()}
    scalar_types = {
        "artifact_name": str,
        "candidate_sha256": str,
        "distribution_manifest_sha256": str,
        "gitea_provenance_sha256": str,
        "run_attempt": int,
        "run_id": int,
        "source_sha": str,
        "tag": str,
        "version": str,
    }
    if any(not isinstance(handoff[key], kind) for key, kind in scalar_types.items()):
        raise PublisherError("Verified handoff scalar identity is invalid")
    if _sha256(files["distribution-manifest.json"]) != handoff["distribution_manifest_sha256"]:
        raise PublisherError("Canonical distribution manifest digest differs from handoff")
    if _sha256(files["gitea-provenance.json"]) != handoff["gitea_provenance_sha256"]:
        raise PublisherError("Gitea provenance digest differs from handoff")
    return VerifiedCandidate(
        artifact_name=handoff["artifact_name"],
        candidate_sha256=handoff["candidate_sha256"],
        distributions=distributions,
        metadata=checked_metadata,
        run_attempt=handoff["run_attempt"],
        run_id=handoff["run_id"],
        source_sha=handoff["source_sha"],
        tag=handoff["tag"],
        version=handoff["version"],
        distribution_manifest_sha256=handoff["distribution_manifest_sha256"],
        gitea_provenance_sha256=handoff["gitea_provenance_sha256"],
        distribution_manifest=files["distribution-manifest.json"],
        gitea_provenance=files["gitea-provenance.json"],
    )


def load_sealed_candidate(sealed: Path) -> VerifiedCandidate:
    """Rehash and load a root-owned handoff without any Gitea subprocess."""

    details = sealed.lstat()
    if not stat.S_ISDIR(details.st_mode) or details.st_uid != 0 or details.st_mode & 0o022:
        raise PublisherError("Verified handoff directory is not root-sealed")
    for path in sealed.rglob("*"):
        details = path.lstat()
        if stat.S_ISLNK(details.st_mode) or details.st_uid != 0 or details.st_mode & 0o022:
            raise PublisherError("Verified handoff member is not root-sealed")
    return _candidate_from_handoff(sealed)


def _require_actions_candidate_identity(
    candidate: VerifiedCandidate,
    *,
    source_sha: str,
    run_id: int,
    run_attempt: int,
    tag: str,
    version: str,
) -> None:
    expected = (source_sha, run_id, run_attempt, tag, version)
    actual = (
        candidate.source_sha,
        candidate.run_id,
        candidate.run_attempt,
        candidate.tag,
        candidate.version,
    )
    _require_equal(actual, expected, "Actions sealed candidate identity")


def harden_actions_seal(
    sealed: Path,
    *,
    expected_sha256: str,
    source_sha: str,
    run_id: int,
    run_attempt: int,
    tag: str,
    version: str,
) -> VerifiedCandidate:
    """Restore private modes after artifact transport and rehash the closed seal."""

    try:
        details = sealed.lstat()
        members = sorted(sealed.rglob("*"), key=lambda path: len(path.parts), reverse=True)
    except OSError as exc:
        raise PublisherError("Downloaded Actions seal is unavailable") from exc
    if sealed.is_symlink() or not stat.S_ISDIR(details.st_mode):
        raise PublisherError("Downloaded Actions seal is not a real directory")
    for path in members:
        details = path.lstat()
        if stat.S_ISLNK(details.st_mode) or not (path.is_file() or path.is_dir()):
            raise PublisherError("Downloaded Actions seal contains an unsafe member")
    _validate_actions_seal_directories(sealed)
    verify_actions_seal_manifest(
        sealed,
        expected_sha256=expected_sha256,
        source_sha=source_sha,
        run_id=run_id,
        run_attempt=run_attempt,
        tag=tag,
        version=version,
    )
    candidate = _candidate_from_handoff(sealed)
    _require_actions_candidate_identity(
        candidate,
        source_sha=source_sha,
        run_id=run_id,
        run_attempt=run_attempt,
        tag=tag,
        version=version,
    )
    for path in members:
        path.chmod(0o500 if path.is_dir() else 0o400)
    sealed.chmod(0o500)
    return candidate


def load_actions_sealed_candidate(
    sealed: Path,
    *,
    expected_sha256: str,
    source_sha: str,
    run_id: int,
    run_attempt: int,
    tag: str,
    version: str,
) -> VerifiedCandidate:
    """Load a read-only Actions seal and require its exact hashes and file set."""

    try:
        details = sealed.lstat()
        members = list(sealed.rglob("*"))
    except OSError as exc:
        raise PublisherError("Downloaded Actions seal is unavailable") from exc
    if sealed.is_symlink() or not stat.S_ISDIR(details.st_mode) or details.st_mode & 0o222:
        raise PublisherError("Downloaded Actions seal is not hardened read-only")
    for path in members:
        details = path.lstat()
        if stat.S_ISLNK(details.st_mode) or details.st_mode & 0o222:
            raise PublisherError("Downloaded Actions seal member is not hardened read-only")
    _validate_actions_seal_directories(sealed)
    verify_actions_seal_manifest(
        sealed,
        expected_sha256=expected_sha256,
        source_sha=source_sha,
        run_id=run_id,
        run_attempt=run_attempt,
        tag=tag,
        version=version,
    )
    candidate = _candidate_from_handoff(sealed)
    _require_actions_candidate_identity(
        candidate,
        source_sha=source_sha,
        run_id=run_id,
        run_attempt=run_attempt,
        tag=tag,
        version=version,
    )
    return candidate


def write_publication_evidence(
    candidate: VerifiedCandidate,
    evidence_path: Path,
    *,
    seal_sha256: str,
    server_url: str,
    owner: str,
    repository: str,
    result: str,
    registry_state: RegistryState,
) -> None:
    """Write non-secret evidence only after exact served bytes are confirmed."""

    if HEX64.fullmatch(seal_sha256) is None:
        raise PublisherError("Publication evidence seal digest is invalid")
    _require_equal(
        (server_url, owner, repository),
        (EXPECTED_SERVER, EXPECTED_OWNER, EXPECTED_REPOSITORY),
        "publication registry identity",
    )
    if classify_registry_state(registry_state, candidate) != "exact":
        raise PublisherError("Publication evidence requires an exact registry state")
    if registry_state.repository not in {None, EXPECTED_FULL_NAME}:
        raise PublisherError("Publication evidence repository association is invalid")
    if result not in {"already exact", "published exact"}:
        raise PublisherError("Publication evidence result is invalid")
    evidence_path.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    evidence_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "artifact_name": candidate.artifact_name,
                "candidate_sha256": candidate.candidate_sha256,
                "distribution_sha256": {
                    name: _sha256(path) for name, path in sorted(candidate.distributions.items())
                },
                "distribution_manifest_sha256": candidate.distribution_manifest_sha256,
                "final_registry_inventory": [
                    {
                        "filename": artifact.name,
                        "sha256": artifact.sha256,
                        "size": artifact.size,
                    }
                    for artifact in sorted(registry_state.artifacts, key=lambda item: item.name)
                ],
                "gitea_provenance_sha256": candidate.gitea_provenance_sha256,
                "owner": owner,
                "repository": repository,
                "repository_association": registry_state.repository,
                "registry_version_exists": registry_state.version_exists,
                "result": result,
                "run_attempt": candidate.run_attempt,
                "run_id": candidate.run_id,
                "seal_sha256": seal_sha256,
                "server_url": server_url,
                "source_sha": candidate.source_sha,
                "tag": candidate.tag,
                "version": candidate.version,
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    evidence_path.chmod(0o600)


def _credential_directory() -> Path:
    value = os.environ.get("CREDENTIALS_DIRECTORY")
    if not value:
        raise PublisherError("CREDENTIALS_DIRECTORY is required; use the hardened systemd unit")
    return Path(value)


def _actions_directory(value: Path | None, environment_name: str, leaf: str) -> Path:
    if value is not None:
        return value.resolve()
    configured = os.environ.get(environment_name)
    if configured:
        return Path(configured).resolve()
    workspace = Path(os.environ.get("GITHUB_WORKSPACE", Path.cwd()))
    return (workspace / ".tmp" / "gitea-package" / leaf).resolve()


def _run_actions_verify(args: argparse.Namespace) -> None:
    inbox = _actions_directory(args.inbox_dir, "PROXMOX_SDK_PUBLISHER_INBOX", "inbox")
    evidence = _actions_directory(args.evidence_dir, "PROXMOX_SDK_PUBLISHER_EVIDENCE", "evidence")
    candidate_tar = (args.candidate_tar or inbox / PAYLOAD_NAME).resolve()
    sealed = (args.sealed_dir or evidence / "sealed").resolve()
    work = (args.work_dir or evidence / "verify-work").resolve()
    if args.event_name != "push":
        raise PublisherError("Actions package verification requires a tag push event")
    candidate = verify_actions_candidate(
        source_root=args.source_root.resolve(),
        interpreter=args.python.resolve(),
        candidate_tar=candidate_tar,
        expected_candidate_sha256=args.candidate_sha256,
        run_id=args.run_id,
        run_attempt=args.run_attempt,
        source_sha=args.source_sha,
        tag=args.tag,
        repository=args.repository,
        server_url=args.server_url,
        work=work,
    )
    sealed.parent.mkdir(mode=0o700, parents=True, exist_ok=True)
    seal_sha256 = write_verified_staging(candidate, sealed)
    try:
        with args.github_output.open("a", encoding="utf-8") as output:
            output.write(f"seal_sha256={seal_sha256}\n")
    except OSError as exc:
        raise PublisherError("Actions output file is unavailable") from exc
    print(f"Verified and sealed {EXPECTED_PACKAGE}=={candidate.version} without credentials")


def _run_actions_harden(args: argparse.Namespace) -> None:
    evidence = _actions_directory(args.evidence_dir, "PROXMOX_SDK_PUBLISHER_EVIDENCE", "evidence")
    sealed = (args.sealed_dir or evidence / "sealed").resolve()
    candidate = harden_actions_seal(
        sealed,
        expected_sha256=args.seal_sha256,
        source_sha=args.source_sha,
        run_id=args.run_id,
        run_attempt=args.run_attempt,
        tag=args.tag,
        version=args.version,
    )
    print(f"Hardened exact Actions seal for {EXPECTED_PACKAGE}=={candidate.version}")


def _run_actions_publish(args: argparse.Namespace) -> None:
    evidence = _actions_directory(args.evidence_dir, "PROXMOX_SDK_PUBLISHER_EVIDENCE", "evidence")
    sealed = (args.sealed_dir or evidence / "sealed").resolve()
    evidence_path = (args.publication_evidence or evidence / "publication.json").resolve()
    token = _validate_package_token(os.environ.get(args.token_env, ""))
    _require_equal(args.server_url, EXPECTED_SERVER, "registry server URL")
    _require_equal(args.owner, EXPECTED_OWNER, "registry owner")
    _require_equal(args.repository, EXPECTED_REPOSITORY, "registry repository")
    _require_equal(args.username, EXPECTED_OWNER, "registry username")
    candidate = load_actions_sealed_candidate(
        sealed,
        expected_sha256=args.seal_sha256,
        source_sha=args.source_sha,
        run_id=args.run_id,
        run_attempt=args.run_attempt,
        tag=args.tag,
        version=args.version,
    )
    client = BoundedRegistryClient(
        server_url=args.server_url,
        token=token,
        deadline_seconds=args.deadline_seconds,
        request_timeout=args.request_timeout,
    )
    registry = ActionsGiteaRegistry(client, args.owner, args.repository, args.username)

    def revalidate() -> None:
        load_actions_sealed_candidate(
            sealed,
            expected_sha256=args.seal_sha256,
            source_sha=args.source_sha,
            run_id=args.run_id,
            run_attempt=args.run_attempt,
            tag=args.tag,
            version=args.version,
        )

    result, final_state = reconcile_actions_publication(
        candidate=candidate,
        registry=registry,
        revalidate_seal=revalidate,
    )
    write_publication_evidence(
        candidate,
        evidence_path,
        seal_sha256=args.seal_sha256,
        server_url=args.server_url,
        owner=args.owner,
        repository=args.repository,
        result=result,
        registry_state=final_state,
    )
    print(f"Published and verified {EXPECTED_PACKAGE}=={candidate.version}: {result}")


def _parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    verify = commands.add_parser("verify")
    verify.add_argument("--run-id", type=int, required=True)
    verify.add_argument("--artifact-zip", type=Path, required=True)
    verify.add_argument("--staging", type=Path, required=True)
    seal = commands.add_parser("seal")
    seal.add_argument("--staging", type=Path, required=True)
    seal.add_argument("--handoff", type=Path, required=True)
    publish = commands.add_parser("publish")
    publish.add_argument("--handoff", type=Path, required=True)
    publish.add_argument("--evidence", type=Path, required=True)
    actions_verify = commands.add_parser("verify-actions")
    actions_verify.add_argument("--source-root", type=Path, required=True)
    actions_verify.add_argument("--python", type=Path, required=True)
    actions_verify.add_argument("--candidate-tar", type=Path)
    actions_verify.add_argument("--candidate-sha256", required=True)
    actions_verify.add_argument("--inbox-dir", type=Path)
    actions_verify.add_argument("--evidence-dir", type=Path)
    actions_verify.add_argument("--sealed-dir", type=Path)
    actions_verify.add_argument("--work-dir", type=Path)
    actions_verify.add_argument("--event-name", required=True)
    actions_verify.add_argument("--run-id", type=int, required=True)
    actions_verify.add_argument("--run-attempt", type=int, required=True)
    actions_verify.add_argument("--source-sha", required=True)
    actions_verify.add_argument("--tag", required=True)
    actions_verify.add_argument("--repository", required=True)
    actions_verify.add_argument("--server-url", required=True)
    actions_verify.add_argument("--github-output", type=Path, required=True)
    actions_harden = commands.add_parser("harden-actions-seal")
    actions_harden.add_argument("--evidence-dir", type=Path)
    actions_harden.add_argument("--sealed-dir", type=Path)
    actions_harden.add_argument("--source-sha", required=True)
    actions_harden.add_argument("--run-id", type=int, required=True)
    actions_harden.add_argument("--run-attempt", type=int, required=True)
    actions_harden.add_argument("--tag", required=True)
    actions_harden.add_argument("--version", required=True)
    actions_harden.add_argument("--seal-sha256", required=True)
    actions_publish = commands.add_parser("publish-actions")
    actions_publish.add_argument("--evidence-dir", type=Path)
    actions_publish.add_argument("--sealed-dir", type=Path)
    actions_publish.add_argument("--publication-evidence", type=Path)
    actions_publish.add_argument("--source-sha", required=True)
    actions_publish.add_argument("--run-id", type=int, required=True)
    actions_publish.add_argument("--run-attempt", type=int, required=True)
    actions_publish.add_argument("--tag", required=True)
    actions_publish.add_argument("--version", required=True)
    actions_publish.add_argument("--seal-sha256", required=True)
    actions_publish.add_argument("--server-url", required=True)
    actions_publish.add_argument("--owner", required=True)
    actions_publish.add_argument("--repository", required=True)
    actions_publish.add_argument("--username", required=True)
    actions_publish.add_argument("--token-env", default="PACKAGE_WRITE_TOKEN")
    actions_publish.add_argument("--deadline-seconds", type=float, default=180.0)
    actions_publish.add_argument("--request-timeout", type=float, default=15.0)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the hardened host publisher command."""

    args = _parse_args(list(sys.argv[1:] if argv is None else argv))
    if args.command == "verify":
        credentials = _credential_directory()
        with tempfile.TemporaryDirectory(prefix="proxmox-sdk-verifier-") as temporary:
            candidate = verify_candidate(
                NmsGitReader(credentials / "gitea-read.json"),
                policy=load_publisher_policy(credentials / "policy.json"),
                rebuilder=TrustedSourceRebuilder(),
                run_id=args.run_id,
                artifact_zip=args.artifact_zip.resolve(),
                work=Path(temporary),
            )
            write_verified_staging(candidate, args.staging.resolve())
        print(f"Verified {EXPECTED_PACKAGE}=={candidate.version} from run {candidate.run_id}")
    elif args.command == "seal":
        seal_verified_staging(args.staging.resolve(), args.handoff.resolve())
        print("Root-sealed verified package handoff")
    elif args.command == "publish":
        credentials = _credential_directory()
        candidate = load_sealed_candidate(args.handoff.resolve())
        registry = GiteaPackageRegistry(load_registry_credential(credentials / "registry.json"))
        result, final_state = publish_verified_candidate(candidate, registry)
        write_publication_evidence(
            candidate,
            args.evidence.resolve(),
            seal_sha256=_sha256(args.handoff.resolve() / SEAL_MANIFEST_NAME),
            server_url=EXPECTED_SERVER,
            owner=EXPECTED_OWNER,
            repository=EXPECTED_REPOSITORY,
            result=result,
            registry_state=final_state,
        )
        print(
            "Published root-sealed "
            f"{EXPECTED_PACKAGE}=={candidate.version} from run {candidate.run_id} "
            f"at source {candidate.source_sha}"
        )
    elif args.command == "verify-actions":
        _run_actions_verify(args)
    elif args.command == "harden-actions-seal":
        _run_actions_harden(args)
    else:
        _run_actions_publish(args)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except PublisherError as exc:
        print(f"publisher refused: {exc}", file=sys.stderr)
        raise SystemExit(1) from None

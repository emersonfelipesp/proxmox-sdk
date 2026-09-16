"""Security-boundary tests for the host-side Gitea package publisher."""

from __future__ import annotations

import argparse
import base64
import contextlib
import email.policy
import gzip
import hashlib
import http.client
import http.server
import io
import json
import os
import sys
import tarfile
import threading
import traceback
import zipfile
from collections.abc import Callable, Iterator
from email.parser import BytesParser
from pathlib import Path
from types import SimpleNamespace
from typing import Any

import pytest

from tools import gitea_package_publisher as publisher

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.0.15rc5"
SOURCE_SHA = "a" * 40
TAG_OBJECT_SHA = "b" * 40
RUN_ID = 715
RUN_ATTEMPT = 2
ARTIFACT_NAME = f"gitea-dist-{SOURCE_SHA}-{RUN_ID}-{RUN_ATTEMPT}"


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _encoded(value: bytes) -> dict[str, str]:
    return {"encoding": "base64", "content": base64.b64encode(value).decode("ascii")}


def _wheel() -> bytes:
    result = io.BytesIO()
    metadata = (
        "Metadata-Version: 2.4\n"
        "Name: proxmox-sdk\n"
        f"Version: {VERSION}\n"
        "Summary: test package\n"
        "Requires-Python: >=3.11\n\n"
    ).encode()
    with zipfile.ZipFile(result, "w") as archive:
        info = zipfile.ZipInfo(
            f"proxmox_sdk-{VERSION}.dist-info/METADATA",
            date_time=(2020, 1, 1, 0, 0, 0),
        )
        info.external_attr = 0o100644 << 16
        archive.writestr(info, metadata)
    return result.getvalue()


def _sdist(*, roots: tuple[str, ...] = (f"proxmox_sdk-{VERSION}",)) -> bytes:
    """Build a setuptools-shaped sdist: root PKG-INFO plus the egg-info copy."""
    result = io.BytesIO()
    metadata = (
        "Metadata-Version: 2.4\n"
        "Name: proxmox-sdk\n"
        f"Version: {VERSION}\n"
        "Summary: test package\n"
        "Requires-Python: >=3.11\n\n"
    ).encode()
    with gzip.GzipFile(fileobj=result, mode="wb", mtime=0) as compressed:
        with tarfile.open(fileobj=compressed, mode="w") as archive:
            for root in roots:
                for name in (f"{root}/PKG-INFO", f"{root}/proxmox_sdk.egg-info/PKG-INFO"):
                    info = tarfile.TarInfo(name)
                    info.size = len(metadata)
                    info.mtime = 0
                    archive.addfile(info, io.BytesIO(metadata))
    return result.getvalue()


def _artifact_zip(
    tmp_path: Path,
    *,
    checksum_override: str | None = None,
    manifest_override: dict[str, Any] | None = None,
    provenance_override: dict[str, Any] | None = None,
    extra_member: str | None = None,
) -> tuple[Path, str]:
    workflow = (ROOT / publisher.EXPECTED_WORKFLOW_PATH).read_bytes()
    wheel_name = f"proxmox_sdk-{VERSION}-py3-none-any.whl"
    sdist_name = f"proxmox_sdk-{VERSION}.tar.gz"
    distributions = {wheel_name: _wheel(), sdist_name: _sdist()}
    artifacts = {name: _sha256_bytes(value) for name, value in distributions.items()}
    manifest: dict[str, Any] = {
        "algorithm": "sha256",
        "artifacts": artifacts,
        "source_date_epoch": 1_786_120_800,
        "source_sha": SOURCE_SHA,
        "version": VERSION,
    }
    if manifest_override:
        manifest.update(manifest_override)
    manifest_bytes = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
    provenance: dict[str, Any] = {
        "artifact_name": ARTIFACT_NAME,
        "distribution_manifest_sha256": _sha256_bytes(manifest_bytes),
        "event": "push",
        "ref": f"refs/tags/v{VERSION}",
        "repository": publisher.EXPECTED_FULL_NAME,
        "run_attempt": RUN_ATTEMPT,
        "run_id": RUN_ID,
        "schema_version": 1,
        "server_url": publisher.EXPECTED_SERVER,
        "source_sha": SOURCE_SHA,
        "tag": f"v{VERSION}",
        "version": VERSION,
        "workflow_name": publisher.EXPECTED_WORKFLOW_NAME,
        "workflow_path": publisher.EXPECTED_WORKFLOW_PATH,
        "workflow_sha256": _sha256_bytes(workflow),
    }
    if provenance_override:
        provenance.update(provenance_override)
    provenance_bytes = (json.dumps(provenance, indent=2, sort_keys=True) + "\n").encode()
    checksums = "".join(f"{artifacts[name]}  dist/{name}\n" for name in sorted(artifacts)).encode()
    if checksum_override is not None:
        checksums = checksum_override.encode()

    payload = tmp_path / publisher.PAYLOAD_NAME
    with tarfile.open(payload, "w") as archive:
        members = {
            **{f"dist/{name}": value for name, value in distributions.items()},
            "release-artifacts/distribution-manifest.json": manifest_bytes,
            "release-artifacts/gitea-provenance.json": provenance_bytes,
            "release-artifacts/SHA256SUMS": checksums,
        }
        if extra_member:
            members[extra_member] = b"untrusted"
        for name, value in members.items():
            info = tarfile.TarInfo(name)
            info.size = len(value)
            archive.addfile(info, io.BytesIO(value))

    artifact = tmp_path / f"{ARTIFACT_NAME}.zip"
    with zipfile.ZipFile(artifact, "w") as archive:
        archive.write(payload, publisher.PAYLOAD_NAME)
    return artifact, publisher._sha256(payload)


class FakeGitea:
    def __init__(self, candidate_digest: str) -> None:
        prefix = f"/repos/{publisher.EXPECTED_FULL_NAME}"
        workflow = (ROOT / publisher.EXPECTED_WORKFLOW_PATH).read_bytes()
        pyproject = (ROOT / "pyproject.toml").read_bytes()
        run = {
            "id": RUN_ID,
            "path": f"{publisher.EXPECTED_WORKFLOW_ID}@refs/tags/v{VERSION}",
            "event": "push",
            "status": "completed",
            "conclusion": "success",
            "repository": {"full_name": publisher.EXPECTED_FULL_NAME},
            "head_repository": {"full_name": publisher.EXPECTED_FULL_NAME},
            "head_sha": SOURCE_SHA,
            "head_branch": "",
            "run_attempt": 0,
            "started_at": "2026-08-07T16:40:00Z",
        }
        self.values: dict[str, Any] = {
            prefix: {
                "full_name": publisher.EXPECTED_FULL_NAME,
                "clone_url": f"{publisher.EXPECTED_SERVER}/{publisher.EXPECTED_FULL_NAME}.git",
            },
            f"{prefix}/actions/runs/{RUN_ID}": run,
            f"{prefix}/actions/workflows/{publisher.EXPECTED_WORKFLOW_ID}": {
                "id": publisher.EXPECTED_WORKFLOW_ID,
                "name": publisher.EXPECTED_WORKFLOW_NAME,
                "path": publisher.EXPECTED_WORKFLOW_PATH,
                "state": "active",
            },
            f"{prefix}/actions/runs/{RUN_ID}/jobs": {
                "jobs": [
                    {
                        "id": 911,
                        "run_id": RUN_ID,
                        "run_attempt": RUN_ATTEMPT,
                        "head_sha": SOURCE_SHA,
                        "head_branch": "",
                        "status": "completed",
                        "conclusion": "success",
                        "name": publisher.EXPECTED_JOB_NAME,
                        "labels": [publisher.EXPECTED_RUNNER_LABEL],
                        "runner_id": 47,
                    }
                ]
            },
            f"{prefix}/tags/v{VERSION}": {
                "name": f"v{VERSION}",
                "id": TAG_OBJECT_SHA,
                "commit": {"sha": SOURCE_SHA},
            },
            f"{prefix}/git/tags/{TAG_OBJECT_SHA}": {
                "tag": f"v{VERSION}",
                "sha": TAG_OBJECT_SHA,
                "object": {"type": "commit", "sha": SOURCE_SHA},
            },
            f"{prefix}/tag_protections": [
                {
                    "id": 1,
                    "name_pattern": "v*",
                    "whitelist_usernames": [publisher.EXPECTED_OWNER],
                    "whitelist_teams": [],
                    "created_at": "2026-08-01T00:00:00Z",
                    "updated_at": "2026-08-01T00:00:00Z",
                }
            ],
            f"{prefix}/compare/main...{SOURCE_SHA}": {"total_commits": 0, "commits": []},
            f"{prefix}/commits/{SOURCE_SHA}": {
                "commit": {"committer": {"date": "2026-08-07T16:40:00Z"}}
            },
            f"{prefix}/contents/pyproject.toml?ref={SOURCE_SHA}": _encoded(pyproject),
            f"{prefix}/contents/{publisher.EXPECTED_WORKFLOW_PATH}?ref={SOURCE_SHA}": _encoded(
                workflow
            ),
        }
        self.bytes = {
            f"{prefix}/actions/jobs/911/logs": (
                "2026-08-07T16:41:00.1234567Z "
                f"PROXMOX_SDK_ARTIFACT_NAME={ARTIFACT_NAME}\n"
                "2026-08-07T16:41:00.2345678Z "
                f"PROXMOX_SDK_CANDIDATE_SHA256={candidate_digest}\n"
            ).encode()
        }
        self.events: list[str] = []

    def get_json(self, path: str) -> Any:
        self.events.append(f"json:{path}")
        return self.values[path]

    def get_bytes(self, path: str) -> bytes:
        self.events.append(f"bytes:{path}")
        return self.bytes[path]


class FakeRegistry:
    def __init__(self, events: list[str]) -> None:
        self.events = events
        self.remote: dict[str, str] = {}
        self.uploaded: list[str] = []

    def inspect(self, package: str, version: str) -> dict[str, str]:
        self.events.append("registry:inspect")
        assert package == publisher.EXPECTED_PACKAGE
        assert version == VERSION
        return dict(self.remote)

    def upload(self, artifact: Path, metadata: dict[str, str]) -> None:
        self.events.append("registry:upload")
        assert metadata["name"] == publisher.EXPECTED_PACKAGE
        assert metadata["version"] == VERSION
        self.remote[artifact.name] = publisher._sha256(artifact)
        self.uploaded.append(artifact.name)


class FakeRebuilder:
    def __init__(self, events: list[str], *, malicious: bool = False) -> None:
        self.events = events
        self.malicious = malicious

    def rebuild(
        self,
        client: publisher.GiteaReader,
        *,
        source_sha: str,
        source_date_epoch: int,
        work: Path,
    ) -> dict[str, Path]:
        del client
        self.events.append("trusted:rebuild")
        assert source_sha == SOURCE_SHA
        assert source_date_epoch == 1_786_120_800
        output = work / "trusted-test-build"
        output.mkdir()
        values = {
            f"proxmox_sdk-{VERSION}-py3-none-any.whl": _wheel(),
            f"proxmox_sdk-{VERSION}.tar.gz": _sdist(),
        }
        if self.malicious:
            values[f"proxmox_sdk-{VERSION}-py3-none-any.whl"] += b"malicious-runner"
        result = {}
        for name, value in values.items():
            path = output / name
            path.write_bytes(value)
            result[name] = path
        return result


def _publish(
    tmp_path: Path,
    client: FakeGitea,
    artifact: Path,
    events: list[str],
) -> tuple[publisher.VerifiedCandidate, FakeRegistry]:
    candidate = publisher.verify_candidate(
        client,
        policy=publisher.PublisherPolicy(1, (publisher.EXPECTED_OWNER,), ()),
        rebuilder=FakeRebuilder(events),
        run_id=RUN_ID,
        artifact_zip=artifact,
        work=tmp_path / "verify-work",
    )
    events.append("credential:load")
    registry = FakeRegistry(events)
    result, final_state = publisher.publish_verified_candidate(candidate, registry)
    publisher.write_publication_evidence(
        candidate,
        tmp_path / "evidence.json",
        seal_sha256="c" * 64,
        server_url=publisher.EXPECTED_SERVER,
        owner=publisher.EXPECTED_OWNER,
        repository=publisher.EXPECTED_REPOSITORY,
        result=result,
        registry_state=final_state,
    )
    return candidate, registry


def test_credentials_are_loaded_only_after_complete_provenance_verification(
    tmp_path: Path,
) -> None:
    artifact, digest = _artifact_zip(tmp_path)
    client = FakeGitea(digest)
    events = client.events

    candidate, registry = _publish(tmp_path, client, artifact, events)

    assert candidate.version == VERSION
    assert set(registry.uploaded) == {
        f"proxmox_sdk-{VERSION}-py3-none-any.whl",
        f"proxmox_sdk-{VERSION}.tar.gz",
    }
    credential_index = events.index("credential:load")
    assert all(
        event.startswith(("json:", "bytes:", "trusted:")) for event in events[:credential_index]
    )
    assert "trusted:rebuild" in events[:credential_index]
    assert events[credential_index + 1 :] == [
        "registry:inspect",
        "registry:upload",
        "registry:upload",
        "registry:inspect",
    ]
    evidence = json.loads((tmp_path / "evidence.json").read_text(encoding="utf-8"))
    assert evidence["candidate_sha256"] == digest
    assert evidence["run_id"] == RUN_ID
    assert "opaque-test-token" not in (tmp_path / "evidence.json").read_text(encoding="utf-8")


@pytest.mark.parametrize(
    ("mutate", "match"),
    [
        (
            lambda client: client.values[
                f"/repos/{publisher.EXPECTED_FULL_NAME}/actions/runs/{RUN_ID}"
            ].update(conclusion="failure"),
            "workflow conclusion",
        ),
        (
            lambda client: client.values.__setitem__(
                f"/repos/{publisher.EXPECTED_FULL_NAME}/tag_protections", []
            ),
            "protected v\\* rule",
        ),
        (
            lambda client: client.values[f"/repos/{publisher.EXPECTED_FULL_NAME}/tag_protections"][
                0
            ].update(whitelist_usernames=["unexpected-user"]),
            "allowlists differ",
        ),
        (
            lambda client: client.values[
                f"/repos/{publisher.EXPECTED_FULL_NAME}/git/tags/{TAG_OBJECT_SHA}"
            ]["object"].update(type="tree"),
            "target type",
        ),
        (
            lambda client: client.values[
                f"/repos/{publisher.EXPECTED_FULL_NAME}/actions/runs/{RUN_ID}/jobs"
            ]["jobs"][0].update(labels=["release-publisher"]),
            "untrusted release label",
        ),
    ],
)
def test_remote_boundary_failures_never_load_package_credentials(
    tmp_path: Path,
    mutate: Callable[[FakeGitea], None],
    match: str,
) -> None:
    artifact, digest = _artifact_zip(tmp_path)
    client = FakeGitea(digest)
    mutate(client)
    events = client.events

    with pytest.raises(publisher.PublisherError, match=match):
        _publish(tmp_path, client, artifact, events)

    assert "credential:load" not in events
    assert not any(event.startswith("registry:") for event in events)


@pytest.mark.parametrize(
    ("artifact_factory", "match"),
    [
        (
            lambda path: _artifact_zip(path, checksum_override="0" * 64 + "  dist/bad.whl\n"),
            "SHA256SUMS",
        ),
        (
            lambda path: _artifact_zip(path, manifest_override={"source_sha": "c" * 40}),
            "manifest source_sha",
        ),
    ],
)
def test_candidate_tampering_never_loads_package_credentials(
    tmp_path: Path,
    artifact_factory: Callable[[Path], tuple[Path, str]],
    match: str,
) -> None:
    artifact, digest = artifact_factory(tmp_path)
    client = FakeGitea(digest)
    events = client.events

    with pytest.raises(publisher.PublisherError, match=match):
        _publish(tmp_path, client, artifact, events)

    assert "credential:load" not in events
    assert not any(event.startswith("registry:") for event in events)


def test_local_artifact_substitution_is_rejected_before_credentials(tmp_path: Path) -> None:
    artifact, digest = _artifact_zip(tmp_path)
    client = FakeGitea("f" * 64)
    events = client.events

    with pytest.raises(publisher.PublisherError, match="exact successful job log"):
        _publish(tmp_path, client, artifact, events)

    assert digest != "f" * 64
    assert "credential:load" not in events


def test_tagged_workflow_unexpected_credential_path_is_rejected_before_credentials(
    tmp_path: Path,
) -> None:
    malicious_workflow = (
        ROOT / publisher.EXPECTED_WORKFLOW_PATH
    ).read_bytes() + b"\n# forbidden reference: secrets.PACKAGE_TOKEN\n"
    artifact, digest = _artifact_zip(
        tmp_path,
        provenance_override={"workflow_sha256": _sha256_bytes(malicious_workflow)},
    )
    client = FakeGitea(digest)
    workflow_path = (
        f"/repos/{publisher.EXPECTED_FULL_NAME}/contents/"
        f"{publisher.EXPECTED_WORKFLOW_PATH}?ref={SOURCE_SHA}"
    )
    client.values[workflow_path] = _encoded(malicious_workflow)
    events = client.events

    with pytest.raises(publisher.PublisherError, match="secret set or cardinality"):
        _publish(tmp_path, client, artifact, events)

    assert "credential:load" not in events
    assert not any(event.startswith("registry:") for event in events)


def test_tagged_workflow_bracket_secret_is_rejected_before_credentials(tmp_path: Path) -> None:
    malicious_workflow = (
        ROOT / publisher.EXPECTED_WORKFLOW_PATH
    ).read_bytes() + b"\n# forbidden reference: secrets['PACKAGE_TOKEN']\n"
    artifact, digest = _artifact_zip(
        tmp_path,
        provenance_override={"workflow_sha256": _sha256_bytes(malicious_workflow)},
    )
    client = FakeGitea(digest)
    workflow_path = (
        f"/repos/{publisher.EXPECTED_FULL_NAME}/contents/"
        f"{publisher.EXPECTED_WORKFLOW_PATH}?ref={SOURCE_SHA}"
    )
    client.values[workflow_path] = _encoded(malicious_workflow)

    with pytest.raises(publisher.PublisherError, match="secret set or cardinality"):
        _publish(tmp_path, client, artifact, client.events)

    assert "credential:load" not in client.events
    assert not any(event.startswith("registry:") for event in client.events)


def test_existing_registry_mismatch_fails_closed_without_upload(tmp_path: Path) -> None:
    artifact, digest = _artifact_zip(tmp_path)
    client = FakeGitea(digest)
    events = client.events
    registry = FakeRegistry(events)
    registry.remote[f"proxmox_sdk-{VERSION}-py3-none-any.whl"] = "f" * 64

    candidate = publisher.verify_candidate(
        client,
        policy=publisher.PublisherPolicy(1, (publisher.EXPECTED_OWNER,), ()),
        rebuilder=FakeRebuilder(events),
        run_id=RUN_ID,
        artifact_zip=artifact,
        work=tmp_path / "verify-work",
    )
    with pytest.raises(publisher.PublisherError, match="unexpected or mismatched"):
        publisher.publish_verified_candidate(candidate, registry)

    assert registry.uploaded == []


def test_compromised_runner_bytes_fail_independent_rebuild(tmp_path: Path) -> None:
    artifact, digest = _artifact_zip(tmp_path)
    client = FakeGitea(digest)
    with pytest.raises(publisher.PublisherError, match="trusted source rebuild"):
        publisher.verify_candidate(
            client,
            policy=publisher.PublisherPolicy(1, (publisher.EXPECTED_OWNER,), ()),
            rebuilder=FakeRebuilder(client.events, malicious=True),
            run_id=RUN_ID,
            artifact_zip=artifact,
            work=tmp_path / "verify-work",
        )


def test_tag_protection_created_after_run_is_rejected(tmp_path: Path) -> None:
    artifact, digest = _artifact_zip(tmp_path)
    client = FakeGitea(digest)
    protections = client.values[f"/repos/{publisher.EXPECTED_FULL_NAME}/tag_protections"]
    protections[0]["created_at"] = "2026-08-07T16:41:00Z"
    with pytest.raises(publisher.PublisherError, match="created after"):
        publisher.verify_candidate(
            client,
            policy=publisher.PublisherPolicy(1, (publisher.EXPECTED_OWNER,), ()),
            rebuilder=FakeRebuilder(client.events),
            run_id=RUN_ID,
            artifact_zip=artifact,
            work=tmp_path / "verify-work",
        )


def test_candidate_tar_traversal_is_rejected(tmp_path: Path) -> None:
    artifact, digest = _artifact_zip(tmp_path, extra_member="dist/../../escape.whl")
    client = FakeGitea(digest)
    with pytest.raises(publisher.PublisherError, match="unsafe member path"):
        publisher.verify_candidate(
            client,
            policy=publisher.PublisherPolicy(1, (publisher.EXPECTED_OWNER,), ()),
            rebuilder=FakeRebuilder(client.events),
            run_id=RUN_ID,
            artifact_zip=artifact,
            work=tmp_path / "verify-work",
        )


def test_publisher_rejects_modified_root_sealed_handoff(tmp_path: Path) -> None:
    if os.geteuid() != 0:
        pytest.skip("root-owned handoff mutation requires a root test process")
    artifact, digest = _artifact_zip(tmp_path)
    client = FakeGitea(digest)
    candidate = publisher.verify_candidate(
        client,
        policy=publisher.PublisherPolicy(1, (publisher.EXPECTED_OWNER,), ()),
        rebuilder=FakeRebuilder(client.events),
        run_id=RUN_ID,
        artifact_zip=artifact,
        work=tmp_path / "verify-work",
    )
    staging = tmp_path / "staging"
    sealed = tmp_path / "sealed"
    publisher.write_verified_staging(candidate, staging)
    publisher.seal_verified_staging(staging, sealed)
    wheel = next((sealed / "dist").glob("*.whl"))
    wheel.chmod(0o600)
    wheel.write_bytes(wheel.read_bytes() + b"tampered")
    wheel.chmod(0o400)
    with pytest.raises(publisher.PublisherError, match="digest mismatch"):
        publisher.load_sealed_candidate(sealed)


def test_root_sealed_handoff_round_trip_publishes_verified_bytes(tmp_path: Path) -> None:
    if os.geteuid() != 0:
        pytest.skip("root-owned handoff sealing requires a root test process")
    artifact, digest = _artifact_zip(tmp_path)
    client = FakeGitea(digest)
    candidate = publisher.verify_candidate(
        client,
        policy=publisher.PublisherPolicy(1, (publisher.EXPECTED_OWNER,), ()),
        rebuilder=FakeRebuilder(client.events),
        run_id=RUN_ID,
        artifact_zip=artifact,
        work=tmp_path / "verify-work",
    )
    staging = tmp_path / "staging"
    sealed = tmp_path / "sealed"
    publisher.write_verified_staging(candidate, staging)
    publisher.seal_verified_staging(staging, sealed)

    loaded = publisher.load_sealed_candidate(sealed)
    registry = FakeRegistry(client.events)
    publisher.publish_verified_candidate(loaded, registry)

    assert loaded.artifact_name == candidate.artifact_name
    assert loaded.candidate_sha256 == candidate.candidate_sha256
    assert loaded.distribution_manifest_sha256 == candidate.distribution_manifest_sha256
    assert loaded.gitea_provenance_sha256 == candidate.gitea_provenance_sha256
    assert loaded.metadata == candidate.metadata
    assert loaded.run_id == candidate.run_id
    assert loaded.source_sha == candidate.source_sha
    assert loaded.tag == candidate.tag
    assert loaded.version == candidate.version
    assert {name: publisher._sha256(path) for name, path in loaded.distributions.items()} == {
        name: publisher._sha256(path) for name, path in candidate.distributions.items()
    }
    assert set(registry.uploaded) == set(candidate.distributions)


def test_registry_credential_rejects_symlink_and_open_permissions(tmp_path: Path) -> None:
    secret = tmp_path / "registry.json"
    secret.write_text('{"username":"publisher","token":"token"}', encoding="utf-8")
    secret.chmod(0o644)
    with pytest.raises(publisher.PublisherError, match="group/world"):
        publisher.load_registry_credential(secret)

    secret.chmod(0o600)
    link = tmp_path / "registry-link.json"
    link.symlink_to(secret)
    with pytest.raises(publisher.PublisherError, match="non-symlink"):
        publisher.load_registry_credential(link)


def test_actions_directories_use_arguments_environment_and_workspace(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    explicit = tmp_path / "explicit"
    assert publisher._actions_directory(explicit, "TEST_ACTIONS_DIR", "inbox") == explicit

    configured = tmp_path / "configured"
    monkeypatch.setenv("TEST_ACTIONS_DIR", str(configured))
    assert publisher._actions_directory(None, "TEST_ACTIONS_DIR", "inbox") == configured

    monkeypatch.delenv("TEST_ACTIONS_DIR")
    monkeypatch.setenv("GITHUB_WORKSPACE", str(tmp_path / "workspace"))
    assert publisher._actions_directory(None, "TEST_ACTIONS_DIR", "inbox") == (
        tmp_path / "workspace" / ".tmp" / "gitea-package" / "inbox"
    )


def test_actions_seal_round_trip_uses_non_host_paths(tmp_path: Path) -> None:
    candidate = _verified_candidate(tmp_path)
    seal = tmp_path / ".tmp" / "actions-evidence" / "sealed"
    seal.parent.mkdir(parents=True)
    seal_sha256 = publisher.write_verified_staging(candidate, seal)

    identity = {
        "expected_sha256": seal_sha256,
        "source_sha": candidate.source_sha,
        "run_id": candidate.run_id,
        "run_attempt": candidate.run_attempt,
        "tag": candidate.tag,
        "version": candidate.version,
    }
    hardened = publisher.harden_actions_seal(seal, **identity)
    loaded = publisher.load_actions_sealed_candidate(seal, **identity)

    assert hardened.source_sha == SOURCE_SHA
    assert loaded.candidate_sha256 == candidate.candidate_sha256
    assert {name: publisher._sha256(path) for name, path in loaded.distributions.items()} == {
        name: publisher._sha256(path) for name, path in candidate.distributions.items()
    }


def test_whole_actions_seal_replacement_is_refused(tmp_path: Path) -> None:
    candidate = _verified_candidate(tmp_path)
    original = tmp_path / "original"
    forged = tmp_path / "downloaded-seal"
    expected_sha256 = publisher.write_verified_staging(candidate, original)
    publisher.write_verified_staging(candidate, forged)

    wheel = next((forged / "dist").glob("*.whl"))
    wheel.write_bytes(wheel.read_bytes() + b"self-consistent-forgery")
    handoff_path = forged / "handoff.json"
    handoff = json.loads(handoff_path.read_text(encoding="utf-8"))
    handoff["file_sha256"][f"dist/{wheel.name}"] = publisher._sha256(wheel)
    handoff_path.write_text(json.dumps(handoff, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    manifest_path = forged / publisher.SEAL_MANIFEST_NAME
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["files"][f"dist/{wheel.name}"] = publisher._sha256(wheel)
    manifest["files"]["handoff.json"] = publisher._sha256(handoff_path)
    manifest_path.write_bytes(publisher._canonical_json_bytes(manifest))

    with pytest.raises(publisher.PublisherError, match="digest does not match verifier output"):
        publisher.harden_actions_seal(
            forged,
            expected_sha256=expected_sha256,
            source_sha=candidate.source_sha,
            run_id=candidate.run_id,
            run_attempt=candidate.run_attempt,
            tag=candidate.tag,
            version=candidate.version,
        )


def _verified_candidate(tmp_path: Path) -> publisher.VerifiedCandidate:
    artifact, digest = _artifact_zip(tmp_path)
    client = FakeGitea(digest)
    return publisher.verify_candidate(
        client,
        policy=publisher.PublisherPolicy(1, (publisher.EXPECTED_OWNER,), ()),
        rebuilder=FakeRebuilder(client.events),
        run_id=RUN_ID,
        artifact_zip=artifact,
        work=tmp_path / "verify-work",
    )


class _FunctionalActionsRebuilder:
    def __init__(self, source_root: Path, interpreter: Path) -> None:
        assert source_root.is_dir()
        assert interpreter.is_absolute()

    def rebuild(
        self,
        client: publisher.GiteaReader,
        *,
        source_sha: str,
        source_date_epoch: int,
        work: Path,
    ) -> dict[str, Path]:
        del client
        assert source_sha == SOURCE_SHA
        assert source_date_epoch == 1_786_120_800
        output = work / "actions-rebuild"
        output.mkdir()
        distributions = {
            f"proxmox_sdk-{VERSION}-py3-none-any.whl": _wheel(),
            f"proxmox_sdk-{VERSION}.tar.gz": _sdist(),
        }
        result: dict[str, Path] = {}
        for name, value in distributions.items():
            path = output / name
            path.write_bytes(value)
            result[name] = path
        return result


def test_verify_actions_candidate_exercises_attestation_and_rebuild_boundaries(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, digest = _artifact_zip(tmp_path)
    source_root = tmp_path / "source"
    source_root.mkdir()
    workflow = (ROOT / publisher.EXPECTED_WORKFLOW_PATH).read_bytes()
    monkeypatch.setattr(
        publisher,
        "validate_actions_source",
        lambda **_kwargs: (VERSION, 1_786_120_800, workflow),
    )
    monkeypatch.setattr(publisher, "ActionsSourceRebuilder", _FunctionalActionsRebuilder)

    candidate = publisher.verify_actions_candidate(
        source_root=source_root,
        interpreter=Path("/usr/bin/python3"),
        candidate_tar=tmp_path / publisher.PAYLOAD_NAME,
        expected_candidate_sha256=digest,
        run_id=RUN_ID,
        run_attempt=RUN_ATTEMPT,
        source_sha=SOURCE_SHA,
        tag=f"v{VERSION}",
        repository=publisher.EXPECTED_FULL_NAME,
        server_url=publisher.EXPECTED_SERVER,
        work=tmp_path / "actions-work",
    )

    assert candidate.source_sha == SOURCE_SHA
    assert candidate.run_id == RUN_ID
    assert set(candidate.distributions) == {
        f"proxmox_sdk-{VERSION}-py3-none-any.whl",
        f"proxmox_sdk-{VERSION}.tar.gz",
    }


class _ResumableActionsRegistry:
    expected_repository = publisher.EXPECTED_FULL_NAME

    def __init__(
        self,
        candidate: publisher.VerifiedCandidate,
        *,
        present: tuple[publisher.RegistryArtifact, ...] = (),
        fail_after: set[str] | None = None,
    ) -> None:
        self.candidate = candidate
        self.remote = {record.name: record for record in present}
        self.repository = publisher.EXPECTED_FULL_NAME if present else None
        self.fail_after = fail_after or set()
        self.uploaded: list[str] = []
        self.inspections = 0

    def inspect(self, candidate: publisher.VerifiedCandidate) -> publisher.RegistryState:
        assert candidate is self.candidate
        self.inspections += 1
        return publisher.RegistryState(
            bool(self.remote), self.repository, tuple(self.remote.values())
        )

    def upload(self, candidate: publisher.VerifiedCandidate, artifact: Path) -> None:
        assert candidate is self.candidate
        record = next(
            item
            for item in publisher._candidate_registry_artifacts(candidate)
            if item.name == artifact.name
        )
        self.remote[record.name] = record
        self.uploaded.append(record.name)
        if record.name in self.fail_after:
            raise OSError("simulated response loss after storage")

    def link(self) -> None:
        self.repository = self.expected_repository


@pytest.mark.parametrize("failed_index", [0, 1])
def test_actions_upload_failure_after_each_artifact_is_rerunnable(
    tmp_path: Path, failed_index: int
) -> None:
    candidate = _verified_candidate(tmp_path)
    records = publisher._candidate_registry_artifacts(candidate)
    registry = _ResumableActionsRegistry(candidate, fail_after={records[failed_index].name})
    revalidations: list[str] = []

    result, _ = publisher.reconcile_actions_publication(
        candidate=candidate,
        registry=registry,  # type: ignore[arg-type]
        revalidate_seal=lambda: revalidations.append("checked"),
    )
    assert result == "published exact"
    first_uploads = list(registry.uploaded)
    registry.fail_after.clear()
    result, _ = publisher.reconcile_actions_publication(
        candidate=candidate,
        registry=registry,  # type: ignore[arg-type]
        revalidate_seal=lambda: revalidations.append("checked"),
    )
    assert result == "already exact"
    assert registry.uploaded == first_uploads
    assert set(first_uploads) == {record.name for record in records}
    assert registry.inspections >= 5
    assert len(revalidations) >= 6


def test_actions_rerun_uploads_only_the_missing_sealed_artifact(tmp_path: Path) -> None:
    candidate = _verified_candidate(tmp_path)
    records = publisher._candidate_registry_artifacts(candidate)
    registry = _ResumableActionsRegistry(candidate, present=records[:1])

    publisher.reconcile_actions_publication(
        candidate=candidate,
        registry=registry,  # type: ignore[arg-type]
        revalidate_seal=lambda: None,
    )

    assert registry.uploaded == [records[1].name]


def test_actions_mismatched_partial_never_uploads(tmp_path: Path) -> None:
    candidate = _verified_candidate(tmp_path)
    records = publisher._candidate_registry_artifacts(candidate)
    mismatch = publisher.RegistryArtifact(records[0].name, records[0].size, "f" * 64)
    registry = _ResumableActionsRegistry(candidate, present=(mismatch,))

    with pytest.raises(publisher.PublisherError, match="size or digest mismatch"):
        publisher.reconcile_actions_publication(
            candidate=candidate,
            registry=registry,  # type: ignore[arg-type]
            revalidate_seal=lambda: None,
        )

    assert registry.uploaded == []


def test_actions_registry_exact_partial_response_is_resumable(tmp_path: Path) -> None:
    candidate = _verified_candidate(tmp_path)
    records = publisher._candidate_registry_artifacts(candidate)
    state = publisher.RegistryState(True, publisher.EXPECTED_FULL_NAME, records[:1])

    assert publisher.classify_registry_state(state, candidate) == "partial"


def test_actions_registry_mismatched_partial_response_fails_closed(tmp_path: Path) -> None:
    candidate = _verified_candidate(tmp_path)
    records = publisher._candidate_registry_artifacts(candidate)
    state = publisher.RegistryState(
        True,
        publisher.EXPECTED_FULL_NAME,
        (publisher.RegistryArtifact(records[0].name, records[0].size, "f" * 64),),
    )

    with pytest.raises(publisher.PublisherError, match="size or digest mismatch"):
        publisher.classify_registry_state(state, candidate)


class _RedirectResponse:
    status = 302

    def getheader(self, name: str) -> str | None:
        del name
        return "0"


class _Socket:
    def settimeout(self, timeout: float) -> None:
        del timeout


class _RedirectConnection:
    def __init__(self) -> None:
        self.sock = _Socket()

    def request(self, method: str, url: str, body: bytes | None, headers: dict[str, str]) -> None:
        del method, url, body, headers

    def putrequest(self, method: str, url: str) -> None:
        del method, url

    def putheader(self, header: str, *values: str) -> None:
        del header, values

    def endheaders(self) -> None:
        return None

    def send(self, data: bytes) -> None:
        del data

    def getresponse(self) -> _RedirectResponse:
        return _RedirectResponse()

    def close(self) -> None:
        return None


class _MalformedHeaderConnection(_RedirectConnection):
    def request(self, method: str, url: str, body: bytes | None, headers: dict[str, str]) -> None:
        del method, url, body, headers
        raise ValueError("secret-bearing invalid header detail")


class _UploadResponse:
    status = 201

    def getheader(self, name: str) -> str | None:
        return "0" if name == "Content-Length" else None

    def read(self, amount: int) -> bytes:
        del amount
        return b""


class _RecordingSocket:
    def __init__(self) -> None:
        self.timeouts: list[float] = []

    def settimeout(self, timeout: float) -> None:
        self.timeouts.append(timeout)


class _UploadConnection:
    def __init__(self) -> None:
        self.sock = _RecordingSocket()
        self.method = ""
        self.path = ""
        self.headers: dict[str, str] = {}
        self.body = bytearray()
        self.closed = False

    def putrequest(self, method: str, url: str) -> None:
        self.method, self.path = method, url

    def request(self, method: str, url: str, body: bytes | None, headers: dict[str, str]) -> None:
        del method, url, body, headers

    def putheader(self, header: str, *values: str) -> None:
        self.headers[header] = ", ".join(values)

    def endheaders(self) -> None:
        return None

    def send(self, data: bytes) -> None:
        self.body.extend(data)

    def getresponse(self) -> _UploadResponse:
        return _UploadResponse()

    def close(self) -> None:
        self.closed = True


def _parse_multipart_upload(
    payload: bytes, content_type: str
) -> tuple[dict[str, str], bytes, str, str]:
    raw = f"Content-Type: {content_type}\r\nMIME-Version: 1.0\r\n\r\n".encode() + payload
    message = BytesParser(policy=email.policy.default).parsebytes(raw)
    assert message.is_multipart()
    fields: dict[str, str] = {}
    content: bytes | None = None
    content_filename: str | None = None
    content_part_type: str | None = None
    for part in message.iter_parts():
        name = part.get_param("name", header="content-disposition")
        value = part.get_payload(decode=True)
        assert isinstance(name, str)
        assert isinstance(value, bytes)
        assert name not in fields
        if name == "content":
            assert content is None
            content = value
            content_filename = part.get_filename()
            content_part_type = part.get_content_type()
        else:
            assert part.get_filename() is None
            fields[name] = value.decode("utf-8")
    assert content is not None
    assert isinstance(content_filename, str)
    assert isinstance(content_part_type, str)
    return fields, content, content_filename, content_part_type


def _basic_authorization_username(authorization: str) -> str:
    scheme, encoded = authorization.split(" ", 1)
    username, separator, _token = base64.b64decode(encoded, validate=True).partition(b":")
    assert scheme == "Basic"
    assert separator == b":"
    return username.decode("ascii")


class _LocalRegistryState:
    def __init__(self, candidate: publisher.VerifiedCandidate) -> None:
        self.candidate = candidate
        self.files: dict[str, bytes] = {}
        self.repository: str | None = None
        self.upload_requests: list[dict[str, str]] = []

    def store_upload(self, payload: bytes, content_type: str, authorization: str) -> int:
        fields, content, content_filename, content_part_type = _parse_multipart_upload(
            payload, content_type
        )
        assert content_filename in self.candidate.distributions
        assert content_part_type == "application/octet-stream"
        expected_fields = {
            ":action": "file_upload",
            "protocol_version": "1",
            **self.candidate.metadata[content_filename],
            "sha256_digest": _sha256_bytes(content),
        }
        assert fields == expected_fields
        username = _basic_authorization_username(authorization)
        assert username == publisher.EXPECTED_OWNER
        self.upload_requests.append(
            {
                ":action": fields[":action"],
                "authorization_username": username,
                "content_filename": content_filename,
                "content_type": content_part_type,
                "filetype": fields["filetype"],
                "metadata_version": fields["metadata_version"],
                "name": fields["name"],
                "protocol_version": fields["protocol_version"],
                "pyversion": fields["pyversion"],
                "sha256_digest": fields["sha256_digest"],
                "version": fields["version"],
            }
        )
        if content_filename in self.files:
            return 409
        self.files[content_filename] = content
        return 201


def _registry_handler(state: _LocalRegistryState) -> type[http.server.BaseHTTPRequestHandler]:
    class Handler(http.server.BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def _reply(self, status: int, payload: bytes = b"") -> None:
            self.send_response(status)
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)

        def _json(self, value: Any) -> None:
            self._reply(200, json.dumps(value).encode())

        def do_GET(self) -> None:  # noqa: N802
            package_path = (
                f"/api/v1/packages/{publisher.EXPECTED_OWNER}/pypi/"
                f"{publisher.EXPECTED_PACKAGE}/{VERSION}"
            )
            if self.path == package_path and state.files:
                self._json(
                    {
                        "type": "pypi",
                        "name": publisher.EXPECTED_PACKAGE,
                        "version": VERSION,
                        "repository": (
                            {"full_name": state.repository} if state.repository else None
                        ),
                    }
                )
                return
            if self.path == f"{package_path}/files" and state.files:
                self._json(
                    [
                        {
                            "name": name,
                            "size": len(value),
                            "sha256": _sha256_bytes(value),
                        }
                        for name, value in sorted(state.files.items())
                    ]
                )
                return
            prefix = (
                f"/api/packages/{publisher.EXPECTED_OWNER}/pypi/files/"
                f"{publisher.EXPECTED_PACKAGE}/{VERSION}/"
            )
            if self.path.startswith(prefix) and self.path.removeprefix(prefix) in state.files:
                self._reply(200, state.files[self.path.removeprefix(prefix)])
                return
            self._reply(404)

        def do_POST(self) -> None:  # noqa: N802
            upload_path = f"/api/packages/{publisher.EXPECTED_OWNER}/pypi/"
            if self.path == upload_path:
                length = int(self.headers["Content-Length"])
                self._reply(
                    state.store_upload(
                        self.rfile.read(length),
                        self.headers["Content-Type"],
                        self.headers["Authorization"],
                    )
                )
                return
            state.repository = publisher.EXPECTED_FULL_NAME
            self._reply(200)

        def log_message(self, format: str, *args: Any) -> None:
            del format, args

    return Handler


@contextlib.contextmanager
def _local_registry(
    candidate: publisher.VerifiedCandidate,
) -> Iterator[tuple[_LocalRegistryState, int]]:
    state = _LocalRegistryState(candidate)
    try:
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), _registry_handler(state))
    except OSError as exc:
        pytest.skip(f"local socket bind denied: {exc}")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield state, server.server_port
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def _expected_upload_request(candidate: publisher.VerifiedCandidate, name: str) -> dict[str, str]:
    metadata = candidate.metadata[name]
    return {
        ":action": "file_upload",
        "authorization_username": publisher.EXPECTED_OWNER,
        "content_filename": name,
        "content_type": "application/octet-stream",
        "filetype": metadata["filetype"],
        "metadata_version": metadata["metadata_version"],
        "name": publisher.EXPECTED_PACKAGE,
        "protocol_version": "1",
        "pyversion": metadata["pyversion"],
        "sha256_digest": publisher._sha256(candidate.distributions[name]),
        "version": VERSION,
    }


def test_fake_registry_parses_gitea_multipart_contract(tmp_path: Path) -> None:
    candidate = _verified_candidate(tmp_path)
    name = next(iter(sorted(candidate.distributions)))
    connection = _UploadConnection()
    client = publisher.BoundedRegistryClient(
        server_url=publisher.EXPECTED_SERVER,
        token="opaque-test-token",
        connection_factory=lambda _host, _timeout: connection,
    )
    registry = publisher.ActionsGiteaRegistry(
        client,
        publisher.EXPECTED_OWNER,
        publisher.EXPECTED_REPOSITORY,
        publisher.EXPECTED_OWNER,
    )
    state = _LocalRegistryState(candidate)

    registry.upload(candidate, candidate.distributions[name])
    status = state.store_upload(
        bytes(connection.body),
        connection.headers["Content-Type"],
        connection.headers["Authorization"],
    )

    assert status == 201
    assert state.upload_requests == [_expected_upload_request(candidate, name)]
    assert state.files[name] == candidate.distributions[name].read_bytes()
    assert (
        state.store_upload(
            bytes(connection.body),
            connection.headers["Content-Type"],
            connection.headers["Authorization"],
        )
        == 409
    )


def test_actions_registry_upload_and_reconcile_against_local_registry(tmp_path: Path) -> None:
    candidate = _verified_candidate(tmp_path)
    revalidations: list[str] = []
    with _local_registry(candidate) as (state, port):
        client = publisher.BoundedRegistryClient(
            server_url=publisher.EXPECTED_SERVER,
            token="opaque-test-token",
            deadline_seconds=30,
            request_timeout=5,
            connection_factory=lambda _host, timeout: http.client.HTTPConnection(
                "127.0.0.1", port, timeout=timeout
            ),
        )
        registry = publisher.ActionsGiteaRegistry(
            client,
            publisher.EXPECTED_OWNER,
            publisher.EXPECTED_REPOSITORY,
            publisher.EXPECTED_OWNER,
        )
        result, final_state = publisher.reconcile_actions_publication(
            candidate=candidate,
            registry=registry,
            revalidate_seal=lambda: revalidations.append("checked"),
        )

    assert result == "published exact"
    assert state.repository == publisher.EXPECTED_FULL_NAME
    assert set(state.files) == set(candidate.distributions)
    assert len(state.upload_requests) == 2
    expected_requests = [
        _expected_upload_request(candidate, name) for name in sorted(candidate.distributions)
    ]
    assert (
        sorted(state.upload_requests, key=lambda row: row["content_filename"]) == expected_requests
    )
    assert final_state == publisher.RegistryState(
        True,
        publisher.EXPECTED_FULL_NAME,
        publisher._candidate_registry_artifacts(candidate),
    )
    assert len(revalidations) >= 6


def test_publication_evidence_records_final_registry_state(tmp_path: Path) -> None:
    candidate = _verified_candidate(tmp_path)
    state = publisher.RegistryState(
        True,
        publisher.EXPECTED_FULL_NAME,
        publisher._candidate_registry_artifacts(candidate),
    )
    evidence_path = tmp_path / "publication.json"

    publisher.write_publication_evidence(
        candidate,
        evidence_path,
        seal_sha256="c" * 64,
        server_url=publisher.EXPECTED_SERVER,
        owner=publisher.EXPECTED_OWNER,
        repository=publisher.EXPECTED_REPOSITORY,
        result="published exact",
        registry_state=state,
    )

    evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
    assert evidence == {
        "artifact_name": candidate.artifact_name,
        "candidate_sha256": candidate.candidate_sha256,
        "distribution_manifest_sha256": candidate.distribution_manifest_sha256,
        "distribution_sha256": {
            name: publisher._sha256(path) for name, path in sorted(candidate.distributions.items())
        },
        "final_registry_inventory": [
            {
                "filename": record.name,
                "sha256": record.sha256,
                "size": record.size,
            }
            for record in publisher._candidate_registry_artifacts(candidate)
        ],
        "gitea_provenance_sha256": candidate.gitea_provenance_sha256,
        "owner": publisher.EXPECTED_OWNER,
        "registry_version_exists": True,
        "repository": publisher.EXPECTED_REPOSITORY,
        "repository_association": publisher.EXPECTED_FULL_NAME,
        "result": "published exact",
        "run_attempt": candidate.run_attempt,
        "run_id": candidate.run_id,
        "schema_version": 1,
        "seal_sha256": "c" * 64,
        "server_url": publisher.EXPECTED_SERVER,
        "source_sha": candidate.source_sha,
        "tag": candidate.tag,
        "version": candidate.version,
    }


def test_duplicate_same_bytes_is_idempotent_per_reconciliation(tmp_path: Path) -> None:
    candidate = _verified_candidate(tmp_path)
    registry = _ResumableActionsRegistry(candidate)
    first, _ = publisher.reconcile_actions_publication(
        candidate=candidate,
        registry=registry,  # type: ignore[arg-type]
        revalidate_seal=lambda: None,
    )
    request_count = len(registry.uploaded)
    second, _ = publisher.reconcile_actions_publication(
        candidate=candidate,
        registry=registry,  # type: ignore[arg-type]
        revalidate_seal=lambda: None,
    )

    assert first == "published exact"
    assert second == "already exact"
    assert request_count == 2
    assert len(registry.uploaded) == request_count


def test_duplicate_different_bytes_conflicts_before_upload(tmp_path: Path) -> None:
    candidate = _verified_candidate(tmp_path)
    first = publisher._candidate_registry_artifacts(candidate)[0]
    mismatch = publisher.RegistryArtifact(first.name, first.size, "f" * 64)
    registry = _ResumableActionsRegistry(candidate, present=(mismatch,))
    with pytest.raises(publisher.PublisherError, match="size or digest mismatch"):
        publisher.reconcile_actions_publication(
            candidate=candidate,
            registry=registry,  # type: ignore[arg-type]
            revalidate_seal=lambda: None,
        )

    assert registry.uploaded == []


def test_every_upload_uses_bounded_streaming_transport(tmp_path: Path) -> None:
    artifact = tmp_path / "example.whl"
    artifact.write_bytes(b"wheel-bytes")
    connection = _UploadConnection()
    factory_timeouts: list[float] = []

    def factory(_host: str, timeout: float) -> _UploadConnection:
        factory_timeouts.append(timeout)
        return connection

    client = publisher.BoundedRegistryClient(
        server_url=publisher.EXPECTED_SERVER,
        token="opaque-test-token",
        deadline_seconds=30,
        request_timeout=7,
        connection_factory=factory,
    )
    client.upload_distribution(
        path="/api/packages/emersonfelipesp/pypi/",
        username="emersonfelipesp",
        artifact=artifact,
        fields={"name": publisher.EXPECTED_PACKAGE, "version": VERSION},
    )

    assert factory_timeouts == [7]
    assert connection.method == "POST"
    assert connection.path == "/api/packages/emersonfelipesp/pypi/"
    assert connection.headers["Content-Type"].startswith("multipart/form-data; boundary=")
    assert connection.headers["Authorization"].startswith("Basic ")
    assert int(connection.headers["Content-Length"]) == len(connection.body)
    assert connection.sock.timeouts and max(connection.sock.timeouts) <= 7
    assert connection.closed


def test_actions_registry_redirect_response_is_refused() -> None:
    client = publisher.BoundedRegistryClient(
        server_url=publisher.EXPECTED_SERVER,
        token="opaque-test-token",
        connection_factory=lambda _host, _timeout: _RedirectConnection(),
    )

    with pytest.raises(publisher.PublisherError, match="redirect was refused"):
        client.request_bytes(method="GET", path="/api/v1/packages", maximum=1024)


def test_registry_header_value_error_is_sanitized() -> None:
    client = publisher.BoundedRegistryClient(
        server_url=publisher.EXPECTED_SERVER,
        token="opaque-test-token",
        connection_factory=lambda _host, _timeout: _MalformedHeaderConnection(),
    )

    with pytest.raises(publisher.PublisherError, match="headers are invalid") as raised:
        client.request_bytes(method="GET", path="/api/v1/packages", maximum=1024)

    assert "opaque-test-token" not in str(raised.value)
    rendered = "".join(traceback.format_exception(raised.type, raised.value, raised.tb))
    assert "invalid header containing opaque-test-token" not in rendered


@pytest.mark.parametrize(
    "token",
    ["bad\rtoken", "bad\ntoken", "bad\0token", "x" * 4097, "tökën"],
)
def test_actions_registry_rejects_malformed_tokens_before_connection(
    token: str,
) -> None:
    connections: list[str] = []

    with pytest.raises(publisher.PublisherError, match="PACKAGE_WRITE_TOKEN") as raised:
        publisher.BoundedRegistryClient(
            server_url=publisher.EXPECTED_SERVER,
            token=token,
            connection_factory=lambda _host, _timeout: connections.append("constructed"),  # type: ignore[arg-type,return-value]
        )

    assert connections == []
    assert token not in str(raised.value)


def test_actions_command_rejects_token_before_registry_client_construction(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    constructions: list[str] = []
    monkeypatch.setenv("MALFORMED_PACKAGE_TOKEN", "bad\ntoken")
    monkeypatch.setattr(
        publisher,
        "BoundedRegistryClient",
        lambda **_kwargs: constructions.append("constructed"),
    )
    args = SimpleNamespace(
        evidence_dir=tmp_path / "evidence",
        sealed_dir=tmp_path / "sealed",
        publication_evidence=tmp_path / "publication.json",
        token_env="MALFORMED_PACKAGE_TOKEN",
    )

    with pytest.raises(publisher.PublisherError, match="PACKAGE_WRITE_TOKEN"):
        publisher._run_actions_publish(args)

    assert constructions == []


def test_actions_registry_requires_package_write_token() -> None:
    with pytest.raises(publisher.PublisherError, match="invalid length"):
        publisher.BoundedRegistryClient(server_url=publisher.EXPECTED_SERVER, token="")


def test_run_actions_verify_keeps_venv_interpreter_symlink(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """The Actions verifier must hand the venv launcher to the rebuilder unresolved.

    ``venv/bin/python`` is a symlink to the uv-managed base interpreter; resolving
    it escapes the venv and the locked build tools disappear.
    """
    venv_bin = tmp_path / "venv" / "bin"
    venv_bin.mkdir(parents=True)
    launcher = venv_bin / "python"
    launcher.symlink_to(Path(sys.executable))
    assert launcher.resolve() != launcher

    captured: dict[str, Path] = {}

    def _capture(**kwargs: object) -> object:
        captured["interpreter"] = Path(str(kwargs["interpreter"]))
        raise publisher.PublisherError("stop after capture")

    monkeypatch.setattr(publisher, "verify_actions_candidate", _capture)
    args = argparse.Namespace(
        inbox_dir=tmp_path / "inbox",
        evidence_dir=tmp_path / "evidence",
        candidate_tar=None,
        sealed_dir=None,
        work_dir=None,
        event_name="push",
        source_root=tmp_path,
        python=launcher,
        candidate_sha256="0" * 64,
        run_id=RUN_ID,
        run_attempt=RUN_ATTEMPT,
        source_sha=SOURCE_SHA,
        tag=f"v{VERSION}",
        repository=publisher.EXPECTED_FULL_NAME,
        server_url=publisher.EXPECTED_SERVER,
        github_output=tmp_path / "output",
    )

    with pytest.raises(publisher.PublisherError, match="stop after capture"):
        publisher._run_actions_verify(args)

    assert captured["interpreter"] == launcher.absolute()
    assert captured["interpreter"].is_absolute()
    assert captured["interpreter"] != launcher.resolve()


def test_distribution_metadata_reads_root_pkg_info_of_setuptools_sdist(tmp_path: Path) -> None:
    """The egg-info copy of PKG-INFO must not make the sdist ambiguous."""
    sdist = tmp_path / f"proxmox_sdk-{VERSION}.tar.gz"
    sdist.write_bytes(_sdist())
    with tarfile.open(sdist, mode="r:gz") as archive:
        names = [m.name for m in archive.getmembers() if m.name.endswith("PKG-INFO")]
    assert len(names) == 2, names

    metadata = publisher._distribution_metadata(sdist)

    assert metadata["version"] == VERSION


def test_distribution_metadata_refuses_multi_root_sdist(tmp_path: Path) -> None:
    sdist = tmp_path / f"proxmox_sdk-{VERSION}.tar.gz"
    sdist.write_bytes(_sdist(roots=(f"proxmox_sdk-{VERSION}", "other-root")))

    with pytest.raises(publisher.PublisherError, match="unique PKG-INFO"):
        publisher._distribution_metadata(sdist)

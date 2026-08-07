"""Security-boundary tests for the host-side Gitea package publisher."""

from __future__ import annotations

import base64
import hashlib
import io
import json
import tarfile
import zipfile
from collections.abc import Callable
from pathlib import Path
from typing import Any

import pytest

from tools import gitea_package_publisher as publisher

ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.0.13.post4"
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
        archive.writestr(f"proxmox_sdk-{VERSION}.dist-info/METADATA", metadata)
    return result.getvalue()


def _sdist() -> bytes:
    result = io.BytesIO()
    metadata = (
        "Metadata-Version: 2.4\n"
        "Name: proxmox-sdk\n"
        f"Version: {VERSION}\n"
        "Summary: test package\n"
        "Requires-Python: >=3.11\n\n"
    ).encode()
    with tarfile.open(fileobj=result, mode="w:gz") as archive:
        info = tarfile.TarInfo(f"proxmox_sdk-{VERSION}/PKG-INFO")
        info.size = len(metadata)
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
    staging = tmp_path / "staging"
    sealed = tmp_path / "sealed"
    publisher.write_verified_staging(candidate, staging)
    publisher.seal_verified_staging(staging, sealed)
    candidate = publisher.load_sealed_candidate(sealed)
    events.append("credential:load")
    registry = FakeRegistry(events)
    publisher.publish_verified_candidate(candidate, registry)
    publisher.write_publication_evidence(candidate, tmp_path / "evidence.json")
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


def test_tagged_workflow_credential_path_is_rejected_before_credentials(tmp_path: Path) -> None:
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

    with pytest.raises(publisher.PublisherError, match="forbidden publisher credential path"):
        _publish(tmp_path, client, artifact, events)

    assert "credential:load" not in events
    assert not any(event.startswith("registry:") for event in events)


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

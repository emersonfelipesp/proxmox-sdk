"""Schema-level tests for hand-coded PBS Pydantic models.

These models cover the v1 read-only surface. Tests assert that PBS's
hyphenated wire fields map to snake_case attributes via Pydantic aliases,
and that ``extra="allow"`` keeps forward-compatible fields available.
"""

from __future__ import annotations

from proxmox_sdk.pbs import models as m


def test_version_minimal():
    v = m.PBSVersion.model_validate({"version": "3.2.7", "release": "1", "repoid": "abc"})
    assert v.version == "3.2.7"
    assert v.release == "1"


def test_node_status_partial():
    s = m.PBSNodeStatus.model_validate(
        {
            "uptime": 1234,
            "cpu": 0.42,
            "loadavg": [0.1, 0.2, 0.3],
            "memory": {"total": 1024, "used": 512, "free": 512},
            "cpuinfo": {"cpus": 4, "model": "Xeon"},
        }
    )
    assert s.uptime == 1234
    assert s.memory and s.memory.used == 512
    assert s.cpuinfo and s.cpuinfo.cpus == 4


def test_datastore_aliases_store_to_name():
    d = m.PBSDatastore.model_validate(
        {
            "store": "tank",
            "path": "/mnt/tank",
            "total": 1000,
            "used": 250,
            "avail": 750,
            "gc-status": "ok",
            "estimated-full-date": 1234567890,
        }
    )
    assert d.name == "tank"
    assert d.gc_status == "ok"
    assert d.estimated_full_date == 1234567890


def test_backup_group_hyphenated_fields():
    g = m.PBSBackupGroup.model_validate(
        {
            "backup-type": "vm",
            "backup-id": "100",
            "last-backup": 1700000000,
            "backup-count": 5,
            "owner": "root@pam",
        }
    )
    assert g.backup_type == "vm"
    assert g.backup_id == "100"
    assert g.last_backup == 1700000000


def test_snapshot_with_files_and_verification():
    s = m.PBSSnapshot.model_validate(
        {
            "backup-type": "vm",
            "backup-id": "100",
            "backup-time": 1700000000,
            "size": 12345,
            "files": [{"filename": "qemu.img.fidx", "size": 999, "crypt-mode": "none"}],
            "verification": {"state": "ok", "upid": "UPID:..."},
            "fingerprint": "ab:cd",
        }
    )
    assert s.backup_type == "vm"
    assert s.backup_id == "100"
    assert s.files and s.files[0].filename == "qemu.img.fidx"
    assert s.verification and s.verification.state == "ok"


def test_job_normalization_carries_job_type():
    j = m.PBSJob.model_validate(
        {
            "job_type": "verify",
            "id": "v-daily",
            "store": "tank",
            "schedule": "daily",
            "last-run-state": "ok",
            "last-run-endtime": 1700000000,
        }
    )
    assert j.job_type == "verify"
    assert j.job_id == "v-daily"
    assert j.last_run_state == "ok"


def test_extra_fields_preserved():
    """PBS may add fields between releases; extra='allow' must keep them."""
    d = m.PBSDatastore.model_validate({"store": "tank", "future-field": 42})
    assert d.model_dump(by_alias=True).get("future-field") == 42

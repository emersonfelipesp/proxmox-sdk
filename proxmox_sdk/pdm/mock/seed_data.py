"""Realistic default fixture data for the PDM mock API.

Returns a fresh deep-copy on every call so tests can mutate the resulting
dict without polluting subsequent runs.
"""

from __future__ import annotations

import copy
from typing import Any

# The seed mirrors the structure the PDM mock state expects. See
# :class:`proxmox_sdk.pdm.mock.routes.PDMMockState` for the schema.
_DEFAULT_SEED: dict[str, Any] = {
    "version": {"version": "1.0.4", "release": "1", "repoid": "abcdef01"},
    "remotes": [
        {
            "id": "pve-cluster-a",
            "type": "pve",
            "nodes": [
                {"hostname": "pve-a-1"},
                {"hostname": "pve-a-2"},
                {"hostname": "pve-a-3"},
            ],
            "authid": "root@pam!pdm",
            "fingerprint": "AA:BB:CC:DD:EE:FF",
            "web-url": "https://pve-a-1.example.com:8006",
        },
        {
            "id": "pve-cluster-b",
            "type": "pve",
            "nodes": [
                {"hostname": "pve-b-1"},
                {"hostname": "pve-b-2"},
            ],
            "authid": "root@pam!pdm",
            "fingerprint": "11:22:33:44:55:66",
        },
        {
            "id": "pbs-main",
            "type": "pbs",
            "nodes": [{"hostname": "pbs-main"}],
            "authid": "root@pam!pdm",
            "fingerprint": "F1:F2:F3:F4:F5:F6",
        },
    ],
    "remote_versions": {
        "pve-cluster-a": {"version": "9.1.11", "release": "1"},
        "pve-cluster-b": {"version": "9.1.11", "release": "1"},
        "pbs-main": {"version": "3.4.2", "release": "1"},
    },
    "pve": {
        "pve-cluster-a": {
            "nodes": [
                {"node": "pve-a-1", "status": "online", "cpu": 0.18, "maxcpu": 16},
                {"node": "pve-a-2", "status": "online", "cpu": 0.05, "maxcpu": 16},
                {"node": "pve-a-3", "status": "online", "cpu": 0.42, "maxcpu": 16},
            ],
            "qemu": [
                {
                    "vmid": 100,
                    "name": "web-prod-1",
                    "status": "running",
                    "node": "pve-a-1",
                    "cpu": 0.12,
                    "cpus": 4,
                    "mem": 2_147_483_648,
                    "maxmem": 4_294_967_296,
                    "uptime": 1_200_000,
                },
                {
                    "vmid": 101,
                    "name": "db-prod",
                    "status": "running",
                    "node": "pve-a-2",
                    "cpu": 0.40,
                    "cpus": 8,
                    "mem": 8_589_934_592,
                    "maxmem": 17_179_869_184,
                    "uptime": 1_100_000,
                },
                {
                    "vmid": 102,
                    "name": "staging",
                    "status": "stopped",
                    "node": "pve-a-3",
                    "cpus": 2,
                },
                {
                    "vmid": 103,
                    "name": "build-runner",
                    "status": "running",
                    "node": "pve-a-1",
                    "cpus": 4,
                },
                {
                    "vmid": 104,
                    "name": "ldap",
                    "status": "running",
                    "node": "pve-a-2",
                    "cpus": 2,
                },
                {"vmid": 105, "name": "mail", "status": "running", "node": "pve-a-3", "cpus": 4},
                {
                    "vmid": 106,
                    "name": "monitor",
                    "status": "running",
                    "node": "pve-a-1",
                    "cpus": 2,
                },
                {
                    "vmid": 107,
                    "name": "git",
                    "status": "running",
                    "node": "pve-a-2",
                    "cpus": 4,
                },
                {
                    "vmid": 108,
                    "name": "ci-coordinator",
                    "status": "stopped",
                    "node": "pve-a-3",
                    "cpus": 2,
                },
                {
                    "vmid": 109,
                    "name": "test-vm",
                    "status": "running",
                    "node": "pve-a-1",
                    "cpus": 1,
                },
            ],
            "lxc": [
                {
                    "vmid": 200,
                    "name": "logs",
                    "status": "running",
                    "node": "pve-a-1",
                    "cpus": 2,
                },
                {
                    "vmid": 201,
                    "name": "ingest",
                    "status": "running",
                    "node": "pve-a-2",
                    "cpus": 1,
                },
                {
                    "vmid": 202,
                    "name": "proxy",
                    "status": "stopped",
                    "node": "pve-a-3",
                    "cpus": 1,
                },
                {
                    "vmid": 203,
                    "name": "redis",
                    "status": "running",
                    "node": "pve-a-1",
                    "cpus": 1,
                },
                {
                    "vmid": 204,
                    "name": "cache",
                    "status": "running",
                    "node": "pve-a-2",
                    "cpus": 1,
                },
            ],
            "tasks": [
                {
                    "upid": "UPID:pve-a-1:0000:00000:ABCDEF01:vzstart:100:root@pam:",
                    "type": "vzstart",
                    "node": "pve-a-1",
                    "status": "OK",
                    "starttime": 1_700_000_000,
                    "endtime": 1_700_000_300,
                    "user": "root@pam",
                }
            ],
        },
        "pve-cluster-b": {
            "nodes": [
                {"node": "pve-b-1", "status": "online", "cpu": 0.08, "maxcpu": 12},
                {"node": "pve-b-2", "status": "online", "cpu": 0.32, "maxcpu": 12},
            ],
            "qemu": [
                {
                    "vmid": 300,
                    "name": "edge-1",
                    "status": "running",
                    "node": "pve-b-1",
                    "cpus": 2,
                },
                {
                    "vmid": 301,
                    "name": "edge-2",
                    "status": "running",
                    "node": "pve-b-1",
                    "cpus": 2,
                },
                {
                    "vmid": 302,
                    "name": "edge-3",
                    "status": "running",
                    "node": "pve-b-2",
                    "cpus": 2,
                },
                {
                    "vmid": 303,
                    "name": "edge-4",
                    "status": "stopped",
                    "node": "pve-b-2",
                    "cpus": 2,
                },
                {
                    "vmid": 304,
                    "name": "edge-5",
                    "status": "running",
                    "node": "pve-b-1",
                    "cpus": 2,
                },
                {
                    "vmid": 305,
                    "name": "edge-6",
                    "status": "running",
                    "node": "pve-b-2",
                    "cpus": 2,
                },
            ],
            "lxc": [],
            "tasks": [],
        },
    },
    "pbs": {
        "pbs-main": {
            "datastores": [
                {
                    "store": "tank",
                    "total": 10_000_000_000_000,
                    "used": 4_500_000_000_000,
                    "avail": 5_500_000_000_000,
                    "comment": "primary backup pool",
                },
                {
                    "store": "cold",
                    "total": 50_000_000_000_000,
                    "used": 30_000_000_000_000,
                    "avail": 20_000_000_000_000,
                    "comment": "archive",
                },
            ],
            "snapshots": [
                {
                    "store": "tank",
                    "namespace": "prod",
                    "backup-type": "vm",
                    "backup-id": "100",
                    "backup-time": 1_700_000_000,
                    "size": 12_345_678_900,
                    "owner": "root@pam",
                },
                {
                    "store": "tank",
                    "namespace": "prod",
                    "backup-type": "vm",
                    "backup-id": "101",
                    "backup-time": 1_700_086_400,
                    "size": 23_456_789_012,
                    "owner": "root@pam",
                },
                {
                    "store": "cold",
                    "namespace": "archive",
                    "backup-type": "ct",
                    "backup-id": "200",
                    "backup-time": 1_690_000_000,
                    "size": 1_234_567_890,
                    "owner": "root@pam",
                },
            ],
            "tasks": [],
        }
    },
    "resources": {
        "status": [
            {"remote": "pve-cluster-a", "status": "online"},
            {"remote": "pve-cluster-b", "status": "online"},
            {"remote": "pbs-main", "status": "online"},
        ],
        "subscriptions": [
            {
                "remote": "pve-cluster-a",
                "status": "active",
                "productname": "Proxmox VE Standard",
                "level": "standard",
            },
            {
                "remote": "pve-cluster-b",
                "status": "active",
                "productname": "Proxmox VE Community",
                "level": "community",
            },
            {
                "remote": "pbs-main",
                "status": "active",
                "productname": "Proxmox Backup Server Basic",
                "level": "basic",
            },
        ],
    },
    "metrics": {"status": {"enabled": True, "status": "ok", "last-collection": 1_700_000_000}},
    "access": {
        "users": [
            {"userid": "root@pam", "enable": True, "comment": "default admin"},
            {"userid": "ops@pdm", "enable": True, "comment": "operations team"},
            {"userid": "auditor@pdm", "enable": True, "comment": "read-only auditor"},
        ],
        "acl": [
            {
                "path": "/",
                "type": "user",
                "ugid": "root@pam",
                "roleid": "Admin",
                "propagate": True,
            },
            {
                "path": "/remote/pve-cluster-a",
                "type": "user",
                "ugid": "ops@pdm",
                "roleid": "PVEAdmin",
                "propagate": True,
            },
            {
                "path": "/remote/pve-cluster-b",
                "type": "user",
                "ugid": "ops@pdm",
                "roleid": "PVEOperator",
                "propagate": True,
            },
            {
                "path": "/",
                "type": "user",
                "ugid": "auditor@pdm",
                "roleid": "Auditor",
                "propagate": True,
            },
            {
                "path": "/remote/pbs-main",
                "type": "user",
                "ugid": "ops@pdm",
                "roleid": "PBSDatastoreAdmin",
                "propagate": True,
            },
        ],
        "tfa": {},
        "tokens": {},
    },
    "views": [
        {
            "id": "prod-overview",
            "name": "Production Overview",
            "comment": "All prod resources across PVE clusters",
        },
        {
            "id": "backups",
            "name": "Backups",
            "comment": "PBS-only view across remotes",
        },
    ],
}


def get_default_pdm_seed() -> dict[str, Any]:
    """Return a fresh deep copy of the default PDM seed data."""
    return copy.deepcopy(_DEFAULT_SEED)

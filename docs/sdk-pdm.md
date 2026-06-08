# Proxmox Datacenter Manager (PDM): HOW-TO Guide

Complete guide for managing a Proxmox Datacenter Manager instance using the
SDK — from connecting and listing remotes to querying VMs, PBS datastores,
subscriptions, metrics, views, and access control.

---

## Overview

PDM (Proxmox Datacenter Manager) is a centralised management layer that
multiplexes across registered PVE clusters and PBS instances ("remotes").
`PDMClient` is a typed facade that wraps `ProxmoxSDK(service="PDM")` and
organises PDM domains:

| Domain | Attribute | Description |
|---|---|---|
| `RemotesDomain` | `.remotes` | Registered PVE/PBS remotes |
| `PVEDomain` | `.pve` | PVE guests (VMs + CTs) across remotes |
| `PBSDomain` | `.pbs` | PBS datastores across remotes |
| `GlobalResourcesDomain` | `.resources` | Cluster-wide resource overview |
| `SubscriptionsDomain` | `.subscriptions` | Subscription status per remote |
| `MetricsDomain` | `.metrics` | Performance metrics |
| `AccessDomain` | `.access` | Users, tokens, ACLs |
| `ViewsDomain` | `.views` | Saved resource views |

!!! note "remote argument"
    Because PDM multiplexes across registered clusters, most guest/datastore
    operations require a `remote` argument (the registered remote name, e.g.
    `"pve-prod"`) in addition to the resource ID.

### PDM vs PBS vs PVE Differences

| Aspect | PVE | PBS | PDM |
|--------|-----|-----|-----|
| Default port | 8006 | 8007 | **8443** |
| Auth cookie | `PVEAuthCookie` | `PBSAuthCookie` | `PDMAuthCookie` |
| Token separator | `=` | `:` | **`:`** |
| `pvesh` CLI | Yes | No | No |
| Remote argument | N/A | N/A | **Required for guest/datastore ops** |

---

## Installation

PDM support is included in the base `proxmox-sdk` package (no extra optional
groups required).  The optional `pdm` extra is reserved for future
PDM-specific heavy dependencies if needed.

---

## Session Setup

### Async (Recommended)

```python
import asyncio
from proxmox_sdk.pdm import PDMClient

async def main():
    async with PDMClient(
        host="pdm.example.com",
        user="admin@pam",
        token_name="automation",
        token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        port=8443,   # default for PDM
    ) as pdm:
        version = await pdm.version()
        print(f"PDM version: {version.version}")

asyncio.run(main())
```

### Sync (Blocking)

```python
from proxmox_sdk.pdm import SyncPDMClient

with SyncPDMClient(
    host="pdm.example.com",
    user="admin@pam",
    token_name="automation",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    port=8443,
) as pdm:
    version = pdm.version()
    print(f"PDM version: {version.version}")
```

### From an Existing ProxmoxSDK

```python
from proxmox_sdk import ProxmoxSDK
from proxmox_sdk.pdm import PDMClient

async def main():
    async with ProxmoxSDK(
        host="pdm.example.com",
        user="admin@pam",
        password="secret",
        service="PDM",
        port=8443,
    ) as sdk:
        pdm = PDMClient.from_sdk(sdk)
        version = await pdm.version()

asyncio.run(main())
```

### Mock Mode (for Tests)

```python
from proxmox_sdk.pdm import PDMClient

async with PDMClient.mock() as pdm:
    version = await pdm.version()
```

---

## Remotes

List, inspect, and filter the PVE/PBS instances registered with PDM.

```python
async with PDMClient(...) as pdm:
    remotes = await pdm.remotes.list()
    for remote in remotes:
        print(f"{remote.id}: {remote.type} — {remote.url}")
```

---

## PVE Guests

Because PDM spans multiple clusters, most operations require a `remote` name.

```python
async with PDMClient(...) as pdm:
    # List all VMs across a remote
    vms = await pdm.pve.vms(remote="pve-prod")
    for vm in vms:
        print(f"VM {vm.vmid}: {vm.name} ({vm.status})")

    # List all LXC containers
    cts = await pdm.pve.lxc(remote="pve-prod")

    # Get a specific VM
    vm = await pdm.pve.vm(remote="pve-prod", vmid=100)
    print(f"VM {vm.vmid} running on node {vm.node}")
```

---

## PBS Datastores

```python
async with PDMClient(...) as pdm:
    datastores = await pdm.pbs.datastores(remote="pbs-backup")
    for ds in datastores:
        print(f"Datastore: {ds.store}, usage: {ds.used}/{ds.total}")

    snapshots = await pdm.pbs.snapshots(remote="pbs-backup", store="vm-backups")
    for snap in snapshots:
        print(f"{snap.backup_type}/{snap.backup_id} @ {snap.backup_time}")
```

---

## Resources

Cluster-wide resource aggregation.

```python
async with PDMClient(...) as pdm:
    resources = await pdm.resources.list()
    for r in resources:
        print(f"{r.type}/{r.id}: {r.status}")
```

---

## Subscriptions

```python
async with PDMClient(...) as pdm:
    subs = await pdm.subscriptions.list()
    for sub in subs:
        print(f"{sub.remote}: {sub.status} (level: {sub.level})")
```

---

## Metrics

```python
async with PDMClient(...) as pdm:
    metrics = await pdm.metrics.list()
```

---

## Access Control

```python
async with PDMClient(...) as pdm:
    # Users
    users = await pdm.access.users()
    for user in users:
        print(f"User: {user.userid}")

    # ACL entries
    acl = await pdm.access.acl()
```

---

## Views

Saved resource views (named filtered subsets of resources).

```python
async with PDMClient(...) as pdm:
    views = await pdm.views.list()
    for view in views:
        print(f"View: {view.id}")
```

---

## PDM Mock Server (`proxmox-sdk-pdm-mock`)

`proxmox-sdk-pdm-mock` is a standalone FastAPI mock for the PDM REST API.
It ships with a bundled default seed (3 remotes, 16 VMs, 5 CTs, 2 datastores,
50+ snapshots, 3 users, 5 ACL entries, 2 views) so E2E tests run without a
live PDM instance.

### Starting the mock

```bash
# Default: binds to 0.0.0.0:8443
proxmox-sdk-pdm-mock
```

### Environment variables

| Variable | Default | Description |
|---|---|---|
| `PROXMOX_PDM_MOCK_HOST` | `0.0.0.0` | Bind host |
| `PROXMOX_PDM_MOCK_PORT` | `8443` | Bind port |
| `PROXMOX_PDM_MOCK_SEED_FILE` | — | JSON file to use as initial state |
| `PROXMOX_PDM_MOCK_SCHEMA_VERSION` | `1.0` | Reserved for future PDM codegen pipeline |

### Custom seed file

```bash
export PROXMOX_PDM_MOCK_SEED_FILE=/path/to/seed.json
proxmox-sdk-pdm-mock
```

### Programmatic use in tests

```python
from proxmox_sdk.pdm_mock_main import create_pdm_mock_app
from httpx import AsyncClient

app = create_pdm_mock_app()

async with AsyncClient(app=app, base_url="http://test") as client:
    resp = await client.get("/health")
    assert resp.json()["status"] == "ready"
```

You can also pass a custom `seed` dict or a shared `PDMMockState` to
`create_pdm_mock_app()` so multiple test fixtures coordinate state without
going through HTTP.

---

## See Also

- [SDK Guide](./sdk-guide.md) — Overview, backends, and core concepts
- [SDK Internals](./sdk-internals.md) — Services layer and transport details
- [Proxmox Backup Server HOW-TO](./sdk-pbs.md) — PBS datastores, snapshots, GC
- [Ceph HOW-TO](./sdk-ceph.md) — Ceph cluster management
- [Authentication Guide](./sdk-authentication.md) — Credential setup

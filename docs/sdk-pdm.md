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

### Schema Contract and Provenance

The authoritative PDM wire contract bundled with this release is
`proxmox_sdk/generated/pdm/latest/openapi.json`, generated from the Proxmox API
Viewer capture in the adjacent `raw_capture.json`. The `latest` artifact contains
246 paths and 318 operations. Hand-written domain models intentionally sit at the
boundary: they preserve the public Python API while validating the captured wire
cardinality, aliases, required identifiers, and discriminator values.

| Public read | Captured wire shape | SDK result |
|---|---|---|
| `version()` | object | `PDMVersion` |
| `ping()` | string | `str` |
| `remotes.list()` / `remotes.get()` | array / config object | `list[PDMRemote]` / `PDMRemote` |
| PVE guest, node, resource, task, and RRD reads | arrays, except guest config | typed model lists / `PDMGuestConfig` |
| PBS datastore, snapshot, task, and RRD reads | arrays, except task status | typed model lists / `PDMTaskStatus` |
| `resources.list()` | array of per-remote envelopes | flattened `list[PDMResource]` with `remote` injected |
| `resources.status()` | one per-remote envelope | `PDMResourceStatus` |
| subscriptions and metric status | arrays | typed model lists |
| access and view reads | arrays, except user/view detail | typed model lists / detail model |

Malformed object/list cardinality and missing required identifiers raise
`PDMResponseContractError`. Messages report only the operation, expected shape,
received type, and invalid field locations; response values are not included or
retained as exception context. Operator-controlled `error` strings at every
typed PDM response boundary are replaced with the static `"remote reported an
error"` marker before model validation. When a resource
envelope contains stale resources plus an error, each returned
`PDMResource.remote_error` carries only that marker. An errored envelope with no
usable resources raises the same typed, redacted exception.

Resource discriminators are required and closed over the captured local PVE and
global PDM enums. RRD reads always send the schema-required `timeframe` and `cf`
parameters; defaults are `hour` and `AVERAGE`. Datastore RRD samples expose
`disk_used` and `disk_available` separately so available capacity is never
silently collapsed into used capacity.

!!! warning "Corrected public read shapes"
    This contract revision corrects previously permissive public return shapes:
    `ping()` returns a string, metric status returns a list, and resource status
    returns one status model. Consumers pinned to an earlier SDK should validate
    these shapes before updating their package constraint.

The schema artifact and generated mock are high-fidelity development evidence,
not a substitute for version-specific validation against an operator-approved
live PDM deployment.

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

## Liveness Probe (`ping()`)

`PDMClient.ping()` / `SyncPDMClient.ping()` call `GET /ping`, a lightweight
liveness probe that does not require authentication scope beyond a valid
session — useful for health checks before running heavier operations.

```python
async with PDMClient(...) as pdm:
    result = await pdm.ping()
    print(result)
```

```python
with SyncPDMClient(...) as pdm:
    result = pdm.ping()
    print(result)
```

---

## Remotes

List, inspect, and filter the PVE/PBS instances registered with PDM.

```python
async with PDMClient(...) as pdm:
    remotes = await pdm.remotes.list()
    for remote in remotes:
        print(f"{remote.id}: {remote.type} — {remote.web_url}")

    remote = await pdm.remotes.get("pve-prod")
    version = await pdm.remotes.version("pve-prod")
```

---

## PVE Guests

Because PDM spans multiple clusters, most operations require a `remote` name.

```python
async with PDMClient(...) as pdm:
    # List QEMU VMs on a remote
    vms = await pdm.pve.qemu.list("pve-prod")
    for vm in vms:
        print(f"VM {vm.vmid}: {vm.name} ({vm.status})")

    # List all LXC containers
    cts = await pdm.pve.lxc.list("pve-prod")

    # Read the pending configuration (the PDM schema default). Use
    # state="active" to inspect the currently active configuration instead.
    config = await pdm.pve.qemu.config("pve-prod", 100)
    print(f"Configured VM name: {config.name}")
```

---

## PBS Datastores

```python
async with PDMClient(...) as pdm:
    datastores = await pdm.pbs.datastores(remote="pbs-backup")
    for ds in datastores:
        print(f"Datastore: {ds.store} ({ds.comment or 'no comment'})")

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
        if r.remote_error:
            print(f"  Resource data for {r.remote} is degraded")

    status = await pdm.resources.status()
    print(f"Status response for {status.remote}: {len(status.resources)} resources")
```

---

## Subscriptions

```python
async with PDMClient(...) as pdm:
    subs = await pdm.subscriptions.list()
    for sub in subs:
        print(f"{sub.remote}: {sub.state}")
```

---

## Metrics

```python
async with PDMClient(...) as pdm:
    statuses = await pdm.metrics.status()
    for status in statuses:
        print(f"{status.remote}: last collection {status.last_collection}")
```

---

## Access Control

```python
async with PDMClient(...) as pdm:
    # Users
    users = await pdm.access.users.list()
    for user in users:
        print(f"User: {user.userid}")

    # ACL entries
    acl = await pdm.access.acl.list()
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
3 snapshots, 3 users, 5 ACL entries, 2 views) so E2E tests run without a
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

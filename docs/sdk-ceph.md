# Ceph: HOW-TO Guide

Complete guide for managing Ceph storage through proxmox-sdk — using both the
Proxmox VE-managed API (via `CephClient`) and the direct provider clients
(`DashboardCephClient`, `RGWAdminClient`, `RBDClient`) for Proxmox-managed or
external standalone clusters.

---

## Overview

Proxmox VE exposes Ceph management under `/cluster/ceph` and
`/nodes/{node}/ceph`.  `CephClient` is a typed facade that wraps
`ProxmoxSDK(service="PVE")` and organises these endpoints into three focused
domains:

| Domain | Attribute | Description |
|---|---|---|
| `ClusterCeph` | `.cluster` | Cluster-wide status, metadata, flags |
| `NodeCeph` | `.nodes` | Per-node OSD, MON, MDS, MGR inventory |
| `CephWrite` | `.write` | Destructive operations (pool create/delete, OSD in/out, …) |

The **direct provider clients** (`ceph.providers`) target Ceph services
directly — not through PVE — so they work with both Proxmox-managed and
external standalone clusters.

---

## Installation

Ceph support is included in the base `proxmox-sdk` package.  No extra
optional dependency groups are required.

---

## Session Setup

### Async (Recommended)

```python
import asyncio
from proxmox_sdk.ceph import CephClient

async def main():
    async with CephClient(
        host="pve.example.com",
        user="admin@pam",
        token_name="automation",
        token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    ) as ceph:
        status = await ceph.status()
        print(f"Ceph health: {status.health}")

asyncio.run(main())
```

### Sync (Blocking)

```python
from proxmox_sdk.ceph import SyncCephClient

with SyncCephClient(
    host="pve.example.com",
    user="admin@pam",
    token_name="automation",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
) as ceph:
    status = ceph.status()
    print(f"Ceph health: {status.health}")
```

### From an Existing ProxmoxSDK

```python
from proxmox_sdk import ProxmoxSDK
from proxmox_sdk.ceph import CephClient

async def main():
    async with ProxmoxSDK(host="pve.example.com", user="admin@pam",
                          password="secret", service="PVE") as sdk:
        ceph = CephClient.from_sdk(sdk)
        status = await ceph.status()

asyncio.run(main())
```

### Mock Mode (for Tests)

```python
from proxmox_sdk.ceph import CephClient

async with CephClient.mock() as ceph:
    status = await ceph.status()
```

---

## Cluster-Wide Reads (`.cluster`)

```python
async with CephClient(...) as ceph:
    # Overall cluster health/status
    status = await ceph.cluster.status()
    print(status.health)

    # Detailed metadata (daemons, versions)
    meta = await ceph.cluster.metadata()

    # Global flags
    flags = await ceph.cluster.flags()
    for flag in flags:
        print(f"{flag.name} = {flag.value}")
```

---

## Per-Node Reads (`.nodes`)

```python
async with CephClient(...) as ceph:
    # List OSDs on a node
    osds = await ceph.nodes.osds(node="pve1")
    for osd in osds:
        print(f"OSD {osd.osd}: {osd.status}")

    # MON status
    mons = await ceph.nodes.mons(node="pve1")

    # MDS status
    mds = await ceph.nodes.mds(node="pve1")
```

---

## Destructive Write Operations (`.write`)

!!! warning "Destructive operations require opt-in"
    Every method in `CephWrite` that can delete or disable something requires
    `confirm_destroy=True`.  Omitting the flag raises `ValueError` before any
    HTTP request is sent.

```python
async with CephClient(...) as ceph:
    # Create a pool (returns task UPID)
    upid = await ceph.write.pool_create(
        node="pve1",
        name="my-pool",
    )

    # Delete a pool — must opt in
    upid = await ceph.write.pool_delete(
        node="pve1",
        name="my-pool",
        confirm_destroy=True,   # required
    )

    # Mark an OSD out of the cluster
    await ceph.write.osd_out(node="pve1", osdid=3)

    # Destroy an OSD — must opt in
    upid = await ceph.write.osd_destroy(
        node="pve1",
        osdid=3,
        confirm_destroy=True,   # required
    )
```

The `confirm_destroy` gate is implemented in `proxmox_sdk.ceph._confirm`:

```python
def require_confirm(operation: str, confirm_destroy: bool) -> None:
    if not confirm_destroy:
        raise ValueError(f"{operation} is destructive; pass confirm_destroy=True to proceed.")
```

---

## Direct Provider Clients (`ceph.providers`)

The direct provider clients talk to Ceph services directly (not via PVE) and
support Proxmox-managed *and* external/standalone Ceph clusters.

### `DashboardCephClient`

```python
from proxmox_sdk.ceph.providers import DashboardCephClient

async with DashboardCephClient(
    base_url="https://ceph-dashboard.example.com:8443",
    username="admin",
    password="secret",
) as client:
    caps = await client.capabilities()
    print(f"available={caps.available}, write={caps.write}")

    health = await client.health()
    osds   = await client.osds()
    pools  = await client.pools()
```

### `RGWAdminClient`

```python
from proxmox_sdk.ceph.providers import RGWAdminClient

async with RGWAdminClient(
    base_url="https://rgw.example.com:7480",
    access_key="AKIAIOSFODNN7EXAMPLE",
    secret_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
) as client:
    caps  = await client.capabilities()
    users = await client.users()
    buckets = await client.buckets()
```

### `RBDClient`

```python
from proxmox_sdk.ceph.providers import RBDClient

async with RBDClient(
    base_url="https://ceph-dashboard.example.com:8443",
    username="admin",
    password="secret",
) as client:
    images = await client.images(pool="rbd")
```

---

## `ProviderCapability` and `capabilities()`

Every direct provider client exposes `async capabilities() -> ProviderCapability`.
Higher layers (e.g. `proxbox-api`) call `capabilities()` to negotiate what a
provider can do before planning an operation.

```python
from proxmox_sdk.ceph.providers import DashboardCephClient, ProviderCapability

async with DashboardCephClient(...) as client:
    caps: ProviderCapability = await client.capabilities()

    print(f"provider:   {caps.provider}")
    print(f"available:  {caps.available}")
    print(f"version:    {caps.version}")
    print(f"read:       {caps.read}")
    print(f"write:      {caps.write}")
    print(f"metrics:    {caps.metrics}")

    # Fine-grained check
    if caps.supports("pool", "create"):
        await ceph.write.pool_create(node="pve1", name="my-pool")
    else:
        print("Pool creation not supported by this provider.")
```

`ProviderCapability.supports(kind, action)` uses the `operations` dict with a
priority chain (`kind:action` → `kind:*` → `action` → `kind`) before falling
back to the `read` flag for non-destructive operations.  Unknown write-like
actions always return `False` so the gate never fails open on a destructive op.

---

## See Also

- [SDK Guide](./sdk-guide.md) — Overview, backends, and core concepts
- [SDK Internals](./sdk-internals.md) — Services layer and transport details
- [Proxmox Backup Server HOW-TO](./sdk-pbs.md) — PBS datastores, snapshots, GC
- [Proxmox Datacenter Manager HOW-TO](./sdk-pdm.md) — PDM remotes and resources
- [Authentication Guide](./sdk-authentication.md) — Credential setup

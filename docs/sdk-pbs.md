# Proxmox Backup Server (PBS): HOW-TO Guide

Complete guide for managing Proxmox Backup Server using the SDK — from instantiating a session to managing datastores, snapshots, garbage collection, pruning, and monitoring tasks.

---

## Overview

PBS is a standalone Proxmox service for backup management. It runs on a separate host from PVE and has its own API and authentication system.

### PBS vs PVE Differences

| Aspect | PVE | PBS |
|--------|-----|-----|
| Default port | 8006 | **8007** |
| Auth cookie | `PVEAuthCookie` | `PBSAuthCookie` |
| Token separator | `=` | **`:`** |
| Token header example | `PVEAPIToken=user!name=value` | `PBSAPIToken=user!name:value` |
| Supported backends | https, ssh, local, mock | **https, mock only** |
| CLI equivalent | `pvesh` | None |

!!! warning "No SSH or Local Backend"
    PBS does not support the `ssh_paramiko`, `openssh`, or `local` backends.
    Unlike PVE, PBS has no `pvesh`-equivalent CLI tool. Only `https` and `mock`
    backends are available.

!!! tip "Token Header Format"
    The SDK handles the PBS token separator automatically. When you pass
    `token_name` and `token_value`, the SDK builds the correct
    `PBSAPIToken=user!name:value` header — no extra configuration needed.

---

## Session Setup

All examples below assume a connection object named `pbs`. Replace credentials with your actual values.

### Password Authentication

=== "Async (Recommended)"

    ```python
    import asyncio
    from proxmox_openapi import ProxmoxSDK

    async def main():
        async with ProxmoxSDK(
            host="pbs.example.com",
            user="admin@pam",
            password="secret",
            service="PBS",
            port=8007,
        ) as pbs:
            # Your code here
            pass

    asyncio.run(main())
    ```

=== "Sync (Blocking)"

    ```python
    from proxmox_openapi import ProxmoxSDK

    with ProxmoxSDK.sync(
        host="pbs.example.com",
        user="admin@pam",
        password="secret",
        service="PBS",
        port=8007,
    ) as pbs:
        # Your code here (blocking calls)
        pass
    ```

### Token Authentication (Recommended for Automation)

API tokens are preferred for automation: they do not expire and support fine-grained permissions.

=== "Async (Recommended)"

    ```python
    import asyncio
    from proxmox_openapi import ProxmoxSDK

    async def main():
        async with ProxmoxSDK(
            host="pbs.example.com",
            user="backup-operator@pam",
            token_name="automation",
            token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
            service="PBS",
            port=8007,
        ) as pbs:
            # Your code here
            pass

    asyncio.run(main())
    ```

=== "Sync (Blocking)"

    ```python
    from proxmox_openapi import ProxmoxSDK

    with ProxmoxSDK.sync(
        host="pbs.example.com",
        user="backup-operator@pam",
        token_name="automation",
        token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
        service="PBS",
        port=8007,
    ) as pbs:
        pass
    ```

### SSL Configuration

For PBS servers with self-signed certificates (common in homelab and internal environments):

```python
# Disable SSL verification — development only
ProxmoxSDK(
    host="pbs.example.com",
    user="admin@pam",
    password="secret",
    service="PBS",
    port=8007,
    verify_ssl=False,
)

# Or provide a custom CA certificate
ProxmoxSDK(
    host="pbs.example.com",
    user="admin@pam",
    password="secret",
    service="PBS",
    port=8007,
    cert="/etc/ssl/certs/pbs-ca.pem",
)
```

---

## Listing Datastores

Datastores are the primary storage units in PBS. Each datastore maps to a directory on the PBS host.

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        datastores = await pbs.admin.datastore.get()

        for ds in datastores:
            print(f"Datastore: {ds['store']}")
            print(f"  Path:    {ds.get('path', 'N/A')}")
            print(f"  Comment: {ds.get('comment', '')}")
            # Output:
            # Datastore: vm-backups
            #   Path:    /mnt/backup/vm-backups
            #   Comment: Production VM backups
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(..., service="PBS", port=8007) as pbs:
        datastores = pbs.admin.datastore.get()
        for ds in datastores:
            print(f"Datastore: {ds['store']}, Path: {ds.get('path', 'N/A')}")
    ```

### Datastore Details

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        # Get configuration of a specific datastore
        ds_config = await pbs.admin.datastore("vm-backups").config.get()

        print(f"Store:      {ds_config['store']}")
        print(f"Path:       {ds_config['path']}")
        print(f"GC Notify:  {ds_config.get('notify', 'always')}")
        print(f"Prune Jobs: {ds_config.get('prune-schedule', 'none')}")
    ```

### Datastore Usage

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        # Usage summary for all datastores
        usage_list = await pbs.status("datastore-usage").get()

        for usage in usage_list:
            store = usage["store"]
            total_gb = usage.get("total", 0) / 1024**3
            used_gb = usage.get("used", 0) / 1024**3
            avail_gb = usage.get("avail", 0) / 1024**3
            pct = (usage.get("used", 0) / usage.get("total", 1)) * 100

            print(f"{store}: {used_gb:.1f} GB / {total_gb:.1f} GB ({pct:.1f}% used, {avail_gb:.1f} GB free)")
            # Output:
            # vm-backups: 182.4 GB / 500.0 GB (36.5% used, 317.6 GB free)
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(..., service="PBS", port=8007) as pbs:
        usage_list = pbs.status("datastore-usage").get()
        for usage in usage_list:
            used_gb = usage.get("used", 0) / 1024**3
            total_gb = usage.get("total", 0) / 1024**3
            print(f"{usage['store']}: {used_gb:.1f} / {total_gb:.1f} GB")
    ```

---

## Working with Snapshots

Each backup in PBS is stored as a **snapshot** (also called a backup group entry). Snapshots are organized by backup type, backup ID, and timestamp.

### List Snapshots in a Datastore

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        snapshots = await pbs.admin.datastore("vm-backups").snapshots.get()

        for snap in snapshots:
            btype = snap["backup-type"]   # "vm", "ct", or "host"
            bid   = snap["backup-id"]     # e.g. "100" for VMID 100
            btime = snap["backup-time"]   # Unix timestamp
            size  = snap.get("size", 0) / 1024**3

            print(f"{btype}/{bid}  @ {btime}  ({size:.2f} GB)")
            # Output:
            # vm/100  @ 1710000000  (4.31 GB)
            # vm/101  @ 1710003600  (2.17 GB)
            # ct/200  @ 1710007200  (0.84 GB)
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(..., service="PBS", port=8007) as pbs:
        snapshots = pbs.admin.datastore("vm-backups").snapshots.get()
        for snap in snapshots:
            print(f"{snap['backup-type']}/{snap['backup-id']} @ {snap['backup-time']}")
    ```

### Filter Snapshots by Type

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        snapshots = await pbs.admin.datastore("vm-backups").snapshots.get()

        # Only VM backups
        vm_snaps = [s for s in snapshots if s["backup-type"] == "vm"]

        print(f"Found {len(vm_snaps)} VM snapshots:")
        for snap in vm_snaps:
            print(f"  VM {snap['backup-id']} — {snap['backup-time']}")
    ```

### Delete a Snapshot

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        # Delete a specific snapshot
        await pbs.admin.datastore("vm-backups").snapshots.delete(
            **{
                "backup-type": "vm",
                "backup-id": "100",
                "backup-time": 1710000000,
            }
        )
        print("Snapshot deleted")
    ```

---

## Garbage Collection

Garbage collection (GC) reclaims disk space from deleted or pruned backup chunks that are no longer referenced.

=== "Async"

    ```python
    from proxmox_openapi import ProxmoxSDK
    from proxmox_openapi.sdk.tools import Tasks

    async def run_garbage_collection(store: str):
        async with ProxmoxSDK(
            host="pbs.example.com",
            user="admin@pam",
            password="secret",
            service="PBS",
            port=8007,
        ) as pbs:
            print(f"Starting GC on datastore '{store}'...")

            result = await pbs.admin.datastore(store).gc.post()
            task_id = result.get("upid") if isinstance(result, dict) else result

            if task_id:
                tasks = Tasks(pbs)
                status = await tasks.wait_task(task_id, timeout=3600)
                print(f"GC completed: {status}")
            else:
                print(f"GC triggered (no task ID returned): {result}")

    import asyncio
    asyncio.run(run_garbage_collection("vm-backups"))
    ```

=== "Sync"

    ```python
    from proxmox_openapi import ProxmoxSDK
    from proxmox_openapi.sdk.tools import Tasks

    with ProxmoxSDK.sync(
        host="pbs.example.com",
        user="admin@pam",
        password="secret",
        service="PBS",
        port=8007,
    ) as pbs:
        result = pbs.admin.datastore("vm-backups").gc.post()
        print(f"GC task started: {result}")
    ```

---

## Verification Jobs

Verification confirms that all backup chunks for a datastore are intact and readable.

=== "Async"

    ```python
    from proxmox_openapi import ProxmoxSDK
    from proxmox_openapi.sdk.tools import Tasks

    async def verify_datastore(store: str, ignore_verified: bool = True):
        """Run a verification job on a PBS datastore."""
        async with ProxmoxSDK(
            host="pbs.example.com",
            user="admin@pam",
            password="secret",
            service="PBS",
            port=8007,
        ) as pbs:
            print(f"Verifying datastore '{store}'...")

            result = await pbs.admin.datastore(store).verify.post(
                **{"ignore-verified": ignore_verified},  # Skip already-verified chunks
            )
            task_id = result.get("upid") if isinstance(result, dict) else result

            if task_id:
                tasks = Tasks(pbs)
                status = await tasks.wait_task(task_id, timeout=7200)
                print(f"Verification complete: {status}")

    import asyncio
    asyncio.run(verify_datastore("vm-backups"))
    ```

=== "Sync"

    ```python
    from proxmox_openapi import ProxmoxSDK

    with ProxmoxSDK.sync(
        host="pbs.example.com",
        user="admin@pam",
        password="secret",
        service="PBS",
        port=8007,
    ) as pbs:
        result = pbs.admin.datastore("vm-backups").verify.post()
        print(f"Verification started: {result}")
    ```

---

## Pruning Old Backups

Pruning removes old snapshots from a datastore according to a retention policy. The policy is defined by how many backups to keep across different time intervals.

### Prune a Specific Backup Group

=== "Async"

    ```python
    from proxmox_openapi import ProxmoxSDK
    from proxmox_openapi.sdk.tools import Tasks

    async def prune_vm_backups(store: str, vmid: int):
        """Prune backups for a specific VM, keeping recent copies."""
        async with ProxmoxSDK(
            host="pbs.example.com",
            user="admin@pam",
            password="secret",
            service="PBS",
            port=8007,
        ) as pbs:
            result = await pbs.admin.datastore(store).prune.post(
                **{
                    "backup-type": "vm",
                    "backup-id": str(vmid),
                    "keep-last":    3,   # Keep the 3 most recent backups
                    "keep-daily":   7,   # Keep 1 backup per day for 7 days
                    "keep-weekly":  4,   # Keep 1 per week for 4 weeks
                    "keep-monthly": 3,   # Keep 1 per month for 3 months
                    "keep-yearly":  1,   # Keep 1 per year
                }
            )
            task_id = result.get("upid") if isinstance(result, dict) else result

            if task_id:
                tasks = Tasks(pbs)
                status = await tasks.wait_task(task_id, timeout=600)
                print(f"Prune complete for VM {vmid}: {status}")
            else:
                print(f"Prune result: {result}")

    import asyncio
    asyncio.run(prune_vm_backups("vm-backups", vmid=100))
    ```

=== "Sync"

    ```python
    from proxmox_openapi import ProxmoxSDK

    with ProxmoxSDK.sync(
        host="pbs.example.com",
        user="admin@pam",
        password="secret",
        service="PBS",
        port=8007,
    ) as pbs:
        result = pbs.admin.datastore("vm-backups").prune.post(
            **{
                "backup-type": "vm",
                "backup-id": "100",
                "keep-last":  3,
                "keep-daily": 7,
            }
        )
        print(f"Prune result: {result}")
    ```

### Dry Run (Preview What Would Be Deleted)

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        # dry_run=1 shows what would be pruned without deleting
        result = await pbs.admin.datastore("vm-backups").prune.post(
            **{
                "backup-type": "vm",
                "backup-id": "100",
                "keep-last":  3,
                "keep-daily": 7,
                "dry-run":    1,
            }
        )
        print("Dry run — backups that would be removed:")
        if isinstance(result, list):
            for snap in result:
                action = snap.get("action", "unknown")
                ts     = snap.get("backup-time", "?")
                print(f"  [{action}] backup-time={ts}")
    ```

---

## Node Status and Monitoring

### List PBS Nodes

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        nodes = await pbs.nodes.get()

        for node in nodes:
            print(f"Node: {node['node']} ({node.get('status', 'unknown')})")
            # Output:
            # Node: pbs1 (online)
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(..., service="PBS", port=8007) as pbs:
        nodes = pbs.nodes.get()
        for node in nodes:
            print(f"Node: {node['node']}")
    ```

### Node Resource Status

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        status = await pbs.nodes("pbs1").status.get()

        uptime_h = status.get("uptime", 0) / 3600
        cpu_pct  = status.get("cpu", 0) * 100
        mem_used = status.get("memory", {}).get("used", 0) / 1024**3
        mem_total= status.get("memory", {}).get("total", 1) / 1024**3

        print(f"Uptime:  {uptime_h:.1f} hours")
        print(f"CPU:     {cpu_pct:.1f}%")
        print(f"Memory:  {mem_used:.1f} GB / {mem_total:.1f} GB")
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(..., service="PBS", port=8007) as pbs:
        status = pbs.nodes("pbs1").status.get()
        print(f"CPU: {status.get('cpu', 0) * 100:.1f}%")
    ```

---

## Task Monitoring

Long-running PBS operations (GC, verify, prune) return a task UPID. You can monitor these tasks directly.

### List Recent Tasks

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        tasks = await pbs.nodes("pbs1").tasks.get()

        print("Recent tasks:")
        for task in tasks[:10]:
            upid   = task.get("upid", "?")
            status = task.get("status", "running")
            wtype  = task.get("type", "?")
            print(f"  [{status}] {wtype} — {upid}")
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(..., service="PBS", port=8007) as pbs:
        tasks = pbs.nodes("pbs1").tasks.get()
        for task in tasks[:5]:
            print(f"  {task.get('type')}: {task.get('status')}")
    ```

### Check Task Status

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        upid = "UPID:pbs1:00001234:00000001:..."

        task_status = await pbs.nodes("pbs1").tasks(upid).status.get()
        print(f"Status:    {task_status.get('status')}")
        print(f"Exit code: {task_status.get('exitstatus', 'running')}")
    ```

### Read Task Log

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        upid = "UPID:pbs1:00001234:00000001:..."

        log = await pbs.nodes("pbs1").tasks(upid).log.get()
        for line in log:
            print(line.get("t", ""))  # "t" contains the log text
    ```

### Wait for Task with Timeout

Use the built-in `Tasks` tool to poll until a task finishes:

=== "Async"

    ```python
    from proxmox_openapi.sdk.tools import Tasks

    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        # Start a GC job
        result = await pbs.admin.datastore("vm-backups").gc.post()
        task_id = result.get("upid") if isinstance(result, dict) else result

        # Wait up to 30 minutes
        tasks_tool = Tasks(pbs)
        final_status = await tasks_tool.wait_task(task_id, timeout=1800)
        print(f"Task finished with: {final_status}")
    ```

---

## User and Token Management

### List PBS Users

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        users = await pbs.access.users.get()

        for user in users:
            print(f"User: {user['userid']}")
            if user.get("comment"):
                print(f"  Comment: {user['comment']}")
            if user.get("expire"):
                print(f"  Expires: {user['expire']}")
    ```

=== "Sync"

    ```python
    with ProxmoxSDK.sync(..., service="PBS", port=8007) as pbs:
        users = pbs.access.users.get()
        for user in users:
            print(user["userid"])
    ```

### Create a PBS User

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        await pbs.access.users.post(
            userid="backup-operator@pam",
            comment="Automation service account",
        )
        print("User created")
    ```

### List API Tokens for a User

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        tokens = await pbs.access.users("admin@pam").token.get()

        for token in tokens:
            print(f"Token: {token['tokenid']}")
            if token.get("comment"):
                print(f"  Comment: {token['comment']}")
    ```

### Create an API Token

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        result = await pbs.access.users("backup-operator@pam").token("automation").post(
            comment="CI/CD automation token",
        )

        # IMPORTANT: The token secret is only shown once on creation
        token_value = result.get("value")
        print(f"Token created. Secret (save now): {token_value}")
        print(f"Connect using: PBSAPIToken=backup-operator@pam!automation:{token_value}")
    ```

### List Auth Realms (Domains)

=== "Async"

    ```python
    async with ProxmoxSDK(..., service="PBS", port=8007) as pbs:
        domains = await pbs.access.domains.get()

        for domain in domains:
            print(f"Realm: {domain['realm']} (type: {domain['type']})")
            # Output:
            # Realm: pam (type: pam)
            # Realm: pbs (type: pbs)
    ```

---

## Real-World Examples

### Example 1: Automated Backup Maintenance

Run garbage collection, verify, and prune in sequence for all datastores:

=== "Async"

    ```python
    import asyncio
    from proxmox_openapi import ProxmoxSDK
    from proxmox_openapi.sdk.tools import Tasks

    async def maintenance_all_datastores():
        """Run GC → verify → prune on every datastore."""
        async with ProxmoxSDK(
            host="pbs.example.com",
            user="admin@pam",
            password="secret",
            service="PBS",
            port=8007,
        ) as pbs:
            datastores = await pbs.admin.datastore.get()
            tasks_tool = Tasks(pbs)

            for ds in datastores:
                store = ds["store"]
                print(f"\n=== Maintaining datastore: {store} ===")

                # Step 1: Garbage collection
                print("  [1/3] Running garbage collection...")
                result = await pbs.admin.datastore(store).gc.post()
                task_id = result.get("upid") if isinstance(result, dict) else result
                if task_id:
                    await tasks_tool.wait_task(task_id, timeout=3600)
                print("  GC done.")

                # Step 2: Verify all chunks
                print("  [2/3] Verifying chunks...")
                result = await pbs.admin.datastore(store).verify.post(
                    **{"ignore-verified": True}
                )
                task_id = result.get("upid") if isinstance(result, dict) else result
                if task_id:
                    await tasks_tool.wait_task(task_id, timeout=7200)
                print("  Verification done.")

                # Step 3: Prune — each backup group needs a separate call
                print("  [3/3] Pruning old snapshots...")
                snapshots = await pbs.admin.datastore(store).snapshots.get()

                # Collect unique backup groups
                groups = {
                    (s["backup-type"], s["backup-id"])
                    for s in snapshots
                }

                for btype, bid in groups:
                    result = await pbs.admin.datastore(store).prune.post(
                        **{
                            "backup-type": btype,
                            "backup-id":   bid,
                            "keep-last":   3,
                            "keep-daily":  7,
                            "keep-weekly": 4,
                        }
                    )
                    task_id = result.get("upid") if isinstance(result, dict) else result
                    if task_id:
                        await tasks_tool.wait_task(task_id, timeout=300)

                print("  Pruning done.")
                print(f"=== {store} maintenance complete ===")

    asyncio.run(maintenance_all_datastores())
    ```

---

### Example 2: Datastore Health Report

Generate a summary of datastore usage and snapshot counts:

=== "Async"

    ```python
    import asyncio
    from proxmox_openapi import ProxmoxSDK

    async def datastore_health_report():
        async with ProxmoxSDK(
            host="pbs.example.com",
            user="admin@pam",
            password="secret",
            service="PBS",
            port=8007,
        ) as pbs:
            datastores = await pbs.admin.datastore.get()
            usage_map  = {
                u["store"]: u
                for u in await pbs.status("datastore-usage").get()
            }

            print("\n" + "=" * 65)
            print("PROXMOX BACKUP SERVER — DATASTORE HEALTH REPORT")
            print("=" * 65)

            for ds in datastores:
                store = ds["store"]
                usage = usage_map.get(store, {})

                total_gb = usage.get("total", 0) / 1024**3
                used_gb  = usage.get("used",  0) / 1024**3
                avail_gb = usage.get("avail", 0) / 1024**3
                pct      = (used_gb / total_gb * 100) if total_gb else 0

                snapshots = await pbs.admin.datastore(store).snapshots.get()

                vm_count  = sum(1 for s in snapshots if s["backup-type"] == "vm")
                ct_count  = sum(1 for s in snapshots if s["backup-type"] == "ct")
                host_count= sum(1 for s in snapshots if s["backup-type"] == "host")

                print(f"\nDatastore: {store}")
                print(f"  Path:      {ds.get('path', 'N/A')}")
                print(f"  Usage:     {used_gb:.1f} GB / {total_gb:.1f} GB ({pct:.1f}%)")
                print(f"  Free:      {avail_gb:.1f} GB")
                print(f"  Snapshots: {len(snapshots)} total "
                      f"(VM: {vm_count}, CT: {ct_count}, Host: {host_count})")

                if pct > 85:
                    print("  *** WARNING: datastore is more than 85% full ***")

            print("\n" + "=" * 65)

    asyncio.run(datastore_health_report())
    ```

---

## Common Parameters Reference

### Prune Retention Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `keep-last` | int | Keep the N most recent backups regardless of time |
| `keep-daily` | int | Keep one backup per day for the last N days |
| `keep-weekly` | int | Keep one backup per week for the last N weeks |
| `keep-monthly` | int | Keep one backup per month for the last N months |
| `keep-yearly` | int | Keep one backup per year for the last N years |
| `keep-hourly` | int | Keep one backup per hour for the last N hours |
| `dry-run` | int (`1`) | Preview what would be pruned without deleting |

!!! tip "Retention Policy Interaction"
    Parameters are applied in combination. A snapshot is kept if it matches
    **any** active retention rule. Set only the parameters you need — omitting
    a parameter means that rule is not enforced.

### Backup Types

| Value | Description |
|-------|-------------|
| `vm` | QEMU/KVM virtual machine backup |
| `ct` | LXC container backup |
| `host` | PBS host/system backup |

---

## Troubleshooting

### Connection Refused on Default Port

PBS listens on **port 8007**, not 8006. Always pass `port=8007` explicitly:

```python
ProxmoxSDK(
    host="pbs.example.com",
    user="admin@pam",
    password="secret",
    service="PBS",
    port=8007,   # Required — PBS is not on port 8006
)
```

### SSH or Local Backend Raises `ValueError`

PBS does not support SSH or local backends:

```python
# This raises: ValueError: Backend 'ssh_paramiko' is not supported for service 'PBS'
ProxmoxSDK(host="pbs.example.com", user="root", password="s", service="PBS", backend="ssh_paramiko")
```

Use `backend="https"` (default) or `backend="mock"` for testing.

### Token Authentication Fails

PBS uses a **colon** (`:`) as the token separator, not an equals sign (`=`). The SDK handles this automatically — make sure you pass `service="PBS"` so the correct format is used:

```python
# Wrong — PVE token format (= separator)
# Authorization: PVEAPIToken=user!name=value

# Correct — SDK builds the PBS header automatically when service="PBS"
ProxmoxSDK(
    host="pbs.example.com",
    user="admin@pam",
    token_name="my-token",
    token_value="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    service="PBS",   # Critical: ensures PBSAPIToken header format
    port=8007,
)
# Authorization: PBSAPIToken=admin@pam!my-token:xxxxxxxx-...
```

### Permission Denied on Datastore Operations

PBS has its own ACL system separate from PVE. The user/token needs the `DatastoreAdmin` or `DatastoreBackup` role on the specific datastore path:

```
Path:  /datastore/vm-backups
Role:  DatastoreAdmin
User:  backup-operator@pam
```

Configure this in the PBS web UI under **Configuration → Access Control**.

### SSL Certificate Error

PBS typically uses a self-signed certificate. For production, either:

```python
# Option 1: Provide the PBS CA certificate
ProxmoxSDK(..., service="PBS", port=8007, cert="/etc/pve/pbs-ca.pem")

# Option 2: Disable verification (development only)
ProxmoxSDK(..., service="PBS", port=8007, verify_ssl=False)
```

---

## See Also

- [SDK Guide](./sdk-guide.md) — Overview, backends, and core concepts
- [Authentication Guide](./sdk-authentication.md) — Detailed credential setup
- [Virtual Machines Guide](./sdk-virtual-machines.md) — Managing PVE VMs
- [Examples & Recipes](./sdk-examples.md) — Backup, cluster, and monitoring examples
- [API Reference](./api-reference.md) — Complete endpoint documentation

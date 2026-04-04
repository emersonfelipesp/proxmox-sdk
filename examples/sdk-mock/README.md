An index of Proxmox SDK mock usage examples.

## Running Examples

All examples can be run directly:

```bash
# Run a specific example
python examples/sdk-mock/01_basic_async.py
python examples/sdk-mock/02_basic_sync.py

# Or using the installed package
proxmox-openapi-example-01
```

## Example List

| # | Example | Description | Type |
|---|---------|-------------|------|
| 1 | [01_basic_async.py](01_basic_async.py) | Basic SDK usage with async/await | Async |
| 2 | [02_basic_sync.py](02_basic_sync.py) | Basic SDK usage with sync wrapper (no async) | Sync |
| 3 | [03_crud_operations.py](03_crud_operations.py) | Create, Read, Update, Delete workflows | Async |
| 4 | [04_testing.py](04_testing.py) | Using mock SDK for unit tests | Async |
| 5 | [05_multi_service.py](05_multi_service.py) | Multi-service support (PVE, PMG, PBS) | Async |
| 6 | [06_schema_versions.py](06_schema_versions.py) | Schema version selection | Async |
| 7 | [07_error_handling.py](07_error_handling.py) | Error handling and exception catching | Async |

## Quick Start

**Async (with async/await):**
```python
from proxmox_openapi.sdk import ProxmoxSDK

async with ProxmoxSDK.mock() as proxmox:
    nodes = await proxmox.nodes.get()
    print(nodes)
```

**Sync (without async/await):**
```python
from proxmox_openapi.sdk import ProxmoxSDK

with ProxmoxSDK.sync_mock() as proxmox:
    nodes = proxmox.nodes.get()
    print(nodes)
```

## Key Points

- ✅ **Zero setup** — No real Proxmox server required
- ✅ **In-memory mock data** — Deterministic, seed-based generation
- ✅ **CRUD support** — Create, read, update, delete operations
- ✅ **State persistence** — Changes persist during runtime
- ⚠️ **Memory-only** — State resets when SDK instance closes

For more information, see [SDK Mock Documentation](../../docs/sdk-mock.md).

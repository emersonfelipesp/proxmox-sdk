# Performance

This document describes the performance characteristics of proxmox-sdk and the
optimisations applied to startup time, per-request throughput, and the SDK hot
paths. It focuses on the v0.0.8 performance work: generated route metadata,
lazy Pydantic model shards, SQLite/WAL mock state, optional faster JSON
serialization, and the decision to keep native acceleration at the ASGI server
boundary through the Granian Docker image.

The short version: proxmox-sdk stays Python-first internally. The largest wins
came from doing less work at startup and from changing the mock-state storage
shape. A custom Rust/PyO3 extension would add packaging and maintenance cost
without addressing the largest bottlenecks that were measured.

---

## v0.0.8 Performance Summary

| Area | Change | Result |
|---|---|---|
| Route registration | Load generated `route_metadata.json` instead of rebuilding topology from OpenAPI | Startup avoids repeated topology, path, and child-relationship derivation |
| Pydantic models | Lazy-load `models/<group>.py` shards using `model_index.json` | App import no longer executes the full aggregate `pydantic_models.py` module |
| Mock state | Default to SQLite rows in WAL mode | Avoids whole-state JSON serialization under a process-wide lock |
| Serialization | Use `orjson` when installed, stdlib `json` otherwise | Faster payload blob encoding without custom native code |
| Server runtime | Keep using the Granian Docker variant for Rust ASGI/TLS | Native HTTP server gains without changing package internals |
| CI guards | Verify metadata/model indexes for every supported schema tag | Prevents stale generated artifacts from shipping |

## Startup Time

### Lazy package imports

`import proxmox_sdk` no longer constructs any FastAPI app or imports the SDK. All top-level exports are resolved on first attribute access via `__getattr__`. This means:

- CLI tools that `import proxmox_sdk` for `__version__` or SDK classes start without paying the FastAPI app construction cost.
- The `app` and `mock_app` attributes are only materialised when accessed (e.g. by uvicorn).

### Generated route metadata

675 operations across 449 Proxmox VE 9.2 paths are registered at startup.
Runtime registration now prefers pre-generated `route_metadata.json` artifacts,
so it does not rebuild topology, parameter maps, mounted paths, model names, and
child collection relationships from OpenAPI on every app import.

| Step | Before | After |
|---|---|---|
| Child path discovery | O(P²) scan across every path pair | O(P) single-pass index during codegen |
| Schema fingerprint | `model_dump` + `json.dumps` + `sha256` on every call | Computed once, cached as `@cached_property` |
| Route topology | Derived from OpenAPI during startup | Loaded from `route_metadata.json` |
| Generated Pydantic models | Full module generated and executed during startup | Route-group model shards lazy-load on first use |

The codegen pipeline writes three runtime artifacts per schema version:

- `route_metadata.json` — mounted paths, operation IDs, parameter metadata, and mock topology.
- `model_index.json` — operation-to-model and operation-to-shard lookup.
- `models/<group>.py` — lazy Pydantic model shards grouped by first API path segment.

The runtime loading path is:

1. `register_generated_proxmox_mock_routes()` loads the bundled OpenAPI document
   for the selected `PROXMOX_MOCK_SCHEMA_VERSION`.
2. It calls `load_route_metadata(version_tag)`.
3. If `route_metadata.json` is present, route registration iterates the metadata
   routes and builds lightweight FastAPI dispatcher closures.
4. Each dispatcher uses the precomputed mounted path, operation ID, parameter
   metadata, request schema, response schema, and mock topology.
5. The generated OpenAPI document is merged directly into `/openapi.json`.

FastAPI routes are registered as lightweight request dispatchers and excluded
from automatic schema generation. The application merges the bundled generated
OpenAPI paths into `/openapi.json`, preserving Swagger/ReDoc detail without
importing every generated model at startup.

If metadata is missing, the route builder falls back to the older OpenAPI
walk. That fallback is intentionally retained for development and compatibility,
but the shipped package and CI-tested schemas use the metadata path.

### Lazy Pydantic model shards

The aggregate `pydantic_models.py` file still ships for compatibility, but it is
no longer the primary startup path. The codegen pipeline also writes
`models/<group>.py` files and `model_index.json`:

```text
proxmox_sdk/generated/proxmox/latest/
├── openapi.json
├── pydantic_models.py       # compatibility aggregate
├── route_metadata.json      # route registration input
├── model_index.json         # operation -> shard/model lookup
└── models/
    ├── access.py
    ├── cluster.py
    ├── nodes.py
    ├── pools.py
    ├── storage.py
    └── version.py
```

When a route needs a request or response model, the runtime asks
`load_operation_model(version_tag, operation_id, role)`. That function reads the
operation entry from `model_index.json`, imports only the matching
`models/<group>.py` shard, rebuilds models in that module, and returns the
specific class. Requests to `/api2/json/nodes` therefore import the `nodes`
shard and do not import the aggregate module.

The behavior is covered by `tests/mock/test_routes.py`, which asserts that
loading `get_nodes` imports `proxmox_sdk._generated_models.<tag>.nodes` and
does not import the aggregate module.

---

## Per-Request Throughput (Mock Mode)

### SQLite/WAL state store

The default mock state backend is now `SQLiteMockStore`, selected by
`PROXMOX_MOCK_STORE=sqlite` or by leaving the variable unset. It stores objects,
collection members, and tombstones as separate SQLite rows instead of serialising
the entire mock state into one shared-memory JSON blob for every read/write.

Configuration:

```bash
PROXMOX_MOCK_STORE=sqlite              # default
PROXMOX_MOCK_STATE_PATH=/tmp/mock.db   # optional explicit DB path
PROXMOX_MOCK_STORE=shared-memory       # legacy shared-memory backend
PROXMOX_MOCK_STORE=dict                # process-local test fallback
```

SQLite runs in WAL mode with a per-process connection and still resets state
when the loaded schema fingerprint changes. Instead of storing one global JSON
object, it stores separate rows for:

- scalar/object resources
- collection members
- tombstones for deleted resources
- metadata, including the active schema fingerprint

This matters more than Python-versus-Rust serialization for realistic mock
state sizes. Whole-state JSON serialization under a lock makes every request
pay for unrelated mock data. Row-level storage keeps reads and writes scoped to
the resource path being accessed.

Payload blobs use `orjson` when it is installed, falling back to the standard
`json` module otherwise. This is the preferred native-speed JSON path before
considering custom PyO3 serialization.

### Shared-memory locking

The legacy shared-memory backend remains available and is backed by a shared-memory segment protected by a filesystem lock (`fcntl.flock`).

| Operation | Before | After |
|---|---|---|
| Read (GET) | `LOCK_EX` — serialises all readers | `LOCK_SH` — concurrent reads allowed |
| Write (POST/PUT/DELETE) | `LOCK_EX` | `LOCK_EX` (unchanged) |

Concurrent GET requests no longer block each other.

### Deleted-item tracking

The set of deleted keys was stored as a JSON list (O(n) membership checks). It is now materialised as a Python `set` during each request (O(1) checks) and serialised back to a list only when writing state.

---

## SDK Hot Paths

### URL construction (`https.py`)

`_url_for()` is called on every API request to join the base URL with the request path. Previously it re-parsed `self._base_url` with `urlsplit`/`urlunsplit` on every call.

Now the components `(scheme, netloc, base_path)` are parsed once in `__init__` and reused:

```python
# __init__
_parsed = urlsplit(self._base_url)
self._base_scheme = _parsed.scheme
self._base_netloc = _parsed.netloc
self._base_path = _parsed.path or "/"

# _url_for (called per-request)
joined = posixpath.join(self._base_path, path.lstrip("/"))
return urlunsplit((self._base_scheme, self._base_netloc, joined, "", ""))
```

`posixpath` is now a top-level module import instead of a deferred `import posixpath` inside the method.

### Path joining (`resource.py`)

`_url_join()` is called on every attribute navigation step (`proxmox.nodes`, `.qemu`, etc.). A fast path now avoids `urlsplit`/`urlunsplit` for plain path strings (no `://`), which is the common case for SDK usage:

```python
def _url_join(base: str, *args: str) -> str:
    if "://" not in base:
        return posixpath.join(base or "/", *[str(a) for a in args])
    # full URL parsing only for absolute URLs
    ...
```

### None filtering (`resource.py`)

`_filter_none()` is called once per HTTP method to strip `None` values from params/data dicts. A fast path skips the dict comprehension when no `None` values are present (common for well-formed requests):

```python
def _filter_none(d: dict) -> dict:
    if all(v is not None for v in d.values()):
        return d  # avoid allocation
    return {k: v for k, v in d.items() if v is not None}
```

---

## Task Polling

`Tasks.blocking_status()` previously polled at a fixed interval (2 s), which means:

- Short tasks were checked 2 s late on average.
- Long tasks (VM migrations, backups) generated many unnecessary API calls.

It now uses **exponential backoff**:

```
1s → 2s → 4s → 8s → 16s → 30s (cap)
```

Timeout tracking uses `time.monotonic()` for accurate wall-clock measurement instead of cumulative addition (which underestimates actual elapsed time by the duration of each HTTP request).

---

## Request Retry

`HttpsBackend.request()` supports opt-in automatic retry for transient failures.

### When retries occur

| Condition | Retried? |
|---|---|
| HTTP 502, 503, 504 | Yes (GET/HEAD only) |
| `asyncio.TimeoutError` | Yes (GET/HEAD only) |
| `aiohttp.ClientError` (DNS, refused, etc.) | Yes (GET/HEAD only) |
| SSL error | Never (not transient) |
| HTTP 4xx (client error) | Never |
| POST / PUT / DELETE | Never (not safe to duplicate) |

### Backoff strategy

Retries use exponential backoff:

```
attempt 1: backoff * 2⁰  → 0.5s
attempt 2: backoff * 2¹  → 1.0s
attempt 3: backoff * 2²  → 2.0s
…                          (capped at 30s)
```

Default `max_retries=0` preserves existing behaviour with no delay or overhead on the hot path.

### Configuration

```python
ProxmoxSDK(
    host="pve.example.com",
    user="admin@pam", password="secret",
    max_retries=3,       # 3 retries = 4 total attempts
    retry_backoff=0.5,   # 0.5s, 1.0s, 2.0s
)
```

Or via environment:

```bash
PROXMOX_API_RETRIES=3
PROXMOX_API_RETRY_BACKOFF=0.5
```

---

## Runtime Server

The project keeps native server acceleration at the ASGI boundary. Use the
existing Granian Docker variant when you want a Rust-based HTTP/TLS server
without adding PyO3 or native extensions to the SDK internals:

```bash
docker run -p 8443:8000 emersonfelipesp/proxmox-sdk:latest-granian
```

The SDK, route metadata, lazy model loading, and mock state code remain pure
Python so source installs and generated artifacts stay simple.

### Why not a custom Rust/PyO3 extension?

The measured bottlenecks were not "Python loops are slow" in isolation. They
were:

- repeated OpenAPI topology work during startup
- eager import and execution of the full generated model module
- whole-state JSON serialization under locks
- ASGI/server overhead that is already handled by Granian

PyO3 would not remove the need to generate route metadata, shard models, or
change the mock-state storage shape. It would also introduce native build
requirements for a package that currently installs as pure Python. The current
policy is therefore:

1. pre-generate static route metadata where the schema is already known
2. lazy-load generated Python models by route group
3. use proven serializers such as `orjson` or `msgspec` before custom native code
4. fix the storage design if state grows beyond SQLite/WAL needs
5. use Granian for Rust-native ASGI/server wins

Revisit PyO3 only if profiling shows a narrow, stable CPU hotspot that remains
after those design issues are addressed and cannot be solved with an existing
native dependency.

---

## Config Loading

`ProxmoxConfig.from_env()` previously copied the entire `os.environ` dict (50–200+ keys) on every call. It now reads only the ~20 specific keys it needs:

```python
_KEYS = (
    "PROXMOX_API_MODE", "PROXMOX_API_URL", "PROXMOX_API_TOKEN_ID", ...
)
env_config = {k: v for k in _KEYS if (v := os.environ.get(k)) is not None}
```

`yaml` (PyYAML) is only imported when a YAML config file is actually present, avoiding a heavy import on every startup.

---

## Dead Code Removed

`mock/schema_helpers.py` previously contained ~200 lines of private functions (`_seed_int`, `_field_hint`, `_semantic_string_value`, etc.) that duplicated the same logic inside `ProxmoxSchemaValue` in `schema.py`. None of the module's public functions called these copies — they all delegated directly to `ProxmoxSchemaValue`. The dead code was removed, reducing module load time and memory footprint.

---

## Regex Pre-compilation

The pattern `r"(^|_)name$"` used in semantic mock value generation was previously compiled on every call via `re.search(pattern, hint)`. It is now compiled once at module load:

```python
_RE_NAME_HINT = re.compile(r"(^|_)name$")
```

---

## CI and Packaging Guards

The generated performance artifacts are part of the package contract. They are
included through `pyproject.toml` package data:

```toml
[tool.setuptools.package-data]
proxmox_sdk = [
    "generated/proxmox/**/*.json",
    "generated/proxmox/**/*.py",
]
```

The integrity tests check all supported schema tags (`latest`, `9.2`, and
`9.1.11`):

- `openapi.json` SHA matches the generated model metadata
- `route_metadata.json` source SHA matches `openapi.json`
- route count and path count match the OpenAPI document
- every operation in `route_metadata.json` is covered by `model_index.json`
- every shard listed by `model_index.json` exists under `models/`

Run the focused guard suite locally with:

```bash
uv run pytest tests/test_generated_integrity.py tests/mock/test_routes.py
```

The GitHub CI and release workflows run the full test suite across:

```bash
PROXMOX_MOCK_SCHEMA_VERSION=latest
PROXMOX_MOCK_SCHEMA_VERSION=9.2
PROXMOX_MOCK_SCHEMA_VERSION=9.1.11
```

The scheduled/manual schema update workflow also runs `proxmox-sdk-codegen`.
That command writes `route_metadata.json`, `model_index.json`, and
`models/<group>.py` for both the package-internal tree and the source-of-record
`generated/proxmox/` tree.

---

## Performance Characteristics (Updated)

### Mock Mode

| Metric | Value |
|---|---|
| Startup (schema load + route registration) | ~2.1 s full app import in local smoke test |
| Route registration only | ~0.75 s in local smoke test |
| Request latency (SQLite/WAL, warm state) | ~4 ms via local TestClient smoke test |
| Concurrent read throughput | SQLite WAL readers avoid whole-state JSON serialisation |
| Memory (schema + state) | ~100 MB |

### Real Mode

| Metric | Value |
|---|---|
| Startup | ~500 ms |
| Request latency | Proxmox latency + ~10–20 ms validation overhead |
| Memory | ~80 MB |

### SDK

| Operation | Notes |
|---|---|
| First request | One SSL context build + one session open |
| Subsequent requests | Connection reused from aiohttp pool |
| Ticket renewal | Automatic, uses same SSL context as API requests |
| Task polling | Exponential backoff, accurate monotonic timeout |

---

## Profiling Tips

To measure startup time:

```bash
python -c "
import time
t0 = time.perf_counter()
from proxmox_sdk.main import app
print(f'app ready in {time.perf_counter() - t0:.3f}s')
"
```

To measure mock route registration specifically:

```bash
python -c "
import time, json
from proxmox_sdk.mock.routes import register_generated_proxmox_mock_routes
from proxmox_sdk.schema import load_proxmox_generated_openapi
from fastapi import FastAPI

doc = load_proxmox_generated_openapi()
app = FastAPI()
t0 = time.perf_counter()
register_generated_proxmox_mock_routes(app, openapi_document=doc)
print(f'route registration: {time.perf_counter() - t0:.3f}s')
"
```

# proxmox-sdk Agent Index — AGENTS.md Mirror

This file mirrors the sibling `CLAUDE.md` guidance for agents that read `AGENTS.md`. Treat `CLAUDE.md` as the source material; the content below preserves the current guide.

## Source

@CLAUDE.md

---

# proxmox-sdk Agent Index

## Workspace Context

This file lives at `/root/personal-context/nmulticloud-context/proxmox-sdk/CLAUDE.md` inside the `personal-context` workspace.
Workspace guidance: `/root/personal-context/CLAUDE.md`.
Per-repo deep-dive: `/root/personal-context/claude-reference/proxmox-sdk.md`.
Submodule layout and cross-repo links: `/root/personal-context/claude-reference/dependency-map.md`.

---

## Overview

`proxmox-sdk` is a schema-driven FastAPI package for Proxmox API that provides:

1. **Dual-mode operation** - Mock mode (default, in-memory CRUD) or Real mode (proxy to actual Proxmox)
2. **Standalone Python SDK** - Production-ready SDK without FastAPI server (async + sync)
3. **CLI + TUI** - Typer CLI and Textual terminal UI for interactive use
4. **Codegen pipeline** - Automatically crawl Proxmox API Viewer and convert to OpenAPI schema
5. **675 operations / 444 endpoints** - Pre-generated Proxmox VE 9.2 API with full OpenAPI schema (9.1.11 retained for backward compatibility)
6. **318 operations / 246 endpoints** - Pre-generated Proxmox Datacenter Manager (PDM) API with strict typed read-boundary validation
7. **Rate limiting** - Built-in protection via SlowAPI

## Package Structure

```
proxmox_sdk/
├── __init__.py               # Package exports and public API
├── main.py                   # Full API server (mock OR real mode)
├── mock_main.py              # Standalone mock-only server entrypoint
├── schema.py                 # Schema management (load/save OpenAPI)
├── generated/pdm/latest/     # Packaged PDM OpenAPI + raw capture artifacts
├── rate_limit.py             # SlowAPI rate limiting configuration
├── exception.py              # Exception classes
├── logger.py                 # Logging utilities
├── telemetry.py              # Optional OpenTelemetry tracing
├── routes/
│   ├── codegen.py            # Code generation endpoints (protected)
│   ├── helpers.py            # Shared route utilities
│   ├── mock.py               # Mock route handlers
│   └── versions.py           # Version management endpoints
├── proxmox/                  # Real API proxy
│   ├── routes.py             # Proxmox API proxy routes with validation
│   ├── config.py             # ProxmoxConfig dataclass
│   └── client.py             # FastAPI adapter wrapping the SDK HTTPS backend
├── ceph/                     # Ceph facade (PVE service)
│   ├── client.py             # CephClient / SyncCephClient
│   ├── models.py             # Pydantic models for Ceph responses
│   ├── _confirm.py           # confirm_destroy gate (shared)
│   ├── domains/              # Cluster, Node, Write domain helpers
│   └── providers/            # Direct provider clients (Dashboard, RGW, RBD)
│       ├── capability.py     # ProviderCapability descriptor
│       ├── dashboard.py      # DashboardCephClient
│       ├── rgw.py            # RGWAdminClient
│       └── rbd.py            # RBDClient
├── pbs/                      # Proxmox Backup Server facade
│   ├── client.py             # PBSClient / SyncPBSClient
│   ├── models.py             # Pydantic models for PBS responses
│   └── domains/              # Datastores, Jobs, Nodes, Snapshots
├── pdm/                      # Proxmox Datacenter Manager facade
│   ├── client.py             # PDMClient / SyncPDMClient
│   ├── models.py             # Pydantic models for PDM responses
│   ├── errors.py             # Redacted PDMResponseContractError
│   ├── _normalization.py     # Strict object/list/string and model validation
│   ├── domains/              # Access, Metrics, PBS, PVE, Remotes, Resources, Views
│   └── mock/                 # PDM mock routes for proxmox-sdk-pdm-mock
├── node/                     # Node-level helpers
│   └── hardware/             # Hardware discovery
├── ssh/                      # SSH utilities
│   └── __init__.py
├── proxmox_cli/              # CLI + TUI application
│   ├── app.py                # Typer app construction and setup_logging
│   ├── batch.py              # Batch request execution
│   ├── cache.py              # Response caching layer
│   ├── cli.py                # CLI entrypoint (proxmox, pbx, proxmox-cli)
│   ├── completion.py         # Shell completion helpers
│   ├── config.py             # Config file management
│   ├── config_commands.py    # `config` subcommand group
│   ├── doc_commands.py       # `docs` subcommand group
│   ├── docgen_capture.py     # CLI docs capture pipeline
│   ├── exceptions.py         # CLI-specific exceptions
│   ├── install.py            # Self-install helpers
│   ├── output.py             # Shared output formatting
│   ├── pdm_tui_app.py        # PDM TUI entrypoint
│   ├── performance.py        # Performance profiling helpers
│   ├── release.py            # Release tooling
│   ├── sdk_bridge.py         # Bridge between CLI and ProxmoxSDK
│   ├── tui_app.py            # Textual TUI application (PVE)
│   ├── tui_runner.py         # TUI launch wrapper
│   ├── utils.py              # Path/param parsing utilities
│   ├── tui/                  # Per-service Textual TUI apps
│   │   ├── ceph_app.py       # Ceph TUI
│   │   ├── pbs_app.py        # PBS TUI
│   │   ├── pdm_app.py        # PDM TUI
│   │   └── pve_app.py        # PVE TUI
│   ├── commands/             # Subcommands
│   │   ├── _common.py        # Shared command utilities
│   │   ├── create.py         # `create` subcommand
│   │   ├── delete.py         # `delete` subcommand
│   │   ├── get.py            # `get` subcommand
│   │   ├── help.py           # `help` subcommand
│   │   ├── ls.py             # `ls` subcommand
│   │   ├── set.py            # `set` subcommand
│   │   ├── tui.py            # `tui` subcommand
│   │   └── usage.py          # `usage` subcommand
│   ├── docgen/               # CLI docs generation
│   │   ├── discovery.py      # Command discovery
│   │   ├── engine.py         # Doc generation engine
│   │   ├── models.py         # Doc data models
│   │   └── specs.py          # OpenAPI spec helpers
│   ├── plugins/              # Plugin extension point
│   └── themes/               # TUI themes
├── proxmox_codegen/          # Proxmox API Viewer crawler
│   ├── apidoc_parser.py      # Parse Proxmox apidoc.js
│   ├── crawler.py            # Playwright-based crawler
│   ├── normalize.py          # Normalize captured endpoints
│   ├── openapi_generator.py # Generate OpenAPI schema
│   ├── pydantic_generator.py # Generate Pydantic models
│   ├── pipeline.py           # Generation pipeline orchestration
│   ├── security.py           # SSRF protection, URL validation
│   ├── models.py
│   ├── utils.py
│   └── cli.py                # Codegen CLI commands
├── sdk/                      # Standalone Python SDK
│   ├── api.py                # ProxmoxSDK main class
│   ├── sync.py               # SyncProxmoxSDK wrapper
│   ├── sync_adapter.py       # BlockingDomainProxy for sync typed clients
│   ├── resource.py           # Resource navigation (attribute-based)
│   ├── services.py           # Service configs (PVE, PMG, PBS, PDM)
│   ├── exceptions.py         # SDK-specific exceptions
│   ├── backends/             # Transport backends
│   │   ├── base.py           # AbstractBackend protocol
│   │   ├── _cli_base.py      # Shared base for pvesh/openssh CLI backends
│   │   ├── https.py          # aiohttp HTTPS backend (default)
│   │   ├── mock.py           # In-memory mock backend
│   │   ├── local.py          # Local pvesh CLI backend
│   │   ├── ssh_paramiko.py   # SSH via Paramiko
│   │   └── openssh.py        # SSH via openssh-wrapper
│   ├── auth/                 # Authentication handlers
│   │   ├── base.py           # BaseAuth abstract protocol
│   │   ├── token.py          # API token auth
│   │   └── ticket.py         # Password/ticket auth + TOTP
│   └── tools/                # Helper tools
│       ├── files.py          # File upload/download
│       └── tasks.py          # Task monitoring
└── mock/                     # Mock API implementation
    ├── app.py                # Mock FastAPI app
    ├── routes.py             # Dynamic route registration with CRUD
    ├── state.py              # SharedMemoryMockStore (in-memory persistence)
    ├── schema_helpers.py     # Mock value generation
    └── loader.py             # Mock data loading from JSON/YAML
```

## Required Checks

```bash
# Install dependencies
uv sync

# Install git hooks (one-time setup)
uv run pre-commit install --hook-type pre-commit --hook-type pre-push

# Run pre-commit checks (required before commit and push)
uv run pre-commit run --all-files

# Run linting
ruff check .
ruff format --check .

# Run type checks
uv run ty check proxmox_sdk tests --output-format concise
uv run pyright proxmox_sdk

# IDE support
# proxmox_sdk ships a py.typed PEP 561 marker. Pyright mirrors Pylance at
# typeCheckingMode = "basic"; current typing debt is surfaced as warnings.

# Compile package
uv run python -m compileall proxmox_sdk

# Test core imports
uv run python -c "import proxmox_sdk.main"
uv run python -c "import proxmox_sdk.mock_main"

# Test SDK imports
uv run python -c "from proxmox_sdk.sdk import ProxmoxSDK"
uv run python -c "from proxmox_sdk.sdk.sync import SyncProxmoxSDK"

# Build and verify runtime artifacts from the wheel, outside the source tree
uv lock --check
uv sync --locked --group dev
uv run --locked python -m build --no-isolation
uv run --locked python tests/verify_wheel_contract.py dist/*.whl

# Verify all 32 schema-backed PDM reads and their CLI route mappings
uv run pytest tests/pdm/test_schema_read_contract.py tests/cli/test_pdm_commands.py

# Test CLI imports
uv run python -c "from proxmox_sdk.proxmox_cli.cli import cli"

# Run tests
pytest
```

## Continuous Integration

`.gitea/workflows/ci.yml` mirrors the secret-free review gates from GitHub for
the Gitea-first feature path: pinned workflow tooling, Ruff, ty, Pyright,
compile/import contracts, the full `latest`/`9.2`/`9.1.11` schema matrix,
strict documentation, and installed-wheel validation. Pull-request jobs run
only on the isolated `ci-untrusted-python312` label with read-only repository
permissions; they must never publish, deploy, push, or receive credentials.

The workflow definition is necessary but not sufficient to claim an
authoritative merge gate. Operators must also provision an eligible
organization/repository runner and required branch status checks. Until those
external controls exist and a PR records successful terminal contexts, retain
the complete local evidence and do not represent Gitea CI as green or bypass a
pending context.

## Security Controls

See [docs/security.md](docs/security.md) for the full reference. Key patterns to follow:

- **SSRF protection** — All user-supplied URLs must be passed through `validate_source_url()` in `proxmox_codegen/security.py` before any outbound request. Non-Proxmox domains are blocked by default (`allow_any_domain=False`). Private IPv4, private IPv6, IPv4-mapped IPv6 (`::ffff:`), and 6to4 addresses are all blocked.
- **Download checksum-discovery SSRF guard** — `Files._discover_checksum()` (`sdk/tools/files.py`) probes sibling URLs *from the SDK host* to auto-find a checksum. `_is_safe_probe_url()` gates this: only `http`/`https` schemes, and hosts that are loopback/private/link-local/reserved IP literals (incl. IPv4-mapped IPv6 and `localhost`) are refused, so a download URL pointing at cloud-metadata or internal services never triggers an SDK-side probe. Public hostnames pass; an explicit `checksum=` bypasses discovery entirely.
- **Typed auth failures** — `TicketAuth._request_ticket()` wraps non-JSON `/access/ticket` responses (e.g. an HTML 502 from a reverse proxy) as `AuthenticationError` instead of leaking a raw `JSONDecodeError`.
- **Codegen auth** — `POST /codegen/generate` and related endpoints require a `Bearer` token via `CODEGEN_API_KEY`. Rate-limited to 1 req/hour.
- **CORS** — Disabled by default. Enable via `CORS_ORIGINS`. Allowed headers are restricted to `Content-Type`, `Authorization`, `X-Requested-With`. Wildcards are never used.
- **Health endpoint** — Returns `404` for non-localhost callers. `testclient` is only added to the allowlist when `TESTING=1`.
- **SSH backends** — `SshParamikoBackend` defaults to `WarningPolicy` (not `AutoAddPolicy`). All SSH commands use `shlex.join()`/`shlex.quote()` to prevent shell injection. Temp files use `secrets.token_hex(8)`.
- **Log sanitization** — `SensitiveDataFilter` in `logger.py` redacts credentials (`password=`, `token_value=`, `PVEAuthCookie=`, `PMGAuthCookie=`, `PBSAuthCookie=`, `CSRFPreventionToken=`, `Authorization=`) from all log output.
- **PDM response redaction** — Typed PDM contract failures retain neither raw payloads nor Pydantic exception context. Every typed successful PDM model boundary replaces operator-controlled upstream `error` strings with a static degraded-state marker; resource adapters additionally discard nested error extras and bind remote identity to the trusted response envelope or request path.
- **Credential clearing** — `PROXMOX_API_TOKEN_SECRET`, `PROXMOX_API_PASSWORD`, `PROXMOX_API_OTP` are overwritten with `"********"` in `os.environ` after being read.
- **Config symlink protection** — `save_config()` refuses to write if the config file or its parent directory is a symlink.
- **SSL context** — `TicketAuth` receives the same `ssl` context as the main HTTPS backend, so `verify_ssl=False` applies consistently to both auth and API requests.
- **Proxy threading** — `TicketAuth._request_ticket()` forwards `proxy=` to `session.post()` so authentication requests go through the same proxy as all other API calls. Omitting this would cause auth to bypass the proxy in proxy-only networks.
- **Bring-your-own session** — `ProxmoxSDK(session=...)` / `HttpsBackend(session=...)` reuse a caller-supplied `aiohttp.ClientSession` verbatim and never close it (the caller owns its lifecycle). For ticket auth the backend removes the auth cookie from the external jar and sends `PVEAuthCookie` verbatim in an explicit `Cookie` header — an external jar re-quotes the cookie and overrides the header, and Proxmox rejects a quoted cookie with `401`. Internal (SDK-created) sessions are unchanged: they use a `quote_cookie=False` jar and are closed on `close()`.
- **OpenTelemetry span hygiene** — Optional tracing never records request params, request bodies, auth headers, cookies, passwords, tickets, CSRF tokens, or API token values as span data.

## Performance Patterns

See [docs/performance.md](docs/performance.md) for the full reference. Key patterns to be aware of:

- **Lazy package imports** — `proxmox_sdk/__init__.py` uses `__getattr__` to defer app construction. `import proxmox_sdk` alone does not build any FastAPI app.
- **Route metadata artifacts** — `generated/proxmox/<version>/route_metadata.json` drives generated route registration, avoiding runtime topology/signature rebuilding.
- **Lazy model shards** — `generated/proxmox/<version>/model_index.json` maps operations to route-group Pydantic shards under `models/`; the aggregate `pydantic_models.py` remains for compatibility but is not imported at startup.
- **Schema fingerprint** — `ProxmoxSchemaValue.fingerprint` is a `@cached_property`; the JSON hash is computed once per object.
- **SQLite mock state** — `SQLiteMockStore` is the default `PROXMOX_MOCK_STORE=sqlite` backend and stores objects/collection members/tombstones as rows instead of serialising one whole-state blob. `shared-memory` and `dict` remain selectable.
- **Mock-state serialization** — value blobs use `orjson` when available, with stdlib JSON fallback.
- **URL construction** — `HttpsBackend` caches `(scheme, netloc, base_path)` in `__init__`; `_url_for()` uses `posixpath.join` with cached components instead of calling `urlsplit` on every request.
- **Path joining fast path** — `_url_join()` in `resource.py` skips `urlsplit`/`urlunsplit` for plain paths (no `://`).
- **None filtering fast path** — `_filter_none()` in `resource.py` returns the original dict unchanged when no `None` values are present.
- **Task polling** — `Tasks.blocking_status()` uses exponential backoff (1s→2s→4s→8s→16s→30s cap) with `time.monotonic()` for accurate timeout tracking.
- **Request retry** — `HttpsBackend.request()` retries GET/HEAD requests on 502/503/504 and transport errors with exponential backoff (base × 2ⁿ, capped at 30s). POST/PUT/DELETE never retry to prevent double-mutation. `max_retries=0` by default keeps existing behaviour.
- **Config loading** — `ProxmoxConfig.from_env()` reads only the ~20 specific env keys it needs. `yaml` is only imported when a YAML config file is present.
- **Regex pre-compilation** — `_RE_NAME_HINT` in `schema.py` is compiled once at module load.

## Commit and Push Policy

Before every `git commit` and every `git push`, run:

```bash
uv run pre-commit run --all-files
```

If any hook fails, fix the issues and rerun until all hooks pass.

## Release Process

Follow the package-first lifecycle in `docs/release-evidence.md` and the
workspace `deploy-workflow`; never publish directly from an ad-hoc shell.

1. Record NASA-aligned requirements, design, implementation, test/coverage,
   defect, operations, and approval evidence, then prepare `X.Y.ZrcN`.
2. Merge through Gitea review and push the protected matching tag. The Gitea
   workflow builds the wheel/sdist twice under the commit `SOURCE_DATE_EPOCH`,
   runs all gates, publishes the package of record, and verifies served bytes.
3. Verify the record with `nms git packages`, promote the RC tag, and require the
   GitHub `v*rc*` TestPyPI matrix to pass. RCs cannot reach public PyPI or stable
   Docker tags.
4. After a clean RC, create and verify the final Gitea package of record. Fill
   `.github/RELEASE_EVIDENCE_TEMPLATE.md` with public product evidence and the
   Gitea evidence artifact's `distribution_manifest_sha256`, then publish the
   matching non-prerelease GitHub Release. GitHub rebuilds that manifest and
   rejects a mismatch.
5. The public workflow publishes from artifacts in protected environments,
   downloads the wheel back from PyPI, and binds service images to that served
   filename/SHA256. Core and service images build without registry credentials,
   emit CycloneDX inventories, and run on amd64 and arm64 before candidate
   manifests converge at one stable-alias fan-in. Archives, SBOMs, candidate
   tags, and evidence are source/run/attempt-bound; the serialized fan-in
   refuses to move aliases for a release that is no longer current latest.
6. Validate the post-release 14-image matrix, update downstream consumers, and
   archive the retained distribution, PyPI, SBOM, manifest, promotion, coverage,
   and defect evidence.

Configure the `testpypi`, `pypi`, `dockerhub-candidate`,
`dockerhub-development`, `dockerhub-release`, and `gitea-package-registry`
environments exactly as documented. Environment secrets, required reviewers,
deployment branch/tag policies, protected tags, and isolated Gitea
`release-builder`/`release-publisher` runners are external prerequisites and
cannot be created by workflow YAML.

An OCI digest is the immutable image identity. A `sha-<commit>` alias is a
commit traceability tag, not an immutable object. Docker Hub has no multi-image
atomic tag transaction: the pipeline gates all candidates before promotion and
can safely re-point aliases from recorded digests after an external partial
failure, but it never rebuilds or deletes a released artifact.

## Key Endpoints

### Core
- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /version` - Version info
- `GET /mode` - Current mode (mock/real)
- `GET /docs` - Swagger documentation
- `GET /redoc` - ReDoc documentation

### Codegen (Protected)
- `POST /codegen/generate` - Generate OpenAPI schema from Proxmox API Viewer (requires auth, rate-limited 1/hour)
- `GET /codegen/openapi` - Get generated OpenAPI schema (requires auth)
- `GET /codegen/pydantic` - Get generated Pydantic v2 models (requires auth, rate-limited 5/hour)
- `GET /codegen/versions` - List available versions (requires auth)

### Mock
- `GET /versions/` - List available Proxmox OpenAPI versions
- `GET /mock/openapi` - Mock mode OpenAPI schema
- `POST /mock/reset` - Reset mock data to defaults
- `GET /mock/state` - Get current mock state

## Environment Variables

### Mock Mode (Default)
- `PROXMOX_API_MODE` - Set to "mock" (default) or "real"
- `PROXMOX_MOCK_SCHEMA_VERSION` - Version tag for mock (default: "latest")
- `PROXMOX_MOCK_DATA_PATH` - Path to custom mock data JSON/YAML file
- `PROXMOX_MOCK_STORE` - Mock state backend: "sqlite" (default), "shared-memory", or "dict"
- `PROXMOX_MOCK_STATE_PATH` - Optional SQLite mock-state database path (default: tempdir-scoped)

### Real Mode
- `PROXMOX_API_MODE` - Set to "real" to enable Proxmox integration
- `PROXMOX_API_URL` - Proxmox server URL (e.g., "https://proxmox.example.com:8006")
- `PROXMOX_API_TOKEN_ID` - API token ID (format: "user@realm!tokenid")
- `PROXMOX_API_TOKEN_SECRET` - API token secret UUID
- `PROXMOX_API_USERNAME` - Username for password auth (format: "user@realm")
- `PROXMOX_API_PASSWORD` - Password for password auth
- `PROXMOX_API_VERIFY_SSL` - Verify SSL certificates (default: true)
- `PROXMOX_API_SERVICE` - Service type: PVE, PMG, PBS, or PDM (default: "PVE")
- `PROXMOX_API_BACKEND` - Transport backend: https, mock, local, ssh_paramiko, openssh (default: "https")
- `PROXMOX_API_PATH_PREFIX` - Reverse-proxy path prefix (default: "")
- `PROXMOX_API_OTP` - OTP/TOTP code for 2FA (default: none)
- `PROXMOX_API_OTPTYPE` - OTP type (default: "totp")
- `PROXMOX_CONFIG_FILE` - Path to YAML/JSON config file; keys are read as PROXMOX_API_* env vars

### Connection Tuning
- `PROXMOX_API_TIMEOUT` - Total request timeout in seconds (default: `"5"`)
- `PROXMOX_API_CONNECT_TIMEOUT` - TCP connection timeout in seconds, separate from total (default: unset)
- `PROXMOX_API_RETRIES` - Max retry attempts for GET/HEAD on 502/503/504 or transport errors (default: `"0"`)
- `PROXMOX_API_RETRY_BACKOFF` - Exponential backoff base in seconds for retries (default: `"0.5"`)

### Proxy Configuration
- `HTTP_PROXY` - HTTP proxy URL
- `HTTPS_PROXY` - HTTPS proxy URL
- `PROXMOX_API_HTTP_PROXY` - Override HTTP proxy for SDK
- `PROXMOX_API_HTTPS_PROXY` - Override HTTPS proxy for SDK

### Server
- `HOST` - Host to bind to (default: "0.0.0.0")
- `PORT` - Port to bind to (default: "8000")
- `CORS_ORIGINS` - Comma-separated CORS origins

### Logging
- `LOG_LEVEL` - Logging level (default: "INFO")

### OpenTelemetry Tracing
- `PROXMOX_OTEL_ENABLED` - Enable outbound SDK CLIENT spans and inbound FastAPI SERVER spans (default: false)
- `OTEL_EXPORTER_OTLP_ENDPOINT` - OTLP HTTP collector endpoint (default base endpoint: `"http://localhost:4318"`)
- `OTEL_EXPORTER_OTLP_PROTOCOL` - Must be `"http/protobuf"` for the bundled HTTP exporter
- `OTEL_EXPORTER_OTLP_HEADERS` - Optional OTLP headers
- `OTEL_SERVICE_NAME` - Service name resource attribute (default: `"proxmox-sdk"`)
- `OTEL_RESOURCE_ATTRIBUTES` - Additional OpenTelemetry resource attributes
- `OTEL_SDK_DISABLED` - Standard OpenTelemetry kill switch; truthy values disable tracing
- `OTEL_TRACES_SAMPLER` - Standard OpenTelemetry trace sampler
- `OTEL_TRACES_EXPORTER` - Set to `"otlp"` or leave unset for OTLP export; set `"none"` to disable export

### Security / Auth
- `CODEGEN_API_KEY` - Bearer token required for all `/codegen/*` endpoints (`POST /codegen/generate`, `GET /codegen/openapi`, `GET /codegen/pydantic`, `GET /codegen/versions`)
- `TESTING` - Set to `1` or `true` to add `testclient` to the health endpoint's localhost allowlist (test use only)

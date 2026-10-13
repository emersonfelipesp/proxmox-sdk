# proxmox_sdk — Python Package

## Workspace Context

This file lives at `/root/personal-context/nmulticloud-context/proxmox-sdk/proxmox_sdk/CLAUDE.md` inside the `personal-context` workspace.
Workspace guidance: `/root/personal-context/CLAUDE.md`.
Per-repo deep-dive: `/root/personal-context/claude-reference/proxmox-sdk.md`.
Submodule layout and cross-repo links: `/root/personal-context/claude-reference/dependency-map.md`.

---

Schema-driven Proxmox API toolkit Python package. Pre-generated 675-operation / 444-endpoint Proxmox VE 9.2 surface (`latest` mirrors 9.2; 9.1.11 retained), plus a 318-operation / 246-endpoint Proxmox Datacenter Manager (PDM) surface (`proxmox_sdk/generated/pdm/latest/`). Dual-mode: mock (in-memory CRUD, `reset_state()`) or real (proxy to a Proxmox node via HTTPS / local `pvesh` / SSH).

## Standalone SDK Entry Point

`from proxmox_sdk.sdk import ProxmoxSDK` — async + sync, no server required.

## OpenTelemetry

FastAPI 0.143.0 owns native HTTP traces, duration metrics, validation/error logs,
and WebSocket traces and logs in the main, PVE, PBS, and PDM applications. Native
server export is opt-in through standard OTLP endpoints; there is no application
collector default. Configure native providers and signal controls through the
shipping factories' `telemetry` argument. Explicit empty endpoints and standard
SDK disable/export controls remain authoritative.

Standalone SDK CLIENT tracing stays lazy, optional, and disabled by default.
Install the `otel` extra and set `PROXMOX_OTEL_ENABLED=true` or enable tracing in
the client configuration. This flag controls outbound tracing only. The client
HTTP exporter retains its localhost fallback when explicitly enabled.

Library-owned native server and global SDK client tracer providers are separate
to avoid duplicate exporters in either startup order, while preserving trace
context. Existing global and explicitly supplied caller providers remain
caller-owned. Use native `auto_configure=False` when callers already configure
exporters, and retain caller responsibility for flushing and shutdown.

Native scoped privacy processors redact concrete paths/query values and omit
exception message/stacktrace attributes while preserving route templates, error
types, and static bodies. Install caller log exporters after
`native_server_configuration()` to preserve processor ordering; already-installed
caller exporters require caller-owned sanitization. Spans must never include
request params, bodies, auth headers, cookies, passwords, tickets, CSRF tokens,
or API token values.

`instrument_fastapi_app()` is a deprecated compatibility no-op and does not
instrument externally constructed apps. Do not add legacy contrib FastAPI
instrumentation. See the root README OpenTelemetry section for standard signal
endpoint, protocol, header, resource, sampler, and exporter controls.

## Multi-Surface Consumers in This Workspace

- `proxbox-api/` — uses this SDK as its Proxmox API layer; pin `proxmox-sdk==0.0.13`.
- CLI entrypoints `proxmox`, `proxmox-cli`, `pbx` (all alias `proxmox_sdk.proxmox_cli.cli:cli_main`, and `pbx tui` Textual TUI).
- `proxmox-sdk-codegen` — Playwright → Proxmox API Viewer → OpenAPI → Pydantic codegen pipeline.
- `proxmox-sdk-mock` — standalone PVE mock server.
- `proxmox-sdk-pdm-mock` — standalone Proxmox Datacenter Manager mock server (default port 8443).

Generated response models retain Proxmox composite string fields, while also
accepting the native integer or boolean scalar documented by a format's single
`default_key`. This compatibility applies to responses only; request fields and
string-default/free-form composites remain strict strings. Native response
arms are strict and preserve captured integer range/multiple/enum constraints;
boolean formats accept only booleans and exact integer flags `0`/`1`, never
coercive floats or arbitrary integers. Every generated string annotation is
strict (including request and non-widened response fields), and integer enums
remain visible in generated JSON Schema as well as enforced at runtime.
Non-finite numeric bounds and non-positive/non-finite multiples fail closed to
the strict-string form. The installed-wheel verifier exercises these strict
PVE scalar contracts for all three shipped schema tags as well as the PDM
schema/client smoke, preventing a stale archive from hiding behind source tests.

## Typed Service Facades

High-level service-specific clients are available alongside the low-level `ProxmoxSDK`:

- **`proxmox_sdk.ceph`** — `CephClient` / `SyncCephClient`: typed Ceph facade over PVE API. Destructive operations (pool/daemon removal) are gated by `confirm_destroy=True`. Includes direct provider clients `DashboardCephClient`, `RGWAdminClient`, `RBDClient` (in `proxmox_sdk.ceph.providers`) and the `ProviderCapability` / `capabilities()` pattern for capability negotiation.
- **`proxmox_sdk.pbs`** — `PBSClient` / `SyncPBSClient`: typed read-only PBS facade. Domains: `datastores`, `snapshots`, `jobs`, `nodes`. Default port 8007.
- **`proxmox_sdk.pdm`** — `PDMClient` / `SyncPDMClient`: typed PDM facade. Domains: `remotes`, `pve`, `pbs`, `resources`, `subscriptions`, `metrics`, `access`, `views`. Default port 8443. Every guest/datastore operation requires a `remote` argument (PDM multiplexes across registered clusters).

Implicit native server providers are allocated only when their native signal is
enabled, automatic configuration is enabled, and the standard environment selects
an exporter and endpoint. Empty signal endpoints fall back to the generic endpoint
as FastAPI specifies. An ineligible implicit SDK client provider uses a no-op server
provider to preserve client/server export isolation. Explicit caller providers retain
manual telemetry with `auto_configure=False`; selected real caller providers receive
scoped privacy processors even without an environment endpoint. Privacy callbacks
are inert while `OTEL_SDK_DISABLED` is true, including after provider construction.

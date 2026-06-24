# proxmox_sdk — Python Package

## Workspace Context

This file lives at `/root/personal-context/nmulticloud-context/proxmox-sdk/proxmox_sdk/CLAUDE.md` inside the `personal-context` workspace.
Workspace guidance: `/root/personal-context/CLAUDE.md`.
Per-repo deep-dive: `/root/personal-context/claude-reference/proxmox-sdk.md`.
Submodule layout and cross-repo links: `/root/personal-context/claude-reference/dependency-map.md`.

---

Schema-driven Proxmox API toolkit Python package. Pre-generated 675-operation / 449-endpoint Proxmox VE 9.2 surface (`latest` mirrors 9.2; 9.1.11 retained). Dual-mode: mock (in-memory CRUD, `reset_state()`) or real (proxy to a Proxmox node via HTTPS / local `pvesh` / SSH).

## Standalone SDK Entry Point

`from proxmox_sdk.sdk import ProxmoxSDK` — async + sync, no server required.

## OpenTelemetry Tracing

OpenTelemetry tracing is optional and disabled by default. Install the
`otel` extra, then set `PROXMOX_OTEL_ENABLED=true` to emit one CLIENT span per
SDK backend request and SERVER spans for FastAPI apps through
`opentelemetry-instrumentation-fastapi`. Export uses OTLP over HTTP/protobuf via
`opentelemetry-exporter-otlp-proto-http`.

Supported env vars:

- `PROXMOX_OTEL_ENABLED` — proxmox-sdk enable flag.
- `OTEL_EXPORTER_OTLP_ENDPOINT`, `OTEL_EXPORTER_OTLP_PROTOCOL`, `OTEL_EXPORTER_OTLP_HEADERS` — collector endpoint/protocol/headers.
- `OTEL_SERVICE_NAME`, `OTEL_RESOURCE_ATTRIBUTES` — resource metadata.
- `OTEL_SDK_DISABLED`, `OTEL_TRACES_SAMPLER`, `OTEL_TRACES_EXPORTER` — standard SDK disable/sampling/export controls.

Security rule: spans must never include request params, request bodies, auth
headers, cookies, passwords, tickets, CSRF tokens, or API token values.

## Multi-Surface Consumers in This Workspace

- `proxbox-api/` — uses this SDK as its Proxmox API layer; pin `proxmox-sdk==0.0.11.post2`.
- CLI entrypoints `proxmox`, `proxmox-cli`, `pbx` (all alias `proxmox_sdk.proxmox_cli.cli:cli_main`, and `pbx tui` Textual TUI).
- `proxmox-sdk-codegen` — Playwright → Proxmox API Viewer → OpenAPI → Pydantic codegen pipeline.
- `proxmox-sdk-mock` — standalone PVE mock server.
- `proxmox-sdk-pdm-mock` — standalone Proxmox Datacenter Manager mock server (default port 8443).

## Typed Service Facades

High-level service-specific clients are available alongside the low-level `ProxmoxSDK`:

- **`proxmox_sdk.ceph`** — `CephClient` / `SyncCephClient`: typed Ceph facade over PVE API. Destructive operations (pool/daemon removal) are gated by `confirm_destroy=True`. Includes direct provider clients `DashboardCephClient`, `RGWAdminClient`, `RBDClient` (in `proxmox_sdk.ceph.providers`) and the `ProviderCapability` / `capabilities()` pattern for capability negotiation.
- **`proxmox_sdk.pbs`** — `PBSClient` / `SyncPBSClient`: typed read-only PBS facade. Domains: `datastores`, `snapshots`, `jobs`, `nodes`. Default port 8007.
- **`proxmox_sdk.pdm`** — `PDMClient` / `SyncPDMClient`: typed PDM facade. Domains: `remotes`, `pve`, `pbs`, `resources`, `subscriptions`, `metrics`, `access`, `views`. Default port 8443. Every guest/datastore operation requires a `remote` argument (PDM multiplexes across registered clusters).

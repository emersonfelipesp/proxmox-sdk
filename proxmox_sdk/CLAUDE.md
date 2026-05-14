# proxmox_sdk — Python Package

## Workspace Context

This file lives at `/root/personal-context/nmulticloud-context/proxmox-sdk/proxmox_sdk/CLAUDE.md` inside the `personal-context` workspace.
Workspace guidance: `/root/personal-context/CLAUDE.md`.
Per-repo deep-dive: `/root/personal-context/claude-reference/proxmox-sdk.md`.
Submodule layout and cross-repo links: `/root/personal-context/claude-reference/dependency-map.md`.

---

Schema-driven Proxmox API toolkit Python package. Pre-generated 646-endpoint Proxmox VE 9.1.11 surface (`latest` mirrors 9.1.11). Dual-mode: mock (in-memory CRUD, `reset_state()`) or real (proxy to a Proxmox node via HTTPS / local `pvesh` / SSH).

## Standalone SDK Entry Point

`from proxmox_sdk.sdk import ProxmoxSDK` — async + sync, no server required.

## Multi-Surface Consumers in This Workspace

- `proxbox-api/` — uses this SDK as its Proxmox API layer; pin `proxmox-sdk==0.0.3.post1`.
- CLI entrypoints `proxmox`, `proxmox-cli`, `pbx` (and `pbx tui` Textual TUI).
- `proxmox-sdk-codegen` — Playwright → Proxmox API Viewer → OpenAPI → Pydantic codegen pipeline.
- `proxmox-sdk-mock` — standalone mock server.

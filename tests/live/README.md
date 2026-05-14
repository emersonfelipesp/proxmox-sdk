# Live Proxmox tests

Tests under `tests/live/` hit a real Proxmox node and are **excluded from CI by
default**. They are gated by the `live` pytest marker so they only run when
explicitly opted in.

## Run them locally

```bash
export PROXMOX_API_URL=https://10.0.30.91:8006
export PROXMOX_API_TOKEN_ID='root@pam!proxbox'
export PROXMOX_API_TOKEN_SECRET=...   # from .hosts-env or your own credentials
uv run pytest -m live -v
```

## Why not in CI?

The current lab is LAN-only (`10.0.30.0/24`). CI exercises the offline schema
matrix (`PROXMOX_MOCK_SCHEMA_VERSION=latest` and `=9.1.11`) which is sufficient
to catch regressions in mock routing, generated Pydantic models, and schema
parsing. The live suite is for local certification of a new Proxmox release
against the freshly-captured schema.

## Adding a new live test

- Mark the module with `pytestmark = pytest.mark.live`.
- Skip when the credentials are missing — never hard-fail in environments
  without the lab.
- Prefer read-only API calls. Anything that mutates a node should be opt-in via
  an extra env var.

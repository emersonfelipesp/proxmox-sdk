# Live Proxmox tests

Tests under `tests/live/` hit a real Proxmox node and are **excluded from CI by
default**. They are gated by the `live` pytest marker so they only run when
explicitly opted in.

## Run them locally

```bash
export PROXMOX_API_URL=https://10.0.30.95:8006
export PROXMOX_API_TOKEN_ID='root@pam!proxbox'
export PROXMOX_API_TOKEN_SECRET=...   # from .hosts-env or your own credentials
uv run pytest -m live -v
```

To also run write tests (creates and auto-deletes a temporary API token):

```bash
PROXMOX_LIVE_WRITE_TESTS=1 uv run pytest -m live -v
```

## CLI smoke tests

The CLI requires a config file for token auth. Pass a temporary config via `--config`:

```bash
cat > /tmp/pve-9.2.json << 'EOF'
{
  "profiles": {
    "live-9.2": {
      "host": "10.0.30.95", "port": 8006, "user": "root@pam",
      "token_name": "proxbox", "token_value": "...", "verify_ssl": false
    }
  },
  "default_profile": "live-9.2"
}
EOF
chmod 600 /tmp/pve-9.2.json

uv run pbx --config /tmp/pve-9.2.json get /version
uv run pbx --config /tmp/pve-9.2.json get /cluster/options
uv run pbx --config /tmp/pve-9.2.json get /cluster/ha/rules
```

## Test coverage (Proxmox VE 9.2)

The suite covers the following API areas:

| Test | Endpoint | 9.2 feature |
|---|---|---|
| `test_live_version_is_9_2` | `GET /version` | Version assertion |
| `test_live_nodes_list` | `GET /nodes` | Connectivity |
| `test_live_cluster_resources` | `GET /cluster/resources` | Connectivity |
| `test_live_cluster_options_crs` | `GET /cluster/options` | CRS / Dynamic Load Balancing (xfail if unconfigured) |
| `test_live_ha_resources` | `GET /cluster/ha/resources` | HA resource list |
| `test_live_ha_groups_deprecated` | `GET /cluster/ha/groups` | Documents 9.2 migration to rules (xfail expected) |
| `test_live_ha_rules` | `GET /cluster/ha/rules` | New 9.2 affinity rules endpoint |
| `test_live_ha_status_current` | `GET /cluster/ha/status/current` | HA status (includes CRS state) |
| `test_live_node_status` | `GET /nodes/{node}/status` | Node connectivity |
| `test_live_storage_list` | `GET /nodes/{node}/storage` | Storage |
| `test_live_vms_list` | `GET /nodes/{node}/qemu` | QEMU VMs |
| `test_live_lxc_list` | `GET /nodes/{node}/lxc` | LXC containers |
| `test_live_access_users` | `GET /access/users` | Access control |
| `test_live_sdn_zones` | `GET /cluster/sdn/zones` | SDN ACL paths (zones added in 9.2) |
| `test_live_write_cluster_options_crs_roundtrip` *(write)* | `PUT /cluster/options` | CRS write path |
| `test_live_access_token_lifecycle` *(write)* | `POST/GET/DELETE /access/users/{u}/token/{t}` | Token lifecycle / secret rotation API |

## Why not in CI?

The current lab is LAN-only (`10.0.30.0/24`). CI exercises the offline schema
matrix (`PROXMOX_MOCK_SCHEMA_VERSION=latest`, `=9.2`, and `=9.1.11`) which is
sufficient to catch regressions in mock routing, generated Pydantic models, and
schema parsing. The live suite is for local certification of a new Proxmox
release against the freshly-captured schema.

## Adding a new live test

- Mark the module with `pytestmark = pytest.mark.live`.
- Skip when the credentials are missing — never hard-fail in environments
  without the lab.
- Prefer read-only API calls. Gate write operations behind
  `PROXMOX_LIVE_WRITE_TESTS=1` using the `write_enabled` fixture.

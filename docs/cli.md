# CLI and TUI Command Guide

The `proxmox` console script is a Typer CLI for Proxmox automation. It shares
the same backend layer as `ProxmoxSDK`, so CLI commands can target HTTPS,
mock, SSH, and local `pvesh` backends where the selected service supports them.

Install the CLI extras when you need command output formatting or Textual TUIs:

```bash
pip install "proxmox-sdk[cli]"
```

The package exposes three equivalent entry points:

| Command | Purpose |
|---|---|
| `proxmox` | Primary CLI entry point |
| `proxmox-cli` | Compatibility alias |
| `pbx` | Short alias for interactive use |

## Global Options

Common commands use the same connection options:

```bash
proxmox --service PVE --host pve.example.com --user root@pam --token-value "$TOKEN" get /nodes
```

| Option | Notes |
|---|---|
| `--service` / `-S` | `PVE`, `PMG`, `PBS`, or `PDM`; defaults to `PVE` |
| `--backend` / `-b` | `https`, `ssh_paramiko`, `openssh`, `local`, or `mock` |
| `--host` / `-H` | Target host for network backends |
| `--user` / `-U` | User or token principal |
| `--password` / `-P` | Password auth; prefer tokens or environment/config for automation |
| `--token-value` | API token secret |
| `--port` | Overrides the service default port |
| `--output` / `-o` | `human`, `json`, `yaml`, `markdown`, `table`, `text`, or `raw` |

The CLI also supports `--json`, `--yaml`, and `--markdown` shortcuts.

## Generic API Commands

The generic commands map directly to Proxmox API paths:

| Command | Action |
|---|---|
| `get <path>` | Read a resource |
| `create <path>` | Create a resource or trigger an action |
| `set-cmd <path>` | Update a resource |
| `delete <path>` | Delete a resource |
| `ls <path>` | List child resources below a path |
| `usage <path>` | Show schema and usage metadata for an endpoint |
| `help-cmd <path>` | Show endpoint help |
| `batch <file>` | Execute batch operations from JSON |

Examples:

```bash
proxmox --backend mock get /nodes --json
proxmox --host pve.example.com --user root@pam ls /
proxmox --host pve.example.com --user root@pam usage /nodes --markdown
```

## Configuration Profiles

Use profiles when commands need repeatable connection settings:

```bash
proxmox init
proxmox config-add lab --host pve.example.com --user root@pam --service PVE
proxmox config-list
proxmox config-set-default lab
```

Credentials are stored in `~/.proxmox-cli/config.json`. The loader warns when
the file has group or world read/write permissions.

## Textual TUI

The top-level TUI browses API paths and works with production or mock backends:

```bash
proxmox tui
proxmox tui mock
proxmox tui --path /nodes/pve1/qemu
```

Module-specific TUI launchers are also available:

```bash
proxmox pbs tui
proxmox pdm tui
proxmox pdm tui mock
proxmox ceph tui
```

## PDM Command Tree

PDM has a dedicated command group because PDM multiplexes across registered PVE
and PBS remotes. Commands operate on the PDM API, not directly on a PVE or PBS
node.

```bash
proxmox --service PDM --host pdm.example.com pdm remote list
proxmox --service PDM --host pdm.example.com pdm resources list --json
proxmox --service PDM --host pdm.example.com pdm pve qemu list pve-prod
proxmox --service PDM --host pdm.example.com pdm pbs datastore list pbs-prod
```

Top-level PDM groups:

| Group | Scope |
|---|---|
| `pdm remote` | Register, update, remove, list, and inspect remotes |
| `pdm pve` | PVE remote resources, tasks, QEMU, LXC, and node metrics |
| `pdm pbs` | PBS datastores, snapshots, node metrics, and tasks |
| `pdm resources` | Cross-remote resource inventory and status |
| `pdm subscriptions` | Fleet subscription state |
| `pdm metrics` | Metric collection status and trigger |
| `pdm access` | Users, ACLs, TFA, and API tokens |
| `pdm views` | Custom cross-remote dashboards |
| `pdm tui` | PDM-specific Textual interface |

Most PDM guest and datastore commands require a `remote` argument. Use
`proxmox pdm remote list` first when you need the registered remote names.
The dedicated commands follow the captured PDM routes exactly: remotes use
`/remotes/remote`, PVE guests are directly under `/pve/remotes/{remote}/qemu`
or `/lxc`, PBS uses singular `/datastore`, and metric collection is under
`/remotes/metric-collection`. `pdm resources list --type vm` and `--type ct`
remain convenient CLI aliases and are sent as the schema values `qemu` and
`lxc` through the `resource-type` query parameter.
Guest `config` commands default `--state pending` as defined by the captured
schema; pass `--state active` explicitly for the active configuration. Every
PVE/PBS `rrddata` command sends both required query parameters and defaults to
`--timeframe hour --cf AVERAGE`. Typer rejects values outside the captured
timeframe, consolidation, and configuration-state enums before making a request.

## Ceph and PBS Commands

`proxmox ceph` is scoped to the Proxmox VE Ceph API. It exposes read commands
for cluster status, metadata, flags, monitor/manager/MDS inventory, OSDs,
pools, filesystems, logs, and a Ceph TUI. Write-oriented Ceph SDK helpers still
require explicit confirmation flags in the Python API.

`proxmox pbs` currently provides the PBS TUI entry point. Programmatic PBS
automation should use the `PBSClient` facade or the generic `--service PBS`
API commands.

## Documentation Capture

The `docs` command regenerates MkDocs CLI capture artifacts:

```bash
proxmox docs generate-capture
uv run mkdocs build --strict
```

The generated capture pages are useful for release documentation, but they can
lag behind command changes if they have not been regenerated. Prefer this guide
and live `--help` output when validating the current command surface.

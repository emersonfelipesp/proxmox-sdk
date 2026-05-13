# Node Hardware Discovery (`proxmox_sdk.node.hardware`)

Proxmox VE does not expose chassis serial, manufacturer, product name, or
per-NIC link speed through its REST API. The `proxmox_sdk.node.hardware`
submodule fills that gap by composing a small set of well-known shell tools
over an already-connected `RemoteSSHClient`.

This module is **pure** — every parser is a `text → dataclass` function with
no I/O, no policy, and no network access. The only async surface is the
`discover_node` composer, which calls `client.run(...)` four-plus times. All
credential storage, scheduling, and progress emission live in the consumer.

## Public surface

```python
from proxmox_sdk.node.hardware import (
    discover_node,
    DEFAULT_NIC_SKIP,
    HardwareFacts,
    SystemFacts,
    ChassisFacts,
    NicFacts,
    EthtoolFacts,
    is_valid_nic_name,
    parse_dmidecode_system,
    parse_dmidecode_chassis,
    parse_ip_link,
    parse_ethtool,
)
```

## `discover_node` composer

```python
async def discover_node(
    client: RemoteSSHClient,
    *,
    nic_skip: re.Pattern[str] = DEFAULT_NIC_SKIP,
) -> HardwareFacts: ...
```

Issues exactly:

1. `dmidecode -t 1`
2. `dmidecode -t 3`
3. `ip -o link show`
4. `ethtool <iface>` per surviving NIC

A NIC "survives" when its name does **not** match `nic_skip` and passes
`is_valid_nic_name()` (≤15 chars, `^[a-zA-Z0-9._-]+$`, never empty). The
second check is a defence-in-depth guard against argv injection if a
malicious `ip` output ever made it through.

**`CommandNotAllowed`** from any call aborts discovery. Any other per-NIC
exception drops the link facts (`ethtool=None`) but keeps the NIC. Non-zero
`ethtool` exit codes are treated the same way — virtual bridges and unsupported
interfaces fail `ethtool` routinely, and an aborted run would be worse than
incomplete data.

If the caller pinned an allowlist on `RemoteSSHClient`, it **must** include
`dmidecode`, `ip`, and `ethtool`.

```python
async with RemoteSSHClient(
    host=node.address,
    username=cred.username,
    known_host_fingerprint=cred.fingerprint,
    private_key=cred.private_key,
    command_allowlist=["dmidecode", "ip", "ethtool"],
) as ssh:
    facts = await discover_node(ssh)

print(facts.system.serial_number)
print(facts.chassis.height_u)
for nic in facts.nics:
    print(nic.name, nic.speed_gbps, nic.mac_address)
```

## Fact dataclasses

All facts are frozen dataclasses. Every parsed field is `Optional` so a
whitebox or partial-data node never raises — placeholders like `"To Be Filled
By O.E.M."` and `"Not Specified"` map to `None`.

| Dataclass | Source | Notable fields |
|---|---|---|
| `SystemFacts` | `dmidecode -t 1` | `manufacturer`, `product_name`, `serial_number`, `uuid`, `sku_number`, `family`, `version` |
| `ChassisFacts` | `dmidecode -t 3` | `manufacturer`, `type`, `serial_number`, `asset_tag`, `height_u`, `sku_number` |
| `EthtoolFacts` | `ethtool <iface>` | `speed_mbps`, `duplex`, `link_detected`, `port`, `auto_negotiation` |
| `NicFacts` | `ip -o link show` + ethtool | `name`, `mac_address`, `mtu`, `operstate`, `kind`, `ethtool` (`EthtoolFacts | None`). Convenience: `speed_gbps` derived from `ethtool.speed_mbps`. |
| `HardwareFacts` | all of the above | `system`, `chassis`, `nics: tuple[NicFacts, ...]` |

`asset_tag` is preserved verbatim — Dell's legitimate `"00000"` default is
**not** mapped to `None` so operators can re-stamp authoritatively in NetBox
if they choose to.

## NIC skip filter

`DEFAULT_NIC_SKIP` matches the long tail of virtual interfaces that a typical
Proxmox node exposes:

```
lo, docker\d+, veth.*, vmbr\d+, tap\d+i\d+, fwbr.*, fwln.*, fwpr.*,
bond\d+, virbr\d+, wg\d+
```

Pass a custom `re.Pattern` via `nic_skip=` to widen or narrow the filter. The
pattern is matched with `.match()`, so it implicitly anchors at the start.

## Fixture-driven tests

The parser tests under `tests/test_node_hardware_parsers.py` pin every parser
against real captured output:

```
tests/fixtures/
├── dmidecode/
│   ├── dell_r740_system.txt        — full Dell PowerEdge R740 -t 1
│   ├── dell_r740_chassis.txt       — full Dell PowerEdge R740 -t 3 (2U)
│   └── whitebox_unknown_system.txt — all "To Be Filled By O.E.M." placeholders
├── ethtool/
│   ├── eno1_1g.txt                 — 1G copper, link up, autoneg on
│   ├── enp94s0f0_10g.txt           — 10G fiber, link up, autoneg off
│   └── no_link.txt                 — link down ("Unknown!" speed)
└── ip_link/
    └── proxmox_node.txt            — real backslash-continuation form
                                       (lo, 4 physical NICs, vmbr0, tap, fwbr, bond0)
```

Adding a new node type means dropping a new fixture in the corresponding
directory and pinning expected fields in a new test case. There is no
codegen step — parsers are intentionally easy to extend without ceremony.

## Why this module is in `proxmox-sdk`

Hardware discovery is a Proxmox-host concern (the commands run on the
hypervisor), but the parsers and `RemoteSSHClient` are useful for any Debian-
based node. Keeping them here means:

* proxbox-api stays paramiko-free; it imports `proxmox_sdk.node.hardware` and
  `proxmox_sdk.ssh` and does no protocol work of its own.
* Any future consumer (netbox-bng, internal tooling, etc.) gets the same
  primitives without reimplementing them.
* The fixture corpus lives next to the parsers, so a regression in field
  extraction is caught here rather than downstream.

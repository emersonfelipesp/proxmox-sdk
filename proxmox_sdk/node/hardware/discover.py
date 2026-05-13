"""High-level composer: run dmidecode + ip + ethtool and assemble HardwareFacts.

Designed to be called from any orchestrator that already holds a connected
:class:`proxmox_sdk.ssh.RemoteSSHClient`. This module is intentionally pure
async + parser-only — it adds no policy beyond a small NIC-name regex filter.
Credential storage, retry behaviour, and progress emission live in the
consumer (e.g. proxbox-api's ``hardware_discovery`` service).
"""

from __future__ import annotations

import re

from proxmox_sdk.node.hardware.dmidecode import (
    parse_dmidecode_chassis,
    parse_dmidecode_system,
)
from proxmox_sdk.node.hardware.ethtool import (
    is_valid_nic_name,
    parse_ethtool,
    parse_ip_link,
)
from proxmox_sdk.node.hardware.facts import HardwareFacts, NicFacts
from proxmox_sdk.ssh import CommandNotAllowed, RemoteSSHClient

#: NICs whose names match this default filter are skipped. ``lo`` is always
#: skipped; otherwise this excludes the long tail of virtual bridges, tap
#: interfaces, veth pairs and Open vSwitch internals that ``ip -o link show``
#: exposes on a typical Proxmox node.
DEFAULT_NIC_SKIP = re.compile(
    r"^(lo|docker\d+|veth.*|vmbr\d+|tap\d+i\d+|fwbr.*|fwln.*|fwpr.*|"
    r"bond\d+|virbr\d+|wg\d+)$"
)


async def discover_node(
    client: RemoteSSHClient,
    *,
    nic_skip: re.Pattern[str] = DEFAULT_NIC_SKIP,
) -> HardwareFacts:
    """Run the discovery commands and parse the results.

    The caller is responsible for connecting/closing ``client``. This function
    issues four commands per node plus one ``ethtool`` per surviving NIC:

    1. ``dmidecode -t 1``
    2. ``dmidecode -t 3``
    3. ``ip -o link show``
    4. ``ethtool <iface>`` for each NIC not matched by ``nic_skip``

    If ``client`` has a command allowlist configured, it MUST include
    ``dmidecode``, ``ip`` and ``ethtool`` — otherwise the relevant calls will
    raise :class:`proxmox_sdk.ssh.CommandNotAllowed` and discovery aborts.
    """
    sys_res = await client.run(["dmidecode", "-t", "1"])
    chs_res = await client.run(["dmidecode", "-t", "3"])
    link_res = await client.run(["ip", "-o", "link", "show"])

    system = parse_dmidecode_system(sys_res.stdout)
    chassis = parse_dmidecode_chassis(chs_res.stdout)
    nics_raw = parse_ip_link(link_res.stdout)

    enriched: list[NicFacts] = []
    for nic in nics_raw:
        if nic_skip.match(nic.name):
            continue
        if not is_valid_nic_name(nic.name):
            # Refuse to pass anything weird to ethtool's argv.
            continue
        try:
            eth_res = await client.run(["ethtool", nic.name])
        except CommandNotAllowed:
            raise
        except Exception:  # noqa: BLE001 - we keep going on per-NIC failures
            enriched.append(nic)
            continue
        # ethtool returns non-zero on virtual / unsupported NICs; treat as
        # "no link facts" rather than discarding the NIC entirely.
        eth = parse_ethtool(eth_res.stdout) if eth_res.exit_code == 0 else None
        enriched.append(
            NicFacts(
                name=nic.name,
                mac_address=nic.mac_address,
                mtu=nic.mtu,
                operstate=nic.operstate,
                kind=nic.kind,
                ethtool=eth,
            )
        )

    return HardwareFacts(system=system, chassis=chassis, nics=tuple(enriched))


__all__ = ["DEFAULT_NIC_SKIP", "discover_node"]

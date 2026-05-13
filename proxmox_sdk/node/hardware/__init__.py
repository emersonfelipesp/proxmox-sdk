"""Node hardware discovery primitives.

Composes pure parsers (``dmidecode``, ``ethtool``, ``ip -o link``) on top of a
:class:`proxmox_sdk.ssh.RemoteSSHClient`. Pure-Python, no Proxmox dependency.
"""

from proxmox_sdk.node.hardware.discover import DEFAULT_NIC_SKIP, discover_node
from proxmox_sdk.node.hardware.dmidecode import (
    parse_dmidecode_chassis,
    parse_dmidecode_system,
)
from proxmox_sdk.node.hardware.ethtool import (
    is_valid_nic_name,
    parse_ethtool,
    parse_ip_link,
)
from proxmox_sdk.node.hardware.facts import (
    ChassisFacts,
    EthtoolFacts,
    HardwareFacts,
    NicFacts,
    SystemFacts,
)

__all__ = [
    "ChassisFacts",
    "DEFAULT_NIC_SKIP",
    "EthtoolFacts",
    "HardwareFacts",
    "NicFacts",
    "SystemFacts",
    "discover_node",
    "is_valid_nic_name",
    "parse_dmidecode_chassis",
    "parse_dmidecode_system",
    "parse_ethtool",
    "parse_ip_link",
]

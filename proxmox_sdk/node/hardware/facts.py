"""Dataclasses for parsed node hardware facts.

These shapes are the contract between :mod:`proxmox_sdk.node.hardware.discover`
and any consumer (notably proxbox-api's ``hardware_discovery`` orchestrator).
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SystemFacts:
    """Chassis-independent system identity (``dmidecode -t 1``)."""

    manufacturer: str | None = None
    product_name: str | None = None
    serial_number: str | None = None
    uuid: str | None = None
    sku_number: str | None = None
    family: str | None = None
    version: str | None = None


@dataclass(frozen=True)
class ChassisFacts:
    """Physical chassis identity (``dmidecode -t 3``)."""

    manufacturer: str | None = None
    type: str | None = None
    serial_number: str | None = None
    version: str | None = None
    asset_tag: str | None = None
    height_u: int | None = None
    sku_number: str | None = None


@dataclass(frozen=True)
class EthtoolFacts:
    """Per-NIC ``ethtool`` facts. All fields optional — ethtool may omit them."""

    speed_mbps: int | None = None
    duplex: str | None = None
    link_detected: bool | None = None
    port: str | None = None
    auto_negotiation: bool | None = None


@dataclass(frozen=True)
class NicFacts:
    """Per-NIC facts derived from ``ip -o link show`` plus ``ethtool``."""

    name: str
    mac_address: str | None = None
    mtu: int | None = None
    operstate: str | None = None
    kind: str | None = None  # link/ether, link/loopback, link/none, ...
    ethtool: EthtoolFacts | None = None

    @property
    def speed_gbps(self) -> float | None:
        """Convenience: speed expressed in Gbps."""
        if self.ethtool is None or self.ethtool.speed_mbps is None:
            return None
        return self.ethtool.speed_mbps / 1000


@dataclass(frozen=True)
class HardwareFacts:
    """All hardware facts collected by ``discover_node``."""

    system: SystemFacts
    chassis: ChassisFacts
    nics: tuple[NicFacts, ...] = field(default_factory=tuple)


__all__ = [
    "ChassisFacts",
    "EthtoolFacts",
    "HardwareFacts",
    "NicFacts",
    "SystemFacts",
]

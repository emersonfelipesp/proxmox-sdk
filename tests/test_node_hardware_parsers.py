"""Fixture-driven tests for the node.hardware parsers.

These tests pin the parser shape against captured ``dmidecode``, ``ethtool``,
and ``ip -o link show`` output so any regression in field extraction is caught
before it reaches downstream consumers (netbox-proxbox + proxbox-api).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from proxmox_sdk.node.hardware import (
    EthtoolFacts,
    NicFacts,
    is_valid_nic_name,
    parse_dmidecode_chassis,
    parse_dmidecode_system,
    parse_ethtool,
    parse_ip_link,
)

FIXTURES = Path(__file__).parent / "fixtures"


def _read(rel: str) -> str:
    return (FIXTURES / rel).read_text(encoding="utf-8")


# --- dmidecode -t 1 ---------------------------------------------------------


def test_parse_dmidecode_system_dell_r740() -> None:
    facts = parse_dmidecode_system(_read("dmidecode/dell_r740_system.txt"))
    assert facts.manufacturer == "Dell Inc."
    assert facts.product_name == "PowerEdge R740"
    assert facts.serial_number == "7XQZ1Y3"
    assert facts.uuid == "4c4c4544-0058-5110-805a-c2c04f315933"
    assert facts.sku_number == "SKU=NotProvided;ModelName=PowerEdge R740"
    assert facts.family == "PowerEdge"
    assert facts.version is None  # "Not Specified" → None


def test_parse_dmidecode_system_whitebox_all_placeholders() -> None:
    facts = parse_dmidecode_system(_read("dmidecode/whitebox_unknown_system.txt"))
    assert facts.manufacturer is None
    assert facts.product_name is None
    assert facts.serial_number is None
    assert facts.sku_number is None
    assert facts.family is None
    assert facts.version is None
    # UUID is genuine even on a whitebox board.
    assert facts.uuid == "03000200-0400-0500-0006-000700080009"


def test_parse_dmidecode_system_empty_input() -> None:
    facts = parse_dmidecode_system("")
    assert facts.manufacturer is None
    assert facts.product_name is None


# --- dmidecode -t 3 ---------------------------------------------------------


def test_parse_dmidecode_chassis_dell_r740() -> None:
    facts = parse_dmidecode_chassis(_read("dmidecode/dell_r740_chassis.txt"))
    assert facts.manufacturer == "Dell Inc."
    assert facts.type == "Rack Mount Chassis"
    assert facts.serial_number == "7XQZ1Y3"
    # "00000" is a legit-looking value, not a placeholder Dell ships by default.
    # The parser preserves it verbatim; operators can re-stamp if needed.
    assert facts.asset_tag == "00000"
    assert facts.height_u == 2
    assert facts.sku_number is None  # "Not Specified" → None


# --- ethtool ----------------------------------------------------------------


def test_parse_ethtool_1g_link_up() -> None:
    facts = parse_ethtool(_read("ethtool/eno1_1g.txt"))
    assert facts == EthtoolFacts(
        speed_mbps=1000,
        duplex="Full",
        link_detected=True,
        port="Twisted Pair",
        auto_negotiation=True,
    )


def test_parse_ethtool_10g_link_up() -> None:
    facts = parse_ethtool(_read("ethtool/enp94s0f0_10g.txt"))
    assert facts.speed_mbps == 10000
    assert facts.duplex == "Full"
    assert facts.link_detected is True
    assert facts.port == "FIBRE"
    assert facts.auto_negotiation is False


def test_parse_ethtool_no_link() -> None:
    facts = parse_ethtool(_read("ethtool/no_link.txt"))
    # Speed/duplex unknown when link is down — must map to None, not crash.
    assert facts.speed_mbps is None
    assert facts.link_detected is False
    assert facts.auto_negotiation is True
    assert facts.port == "Twisted Pair"


def test_parse_ethtool_empty_input() -> None:
    facts = parse_ethtool("")
    assert facts == EthtoolFacts()


# --- ip -o link show --------------------------------------------------------


def test_parse_ip_link_proxmox_node() -> None:
    nics = parse_ip_link(_read("ip_link/proxmox_node.txt"))
    by_name = {n.name: n for n in nics}

    # Loopback must parse but later be filtered out by DEFAULT_NIC_SKIP.
    assert "lo" in by_name
    assert by_name["lo"].kind == "link/loopback"
    assert by_name["lo"].mac_address == "00:00:00:00:00:00"

    # Primary physical NIC carries a real MAC and is UP.
    assert by_name["eno1"] == NicFacts(
        name="eno1",
        mac_address="ac:1f:6b:2c:8d:e1",
        mtu=1500,
        operstate="UP",
        kind="link/ether",
        ethtool=None,
    )

    # 10G NIC: jumbo MTU preserved.
    assert by_name["enp94s0f0"].mtu == 9000
    assert by_name["enp94s0f0"].operstate == "UP"
    assert by_name["enp94s0f0"].mac_address == "3c:fd:fe:a1:b2:c3"

    # Bridge / tap / bond lines parse cleanly (the discover composer skips them).
    assert by_name["vmbr0"].kind == "link/ether"
    assert by_name["tap100i0"].kind == "link/ether"
    assert by_name["bond0"].operstate == "DOWN"


def test_parse_ip_link_empty_input() -> None:
    assert parse_ip_link("") == []


# --- NIC name validation ----------------------------------------------------


@pytest.mark.parametrize(
    "name",
    ["eno1", "eth0", "enp94s0f0", "ens3", "br-lan", "veth.123", "en_p0"],
)
def test_is_valid_nic_name_accepts_real_names(name: str) -> None:
    assert is_valid_nic_name(name) is True


@pytest.mark.parametrize(
    "name",
    [
        "",
        "a" * 16,  # Linux NIC names are at most 15 chars
        "eno1; rm -rf /",
        "eno1 && id",
        "eno1`id`",
        "eno1$(id)",
        "eno1|id",
        "eno1\nid",
        "../etc/passwd",
        "eno1 eno2",
    ],
)
def test_is_valid_nic_name_rejects_metacharacters(name: str) -> None:
    assert is_valid_nic_name(name) is False

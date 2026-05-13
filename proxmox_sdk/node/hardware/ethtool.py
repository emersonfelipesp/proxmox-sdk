"""Parsers for ``ethtool <iface>`` and ``ip -o link show``."""

from __future__ import annotations

import re

from proxmox_sdk.node.hardware.facts import EthtoolFacts, NicFacts

_SPEED_RE = re.compile(r"^(?P<n>\d+)\s*(?P<unit>[GMK]?)b/?s?$", re.IGNORECASE)
_IP_LINK_RE = re.compile(
    r"^\d+:\s+(?P<name>[^:@]+)(?:@\S+)?:\s+<(?P<flags>[^>]*)>\s+"
    r"mtu\s+(?P<mtu>\d+)\s+.*?state\s+(?P<state>\S+)",
)
_IP_LINK_KIND_RE = re.compile(r"\s+(?P<kind>link/\S+)\s+(?P<addr>\S+)?")

_NIC_NAME_RE = re.compile(r"^[a-z0-9._-]{1,15}$", re.IGNORECASE)


def is_valid_nic_name(name: str) -> bool:
    """Return True if ``name`` is a safe NIC name to pass to ethtool.

    Linux interface names are at most 15 chars. We further restrict the
    character set to the conservative ``[a-z0-9._-]`` so a metacharacter
    cannot smuggle into the argv list even if a caller bypasses the SSH-side
    allowlist.
    """
    return bool(_NIC_NAME_RE.match(name))


def _parse_speed_mbps(value: str | None) -> int | None:
    if not value:
        return None
    s = value.strip()
    if s.lower() in {"unknown!", "unknown"}:
        return None
    m = _SPEED_RE.match(s)
    if not m:
        return None
    try:
        n = int(m.group("n"))
    except ValueError:  # pragma: no cover - regex guarantees \d+
        return None
    unit = m.group("unit").upper()
    if unit == "G":
        return n * 1000
    if unit == "K":
        # Unlikely but mathematically defined.
        return max(1, n // 1000)
    # "M" or empty (assume Mb/s)
    return n


def _parse_yes_no(value: str | None) -> bool | None:
    if not value:
        return None
    s = value.strip().lower()
    if s in {"yes", "on", "true"}:
        return True
    if s in {"no", "off", "false"}:
        return False
    return None


def parse_ethtool(text: str) -> EthtoolFacts:
    """Parse ``ethtool <iface>`` output into :class:`EthtoolFacts`."""
    fields: dict[str, str] = {}
    # The first line is ``Settings for <iface>:`` and is informational only.
    for raw in text.splitlines():
        line = raw.strip()
        if not line or ":" not in line:
            continue
        key, _, val = line.partition(":")
        fields[key.strip()] = val.strip()

    return EthtoolFacts(
        speed_mbps=_parse_speed_mbps(fields.get("Speed")),
        duplex=fields.get("Duplex") or None,
        link_detected=_parse_yes_no(fields.get("Link detected")),
        port=fields.get("Port") or None,
        auto_negotiation=_parse_yes_no(fields.get("Auto-negotiation")),
    )


def parse_ip_link(text: str) -> list[NicFacts]:
    """Parse ``ip -o link show`` output into a list of :class:`NicFacts`."""
    nics: list[NicFacts] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        m = _IP_LINK_RE.match(line)
        if not m:
            continue
        name = m.group("name").strip()
        try:
            mtu = int(m.group("mtu"))
        except ValueError:  # pragma: no cover - regex guarantees \d+
            mtu = None
        operstate = m.group("state")
        # Trailing "link/ether aa:bb:..." or "link/loopback 00:..."
        tail = line[m.end() :]
        kind_match = _IP_LINK_KIND_RE.search(tail)
        kind = kind_match.group("kind") if kind_match else None
        mac = kind_match.group("addr") if kind_match else None
        nics.append(
            NicFacts(
                name=name,
                mac_address=mac,
                mtu=mtu,
                operstate=operstate,
                kind=kind,
            )
        )
    return nics


__all__ = [
    "is_valid_nic_name",
    "parse_ethtool",
    "parse_ip_link",
]

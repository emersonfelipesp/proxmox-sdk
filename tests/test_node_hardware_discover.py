"""End-to-end tests for ``discover_node`` against a fake RemoteSSHClient.

The composer is the public surface that netbox-proxbox + proxbox-api consume,
so we pin its full behaviour: which commands it issues, NIC filtering, per-NIC
ethtool failures, and ``CommandNotAllowed`` propagation.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from proxmox_sdk.node.hardware import DEFAULT_NIC_SKIP, discover_node
from proxmox_sdk.ssh import CommandNotAllowed, CommandResult

FIXTURES = Path(__file__).parent / "fixtures"


def _read(rel: str) -> str:
    return (FIXTURES / rel).read_text(encoding="utf-8")


class _FakeClient:
    """Stand-in for ``RemoteSSHClient`` driven by a per-command fixture map."""

    def __init__(
        self,
        *,
        responses: dict[tuple[str, ...], CommandResult],
        raise_on: dict[tuple[str, ...], BaseException] | None = None,
    ) -> None:
        self._responses = responses
        self._raise_on = raise_on or {}
        self.calls: list[tuple[str, ...]] = []

    async def run(self, argv: list[str]) -> CommandResult:
        key = tuple(argv)
        self.calls.append(key)
        if key in self._raise_on:
            raise self._raise_on[key]
        if key not in self._responses:
            return CommandResult(argv=key, stdout="", stderr="", exit_code=1, duration_s=0.0)
        return self._responses[key]


def _ok(argv: tuple[str, ...], stdout: str) -> CommandResult:
    return CommandResult(argv=argv, stdout=stdout, stderr="", exit_code=0, duration_s=0.0)


def _make_client(**overrides: Any) -> _FakeClient:
    base = {
        ("dmidecode", "-t", "1"): _ok(
            ("dmidecode", "-t", "1"),
            _read("dmidecode/dell_r740_system.txt"),
        ),
        ("dmidecode", "-t", "3"): _ok(
            ("dmidecode", "-t", "3"),
            _read("dmidecode/dell_r740_chassis.txt"),
        ),
        ("ip", "-o", "link", "show"): _ok(
            ("ip", "-o", "link", "show"),
            _read("ip_link/proxmox_node.txt"),
        ),
        ("ethtool", "eno1"): _ok(("ethtool", "eno1"), _read("ethtool/eno1_1g.txt")),
        ("ethtool", "eno2"): _ok(("ethtool", "eno2"), _read("ethtool/no_link.txt")),
        ("ethtool", "enp94s0f0"): _ok(
            ("ethtool", "enp94s0f0"),
            _read("ethtool/enp94s0f0_10g.txt"),
        ),
        ("ethtool", "enp94s0f1"): _ok(
            ("ethtool", "enp94s0f1"),
            _read("ethtool/enp94s0f0_10g.txt"),
        ),
    }
    base.update(overrides.get("responses", {}))
    return _FakeClient(responses=base, raise_on=overrides.get("raise_on"))


@pytest.mark.asyncio
async def test_discover_node_happy_path() -> None:
    client = _make_client()
    facts = await discover_node(client)  # type: ignore[arg-type]

    assert facts.system.product_name == "PowerEdge R740"
    assert facts.system.serial_number == "7XQZ1Y3"
    assert facts.chassis.type == "Rack Mount Chassis"
    assert facts.chassis.height_u == 2

    # DEFAULT_NIC_SKIP filters lo, vmbr0, tap100i0, fwbr100i0, bond0.
    surviving = {n.name for n in facts.nics}
    assert surviving == {"eno1", "eno2", "enp94s0f0", "enp94s0f1"}

    eno1 = next(n for n in facts.nics if n.name == "eno1")
    assert eno1.ethtool is not None
    assert eno1.ethtool.speed_mbps == 1000
    assert eno1.speed_gbps == 1.0

    enp = next(n for n in facts.nics if n.name == "enp94s0f0")
    assert enp.ethtool is not None
    assert enp.ethtool.speed_mbps == 10000
    assert enp.speed_gbps == 10.0


@pytest.mark.asyncio
async def test_discover_node_issues_exactly_the_expected_argv() -> None:
    client = _make_client()
    await discover_node(client)  # type: ignore[arg-type]

    assert client.calls[0] == ("dmidecode", "-t", "1")
    assert client.calls[1] == ("dmidecode", "-t", "3")
    assert client.calls[2] == ("ip", "-o", "link", "show")
    # The remaining calls are ethtool per surviving NIC. We don't pin order
    # beyond "ethtool comes after the three discovery commands".
    ethtool_calls = [c for c in client.calls if c[0] == "ethtool"]
    assert len(ethtool_calls) == 4
    assert {c[1] for c in ethtool_calls} == {"eno1", "eno2", "enp94s0f0", "enp94s0f1"}


@pytest.mark.asyncio
async def test_discover_node_tolerates_ethtool_nonzero_exit() -> None:
    failing = CommandResult(
        argv=("ethtool", "eno2"),
        stdout="",
        stderr="Operation not supported",
        exit_code=75,
        duration_s=0.0,
    )
    client = _make_client(responses={("ethtool", "eno2"): failing})
    facts = await discover_node(client)  # type: ignore[arg-type]
    eno2 = next(n for n in facts.nics if n.name == "eno2")
    # Non-zero ethtool exit must drop the link facts but keep the NIC.
    assert eno2.ethtool is None
    assert eno2.mac_address is not None


@pytest.mark.asyncio
async def test_discover_node_tolerates_per_nic_exception() -> None:
    client = _make_client(raise_on={("ethtool", "eno1"): RuntimeError("boom")})
    facts = await discover_node(client)  # type: ignore[arg-type]
    eno1 = next(n for n in facts.nics if n.name == "eno1")
    assert eno1.ethtool is None
    # The other three NICs still have ethtool data.
    enp = next(n for n in facts.nics if n.name == "enp94s0f0")
    assert enp.ethtool is not None


@pytest.mark.asyncio
async def test_discover_node_propagates_command_not_allowed() -> None:
    client = _make_client(raise_on={("ethtool", "eno1"): CommandNotAllowed("ethtool not allowed")})
    # If the SSH-side allowlist refuses ethtool we MUST abort rather than
    # silently emit blank NIC speeds across the fleet.
    with pytest.raises(CommandNotAllowed):
        await discover_node(client)  # type: ignore[arg-type]


def test_default_nic_skip_matches_expected_virtuals() -> None:
    for name in ("lo", "vmbr0", "vmbr99", "tap100i0", "fwbr100i0", "bond0", "veth1234", "wg0"):
        assert DEFAULT_NIC_SKIP.match(name), f"expected {name} to be skipped"
    for name in ("eno1", "eth0", "enp94s0f0", "ens3"):
        assert not DEFAULT_NIC_SKIP.match(name), f"expected {name} to survive"

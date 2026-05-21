"""Live Proxmox API smoke tests — Proxmox VE 9.2 feature coverage.

These tests hit a real Proxmox node and are excluded from CI by default
(see ``markers`` in ``pyproject.toml`` and ``pytest -m live`` to opt in).

Required environment variables:

- ``PROXMOX_API_URL`` (e.g. ``https://10.0.30.95:8006``)
- ``PROXMOX_API_TOKEN_ID`` (e.g. ``root@pam!proxbox``)
- ``PROXMOX_API_TOKEN_SECRET``

Write tests (create/delete a temporary API token) require an extra opt-in:

- ``PROXMOX_LIVE_WRITE_TESTS=1``
"""

from __future__ import annotations

import os
import secrets
from urllib.parse import urlsplit

import pytest

pytestmark = pytest.mark.live


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
async def sdk():
    url = os.getenv("PROXMOX_API_URL")
    token_id = os.getenv("PROXMOX_API_TOKEN_ID")
    token_secret = os.getenv("PROXMOX_API_TOKEN_SECRET")
    if not (url and token_id and token_secret):
        pytest.skip(
            "PROXMOX_API_URL / PROXMOX_API_TOKEN_ID / PROXMOX_API_TOKEN_SECRET not set",
        )

    from proxmox_sdk.sdk import ProxmoxSDK
    from proxmox_sdk.sdk.auth.token import parse_token_id

    user, token_name = parse_token_id(token_id)
    parsed = urlsplit(url)
    host = parsed.hostname or url
    port = parsed.port

    instance = ProxmoxSDK(
        host=host,
        user=user,
        token_name=token_name,
        token_value=token_secret,
        service="PVE",
        backend="https",
        port=port,
        verify_ssl=False,
    )
    try:
        yield instance
    finally:
        await instance.close()


@pytest.fixture
async def node_name(sdk) -> str:
    """Return the name of the first available cluster node."""
    nodes = await sdk.nodes.get()
    assert nodes, "cluster returned an empty node list"
    return nodes[0]["node"]


@pytest.fixture
def write_enabled() -> None:
    """Gate write tests behind PROXMOX_LIVE_WRITE_TESTS=1."""
    if os.getenv("PROXMOX_LIVE_WRITE_TESTS", "").strip() not in ("1", "true", "yes"):
        pytest.skip("write tests disabled — set PROXMOX_LIVE_WRITE_TESTS=1 to enable")


# ---------------------------------------------------------------------------
# Version / basic connectivity
# ---------------------------------------------------------------------------


async def test_live_version_is_9_2(sdk) -> None:
    """Version string must start with '9.2' — confirms the node is Proxmox VE 9.2.x."""
    info = await sdk.version.get()
    version = (info or {}).get("version") or ""
    assert version.startswith("9.2"), (
        f"expected Proxmox 9.2.x on live node, got {version!r}"
    )


# ---------------------------------------------------------------------------
# Cluster-level read tests
# ---------------------------------------------------------------------------


async def test_live_nodes_list(sdk) -> None:
    """Node list is non-empty; each entry has 'node' and 'status' keys."""
    nodes = await sdk.nodes.get()
    assert isinstance(nodes, list) and nodes, "expected a non-empty node list"
    for n in nodes:
        assert "node" in n, f"node entry missing 'node' key: {n}"
        assert "status" in n, f"node entry missing 'status' key: {n}"


async def test_live_cluster_resources(sdk) -> None:
    """Cluster resource index (/cluster/resources) is reachable and non-empty."""
    resources = await sdk.cluster.resources.get()
    assert isinstance(resources, list) and resources, "expected non-empty cluster resources"


async def test_live_cluster_options_crs(sdk) -> None:
    """GET /cluster/options — validates CRS (Dynamic Load Balancing) key (new in 9.2).

    The ``crs`` sub-object appears in datacenter config on Proxmox VE 9.2+.
    Its value is an empty dict when CRS is not explicitly configured.
    An xfail is raised (not a hard failure) if the key is absent.
    """
    opts = await sdk.cluster.options.get()
    assert isinstance(opts, dict), (
        f"expected a dict from /cluster/options, got {type(opts)}"
    )
    crs_value = opts.get("crs")
    print(f"\n[live] cluster CRS config: {crs_value!r}")
    if "crs" not in opts:
        pytest.xfail(
            "'crs' key absent from cluster options — node may need explicit CRS config; "
            "expected to be present on PVE 9.2+"
        )


async def test_live_ha_resources(sdk) -> None:
    """GET /cluster/ha/resources — HA resource list is reachable."""
    resources = await sdk.cluster.ha.resources.get()
    assert isinstance(resources, list), (
        f"expected list from /cluster/ha/resources, got {type(resources)}"
    )


async def test_live_ha_groups_deprecated(sdk) -> None:
    """GET /cluster/ha/groups — deprecated in 9.2; replaced by /cluster/ha/rules.

    Proxmox VE 9.2 migrated HA groups to affinity rules.  The old endpoint
    returns HTTP 500 with "ha groups have been migrated to rules" on upgraded
    clusters.  This test documents the migration and marks it as xfail.
    """
    from proxmox_sdk.sdk.exceptions import ResourceException

    try:
        groups = await sdk.cluster.ha.groups.get()
        # If it succeeds, the cluster has not yet migrated — that's fine too.
        assert isinstance(groups, list), (
            f"expected list from /cluster/ha/groups, got {type(groups)}"
        )
    except ResourceException as exc:
        if "migrated to rules" in str(exc).lower():
            pytest.xfail(
                "/cluster/ha/groups is deprecated in PVE 9.2 — groups migrated to "
                "/cluster/ha/rules (affinity rules); see test_live_ha_rules"
            )
        raise


async def test_live_ha_rules(sdk) -> None:
    """GET /cluster/ha/rules — new in 9.2, replaces HA groups with affinity rules."""
    rules = await sdk.cluster.ha.rules.get()
    assert isinstance(rules, list), (
        f"expected list from /cluster/ha/rules, got {type(rules)}"
    )
    print(f"\n[live] HA affinity rules count: {len(rules)}")
    if rules:
        print(f"[live] sample rule keys: {sorted(rules[0].keys())}")


async def test_live_ha_status_current(sdk) -> None:
    """GET /cluster/ha/status/current — HA status is reachable (includes CRS state)."""
    status = await sdk.cluster.ha.status.current.get()
    assert isinstance(status, (list, dict)), (
        f"expected list or dict from /cluster/ha/status/current, got {type(status)}"
    )


# ---------------------------------------------------------------------------
# Node-level read tests
# ---------------------------------------------------------------------------


async def test_live_node_status(sdk, node_name) -> None:
    """GET /nodes/{node}/status — response contains 'uptime' field."""
    status = await sdk.nodes(node_name).status.get()
    assert isinstance(status, dict), (
        f"expected dict from /nodes/{node_name}/status, got {type(status)}"
    )
    assert "uptime" in status, (
        f"'uptime' missing from node status keys: {sorted(status.keys())}"
    )


async def test_live_storage_list(sdk, node_name) -> None:
    """GET /nodes/{node}/storage — storage list is non-empty."""
    storages = await sdk.nodes(node_name).storage.get()
    assert isinstance(storages, list) and storages, (
        f"expected non-empty storage list for node {node_name!r}"
    )
    for s in storages:
        assert "storage" in s, f"storage entry missing 'storage' key: {s}"


async def test_live_vms_list(sdk, node_name) -> None:
    """GET /nodes/{node}/qemu — QEMU VM list is reachable."""
    vms = await sdk.nodes(node_name).qemu.get()
    assert isinstance(vms, list), (
        f"expected list from /nodes/{node_name}/qemu, got {type(vms)}"
    )


async def test_live_lxc_list(sdk, node_name) -> None:
    """GET /nodes/{node}/lxc — LXC container list is reachable."""
    containers = await sdk.nodes(node_name).lxc.get()
    assert isinstance(containers, list), (
        f"expected list from /nodes/{node_name}/lxc, got {type(containers)}"
    )


# ---------------------------------------------------------------------------
# Access control read tests
# ---------------------------------------------------------------------------


async def test_live_access_users(sdk) -> None:
    """GET /access/users — user list is reachable and non-empty."""
    users = await sdk.access.users.get()
    assert isinstance(users, list) and users, "expected non-empty access user list"


# ---------------------------------------------------------------------------
# SDN read tests
# ---------------------------------------------------------------------------


async def test_live_sdn_zones(sdk) -> None:
    """GET /cluster/sdn/zones — zones reachable (9.2 adds them to ACL permission paths)."""
    zones = await sdk.cluster.sdn.zones.get()
    assert isinstance(zones, list), (
        f"expected list from /cluster/sdn/zones, got {type(zones)}"
    )


# ---------------------------------------------------------------------------
# Write tests (PROXMOX_LIVE_WRITE_TESTS=1 required)
# ---------------------------------------------------------------------------


async def test_live_write_cluster_options_crs_roundtrip(sdk, write_enabled) -> None:
    """PUT /cluster/options — non-destructive round-trip confirming write path works.

    Reads the current keyboard setting and writes it back unchanged.
    This exercises the PUT path for cluster options (which includes CRS config fields).
    """
    opts = await sdk.cluster.options.get()
    assert isinstance(opts, dict), (
        f"expected dict from GET /cluster/options, got {type(opts)}"
    )
    keyboard = opts.get("keyboard") or "en-us"
    result = await sdk.cluster.options.put(keyboard=keyboard)
    # PUT /cluster/options returns null on success
    assert result is None or isinstance(result, (dict, str)), (
        f"unexpected PUT response type: {type(result)}"
    )


async def test_live_access_token_lifecycle(sdk, write_enabled) -> None:
    """POST / GET / DELETE /access/users/{userid}/token/{tokenid} — full lifecycle.

    Creates a temporary access token, reads it back to verify creation,
    then deletes it in a finally block. Demonstrates the token management
    API surface (including secret rotation available in 9.2).
    """
    userid = "root@pam"
    tokenid = f"sdktest{secrets.token_hex(3)}"  # e.g. sdktestab12cd
    created = None
    try:
        created = await sdk.access.users(userid).token(tokenid).post(
            comment="proxmox-sdk live test — auto-deleted"
        )
        assert created is not None, "token creation returned nothing"
        assert "value" in created, (
            f"expected 'value' (secret) in creation response keys: {sorted(created.keys())}"
        )
        info = await sdk.access.users(userid).token(tokenid).get()
        assert info is not None, "GET on newly created token returned nothing"
        print(f"\n[live] created token info: {info}")
    finally:
        if created is not None:
            try:
                await sdk.access.users(userid).token(tokenid).delete()
            except Exception as exc:
                print(f"[live] warning: could not delete test token {tokenid!r}: {exc}")

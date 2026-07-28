"""Remote CRUD + per-remote version query."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from proxmox_sdk.pdm import PDMClient
from proxmox_sdk.pdm.models import PDMRemoteNode

from .conftest import make_pdm_sdk


async def test_remotes_list_hits_remotes_path():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/remotes/remote": {
                "data": [
                    {"id": "pve-a", "type": "pve"},
                    {"id": "pbs", "type": "pbs"},
                ]
            }
        }
    )
    pdm = PDMClient(_sdk=sdk)
    remotes = await pdm.remotes.list()
    assert [r.id for r in remotes] == ["pve-a", "pbs"]
    assert {r.type for r in remotes} == {"pve", "pbs"}
    assert backend.calls[0][1] == "/api2/json/remotes/remote"


async def test_remotes_list_normalizes_schema_node_addresses():
    sdk, _ = make_pdm_sdk(
        {
            "/api2/json/remotes/remote": {
                "data": [
                    {
                        "id": "pve-a",
                        "type": "pve",
                        "nodes": ["pve-a-1", "10.0.0.2"],
                    }
                ]
            }
        }
    )
    pdm = PDMClient(_sdk=sdk)

    remote = (await pdm.remotes.list())[0]

    assert remote.nodes == [
        PDMRemoteNode(hostname="pve-a-1"),
        PDMRemoteNode(hostname="10.0.0.2"),
    ]


async def test_remotes_get_single_remote():
    sdk, backend = make_pdm_sdk(
        {"/api2/json/remotes/remote/pve-a/config": {"data": {"id": "pve-a", "type": "pve"}}}
    )
    pdm = PDMClient(_sdk=sdk)
    r = await pdm.remotes.get("pve-a")
    assert r.id == "pve-a"
    assert backend.calls[0][1] == "/api2/json/remotes/remote/pve-a/config"


async def test_remotes_add_posts_payload():
    sdk, backend = make_pdm_sdk({"/api2/json/remotes/remote": {"data": None}})
    pdm = PDMClient(_sdk=sdk)
    await pdm.remotes.add(
        id="pve-a",
        type="pve",
        authid="root@pam!api",
        token="secret",
        nodes=[{"hostname": "pve1"}],
    )
    assert backend.calls[0][0] == "POST"
    body = backend.calls[0][3] or {}
    assert body["id"] == "pve-a"
    assert body["type"] == "pve"
    assert body["authid"] == "root@pam!api"
    assert body["nodes"] == ["pve1"]


async def test_remotes_add_accepts_public_node_models():
    sdk, backend = make_pdm_sdk({"/api2/json/remotes/remote": {"data": None}})
    pdm = PDMClient(_sdk=sdk)

    await pdm.remotes.add(
        id="pve-a",
        type="pve",
        nodes=[PDMRemoteNode(hostname="pve1")],
    )

    assert (backend.calls[0][3] or {})["nodes"] == ["pve1"]


async def test_remotes_add_rejects_malformed_node_mappings():
    sdk, backend = make_pdm_sdk({"/api2/json/remotes/remote": {"data": None}})
    pdm = PDMClient(_sdk=sdk)

    with pytest.raises(ValidationError):
        await pdm.remotes.add(
            id="pve-a",
            type="pve",
            nodes=[{"hostname": ["pve1"]}],
        )

    assert backend.calls == []


async def test_remotes_update_and_remove():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/remotes/remote/pve-a": {"data": None},
        }
    )
    pdm = PDMClient(_sdk=sdk)
    await pdm.remotes.update("pve-a", token="new-secret")
    assert backend.calls[0][0] == "PUT"
    assert (backend.calls[0][3] or {})["token"] == "new-secret"

    await pdm.remotes.remove("pve-a")
    assert backend.calls[1][0] == "DELETE"


async def test_remotes_update_normalizes_public_node_inputs():
    sdk, backend = make_pdm_sdk({"/api2/json/remotes/remote/pve-a": {"data": None}})
    pdm = PDMClient(_sdk=sdk)

    await pdm.remotes.update(
        "pve-a",
        nodes=[PDMRemoteNode(hostname="pve1"), {"hostname": "10.0.0.2"}],
    )

    assert (backend.calls[0][3] or {})["nodes"] == ["pve1", "10.0.0.2"]


async def test_remotes_update_rejects_non_list_nodes():
    sdk, backend = make_pdm_sdk({"/api2/json/remotes/remote/pve-a": {"data": None}})
    pdm = PDMClient(_sdk=sdk)

    with pytest.raises(ValueError, match="must be provided as a list"):
        await pdm.remotes.update("pve-a", nodes="pve1")

    assert backend.calls == []


async def test_remote_version_query():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/remotes/remote/pve-a/version": {
                "data": {"version": "9.1", "release": "1", "repoid": "pve01"}
            }
        }
    )
    pdm = PDMClient(_sdk=sdk)
    v = await pdm.remotes.version("pve-a")
    assert v.version == "9.1"
    assert backend.calls[0][1] == "/api2/json/remotes/remote/pve-a/version"

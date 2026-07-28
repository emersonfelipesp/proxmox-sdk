"""Global resources, subscriptions, metric collection, views."""

from __future__ import annotations

from proxmox_sdk.pdm import PDMClient

from .conftest import make_pdm_sdk


async def test_resources_list_with_type_filter():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/resources/list": {
                "data": [
                    {
                        "remote": "pve-a",
                        "resources": [{"type": "pve-qemu", "id": "qemu/100"}],
                    },
                ]
            }
        }
    )
    pdm = PDMClient(_sdk=sdk)
    rsc = await pdm.resources.list(type="vm")
    assert rsc[0].id == "qemu/100"
    assert rsc[0].remote == "pve-a"
    assert (backend.calls[0][2] or {})["resource-type"] == "qemu"


async def test_resources_status_path():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/resources/status": {
                "data": {
                    "remote": "pve-a",
                    "resources": [{"type": "pve-node", "id": "node/pve-a-1"}],
                }
            }
        }
    )
    pdm = PDMClient(_sdk=sdk)
    status = await pdm.resources.status()
    assert status.remote == "pve-a"
    assert status.resources[0].id == "node/pve-a-1"
    assert backend.calls[0][1] == "/api2/json/resources/status"


async def test_subscriptions_list_path():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/resources/subscription": {
                "data": [{"remote": "pve-a", "state": "active", "node-status": {}}]
            }
        }
    )
    pdm = PDMClient(_sdk=sdk)
    subs = await pdm.subscriptions.list()
    assert subs[0].state == "active"
    assert backend.calls[0][1] == "/api2/json/resources/subscription"


async def test_metrics_status_and_trigger():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/remotes/metric-collection/status": {
                "data": [{"remote": "pve-a", "last-collection": 1_700_000_000}]
            },
            "/api2/json/remotes/metric-collection/trigger": {"data": "UPID:metrics:1"},
        }
    )
    pdm = PDMClient(_sdk=sdk)
    statuses = await pdm.metrics.status()
    assert statuses[0].remote == "pve-a"
    assert statuses[0].last_collection == 1_700_000_000

    upid = await pdm.metrics.trigger()
    assert upid == "UPID:metrics:1"
    assert backend.calls[1][0] == "POST"


async def test_views_crud_paths():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/config/views": {"data": [{"id": "ops", "include": ["tag=operations"]}]},
            "/api2/json/config/views/ops": {"data": {"id": "ops", "include": ["tag=operations"]}},
        }
    )
    pdm = PDMClient(_sdk=sdk)
    views = await pdm.views.list()
    assert views[0].id == "ops"

    v = await pdm.views.get("ops")
    assert v.include == ["tag=operations"]

    await pdm.views.create(id="dev", name="Dev")
    assert backend.calls[2][0] == "POST"
    assert (backend.calls[2][3] or {})["id"] == "dev"

"""PBS-via-PDM operations: datastores, snapshots, RRD, tasks."""

from __future__ import annotations

from proxmox_sdk.pdm import PDMClient

from .conftest import make_pdm_sdk


async def test_pbs_datastores_list_injects_remote():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/pbs/remotes/pbs-main/datastore": {
                "data": [{"store": "tank", "total": 1000, "used": 100}]
            }
        }
    )
    pdm = PDMClient(_sdk=sdk)
    ds = await pdm.pbs.datastores("pbs-main")
    assert ds[0].store == "tank"
    assert ds[0].remote == "pbs-main"
    assert backend.calls[0][1] == "/api2/json/pbs/remotes/pbs-main/datastore"


async def test_pbs_datastore_rrddata_path_and_params():
    sdk, backend = make_pdm_sdk(
        {"/api2/json/pbs/remotes/pbs-main/datastore/tank/rrddata": {"data": [{"time": 1}]}}
    )
    pdm = PDMClient(_sdk=sdk)
    await pdm.pbs.datastore_rrddata("pbs-main", "tank", timeframe="week", cf="AVERAGE")
    assert (backend.calls[0][2] or {})["timeframe"] == "week"
    assert (backend.calls[0][2] or {})["cf"] == "AVERAGE"


async def test_pbs_snapshots_filters_by_namespace():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/pbs/remotes/pbs-main/datastore/tank/snapshots": {
                "data": [{"backup-type": "vm", "backup-id": "100", "backup-time": 1700000000}]
            }
        }
    )
    pdm = PDMClient(_sdk=sdk)
    snaps = await pdm.pbs.snapshots("pbs-main", "tank", namespace="prod")
    assert snaps[0].backup_id == "100"
    assert snaps[0].store == "tank"
    assert snaps[0].remote == "pbs-main"
    assert (backend.calls[0][2] or {})["ns"] == "prod"


async def test_pbs_tasks_list_and_status():
    sdk, _ = make_pdm_sdk(
        {
            "/api2/json/pbs/remotes/pbs-main/tasks": {"data": [{"upid": "UPID:pbs:1"}]},
            "/api2/json/pbs/remotes/pbs-main/tasks/UPID%3Apbs%3A1/status": {
                "data": {"upid": "UPID:pbs:1", "status": "OK"}
            },
        }
    )
    pdm = PDMClient(_sdk=sdk)
    tasks = await pdm.pbs.tasks("pbs-main")
    assert tasks[0].upid == "UPID:pbs:1"
    status = await pdm.pbs.task_status("pbs-main", "UPID:pbs:1")
    assert status.status == "OK"


async def test_pbs_node_rrddata():
    sdk, backend = make_pdm_sdk(
        {"/api2/json/pbs/remotes/pbs-main/rrddata": {"data": [{"time": 1}]}}
    )
    pdm = PDMClient(_sdk=sdk)
    rrd = await pdm.pbs.node_rrddata("pbs-main")
    assert rrd[0].time == 1
    assert backend.calls[0][1] == "/api2/json/pbs/remotes/pbs-main/rrddata"

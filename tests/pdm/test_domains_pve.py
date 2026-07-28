"""PVE-via-PDM operations: nodes, qemu/lxc, resources, tasks, RRD."""

from __future__ import annotations

from proxmox_sdk.pdm import PDMClient

from .conftest import make_pdm_sdk


async def test_qemu_list_returns_guests_with_remote_injected():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/pve/remotes/pve-a/qemu": {
                "data": [
                    {"vmid": 100, "name": "web", "status": "running", "cpus": 4.5},
                    {"vmid": 101, "name": "db", "status": "stopped"},
                ]
            }
        }
    )
    pdm = PDMClient(_sdk=sdk)
    guests = await pdm.pve.qemu.list("pve-a")
    assert [g.vmid for g in guests] == [100, 101]
    assert all(g.remote == "pve-a" for g in guests)
    assert all(g.type == "qemu" for g in guests)
    assert guests[0].cpus == 4.5
    assert backend.calls[0][1] == "/api2/json/pve/remotes/pve-a/qemu"


async def test_lxc_list_uses_lxc_path():
    sdk, backend = make_pdm_sdk(
        {"/api2/json/pve/remotes/pve-a/lxc": {"data": [{"vmid": 200, "cpus": 2.5}]}}
    )
    pdm = PDMClient(_sdk=sdk)
    cts = await pdm.pve.lxc.list("pve-a")
    assert cts[0].type == "lxc"
    assert cts[0].cpus == 2.5
    assert backend.calls[0][1] == "/api2/json/pve/remotes/pve-a/lxc"


async def test_qemu_lifecycle_endpoints():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/pve/remotes/pve-a/qemu/100/start": {"data": "UPID:x"},
            "/api2/json/pve/remotes/pve-a/qemu/100/stop": {"data": "UPID:y"},
            "/api2/json/pve/remotes/pve-a/qemu/100/shutdown": {"data": "UPID:z"},
        }
    )
    pdm = PDMClient(_sdk=sdk)
    assert await pdm.pve.qemu.start("pve-a", 100) == "UPID:x"
    assert await pdm.pve.qemu.stop("pve-a", 100) == "UPID:y"
    assert await pdm.pve.qemu.shutdown("pve-a", 100) == "UPID:z"
    assert [c[0] for c in backend.calls] == ["POST", "POST", "POST"]


async def test_qemu_migrate_passes_target():
    sdk, backend = make_pdm_sdk(
        {"/api2/json/pve/remotes/pve-a/qemu/100/migrate": {"data": "UPID:m"}}
    )
    pdm = PDMClient(_sdk=sdk)
    await pdm.pve.qemu.migrate("pve-a", 100, target="pve2", online=True)
    body = backend.calls[0][3] or {}
    assert body["target"] == "pve2"
    assert body["online"] is True


async def test_qemu_remote_migrate_passes_hyphenated_params():
    sdk, backend = make_pdm_sdk(
        {"/api2/json/pve/remotes/pve-a/qemu/100/remote-migrate": {"data": "UPID:r"}}
    )
    pdm = PDMClient(_sdk=sdk)
    await pdm.pve.qemu.remote_migrate(
        "pve-a", 100, target_remote="pve-b", target_vmid=999, target_node="n1"
    )
    body = backend.calls[0][3] or {}
    assert body["target-remote"] == "pve-b"
    assert body["target-vmid"] == 999
    assert body["target-node"] == "n1"


async def test_qemu_config_unwraps_data():
    sdk, backend = make_pdm_sdk(
        {
            "/api2/json/pve/remotes/pve-a/qemu/100/config": {
                "data": {"name": "web", "cores": 4, "memory": "current=4096"}
            }
        }
    )
    pdm = PDMClient(_sdk=sdk)
    cfg = await pdm.pve.qemu.config("pve-a", 100)
    assert cfg.name == "web"
    assert cfg.cores == 4
    assert cfg.memory == "current=4096"
    assert (backend.calls[0][2] or {})["state"] == "pending"


async def test_qemu_rrddata_passes_timeframe():
    sdk, backend = make_pdm_sdk(
        {"/api2/json/pve/remotes/pve-a/qemu/100/rrddata": {"data": [{"time": 1, "cpu": 0.1}]}}
    )
    pdm = PDMClient(_sdk=sdk)
    rrd = await pdm.pve.qemu.rrddata("pve-a", 100, timeframe="day")
    assert rrd[0].cpu == 0.1
    assert (backend.calls[0][2] or {})["timeframe"] == "day"
    assert (backend.calls[0][2] or {})["cf"] == "AVERAGE"


async def test_pve_nodes_list_injects_remote():
    sdk, _ = make_pdm_sdk(
        {"/api2/json/pve/remotes/pve-a/nodes": {"data": [{"node": "n1", "status": "online"}]}}
    )
    pdm = PDMClient(_sdk=sdk)
    nodes = await pdm.pve.nodes("pve-a")
    assert nodes[0].node == "n1"
    assert nodes[0].remote == "pve-a"


async def test_pve_resources_with_type_filter():
    sdk, backend = make_pdm_sdk(
        {"/api2/json/pve/remotes/pve-a/resources": {"data": [{"id": "qemu/100", "type": "qemu"}]}}
    )
    pdm = PDMClient(_sdk=sdk)
    res = await pdm.pve.resources("pve-a", type="vm")
    assert res[0].id == "qemu/100"
    assert (backend.calls[0][2] or {})["kind"] == "vm"


async def test_pve_tasks_list():
    sdk, _ = make_pdm_sdk(
        {"/api2/json/pve/remotes/pve-a/tasks": {"data": [{"upid": "UPID:n1:1234", "status": "OK"}]}}
    )
    pdm = PDMClient(_sdk=sdk)
    tasks = await pdm.pve.tasks("pve-a")
    assert tasks[0].upid.startswith("UPID:")

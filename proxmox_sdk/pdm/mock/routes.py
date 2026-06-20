"""Hand-coded FastAPI route handlers for the PDM mock server.

Every PDM SDK code path in :mod:`proxmox_sdk.pdm.domains` has a matching
route here so E2E tests can exercise the SDK end-to-end without a live PDM
instance. State is held in-memory in :class:`PDMMockState`; mutations
(register a remote, add a user, edit an ACL) survive within the process
lifetime and can be exported/imported via the dedicated ``/mock/*``
management endpoints.
"""

from __future__ import annotations

import copy
import json
import threading
from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException, Request

from proxmox_sdk.pdm.mock.seed_data import get_default_pdm_seed

_API_PREFIX = "/api2/json"


class PDMMockState:
    """In-memory PDM mock state with thread-safe read/write access.

    The state mirrors the structure returned by
    :func:`proxmox_sdk.pdm.mock.seed_data.get_default_pdm_seed`. All
    mutations go through ``replace`` / accessor helpers under a single lock
    so concurrent FastAPI requests don't race.
    """

    def __init__(self, seed: dict[str, Any] | None = None) -> None:
        self._lock = threading.RLock()
        self._state: dict[str, Any] = copy.deepcopy(seed or get_default_pdm_seed())

    # -- accessors -----------------------------------------------------

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return copy.deepcopy(self._state)

    def replace(self, new_state: dict[str, Any]) -> None:
        with self._lock:
            self._state = copy.deepcopy(new_state)

    def reset(self) -> None:
        with self._lock:
            self._state = get_default_pdm_seed()

    def section(self, key: str) -> Any:
        with self._lock:
            return self._state.get(key)

    def write(self, key: str, value: Any) -> None:
        with self._lock:
            self._state[key] = value

    # -- bulk helpers --------------------------------------------------

    def remotes(self) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._state.get("remotes", []))

    def find_remote(self, remote_id: str) -> dict[str, Any] | None:
        for r in self.remotes():
            if r.get("id") == remote_id:
                return r
        return None

    def upsert_remote(self, remote: dict[str, Any]) -> None:
        with self._lock:
            remotes = list(self._state.get("remotes", []))
            for i, r in enumerate(remotes):
                if r.get("id") == remote.get("id"):
                    remotes[i] = {**r, **remote}
                    break
            else:
                remotes.append(remote)
            self._state["remotes"] = remotes

    def remove_remote(self, remote_id: str) -> bool:
        with self._lock:
            remotes = self._state.get("remotes", [])
            new = [r for r in remotes if r.get("id") != remote_id]
            self._state["remotes"] = new
            return len(new) != len(remotes)

    # -- pve guests ----------------------------------------------------

    def _pve_bucket(self, remote: str) -> dict[str, Any]:
        with self._lock:
            return self._state.setdefault("pve", {}).setdefault(
                remote,
                {"nodes": [], "qemu": [], "lxc": [], "tasks": []},
            )

    def list_guests(self, remote: str, kind: str) -> list[dict[str, Any]]:
        bucket = self._pve_bucket(remote)
        return list(bucket.get(kind, []))

    def find_guest(self, remote: str, kind: str, vmid: int) -> dict[str, Any] | None:
        for g in self.list_guests(remote, kind):
            if int(g.get("vmid", -1)) == int(vmid):
                return g
        return None

    def update_guest_status(self, remote: str, kind: str, vmid: int, status: str) -> bool:
        with self._lock:
            bucket = self._pve_bucket(remote)
            for g in bucket.get(kind, []):
                if int(g.get("vmid", -1)) == int(vmid):
                    g["status"] = status
                    return True
        return False


# ---------------------------------------------------------------------------
# Route registration
# ---------------------------------------------------------------------------


def register_generated_pdm_mock_routes(
    app: FastAPI,
    *,
    state: PDMMockState | None = None,
    seed: dict[str, Any] | None = None,
) -> PDMMockState:
    """Attach all PDM mock routes to ``app`` and return its mutable state.

    Pass an existing ``state`` to share mutable state across multiple mock
    apps (e.g. a CLI + a test process), or pass ``seed`` to bootstrap a
    fresh state with custom fixture data.
    """
    mock_state = state if state is not None else PDMMockState(seed=seed)

    def wrap(data: Any) -> dict[str, Any]:
        return {"data": data}

    # -- /version --------------------------------------------------------

    @app.get(f"{_API_PREFIX}/version")
    async def version() -> dict[str, Any]:
        return wrap(mock_state.section("version") or {})

    # -- /remotes/remote -------------------------------------------------

    @app.get(f"{_API_PREFIX}/remotes/remote")
    async def remotes_list() -> dict[str, Any]:
        return wrap(mock_state.remotes())

    @app.post(f"{_API_PREFIX}/remotes/remote")
    async def remotes_create(request: Request) -> dict[str, Any]:
        body = await _read_body(request)
        if not body.get("id") or not body.get("type"):
            raise HTTPException(status_code=400, detail="id and type are required")
        mock_state.upsert_remote(body)
        return wrap(None)

    @app.get(f"{_API_PREFIX}/remotes/remote/{{id}}")
    async def remote_get(id: str) -> dict[str, Any]:
        r = mock_state.find_remote(id)
        if r is None:
            raise HTTPException(status_code=404, detail=f"remote '{id}' not found")
        return wrap(r)

    @app.put(f"{_API_PREFIX}/remotes/remote/{{id}}")
    async def remote_update(id: str, request: Request) -> dict[str, Any]:
        r = mock_state.find_remote(id)
        if r is None:
            raise HTTPException(status_code=404, detail=f"remote '{id}' not found")
        body = await _read_body(request)
        mock_state.upsert_remote({**r, **body, "id": id})
        return wrap(None)

    @app.delete(f"{_API_PREFIX}/remotes/remote/{{id}}")
    async def remote_delete(id: str) -> dict[str, Any]:
        if not mock_state.remove_remote(id):
            raise HTTPException(status_code=404, detail=f"remote '{id}' not found")
        return wrap(None)

    @app.get(f"{_API_PREFIX}/remotes/remote/{{id}}/version")
    async def remote_version(id: str) -> dict[str, Any]:
        versions = mock_state.section("remote_versions") or {}
        if id not in versions:
            raise HTTPException(status_code=404, detail=f"remote '{id}' not found")
        return wrap(versions[id])

    # -- /pve/remotes/{remote}/... --------------------------------------

    @app.get(f"{_API_PREFIX}/pve/remotes/{{remote}}/nodes")
    async def pve_nodes(remote: str) -> dict[str, Any]:
        bucket = mock_state._pve_bucket(remote)
        return wrap(list(bucket.get("nodes", [])))

    @app.get(f"{_API_PREFIX}/pve/remotes/{{remote}}/nodes/{{node}}/rrddata")
    async def pve_node_rrd(remote: str, node: str) -> dict[str, Any]:
        _ = remote, node
        return wrap(_synthetic_rrd())

    @app.get(f"{_API_PREFIX}/pve/remotes/{{remote}}/resources")
    async def pve_resources(remote: str, type: str | None = None) -> dict[str, Any]:
        bucket = mock_state._pve_bucket(remote)
        entries: list[dict[str, Any]] = []
        for vm in bucket.get("qemu", []):
            entries.append({**vm, "id": f"qemu/{vm.get('vmid')}", "type": "qemu"})
        for ct in bucket.get("lxc", []):
            entries.append({**ct, "id": f"lxc/{ct.get('vmid')}", "type": "lxc"})
        if type is not None:
            entries = [e for e in entries if e.get("type") == type]
        return wrap(entries)

    @app.get(f"{_API_PREFIX}/pve/remotes/{{remote}}/tasks")
    async def pve_tasks(remote: str) -> dict[str, Any]:
        bucket = mock_state._pve_bucket(remote)
        return wrap(list(bucket.get("tasks", [])))

    @app.get(f"{_API_PREFIX}/pve/remotes/{{remote}}/{{kind}}")
    async def guests_list(remote: str, kind: str) -> dict[str, Any]:
        return wrap(mock_state.list_guests(remote, kind))

    @app.get(f"{_API_PREFIX}/pve/remotes/{{remote}}/{{kind}}/{{vmid}}/config")
    async def guest_config(remote: str, kind: str, vmid: int) -> dict[str, Any]:
        g = mock_state.find_guest(remote, kind, vmid)
        if g is None:
            raise HTTPException(status_code=404, detail="guest not found")
        return wrap(
            {
                "name": g.get("name"),
                "cores": g.get("cpus"),
                "memory": (g.get("maxmem") or 0) // (1024 * 1024) or None,
                "ostype": "l26",
                "boot": "order=scsi0",
            }
        )

    @app.post(f"{_API_PREFIX}/pve/remotes/{{remote}}/{{kind}}/{{vmid}}/start")
    async def guest_start(remote: str, kind: str, vmid: int) -> dict[str, Any]:
        if not mock_state.update_guest_status(remote, kind, vmid, "running"):
            raise HTTPException(status_code=404, detail="guest not found")
        return wrap(f"UPID:{remote}:0001:start:{vmid}")

    @app.post(f"{_API_PREFIX}/pve/remotes/{{remote}}/{{kind}}/{{vmid}}/stop")
    async def guest_stop(remote: str, kind: str, vmid: int) -> dict[str, Any]:
        if not mock_state.update_guest_status(remote, kind, vmid, "stopped"):
            raise HTTPException(status_code=404, detail="guest not found")
        return wrap(f"UPID:{remote}:0002:stop:{vmid}")

    @app.post(f"{_API_PREFIX}/pve/remotes/{{remote}}/{{kind}}/{{vmid}}/shutdown")
    async def guest_shutdown(remote: str, kind: str, vmid: int) -> dict[str, Any]:
        if not mock_state.update_guest_status(remote, kind, vmid, "stopped"):
            raise HTTPException(status_code=404, detail="guest not found")
        return wrap(f"UPID:{remote}:0003:shutdown:{vmid}")

    @app.post(f"{_API_PREFIX}/pve/remotes/{{remote}}/{{kind}}/{{vmid}}/migrate")
    async def guest_migrate(remote: str, kind: str, vmid: int) -> dict[str, Any]:
        if mock_state.find_guest(remote, kind, vmid) is None:
            raise HTTPException(status_code=404, detail="guest not found")
        return wrap(f"UPID:{remote}:0004:migrate:{vmid}")

    @app.post(f"{_API_PREFIX}/pve/remotes/{{remote}}/{{kind}}/{{vmid}}/remote-migrate")
    async def guest_remote_migrate(remote: str, kind: str, vmid: int) -> dict[str, Any]:
        if mock_state.find_guest(remote, kind, vmid) is None:
            raise HTTPException(status_code=404, detail="guest not found")
        return wrap(f"UPID:{remote}:0005:remote-migrate:{vmid}")

    @app.get(f"{_API_PREFIX}/pve/remotes/{{remote}}/{{kind}}/{{vmid}}/rrddata")
    async def guest_rrd(remote: str, kind: str, vmid: int) -> dict[str, Any]:
        _ = remote, kind, vmid
        return wrap(_synthetic_rrd())

    # -- /pbs/remotes/{remote}/... --------------------------------------

    @app.get(f"{_API_PREFIX}/pbs/remotes/{{remote}}/datastore")
    async def pbs_datastores(remote: str) -> dict[str, Any]:
        pbs = mock_state.section("pbs") or {}
        return wrap(list(pbs.get(remote, {}).get("datastores", [])))

    @app.get(f"{_API_PREFIX}/pbs/remotes/{{remote}}/datastore/{{datastore}}/rrddata")
    async def pbs_datastore_rrd(remote: str, datastore: str) -> dict[str, Any]:
        _ = remote, datastore
        return wrap(_synthetic_rrd())

    @app.get(f"{_API_PREFIX}/pbs/remotes/{{remote}}/datastore/{{datastore}}/snapshots")
    async def pbs_snapshots(remote: str, datastore: str, ns: str | None = None) -> dict[str, Any]:
        pbs = mock_state.section("pbs") or {}
        snaps = [s for s in pbs.get(remote, {}).get("snapshots", []) if s.get("store") == datastore]
        if ns is not None:
            snaps = [s for s in snaps if s.get("namespace") == ns]
        return wrap(snaps)

    @app.get(f"{_API_PREFIX}/pbs/remotes/{{remote}}/rrddata")
    async def pbs_node_rrd(remote: str) -> dict[str, Any]:
        _ = remote
        return wrap(_synthetic_rrd())

    @app.get(f"{_API_PREFIX}/pbs/remotes/{{remote}}/tasks")
    async def pbs_tasks(remote: str) -> dict[str, Any]:
        pbs = mock_state.section("pbs") or {}
        return wrap(list(pbs.get(remote, {}).get("tasks", [])))

    @app.get(f"{_API_PREFIX}/pbs/remotes/{{remote}}/tasks/{{upid}}/status")
    async def pbs_task_status(remote: str, upid: str) -> dict[str, Any]:
        return wrap({"upid": upid, "node": remote, "status": "OK"})

    # -- /resources, /resources/status, /resources/subscription --------

    @app.get(f"{_API_PREFIX}/resources/list")
    async def resources_list(type: str | None = None) -> dict[str, Any]:
        entries: list[dict[str, Any]] = []
        pve = mock_state.section("pve") or {}
        for remote_id, bucket in pve.items():
            for vm in bucket.get("qemu", []):
                entries.append(
                    {
                        "remote": remote_id,
                        "type": "qemu",
                        "id": f"qemu/{vm.get('vmid')}",
                        "name": vm.get("name"),
                        "node": vm.get("node"),
                        "status": vm.get("status"),
                    }
                )
            for ct in bucket.get("lxc", []):
                entries.append(
                    {
                        "remote": remote_id,
                        "type": "lxc",
                        "id": f"lxc/{ct.get('vmid')}",
                        "name": ct.get("name"),
                        "node": ct.get("node"),
                        "status": ct.get("status"),
                    }
                )
        if type is not None:
            entries = [e for e in entries if e.get("type") == type]
        return wrap(entries)

    @app.get(f"{_API_PREFIX}/resources/status")
    async def resources_status() -> dict[str, Any]:
        return wrap((mock_state.section("resources") or {}).get("status", []))

    @app.get(f"{_API_PREFIX}/resources/subscription")
    async def resources_subscription() -> dict[str, Any]:
        return wrap((mock_state.section("resources") or {}).get("subscriptions", []))

    # -- /remotes/metric-collection, /config/views -----------------------

    @app.get(f"{_API_PREFIX}/remotes/metric-collection/status")
    async def metrics_status() -> dict[str, Any]:
        return wrap((mock_state.section("metrics") or {}).get("status", {}))

    @app.post(f"{_API_PREFIX}/remotes/metric-collection/trigger")
    async def metrics_trigger() -> dict[str, Any]:
        return wrap("UPID:pdm:metrics:0001:trigger")

    @app.get(f"{_API_PREFIX}/config/views")
    async def views_list() -> dict[str, Any]:
        return wrap(list(mock_state.section("views") or []))

    @app.post(f"{_API_PREFIX}/config/views")
    async def views_create(request: Request) -> dict[str, Any]:
        body = await _read_body(request)
        if not body.get("id"):
            raise HTTPException(status_code=400, detail="id is required")
        views = list(mock_state.section("views") or [])
        views.append(body)
        mock_state.write("views", views)
        return wrap(None)

    @app.get(f"{_API_PREFIX}/config/views/{{view_id}}")
    async def views_get(view_id: str) -> dict[str, Any]:
        for v in mock_state.section("views") or []:
            if v.get("id") == view_id:
                return wrap(v)
        raise HTTPException(status_code=404, detail=f"view '{view_id}' not found")

    @app.put(f"{_API_PREFIX}/config/views/{{view_id}}")
    async def views_update(view_id: str, request: Request) -> dict[str, Any]:
        body = await _read_body(request)
        views = list(mock_state.section("views") or [])
        for i, v in enumerate(views):
            if v.get("id") == view_id:
                views[i] = {**v, **body, "id": view_id}
                mock_state.write("views", views)
                return wrap(None)
        raise HTTPException(status_code=404, detail=f"view '{view_id}' not found")

    @app.delete(f"{_API_PREFIX}/config/views/{{view_id}}")
    async def views_delete(view_id: str) -> dict[str, Any]:
        views = list(mock_state.section("views") or [])
        new = [v for v in views if v.get("id") != view_id]
        if len(new) == len(views):
            raise HTTPException(status_code=404, detail=f"view '{view_id}' not found")
        mock_state.write("views", new)
        return wrap(None)

    # -- /access/users + /access/acl + /access/tfa + tokens -------------

    @app.get(f"{_API_PREFIX}/access/users")
    async def users_list() -> dict[str, Any]:
        return wrap(list((mock_state.section("access") or {}).get("users", [])))

    @app.post(f"{_API_PREFIX}/access/users")
    async def users_create(request: Request) -> dict[str, Any]:
        body = await _read_body(request)
        if not body.get("userid"):
            raise HTTPException(status_code=400, detail="userid is required")
        access = dict(mock_state.section("access") or {})
        users = list(access.get("users", []))
        users.append(body)
        access["users"] = users
        mock_state.write("access", access)
        return wrap(None)

    @app.get(f"{_API_PREFIX}/access/users/{{userid}}")
    async def users_get(userid: str) -> dict[str, Any]:
        for u in (mock_state.section("access") or {}).get("users", []):
            if u.get("userid") == userid:
                return wrap(u)
        raise HTTPException(status_code=404, detail=f"user '{userid}' not found")

    @app.put(f"{_API_PREFIX}/access/users/{{userid}}")
    async def users_update(userid: str, request: Request) -> dict[str, Any]:
        body = await _read_body(request)
        access = dict(mock_state.section("access") or {})
        users = list(access.get("users", []))
        for i, u in enumerate(users):
            if u.get("userid") == userid:
                users[i] = {**u, **body, "userid": userid}
                access["users"] = users
                mock_state.write("access", access)
                return wrap(None)
        raise HTTPException(status_code=404, detail=f"user '{userid}' not found")

    @app.delete(f"{_API_PREFIX}/access/users/{{userid}}")
    async def users_delete(userid: str) -> dict[str, Any]:
        access = dict(mock_state.section("access") or {})
        users = [u for u in access.get("users", []) if u.get("userid") != userid]
        access["users"] = users
        mock_state.write("access", access)
        return wrap(None)

    @app.get(f"{_API_PREFIX}/access/acl")
    async def acl_list() -> dict[str, Any]:
        return wrap(list((mock_state.section("access") or {}).get("acl", [])))

    @app.put(f"{_API_PREFIX}/access/acl")
    async def acl_update(request: Request) -> dict[str, Any]:
        body = await _read_body(request)
        path = body.get("path")
        roles = body.get("roles")
        ugid = body.get("users") or body.get("groups")
        if not path or not roles or not ugid:
            raise HTTPException(status_code=400, detail="path, roles, users|groups are required")
        access = dict(mock_state.section("access") or {})
        acl = list(access.get("acl", []))
        if body.get("delete"):
            acl = [
                a
                for a in acl
                if not (
                    a.get("path") == path and a.get("roleid") == roles and a.get("ugid") == ugid
                )
            ]
        else:
            acl.append(
                {
                    "path": path,
                    "type": "user" if body.get("users") else "group",
                    "ugid": ugid,
                    "roleid": roles,
                    "propagate": body.get("propagate", True),
                }
            )
        access["acl"] = acl
        mock_state.write("access", access)
        return wrap(None)

    @app.get(f"{_API_PREFIX}/access/tfa/{{userid}}")
    async def tfa_list(userid: str) -> dict[str, Any]:
        tfa = (mock_state.section("access") or {}).get("tfa", {})
        return wrap(list(tfa.get(userid, [])))

    @app.post(f"{_API_PREFIX}/access/tfa/{{userid}}")
    async def tfa_add(userid: str, request: Request) -> dict[str, Any]:
        body = await _read_body(request)
        access = dict(mock_state.section("access") or {})
        tfa = dict(access.get("tfa", {}))
        user_factors = list(tfa.get(userid, []))
        new_factor = {
            "id": f"factor-{len(user_factors) + 1}",
            "type": body.get("type", "totp"),
            "description": body.get("description"),
            "enable": True,
        }
        user_factors.append(new_factor)
        tfa[userid] = user_factors
        access["tfa"] = tfa
        mock_state.write("access", access)
        return wrap(new_factor)

    @app.delete(f"{_API_PREFIX}/access/tfa/{{userid}}/{{tfa_id}}")
    async def tfa_delete(userid: str, tfa_id: str) -> dict[str, Any]:
        access = dict(mock_state.section("access") or {})
        tfa = dict(access.get("tfa", {}))
        user_factors = [f for f in tfa.get(userid, []) if f.get("id") != tfa_id]
        tfa[userid] = user_factors
        access["tfa"] = tfa
        mock_state.write("access", access)
        return wrap(None)

    @app.get(f"{_API_PREFIX}/access/users/{{userid}}/token")
    async def tokens_list(userid: str) -> dict[str, Any]:
        tokens = (mock_state.section("access") or {}).get("tokens", {})
        return wrap(list(tokens.get(userid, [])))

    @app.post(f"{_API_PREFIX}/access/users/{{userid}}/token/{{tokenid}}")
    async def tokens_create(userid: str, tokenid: str, request: Request) -> dict[str, Any]:
        body = await _read_body(request)
        access = dict(mock_state.section("access") or {})
        tokens = dict(access.get("tokens", {}))
        user_tokens = list(tokens.get(userid, []))
        user_tokens.append({"tokenid": tokenid, **body})
        tokens[userid] = user_tokens
        access["tokens"] = tokens
        mock_state.write("access", access)
        return wrap({"tokenid": tokenid, "value": "mock-secret-uuid"})

    @app.put(f"{_API_PREFIX}/access/users/{{userid}}/token/{{tokenid}}")
    async def tokens_update(userid: str, tokenid: str, request: Request) -> dict[str, Any]:
        body = await _read_body(request)
        access = dict(mock_state.section("access") or {})
        tokens = dict(access.get("tokens", {}))
        user_tokens = list(tokens.get(userid, []))
        for i, t in enumerate(user_tokens):
            if t.get("tokenid") == tokenid:
                user_tokens[i] = {**t, **body}
                tokens[userid] = user_tokens
                access["tokens"] = tokens
                mock_state.write("access", access)
                return wrap(None)
        raise HTTPException(status_code=404, detail=f"token '{tokenid}' not found")

    @app.delete(f"{_API_PREFIX}/access/users/{{userid}}/token/{{tokenid}}")
    async def tokens_delete(userid: str, tokenid: str) -> dict[str, Any]:
        access = dict(mock_state.section("access") or {})
        tokens = dict(access.get("tokens", {}))
        user_tokens = [t for t in tokens.get(userid, []) if t.get("tokenid") != tokenid]
        tokens[userid] = user_tokens
        access["tokens"] = tokens
        mock_state.write("access", access)
        return wrap(None)

    # -- /mock/* management endpoints -----------------------------------

    @app.post("/mock/seed")
    async def mock_seed(request: Request) -> dict[str, str]:
        """Replace the entire state with the JSON body."""
        body = await _read_body(request)
        mock_state.replace(body)
        return {"status": "ok"}

    @app.get("/mock/export")
    async def mock_export() -> dict[str, Any]:
        """Dump current in-memory state."""
        return mock_state.snapshot()

    @app.post("/mock/import")
    async def mock_import(request: Request) -> dict[str, str]:
        """Identical to /mock/seed but kept distinct per the issue spec."""
        body = await _read_body(request)
        mock_state.replace(body)
        return {"status": "ok"}

    @app.delete("/mock/reset")
    async def mock_reset() -> dict[str, str]:
        """Reset state to the bundled default seed."""
        mock_state.reset()
        return {"status": "ok"}

    return mock_state


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


async def _read_body(request: Request) -> dict[str, Any]:
    """Tolerantly read a JSON body, or a form body, or return {}."""
    raw = await request.body()
    if not raw:
        return {}
    try:
        decoded = json.loads(raw)
        if isinstance(decoded, dict):
            return decoded
    except json.JSONDecodeError:
        pass
    # Form-encoded fallback (Proxmox CLI clients sometimes send form bodies).
    try:
        form = await request.form()
        return {k: form[k] for k in form}
    except Exception:
        return {}


def _synthetic_rrd() -> list[dict[str, Any]]:
    """Return a small RRD-like sample series."""
    return [
        {"time": 1_700_000_000 + 60 * i, "cpu": 0.1 + 0.01 * i, "mem": 1.0e9 + 5.0e6 * i}
        for i in range(10)
    ]


def load_seed_from_file(path: str | Path) -> dict[str, Any]:
    """Load a seed JSON file from disk; raise if missing or malformed."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"PDM mock seed file not found: {p}")
    return json.loads(p.read_text())

from __future__ import annotations

from proxmox_sdk.mock.state import SQLiteMockStore


def test_sqlite_store_object_lifecycle(tmp_path) -> None:
    store = SQLiteMockStore(owner_pid=123, namespace="sqlite-unit", path=tmp_path / "state.db")
    try:
        assert store.touch_schema("schema-a") is True
        assert store.touch_schema("schema-a") is False

        stored = store.set_object("/api2/json/nodes/pve1", {"node": "pve1"})
        assert stored == {"node": "pve1"}
        assert store.get_object("/api2/json/nodes/pve1") == {"node": "pve1"}

        store.delete_object("/api2/json/nodes/pve1")
        assert store.get_object("/api2/json/nodes/pve1") is None
        assert store.is_deleted("/api2/json/nodes/pve1") is True

        store.set_object("/api2/json/nodes/pve1", {"node": "pve1"})
        assert store.is_deleted("/api2/json/nodes/pve1") is False
    finally:
        store.close(unlink=True)


def test_sqlite_store_collection_lifecycle(tmp_path) -> None:
    store = SQLiteMockStore(owner_pid=123, namespace="sqlite-unit", path=tmp_path / "state.db")
    try:
        store.touch_schema("schema-a")
        assert store.get_collection("/api2/json/access/users") is None

        store.replace_collection("/api2/json/access/users", [{"userid": "root@pam"}])
        assert store.get_collection("/api2/json/access/users") == [{"userid": "root@pam"}]

        members = store.upsert_collection_member(
            "/api2/json/access/users",
            "/api2/json/access/users/test@pve",
            {"userid": "test@pve"},
        )
        assert members == [{"userid": "root@pam"}, {"userid": "test@pve"}]

        members = store.delete_collection_member(
            "/api2/json/access/users",
            "/api2/json/access/users/test@pve",
        )
        assert members == [{"userid": "root@pam"}]
        assert store.is_deleted("/api2/json/access/users/test@pve") is True

        store.replace_collection("/api2/json/access/users", [])
        assert store.get_collection("/api2/json/access/users") == []
    finally:
        store.close(unlink=True)


def test_sqlite_store_schema_change_resets_state(tmp_path) -> None:
    store = SQLiteMockStore(owner_pid=123, namespace="sqlite-unit", path=tmp_path / "state.db")
    try:
        store.touch_schema("schema-a")
        store.set_object("/api2/json/version", {"version": "9.2"})
        assert store.get_object("/api2/json/version") == {"version": "9.2"}

        assert store.touch_schema("schema-b") is True
        assert store.get_object("/api2/json/version") is None
    finally:
        store.close(unlink=True)

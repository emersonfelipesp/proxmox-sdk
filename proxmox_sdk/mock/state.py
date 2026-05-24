"""Shared in-memory state for the generated Proxmox mock API."""

from __future__ import annotations

import atexit
import hashlib
import json
import os
import sqlite3
import tempfile
import threading
from contextlib import contextmanager
from copy import deepcopy
from multiprocessing import shared_memory
from pathlib import Path
from typing import Any, Iterator, Protocol

from proxmox_sdk.logger import logger

try:
    import fcntl
except ImportError:  # pragma: no cover - non-Unix fallback
    fcntl = None

try:
    import orjson
except ImportError:  # pragma: no cover - fallback for source installs
    orjson = None

_DEFAULT_STATE_BYTES = 8 * 1024 * 1024
_STATE_HEADER_BYTES = 8
_STATE_CACHE_LOCK = threading.RLock()
_STATE_CLIENTS: dict[str, "MockStateStore"] = {}

# Module-level dict store for DictMockStore instances.  Keyed by
# "{namespace}:{schema_fingerprint}" so multiple processes (or same-process
# calls with different fingerprints) each get their own fresh bucket while
# calls within the same process sharing a fingerprint reuse state.
_DICT_STATE_STORE: dict[str, dict[str, Any]] = {}


class MockStateStore(Protocol):
    """Protocol shared by all mock-state backend implementations."""

    owner_pid: int
    namespace: str

    def touch_schema(self, schema_fingerprint: str) -> bool: ...

    def reset(self) -> None: ...

    def get_object(self, key: str) -> Any | None: ...

    def set_object(self, key: str, value: Any) -> Any: ...

    def delete_object(self, key: str) -> None: ...

    def is_deleted(self, key: str) -> bool: ...

    def get_collection(self, key: str) -> list[Any] | None: ...

    def replace_collection(self, key: str, values: list[Any]) -> list[Any]: ...

    def upsert_collection_member(self, key: str, member_key: str, value: Any) -> list[Any]: ...

    def delete_collection_member(self, key: str, member_key: str) -> list[Any]: ...

    def close(self, *, unlink: bool = False) -> None: ...


def _json_loads_bytes(payload: bytes) -> Any:
    if orjson is not None:
        return orjson.loads(payload)
    return json.loads(payload.decode("utf-8"))


def _json_dumps_bytes(value: Any, *, sort_keys: bool = False) -> bytes:
    if orjson is not None:
        option = orjson.OPT_SORT_KEYS if sort_keys else 0
        return orjson.dumps(value, option=option)
    return json.dumps(value, sort_keys=sort_keys, separators=(",", ":")).encode("utf-8")


def _process_exists(pid: int) -> bool:
    """Return whether the process with the given PID is still running."""
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    return True


def mock_state_owner_pid() -> int:
    """Return the long-lived owner pid used to scope reload-safe state."""

    try:
        from multiprocessing import parent_process

        parent = parent_process()
    except Exception:  # pragma: no cover - defensive import
        parent = None
    if parent is not None and parent.pid is not None:
        return parent.pid
    return os.getpid()


def _resolved_namespace(namespace: str | None) -> str:
    """Resolve the active shared-state namespace."""
    return namespace or os.environ.get("PROXMOX_MOCK_STATE_NAMESPACE", "default")


def _namespace_digest(namespace: str) -> str:
    """Return a stable digest for a namespace name."""
    return hashlib.sha256(namespace.encode("utf-8")).hexdigest()[:8]


def _state_basename(owner_pid: int, namespace: str) -> str:
    """Build the shared-memory base name for a namespace and owner PID."""
    return f"pmxmock_{_namespace_digest(namespace)}_{owner_pid}"


def _meta_path(owner_pid: int, namespace: str) -> Path:
    """Return the metadata file path for a shared mock state store."""
    return Path(tempfile.gettempdir()) / f"{_state_basename(owner_pid, namespace)}.meta"


def _lock_path(owner_pid: int, namespace: str) -> Path:
    """Return the lock file path for a shared mock state store."""
    return Path(tempfile.gettempdir()) / f"{_state_basename(owner_pid, namespace)}.lock"


@contextmanager
def _locked_file(path: Path, *, exclusive: bool = True) -> Iterator[None]:
    """Acquire an interprocess lock for a filesystem-backed state file.

    Uses LOCK_SH (shared) for read-only access so concurrent readers do not
    block each other, and LOCK_EX (exclusive) only for writes.
    """
    path.touch(exist_ok=True)
    with path.open("r+", encoding="utf-8") as handle:
        if fcntl is not None:
            lock_type = fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH
            fcntl.flock(handle.fileno(), lock_type)
        try:
            yield
        finally:
            if fcntl is not None:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class SharedMemoryMockStore:
    """JSON-backed state stored in a named shared-memory segment."""

    def __init__(
        self,
        *,
        owner_pid: int,
        namespace: str,
        shm: shared_memory.SharedMemory,
        state_bytes: int,
    ) -> None:
        """Initialize the shared-memory mock store."""
        self.owner_pid = owner_pid
        self.namespace = namespace
        self._shm = shm
        self._state_bytes = state_bytes
        self._lock_path = _lock_path(owner_pid, namespace)
        self._meta_path = _meta_path(owner_pid, namespace)

    def touch_schema(self, schema_fingerprint: str) -> bool:
        """Reset state when the schema fingerprint changes."""
        with self._locked_state() as state:
            if state["schema_fingerprint"] == schema_fingerprint:
                return False
            state["schema_fingerprint"] = schema_fingerprint
            state["objects"] = {}
            state["collections"] = {}
            state["deleted"] = []
            return True

    def reset(self) -> None:
        """Reset stored objects, collections, and tombstones."""
        with self._locked_state() as state:
            state["objects"] = {}
            state["collections"] = {}
            state["deleted"] = []

    def get_object(self, key: str) -> Any | None:
        """Return a deep copy of a stored object by key."""
        with self._locked_state(write=False) as state:
            value = state["objects"].get(key)
            return deepcopy(value)

    def set_object(self, key: str, value: Any) -> Any:
        """Store an object value and return the persisted copy."""
        with self._locked_state() as state:
            state["objects"][key] = deepcopy(value)
            state["deleted"].discard(key)
            return deepcopy(value)

    def delete_object(self, key: str) -> None:
        """Delete an object and mark it as removed."""
        with self._locked_state() as state:
            state["objects"].pop(key, None)
            state["deleted"].add(key)

    def is_deleted(self, key: str) -> bool:
        """Return whether a key has been marked as deleted."""
        with self._locked_state(write=False) as state:
            return key in state["deleted"]

    def get_collection(self, key: str) -> list[Any] | None:
        """Return a list copy of a stored collection."""
        with self._locked_state(write=False) as state:
            members = state["collections"].get(key)
            if members is None:
                return None
            return [deepcopy(value) for value in members.values()]

    def replace_collection(self, key: str, values: list[Any]) -> list[Any]:
        """Replace a collection with the provided values."""
        with self._locked_state() as state:
            state["collections"][key] = {
                f"seed:{index}": deepcopy(value) for index, value in enumerate(values)
            }
            return [deepcopy(v) for v in values]

    def upsert_collection_member(self, key: str, member_key: str, value: Any) -> list[Any]:
        """Insert or replace a member in a stored collection."""
        with self._locked_state() as state:
            members = state["collections"].setdefault(key, {})
            members[member_key] = deepcopy(value)
            state["deleted"].discard(member_key)
            return [deepcopy(item) for item in members.values()]

    def delete_collection_member(self, key: str, member_key: str) -> list[Any]:
        """Remove a member from a stored collection."""
        with self._locked_state() as state:
            members = state["collections"].setdefault(key, {})
            members.pop(member_key, None)
            state["deleted"].add(member_key)
            return [deepcopy(item) for item in members.values()]

    @contextmanager
    def _locked_state(self, *, write: bool = True) -> Iterator[dict[str, Any]]:
        """Load the current state under a filesystem lock and optionally persist it.

        Read-only callers (write=False) acquire a shared lock so concurrent GETs
        do not block each other.  Write callers always use an exclusive lock.
        """
        with _locked_file(self._lock_path, exclusive=write):
            state = self._read_state()
            # Materialise 'deleted' as a set for O(1) membership checks at runtime.
            state["deleted"] = set(state["deleted"])
            yield state
            if write:
                # Serialise back to list for JSON compatibility.
                state["deleted"] = list(state["deleted"])
                self._write_state(state)

    def _read_state(self) -> dict[str, Any]:
        """Deserialize the shared-memory payload into a normalized state mapping."""
        try:
            length = int.from_bytes(self._shm.buf[:_STATE_HEADER_BYTES], "big")
        except (TypeError, ValueError):
            return self._default_state()

        max_bytes = self._state_bytes - _STATE_HEADER_BYTES
        if length <= 0 or length > max_bytes:
            return self._default_state()

        try:
            payload = bytes(self._shm.buf[_STATE_HEADER_BYTES : _STATE_HEADER_BYTES + length])
            state = _json_loads_bytes(payload)
        except (UnicodeDecodeError, json.JSONDecodeError, ValueError, TypeError):
            return self._default_state()

        return self._normalize_state(state)

    def _write_state(self, state: dict[str, Any]) -> None:
        """Serialize the state mapping back into shared memory."""
        payload = _json_dumps_bytes(state, sort_keys=True)
        max_bytes = self._state_bytes - _STATE_HEADER_BYTES
        if len(payload) > max_bytes:
            raise RuntimeError(
                f"Shared mock state exceeded the allocated {max_bytes} byte capacity."
            )
        self._shm.buf[:_STATE_HEADER_BYTES] = len(payload).to_bytes(_STATE_HEADER_BYTES, "big")
        self._shm.buf[_STATE_HEADER_BYTES : _STATE_HEADER_BYTES + len(payload)] = payload

    def close(self, *, unlink: bool = False) -> None:
        """Close the shared-memory segment and optionally unlink its metadata."""
        try:
            self._shm.close()
        except FileNotFoundError:  # pragma: no cover - defensive cleanup
            return
        if unlink:
            try:
                self._shm.unlink()
            except FileNotFoundError:
                pass
            self._meta_path.unlink(missing_ok=True)
            self._lock_path.unlink(missing_ok=True)

    @staticmethod
    def _default_state() -> dict[str, Any]:
        """Return the default shared mock state structure."""
        return {
            "schema_fingerprint": "",
            "objects": {},
            "collections": {},
            "deleted": [],
        }

    @classmethod
    def _normalize_state(cls, state: Any) -> dict[str, Any]:
        """Coerce loaded state into the expected mapping shape."""
        default_state = cls._default_state()
        if not isinstance(state, dict):
            return default_state

        normalized = default_state.copy()
        schema_fingerprint = state.get("schema_fingerprint")
        if isinstance(schema_fingerprint, str):
            normalized["schema_fingerprint"] = schema_fingerprint

        objects = state.get("objects")
        if isinstance(objects, dict):
            normalized["objects"] = objects

        collections = state.get("collections")
        if isinstance(collections, dict):
            normalized["collections"] = collections

        deleted = state.get("deleted")
        if isinstance(deleted, list):
            normalized["deleted"] = deleted

        return normalized


class DictMockStore:
    """Pure-dict fallback store used when POSIX shared memory is unavailable.

    Suitable for environments such as Vercel serverless where
    ``multiprocessing.shared_memory`` raises ``OSError`` at creation time.
    State is held in the module-level ``_DICT_STATE_STORE`` dict so that
    multiple calls within the same process with the same namespace and schema
    fingerprint share a single bucket.
    """

    def __init__(self, *, owner_pid: int, namespace: str) -> None:
        """Initialize the dict-backed mock store."""
        self.owner_pid = owner_pid
        self.namespace = namespace
        self._current_key: str | None = None

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _state(self) -> dict[str, Any]:
        """Return the current state bucket (only valid after touch_schema)."""
        if self._current_key is None:
            raise RuntimeError("DictMockStore: touch_schema() has not been called yet.")
        return _DICT_STATE_STORE[self._current_key]

    # ------------------------------------------------------------------
    # Public interface (mirrors SharedMemoryMockStore)
    # ------------------------------------------------------------------

    def touch_schema(self, schema_fingerprint: str) -> bool:
        """Reset state when the schema fingerprint changes.

        Returns True if this is the first call for this fingerprint (fresh
        state), False if the fingerprint matches an existing bucket.
        """
        key = f"{self.namespace}:{schema_fingerprint}"
        self._current_key = key
        if key in _DICT_STATE_STORE:
            return False
        _DICT_STATE_STORE[key] = {
            "objects": {},
            "collections": {},
            "deleted": set(),
        }
        return True

    def reset(self) -> None:
        """Clear all stored objects, collections, and tombstones."""
        state = self._state()
        state["objects"] = {}
        state["collections"] = {}
        state["deleted"] = set()

    def get_object(self, key: str) -> Any | None:
        """Return a deep copy of a stored object by key."""
        return deepcopy(self._state()["objects"].get(key))

    def set_object(self, key: str, value: Any) -> Any:
        """Store an object value and return the persisted copy."""
        state = self._state()
        state["objects"][key] = deepcopy(value)
        state["deleted"].discard(key)
        return deepcopy(value)

    def delete_object(self, key: str) -> None:
        """Delete an object and mark it as removed."""
        state = self._state()
        state["objects"].pop(key, None)
        state["deleted"].add(key)

    def is_deleted(self, key: str) -> bool:
        """Return whether a key has been marked as deleted."""
        return key in self._state()["deleted"]

    def get_collection(self, key: str) -> list[Any] | None:
        """Return a list copy of a stored collection, or None if absent."""
        members = self._state()["collections"].get(key)
        if members is None:
            return None
        return [deepcopy(v) for v in members.values()]

    def replace_collection(self, key: str, values: list[Any]) -> list[Any]:
        """Replace a collection with the provided values."""
        self._state()["collections"][key] = {
            f"seed:{index}": deepcopy(value) for index, value in enumerate(values)
        }
        return [deepcopy(v) for v in values]

    def upsert_collection_member(self, key: str, member_key: str, value: Any) -> list[Any]:
        """Insert or replace a member in a stored collection."""
        state = self._state()
        members = state["collections"].setdefault(key, {})
        members[member_key] = deepcopy(value)
        state["deleted"].discard(member_key)
        return [deepcopy(item) for item in members.values()]

    def delete_collection_member(self, key: str, member_key: str) -> list[Any]:
        """Remove a member from a stored collection."""
        state = self._state()
        members = state["collections"].setdefault(key, {})
        members.pop(member_key, None)
        state["deleted"].add(member_key)
        return [deepcopy(item) for item in members.values()]

    def close(self, *, unlink: bool = False) -> None:  # noqa: ARG002
        """No-op — dict state needs no cleanup."""


class SQLiteMockStore:
    """SQLite/WAL mock store that persists each object and collection member separately."""

    def __init__(self, *, owner_pid: int, namespace: str, path: Path) -> None:
        """Initialize the SQLite-backed mock store."""
        self.owner_pid = owner_pid
        self.namespace = namespace
        self.path = path
        self._lock = threading.RLock()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._conn = sqlite3.connect(
            self.path,
            timeout=30.0,
            isolation_level=None,
            check_same_thread=False,
        )
        self._conn.execute("PRAGMA journal_mode=WAL")
        self._conn.execute("PRAGMA synchronous=NORMAL")
        self._conn.execute("PRAGMA busy_timeout=30000")
        self._init_schema()

    def _init_schema(self) -> None:
        with self._lock:
            self._conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS objects (
                    key TEXT PRIMARY KEY,
                    value BLOB NOT NULL
                );
                CREATE TABLE IF NOT EXISTS collections (
                    collection_key TEXT NOT NULL,
                    member_key TEXT NOT NULL,
                    position INTEGER NOT NULL,
                    value BLOB NOT NULL,
                    PRIMARY KEY (collection_key, member_key)
                );
                CREATE TABLE IF NOT EXISTS deleted (
                    key TEXT PRIMARY KEY
                );
                CREATE INDEX IF NOT EXISTS idx_collections_order
                    ON collections (collection_key, position, member_key);
                """
            )

    def touch_schema(self, schema_fingerprint: str) -> bool:
        """Reset state when the schema fingerprint changes."""
        with self._lock, self._conn:
            row = self._conn.execute(
                "SELECT value FROM metadata WHERE key = 'schema_fingerprint'"
            ).fetchone()
            if row is not None and row[0] == schema_fingerprint:
                return False
            self._conn.execute("DELETE FROM objects")
            self._conn.execute("DELETE FROM collections")
            self._conn.execute("DELETE FROM deleted")
            self._conn.execute(
                "INSERT OR REPLACE INTO metadata (key, value) VALUES ('schema_fingerprint', ?)",
                (schema_fingerprint,),
            )
            return True

    def reset(self) -> None:
        """Reset stored objects, collections, and tombstones."""
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM objects")
            self._conn.execute("DELETE FROM collections")
            self._conn.execute("DELETE FROM deleted")

    def get_object(self, key: str) -> Any | None:
        """Return a stored object by key."""
        with self._lock:
            row = self._conn.execute("SELECT value FROM objects WHERE key = ?", (key,)).fetchone()
            if row is None:
                return None
            return deepcopy(_json_loads_bytes(row[0]))

    def set_object(self, key: str, value: Any) -> Any:
        """Store an object value and return the persisted copy."""
        payload = _json_dumps_bytes(value, sort_keys=True)
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT OR REPLACE INTO objects (key, value) VALUES (?, ?)",
                (key, payload),
            )
            self._conn.execute("DELETE FROM deleted WHERE key = ?", (key,))
        return deepcopy(value)

    def delete_object(self, key: str) -> None:
        """Delete an object and mark it as removed."""
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM objects WHERE key = ?", (key,))
            self._conn.execute("INSERT OR IGNORE INTO deleted (key) VALUES (?)", (key,))

    def is_deleted(self, key: str) -> bool:
        """Return whether a key has been marked as deleted."""
        with self._lock:
            row = self._conn.execute("SELECT 1 FROM deleted WHERE key = ?", (key,)).fetchone()
            return row is not None

    def get_collection(self, key: str) -> list[Any] | None:
        """Return a stored collection by key."""
        with self._lock:
            rows = self._conn.execute(
                """
                SELECT value FROM collections
                WHERE collection_key = ?
                ORDER BY position, member_key
                """,
                (key,),
            ).fetchall()
            if not rows:
                marker = self._conn.execute(
                    "SELECT 1 FROM metadata WHERE key = ?",
                    (f"collection:{key}",),
                ).fetchone()
                return [] if marker is not None else None
            return [deepcopy(_json_loads_bytes(row[0])) for row in rows]

    def replace_collection(self, key: str, values: list[Any]) -> list[Any]:
        """Replace a collection with the provided values."""
        with self._lock, self._conn:
            self._conn.execute("DELETE FROM collections WHERE collection_key = ?", (key,))
            self._conn.execute(
                "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, '1')",
                (f"collection:{key}",),
            )
            self._conn.executemany(
                """
                INSERT INTO collections (collection_key, member_key, position, value)
                VALUES (?, ?, ?, ?)
                """,
                [
                    (key, f"seed:{index}", index, _json_dumps_bytes(value, sort_keys=True))
                    for index, value in enumerate(values)
                ],
            )
        return [deepcopy(v) for v in values]

    def upsert_collection_member(self, key: str, member_key: str, value: Any) -> list[Any]:
        """Insert or replace a member in a stored collection."""
        payload = _json_dumps_bytes(value, sort_keys=True)
        with self._lock, self._conn:
            self._conn.execute(
                "INSERT OR REPLACE INTO metadata (key, value) VALUES (?, '1')",
                (f"collection:{key}",),
            )
            existing = self._conn.execute(
                """
                SELECT position FROM collections
                WHERE collection_key = ? AND member_key = ?
                """,
                (key, member_key),
            ).fetchone()
            if existing is None:
                max_position = self._conn.execute(
                    "SELECT COALESCE(MAX(position), -1) FROM collections WHERE collection_key = ?",
                    (key,),
                ).fetchone()[0]
                position = int(max_position) + 1
            else:
                position = int(existing[0])
            self._conn.execute(
                """
                INSERT OR REPLACE INTO collections
                    (collection_key, member_key, position, value)
                VALUES (?, ?, ?, ?)
                """,
                (key, member_key, position, payload),
            )
            self._conn.execute("DELETE FROM deleted WHERE key = ?", (member_key,))
        return self.get_collection(key) or []

    def delete_collection_member(self, key: str, member_key: str) -> list[Any]:
        """Remove a member from a stored collection."""
        with self._lock, self._conn:
            self._conn.execute(
                "DELETE FROM collections WHERE collection_key = ? AND member_key = ?",
                (key, member_key),
            )
            self._conn.execute("INSERT OR IGNORE INTO deleted (key) VALUES (?)", (member_key,))
        return self.get_collection(key) or []

    def close(self, *, unlink: bool = False) -> None:
        """Close the SQLite connection and optionally remove database files."""
        with self._lock:
            self._conn.close()
        if unlink:
            self.path.unlink(missing_ok=True)
            self.path.with_suffix(self.path.suffix + "-wal").unlink(missing_ok=True)
            self.path.with_suffix(self.path.suffix + "-shm").unlink(missing_ok=True)


def _cleanup_stale_states(namespace: str, owner_pid: int) -> None:
    """Remove stale shared-memory segments for a namespace."""
    digest = _namespace_digest(namespace)
    temp_root = Path(tempfile.gettempdir())
    for meta_file in temp_root.glob(f"pmxmock_{digest}_*.meta"):
        try:
            stale_owner = int(meta_file.stem.rsplit("_", 1)[-1])
        except ValueError:
            continue
        if stale_owner == owner_pid or _process_exists(stale_owner):
            continue

        shm_name = meta_file.read_text(encoding="utf-8").strip() or meta_file.stem
        try:
            stale_segment = shared_memory.SharedMemory(name=shm_name, create=False)
        except FileNotFoundError:
            stale_segment = None
        if stale_segment is not None:
            try:
                stale_segment.close()
            finally:
                try:
                    stale_segment.unlink()
                except FileNotFoundError:
                    pass
        meta_file.unlink(missing_ok=True)
        _lock_path(stale_owner, namespace).unlink(missing_ok=True)


def _create_or_attach_store(owner_pid: int, namespace: str) -> SharedMemoryMockStore:
    """Create a new shared-memory store or attach to an existing one."""
    state_bytes = int(os.environ.get("PROXMOX_MOCK_STATE_BYTES", str(_DEFAULT_STATE_BYTES)))
    basename = _state_basename(owner_pid, namespace)
    meta_file = _meta_path(owner_pid, namespace)

    with _locked_file(_lock_path(owner_pid, namespace)):
        try:
            shm = shared_memory.SharedMemory(name=basename, create=False)
        except FileNotFoundError:
            shm = shared_memory.SharedMemory(name=basename, create=True, size=state_bytes)
            shm.buf[:_STATE_HEADER_BYTES] = (0).to_bytes(_STATE_HEADER_BYTES, "big")
            meta_file.write_text(basename, encoding="utf-8")
            logger.info(
                "Created reload-safe Proxmox mock shared state",
                extra={
                    "namespace": namespace,
                    "owner_pid": owner_pid,
                    "state_name": basename,
                },
            )
        else:
            meta_file.write_text(basename, encoding="utf-8")

    return SharedMemoryMockStore(
        owner_pid=owner_pid,
        namespace=namespace,
        shm=shm,
        state_bytes=state_bytes,
    )


def _attach_existing_store(owner_pid: int, namespace: str) -> SharedMemoryMockStore:
    """Attach to an already-created shared-memory store."""
    state_bytes = int(os.environ.get("PROXMOX_MOCK_STATE_BYTES", str(_DEFAULT_STATE_BYTES)))
    basename = _state_basename(owner_pid, namespace)
    shm = shared_memory.SharedMemory(name=basename, create=False)
    return SharedMemoryMockStore(
        owner_pid=owner_pid,
        namespace=namespace,
        shm=shm,
        state_bytes=state_bytes,
    )


def _mock_store_backend() -> str:
    value = os.environ.get("PROXMOX_MOCK_STORE", "sqlite").strip().lower()
    aliases = {
        "shared_memory": "shared-memory",
        "shm": "shared-memory",
        "memory": "shared-memory",
    }
    return aliases.get(value, value)


def _sqlite_state_path(owner_pid: int, namespace: str) -> Path:
    configured = os.environ.get("PROXMOX_MOCK_STATE_PATH")
    if configured:
        return Path(configured)
    return Path(tempfile.gettempdir()) / f"{_state_basename(owner_pid, namespace)}.sqlite3"


def shared_mock_store(
    schema_fingerprint: str,
    *,
    namespace: str | None = None,
    owner_pid: int | None = None,
) -> MockStateStore:
    """Return a reload-safe shared state store for generated mock responses.

    SQLite/WAL is the default backend.  Legacy shared-memory and dict stores
    remain available through ``PROXMOX_MOCK_STORE``.
    """

    resolved_owner = owner_pid or mock_state_owner_pid()
    resolved_namespace = _resolved_namespace(namespace)
    backend = _mock_store_backend()
    sqlite_path = _sqlite_state_path(resolved_owner, resolved_namespace)
    cache_key = f"{backend}:{resolved_namespace}:{resolved_owner}:{sqlite_path}"

    with _STATE_CACHE_LOCK:
        cached = _STATE_CLIENTS.get(cache_key)
        if cached is None:
            if backend == "sqlite":
                cached = SQLiteMockStore(
                    owner_pid=resolved_owner,
                    namespace=resolved_namespace,
                    path=sqlite_path,
                )
            elif backend == "dict":
                cached = DictMockStore(
                    owner_pid=resolved_owner,
                    namespace=resolved_namespace,
                )
            elif backend == "shared-memory":
                try:
                    _cleanup_stale_states(resolved_namespace, resolved_owner)
                    cached = _create_or_attach_store(resolved_owner, resolved_namespace)
                except (OSError, ImportError):
                    logger.warning(
                        "POSIX shared memory unavailable; falling back to DictMockStore",
                        extra={"namespace": resolved_namespace, "owner_pid": resolved_owner},
                    )
                    cached = DictMockStore(
                        owner_pid=resolved_owner,
                        namespace=resolved_namespace,
                    )
            else:
                raise ValueError("PROXMOX_MOCK_STORE must be one of: sqlite, shared-memory, dict.")
            _STATE_CLIENTS[cache_key] = cached
        cached.touch_schema(schema_fingerprint)
        return cached


def reset_shared_mock_state(*, namespace: str | None = None, owner_pid: int | None = None) -> None:
    """Reset the current live mock state back to the deterministic seed."""

    resolved_owner = owner_pid or mock_state_owner_pid()
    resolved_namespace = _resolved_namespace(namespace)
    backend = _mock_store_backend()
    sqlite_path = _sqlite_state_path(resolved_owner, resolved_namespace)
    cache_key = f"{backend}:{resolved_namespace}:{resolved_owner}:{sqlite_path}"

    with _STATE_CACHE_LOCK:
        cached = _STATE_CLIENTS.get(cache_key)
        if cached is None:
            if backend == "sqlite":
                cached = SQLiteMockStore(
                    owner_pid=resolved_owner,
                    namespace=resolved_namespace,
                    path=sqlite_path,
                )
            elif backend == "dict":
                cached = DictMockStore(
                    owner_pid=resolved_owner,
                    namespace=resolved_namespace,
                )
            else:
                try:
                    cached = _attach_existing_store(resolved_owner, resolved_namespace)
                except FileNotFoundError:
                    return
            _STATE_CLIENTS[cache_key] = cached
        cached.reset()


def _close_cached_stores() -> None:
    """Close cached shared-memory stores during interpreter shutdown."""
    current_pid = os.getpid()
    with _STATE_CACHE_LOCK:
        for store in _STATE_CLIENTS.values():
            store.close(unlink=store.owner_pid == current_pid)


atexit.register(_close_cached_stores)

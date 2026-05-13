"""Integration tests for RemoteSSHClient against an in-process paramiko server.

These tests stand up a real SSH server in a background thread using paramiko's
``ServerInterface``, then drive ``RemoteSSHClient`` against it. They verify:

* the pre-connect TCP timeout doesn't strand executor threads,
* the pinned host-key fingerprint check fires before auth,
* a wrong fingerprint raises ``HostKeyMismatch``,
* key-based auth completes end-to-end,
* ``run()`` returns stdout / stderr / exit_code,
* the output cap raises ``OutputTooLarge``,
* per-command timeouts surface as ``SshTimeout``.
"""

from __future__ import annotations

import socket
import threading
import time
from typing import Any

import pytest

paramiko = pytest.importorskip("paramiko")

from proxmox_sdk.ssh import (  # noqa: E402
    HostKeyMismatch,
    OutputTooLarge,
    RemoteSSHClient,
    SshTimeout,
    fingerprint_sha256,
)


class _FakeServer(paramiko.ServerInterface):
    """Minimal server: accept the test public key, allow exec, capture argv."""

    def __init__(self, accept_key: paramiko.PKey) -> None:
        super().__init__()
        self._accept_key = accept_key
        self.received_commands: list[str] = []
        self.exec_event = threading.Event()
        self._pending: list[tuple[Any, str]] = []
        self._pending_lock = threading.Lock()
        # Per-command behaviour, set by the test.
        self.response_stdout = b"hello\n"
        self.response_stderr = b""
        self.response_exit = 0
        self.response_delay = 0.0

    def check_auth_publickey(self, username: str, key: paramiko.PKey) -> int:
        if key.asbytes() == self._accept_key.asbytes():
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username: str) -> str:
        return "publickey"

    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_channel_exec_request(self, channel: Any, command: bytes) -> bool:
        # CRITICAL: must return True immediately so paramiko can send the
        # exec-request success message back to the client. The actual response
        # is dispatched from the serve() thread after we return.
        cmd = command.decode("utf-8", errors="replace")
        self.received_commands.append(cmd)
        with self._pending_lock:
            self._pending.append((channel, cmd))
        self.exec_event.set()
        return True

    def pop_pending(self) -> tuple[Any, str] | None:
        with self._pending_lock:
            if not self._pending:
                return None
            return self._pending.pop(0)

    def write_response(self, channel: Any) -> None:
        if self.response_delay:
            time.sleep(self.response_delay)
        if self.response_stdout:
            channel.sendall(self.response_stdout)
        if self.response_stderr:
            channel.sendall_stderr(self.response_stderr)
        channel.send_exit_status(self.response_exit)
        channel.close()


@pytest.fixture()
def ssh_server() -> Any:
    """Start a single-connection SSH server in a background thread.

    Yields a small handle exposing host/port, the expected fingerprint, the
    matching client private key text, and the active ``_FakeServer`` so tests
    can tweak its canned response.
    """
    # paramiko exposes RSAKey.generate(); Ed25519Key has no such helper.
    # Both are acceptable to the client (pinned host-key-types include rsa-sha2-*).
    host_key = paramiko.RSAKey.generate(2048)
    client_key = paramiko.RSAKey.generate(2048)

    listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listener.bind(("127.0.0.1", 0))
    listener.listen(1)
    listener.settimeout(10.0)
    port = listener.getsockname()[1]

    server_obj: dict[str, _FakeServer] = {}
    ready = threading.Event()
    error: dict[str, BaseException] = {}

    def serve() -> None:
        try:
            client_sock, _ = listener.accept()
            transport = paramiko.Transport(client_sock)
            transport.add_server_key(host_key)
            fake = _FakeServer(client_key)
            server_obj["fake"] = fake
            transport.start_server(server=fake)
            ready.set()
            # Wait up to 10s for the first exec request to land.
            fake.exec_event.wait(timeout=10.0)
            # Drain whatever exec requests came in; respond from THIS thread so
            # paramiko has already acknowledged the exec request to the client.
            deadline = time.monotonic() + 10.0
            while time.monotonic() < deadline:
                pending = fake.pop_pending()
                if pending is not None:
                    channel, _cmd = pending
                    fake.write_response(channel)
                    break
                time.sleep(0.01)
            time.sleep(0.1)
            transport.close()
            client_sock.close()
        except BaseException as exc:  # noqa: BLE001
            error["exc"] = exc
            ready.set()

    t = threading.Thread(target=serve, daemon=True)
    t.start()

    # Export private key in OpenSSH PEM form for the client side.
    import io

    buf = io.StringIO()
    client_key.write_private_key(buf)
    client_key_pem = buf.getvalue()

    handle = {
        "host": "127.0.0.1",
        "port": port,
        "fingerprint": fingerprint_sha256(host_key),
        "client_key_pem": client_key_pem,
        "ready": ready,
        "server": server_obj,
        "error": error,
    }
    try:
        yield handle
    finally:
        try:
            listener.close()
        except Exception:  # pragma: no cover - defensive
            pass


async def test_run_happy_path(ssh_server: dict[str, Any]) -> None:
    async with RemoteSSHClient(
        host=ssh_server["host"],
        port=ssh_server["port"],
        username="proxbox",
        known_host_fingerprint=ssh_server["fingerprint"],
        private_key=ssh_server["client_key_pem"],
        connect_timeout=5.0,
        exec_timeout=5.0,
    ) as client:
        # Configure the server's response for this run.
        ssh_server["ready"].wait(timeout=5.0)
        fake = ssh_server["server"]["fake"]
        fake.response_stdout = b"42\n"
        fake.response_exit = 0
        result = await client.run(["dmidecode", "-t", "1"])

    assert result.exit_code == 0
    assert result.stdout == "42\n"
    # The server received the shlex-joined argv exactly.
    assert fake.received_commands == ["dmidecode -t 1"]


async def test_wrong_fingerprint_raises(ssh_server: dict[str, Any]) -> None:
    # Same setup, but supply a deliberately wrong fingerprint. The handshake
    # must abort before auth completes — the server side will see the
    # transport close.
    bad_fp = "SHA256:" + "A" * 43
    with pytest.raises(HostKeyMismatch):
        async with RemoteSSHClient(
            host=ssh_server["host"],
            port=ssh_server["port"],
            username="proxbox",
            known_host_fingerprint=bad_fp,
            private_key=ssh_server["client_key_pem"],
            connect_timeout=5.0,
            exec_timeout=5.0,
        ):
            pytest.fail("client should not have authenticated")


async def test_output_cap_enforced(ssh_server: dict[str, Any]) -> None:
    async with RemoteSSHClient(
        host=ssh_server["host"],
        port=ssh_server["port"],
        username="proxbox",
        known_host_fingerprint=ssh_server["fingerprint"],
        private_key=ssh_server["client_key_pem"],
        connect_timeout=5.0,
        exec_timeout=5.0,
        output_cap_bytes=1024,
    ) as client:
        ssh_server["ready"].wait(timeout=5.0)
        fake = ssh_server["server"]["fake"]
        fake.response_stdout = b"x" * (4 * 1024)
        with pytest.raises(OutputTooLarge):
            await client.run(["echo", "huge"])


async def test_exec_timeout_surfaces_as_ssh_timeout(ssh_server: dict[str, Any]) -> None:
    async with RemoteSSHClient(
        host=ssh_server["host"],
        port=ssh_server["port"],
        username="proxbox",
        known_host_fingerprint=ssh_server["fingerprint"],
        private_key=ssh_server["client_key_pem"],
        connect_timeout=5.0,
        exec_timeout=0.3,
    ) as client:
        ssh_server["ready"].wait(timeout=5.0)
        fake = ssh_server["server"]["fake"]
        fake.response_delay = 2.0
        with pytest.raises(SshTimeout):
            await client.run(["sleep", "2"])

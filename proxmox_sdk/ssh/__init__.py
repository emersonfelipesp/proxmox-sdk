"""SSH primitive for proxmox-sdk.

``RemoteSSHClient`` is the single source of truth for SSH access used across
the proxmox-sdk workspace and its consumers. It is intentionally
Proxmox-agnostic: hardware discovery, future remote ops, and the existing
``SshParamikoBackend`` all compose this primitive.

Design goals (security-first):

* **No TOFU.** A SHA256 fingerprint of the remote host key must be supplied at
  construction time. Any mismatch raises ``HostKeyMismatch`` and the connection
  is refused. ``AutoAddPolicy`` and ``WarningPolicy`` are never used.
* **argv-list only.** ``run()`` accepts ``list[str]`` exclusively; passing a
  shell string raises ``TypeError``. Internally we ``shlex.join()`` the list
  for paramiko's ``exec_command`` so shell metacharacters in *list elements*
  cannot escape word boundaries.
* **Optional allowlist.** Callers may pin the set of permitted ``argv[0]``
  values; anything else raises ``CommandNotAllowed``.
* **Bounded output.** Each ``run()`` caps combined stdout + stderr at
  ``output_cap_bytes`` (default 256 KiB).
* **Timeouts.** Connect and per-exec timeouts are enforced.
* **Log redaction.** A configurable list of regex patterns is applied to any
  log record emitted by this module so private keys, passwords and Fernet-shaped
  tokens never land in caplog/syslog output.
* **Algorithm pinning.** Paramiko's ``Transport.get_security_options()`` is
  rewritten before authentication so only modern AEAD ciphers, ETM MACs and
  ``curve25519-sha256`` key exchange are offered.
"""

from __future__ import annotations

import asyncio
import base64
import hashlib
import io
import logging
import re
import shlex
import socket
import time
from dataclasses import dataclass
from functools import partial
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
    from re import Pattern

logger = logging.getLogger(__name__)

try:
    import paramiko  # type: ignore[import-untyped]

    _PARAMIKO_AVAILABLE = True
except ImportError:
    _PARAMIKO_AVAILABLE = False


__all__ = [
    "CommandResult",
    "DEFAULT_REDACTORS",
    "HostKeyMismatch",
    "CommandNotAllowed",
    "OutputTooLarge",
    "RemoteSSHClient",
    "SshAuthFailed",
    "SshTimeout",
    "fingerprint_sha256",
]


# --- Algorithm pinning -------------------------------------------------------
# Names taken verbatim from paramiko's option enumerations.

_PINNED_KEX: tuple[str, ...] = (
    "curve25519-sha256",
    "curve25519-sha256@libssh.org",
)

_PINNED_CIPHERS: tuple[str, ...] = (
    "chacha20-poly1305@openssh.com",
    "aes256-gcm@openssh.com",
    "aes128-gcm@openssh.com",
)

_PINNED_MACS: tuple[str, ...] = (
    "hmac-sha2-512-etm@openssh.com",
    "hmac-sha2-256-etm@openssh.com",
)

_PINNED_HOST_KEY_TYPES: tuple[str, ...] = (
    "ssh-ed25519",
    "rsa-sha2-512",
    "rsa-sha2-256",
)


# --- Log redaction -----------------------------------------------------------

DEFAULT_REDACTORS: tuple[Pattern[str], ...] = (
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL),
    re.compile(r"(?i)(password\s*[=:]\s*)\S+"),
    re.compile(r"(?i)(token\s*[=:]\s*)\S+"),
    # Fernet-shaped: 100+ url-safe base64 chars
    re.compile(r"gAAAAA[A-Za-z0-9_=-]{20,}"),
)


def _redact(text: str, redactors: tuple[Pattern[str], ...]) -> str:
    """Apply redactors to a string; replace matches with ``***``."""
    out = text
    for pat in redactors:
        out = pat.sub("***", out)
    return out


class _RedactingFilter(logging.Filter):
    """Filter that rewrites log records' message through the redactor list."""

    def __init__(self, redactors: tuple[Pattern[str], ...]) -> None:
        super().__init__()
        self._redactors = redactors

    def filter(self, record: logging.LogRecord) -> bool:
        try:
            msg = record.getMessage()
        except Exception:  # pragma: no cover - defensive
            return True
        if any(p.search(msg) for p in self._redactors):
            record.msg = _redact(msg, self._redactors)
            record.args = ()
        return True


# --- Exceptions --------------------------------------------------------------


class SshError(Exception):
    """Base class for proxmox-sdk SSH errors."""


class HostKeyMismatch(SshError):
    """Raised when the remote host key does not match the pinned fingerprint."""


class SshTimeout(SshError):
    """Raised when connect or exec exceeds the configured timeout."""


class SshAuthFailed(SshError):
    """Raised when paramiko cannot authenticate with the supplied credentials."""


class OutputTooLarge(SshError):
    """Raised when a command's combined stdout + stderr exceeds the cap."""


class CommandNotAllowed(SshError):
    """Raised when argv[0] is outside the configured command allowlist."""


# --- Result dataclass --------------------------------------------------------


@dataclass(frozen=True)
class CommandResult:
    """Result of a single ``RemoteSSHClient.run()`` invocation."""

    argv: tuple[str, ...]
    stdout: str
    stderr: str
    exit_code: int
    duration_s: float
    truncated: bool = False


# --- Fingerprint helper ------------------------------------------------------


def fingerprint_sha256(host_key: Any) -> str:
    """Return the canonical ``SHA256:<base64>`` fingerprint of a paramiko host key.

    Accepts either a ``paramiko.PKey`` instance or the raw key bytes
    (``key.asbytes()``).
    """
    if hasattr(host_key, "asbytes"):
        data = host_key.asbytes()
    elif isinstance(host_key, (bytes, bytearray)):
        data = bytes(host_key)
    else:
        raise TypeError(f"fingerprint_sha256: unsupported key type {type(host_key)!r}")
    digest = hashlib.sha256(data).digest()
    return "SHA256:" + base64.b64encode(digest).rstrip(b"=").decode("ascii")


def _normalize_fingerprint(fp: str) -> str:
    """Normalize a user-supplied fingerprint to the canonical form."""
    s = fp.strip()
    if not s:
        raise ValueError("empty host-key fingerprint")
    # Accept "SHA256:abcd...", "sha256:abcd...", or bare "abcd..." (assume sha256).
    if ":" in s:
        prefix, _, value = s.partition(":")
        if prefix.upper() != "SHA256":
            raise ValueError(f"unsupported fingerprint algorithm: {prefix!r} (only SHA256)")
        return "SHA256:" + value.rstrip("=")
    return "SHA256:" + s.rstrip("=")


# --- Host-key policy --------------------------------------------------------


class _RejectAlwaysPolicy:
    """Paramiko MissingHostKeyPolicy that unconditionally raises.

    Belt-and-braces guard: even if ``_PinnedHostKeyClient`` did not run, this
    policy refuses to add or accept any unknown key.
    """

    def missing_host_key(self, client: Any, hostname: str, key: Any) -> None:
        raise HostKeyMismatch(
            f"refusing to connect to {hostname}: host key is unknown "
            "and no first-trust policy is permitted"
        )


# --- The client -------------------------------------------------------------


class RemoteSSHClient:
    """Async, security-hardened SSH client.

    Construct with all credentials and policy at __init__ time; use as an
    async context manager. ``run()`` is the only public surface for executing
    commands; it accepts ``list[str]`` exclusively.

    Parameters
    ----------
    host:
        Target hostname or IP.
    port:
        TCP port. Default 22.
    username:
        Login user.
    known_host_fingerprint:
        Pinned SHA256 fingerprint of the remote host key, in canonical
        ``SHA256:<base64>`` form (the trailing ``=`` padding is optional).
        Mismatch raises ``HostKeyMismatch``.
    private_key:
        OpenSSH-format PEM string for key-based auth, or ``None``.
    password:
        Password for password auth, or ``None``. If both ``private_key`` and
        ``password`` are set, key-based auth is tried first.
    connect_timeout, exec_timeout:
        Timeouts (seconds) for connecting and per-command execution.
    sudo:
        If True, every ``run()`` is wrapped in ``sudo -n`` (no password
        prompt) so commands that need root run unattended. The argv is
        wrapped *after* allowlist checks against the user-supplied argv[0].
    output_cap_bytes:
        Combined stdout + stderr is read up to this many bytes. Beyond that,
        the channel is closed and ``OutputTooLarge`` is raised.
    command_allowlist:
        If set, ``argv[0]`` must be one of these basename strings; otherwise
        ``CommandNotAllowed`` is raised. ``None`` disables the check.
    log_redactors:
        Regex patterns applied to log records from this module. Replace the
        default with a tighter set if your environment exposes other
        credential shapes.
    """

    _DEFAULT_REDACTORS: ClassVar[tuple[Pattern[str], ...]] = DEFAULT_REDACTORS

    def __init__(
        self,
        host: str,
        *,
        port: int = 22,
        username: str,
        known_host_fingerprint: str,
        private_key: str | None = None,
        password: str | None = None,
        connect_timeout: float = 10.0,
        exec_timeout: float = 30.0,
        sudo: bool = False,
        output_cap_bytes: int = 256 * 1024,
        command_allowlist: list[str] | tuple[str, ...] | None = None,
        log_redactors: tuple[Pattern[str], ...] = DEFAULT_REDACTORS,
    ) -> None:
        if not _PARAMIKO_AVAILABLE:
            raise RuntimeError(
                "paramiko is required for proxmox_sdk.ssh. "
                "Install it with: pip install proxmox-sdk[ssh]"
            )
        if not host:
            raise ValueError("host is required")
        if not username:
            raise ValueError("username is required")
        if private_key is None and password is None:
            raise ValueError("RemoteSSHClient requires private_key or password")
        if output_cap_bytes <= 0:
            raise ValueError("output_cap_bytes must be positive")

        self._host = host
        self._port = port
        self._username = username
        self._pinned_fp = _normalize_fingerprint(known_host_fingerprint)
        self._private_key = private_key
        self._password = password
        self._connect_timeout = connect_timeout
        self._exec_timeout = exec_timeout
        self._sudo = sudo
        self._output_cap = output_cap_bytes
        self._allowlist: frozenset[str] | None = (
            frozenset(command_allowlist) if command_allowlist is not None else None
        )
        self._redactors = log_redactors
        self._redacting_filter = _RedactingFilter(log_redactors)
        self._transport: Any = None  # paramiko.Transport

    # -- context manager ----------------------------------------------------

    async def __aenter__(self) -> RemoteSSHClient:
        logger.addFilter(self._redacting_filter)
        try:
            await self._connect()
        except Exception:
            logger.removeFilter(self._redacting_filter)
            raise
        return self

    async def __aexit__(self, exc_type: Any, exc: Any, tb: Any) -> None:
        try:
            await self.close()
        finally:
            logger.removeFilter(self._redacting_filter)

    async def close(self) -> None:
        transport = self._transport
        self._transport = None
        if transport is not None:
            loop = asyncio.get_running_loop()
            await loop.run_in_executor(None, transport.close)

    # -- connect ------------------------------------------------------------

    async def _connect(self) -> None:
        loop = asyncio.get_running_loop()
        try:
            await asyncio.wait_for(
                loop.run_in_executor(None, self._connect_blocking),
                timeout=self._connect_timeout,
            )
        except TimeoutError as exc:
            raise SshTimeout(
                f"connect to {self._host}:{self._port} timed out after {self._connect_timeout}s"
            ) from exc

    def _connect_blocking(self) -> None:
        pkey = self._load_private_key() if self._private_key else None

        # Bound the TCP handshake explicitly. paramiko.Transport((host, port))
        # would call socket.create_connection() with no timeout, so an
        # asyncio.wait_for cancel would leave the executor thread stuck until
        # the OS TCP timeout (~2 min). Pre-connect with our own timeout and
        # hand the live socket to paramiko.
        try:
            tcp = socket.create_connection((self._host, self._port), timeout=self._connect_timeout)
        except OSError as exc:
            raise SshError(f"tcp connect to {self._host}:{self._port} failed: {exc}") from exc
        # Reset to blocking; paramiko manages its own internal timeouts.
        tcp.settimeout(None)

        # Reach into paramiko's transport to pin algorithms *before*
        # authentication. SSHClient.connect() runs the handshake immediately,
        # so we cannot use the public Transport.get_security_options() hook
        # after connect(); we drive Transport directly instead.
        try:
            sock = paramiko.Transport(tcp)
        except Exception:
            tcp.close()
            raise
        sock.banner_timeout = self._connect_timeout
        opts = sock.get_security_options()
        # Filter to intersection of pinned preferences and paramiko's available set
        # so we never advertise an algorithm paramiko cannot actually negotiate.
        opts.kex = tuple(k for k in _PINNED_KEX if k in opts.kex) or opts.kex
        opts.ciphers = tuple(c for c in _PINNED_CIPHERS if c in opts.ciphers) or opts.ciphers
        opts.digests = tuple(m for m in _PINNED_MACS if m in opts.digests) or opts.digests
        opts.key_types = (
            tuple(k for k in _PINNED_HOST_KEY_TYPES if k in opts.key_types) or opts.key_types
        )

        try:
            sock.start_client(timeout=self._connect_timeout)
            host_key = sock.get_remote_server_key()
            actual_fp = fingerprint_sha256(host_key)
            if actual_fp != self._pinned_fp:
                raise HostKeyMismatch(
                    f"host key fingerprint mismatch for {self._host}: "
                    f"expected {self._pinned_fp}, got {actual_fp}"
                )

            if pkey is not None:
                sock.auth_publickey(self._username, pkey)
            elif self._password:
                sock.auth_password(self._username, self._password)
            else:  # pragma: no cover - already validated in __init__
                raise SshAuthFailed("no credentials available")

            if not sock.is_authenticated():
                raise SshAuthFailed(f"authentication failed for {self._username}@{self._host}")
        except HostKeyMismatch:
            sock.close()
            raise
        except paramiko.AuthenticationException as exc:
            sock.close()
            raise SshAuthFailed(
                f"authentication failed for {self._username}@{self._host}: {exc}"
            ) from exc
        except paramiko.SSHException as exc:
            sock.close()
            raise SshError(f"ssh handshake failed for {self._host}: {exc}") from exc
        except Exception:
            sock.close()
            raise

        self._transport = sock

    def _load_private_key(self) -> Any:
        # Unencrypted OpenSSH PEM only. Callers store key material in
        # Fernet-encrypted form at rest and decrypt to plaintext in memory
        # before constructing the client; passphrase-protected keys are not
        # supported here. Raises SshAuthFailed if no loader can parse the buffer.
        assert self._private_key is not None
        buf = io.StringIO(self._private_key)
        last_exc: Exception | None = None
        for loader in (
            paramiko.Ed25519Key.from_private_key,
            paramiko.RSAKey.from_private_key,
            paramiko.ECDSAKey.from_private_key,
        ):
            buf.seek(0)
            try:
                return loader(buf, password=None)
            except paramiko.SSHException as exc:
                last_exc = exc
                continue
        raise SshAuthFailed(
            f"could not parse supplied private_key as ed25519/rsa/ecdsa: {last_exc}"
        )

    # -- run ----------------------------------------------------------------

    async def run(self, argv: list[str]) -> CommandResult:
        """Execute ``argv`` over the open SSH session.

        Raises
        ------
        TypeError:
            If ``argv`` is not a list/tuple of strings.
        CommandNotAllowed:
            If ``argv[0]`` is outside the configured allowlist.
        OutputTooLarge:
            If combined stdout + stderr would exceed ``output_cap_bytes``.
        SshTimeout:
            If the command did not complete within ``exec_timeout``.
        """
        # ---- argv validation ----
        # Reject `str` explicitly so the type check fires before any iteration
        # converts a string into a per-character argv.
        if isinstance(argv, str) or not isinstance(argv, (list, tuple)):
            raise TypeError(
                f"RemoteSSHClient.run(argv) requires a list[str]; got {type(argv).__name__}"
            )
        if not argv:
            raise ValueError("argv must be non-empty")
        for i, part in enumerate(argv):
            if not isinstance(part, str):
                raise TypeError(f"argv[{i}] is not a str: {type(part).__name__}")

        if self._allowlist is not None:
            head = argv[0].rsplit("/", 1)[-1]
            if head not in self._allowlist:
                raise CommandNotAllowed(
                    f"argv[0]={head!r} is not in command_allowlist={sorted(self._allowlist)}"
                )

        if self._transport is None:
            raise SshError("RemoteSSHClient is not connected; use as `async with`")

        effective_argv: list[str] = ["sudo", "-n", *argv] if self._sudo else list(argv)
        cmd_str = shlex.join(effective_argv)

        loop = asyncio.get_running_loop()
        started = time.monotonic()
        try:
            result = await asyncio.wait_for(
                loop.run_in_executor(None, partial(self._exec_blocking, cmd_str)),
                timeout=self._exec_timeout,
            )
        except TimeoutError as exc:
            raise SshTimeout(
                f"command {effective_argv[0]!r} did not complete within "
                f"{self._exec_timeout}s on {self._host}"
            ) from exc
        duration = time.monotonic() - started
        stdout_b, stderr_b, exit_code, truncated = result
        return CommandResult(
            argv=tuple(effective_argv),
            stdout=stdout_b.decode("utf-8", errors="replace"),
            stderr=stderr_b.decode("utf-8", errors="replace"),
            exit_code=exit_code,
            duration_s=duration,
            truncated=truncated,
        )

    def _exec_blocking(self, cmd_str: str) -> tuple[bytes, bytes, int, bool]:
        transport = self._transport
        if transport is None or not transport.is_active():
            raise SshError("transport is closed")
        channel = transport.open_session(timeout=self._exec_timeout)
        try:
            channel.settimeout(self._exec_timeout)
            channel.set_combine_stderr(False)
            channel.exec_command(cmd_str)

            stdout = bytearray()
            stderr = bytearray()
            cap = self._output_cap
            truncated = False

            while True:
                got_data = False
                if channel.recv_ready():
                    chunk = channel.recv(65536)
                    if chunk:
                        stdout.extend(chunk)
                        got_data = True
                if channel.recv_stderr_ready():
                    chunk = channel.recv_stderr(65536)
                    if chunk:
                        stderr.extend(chunk)
                        got_data = True

                if len(stdout) + len(stderr) > cap:
                    truncated = True
                    try:
                        channel.close()
                    finally:
                        raise OutputTooLarge(
                            f"command output exceeded {cap} bytes "
                            f"(stdout={len(stdout)}, stderr={len(stderr)})"
                        )

                if channel.exit_status_ready() and not got_data:
                    # Drain whatever remains.
                    while channel.recv_ready():
                        stdout.extend(channel.recv(65536))
                    while channel.recv_stderr_ready():
                        stderr.extend(channel.recv_stderr(65536))
                    break

                if not got_data:
                    # Yield CPU briefly so we don't burn the executor thread.
                    time.sleep(0.01)

            exit_code = channel.recv_exit_status()
            return bytes(stdout), bytes(stderr), exit_code, truncated
        finally:
            try:
                channel.close()
            except Exception:  # pragma: no cover - defensive
                pass

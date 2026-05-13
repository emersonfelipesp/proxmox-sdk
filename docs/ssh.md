# SSH Primitive (`proxmox_sdk.ssh`)

`RemoteSSHClient` is the single source of truth for SSH access used across the
proxmox-sdk workspace and its downstream consumers (notably proxbox-api's
hardware discovery flow). It is intentionally **Proxmox-agnostic**: nothing
about Proxmox VE, `pvesh`, or NetBox is baked in.

> **Where this lives.** The class is exported as
> `from proxmox_sdk.ssh import RemoteSSHClient`. Consumers must depend on this
> module rather than importing `paramiko` directly.

## Security model

Every constructor argument enforces a security property. None of these are
opt-in.

| Property | Mechanism |
|---|---|
| Host-key pinning | `known_host_fingerprint=` (required). The SHA256 of the remote host key is compared via `hashlib.sha256(key.asbytes())`, base64-encoded with the `SHA256:` prefix. Mismatch raises `HostKeyMismatch` **before** auth. |
| No TOFU | A custom `_RejectAlwaysPolicy` is installed alongside the explicit fingerprint check. `AutoAddPolicy` and `WarningPolicy` are never used. |
| Algorithm pinning | The paramiko `Transport`'s security options are rewritten before `start_client()` to prefer curve25519-sha256, ChaCha20-Poly1305 / AES-256-GCM, ETM SHA-512/256 MACs, and rsa-sha2-512/256 + ssh-ed25519 host keys. |
| argv-list only | `run()` accepts `list[str]` exclusively. Passing a `str` raises `TypeError`. Internally `shlex.join()` is used to form the remote command, so shell metacharacters in argv elements cannot escape word boundaries. |
| Optional allowlist | `command_allowlist=["dmidecode", "ip", "ethtool"]` refuses any other `argv[0]` with `CommandNotAllowed`. The basename of an absolute path is used for the check, so sudoers-pinned `/usr/sbin/dmidecode` still matches. |
| Bounded output | `output_cap_bytes` (default 256 KiB) caps combined stdout + stderr per `run()`. Overflow raises `OutputTooLarge` and closes the channel. |
| Bounded time | `connect_timeout` (default 10 s) bounds the TCP handshake explicitly via `socket.create_connection`; `exec_timeout` (default 30 s) bounds each `run()` call via `asyncio.wait_for` plus paramiko channel timeout. |
| Log redaction | `_RedactingFilter` is installed on the module logger. The default patterns cover `password=…`, `token=…`, `BEGIN OPENSSH PRIVATE KEY` blocks, and Fernet-shaped tokens. Override via `log_redactors=`. |

## Construction

```python
from proxmox_sdk.ssh import RemoteSSHClient, fingerprint_sha256

async with RemoteSSHClient(
    host="10.0.0.1",
    port=22,
    username="proxbox-discovery",
    known_host_fingerprint="SHA256:abc…",          # required
    private_key=client_key_pem,                    # OpenSSH PEM string
    connect_timeout=10.0,
    exec_timeout=30.0,
    output_cap_bytes=256 * 1024,
    command_allowlist=["dmidecode", "ip", "ethtool"],
) as ssh:
    result = await ssh.run(["dmidecode", "-t", "1"])
    print(result.stdout, result.exit_code)
```

Credentials are **plaintext in memory only**. Downstream consumers (proxbox-api,
netbox-proxbox) store key material Fernet-encrypted at rest and decrypt just
long enough to construct the client. Passphrase-protected keys are not
supported here — keep the secret store as the only confidentiality boundary.

## Fingerprint workflow

`fingerprint_sha256(key)` returns the canonical `SHA256:<base64>` form (no
trailing `=` padding) for either a `paramiko.PKey` instance or raw key bytes.
Use it to populate the pin in your credential store after a one-time admin
"trust on first connect" probe:

```python
fp = fingerprint_sha256(remote_host_key_bytes)
# Persist `fp` only after explicit operator confirmation in the UI.
```

`_normalize_fingerprint` is applied to constructor input; it accepts the
canonical form, a lowercase `sha256:` prefix, padded base64, or a bare base64
value, and rejects `MD5:` (legacy/weak) and empty strings.

## Exception hierarchy

```
SshError
├── HostKeyMismatch         pinned fingerprint did not match
├── SshAuthFailed           paramiko refused the supplied credentials
├── SshTimeout              connect or exec timeout fired
├── OutputTooLarge          stdout+stderr exceeded output_cap_bytes
└── CommandNotAllowed       argv[0] outside command_allowlist
```

All five subclass `SshError`, so callers can pin a single `except SshError` if
they want to convert any failure into a warning frame.

## `CommandResult`

`run()` returns a frozen dataclass:

```python
@dataclass(frozen=True, slots=True)
class CommandResult:
    argv: tuple[str, ...]
    stdout: str
    stderr: str
    exit_code: int
    duration_s: float
    truncated: bool = False
```

`truncated` is reserved for future buffered-cap support; with the current
`OutputTooLarge` semantics it is always `False` on success.

## Threading model

`RemoteSSHClient` is an `async` context manager. Internally it runs paramiko's
blocking primitives on the default executor via `loop.run_in_executor`,
bounded by `asyncio.wait_for(..., timeout=...)`. Per-call timeouts mean a
stalled remote cannot strand executor threads beyond `exec_timeout`.

## Testing

Two test files cover this module:

* `tests/test_remote_ssh_client.py` — unit tests for argv validation, the
  allowlist, fingerprint normalisation, log redaction, and `CommandResult`
  shape. No socket is opened.
* `tests/test_remote_ssh_client_integration.py` — drives the real client
  against an in-process `paramiko.ServerInterface` running in a background
  thread. Covers the happy path, fingerprint mismatch, output cap, and exec
  timeout. No external SSH server is required.

The integration test fixture is reusable as a pattern for any downstream
project that wants to test against a known-good local SSH server.

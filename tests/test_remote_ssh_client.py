"""Unit tests for ``RemoteSSHClient`` argv validation, allowlist, fingerprint
normalization, and log redaction.

The paramiko-server integration tests live in
``test_remote_ssh_client_integration.py``; this file covers everything that
does not require an actual SSH handshake.
"""

from __future__ import annotations

import logging
import re

import pytest

pytest.importorskip("paramiko")

from proxmox_sdk.ssh import (  # type: ignore[attr-defined]  # noqa: E402
    DEFAULT_REDACTORS,
    CommandNotAllowed,
    CommandResult,
    HostKeyMismatch,
    RemoteSSHClient,
    SshError,
    _normalize_fingerprint,  # type: ignore[attr-defined]
    _redact,
    _RedactingFilter,
    fingerprint_sha256,
)

_VALID_FP = "SHA256:abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGH"


# --- fingerprint helpers ----------------------------------------------------


def test_normalize_fingerprint_accepts_canonical() -> None:
    assert _normalize_fingerprint(_VALID_FP) == _VALID_FP


def test_normalize_fingerprint_strips_base64_padding() -> None:
    assert _normalize_fingerprint("SHA256:abcd==") == "SHA256:abcd"


def test_normalize_fingerprint_accepts_lowercase_prefix() -> None:
    assert _normalize_fingerprint("sha256:abcd") == "SHA256:abcd"


def test_normalize_fingerprint_accepts_bare_value() -> None:
    assert _normalize_fingerprint("abcdef") == "SHA256:abcdef"


def test_normalize_fingerprint_rejects_md5() -> None:
    with pytest.raises(ValueError):
        _normalize_fingerprint("MD5:aa:bb:cc:dd")


def test_normalize_fingerprint_rejects_empty() -> None:
    with pytest.raises(ValueError):
        _normalize_fingerprint("")


def test_fingerprint_sha256_round_trips_bytes() -> None:
    fp = fingerprint_sha256(b"hello world")
    assert fp.startswith("SHA256:")
    # No padding in canonical form.
    assert "=" not in fp.split(":", 1)[1]


# --- constructor validation -------------------------------------------------


def _build(**overrides: object) -> RemoteSSHClient:
    base: dict[str, object] = {
        "host": "10.0.0.1",
        "username": "proxbox",
        "known_host_fingerprint": _VALID_FP,
        "private_key": "-----BEGIN OPENSSH PRIVATE KEY-----\nfake\n-----END OPENSSH PRIVATE KEY-----\n",
    }
    base.update(overrides)
    return RemoteSSHClient(**base)  # type: ignore[arg-type]


def test_constructor_requires_credentials() -> None:
    with pytest.raises(ValueError, match="private_key or password"):
        RemoteSSHClient(
            host="h",
            username="u",
            known_host_fingerprint=_VALID_FP,
        )


def test_constructor_requires_host() -> None:
    with pytest.raises(ValueError, match="host"):
        _build(host="")


def test_constructor_requires_username() -> None:
    with pytest.raises(ValueError, match="username"):
        _build(username="")


def test_constructor_rejects_nonpositive_output_cap() -> None:
    with pytest.raises(ValueError, match="output_cap_bytes"):
        _build(output_cap_bytes=0)


def test_constructor_stores_allowlist_as_frozenset() -> None:
    client = _build(command_allowlist=["dmidecode", "ip", "ethtool"])
    assert client._allowlist == frozenset({"dmidecode", "ip", "ethtool"})  # noqa: SLF001


# --- run() argv validation (no connection required) ------------------------


async def test_run_refuses_when_not_connected() -> None:
    client = _build()
    with pytest.raises(SshError, match="not connected"):
        await client.run(["dmidecode", "-t", "1"])


async def test_run_rejects_string_argv() -> None:
    client = _build()
    with pytest.raises(TypeError, match="list\\[str\\]"):
        await client.run("dmidecode -t 1")  # type: ignore[arg-type]


async def test_run_rejects_non_list_non_tuple() -> None:
    client = _build()
    with pytest.raises(TypeError):
        await client.run(123)  # type: ignore[arg-type]


async def test_run_rejects_empty_argv() -> None:
    client = _build()
    with pytest.raises(ValueError, match="argv must be non-empty"):
        await client.run([])


async def test_run_rejects_non_string_argv_element() -> None:
    client = _build()
    with pytest.raises(TypeError, match="argv\\[1\\] is not a str"):
        await client.run(["dmidecode", 1])  # type: ignore[list-item]


async def test_run_enforces_allowlist_basename() -> None:
    client = _build(command_allowlist=["dmidecode", "ip", "ethtool"])
    with pytest.raises(CommandNotAllowed, match="rm"):
        await client.run(["rm", "-rf", "/"])


async def test_run_allowlist_accepts_absolute_path() -> None:
    # An absolute path is normalized to the basename for the allowlist check;
    # this lets operators ship sudoers-pinned absolute paths from the node side.
    client = _build(command_allowlist=["dmidecode"])
    # Still raises SshError("not connected") rather than CommandNotAllowed:
    # the allowlist must have accepted the call before noticing the closed
    # transport.
    with pytest.raises(SshError, match="not connected"):
        await client.run(["/usr/sbin/dmidecode", "-t", "1"])


# --- log redaction ----------------------------------------------------------


def test_redact_strips_password() -> None:
    out = _redact("password=hunter2 token=abc", DEFAULT_REDACTORS)
    assert "hunter2" not in out
    assert "abc" not in out
    assert "***" in out


def test_redact_strips_private_key_block() -> None:
    text = (
        "key=-----BEGIN OPENSSH PRIVATE KEY-----\nb3BlbnNzaC1rZXkt\n"
        "-----END OPENSSH PRIVATE KEY-----"
    )
    out = _redact(text, DEFAULT_REDACTORS)
    assert "BEGIN OPENSSH PRIVATE KEY" not in out
    assert "b3BlbnNzaC1rZXkt" not in out


def test_redact_strips_fernet_shape() -> None:
    text = "rotated to gAAAAABoZw3KqXAbcdef0123456789_-=abcdefg"
    out = _redact(text, DEFAULT_REDACTORS)
    assert "gAAAAA" not in out


def test_redacting_filter_rewrites_log_record(caplog: pytest.LogCaptureFixture) -> None:
    logger = logging.getLogger("proxmox_sdk.ssh.redact_test")
    f = _RedactingFilter(DEFAULT_REDACTORS)
    logger.addFilter(f)
    try:
        with caplog.at_level(logging.INFO, logger="proxmox_sdk.ssh.redact_test"):
            logger.info("auth attempt password=hunter2")
    finally:
        logger.removeFilter(f)
    assert "hunter2" not in caplog.text
    assert "***" in caplog.text


# --- CommandResult dataclass -----------------------------------------------


def test_command_result_is_frozen_and_typed() -> None:
    r = CommandResult(
        argv=("dmidecode", "-t", "1"),
        stdout="ok",
        stderr="",
        exit_code=0,
        duration_s=0.5,
    )
    assert r.truncated is False
    with pytest.raises(AttributeError):
        r.exit_code = 1  # type: ignore[misc]


# --- exception hierarchy ---------------------------------------------------


def test_exceptions_subclass_ssh_error() -> None:
    for cls in (HostKeyMismatch, CommandNotAllowed):
        assert issubclass(cls, SshError)


def test_default_redactors_compile() -> None:
    for pat in DEFAULT_REDACTORS:
        assert isinstance(pat, re.Pattern)

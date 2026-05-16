"""Unit tests for :class:`PDMMockState`."""

from __future__ import annotations

from proxmox_sdk.pdm.mock.routes import PDMMockState
from proxmox_sdk.pdm.mock.seed_data import get_default_pdm_seed


def test_snapshot_returns_deep_copy():
    state = PDMMockState()
    snap = state.snapshot()
    snap["remotes"].clear()
    assert state.remotes()


def test_replace_overwrites_state():
    state = PDMMockState()
    state.replace({"remotes": [{"id": "x", "type": "pve"}]})
    assert state.remotes() == [{"id": "x", "type": "pve"}]


def test_reset_restores_default_seed():
    state = PDMMockState()
    state.replace({"remotes": []})
    state.reset()
    assert state.remotes() == get_default_pdm_seed()["remotes"]


def test_upsert_inserts_then_updates():
    state = PDMMockState(seed={"remotes": [], "pve": {}, "pbs": {}, "access": {}})
    state.upsert_remote({"id": "pve-x", "type": "pve"})
    state.upsert_remote({"id": "pve-x", "type": "pve", "fingerprint": "AA"})
    remotes = state.remotes()
    assert len(remotes) == 1
    assert remotes[0]["fingerprint"] == "AA"


def test_remove_remote_returns_false_for_missing():
    state = PDMMockState()
    assert state.remove_remote("nope") is False


def test_update_guest_status_round_trip():
    state = PDMMockState()
    assert state.update_guest_status("pve-cluster-a", "qemu", 100, "stopped") is True
    guest = state.find_guest("pve-cluster-a", "qemu", 100)
    assert guest is not None and guest["status"] == "stopped"


def test_update_guest_status_missing_returns_false():
    state = PDMMockState()
    assert state.update_guest_status("pve-cluster-a", "qemu", 9999, "stopped") is False

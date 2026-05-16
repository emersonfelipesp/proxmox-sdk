"""Seed data shape + isolation tests."""

from __future__ import annotations

from proxmox_sdk.pdm.mock.seed_data import get_default_pdm_seed


def test_seed_has_two_pve_and_one_pbs_remote():
    seed = get_default_pdm_seed()
    remotes = seed["remotes"]
    pve = [r for r in remotes if r["type"] == "pve"]
    pbs = [r for r in remotes if r["type"] == "pbs"]
    assert len(pve) == 2
    assert len(pbs) == 1


def test_seed_returns_fresh_copy_per_call():
    a = get_default_pdm_seed()
    b = get_default_pdm_seed()
    a["remotes"].pop()
    assert len(b["remotes"]) > len(a["remotes"])


def test_seed_has_users_and_acl():
    seed = get_default_pdm_seed()
    assert len(seed["access"]["users"]) >= 3
    assert len(seed["access"]["acl"]) >= 5


def test_seed_has_views_and_subscriptions():
    seed = get_default_pdm_seed()
    assert len(seed["views"]) >= 2
    assert len(seed["resources"]["subscriptions"]) >= 3


def test_seed_pve_cluster_a_has_expected_topology():
    seed = get_default_pdm_seed()
    bucket = seed["pve"]["pve-cluster-a"]
    assert len(bucket["nodes"]) == 3
    assert len(bucket["qemu"]) == 10
    assert len(bucket["lxc"]) == 5

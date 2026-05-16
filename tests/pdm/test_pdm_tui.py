"""Unit tests for PDM Textual TUI helpers and surface.

We avoid driving the whole Textual app through ``App.run_test()`` because
that requires a real (or simulated) tty event loop that some sandboxed CI
environments don't provide. Instead we exercise the pure helpers (response
unwrapping, label rendering, tree population) and assert that the
public TUI symbols exist and have the expected shape.
"""

from __future__ import annotations

from typing import Any

from proxmox_sdk.proxmox_cli.pdm_tui_app import (
    ConfirmModal,
    PDMActionPanel,
    PDMGuestPanel,
    PDMTuiApp,
    PDMTuiRuntime,
    RemoteEntry,
    _add_guest_children,
    _as_list,
    run_pdm_tui,
)


# ---------------------------------------------------------------------------
# Response unwrapping
# ---------------------------------------------------------------------------


def test_as_list_unwraps_data_envelope():
    assert _as_list({"data": [{"a": 1}]}) == [{"a": 1}]
    assert _as_list({"data": None}) == []
    assert _as_list({"data": {"k": {"v": 1}}}) == [{"v": 1}]


def test_as_list_passes_through_lists():
    assert _as_list([1, 2]) == [1, 2]


def test_as_list_handles_none_and_scalars():
    assert _as_list(None) == []
    assert _as_list("foo") == ["foo"]
    assert _as_list(42) == [42]


def test_as_list_handles_plain_dict():
    """Dicts without a single `data` key flatten to their values."""
    assert _as_list({"a": {"x": 1}, "b": {"x": 2}}) == [{"x": 1}, {"x": 2}]


# ---------------------------------------------------------------------------
# RemoteEntry icon dispatch
# ---------------------------------------------------------------------------


def test_remote_entry_pve_icon():
    assert RemoteEntry(id="x", type="pve", payload={}).icon == "🖥"


def test_remote_entry_pbs_icon():
    assert RemoteEntry(id="x", type="pbs", payload={}).icon == "💾"


def test_remote_entry_unknown_icon():
    assert RemoteEntry(id="x", type="other", payload={}).icon == "❔"


# ---------------------------------------------------------------------------
# Tree helper
# ---------------------------------------------------------------------------


def test_add_guest_children_populates_tree_node():
    """Inserts one labeled leaf per guest and survives a redraw."""
    from textual.widgets import Tree

    tree: Tree[Any] = Tree("root")
    node = tree.root.add("remote", data=RemoteEntry(id="pve-a", type="pve", payload={}))
    _add_guest_children(
        node,
        [
            {"vmid": 100, "type": "qemu", "name": "web"},
            {"vmid": 200, "type": "lxc", "name": None},
        ],
    )
    labels = [str(c.label) for c in node.children]
    assert any("qemu 100 — web" in lbl for lbl in labels)
    assert any("lxc 200 — unnamed" in lbl for lbl in labels)


def test_add_guest_children_replaces_previous_set():
    """A second call wipes the first set, not appends."""
    from textual.widgets import Tree

    tree: Tree[Any] = Tree("root")
    node = tree.root.add("remote", data=None)
    _add_guest_children(node, [{"vmid": 1, "type": "qemu", "name": "a"}])
    assert len(node.children) == 1
    _add_guest_children(node, [{"vmid": 2, "type": "lxc", "name": "b"}])
    assert len(node.children) == 1
    assert "lxc 2" in str(node.children[0].label)


# ---------------------------------------------------------------------------
# Runtime dataclass
# ---------------------------------------------------------------------------


def test_runtime_defaults():
    r = PDMTuiRuntime(mode="mock")
    assert r.mode == "mock"
    assert r.initial_remote is None


def test_runtime_accepts_initial_remote():
    r = PDMTuiRuntime(mode="production", initial_remote="pve-a")
    assert r.initial_remote == "pve-a"


# ---------------------------------------------------------------------------
# Public API surface
# ---------------------------------------------------------------------------


def test_public_api_exports():
    assert callable(run_pdm_tui)
    # Classes referenced from the CLI bridge must remain importable.
    for cls in (PDMTuiApp, PDMActionPanel, PDMGuestPanel, ConfirmModal):
        assert isinstance(cls, type)


def test_app_can_be_instantiated_without_running():
    """Construction is cheap and doesn't require a tty."""

    class _NoopBridge:
        def get(self, *a: Any, **kw: Any) -> Any:
            return None

        def post(self, *a: Any, **kw: Any) -> Any:
            return None

        def close(self) -> None:
            return None

    app = PDMTuiApp(bridge=_NoopBridge(), runtime=PDMTuiRuntime(mode="mock"))
    assert app._runtime.mode == "mock"
    assert app._remotes == []


def test_status_text_includes_mode():
    class _NoopBridge:
        def get(self, *a: Any, **kw: Any) -> Any:
            return None

        def post(self, *a: Any, **kw: Any) -> Any:
            return None

        def close(self) -> None:
            return None

    app = PDMTuiApp(bridge=_NoopBridge(), runtime=PDMTuiRuntime(mode="production"))
    assert "production" in app._status_text()


def test_action_panel_button_count():
    """Action panel should ship the documented button set."""
    assert len(PDMActionPanel.BUTTONS) == 6
    ids = {b[1] for b in PDMActionPanel.BUTTONS}
    assert {"start", "stop", "shutdown", "migrate", "remote-migrate", "refresh"} == ids

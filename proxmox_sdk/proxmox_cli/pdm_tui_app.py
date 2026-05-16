"""Textual TUI for Proxmox Datacenter Manager (PDM).

3-pane layout:

    ┌─────────────────┬──────────────────────────┬────────────────────┐
    │  Remote Tree    │  Resource list / detail  │  Action panel      │
    │  (sidebar 25%)  │  (center 50%)            │  (right 25%)       │
    └─────────────────┴──────────────────────────┴────────────────────┘

The left tree lists registered PDM remotes (PVE 🖥 and PBS 💾) with their
nodes/datastores as children. Selecting a node loads guests into the
DataTable in the center pane. Selecting a guest fills the detail panel
with its config. The right action panel exposes start/stop/shutdown/
migrate/remote-migrate buttons that call the SDK via the bridge.

Tests run headlessly via ``App.run_test()`` + ``Pilot``.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Any, Literal

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.screen import ModalScreen
from textual.widgets import (
    Button,
    DataTable,
    Footer,
    Header,
    Label,
    Static,
    TextArea,
    Tree,
)
from textual.widgets.tree import TreeNode

from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge

logger = logging.getLogger(__name__)

TuiMode = Literal["production", "mock"]


# ---------------------------------------------------------------------------
# Runtime metadata
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PDMTuiRuntime:
    mode: TuiMode
    initial_remote: str | None = None


@dataclass(frozen=True)
class RemoteEntry:
    """A registered PDM remote shown in the tree."""

    id: str
    type: str  # "pve" | "pbs" | other
    payload: dict[str, Any]

    @property
    def icon(self) -> str:
        return "🖥" if self.type == "pve" else "💾" if self.type == "pbs" else "❔"


# ---------------------------------------------------------------------------
# Modals
# ---------------------------------------------------------------------------


class ConfirmModal(ModalScreen[bool]):
    """Yes/No confirmation modal used before destructive SDK calls."""

    CSS = """
    ConfirmModal {
        align: center middle;
    }
    #confirm-dialog {
        width: 60;
        border: thick $primary;
        background: $surface;
        padding: 1 2;
    }
    #confirm-buttons {
        margin-top: 1;
        align: center middle;
    }
    Button { margin: 0 1; }
    """

    def __init__(self, prompt: str) -> None:
        super().__init__()
        self._prompt = prompt

    def compose(self) -> ComposeResult:
        with Vertical(id="confirm-dialog"):
            yield Label(self._prompt)
            with Horizontal(id="confirm-buttons"):
                yield Button("Confirm", id="confirm-yes", variant="primary")
                yield Button("Cancel", id="confirm-no", variant="default")

    @on(Button.Pressed, "#confirm-yes")
    def _yes(self) -> None:
        self.dismiss(True)

    @on(Button.Pressed, "#confirm-no")
    def _no(self) -> None:
        self.dismiss(False)


# ---------------------------------------------------------------------------
# Action panel — encapsulates SDK calls behind the button row
# ---------------------------------------------------------------------------


class PDMActionPanel(Static):
    """Right-side action buttons that operate on the currently selected guest."""

    BUTTONS: tuple[tuple[str, str, str], ...] = (
        ("Start", "start", "success"),
        ("Stop", "stop", "warning"),
        ("Shutdown", "shutdown", "warning"),
        ("Migrate", "migrate", "default"),
        ("Remote Migrate", "remote-migrate", "default"),
        ("Refresh", "refresh", "primary"),
    )

    def compose(self) -> ComposeResult:
        yield Label("Actions", classes="panel-title")
        yield Label("(no selection)", id="action-selection")
        for label, action_id, variant in self.BUTTONS:
            yield Button(label, id=f"action-{action_id}", variant=variant)


# ---------------------------------------------------------------------------
# Detail panel
# ---------------------------------------------------------------------------


class PDMGuestPanel(Static):
    """Detail viewer for the selected guest (config dump + RRD sparkline)."""

    def compose(self) -> ComposeResult:
        yield Label("Guest detail", classes="panel-title")
        yield TextArea("", id="guest-detail", read_only=True, language="json")


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------


class PDMTuiApp(App[None]):
    """Three-pane PDM TUI driven by the SDK bridge."""

    CSS = """
    Screen { layout: vertical; }
    #top { layout: horizontal; height: 1fr; }
    #remote_tree_panel { width: 25%; border-right: solid $panel; }
    #center_panel { width: 50%; border-right: solid $panel; }
    #action_panel { width: 25%; padding: 1; }
    #status_bar {
        height: auto;
        padding: 0 1;
        background: $surface;
        color: $text-muted;
    }
    .panel-title { text-style: bold; padding: 0 1; }
    """

    BINDINGS = (
        Binding("r", "refresh", "Refresh"),
        Binding("d", "dashboard", "Dashboard"),
        Binding("q", "quit", "Quit"),
    )

    def __init__(self, bridge: ProxmoxSDKBridge, runtime: PDMTuiRuntime) -> None:
        super().__init__()
        self._bridge = bridge
        self._runtime = runtime
        self._remotes: list[RemoteEntry] = []
        self._selected_remote: RemoteEntry | None = None
        self._selected_guest: dict[str, Any] | None = None

    # -- composition -----------------------------------------------------

    def compose(self) -> ComposeResult:
        yield Header(show_clock=False)
        with Horizontal(id="top"):
            with Vertical(id="remote_tree_panel"):
                yield Label("Remotes", classes="panel-title")
                tree: Tree[RemoteEntry | dict[str, Any]] = Tree("PDM", id="remote_tree")
                tree.root.expand()
                yield tree
            with Vertical(id="center_panel"):
                yield Label("Resources", classes="panel-title")
                table: DataTable[Any] = DataTable(id="resource_table", zebra_stripes=True)
                table.cursor_type = "row"
                yield table
                yield PDMGuestPanel(id="detail")
            yield PDMActionPanel(id="action_panel")
        yield Static(self._status_text(), id="status_bar")
        yield Footer()

    def _status_text(self) -> str:
        mode = self._runtime.mode
        return f"PDM TUI ({mode}) — [r] refresh, [d] dashboard, [q] quit"

    # -- lifecycle -------------------------------------------------------

    def on_mount(self) -> None:
        table: DataTable[Any] = self.query_one("#resource_table", DataTable)
        table.add_columns("vmid", "name", "type", "node", "status", "cpu%", "mem", "uptime")
        self._load_remotes()

    # -- data loading ----------------------------------------------------

    def _safe_call(self, fn: Any, *args: Any, **kwargs: Any) -> Any:
        """Call into the bridge and swallow errors into the status bar."""
        try:
            return fn(*args, **kwargs)
        except Exception as exc:  # pragma: no cover - surfaced to UI
            logger.exception("PDM TUI: bridge call failed")
            self._set_status(f"Error: {exc}")
            return None

    def _set_status(self, msg: str) -> None:
        try:
            self.query_one("#status_bar", Static).update(msg)
        except Exception:
            pass

    def _load_remotes(self) -> None:
        result = self._safe_call(self._bridge.get, "/remotes")
        items = _as_list(result)
        self._remotes = [
            RemoteEntry(id=str(r.get("id", "")), type=str(r.get("type", "")), payload=r)
            for r in items
            if isinstance(r, dict) and r.get("id")
        ]
        tree: Tree[RemoteEntry | dict[str, Any]] = self.query_one("#remote_tree", Tree)
        tree.clear()
        for remote in self._remotes:
            label = f"{remote.icon} {remote.id} ({remote.type})"
            tree.root.add(label, data=remote, expand=False)
        tree.root.expand()
        if self._remotes:
            self._set_status(f"Loaded {len(self._remotes)} remote(s).")
        else:
            self._set_status("No PDM remotes found.")

    def _load_guests_for_remote(self, remote: RemoteEntry) -> list[dict[str, Any]]:
        if remote.type != "pve":
            return []
        qemu = _as_list(self._safe_call(self._bridge.get, f"/pve/remotes/{remote.id}/guests/qemu"))
        lxc = _as_list(self._safe_call(self._bridge.get, f"/pve/remotes/{remote.id}/guests/lxc"))
        merged: list[dict[str, Any]] = []
        for entry in qemu:
            if isinstance(entry, dict):
                entry = {**entry, "type": entry.get("type", "qemu"), "remote": remote.id}
                merged.append(entry)
        for entry in lxc:
            if isinstance(entry, dict):
                entry = {**entry, "type": entry.get("type", "lxc"), "remote": remote.id}
                merged.append(entry)
        return merged

    def _render_guest_table(self, guests: list[dict[str, Any]]) -> None:
        table: DataTable[Any] = self.query_one("#resource_table", DataTable)
        table.clear()
        for g in guests:
            table.add_row(
                str(g.get("vmid", "")),
                str(g.get("name", "")),
                str(g.get("type", "")),
                str(g.get("node", "")),
                str(g.get("status", "")),
                f"{(g.get('cpu') or 0) * 100:.1f}" if isinstance(g.get("cpu"), float) else "",
                str(g.get("mem", "")),
                str(g.get("uptime", "")),
            )

    # -- tree selection -> load guests for the chosen remote -------------

    @on(Tree.NodeSelected)
    def _on_tree_select(self, event: Tree.NodeSelected[Any]) -> None:
        node = event.node
        data = node.data
        if isinstance(data, RemoteEntry):
            self._selected_remote = data
            self._set_status(f"Loading guests for {data.id} …")
            guests = self._load_guests_for_remote(data)
            self._render_guest_table(guests)
            self._set_status(f"Loaded {len(guests)} guest(s) on {data.id}.")
            node.expand()
            _add_guest_children(node, guests)

    @on(DataTable.RowSelected)
    def _on_row_select(self, event: DataTable.RowSelected) -> None:
        table: DataTable[Any] = event.data_table
        try:
            row = table.get_row(event.row_key)
        except Exception:
            return
        if not row:
            return
        vmid = str(row[0])
        gtype = str(row[2])
        if not self._selected_remote:
            return
        guest_dict = {"vmid": vmid, "type": gtype, "remote": self._selected_remote.id}
        self._selected_guest = guest_dict
        self.query_one("#action-selection", Label).update(
            f"{self._selected_remote.id}/{gtype}/{vmid}"
        )
        cfg = self._safe_call(
            self._bridge.get,
            f"/pve/remotes/{self._selected_remote.id}/guests/{gtype}/{vmid}/config",
        )
        if cfg is not None:
            try:
                import json as _json

                self.query_one("#guest-detail", TextArea).text = _json.dumps(cfg, indent=2)
            except Exception:
                pass

    # -- action buttons --------------------------------------------------

    @on(Button.Pressed, "#action-refresh")
    def _refresh(self) -> None:
        self._load_remotes()

    @on(Button.Pressed, "#action-start")
    async def _start(self) -> None:
        await self._guest_action("start", "Start this guest?")

    @on(Button.Pressed, "#action-stop")
    async def _stop(self) -> None:
        await self._guest_action("stop", "Force-stop this guest?")

    @on(Button.Pressed, "#action-shutdown")
    async def _shutdown(self) -> None:
        await self._guest_action("shutdown", "Shut down this guest gracefully?")

    @on(Button.Pressed, "#action-migrate")
    async def _migrate(self) -> None:
        # Migrate requires extra input that doesn't fit a simple button row;
        # fall back to surfacing guidance in the status bar.
        self._set_status("Use `proxmox pdm pve qemu migrate <remote> <vmid> --target …`.")

    @on(Button.Pressed, "#action-remote-migrate")
    async def _remote_migrate(self) -> None:
        self._set_status(
            "Use `proxmox pdm pve qemu remote-migrate <remote> <vmid> --target-remote …`."
        )

    async def _guest_action(self, action: str, prompt: str) -> None:
        if not self._selected_guest or not self._selected_remote:
            self._set_status("Select a guest first.")
            return
        confirmed = await self.push_screen_wait(ConfirmModal(prompt))
        if not confirmed:
            self._set_status("Action cancelled.")
            return
        g = self._selected_guest
        path = f"/pve/remotes/{self._selected_remote.id}/guests/{g['type']}/{g['vmid']}/{action}"
        self._safe_call(self._bridge.post, path)
        self._set_status(f"Issued {action} on {g['type']}/{g['vmid']}.")

    # -- key bindings ----------------------------------------------------

    def action_refresh(self) -> None:
        self._load_remotes()

    def action_dashboard(self) -> None:
        result = self._safe_call(self._bridge.get, "/resources/status")
        items = _as_list(result)
        self._set_status(f"Dashboard: {len(items)} remote(s) reporting status.")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _as_list(value: Any) -> list[Any]:
    """Normalise SDK responses (dict-with-data / list / scalar) to a list."""
    if value is None:
        return []
    if isinstance(value, dict):
        if "data" in value and len(value) == 1:
            inner = value["data"]
            if isinstance(inner, list):
                return inner
            if inner is None:
                return []
            if isinstance(inner, dict):
                return list(inner.values())
            return [inner]
        return list(value.values())
    if isinstance(value, list):
        return value
    return [value]


def _add_guest_children(node: TreeNode[Any], guests: list[dict[str, Any]]) -> None:
    """Append a short summary of each guest under the remote node."""
    # Replace any previous children so re-selecting a remote refreshes cleanly.
    node.remove_children()
    for g in guests:
        label = f"{g.get('type', '?')} {g.get('vmid', '?')} — {g.get('name') or 'unnamed'}"
        node.add_leaf(label, data=g)


def run_pdm_tui(
    bridge: ProxmoxSDKBridge,
    *,
    mode: TuiMode,
    initial_remote: str | None = None,
) -> None:
    """Run the PDM Textual TUI."""
    app = PDMTuiApp(
        bridge=bridge,
        runtime=PDMTuiRuntime(mode=mode, initial_remote=initial_remote),
    )
    app.run()


__all__ = [
    "ConfirmModal",
    "PDMActionPanel",
    "PDMGuestPanel",
    "PDMTuiApp",
    "PDMTuiRuntime",
    "RemoteEntry",
    "run_pdm_tui",
]

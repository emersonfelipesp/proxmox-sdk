"""Shared Textual ``App`` base class for path-browser style module TUIs.

PVE, Ceph and PBS share the same generic three-area layout — tree on the
left, command input + JSON view + log on the right — with only the
initial path, title, tree seed paths and module identifier differing.

This module factors that common scaffolding out so each per-module app
becomes a tiny subclass that supplies module-specific seed data while
inheriting the in-app View selector and the rest of the layout.

The View selector dropdown follows the netbox-sdk pattern: choosing a
different module exits the current app with a ``SWITCH_TO_*`` sentinel,
which the runner loop catches to start the next module's app in the
same process.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from typing import Any, ClassVar, Literal

from textual import on
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Horizontal, Vertical
from textual.widgets import Footer, Header, Input, RichLog, Select, Static, TextArea, Tree

from proxmox_sdk.proxmox_cli.sdk_bridge import ProxmoxSDKBridge
from proxmox_sdk.proxmox_cli.tui.chrome import (
    VIEW_SELECT_OPTIONS,
    ModuleName,
    sentinel_for_module,
)
from proxmox_sdk.proxmox_cli.utils import validate_api_path

TuiMode = Literal["production", "mock"]


@dataclass(frozen=True)
class PathBrowserRuntime:
    """Runtime options shared by all path-browser module TUIs."""

    mode: TuiMode
    initial_path: str


@dataclass
class PathNode:
    """Represents a browsable path in the navigation tree."""

    path: str
    label: str
    data: dict[str, Any] | list[dict[str, Any]] | None = None
    children_loaded: bool = False


@dataclass(frozen=True)
class ModuleProfile:
    """Per-module identity used by the path-browser base class."""

    module: ModuleName
    title: str
    sub_title: str
    default_initial_path: str
    tree_root_label: str
    tree_seed: tuple[tuple[str, str], ...] = field(default_factory=tuple)


class PathBrowserApp(App[object]):
    """Generic three-area path browser shared by PVE/Ceph/PBS TUIs.

    Subclasses set :attr:`PROFILE` to declare module-specific labels and
    seed paths. The View selector exits with a SWITCH_TO_* sentinel so
    the runner loop can swap views without restarting the process.
    """

    PROFILE: ClassVar[ModuleProfile]

    CSS = """
    Screen {
        layout: vertical;
    }

    #topbar {
        height: 3;
        padding: 0 1;
        background: $surface;
    }

    #view_select {
        width: 18;
        margin-right: 1;
    }

    #status {
        height: auto;
        padding: 0 1;
        color: $text-muted;
        background: $surface;
    }

    #filter_bar {
        height: auto;
        padding: 0 1;
        background: $surface;
    }

    #filter_input {
        margin: 0 1;
    }

    #main_container {
        layout: horizontal;
        height: 100%;
    }

    #tree_panel {
        width: 30%;
        border-right: solid $panel;
    }

    #detail_panel {
        width: 70%;
    }

    #command_input {
        margin: 0 1;
    }

    #output_log {
        margin: 1;
        border: solid $panel;
        padding: 0 1;
    }

    #json_view {
        margin: 1;
        border: solid $panel;
    }

    .status-online { color: green; }
    .status-offline { color: red; }
    .status-warning { color: yellow; }
    """

    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("i", "focus_input", "Focus input"),
        Binding("f", "toggle_filter", "Filter"),
        Binding("t", "toggle_tree", "Tree"),
        Binding("j", "move_down", "Down", show=False),
        Binding("k", "move_up", "Up", show=False),
        Binding("l", "expand_or_select", "Right", show=False),
        Binding("h", "collapse", "Left", show=False),
        Binding("ctrl+l", "clear_output", "Clear output"),
        Binding("/", "focus_filter", "Search", show=False),
        Binding("escape", "close_filter", "Close search", show=False),
    ]

    def __init__(self, bridge: ProxmoxSDKBridge, runtime: PathBrowserRuntime) -> None:
        super().__init__()
        self._bridge = bridge
        self._runtime = runtime
        self._last_command = runtime.initial_path
        self._current_data: list[dict[str, Any]] | dict[str, Any] | None = None
        self._filter_query: str = ""
        self._show_tree: bool = True

    # -- composition ----------------------------------------------------

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with Vertical():
            with Horizontal(id="topbar"):
                yield Select(
                    options=list(VIEW_SELECT_OPTIONS),
                    value=self.PROFILE.module,
                    allow_blank=False,
                    id="view_select",
                )
                yield Static(
                    f"Mode: {self._runtime.mode} | [b]Keys:[/b] q=quit r=refresh"
                    " f=filter t=tree /=search j/k/l/h=navigate",
                    id="status",
                )
            with Horizontal(id="filter_bar"):
                yield Input(
                    placeholder="Filter results... (press / to focus, Esc to close)",
                    id="filter_input",
                )
            with Horizontal(id="main_container"):
                with Vertical(id="tree_panel"):
                    yield Static("Navigation Tree", id="tree_header")
                    yield Tree(self.PROFILE.tree_root_label, id="nav_tree")
                with Vertical(id="detail_panel"):
                    yield Input(value=self._runtime.initial_path, id="command_input")
                    yield RichLog(id="output_log", wrap=True, highlight=False, markup=False)
                    yield TextArea(id="json_view", read_only=True, show_line_numbers=False)
        yield Footer()

    # -- lifecycle ------------------------------------------------------

    def on_mount(self) -> None:
        self.title = self.PROFILE.title
        self.sub_title = self.PROFILE.sub_title
        self.query_one("#filter_bar", Horizontal).display = False
        self.query_one("#command_input", Input).focus()
        self._init_tree()
        self._execute_command(self._runtime.initial_path)

    def _init_tree(self) -> None:
        tree = self.query_one("#nav_tree", Tree)
        tree.root.label = self.PROFILE.tree_root_label
        for path, label in self.PROFILE.tree_seed:
            node = tree.root.add(label, data=PathNode(path=path, label=label))
            node.expandable = True
        tree.root.expand()

    # -- view switching -------------------------------------------------

    @on(Select.Changed, "#view_select")
    def _on_view_changed(self, event: Select.Changed) -> None:
        if event.value == Select.BLANK:
            return
        target = str(event.value)
        if target == self.PROFILE.module:
            return
        try:
            sentinel = sentinel_for_module(target)  # type: ignore[arg-type]
        except KeyError:
            return
        self.exit(result=sentinel)

    # -- tree -----------------------------------------------------------

    def on_tree_node_expanded(self, event: Tree.NodeExpanded) -> None:
        node = event.node
        data = node.data
        if data and isinstance(data, PathNode) and not data.children_loaded:
            self._load_tree_children(node, data)

    def _load_tree_children(self, node: Tree.Node, data: PathNode) -> None:
        try:
            path = data.path
            if "{node}" in path and self._current_data:
                if isinstance(self._current_data, list) and self._current_data:
                    first_item = self._current_data[0]
                    if "node" in first_item:
                        node_name = first_item["node"]
                        path = path.replace("{node}", node_name)

            result = self._bridge.list_children(path)
            if result and isinstance(result, list):
                data.children_loaded = True
                for item in result[:20]:
                    item_label = (
                        item.get("node") or item.get("vmid") or item.get("name") or str(item)
                    )
                    item_path = f"{path}/{item_label}"
                    child_node = node.add(
                        item_label, data=PathNode(path=item_path, label=str(item_label), data=item)
                    )
                    child_node.expandable = True
        except Exception:
            pass  # tree expansion is best-effort

    def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        node = event.node
        data = node.data
        if data and isinstance(data, PathNode):
            self.query_one("#command_input", Input).value = data.path
            self._execute_command(data.path)

    # -- input ----------------------------------------------------------

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self._execute_command(event.value)

    def action_focus_input(self) -> None:
        self.query_one("#command_input", Input).focus()

    def action_focus_filter(self) -> None:
        self.query_one("#filter_bar", Horizontal).display = True
        self.query_one("#filter_input", Input).focus()

    def action_close_filter(self) -> None:
        self.query_one("#filter_bar", Horizontal).display = False
        self._filter_query = ""
        self.query_one("#command_input", Input).focus()

    def action_toggle_tree(self) -> None:
        self._show_tree = not self._show_tree
        tree_panel = self.query_one("#tree_panel", Vertical)
        detail_panel = self.query_one("#detail_panel", Vertical)
        if self._show_tree:
            tree_panel.display = True
            detail_panel.styles.width = "70%"
        else:
            tree_panel.display = False
            detail_panel.styles.width = "100%"

    def action_toggle_filter(self) -> None:
        filter_bar = self.query_one("#filter_bar", Horizontal)
        if filter_bar.display:
            self.action_close_filter()
        else:
            self.action_focus_filter()

    def action_refresh(self) -> None:
        self._execute_command(self._last_command)

    def action_clear_output(self) -> None:
        self.query_one("#output_log", RichLog).clear()

    def action_move_down(self) -> None:
        pass

    def action_move_up(self) -> None:
        pass

    def action_expand_or_select(self) -> None:
        tree = self.query_one("#nav_tree", Tree)
        selected = tree.selected_node
        if selected and selected.expandable:
            selected.toggle()
        elif selected is not None and not selected.expandable:
            data = selected.data
            if data and isinstance(data, PathNode):
                self._execute_command(data.path)

    def action_collapse(self) -> None:
        tree = self.query_one("#nav_tree", Tree)
        selected = tree.selected_node
        if selected and selected.is_expanded:
            selected.toggle()

    # -- bridge --------------------------------------------------------

    def _execute_command(self, raw: str) -> None:
        method, path = self._parse_command(raw)
        self._last_command = f"{method} {path}" if raw.strip() else self._last_command

        log = self.query_one("#output_log", RichLog)
        log.clear()
        log.write(f"$ {method.upper()} {path}")

        try:
            if method == "get":
                result = self._bridge.get(path)
            elif method == "ls":
                result = self._bridge.list_children(path)
            elif method == "post":
                result = self._bridge.post(path)
            elif method == "put":
                result = self._bridge.put(path)
            elif method == "delete":
                result = self._bridge.delete(path)
            else:
                log.write(f"Unsupported method: {method}")
                return

            self._current_data = result
            json_view = self.query_one("#json_view", TextArea)
            json_str = self._format_result(result)
            json_view.load_text(json_str)
            log.write(json_str[:2000])
        except Exception as exc:
            log.write(f"ERROR: {exc}")

    def _parse_command(self, raw: str) -> tuple[str, str]:
        command = raw.strip()
        if not command:
            return ("get", self._runtime.initial_path)

        if command.startswith("/"):
            return ("get", validate_api_path(command))

        parts = command.split(maxsplit=1)
        if len(parts) == 1:
            return (
                "get",
                validate_api_path(parts[0] if parts[0].startswith("/") else f"/{parts[0]}"),
            )

        method = parts[0].lower()
        path = validate_api_path(parts[1])
        return (method, path)

    @staticmethod
    def _format_result(result: object) -> str:
        if result is None:
            return "null"
        if isinstance(result, (dict, list)):
            return json.dumps(result, indent=2, sort_keys=True, default=str)
        return str(result)


def force_terminal_cleanup() -> None:
    """Best-effort terminal cleanup if Textual exits on exception."""
    stream = getattr(sys, "stdout", None)
    if stream is None or not hasattr(stream, "write"):
        return
    if hasattr(stream, "isatty") and not stream.isatty():
        return
    reset = "".join(
        (
            "\x1b[0m",
            "\x1b[?25h",
            "\x1b[?1000l",
            "\x1b[?1002l",
            "\x1b[?1003l",
            "\x1b[?1006l",
            "\x1b[?1015l",
            "\x1b[?2004l",
        )
    )
    try:
        stream.write(reset)
        stream.flush()
    except Exception:
        return

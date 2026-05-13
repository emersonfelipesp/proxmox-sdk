# IDE Support

`proxmox_sdk` ships a [PEP 561](https://peps.python.org/pep-0561/) `py.typed`
marker and includes it in the wheel package data. Editors that read PEP 561,
including VS Code through Pylance, PyCharm, and Pyright on the command line,
resolve types from an installed `proxmox-sdk` without extra configuration.

## VS Code

The repository commits a minimal workspace under `.vscode/` so a fresh clone
gets a working Python IDE on first open. When VS Code prompts to install the
recommended extensions, accept:

- `ms-python.python`
- `ms-python.vscode-pylance`
- `charliermarsh.ruff`

`.vscode/settings.json` points the interpreter to
`${workspaceFolder}/.venv/bin/python`, enables Pylance indexing and import
completions, enables pytest discovery for `tests`, and uses Ruff as the Python
formatter on save. `python.analysis.typeCheckingMode` is set to `basic` to
match `[tool.pyright]` in `pyproject.toml`.

## Type Checking Gates

Two type checkers run over the same source tree:

- `ty` checks `proxmox_sdk` plus `tests` and remains the fast project gate.
- `pyright` checks `proxmox_sdk` with diagnostics aligned to Pylance.

Run them manually with:

```bash
uv run ty check proxmox_sdk tests --output-format concise
uv run pyright proxmox_sdk
```

The `pyright-check` hook sits next to `ty-check` in `.pre-commit-config.yaml`,
so `uv run pre-commit run --all-files` exercises both gates.

## Excluded Paths

Generated bindings and tests are excluded from Pyright to keep the Pylance gate
focused on the importable package surface:

- `proxmox_sdk/generated/**`
- `tests/**`

`ty` still checks `tests` with the repo's existing rule configuration.

## Rule Severity

`[tool.pyright]` downgrades the current typing debt to warnings so diagnostics
remain visible in the editor without failing the pre-commit gate. The warnings
mostly come from dynamic FastAPI route construction, schema dictionaries typed
as `object`, optional dependency imports, and CLI renderable return types.

Fixing those warnings is a separate typing-hardening task. Do not mix it into
unrelated feature work unless the feature directly touches the affected code.

## Consumers

If you install `proxmox-sdk` from PyPI into another project, Pylance and other
PEP 561-aware tools pick up the bundled type hints automatically. The wheel
includes:

- `proxmox_sdk/py.typed`

Hovering public SDK imports such as `ProxmoxSDK` and `SyncProxmoxSDK` resolves
to the package's real type information.

# proxmox-sdk

Schema-driven FastAPI package, Python SDK, and CLI/TUI for Proxmox APIs:
OpenAPI generation, mock data, in-memory CRUD operations, typed service
facades, and real API connections.

**📚 [Full Documentation](https://emersonfelipesp.github.io/proxmox-sdk/)**

## Features

- **Dual Mode**: Mock mode (default) for development, Real mode for production Proxmox integration
- **675 Operations / 444 Endpoints**: Pre-generated Proxmox VE 9.2 API with full OpenAPI schema
- **318 Operations / 246 Endpoints**: Pre-generated Proxmox Datacenter Manager (PDM) API with full OpenAPI schema
- **Mock Data**: Automatically generate mock data for all endpoints with in-memory CRUD
- **Real API Proxy**: Validated proxy to real Proxmox VE API with request/response validation
- **Typed Facades**: PBS, PDM, and Ceph clients for higher-level workflows
- **CLI/TUI**: Generic path commands, configuration profiles, Ceph/PBS/PDM command groups, and Textual TUIs
- **Code Generation**: Automatically crawl Proxmox API Viewer and convert to OpenAPI schema
- **Multi-version Support**: Select multiple Proxmox versions with `latest` mapped to official Proxmox API viewer
- **Swagger Docs**: FastAPI auto-generates OpenAPI documentation at `/docs`

## Supported Proxmox Versions

| Version | Status | Schema directory |
|---|---|---|
| 9.2 | Primary (CI-tested) | `proxmox_sdk/generated/proxmox/9.2/` |
| latest | Alias for 9.2 (CI-tested) | `proxmox_sdk/generated/proxmox/latest/` |
| 9.1.11 | Previous release (CI-tested) | `proxmox_sdk/generated/proxmox/9.1.11/` |

All three schema directories ship in the package and CI exercises them
in parallel via `PROXMOX_MOCK_SCHEMA_VERSION=[latest, 9.2, 9.1.11]`. Older releases
(8.x, 7.x) may still work for endpoints whose shapes have not changed, but they
are no longer in the CI matrix — regenerate locally with
`proxmox-sdk-codegen --version-tag <your-version>` if you need them.

The generated PDM schema also ships in every wheel at
`proxmox_sdk/generated/pdm/latest/openapi.json`. CI and release validation run
all 32 public typed `PDMClient.mock()` read surfaces from the built wheel outside
the source checkout, so editable imports cannot hide missing package data or
PDM response-shape drift. Domain boundaries reject malformed cardinality and
required identifiers with redacted `PDMResponseContractError` failures.

## Installation

```bash
pip install proxmox-sdk

# Optional OpenTelemetry tracing support
pip install proxmox-sdk[otel]
```

## Quick Start

### Mock Mode (Default)

```bash
# Install
pip install proxmox-sdk

# Start server
uvicorn proxmox_sdk.main:app --reload

# View Swagger docs
# Open http://localhost:8000/docs
```

### SDK Direct Usage (No Server Required)

```python
from proxmox_sdk.sdk import ProxmoxSDK

# Async with mock data
async with ProxmoxSDK.mock() as proxmox:
    nodes = await proxmox.nodes.get()

# Or sync (blocking)
with ProxmoxSDK.sync_mock() as proxmox:
    nodes = proxmox.nodes.get()
```

### CLI TUI

```bash
# Install with CLI extras
pip install proxmox-sdk[cli]

# Generic API path commands
proxmox --backend mock get /nodes --json

# Production TUI
pbx tui

# Mock TUI
pbx tui mock

# PDM command group
proxmox --service PDM --host pdm.example.com pdm remote list
proxmox pdm tui mock
```

### PDM Mock Server

```bash
# Start the standalone Proxmox Datacenter Manager mock (default port 8443)
proxmox-sdk-pdm-mock
```

### Real Mode (Connect to Proxmox)

```bash
# Configure credentials
export PROXMOX_API_MODE=real
export PROXMOX_API_URL=https://proxmox.example.com:8006
export PROXMOX_API_TOKEN_ID=user@realm!tokenid
export PROXMOX_API_TOKEN_SECRET=<uuid>

# Start server
uvicorn proxmox_sdk.main:app --reload
```

See the [Quick Start Guide](https://emersonfelipesp.github.io/proxmox-sdk/quickstart/) for more details.

## Documentation

- **[Home](https://emersonfelipesp.github.io/proxmox-sdk/)** - Overview and features
- **[Installation](https://emersonfelipesp.github.io/proxmox-sdk/installation/)** - Installation options (pip, uv, Docker, source)
- **[Quick Start](https://emersonfelipesp.github.io/proxmox-sdk/quickstart/)** - 5-minute getting started guide
- **[SDK Mock Usage](https://emersonfelipesp.github.io/proxmox-sdk/sdk-mock/)** - Using the SDK with mock data (no server required)
- **[CLI and TUI Command Guide](https://emersonfelipesp.github.io/proxmox-sdk/cli/)** - CLI commands, profiles, PDM commands, and TUIs
- **[Proxmox Backup Server](https://emersonfelipesp.github.io/proxmox-sdk/sdk-pbs/)** - Typed PBS facade
- **[Proxmox Datacenter Manager](https://emersonfelipesp.github.io/proxmox-sdk/sdk-pdm/)** - Typed PDM facade and mock server
- **[Ceph](https://emersonfelipesp.github.io/proxmox-sdk/sdk-ceph/)** - PVE Ceph facade and direct provider clients
- **[Mock API](https://emersonfelipesp.github.io/proxmox-sdk/mock-api/)** - Mock mode guide with custom data
- **[Real API](https://emersonfelipesp.github.io/proxmox-sdk/real-api/)** - Real Proxmox integration guide
- **[API Reference](https://emersonfelipesp.github.io/proxmox-sdk/api-reference/)** - Endpoint documentation
- **[Development](https://emersonfelipesp.github.io/proxmox-sdk/development/)** - Contributing guide
- **[IDE Support](https://emersonfelipesp.github.io/proxmox-sdk/ide-support/)** - VS Code, Pylance, and type-checking setup
- **[Architecture](https://emersonfelipesp.github.io/proxmox-sdk/architecture/)** - How it works internally
- **[FAQ](https://emersonfelipesp.github.io/proxmox-sdk/faq/)** - Frequently asked questions

## Environment Variables

### Mock Mode
- `PROXMOX_API_MODE` - Set to "mock" (default) or "real"
- `PROXMOX_MOCK_SCHEMA_VERSION` - Version tag to use (default: "latest")
- `PROXMOX_MOCK_DATA_PATH` - Path to custom mock data file (default: "/etc/proxmox-sdk/mock-data.json")
- `PROXMOX_MOCK_STORE` - Mock state backend: "sqlite" (default), "shared-memory", or "dict"
- `PROXMOX_MOCK_STATE_PATH` - Optional SQLite mock-state database path

### Real Mode
- `PROXMOX_API_MODE` - Set to "real" to enable Proxmox integration
- `PROXMOX_API_URL` - Proxmox server URL (e.g., "https://proxmox.example.com:8006")
- `PROXMOX_API_TOKEN_ID` - API token ID (format: "user@realm!tokenid")
- `PROXMOX_API_TOKEN_SECRET` - API token secret UUID
- `PROXMOX_API_USERNAME` - Username for password auth (format: "user@realm")
- `PROXMOX_API_PASSWORD` - Password for password auth
- `PROXMOX_API_VERIFY_SSL` - Verify SSL certificates (default: true)

### Server
- `HOST` - Host to bind to (default: "0.0.0.0")
- `PORT` - Port to bind to (default: "8000")

### OpenTelemetry Tracing
- `PROXMOX_OTEL_ENABLED` - Enable outbound SDK CLIENT spans and inbound FastAPI SERVER spans (default: false)
- `OTEL_EXPORTER_OTLP_ENDPOINT` - OTLP HTTP collector endpoint (default base endpoint: "http://localhost:4318")
- `OTEL_EXPORTER_OTLP_PROTOCOL` - Must be "http/protobuf" for the bundled HTTP exporter
- `OTEL_EXPORTER_OTLP_HEADERS` - Optional OTLP headers
- `OTEL_SERVICE_NAME` - Service name resource attribute (default: "proxmox-sdk")
- `OTEL_RESOURCE_ATTRIBUTES` - Additional OpenTelemetry resource attributes
- `OTEL_SDK_DISABLED` - Standard OpenTelemetry kill switch; truthy values disable tracing
- `OTEL_TRACES_SAMPLER` - Standard OpenTelemetry trace sampler
- `OTEL_TRACES_EXPORTER` - Set to "otlp" or leave unset for OTLP export; set "none" to disable export

Tracing never records request params, request bodies, auth headers, cookies,
passwords, tickets, CSRF tokens, or API token values as span data.

### PDM Mock Server
- `PROXMOX_PDM_MOCK_HOST` - Host to bind to (default: "0.0.0.0")
- `PROXMOX_PDM_MOCK_PORT` - Port to bind to (default: "8443")
- `PROXMOX_PDM_MOCK_SEED_FILE` - Optional JSON seed file
- `PROXMOX_PDM_MOCK_SCHEMA_VERSION` - Reserved schema tag (default: "1.0")

## Development

```bash
# Install dependencies
uv sync --extra test

# Run tests
pytest

# Run linting
ruff check .
ruff format --check .

# Run type checks
uv run ty check proxmox_sdk tests --output-format concise
uv run pyright proxmox_sdk
```

## IDE Support

Open the repository in VS Code. When prompted, install the recommended
extensions (`ms-python.vscode-pylance`, `ms-python.python`,
`charliermarsh.ruff`). Pylance picks up types from the installed package
automatically because `proxmox_sdk` ships a `py.typed` PEP 561 marker.

Type checking uses two gates: `ty` for fast project checks and `pyright` for
Pylance-compatible diagnostics. Both run at `typeCheckingMode = "basic"`:

```bash
uv run ty check proxmox_sdk tests --output-format concise
uv run pyright proxmox_sdk
```

## Docker

All images are **Alpine-based** (smaller footprint), built from this repository
with **uv** and **`uv.lock`** in a multi-stage Dockerfile. The Python and uv
multi-architecture images are pinned by digest (currently Python 3.13.14 on
Alpine 3.24), direct APK inputs and Granian are exact-versioned, and each
architecture-specific mkcert download is checked against a reviewed SHA256
before it enters an image. Three server variants are published to Docker Hub:

| Variant | Tags | Description |
|---------|------|-------------|
| **Raw** (default) | `latest`, `<version>` | Pure uvicorn, HTTP only. Smallest image. |
| **Nginx** | `latest-nginx`, `<version>-nginx` | nginx terminates HTTPS via mkcert; proxies to uvicorn. |
| **Granian** | `latest-granian`, `<version>-granian` | [Granian](https://github.com/emmett-framework/granian) (Rust ASGI server) with native TLS via mkcert. No nginx. |

Service-specific mock images use `latest-{all,pve,pbs,pdm}` and
`<version>-{all,pve,pbs,pdm}`. Release builds download the project wheel back
from PyPI, verify the served-byte SHA256, and make that exact wheel the only
project payload accepted by those service images. Core and service images are
smoke-tested on both amd64 and arm64 before stable aliases are promoted. The
QEMU and BuildKit helpers are selected by reviewed multi-architecture digests,
not floating helper tags.

OCI manifest digests are the immutable image identities. `sha-<commit>` aliases
are commit traceability tags and can be moved by a registry operator; deployment
records should therefore retain the resolved `sha256:` manifest digest. Each
tested image also produces a CycloneDX inventory. See
[Release evidence and package promotion](docs/release-evidence.md) for the
package-first RC flow, credential boundaries, archive/SBOM-to-manifest binding,
rerun identity rules, and reproducibility limits.

> **Upgrade note:** before v0.0.2, only runtime+mkcert images existed. From v0.0.2+, `latest` is the raw uvicorn image. Pull `latest-nginx` for HTTPS with nginx.

### Raw image (default)

Plain uvicorn on HTTP — the simplest option for local dev or when you put your own proxy in front.

```bash
docker pull emersonfelipesp/proxmox-sdk:latest
docker run -d -p 8000:8000 --name proxmox-sdk emersonfelipesp/proxmox-sdk:latest
```

Build from source:

```bash
docker build -t proxmox-sdk:raw .
docker run -d -p 8000:8000 proxmox-sdk:raw
```

### Nginx image (nginx + mkcert HTTPS + uvicorn)

**nginx** terminates HTTPS on `PORT` (default **8000**) using certificates from [mkcert](https://github.com/FiloSottile/mkcert) and proxies to **uvicorn** on `127.0.0.1:8001`. **supervisord** manages both processes.

```bash
docker pull emersonfelipesp/proxmox-sdk:latest-nginx
docker run -d -p 8443:8000 --name proxmox-sdk-nginx \
  emersonfelipesp/proxmox-sdk:latest-nginx
```

Build from source:

```bash
docker build --target nginx -t proxmox-sdk:nginx .
docker run -d -p 8443:8000 proxmox-sdk:nginx
```

### Granian image (granian + mkcert HTTPS)

[Granian](https://github.com/emmett-framework/granian) is a Rust-based ASGI server with native HTTP/2, WebSocket, and TLS support. This variant eliminates nginx and supervisord — a single granian process handles everything.

```bash
docker pull emersonfelipesp/proxmox-sdk:latest-granian
docker run -d -p 8443:8000 --name proxmox-sdk-granian \
  emersonfelipesp/proxmox-sdk:latest-granian
```

Build from source:

```bash
docker build --target granian -t proxmox-sdk:granian .
docker run -d -p 8443:8000 proxmox-sdk:granian
```

### mkcert environment variables (nginx and granian images)

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Port the server listens on |
| `MKCERT_CERT_DIR` | `/certs` | Directory where certs are stored |
| `MKCERT_EXTRA_NAMES` | — | Extra SANs (commas or spaces), e.g. `proxmox-api.lan,10.0.0.5` |
| `CAROOT` | — | Mount a volume here to persist the local CA across container restarts |
| `APP_MODULE` | `proxmox_sdk.mock_main:app` | ASGI app to run (change to `proxmox_sdk.main:app` for real mode) |

```bash
docker run -d -p 8443:8000 --name proxmox-sdk-tls \
  -e MKCERT_EXTRA_NAMES='myhost.local,192.168.1.10' \
  -e APP_MODULE='proxmox_sdk.main:app' \
  emersonfelipesp/proxmox-sdk:latest-nginx
```

To run a shell instead of starting the server, pass a command (the entrypoint delegates to it):

```bash
docker run --rm emersonfelipesp/proxmox-sdk:latest-nginx sh
```

## License

MIT

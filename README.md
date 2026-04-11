# proxmox-sdk

Schema-driven FastAPI package for Proxmox API: OpenAPI generation, mock data, and in-memory CRUD operations.

**📚 [Full Documentation](https://emersonfelipesp.github.io/proxmox-sdk/)**

## Features

- **Dual Mode**: Mock mode (default) for development, Real mode for production Proxmox integration
- **646 Endpoints**: Pre-generated Proxmox VE 8.1 API with full OpenAPI schema
- **Mock Data**: Automatically generate mock data for all endpoints with in-memory CRUD
- **Real API Proxy**: Validated proxy to real Proxmox VE API with request/response validation
- **Code Generation**: Automatically crawl Proxmox API Viewer and convert to OpenAPI schema
- **Multi-version Support**: Select multiple Proxmox versions with `latest` mapped to official Proxmox API viewer
- **Swagger Docs**: FastAPI auto-generates OpenAPI documentation at `/docs`

## Installation

```bash
pip install proxmox-sdk
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

# Production TUI
pbx tui

# Mock TUI
pbx tui mock
```

### Real Mode (Connect to Proxmox)

```bash
# Configure credentials
export PROXMOX_API_MODE=real
export PROXMOX_URL=https://proxmox.example.com:8006
export PROXMOX_API_TOKEN=PVEAPIToken=user@realm!tokenid=uuid

# Start server
uvicorn proxmox_sdk.main:app --reload
```

See the [Quick Start Guide](https://emersonfelipesp.github.io/proxmox-sdk/quickstart/) for more details.

## Documentation

- **[Home](https://emersonfelipesp.github.io/proxmox-sdk/)** - Overview and features
- **[Installation](https://emersonfelipesp.github.io/proxmox-sdk/installation/)** - Installation options (pip, uv, Docker, source)
- **[Quick Start](https://emersonfelipesp.github.io/proxmox-sdk/quickstart/)** - 5-minute getting started guide
- **[SDK Mock Usage](https://emersonfelipesp.github.io/proxmox-sdk/sdk-mock/)** - Using the SDK with mock data (no server required)
- **[Mock API](https://emersonfelipesp.github.io/proxmox-sdk/mock-api/)** - Mock mode guide with custom data
- **[Real API](https://emersonfelipesp.github.io/proxmox-sdk/real-api/)** - Real Proxmox integration guide
- **[API Reference](https://emersonfelipesp.github.io/proxmox-sdk/api-reference/)** - Endpoint documentation
- **[Development](https://emersonfelipesp.github.io/proxmox-sdk/development/)** - Contributing guide
- **[Architecture](https://emersonfelipesp.github.io/proxmox-sdk/architecture/)** - How it works internally
- **[FAQ](https://emersonfelipesp.github.io/proxmox-sdk/faq/)** - Frequently asked questions

## Environment Variables

### Mock Mode
- `PROXMOX_API_MODE` - Set to "mock" (default) or "real"
- `PROXMOX_MOCK_SCHEMA_VERSION` - Version tag to use (default: "latest")
- `PROXMOX_MOCK_DATA_PATH` - Path to custom mock data file (default: "/etc/proxmox-sdk/mock-data.json")

### Real Mode
- `PROXMOX_API_MODE` - Set to "real" to enable Proxmox integration
- `PROXMOX_URL` - Proxmox server URL (e.g., "https://proxmox.example.com:8006")
- `PROXMOX_API_TOKEN` - API token (recommended, format: "PVEAPIToken=user@realm!tokenid=uuid")
- `PROXMOX_USERNAME` - Username (fallback, format: "user@realm")
- `PROXMOX_PASSWORD` - Password (fallback)
- `PROXMOX_API_VERIFY_SSL` - Verify SSL certificates (default: true)

### Server
- `HOST` - Host to bind to (default: "0.0.0.0")
- `PORT` - Port to bind to (default: "8000")

## Development

```bash
# Install dependencies
uv sync --extra test

# Run tests
pytest

# Run linting
ruff check .
ruff format --check .
```

## Docker

All images are **Alpine-based** (smaller footprint), built from this repository with **uv** and **`uv.lock`** in a multi-stage Dockerfile. Three variants are published to Docker Hub:

| Variant | Tags | Description |
|---------|------|-------------|
| **Raw** (default) | `latest`, `<version>` | Pure uvicorn, HTTP only. Smallest image. |
| **Nginx** | `latest-nginx`, `<version>-nginx` | nginx terminates HTTPS via mkcert; proxies to uvicorn. |
| **Granian** | `latest-granian`, `<version>-granian` | [Granian](https://github.com/emmett-framework/granian) (Rust ASGI server) with native TLS via mkcert. No nginx. |

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

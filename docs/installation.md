# Installation

## Requirements

- Python 3.11 or higher
- pip or uv package manager

---

## Install from PyPI

The easiest way to install proxmox-sdk:

```bash
pip install proxmox-sdk
```

Or using `uv` (recommended for faster installation):

```bash
uv pip install proxmox-sdk
```

---

## Install from Source

For development or to get the latest unreleased features:

```bash
# Clone the repository
git clone https://github.com/emersonfelipesp/proxmox-sdk.git
cd proxmox-sdk

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

---

## Docker Installation

All Docker images are **Alpine-based** (smaller footprint). Three variants are available:

| Variant | Tags | Description |
|---------|------|-------------|
| **Raw** (default) | `latest`, `<version>` | Pure uvicorn, HTTP only. Smallest image. |
| **Nginx** | `latest-nginx`, `<version>-nginx` | nginx terminates HTTPS via mkcert; proxies to uvicorn. |
| **Granian** | `latest-granian`, `<version>-granian` | Granian (Rust ASGI server) with native TLS via mkcert. |

### Raw image — HTTP only (default)

Simplest option. No proxy in front, plain HTTP. Ideal for local development or behind your own reverse proxy.

```bash
docker pull emersonfelipesp/proxmox-sdk:latest
docker run -d -p 8000:8000 --name proxmox-sdk emersonfelipesp/proxmox-sdk:latest
```

Service URL:

- <http://127.0.0.1:8000>

### Nginx image — HTTPS with mkcert

nginx terminates HTTPS using auto-generated [mkcert](https://github.com/FiloSottile/mkcert) certificates and proxies to uvicorn inside the container.

```bash
docker pull emersonfelipesp/proxmox-sdk:latest-nginx
docker run -d -p 8443:8000 --name proxmox-sdk-nginx \
  emersonfelipesp/proxmox-sdk:latest-nginx
```

Service URL:

- <https://127.0.0.1:8443> (self-signed, trusted on the container host)

### Granian image — HTTPS with mkcert (no nginx)

[Granian](https://github.com/emmett-framework/granian) is a Rust-based ASGI server with native TLS and HTTP/2. A single process handles everything — no nginx or supervisord required.

```bash
docker pull emersonfelipesp/proxmox-sdk:latest-granian
docker run -d -p 8443:8000 --name proxmox-sdk-granian \
  emersonfelipesp/proxmox-sdk:latest-granian
```

Service URL:

- <https://127.0.0.1:8443>

### mkcert environment variables

Available for the `nginx` and `granian` images:

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8000` | Port the server listens on |
| `MKCERT_CERT_DIR` | `/certs` | Directory where certificates are stored |
| `MKCERT_EXTRA_NAMES` | — | Extra SANs (comma or space separated), e.g. `proxmox-api.lan,10.0.0.5` |
| `CAROOT` | — | Mount a volume here to persist the local CA across restarts |
| `APP_MODULE` | `proxmox_sdk.mock_main:app` | ASGI app (change to `proxmox_sdk.main:app` for real mode) |

Example with extra SANs:

```bash
docker run -d -p 8443:8000 --name proxmox-sdk-tls \
  -e MKCERT_EXTRA_NAMES='myhost.local,192.168.1.10' \
  emersonfelipesp/proxmox-sdk:latest-nginx
```

Example with real Proxmox mode:

```bash
docker run -d -p 8443:8000 --name proxmox-sdk-real \
  -e APP_MODULE='proxmox_sdk.main:app' \
  -e PROXMOX_API_MODE=real \
  -e PROXMOX_URL=https://pve.example.com:8006 \
  -e PROXMOX_API_TOKEN=PVEAPIToken=user@pam!mytoken=your-secret \
  emersonfelipesp/proxmox-sdk:latest-granian
```

### Build from source

```bash
git clone https://github.com/emersonfelipesp/proxmox-sdk.git
cd proxmox-sdk

docker build -t proxmox-sdk:raw .                          # raw (default)
docker build --target nginx -t proxmox-sdk:nginx .         # nginx
docker build --target granian -t proxmox-sdk:granian .     # granian
```

---

## Verify Installation

```bash
# Check installed version
python -c "import proxmox_sdk; print(proxmox_sdk.__version__)"

# Run the mock API
proxmox-sdk-mock
```

Visit `http://localhost:8000/docs` to confirm the API is running.

---

## Optional Dependencies

### For Development

```bash
pip install proxmox-sdk[test]
```

Includes:
- `pytest` - Testing framework
- `httpx` - HTTP client for testing
- `playwright` - Browser automation for API Viewer crawling

### For Documentation

```bash
pip install proxmox-sdk[docs]
```

Includes:
- `mkdocs` - Documentation generator
- `mkdocs-material` - Material theme

---

## Next Steps

- **[Quick Start Guide →](quickstart.md)**
- **[Mock API Mode →](mock-api.md)**
- **[Real API Mode →](real-api.md)**

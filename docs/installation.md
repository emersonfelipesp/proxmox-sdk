# Installation

## Requirements

- Python 3.11 or higher
- pip or uv package manager

---

## Install from PyPI

The easiest way to install proxmox-openapi:

```bash
pip install proxmox-openapi
```

Or using `uv` (recommended for faster installation):

```bash
uv pip install proxmox-openapi
```

---

## Install from Source

For development or to get the latest unreleased features:

```bash
# Clone the repository
git clone https://github.com/emersonfelipesp/proxmox-openapi.git
cd proxmox-openapi

# Install with uv (recommended)
uv sync

# Or with pip
pip install -e .
```

---

## Docker Installation

Run the pre-built Docker image:

```bash
# Pull the image
docker pull ghcr.io/emersonfelipesp/proxmox-openapi:latest

# Run in mock mode (default)
docker run -p 8000:8000 ghcr.io/emersonfelipesp/proxmox-openapi:latest

# Run in real mode
docker run -p 8000:8000 \
  -e PROXMOX_API_MODE=real \
  -e PROXMOX_API_URL=https://pve.example.com:8006 \
  -e PROXMOX_API_TOKEN_ID=user@pam!mytoken \
  -e PROXMOX_API_TOKEN_SECRET=your-secret \
  ghcr.io/emersonfelipesp/proxmox-openapi:latest
```

---

## Verify Installation

```bash
# Check installed version
python -c "import proxmox_openapi; print(proxmox_openapi.__version__)"

# Run the mock API
proxmox-openapi-mock
```

Visit `http://localhost:8000/docs` to confirm the API is running.

---

## Optional Dependencies

### For Development

```bash
pip install proxmox-openapi[test]
```

Includes:
- `pytest` - Testing framework
- `httpx` - HTTP client for testing
- `playwright` - Browser automation for API Viewer crawling

### For Documentation

```bash
pip install proxmox-openapi[docs]
```

Includes:
- `mkdocs` - Documentation generator
- `mkdocs-material` - Material theme

---

## Next Steps

- **[Quick Start Guide →](quickstart.md)**
- **[Mock API Mode →](mock-api.md)**
- **[Real API Mode →](real-api.md)**

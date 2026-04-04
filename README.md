# proxmox-openapi

Schema-driven FastAPI package for Proxmox API: OpenAPI generation, mock data, and in-memory CRUD operations.

## Features

- **Crawler of Proxmox API Viewer**: Automatically crawl Proxmox API Viewer and convert to OpenAPI schema
- **Mock Data**: Automatically generate mock data for all endpoints
- **In-Memory CRUD**: Allow users to modify mock data through create, update, and patch operations
- **Multi-version Support**: Select multiple Proxmox versions with `latest` mapped to official Proxmox API viewer
- **Swagger Docs**: FastAPI auto-generates OpenAPI documentation at `/docs`

## Installation

```bash
pip install proxmox-openapi
```

## Quick Start

### Full API Server

```bash
proxmox-openapi
```

This starts the FastAPI server at `http://localhost:8000` with Swagger docs at `/docs`.

### Mock API Server

```bash
proxmox-openapi-mock
```

This starts the standalone mock API server.

## API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /version` - Version info
- `GET /docs` - Swagger documentation
- `POST /codegen/generate` - Generate OpenAPI schema from Proxmox API Viewer
- `GET /codegen/openapi` - Get generated OpenAPI schema
- `GET /codegen/versions` - List available versions
- `GET /versions/` - List available Proxmox OpenAPI versions
- `GET /mock/` - Mock API root (when using mock server)

## Environment Variables

- `PROXMOX_MOCK_SCHEMA_VERSION` - Specify which version tag to use for mock (default: "latest")
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

```bash
# Build the image
docker build -t proxmox-openapi .

# Run the container
docker run -p 8000:8000 proxmox-openapi
```

## License

MIT
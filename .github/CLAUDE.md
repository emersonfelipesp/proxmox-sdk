# .github/ Directory Guide

## Purpose

GitHub Actions CI/CD workflows for `proxmox-sdk`. All workflows live under `.github/workflows/`.

## Workflow Index

| File | Trigger | What it does |
|------|---------|--------------|
| `ci.yml` | Push / PR to any branch | Lint (ruff), compile, import smoke checks, run `tests/` with coverage |
| `ci.yml` docker-images | Push to main/testing or Release published | Builds and pushes Docker images to Docker Hub (dev or release tags) |
| `docs.yml` | Push to `main` | Builds MkDocs site and deploys to GitHub Pages |
| `docker-hub-publish.yml` | Called by CI | Builds three Alpine-based Docker images: raw (uvicorn), nginx (nginx+mkcert+uvicorn), granian (granian+mkcert); pushes under both `proxmox-sdk` (primary) and `proxmox-openapi` (alternate) names |
| `publish-testpypi.yml` | GitHub Release published | Validates release metadata, publishes both `proxmox-sdk` and `proxmox-openapi` to TestPyPI, validates across Python 3.11–3.13, publishes both to PyPI |
| `release-docker-verify.yml` | Release published | Post-release smoke test of all six published Docker image variants (raw/nginx/granian × proxmox-sdk/proxmox-openapi) |

## Dual-Name Publishing

The same package is published under two names on every release:

- **PyPI/TestPyPI**: `proxmox-sdk` (primary) and `proxmox-openapi` (alternate)
- **Docker Hub**: `emersonfelipesp/proxmox-sdk` (primary) and `emersonfelipesp/proxmox-openapi` (alternate)

**How it works**: `pyproject.toml` always has `name = "proxmox-sdk"`. During the `prepare-release` job, after building the `proxmox-sdk` dist, the workflow `sed`s the name to `proxmox-openapi`, rebuilds, and uploads both artifact sets. The internal Python package (`proxmox_sdk`) is unchanged. For Docker, both image names are added as extra tags on the same build — no extra build time.

## CI Job Dependencies

```
ci.yml
├── lint
├── syntax
├── test
└── docker-images (on main/testing push OR release)
    └── calls docker-hub-publish.yml (parallel: docker-raw, docker-nginx, docker-granian)
```

## Docker Image Tags

### Release Mode (GitHub Release)
| Image | Tags |
|-------|------|
| Raw | `<version>`, `latest`, `sha-<sha>` |
| Nginx | `<version>-nginx`, `latest-nginx`, `sha-<sha>-nginx` |
| Granian | `<version>-granian`, `latest-granian`, `sha-<sha>-granian` |

### Dev Mode (main/testing branch push)
| Image | Tags |
|-------|------|
| Raw | `dev`, `sha-<sha>` |
| Nginx | `dev-nginx`, `sha-<sha>-nginx` |
| Granian | `dev-granian`, `sha-<sha>-granian` |

## Key Rules

- The `uv.lock` at the repo root must stay in sync with `pyproject.toml` because CI runs `uv sync --frozen`.
- Release workflows validate that the `pyproject.toml` version matches the Git tag before publishing.
- Do not add secrets to workflow files — use repository secrets (`PYPI_TOKEN`, `DOCKERHUB_TOKEN`, etc.).

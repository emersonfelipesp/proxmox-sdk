# .github/ Directory Guide

## Workspace Context

This file lives at `/root/personal-context/nmulticloud-context/proxmox-sdk/.github/CLAUDE.md` inside the `personal-context` workspace.
Workspace guidance: `/root/personal-context/CLAUDE.md`.
Per-repo deep-dive: `/root/personal-context/claude-reference/proxmox-sdk.md`.
Submodule layout and cross-repo links: `/root/personal-context/claude-reference/dependency-map.md`.

---

## Purpose

GitHub Actions CI/CD workflows for `proxmox-sdk`. All workflows live under `.github/workflows/`.

## Workflow Index

| File | Trigger | What it does |
|------|---------|--------------|
| `ci.yml` | Push / PR to any branch | Lint (ruff), compile, import smoke checks, run `tests/` with coverage across all schema versions |
| `ci.yml` docker-images | Push to main/testing or Release published | Builds and pushes Docker images to Docker Hub (dev or release tags) |
| `docs.yml` | Push to `main` | Builds MkDocs site and deploys to GitHub Pages |
| `docker-hub-publish.yml` | Called by CI | Builds three Alpine-based Docker images: raw (uvicorn), nginx (nginx+mkcert+uvicorn), granian (granian+mkcert) |
| `publish-testpypi.yml` | GitHub Release published | Validates release metadata, publishes `proxmox_sdk` to TestPyPI, validates install across Python 3.11–3.13 × all schema versions, publishes to PyPI |
| `schema-update.yml` | Manual (`workflow_dispatch`) or weekly cron (Monday 03:00 UTC) | Detects upstream Proxmox API drift, runs codegen for a new version tag, verifies SHA integrity, opens a PR with a generated schema update |
| `release-docker-verify.yml` | Release published | Post-release smoke test of all three published Docker images |

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

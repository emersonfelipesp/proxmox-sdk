# docker/ Directory Guide — AGENTS.md Mirror

This file mirrors the sibling `CLAUDE.md` guidance for agents that read `AGENTS.md`. Treat `CLAUDE.md` as the source material; the content below preserves the current guide.

## Source

@CLAUDE.md

---

# docker/ Directory Guide

## Workspace Context

This file lives at `/root/personal-context/nmulticloud-context/proxmox-sdk/docker/CLAUDE.md` inside the `personal-context` workspace.
Workspace guidance: `/root/personal-context/CLAUDE.md`.
Per-repo deep-dive: `/root/personal-context/claude-reference/proxmox-sdk.md`.
Submodule layout and cross-repo links: `/root/personal-context/claude-reference/dependency-map.md`.

---

## Purpose

Container runtime configuration for the `proxmox-sdk` service. This directory holds nginx config templates, supervisord process configs, and shell entrypoints used by the multi-stage `Dockerfile` at the repo root.

## Files

| Path | Role |
|------|------|
| `nginx/proxmox-sdk-https.conf.template` | nginx HTTPS site config template (used by the nginx image) |
| `supervisor/supervisord.conf` | supervisord global config |
| `supervisor/proxmox-sdk.conf` | supervisord program definition — runs uvicorn on `127.0.0.1:8001` and nginx |
| `entrypoint-nginx.sh` | Entrypoint for the nginx image — generates mkcert certs, configures nginx, starts supervisord |
| `entrypoint-granian.sh` | Entrypoint for the granian image — generates mkcert certs, converts key to PKCS#8, starts granian |

## Dockerfile Overview

The `Dockerfile` at the repo root uses six functional stages plus a final raw alias:

1. **builder** — installs the locked, non-editable project plus exact Granian
   into `/app/.venv` (reviewed Python 3.13.14/Alpine 3.24 multi-arch digest)
2. **runtime-base** — minimal Alpine Python image with the virtualenv copied in
3. **raw** (default) — pure uvicorn, no proxy; `docker build .` produces this image
4. **nginx** — extends raw; adds nginx + supervisor + mkcert, HTTPS-only
5. **granian** — extends runtime-base; adds granian + mkcert, HTTPS-only via granian's native TLS
6. **pypi-raw** — installs hash-locked dependencies and the exact wheel bytes
   downloaded back from PyPI for all/pve/pbs/pdm service images

## Image Variants

| Stage | Tags | Protocol | Server |
|-------|------|----------|--------|
| `raw` | `latest`, `<version>` | HTTP | uvicorn on `0.0.0.0:PORT` |
| `nginx` | `latest-nginx`, `<version>-nginx` | HTTPS | nginx → uvicorn on `127.0.0.1:8001` |
| `granian` | `latest-granian`, `<version>-granian` | HTTPS | granian on `0.0.0.0:PORT` |

## Key Notes

- `supervisor/proxmox-sdk.conf` runs the app via uvicorn — update this if the ASGI entry point changes.
- The nginx image always uses HTTPS; there is no HTTP-only nginx variant.
- The granian image requires the TLS key in PKCS#8 format; `entrypoint-granian.sh` converts it automatically with `openssl pkcs8`.
- For Let's Encrypt / production TLS, configure nginx externally with cert volume mounts.
- `TARGETARCH` build arg (set by BuildKit) is used instead of `dpkg --print-architecture` for Alpine compatibility when downloading the mkcert binary.
- Python and uv images are pinned by reviewed multi-architecture digests. uv and
  Granian and every direct APK input are exact-versioned, and mkcert has an
  architecture-specific SHA256 gate. Update the version, index digest, APK
  versions, and checksums together.
- The source-built runtime uses `uv sync --locked --no-dev --no-editable`. The
  PyPI-backed service image exports hash-locked dependencies, verifies
  `PROXMOX_SDK_WHEEL_SHA256`, installs that local served-byte wheel with
  `--no-deps`, and confirms the installed version.
- Every core and service image is built and run on amd64 and arm64 before
  promotion, and each tested archive has a CycloneDX inventory. Registry jobs
  stage candidates from those archives and promote aliases only by OCI digest.
- QEMU and BuildKit helpers are digest-pinned. Candidate staging rejects a
  platform or provenance-label mismatch and records archive/SBOM hashes beside
  the matching per-architecture registry manifest digest.
- `sha-<commit>` is a commit traceability tag, not an immutable identity. Record
  the resolved OCI manifest `sha256:` digest for deployment and rollback.
- Default `APP_MODULE` is `proxmox_sdk.mock_main:app` (mock mode). Change to `proxmox_sdk.main:app` for real Proxmox integration.

## Alpine Migration Notes (v0.0.2)

Before v0.0.2, images were based on `python:3.13-slim-bookworm` (Debian). The v0.0.2 migration to Alpine achieves:

- **~65% size reduction** (from ~150-200MB to ~60-70MB compressed for raw variant)
- Multi-variant architecture (raw/nginx/granian instead of runtime/mkcert)
- Improved build caching with separate GHA cache scopes per variant
- Alpine-specific compatibility fixes:
  - `apk add` instead of `apt-get`
  - `chgrp nginx` instead of `chgrp www-data`
  - `$TARGETARCH` instead of `dpkg --print-architecture`
  - `build-base` for C extension compilation (httptools, uvloop)

# Build dependencies and the app into a virtualenv with uv from the checked-out repo.
# The index digest is multi-architecture (amd64 + arm64 among others), so every
# supported build resolves the reviewed Python 3.13.14 / Alpine 3.24 image.
FROM python:3.13.14-alpine3.24@sha256:399babc8b49529dabfd9c922f2b5eea81d611e4512e3ed250d75bd2e7683f4b0 AS builder

WORKDIR /app

ARG SOURCE_DATE_EPOCH=0

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=never \
    SOURCE_DATE_EPOCH=${SOURCE_DATE_EPOCH}

# build-base ensures C extensions (httptools, uvloop, etc.) can compile if no
# musllinux wheel is available for the target arch. Direct APK inputs are
# exact-versioned against the reviewed Alpine 3.24 repositories.
RUN apk add --no-cache \
    build-base=0.5-r4 \
    curl=8.21.0-r0

COPY --from=ghcr.io/astral-sh/uv:0.11.28@sha256:0f36cb9361a3346885ca3677e3767016687b5a170c1a6b88465ec14aefec90aa /uv /usr/local/bin/uv

# Download mkcert in builder layer
ARG MKCERT_VERSION=1.4.4
ARG TARGETARCH
RUN case "${TARGETARCH}" in \
      amd64) mkcert_sha256="6d31c65b03972c6dc4a14ab429f2928300518b26503f58723e532d1b0a3bbb52" ;; \
      arm64) mkcert_sha256="b98f2cc69fd9147fe4d405d859c57504571adec0d3611c3eefd04107c7ac00d0" ;; \
      *) echo "Unsupported mkcert target architecture: ${TARGETARCH}" >&2; exit 1 ;; \
    esac \
 && curl --fail --show-error --silent --location \
    --output /usr/local/bin/mkcert \
    "https://github.com/FiloSottile/mkcert/releases/download/v${MKCERT_VERSION}/mkcert-v${MKCERT_VERSION}-linux-${TARGETARCH}" \
 && actual_sha256="$(sha256sum /usr/local/bin/mkcert)" \
 && actual_sha256="${actual_sha256%% *}" \
 && test "${actual_sha256}" = "${mkcert_sha256}" \
 && chmod 0755 /usr/local/bin/mkcert

# Build from the local repository so the image always matches the checked-out commit.
COPY README.md pyproject.toml uv.lock ./
COPY proxmox_sdk ./proxmox_sdk

RUN uv sync \
    --locked \
    --no-dev \
    --extra granian \
    --no-editable

# Application tree + venv only (shared by all runtime images).
FROM python:3.13.14-alpine3.24@sha256:399babc8b49529dabfd9c922f2b5eea81d611e4512e3ed250d75bd2e7683f4b0 AS runtime-base

# Create a non-root user
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

ARG APP_MODULE=proxmox_sdk.mock_main:app

ENV PATH="/app/.venv/bin:$PATH" \
    PORT=8000 \
    PYTHONUNBUFFERED=1 \
    APP_MODULE=${APP_MODULE}

# The code in proxmox_sdk uses main:create_app
# We use main:app (which is app = create_app()) to avoid factory issues.

COPY --from=builder --chown=appuser:appgroup /app/.venv /app/.venv

RUN mkdir -p /app/scripts && chown appuser:appgroup /app/scripts

EXPOSE 8000

# Default image: raw uvicorn, no proxy, HTTP only. Smallest possible image.
FROM runtime-base AS raw

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:${PORT:-8000}/health || exit 1

CMD ["sh", "-c", "exec uvicorn ${APP_MODULE} --host 0.0.0.0 --port ${PORT:-8000}"]

# nginx image: nginx terminates HTTPS with mkcert certs, proxies to uvicorn on 127.0.0.1:8001.
# Extra SANs: MKCERT_EXTRA_NAMES. Persist CA: CAROOT + volume.
FROM raw AS nginx

USER root

RUN apk add --no-cache \
    nginx=1.30.4-r1 \
    supervisor=4.3.0-r1 \
    ca-certificates=20260611-r0 \
    nss-tools=3.124-r0 \
 && rm -f /etc/nginx/conf.d/default.conf

COPY --from=builder /usr/local/bin/mkcert /usr/local/bin/mkcert
COPY docker/nginx/proxmox-sdk-https.conf.template /etc/proxmox-sdk/nginx-https.conf.template
COPY docker/nginx/proxmox-sdk-map.conf /etc/nginx/http.d/proxmox-sdk-map.conf
COPY docker/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY docker/supervisor/proxmox-sdk.conf /etc/supervisor/conf.d/proxmox-sdk.conf
COPY docker/entrypoint-nginx.sh /usr/local/bin/docker-entrypoint-nginx.sh

RUN chmod +x /usr/local/bin/docker-entrypoint-nginx.sh \
 && mkdir -p /certs /var/log/supervisor /var/run/supervisor /var/lib/nginx /var/log/nginx /var/run/nginx /etc/nginx/conf.d /etc/nginx/http.d \
 && chown -R appuser:appgroup /certs /var/log/supervisor /var/run/supervisor /etc/proxmox-sdk /etc/supervisor /var/lib/nginx /var/log/nginx /var/run/nginx /etc/nginx/conf.d /etc/nginx/http.d \
 && sed -i 's/user nginx;/#user nginx;/' /etc/nginx/nginx.conf \
 && sed -i 's/pid \/run\/nginx.pid;/pid \/var\/run\/nginx\/nginx.pid;/' /etc/nginx/nginx.conf \
 && chmod -R 0755 /var/lib/nginx /var/log/nginx /var/run/nginx /etc/nginx/conf.d /etc/nginx/http.d

ENV MKCERT_CERT_DIR=/certs

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider --no-check-certificate https://127.0.0.1:8000/health || exit 1

ENTRYPOINT ["/usr/local/bin/docker-entrypoint-nginx.sh"]
CMD []

# granian image: granian ASGI server with native TLS via mkcert. No nginx, no supervisor.
# Smaller than the nginx image; single process handles TLS + HTTP/2 + WebSockets.
FROM runtime-base AS granian

USER root

RUN apk add --no-cache \
    ca-certificates=20260611-r0 \
    nss-tools=3.124-r0 \
    openssl=3.5.7-r0

COPY --from=builder /usr/local/bin/mkcert /usr/local/bin/mkcert
COPY docker/entrypoint-granian.sh /usr/local/bin/docker-entrypoint-granian.sh

RUN chmod +x /usr/local/bin/docker-entrypoint-granian.sh \
 && mkdir -p /certs \
 && chown -R appuser:appgroup /certs

ENV MKCERT_CERT_DIR=/certs

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider --no-check-certificate https://127.0.0.1:${PORT:-8000}/health || exit 1

ENTRYPOINT ["/usr/local/bin/docker-entrypoint-granian.sh"]
CMD []

# pypi-raw: minimal Alpine image that installs the wheel downloaded back from
# PyPI and verified byte-for-byte by the release workflow. Used by the
# service-specific mock containers published after a PyPI release.
# Required build args:
#   PROXMOX_SDK_VERSION      — exact PyPI version to verify after installation
#   PROXMOX_SDK_WHEEL        — basename of the verified wheel under dist/
#   PROXMOX_SDK_WHEEL_SHA256 — SHA256 computed from the served PyPI bytes
#   PROXMOX_MOCK_SERVICE — service variant baked into the image (default: all)
FROM python:3.13.14-alpine3.24@sha256:399babc8b49529dabfd9c922f2b5eea81d611e4512e3ed250d75bd2e7683f4b0 AS pypi-raw

ARG PROXMOX_SDK_VERSION
ARG PROXMOX_SDK_WHEEL
ARG PROXMOX_SDK_WHEEL_SHA256
ARG PROXMOX_MOCK_SERVICE=all

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

ENV PATH="/app/.venv/bin:$PATH" \
    PORT=8000 \
    PYTHONUNBUFFERED=1 \
    APP_MODULE=proxmox_sdk.mock_main:app \
    PROXMOX_MOCK_SERVICE=${PROXMOX_MOCK_SERVICE}

COPY --from=ghcr.io/astral-sh/uv:0.11.28@sha256:0f36cb9361a3346885ca3677e3767016687b5a170c1a6b88465ec14aefec90aa /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock /tmp/proxmox-sdk-lock/
COPY dist/ /tmp/proxmox-sdk-dist/

RUN test -n "${PROXMOX_SDK_VERSION}" \
 && case "${PROXMOX_SDK_WHEEL}" in ""|*[!A-Za-z0-9._-]*) echo "Unsafe wheel filename" >&2; exit 1 ;; esac \
 && printf '%s' "${PROXMOX_SDK_WHEEL_SHA256}" | grep -Eq '^[0-9a-f]{64}$' \
 && test -f "/tmp/proxmox-sdk-dist/${PROXMOX_SDK_WHEEL}" \
 && printf '%s  %s\n' "${PROXMOX_SDK_WHEEL_SHA256}" "/tmp/proxmox-sdk-dist/${PROXMOX_SDK_WHEEL}" \
      | sha256sum -c - \
 && cd /tmp/proxmox-sdk-lock \
 && uv --quiet export \
      --locked \
      --no-dev \
      --no-emit-project \
      --format requirements-txt \
      --output-file /tmp/proxmox-sdk-requirements.txt \
 && uv venv /app/.venv \
 && uv --no-config pip install \
      --python /app/.venv/bin/python \
      --require-hashes \
      --no-cache \
      --requirements /tmp/proxmox-sdk-requirements.txt \
 && uv --no-config pip install \
      --python /app/.venv/bin/python \
      --no-cache \
      --no-deps \
      "/tmp/proxmox-sdk-dist/${PROXMOX_SDK_WHEEL}" \
 && /app/.venv/bin/python -c \
      'import importlib.metadata as m, sys; actual = m.version("proxmox-sdk"); expected = sys.argv[1]; sys.exit(0 if actual == expected else f"installed {actual}, expected {expected}")' \
      "${PROXMOX_SDK_VERSION}" \
 && rm -rf /tmp/proxmox-sdk-lock /tmp/proxmox-sdk-dist /tmp/proxmox-sdk-requirements.txt

EXPOSE 8000

USER appuser

HEALTHCHECK --interval=30s --timeout=30s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://127.0.0.1:${PORT:-8000}/health || exit 1

CMD ["sh", "-c", "exec uvicorn ${APP_MODULE} --host 0.0.0.0 --port ${PORT:-8000}"]

# `docker build .` without --target uses the raw (uvicorn-only) image.
FROM raw

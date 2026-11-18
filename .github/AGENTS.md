# .github/ Directory Guide

## Workspace Context

This file lives at `/root/personal-context/nmulticloud-context/proxmox-sdk/.github/CLAUDE.md` inside the `personal-context` workspace.
Workspace guidance: `/root/personal-context/CLAUDE.md`.
Per-repo deep-dive: `/root/personal-context/claude-reference/proxmox-sdk.md`.
Submodule layout and cross-repo links: `/root/personal-context/claude-reference/dependency-map.md`.

---

## Purpose

GitHub Actions CI/CD workflows for `proxmox-sdk`. All workflows live under `.github/workflows/`.

Third-party actions are pinned to reviewed full commit SHAs. Python build tools
and uv are exact-versioned; package jobs verify `uv.lock`, build twice under the
event commit's `SOURCE_DATE_EPOCH`, and check out the exact protected event SHA.
Update an action or tool only by reviewing and recording the new release commit.
Gitea feature CI is defined in `.gitea/workflows/ci.yml` and mirrors the
secret-free GitHub review policy, but it is not authoritative until operators
provision isolated PR runners and required branch checks. The package-of-record
workflow only builds and attests on `ci-untrusted-python312` with no package
authority. A separately installed host verifier rebuilds and byte-compares the
exact tag before root-sealing a handoff; only a separate publisher process can
read the systemd package credential.

## Workflow Index

| File | Trigger | What it does |
|------|---------|--------------|
| `ci.yml` | Push / PR to the existing branch filters | Lint, compile/import, wheel contracts, complete browser-enabled schema tests, read-only docs, and an always-run complete summary |
| `ci.yml` docker-images | Push to main/testing | Builds/tests without credentials, stages digest-addressed candidates, then promotes `dev` and commit-traceability tags |
| `docs.yml` | Push to `main` | Builds MkDocs site and deploys to GitHub Pages |
| `docker-hub-publish.yml` | Called by CI / release / manual | Builds and smokes raw/nginx/granian on amd64+arm64 without secrets, emits SBOMs, stages candidates in a protected job, and returns manifest digests |
| `publish-testpypi.yml` | `v*rc*`, GitHub Release, or manual | Reproducible build, protected TestPyPI/PyPI publication, served-byte verification, hash-bound service images, and one all-image stable promotion fan-in |
| `schema-update.yml` | Manual (`workflow_dispatch`) or weekly cron (Monday 03:00 UTC) | Detects upstream Proxmox API drift, runs codegen for a new version tag, verifies SHA integrity, opens a PR with a generated schema update |
| `release-docker-verify.yml` | Successful release workflow | Confirms alias digests and smokes core + all/pve/pbs/pdm images on amd64 and arm64 |
| `.gitea/workflows/ci.yml` | Push / PR to `main` or `testing` | Read-only Ruff/type/syntax, three-schema regression, strict docs, and installed-wheel gates on an isolated untrusted runner |
| `.gitea/workflows/publish-package.yml` | Protected `v*` tag | Builds, attests, and uploads a credential-free package candidate for external rebuild/verification and publication |

## CI Job Dependencies

Public browser tests use `ubuntu-24.04` and install the exact locked Chromium
with the official `--with-deps` route on the disposable hosted runner. Keep
every full schema command and original browser assertion and deadline. The
separate read-only docs job reuses docgen and strict-build checks without a
deployment command. The always-run summary requires every quality job and the
expected Docker disposition, including failures, cancellations, and skips.

The optional non-secret repository variable `CI_QUALIFICATION_ONLY` suppresses
only CI Docker publication and the legacy documentation writer when its value
compares equal to `true` under GitHub's case-insensitive string comparison.
The controlled qualification uses the literal `true`. An absent value preserves
normal future publication. It does not disable read-only quality. A controlled
main qualification must retain
explicit terminal skipped-writer evidence before restoring the variable to its
previous absent state. Do not change secrets, Pages mode, release workflows, or
writer inputs to obtain qualification.

The Gitea schema matrix prepares Chromium in a fresh job-private directory.
`tools/prepare_ci_chromium.py` accepts only an unprivileged Debian 12 amd64
job and locked Playwright 1.58.0. It uses the preinstalled root-controlled
Debian archive keyring, isolated APT configuration/state/status/cache, signed
metadata, download-only dependency resolution, and `dpkg-deb --extract`.
It copies the public host dpkg status into private state and reinstalls only
the fixed top-level library packages into the download cache. It refuses core
libc/loader archives before any extraction, preserving the running host ABI.
Every downloaded archive retains Package, Version, Architecture, and SHA-256
in the job log and an inventory artifact. It never installs packages or runs
package scripts. The workflow installs the
locked Chromium revision 1208 into a private browser path and supplies private
library paths to the unchanged full schema suite. An unsupported host, missing
keyring, failed acquisition, or missing browser fails the job; an empty browser
cache must never substitute for the three real browser security tests.
The separately validated `fonts-liberation` entry from locked `nativeDeps.tools`
is acquired in the same signed transaction. A fixed private Fontconfig file
points only at its extracted fonts and a private cache. Fontconfig environment
variables exist only on the original regression step. Do not use host font
configuration, add font selectors, or weaken the navigation visibility check.

The `schema-update.yml` regeneration job uses `ubuntu-24.04` because locked
Playwright 1.58.0 supports that OS and rejects Ubuntu 26.04. Keep its browser,
dependency lock, and command bodies unchanged when maintaining this runner pin.
Detection and PR creation retain their existing runner labels. The workflow's
final job can push a schema branch and open a PR; a full dispatch requires the
applicable source-promotion and write authorization. This OS pin does not prove
hosted recovery or resolve the separate required-browser security lane.

```
ci.yml
├── lint
├── syntax
├── package (build + metadata + installed-wheel PVE/PDM contracts)
├── test
└── docker-images (main/testing push only)
    └── build/smoke 3 variants × 2 arches → candidate manifests → dev aliases

.gitea/workflows/ci.yml
├── static (workflow policy + Ruff + ty + Pyright)
├── syntax (compileall + public import contracts)
├── schema-tests (latest + 9.2 + 9.1.11)
└── docs-package (strict MkDocs + wheel/sdist + installed-wheel verifier)
```

## Native source acquisition

Native CI acquires this public repository anonymously with fixed-argument Git
inside the existing per-job workspace. It validates the event SHA and ref,
fetches the exact ref with complete reachable history, checks the fetched tip,
and checks out that exact SHA detached. A moved or unavailable ref fails closed.
The workflow supplies no credential, changes no global Git or HOME state, and
does not clean or reconfigure the runner's shared remote-action cache. Preserve
every original quality command. The exact setup-uv commit is acquired into the
existing ignored `.tmp/setup-uv` directory separately for each job and invoked
as a supported local action. Preserve its complete action metadata, Node24 main
and post hooks, original inputs, uv version, Python version, and cache behavior.
An unavailable pin or pre-existing action directory fails closed. These fixed
acquisitions avoid the two observed shared-worktree paths for these jobs; they
do not claim that all other remote actions or runner caches are isolated.

## Docker Image Tags

### Release Mode (GitHub Release)
| Image | Tags |
|-------|------|
| Raw | `<version>`, `latest`, `sha-<sha>` |
| Nginx | `<version>-nginx`, `latest-nginx`, `sha-<sha>-nginx` |
| Granian | `<version>-granian`, `latest-granian`, `sha-<sha>-granian` |
| Service all/PVE/PBS/PDM | `<version>-<service>`, `latest-<service>`, `sha-<sha>-<service>` |

### Dev Mode (main/testing branch push)
| Image | Tags |
|-------|------|
| Raw | `dev`, `sha-<sha>` |
| Nginx | `dev-nginx`, `sha-<sha>-nginx` |
| Granian | `dev-granian`, `sha-<sha>-granian` |

## Key Rules

- The `uv.lock` at the repo root must stay in sync with `pyproject.toml` because CI runs `uv lock --check` followed by `uv sync --locked`.
- Gitea feature jobs use read-only permissions and the secret-free
  `ci-untrusted-python312` label. A workflow file alone is not evidence of an
  active gate: require an eligible runner plus protected-branch status checks,
  and never merge while a required context is queued or pending.
- CI and release preparation must run `tests/verify_wheel_contract.py` against
  the built wheel so source imports cannot hide missing or stale generated
  schemas. It validates strict PVE scalar behavior and JSON Schema constraints
  for `latest`, `9.2`, and `9.1.11`, plus the PDM schema/client smoke.
- Release workflows validate that the `pyproject.toml` version matches the Git tag before publishing.
- TestPyPI, PyPI, and Gitea preflight/postflight checks compare complete artifact
  sets and hash bytes downloaded from the repository. Never replace this with
  `--skip-existing` or metadata-only success.
- `v*rc*` publishes to TestPyPI only. A manual release dispatch is TestPyPI-only
  from protected `main`; a manual Docker dispatch never publishes. Public PyPI
  and stable Docker aliases require a final `release.published` event.
- The final release body must pass `tests/verify_release_evidence.py` using
  `.github/RELEASE_EVIDENCE_TEMPLATE.md` before any public publisher can run.
  Its package-record manifest SHA256 must equal the manifest rebuilt on GitHub.
- Publisher jobs use protected environments and download artifacts only. Source
  quality, Docker builds, both-architecture runtime smokes, and SBOM generation
  happen before registry credentials exist.
- PyPI postflight downloads and hashes the served wheel. Service images verify
  that filename/SHA256 in the Dockerfile and install it locally with `--no-deps`.
- All seven Docker candidates fan in before stable aliases are written. OCI
  digests are immutable identities; `sha-<commit>` is a commit traceability tag.
- Stable promotion is serialized and refuses to move aliases for a release that
  is no longer GitHub's current latest release.
- QEMU and BuildKit helpers are digest-pinned. Docker staging verifies platform
  and provenance labels, binds archive/SBOM hashes to per-architecture registry
  manifest digests, and the final fan-in hashes those source/run/attempt-qualified
  evidence records. Candidate tags carry the same run token so reruns and
  same-commit workflows cannot overwrite one another.
- All runner jobs have explicit timeouts. Pytest also bounds individual tests,
  uses HTTPX2 for Starlette's supported TestClient transport, and isolates mock
  state per xdist worker/process.
- Publisher secrets must be environment-scoped, never repository-scoped. The
  required environment reviewers, deployment rules, protected tags, and Gitea
  runner labels are documented in `docs/release-evidence.md` and must be
  provisioned outside the repository.

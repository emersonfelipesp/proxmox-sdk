# Release evidence and package promotion

The release pipeline is package-first and fail-closed. A release candidate and
every final or post release is built reproducibly from a protected tag, recorded
in the Gitea Package Registry, validated through TestPyPI, and only then
eligible for public PyPI and Docker Hub promotion.

## Required sequence

1. Record requirements, design impact, verification scope, coverage, known
   defects, operational impact, and approvals in the private lifecycle record.
2. Create a PEP 440 release-candidate version such as `X.Y.Zrc1` and push the
   matching protected `vX.Y.Zrc1` tag. The Gitea package workflow builds the
   wheel and sdist twice under one `SOURCE_DATE_EPOCH`, requires identical
   SHA256 values, runs the full test suite, and publishes the exact pair to the
   Gitea Package Registry.
   The Gitea jobs use the server-compatible v3 artifact transport, with the
   exact source SHA, run ID, and attempt in the handoff name. The builder uses
   uv to provision the locked Python runtime and release tools; it must not
   depend on mutable host Python, `jq`, or other manually installed utilities.
   Gitea scopes artifacts to a run attempt. If the publisher fails after the
   builder succeeds, rerun **all jobs**, not only the failed publisher job; the
   workflow rejects a publisher-only rerun before touching package credentials.
   A complete rerun is idempotent: the preflight accepts only exact existing
   bytes, stages only a missing wheel or sdist after verifying the existing
   subset, and recreates the complete verification evidence. Unexpected files
   or a served-byte mismatch fail closed. Exact-version classification uses a
   pinned Python packaging parser, including normalized project names,
   equivalent PEP 440 spellings, wheels, and legacy installable archives.
   Missing files are copied into a fresh, verifier-created staging directory;
   persistent-runner leftovers are never reused as publisher input.
3. Verify the Gitea package evidence artifact and the package listing through
   `nms git packages`. Do not promote a tag whose package record is absent or
   whose served bytes differ from the build manifest.
4. Promote the RC tag to GitHub. The `v*rc*` trigger publishes the same pair to
   TestPyPI and validates the bytes served by TestPyPI across Python 3.11, 3.12,
   and 3.13 and all supported schema fixtures. Iterate with `rcN` until clean.
5. Create the final protected tag on Gitea and require its final package record
   to pass the same byte-level verification.
6. Copy `.github/RELEASE_EVIDENCE_TEMPLATE.md` into the public GitHub Release
   body, set the exact version, copy the Gitea evidence artifact's
   `distribution_manifest_sha256`, complete every evidence item, and remove all
   private tracker references. The public workflow rebuilds the manifest and
   rejects a digest mismatch, missing/unchecked evidence, a version mismatch,
   or internal evidence.
7. Publish the non-prerelease GitHub Release. PyPI publication runs in a
   protected, artifact-only job. A later job downloads the project wheel back
   from PyPI, hashes the served bytes, and makes that exact wheel the only
   project payload accepted by service-image builds.
8. Core and service images build without registry credentials, run on amd64 and
   arm64 under a digest-pinned QEMU helper where needed, and emit CycloneDX
   inventories. BuildKit is likewise selected by a reviewed multi-architecture
   digest. Protected jobs load the tested Docker archives, verify the requested
   platform plus source/version/wheel labels, bind each archive and SBOM hash to
   its registry manifest digest, and stage candidate manifests. Every candidate
   is pulled by digest and smoked on both platforms before one final fan-in job
   verifies all per-architecture evidence and writes version, `latest`, and
   commit-traceability aliases.
9. Retain the distribution, served-PyPI, candidate-manifest, SBOM, and final
   promotion evidence artifacts. The post-release workflow rechecks alias
   digests and runs all seven image identities on both architectures.

RC tags never enter the public PyPI or stable Docker paths. A manual public
workflow dispatch is TestPyPI-only and must execute from protected `main`.
Manual Docker dispatches build and test only.

## Required external controls

Repository YAML cannot create environment reviewers, deployment branch rules,
protected-tag rules, runner isolation, or environment-scoped secrets. Operators
must configure all of the following before enabling publication:

| Environment | Credential | Required deployment policy |
|-------------|------------|----------------------------|
| `testpypi` | `TEST_PYPI_TOKEN` | Required reviewer; protected `main` and protected `v*rc*`/prerelease tags only |
| `pypi` | `PYPI_TOKEN` | Required reviewer; protected final/post release tags only |
| `dockerhub-candidate` | `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN` | Protected `main`/`testing` and protected release tags only |
| `dockerhub-development` | Docker Hub credentials | Protected `main`/`testing` only |
| `dockerhub-release` | Docker Hub credentials | Required reviewer; protected final/post release tags only |
| `gitea-package-registry` | `GITEA_PACKAGE_USERNAME`, `GITEA_PACKAGE_TOKEN` | Required reviewer; protected `v*` tags only |

Remove the corresponding repository-scoped publisher secrets after the
environment secrets are configured. Protect tag creation, restrict environment
administrators, and require the `pypi`/`dockerhub-release` reviewer to confirm
the Gitea package-of-record and RC evidence. Provision isolated Gitea runner
labels `release-builder` (no publisher secret) and `release-publisher`
(environment access only); do not place either label on a general PR runner.

## Reproducibility and digest terminology

The Python wheel and sdist are required to reproduce byte for byte under the
tag commit timestamp. Container inputs are constrained by the reviewed
Python/Alpine multi-architecture index digest, exact direct APK versions, the
locked Python graph, checksummed mkcert downloads, source revision labels, and
per-image CycloneDX inventories.

Container binary reproducibility is not claimed: Alpine repositories and
transitive build behavior can change independently of this repository. The OCI
manifest digest is the immutable image identity. Tags named `sha-<commit>` are
commit traceability tags, not immutable objects; all promotion and verification
therefore reads and compares manifest digests.

Within a workflow run, distribution, Docker archive, SBOM, and provenance
artifact names include the validated source SHA, GitHub run ID, and run attempt.
Downloads are restricted to those exact names, so a rerun cannot consume an
earlier attempt's artifact. Candidate registry tags carry the same run token to
prevent a same-commit CI/release race. Candidate evidence records the local
image ID, requested platform, OCI revision/version/wheel labels, archive SHA256,
SBOM SHA256, and the matching digest returned by both the push and registry
inspection. The final promotion evidence hashes the candidate-evidence
documents themselves so a later artifact substitution cannot silently change
the approved identity chain.

Docker Hub does not provide a transaction that atomically updates all aliases.
The workflow gates all candidates before the first stable write and promotes
only from validated digests, but an external registry failure can still stop a
multi-image alias update partway through. A rerun revalidates the candidates and
idempotently re-points every alias to the recorded digests; never rebuild or
delete a released artifact to repair a partial alias update.

Stable Docker promotion is serialized across releases and rechecks that the
triggering GitHub Release is still the repository's current latest release
immediately before alias writes. An older rerun may verify its immutable version
artifacts, but it cannot move `latest*` aliases backward.

## Lifecycle evidence retained

The evidence set covers NASA NPR 7150.2D Chapter 4 lifecycle expectations:

- requirements and acceptance-criteria traceability;
- architecture/design impact and reused-component decisions;
- coding standards, static analysis, tool and dependency versions;
- unit, integration, package, schema-matrix, container, and post-release tests;
- measured coverage or an approved rationale for gaps;
- security checks, known-defect disposition, and reviewer approval;
- delivery manifests containing source, distribution, served-wheel, and OCI
  digest identities;
- operator documentation, rollback, maintenance, archive, and retirement
  assessment.

The workflows retain release evidence artifacts for 90 days. The private issue
and pull-request record remains the long-term lifecycle archive. Public Release
notes contain only the product-facing checklist and must not include private
URLs, issue/PR numbers, branch names, or internal commit references.

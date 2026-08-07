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
   SHA256 values, runs the full test suite, writes the canonical cross-system
   distribution manifest, a separate source/run/workflow-bound Gitea
   provenance document, and `SHA256SUMS`, then uploads one deterministic tar.
   The sole job runs on `ci-untrusted-python312` with read-only contents and
   explicit `packages: none`. No Gitea Actions job, runner, environment, user,
   organization, or repository secret may hold a package credential.
3. Wait for that exact workflow run and its sole builder job to finish
   successfully. Download the source-SHA/run-ID/attempt-scoped Actions ZIP from
   that run into `/var/lib/proxmox-sdk-publisher/inbox/<run-id>.zip`. The
   deployed Gitea-compatible v3 artifact protocol has no authoritative unique
   artifact ID in the REST artifact API, so the separately stored job log is
   the server-side binding: it records the artifact name and SHA256 of the
   candidate tar that the host publisher must reproduce.
4. Start `proxmox-sdk-gitea-verify@<run-id>.service`. The credential-free
   verifier requires the exact owner/repository, workflow path,
   successful run and job identities, untrusted runner label, annotated tag,
   pinned `v*` protection identity and allowlists created before the run, main
   ancestry, tag/commit/version agreement,
   tagged workflow digest/policy, log-bound candidate digest, closed tar member
   set, both evidence documents, `SHA256SUMS`, distribution hashes, and
   wheel/sdist metadata. It downloads the exact tagged source, rebuilds twice
   in the immutable host build environment, and requires byte equality with the
   untrusted Actions candidate. Its root finalizer rehashes and seals the closed
   handoff. Only then start `proxmox-sdk-gitea-publisher@<run-id>.service`; that
   separate process receives only the encrypted registry credential, rehashes
   the root-sealed handoff, performs an idempotent same-origin upload, downloads
   served bytes, requires the exact two-file set, and writes
   `/var/lib/proxmox-sdk-publisher/evidence/<run-id>.json`.
   A partial prior upload is repaired only when every existing byte matches;
   extra or mismatched files fail closed.
5. Verify the package listing through `nms git packages` and archive the host
   evidence. Do not promote a tag whose package record is absent or whose served
   bytes differ from the build manifest.
6. Promote the RC tag to GitHub. The `v*rc*` trigger publishes the same pair to
   TestPyPI and validates the bytes served by TestPyPI across Python 3.11, 3.12,
   and 3.13 and all supported schema fixtures. Iterate with `rcN` until clean.
7. Create the final protected tag on Gitea and require its final package record
   to pass the same byte-level verification.
8. Copy `.github/RELEASE_EVIDENCE_TEMPLATE.md` into the public GitHub Release
   body, set the exact version, copy `distribution_manifest_sha256` from the
   external host publisher evidence, complete every evidence item, and remove all
   private tracker references. The public workflow rebuilds the manifest and
   rejects a digest mismatch, missing/unchecked evidence, a version mismatch,
   or internal evidence.
9. Publish the non-prerelease GitHub Release. PyPI publication runs in a
   protected, artifact-only job. A later job downloads the project wheel back
   from PyPI, hashes the served bytes, and makes that exact wheel the only
   project payload accepted by service-image builds.
10. Core and service images build without registry credentials, run on amd64 and
   arm64 under a digest-pinned QEMU helper where needed, and emit CycloneDX
   inventories. BuildKit is likewise selected by a reviewed multi-architecture
   digest. Protected jobs load the tested Docker archives, verify the requested
   platform plus source/version/wheel labels, bind each archive and SBOM hash to
   its registry manifest digest, and stage candidate manifests. Every candidate
   is pulled by digest and smoked on both platforms before one final fan-in job
   verifies all per-architecture evidence and writes version, `latest`, and
   commit-traceability aliases.
11. Retain the distribution, served-PyPI, candidate-manifest, SBOM, and final
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
| Gitea package registry | systemd encrypted `registry.json` credential on the external publisher host | Exact protected annotated `v*` tags only; never available to Gitea Actions |

Remove the corresponding GitHub repository-scoped publisher secrets after the
GitHub environment secrets are configured. Never store the Gitea package PAT as
a Gitea Actions user, owner, repository, environment, or runner secret: any
same-repository workflow can target an eligible runner, and Gitea environments
do not form a sufficient credential boundary. There is no `release-publisher`
runner. The only Gitea release job uses the same untrusted label as review CI.

Install `tools/gitea_package_publisher.py`, its Python runtime, the reviewed
`nms` binary at `/opt/proxmox-sdk-publisher/bin/nms`, and both systemd units into
root-owned read-only paths before tag creation. The immutable Python 3.13.14
interpreter must contain exactly `build==1.5.0`, `packaging==26.0`,
`pyproject-hooks==1.2.0`, `setuptools==83.0.0`, and `wheel==0.47.0`;
it is never resolved or installed during a release. Record all installed-file SHA256
identities in the private release evidence; never run tools from a tag checkout.
Provision a read-only Gitea credential at
`/etc/proxmox-sdk-publisher/gitea-read.json` for `nms git` evidence reads and an
encrypted systemd credential named `registry.json` containing only `username`
and `token`. Copy `tools/publisher-policy.example.json` to root-owned
`/etc/proxmox-sdk-publisher/policy.json`, replace the invalid zero with the exact
server-assigned `v*` protection ID, and pin the approved user/team allowlists.
The rule's server `created_at` and `updated_at` must predate the workflow run;
no release may proceed until that external rule exists. Credential
values must never appear in an environment variable,
command argument, log, repository secret, or committed configuration. Protect
tag creation, require annotated tags and the exact `v*` protection, restrict
publisher-host administrators, and require the public-release reviewer to
confirm the Gitea package record and host evidence.

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

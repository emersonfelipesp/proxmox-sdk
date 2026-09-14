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
   The `prepare-package` job runs on `ci-untrusted-python312` with read-only
   contents and explicit `packages: none` and receives no package credential.
   Candidate provenance records the canonical public server identity
   `https://git.nmulti.cloud`; it does not consume the runner-facing
   `github.server_url`, which can legitimately contain the server's internal
   configured origin.
3. The dependent `verify-and-seal` job anonymously fetches canonical `main` and
   the exact annotated tag from `https://git.nmulti.cloud`, proves that the tag
   peels to the immutable event SHA and remains in canonical `main`, validates
   the workflow digest and every candidate attestation field, and rebuilds the
   source in two independent Git worktrees. It requires byte equality between
   both rebuilds and the candidate, writes a canonical seal manifest that binds
   every sealed file to the source SHA, run ID, run attempt, tag, and version,
   and exports the manifest SHA256 as a job output before uploading the bounded
   seal. This credential-free job runs only on the dedicated `release-builder`
   lane and never on a `ci-untrusted-*` runner.
4. The `publish-candidate` job anonymously fetches the exact tag from the
   canonical `https://git.nmulti.cloud/emersonfelipesp/proxmox-sdk.git` origin
   into an isolated source tree, checks that the tag peels to `${{ github.sha }}`
   and that the checked-out SHA matches the verifier output, downloads only the
   sealed set, recomputes and compares the verifier-exported seal manifest
   SHA256, and restores private read-only modes. It then uses the locked release
   tools and the same reproducible-build procedure as `prepare-package` to build
   the exact tag source twice on the `release-publisher` runner. Both rebuilt
   distributions must match the sealed wheel and sdist byte for byte before the
   package token is exposed. This job must run only on the dedicated
   `release-publisher` lane and never on a `ci-untrusted-*` runner. Only its
   five-minute `Publish sealed package and verify served bytes` step receives
   the repository secret `PACKAGE_WRITE_TOKEN`. The helper validates the token
   as bounded printable ASCII before constructing a registry client, uses the
   pinned `https://git.nmulti.cloud` origin, and uploads each missing artifact
   through one no-redirect multipart request with bounded connect/read timeouts,
   response size, and a shared global deadline. An exact remote subset is
   resumable only when every present artifact's metadata, served bytes, and
   repository association match the seal; every upload is followed by a fresh
   inspection. Redirected, oversized, timed-out, extra, mismatched, or wrongly
   associated states fail closed. An ambiguous upload or link response is
   accepted only when an independent bounded GET proves exact progress. A final
   credential-free step retains `publication.json` under a source/run/attempt-
   qualified artifact name. That evidence records the verified seal digest,
   canonical server, owner, and repository, observed repository association,
   result, and the final filename, size, and SHA256 inventory.
5. Verify the package record and both served file identities with:

   ```bash
   nms git packages latest --type pypi --name proxmox-sdk --owner emersonfelipesp
   nms git packages detail --type pypi --name proxmox-sdk --version <version> --owner emersonfelipesp
   nms git packages files --type pypi --name proxmox-sdk --version <version> --owner emersonfelipesp
   ```

   Archive these responses with the candidate provenance and distribution
   manifest. Do not promote a tag whose package record, repository association,
   filenames, sizes, or SHA256 values differ from the sealed evidence.
6. Promote the RC tag to GitHub. The `v*rc*` trigger publishes the same pair to
   TestPyPI and validates the bytes served by TestPyPI across Python 3.11, 3.12,
   and 3.13 and all supported schema fixtures. Iterate with `rcN` until clean.
7. Create the final protected tag on Gitea and require its final package record
   to pass the same byte-level verification.
8. Copy `.github/RELEASE_EVIDENCE_TEMPLATE.md` into the public GitHub Release
   body, set the exact version, copy `distribution_manifest_sha256` from the
   Gitea provenance in the verified seal, complete every evidence item, and
   remove all private tracker references. The public workflow rebuilds the
   manifest and rejects a digest mismatch, missing/unchecked evidence, a
   version mismatch, or internal evidence.
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
| Gitea package registry | Repository secret `PACKAGE_WRITE_TOKEN` | Repository-scoped `write:package`; exact protected annotated `v*` tag workflow only |

Remove the corresponding GitHub repository-scoped publisher secrets after the
GitHub environment secrets are configured. Provision the dedicated runner
`ci-deploy-emersonfelipesp-246` with the labels `mirror-host`,
`release-builder`, and `release-publisher`, and confirm that both release lanes
select only that runner and that the runner executes no pull-request workloads.
Do not configure `PACKAGE_WRITE_TOKEN` until the `release-builder` and
`release-publisher` assignments and the absence of pull-request workloads have
been confirmed. Then provision it as the only Gitea package-publisher secret. It
must be a dedicated,
repository-scoped `write:package` credential, must not grant repository-content
write or administrative access, and must not be copied into a runner profile,
command argument, log, artifact, or committed configuration. The built-in job
token remains package-read-only. The `prepare-package` job remains on disposable
`ci-untrusted-python312` workers; `verify-and-seal` is isolated on
`release-builder`, and `publish-candidate` is isolated on `release-publisher`.
If the secret is absent, the credentialed step exits non-zero with an explicit
message.

The systemd verifier and publisher units remain available as a compatibility
path for already provisioned hosts, but they are no longer required for the
normal release sequence. Their credential-file and root-seal controls remain
unchanged. Protect tag creation, require annotated tags and the exact `v*`
protection, restrict repository-secret administration, and require the public
release reviewer to confirm the Gitea package record and retained evidence.

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

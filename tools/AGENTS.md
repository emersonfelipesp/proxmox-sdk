# Gitea package release tools

`gitea_package_publisher.py` implements separate verify, seal, and publish
phases for the private Gitea Python package of record. The normal path runs
those phases in three isolated Gitea Actions jobs. The existing systemd units
remain a compatible option for already provisioned publisher hosts.

The `prepare-package` job builds and attests without credentials. The
`verify-and-seal` job anonymously fetches canonical `main` and the exact
annotated tag, validates the event and attestation, rebuilds in two independent
Git worktrees, requires byte equality, and emits only a bounded exact seal on
the `release-builder` lane. The `publish-candidate` job anonymously fetches the
exact tag from the canonical
`https://git.nmulti.cloud/emersonfelipesp/proxmox-sdk.git` origin into an
isolated source tree, verifies that the tag peels to `${{ github.sha }}`, and
downloads only that seal on the `release-publisher` lane. It exposes the
repository secret `PACKAGE_WRITE_TOKEN` only to the timeout-bounded `Publish
sealed package and verify served bytes` step. Before that step, the job compares
the downloaded canonical seal-manifest digest with the verifier job output,
rebuilds the exact tag source twice with locked tools and the release
reproducibility procedure, and requires both rebuilt distributions to match the
seal byte for byte. The helper reads the token from the environment, validates
it before client construction, and never prints it. The `--python` argument
of `verify-actions` is the locked verifier venv launcher (`venv/bin/python`);
the helper keeps it unresolved, because that launcher is a symlink to the
uv-managed base interpreter and following it would rebuild outside the venv
without the locked build tools. Publication evidence is
uploaded afterward without the package credential and includes the seal digest,
canonical registry identity, repository association, result, and final remote
file inventory.

The `release-builder` and `release-publisher` jobs must never run on a
`ci-untrusted-*` runner. Do not configure `PACKAGE_WRITE_TOKEN` until the
dedicated runner `ci-deploy-emersonfelipesp-246` is confirmed to carry both
labels and to execute no pull-request workloads.

The Actions publisher uses the pinned `https://git.nmulti.cloud` origin and a
direct bounded multipart transport. It resumes only exact remote subsets,
uploads one missing sealed artifact per request, and reinspects the registry
after each upload. Extra, mismatched, redirected, oversized, timed-out, or
wrongly associated states fail closed. An ambiguous upload or link response is
accepted only after an independent exact-state GET.

For the retained host mode, install the helper, immutable Python environment,
reviewed absolute `nms` executable, and both systemd units in root-owned
read-only paths. Its verifier continues to require the exact repository,
workflow, successful builder job, annotated tag, pinned preexisting `v*`
protection, canonical-main ancestry, job-log candidate digest, closed archive
set, and two byte-identical independent rebuilds. It uses `gitea-read.json` and
`policy.json`; its publisher receives only `registry.json`. Do not mix the
Actions token with host credential files.

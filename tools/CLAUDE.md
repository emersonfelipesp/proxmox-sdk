# Host release tools

`gitea_package_publisher.py` implements separate verify/seal/publish phases for
the private Gitea Python package of record. Install it, its immutable Python
environment, the absolute reviewed `nms` executable, and both systemd units in
root-owned read-only paths before tag creation. Never execute them from a tag
checkout or place a package credential in an Actions runner, repository secret,
process environment, command argument, log, or committed file.

The publisher accepts only the exact `emersonfelipesp/proxmox-sdk` repository,
the `Build Gitea package candidate` workflow and builder job, a successful tag
push run, an annotated tag covered by the root-pinned `v*` protection identity
and allowlists before the run began, and a tag commit already contained in
`main`. The verifier obtains those facts and the successful job log through the
absolute `/opt/proxmox-sdk-publisher/bin/nms`; direct HTTP calls are forbidden.

The downloaded Actions ZIP is untrusted input. The verifier requires one
candidate tar, binds its SHA-256 to the exact job log, rejects extra, duplicate,
oversized, encrypted, linked, or traversal entries, verifies the provenance
documents and `SHA256SUMS`, and reads distribution metadata without executing
it. It then downloads the exact source archive and independently builds twice
with preinstalled Python 3.13.14, `build==1.5.0`, `packaging==26.0`,
`pyproject-hooks==1.2.0`, `setuptools==83.0.0`, and `wheel==0.47.0`.
Candidate bytes must match. A root-only finalizer rehashes and
seals the handoff. The separate publisher receives only `registry.json`, never
invokes `nms` or tagged code, rehashes the handoff, and performs same-origin,
closed-set upload and served-byte verification.

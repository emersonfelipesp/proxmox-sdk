<!-- proxmox-sdk-release-evidence:v1 -->

## Release evidence

Release version: `<version>`
Package-of-record manifest SHA256: `<sha256>`

- [ ] **REQ**: Requirements and acceptance criteria are traced to verification results.
- [ ] **ARCH**: Architecture and detailed-design impacts were reviewed and recorded.
- [ ] **IMPL**: Coding standards, tool versions, reused components, and build inputs were reviewed.
- [ ] **STATIC**: Formatting, lint, type, workflow, and security checks passed.
- [ ] **TEST**: Unit, integration, package, multi-schema, and container tests passed.
- [ ] **COVERAGE**: Coverage was measured and accepted, or gaps have a recorded rationale.
- [ ] **DEFECTS**: Known defects are closed or have an approved disposition.
- [ ] **SECURITY**: Credential boundaries, dependency inputs, and supply-chain controls were reviewed.
- [ ] **OPS**: User, operator, API, and agent-facing documentation is current.
- [ ] **RECOVERY**: Rollback, maintenance, archive, and retirement impacts were assessed.
- [ ] **APPROVAL**: The release candidate and package-of-record evidence were approved for promotion.

Replace `<sha256>` with the `distribution_manifest_sha256` from the protected
package-record evidence, replace every unchecked box with `[x]`, and add
concise evidence after each colon. This text is public: describe product
evidence only. Do not include private tracker names, URLs, issue/PR numbers,
branch names, or internal commit references. The public release workflow
rebuilds and compares the manifest digest, then rejects incomplete checklists
and internal references before any PyPI or stable Docker credential is
available.

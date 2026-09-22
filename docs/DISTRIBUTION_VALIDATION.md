# Distribution patch — 1.1.1

This release changes installation guidance and license packaging, not the approved
UI, post, movie, workflow behavior or helper implementations. Test results are
recorded below after execution; source-level compatibility is not an npx test.

## Current verification boundary

The repository shape and commands were checked against the primary READMEs of
[Vercel skills](https://github.com/vercel-labs/skills),
[Vercel agent-skills](https://github.com/vercel-labs/agent-skills), and
[Remotion skills](https://github.com/remotion-dev/skills), and the
[npm npx documentation](https://docs.npmjs.com/cli/v11/commands/npx/).
Anthropic's [skills repository](https://github.com/anthropics/skills) documents a
Claude plugin-marketplace route as another option; this release does not add or
claim a Claude marketplace manifest.

A registry reachability/version query (`npm view skills version engines --json`)
failed with `EAI_AGAIN` for `registry.npmjs.org`. No registry-backed `npx skills`
installation, actual published GitHub install, update/removal through that CLI, or
authenticated host run was completed. Network restrictions were not bypassed.

Offline tests copy only the selected core skill to a disposable directory, then
check its metadata, workflow availability, local links, licenses and helper startup.
They also execute synthetic project initialization without the repository root.
These checks test self-containment, not the external installer's implementation.

## Release checks

- **217 local unit tests passed**, including 7 new distribution checks. No tests skipped.
- Static pack validation passed (syntax, metadata, local documentation links and existing privacy checks).
- **64 example files** match v1.1.0 byte-for-byte: no changes to approved UI, posts, motion or example receipts.
- All 12 workflow files and all 6 helper implementations match v1.1.0 byte-for-byte.
- Skill metadata was bumped to 1.1.1; the entry adds a short installation/runtime pointer.
- Licenses now travel with individually installed skills; the main skill includes the notice.

[Unit test output](evidence/distribution-unit-tests-111.txt) ·
[Static validation](evidence/distribution-static-111.json) ·
[Machine-readable report](distribution-validation.json)

Tests ran on Linux with Python 3.13.5. The installed-core tests use a
disposable copy, without source-root references. They do not simulate a logged-in
model session or claim to exercise the external npx install/update/removal path.

## Still required before claiming a tested public install

Use the actual published repository, a reviewed external CLI version, and a disposable
profile. Check discovery, selected-core install, optional wrapper dependency, real
helper execution, update/removal and host visibility. Test the real target operating
systems. Do not advertise that a documentation-checked command is already end-to-end
verified. Do not claim Python is eliminated: it remains a helper runtime.

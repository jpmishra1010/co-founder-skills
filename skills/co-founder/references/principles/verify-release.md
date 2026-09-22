# verify-release — principles and review

**Core:** Verify the contract, not the agent’s account of its work.

Separate working-tree, CI and deployed evidence; bind each to the actual revision.

Compatibility failures and skipped checks stay visible; do not average them away.

A release needs environment-specific smoke, recovery and an owner, not only green unit tests.

## Required review
- `criteria`: Acceptance criteria map to actual evidence.
- `integrity`: Changed or skipped tests/configuration are disclosed.
- `release-state`: Implemented, tested and deployed states are distinct.

Mark pass / revise / not-checked with an evidence pointer and a concrete reason.
Do not self-certify a result by repeating this checklist. Scope out a criterion
only with an explicit reason; required security or brand gates cannot be waived
by aesthetic preference. Use the shared quality-review record when handing off.

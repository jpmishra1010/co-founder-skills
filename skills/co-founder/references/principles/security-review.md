# security-review — principles and review

**Core:** Follow trust boundaries and demonstrate denied access as well as allowed access.

Use synthetic cross-tenant/role cases and test server enforcement.

Validate attacker-controlled inputs, replay/ordering and resource limits in authorized scope.

No scanner badge substitutes for threat reasoning, incident containment or independent high-risk review.

## Required review
- `threats`: Assets, entry points and trust boundaries are identified.
- `negative-cases`: Relevant deny paths and adversarial inputs are checked.
- `findings`: Findings and untested areas have evidence and remediation.

Mark pass / revise / not-checked with an evidence pointer and a concrete reason.
Do not self-certify a result by repeating this checklist. Scope out a criterion
only with an explicit reason; required security or brand gates cannot be waived
by aesthetic preference. Use the shared quality-review record when handing off.

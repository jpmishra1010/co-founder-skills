# feature-plan — principles and review

**Core:** Design the state machine and data contract, not only the happy-path screen.

Acceptance criteria name observable outcomes and who is allowed to cause them.

Separate source-of-truth updates from read models; cover partial failure and retry.

Describe compatibility and recovery; new scope is not implicitly approved.

## Required review
- `journey`: Main and relevant failure/recovery paths are explicit.
- `invariants`: Business rules and permission boundaries are testable.
- `scope`: In-scope, exclusions and open decisions are clear.

Mark pass / revise / not-checked with an evidence pointer and a concrete reason.
Do not self-certify a result by repeating this checklist. Scope out a criterion
only with an explicit reason; required security or brand gates cannot be waived
by aesthetic preference. Use the shared quality-review record when handing off.

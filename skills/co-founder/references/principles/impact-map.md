# impact-map — principles and review

**Core:** Trace producers, consumers and data ownership; a file list is only a starting point.

Inspect concrete code/schema/event evidence; mark unknown relationships.

Include public APIs, async jobs, imports/exports, caches and other clients.

After changes, compare actual touched areas against the planned impact.

## Required review
- `trace`: Relationships cite actual sources.
- `coverage`: Adjacent workflows have a risk-weighted check matrix.
- `scope-drift`: Actual changes and unmapped areas are reviewed.

Mark pass / revise / not-checked with an evidence pointer and a concrete reason.
Do not self-certify a result by repeating this checklist. Scope out a criterion
only with an explicit reason; required security or brand gates cannot be waived
by aesthetic preference. Use the shared quality-review record when handing off.

# build-fix — principles and review

**Core:** Make the smallest coherent root-cause change; preserve unrelated work.

A regression test must fail for the intended cause, not a broken environment.

Check the diff for swallowed errors, duplicate side effects and dependency churn.

Record falsified hypotheses; after repeated failure change the investigation, not just the patch.

## Required review
- `reproduction`: Reproduction and expected outcome are recorded.
- `diff`: Changes and test/config edits are reviewed.
- `retest`: Original failure and relevant neighbors were exercised.

Mark pass / revise / not-checked with an evidence pointer and a concrete reason.
Do not self-certify a result by repeating this checklist. Scope out a criterion
only with an explicit reason; required security or brand gates cannot be waived
by aesthetic preference. Use the shared quality-review record when handing off.

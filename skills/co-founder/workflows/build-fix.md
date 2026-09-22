# Implement bounded changes and diagnose bugs with evidence

## Project binding and quality
Resolve the project using `references/project-identity.md`; bind this task to
its project ID, environment and, for visuals, the approved surface/brand bundle.
Read `references/principles/build-fix.md`. Apply its evidence-backed review
before handoff. Wrong-project context or an unapproved consequential action
is a blocker, not a missing detail to guess.

## Use and context
Use only for authorized local implementation or debugging. Read the issue or
approved feature criteria and impact plan. Apply `references/debugging.md` for
bugs and `references/engineering-checklist.md` for shared business logic.
Inspect the repository's own instructions and commands. Do not run untrusted
package scripts before reviewing them or broaden host permissions.

## Procedure
1. Identify the current branch/revision, relevant user edits, runtime, and actual
   reproduction. Preserve the reproduction and expected result. When blocked,
   report the blocker and inspect safe evidence rather than inventing a cause.
2. Run relevant baseline checks where practical. Save commands, exit status,
   timestamp, and revision. A failure can be called pre-existing only when the
   same relevant baseline demonstrates it; otherwise classify it unknown.
3. Form one falsifiable hypothesis. Inspect logs/code/data with sanitized inputs.
   Record attempted causes and what ruled them out. Do not repeatedly clear
   caches, add delays, increase CSS specificity, or rewrite code without evidence.
4. Add or identify a test that expresses the agreed behavior and fails for the
   correct reason before the fix when feasible. Make a minimal coherent change
   following project conventions. Address root cause, transaction boundary,
   authorization, or data ownership rather than masking symptoms.
5. Execute the original reproduction and relevant adjacent checks. Inspect actual
   output. `cf.py run-check` offers bounded logging but requires `--execute` and
   is not a sandbox. Use real project commands; never invent a test suite.
6. After two unsuccessful fixes, stop automatic cycling. Summarize findings and
   choose a new hypothesis or request missing access/requirements before more
   substantial work. Do not hide uncertainty with a larger rewrite.
7. Review actual diff, changed tests/configuration, dependencies, and side effects.
   Revisit impact-map if scope changed. Route to verify-release; high-risk areas
   also need security-review. Do not automatically commit, push, deploy, or send.

## Deliverable
State reproduced issue, evidence-backed cause, changes made, checks executed,
results, remaining uncertainty, and exact handoff. Preserve a short attempt log
in an authorized local work record. Distinguish a likely cause from a proven one.

## Hard stops
No deleting/skipping a failing test merely to pass; no broad assertion loosening;
no hardcoded tenant, admin shortcut, swallowed error, fake success response,
disabled type/security rules, or suppression of warnings without justification.
Legitimate behavior changes require visible acceptance-criterion approval.
No destructive git/database operations or production access without authorization.

## Done / handoff
The change meets agreed local criteria and verification has evidence. "Implemented"
is permitted before deployment; "customer fixed" is not. Update support with a
truthful pending-verification or pending-release state.

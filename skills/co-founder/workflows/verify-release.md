# Verify behavior, related flows, and release evidence

## Project binding and quality
Resolve the project using `references/project-identity.md`; bind this task to
its project ID, environment and, for visuals, the approved surface/brand bundle.
Read `references/principles/verify-release.md`. Apply its evidence-backed review
before handoff. Wrong-project context or an unapproved consequential action
is a blocker, not a missing detail to guess.

## Use and context
Use for a review, finished implementation, release readiness, or a recurrent
regression. Read acceptance criteria, impact map, baseline/check evidence, and
actual diff. For visual changes read `references/visual-qa.md`; for security
changes read the security workflow. A review request does not authorize edits.

## Procedure
1. Verify the target revision and environment. Separate existing modifications
   from the proposed change. Inspect test additions/deletions, skipped tests,
   fixture/snapshot changes, exclusion patterns, runner scripts, and CI settings.
2. Compare observed behavior to approved criteria, not to the agent's description.
   Run relevant baseline/candidate checks where compatible; note environment or
   contract changes that make the comparison inconclusive.
3. Exercise the complete changed journey, including durable persistence, relevant
   failure paths, role/tenant boundaries, duplicate actions, reversals, events,
   integrations, and reports identified in the impact matrix. Do not equate a
   working button or a green unit suite with a working feature.
4. For UI changes inspect screenshots of the actual running app at applicable
   widths, loaded states, and navigation paths. Include direct load, navigation,
   refresh, shared header/footer, long content, and keyboard behavior. A static
   preview cannot prove authentication, backend, or native-device behavior.
5. Categorize each check as passed, failed, skipped, not-run, or inconclusive.
   Attach reproducible commands and actual evidence. Report gaps plainly. Do not
   promote missing evidence into a pass. Automated accessibility checks are not
   complete accessibility certification; screenshots are not functional tests.
6. Use `cf.py gate --report REPORT.json` with the report template for a local
   evidence gate. The gate is structural and fail-closed on missing required
   checks; it cannot prove artifact authenticity or independently protect itself.
   Use protected CI and a separate reviewer for consequential releases.
7. Prepare scoped release notes, migration considerations, rollback, smoke tests,
   and monitoring. Deploy only after explicit approval via an existing authorized
   deployment mechanism. Recheck the deployed version before claiming release.

## Deliverable
A readiness report: revision, environment, check results, changed acceptance
criteria, evidence locations, known limitations, risk, and release recommendation.
Use `assets/templates/verification.json` and the human-readable change report.
The recommendation is ready-for-review / blocked / inconclusive, not "bug-free".

## Done / handoff
Only explicitly verified states are advanced. Send customer-care a deployment
identifier and validated behavior, not a generic success message. Public release
copy must match capabilities actually available to its audience.

# Identify related modules and behaviors before changing code

## Project binding and quality
Resolve the project using `references/project-identity.md`; bind this task to
its project ID, environment and, for visuals, the approved surface/brand bundle.
Read `references/principles/impact-map.md`. Apply its evidence-backed review
before handoff. Wrong-project context or an unapproved consequential action
is a blocker, not a missing detail to guess.

## Use and context
Use before a change to shared components, data, permissions, state transitions,
integrations, or a bug with effects outside one screen. Read the scoped feature
or issue and `.co-founder/product-map.json`. Treat that map as a maintained aid,
not an authoritative automated dependency graph. Missing coverage is uncertainty.

## Procedure
1. Record repository/worktree, baseline revision, existing user changes, affected
   environment, and exact scope. Do not reset, stash, or discard user work.
2. Inspect entry points, direct callers, shared helpers, models/tables, migrations,
   permissions, routes, components, cache keys, reports, imports/exports, event
   consumers, webhooks, scheduled jobs, and integrations relevant to the change.
3. Run `python PACK/scripts/cf.py impact --project PROJECT --base BASE` for a
   bounded changed-path inventory. With `--map` use the reviewed product-map.
   The helper is path/rule based, not semantic static analysis; follow up on
   unmapped files and implicit data coupling. No files changed is not no impact.
4. Trace data both upstream and downstream, including background processing.
   Identify business invariants: money totals/rounding, inventory conservation,
   ownership, idempotency, role isolation, event order, and reversal behavior.
5. Identify compatibility and change risks: shared UI across routes, clients
   using older contracts, schema rollback, partially completed transactions,
   stale caches, offline clients, and races. Ask only when the desired business
   behavior cannot be inferred from approved requirements.
6. Build a risk-weighted test matrix. Include the original path, adjacent paths,
   failure/retry/reversal, roles/tenants, and relevant responsive/navigation
   states. Mark not-applicable with a reason, not as an automatic pass.
7. Propose smallest change boundaries. If widening scope is necessary, explain
   why and ask before broad work. Hand security-sensitive paths to review.

## Deliverable
Use `assets/templates/impact.md`: changed area, producers/consumers, shared data,
invariants, affected modules, test matrix, risk level, unknowns, and rollback.
Keep evidence linked to concrete files, schema, or observed behavior. A diagram
with invented module names is not an impact analysis.

## Done / handoff
Build-fix has clear change boundaries and verify-release has a coverage matrix.
After implementation, compare actual changed paths to planned scope. New areas
require updating the analysis; do not assume the original plan still covers them.

## Example
Changing repair completion can affect stock movements, invoices, tax/rounding,
reporting, notifications, duplicate requests, and cancellation. Do not stop at
the route handler or assume every listed module exists in the user's project.

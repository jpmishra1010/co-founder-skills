# Define the whole workflow before implementation

## Project binding and quality
Resolve the project using `references/project-identity.md`; bind this task to
its project ID, environment and, for visuals, the approved surface/brand bundle.
Read `references/principles/feature-plan.md`. Apply its evidence-backed review
before handoff. Wrong-project context or an unapproved consequential action
is a blocker, not a missing detail to guess.

## Use and context
Use after an idea is approved for specification, or when a founder asks what a
feature must include. Read relevant decisions, roles, existing feature behavior,
and product map. Load `references/flow-library.md` only for applicable patterns.
Do not silently expand a request into a complete platform rewrite.

## Procedure
1. Specify the actor, goal, triggering event, starting state, and observable end
   state. Identify the primary path and the roles that cannot perform it.
2. Map the journey as explicit states and transitions: entry, input, validation,
   permission, execution, persistence, confirmation, exit. Add empty, loading,
   failure, partial success, retry, cancel, undo/reversal, and resume paths where
   relevant. Consider desktop, mobile, keyboard, slow networks, and long content.
3. Determine the source of truth and contracts: fields, identifiers, ownership,
   role/tenant boundaries, events, background jobs, integration requests, and
   downstream readers. Separate stored state from a UI-only representation.
4. Define invariants in plain language. For example, a retry must not duplicate
   an irreversible business operation; the application must not silently save
   one user's data into another tenant. Consult impact-map for affected modules.
5. Break scope into a smallest useful release and explicit later work. Reuse the
   existing design system, architecture, error patterns, and terminology. Do not
   add dependencies or rewrite components without a concrete reason.
6. Write observable acceptance criteria, including persistence after refresh,
   authorization failure, double-submit, validation, and at least the relevant
   related-module checks. Define test data and what is deliberately not covered.
7. Include rollout/rollback, compatibility, data migration, feature gating,
   observability, support explanation, and approved public claims when needed.
   Financial, authentication, and data changes require deeper security review.

## Deliverable
Use `assets/templates/feature-plan.md`. Include a compact flow diagram in text,
a state table, acceptance criteria with IDs, impact notes, exclusions, and open
decisions. Each criterion should be executable or manually inspectable; avoid
"must be premium", "fully secure", or "works perfectly" as standalone criteria.

## Done / handoff
Build-fix receives approved scope, invariants, and verification criteria. UI work
receives a visual brief and approved direction, not permission to change behavior.
Do not claim a feature exists because it is specified. Update capabilities only
when implementation and release evidence support the new state.

## Example
A customer editor is not complete when a dialog opens. Define valid input,
error recovery, durable save, edit propagation, access rules, refresh behavior,
and the source of the success message. Exclude unrelated CRM automation unless
explicitly requested.

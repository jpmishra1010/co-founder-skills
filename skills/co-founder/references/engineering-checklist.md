# Engineering change checklist

Use the project's established architecture, conventions, package manager, and
testing tools. Avoid framework migrations and new dependencies for a scoped fix.
Inspect existing uncommitted work and preserve it. Do not execute untrusted
install/test scripts outside an appropriate sandbox.

## Shared business logic
State ownership and source of truth. Apply authorization at the trusted server
boundary. Treat transactions and retries together: what if an action succeeds but
the reply is lost? Account for duplicate and out-of-order events. Use reviewed
precision/rounding rules for money and units; do not silently change reporting.
Define reversal/compensation for already-completed irreversible effects.

## Data and compatibility
Inspect schema readers/writers, migration size/locks, backward compatibility,
rolling deployment, old clients, cache keys, exports, integrations, and background
jobs. Plan rollback honestly; irreversible migrations cannot be undone by simply
reverting application code. Do not touch production data without authorization.

## API and UI
Validate inputs, handle errors explicitly, avoid duplicate submissions, preserve
loading/empty/error states, and confirm durable save. Preserve accessible semantics
and brand design tokens. A hidden action is not authorization. A mock response is
not a completed backend integration.

## Review
Inspect the actual diff and any generated files. Highlight changed tests,
assertions, exclusions, permissions, dependencies, and configuration. Execute
appropriate unit/integration/browser checks; use an honest not-run state when
unavailable. Add regression coverage for the original fault. Review deployment,
rollback, logs, and customer-facing explanation without exposing sensitive data.

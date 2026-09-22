# End-to-end feature patterns

Choose the applicable pattern; do not apply every checklist to every task.

| Pattern | Useful states and checks |
|---|---|
| Create/edit record | Validation, role/tenant ownership, save, server confirmation, refresh, edit propagation, conflict, cancel, undo if supported. |
| Money/stock operation | Calculation precision, transaction boundary, repeated submission, concurrency, reversal, ledger/report consistency, audit history. |
| Upload/import | Supported types, size limits, validation preview, partial rows, error report, safe storage, ownership, retry, duplicate detection. |
| Search/filter | Empty/loading/error, correct scope, combined filters, pagination, URL/state restore, clear filters, long queries, count consistency. |
| Invitation/access | Inviter authorization, recipient match, expiration, replay, revocation, existing account, least privilege, audit and recovery. |
| Background job | Scheduling/authorization, accepted versus completed, retry policy, idempotency, progress, terminal failure, monitoring, cancellation. |
| External integration | Verified identity/callback, allowed scopes, credentials outside context, retries, duplicate/out-of-order events, revocation, outage behavior. |
| Settings | Authorized editor, validation, propagation, saved/unsaved indicator, concurrency, reset, safe default, audit and reversibility. |
| Subscription/entitlement | Source of truth, lifecycle, grace/failure, access transition, reconciliation, retries, cancellation, accurate customer message. |
| Notification | Consent, recipient, trigger, duplicate handling, preference changes, failure, private data in content, unsubscribe where applicable. |

For each journey define input → policy check → state transition → durable effect →
user confirmation → downstream effect. List what happens if the connection fails
between any two steps. A success toast must follow the relevant durable operation,
not an optimistic assumption. State how conflicting updates are resolved.

Test accessible keyboard operation and narrow screens when there is a UI. Preserve
language, timezone, date, currency, units, and locale expectations. Use representative
long and empty content rather than only a short ideal fixture. Keep public marketing
capabilities tied to deployment evidence and actual entitlements.

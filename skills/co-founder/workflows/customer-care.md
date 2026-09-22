# Resolve customer issues beyond the code change

## Project binding and quality
Resolve the project using `references/project-identity.md`; bind this task to
its project ID, environment and, for visuals, the approved surface/brand bundle.
Read `references/principles/customer-care.md`. Apply its evidence-backed review
before handoff. Wrong-project context or an unapproved consequential action
is a blocker, not a missing detail to guess.

## Use and context
Use for support triage, customer-response drafts, recurring complaints, knowledge
content, or an unresolved fix. Use provided sanitized records or an authorized
connector. Do not imply inbox/CRM access if none exists. Read relevant issue,
release, capability, and support-policy records; do not ingest whole mailboxes.

## Procedure
1. Capture the customer's goal, actual/expected behavior, impact, environment,
version, reproduction, and permitted follow-up. Minimize personal information.
Seek essential missing reproduction details, not an exhausting questionnaire.
2. Triage severity using actual business impact: data loss/exposure, blocked work,
incorrect money/stock, repeated degradation, or cosmetic friction. Identify
related incidents without merging different causes prematurely.
3. Acknowledge impact in plain language. State what is known, what is being
checked, the next update owner/time when genuinely committed, and a safe
workaround only if verified. Do not invent timelines or say "fixed" prematurely.
4. Create or update a work record with explicit states: reported, reproduced,
fix-prepared, verified, deployed, customer-confirmed, or closed-with-reason.
Use blocked/waiting states as needed. A Git merge is not a customer resolution.
5. Route diagnosis to build-fix with reproduction and acceptance criteria. Connect
the issue to related flows via impact-map. Track the returned evidence and
deployment identifier. Recheck the customer's affected version/environment.
6. Prepare the customer update, regression explanation, and follow-up. Send only
through an explicitly approved connector action with correct recipient and text.
Customer-confirmed requires actual feedback; an internal smoke test is separate.
7. Feed recurring, sanitized problems into decide/growth. Turn verified solutions
into help articles with exact UI steps. Do not expose private tickets in content.

## Deliverable
An issue record, severity rationale, reproduction, state, linked evidence,
customer reply draft, next action, and closure criteria. Use
`assets/templates/customer-issue.json` and `support-reply.md`.

## Done
The issue has a known next action or a justified closure. Do not close merely
because the user has not replied unless an approved policy allows closure with
that explicit reason. A closed-with-reason issue is not customer-confirmed.
For security incidents, hand off privately to security-review and stop public
content generation about the incident until communication is approved.

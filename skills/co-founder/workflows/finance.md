# Track cash, runway, pricing and revenue from real records

## Project binding and quality
Resolve the project using `references/project-identity.md`; bind this task to
its project ID, environment and, for visuals, the approved surface/brand bundle.
Read `references/principles/finance.md`. Apply its evidence-backed review
before handoff. Wrong-project context or an unapproved consequential action
is a blocker, not a missing detail to guess.

## Use and context
Use for cash position, burn, runway, revenue metrics, pricing and packaging,
recurring spend, invoices and collections, or preparing questions for an
accountant. Read company brief, `.co-founder/metrics.json`, `commitments.json`,
approved offers in `claims.json`, and exports the founder supplies or an
authorized read-only connector returns. Never request, store or repeat
credentials or full bank/card numbers. No payments, transfers, refunds, price
changes, cancellations or invoice sends happen inside this workflow.

## Procedure
1. State the question, as-of date, period, currency and basis (cash or accrual).
Record each figure with its source and period. Missing data stays unknown; do
not estimate a balance, MRR or churn the founder has not supplied.
2. Reconcile before analysing. Check totals against the source, flag duplicates,
refunds, currency conversion, one-off items and personal spending mixed into
business accounts. Keep collected, invoiced, booked and recognized revenue apart.
3. Cash: cash on hand, net burn with the months used, and runway as a base and a
downside scenario with stated assumptions. Include known obligations such as tax
payments, annual renewals and contractor commitments. If the business is cash-flow
positive, say so instead of inventing a runway figure.
4. Revenue health: MRR movement (new, expansion, contraction, churned), customer
count, concentration in the largest customers, and outstanding receivables by
age. Define each metric once in `metrics.json`; do not change a definition
between periods without recording the change.
5. Pricing and packaging: connect the value metric, customer evidence, margin
and current primary-source competitor pricing. Check existing contracts and
commitments before proposing changes for current customers. Route large or
irreversible changes to decide; public price copy needs approval via growth/sales.
6. Spending: list recurring tools and vendors with cost, renewal date and last
known use. Draft cancel/downgrade recommendations; the founder cancels.
7. Collections: draft reminders that follow approved payment terms only. No
threats, invented late fees or changed terms. Sending requires the actual
recipient, approved text and an authorized connector result.
8. Tax filings, entity questions, payroll, sales tax/VAT/GST, audit-grade revenue
recognition, fundraising instruments and investing cash go to a qualified
professional. Prepare a packet with figures, questions and deadlines taken from
the founder or official sources for the stated jurisdiction.
9. When authorized, add dated snapshots to `metrics.json`, record promised
payments or refunds in `commitments.json`, and log pricing decisions. Run
`cf.py metrics` to surface stale or inconsistent records.

## Deliverable
A finance review with sources, cash position, revenue health, one recommendation
with alternatives, approvals needed and a professional packet where relevant.
Use `assets/templates/finance-review.md`.

## Done
The founder knows the current position, how confident it is and the next money
decision. A modelled scenario is not a forecast, a drafted reminder is not a sent
one, and a recommendation is not tax, legal or investment advice.

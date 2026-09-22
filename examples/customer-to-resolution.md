# Synthetic walkthrough: a repair action changes stock twice

This is an authored scenario, not a report from a real customer or executed model
benchmark. Its purpose is to demonstrate handoffs and evidence requirements.

## Request

“Completing a repair twice sometimes deducts two parts. Fix it without breaking
cancellation or reporting.”

## Co-founder workflow

`customer-care` records a sanitized issue and affected version. `impact-map` traces
repair completion, stock movement, retry behavior, reversal and reporting using
actual implementation evidence. Unknown modules stay unknown.

`build-fix` reproduces the problem in a synthetic fixture before changing code.
It identifies the transaction/idempotency problem, proposes the smallest remedy,
and waits for scope approval. It does not rewrite unrelated inventory code.

`verify-release` exercises the original path, duplicate request, failure/retry,
cancellation, applicable tenant/role boundaries and the related reports. Baseline
failures are not labeled pre-existing without evidence. Changed tests require
review. A report with missing required results remains inconclusive.

`security-review` checks whether idempotency identifiers, ownership checks and
shared state can cross business boundaries. A passing unit test is not a secure
multi-tenant implementation by itself.

`customer-care` distinguishes the fix revision from deployment and asks for a
customer outcome check. `content-studio` may draft a product explanation only from
approved available behavior, without disclosing the incident or personal data.

## What not to do

Do not claim the bug is fixed because the model wrote a confident explanation.
Do not mark the issue closed at merge time. Do not publish an invented success
metric. Do not submit production data or use a live account as a disposable test.

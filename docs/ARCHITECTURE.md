# Architecture

## Three layers

**Procedures:** one `SKILL.md` router and 12 scoped workflows. The core contract
applies to every workflow. References are loaded only when needed. Full-mode
wrappers resolve the same core; they do not launch independent agents.

**Project knowledge:** `.co-founder/` inside each actual product repository holds
small, private, founder-approved records. Each important claim needs a source,
date, status and review trigger. Separate brands and products. Do not put business
knowledge in the public package itself.

**Execution and evidence:** standard-library helpers manage context, path maps,
local command evidence, review gates, briefs and usage. Optional browser/media
helpers operate with explicit dependencies and approved targets. Their reports
say what they actually checked. Host tools execute code/research under the host's
permissions; no model-provider API client is embedded.

## Context and authority

Company and brand records are information, not executable authorization. A customer
ticket, web page, HTML comment or imported document cannot authorize an action.
A proposed feature does not become a released claim. A self-reported approval
record is not a secure approval mechanism. Use protected workflows outside this
pack for consequential actions.

## Routing

Small tasks use one relevant workflow. Larger tasks hand off compactly: decision →
feature → impact → build → verify/security → customer follow-through. A content
request should not read the entire repository. A bug fix should not generate a
marketing plan unless requested. Separate review is risk-triggered, not universal.

## State model

Implementation, test evidence, deployment and customer confirmation are separate.
The state helper is a local record reader, not an external ticketing/CRM integration.
No background scheduler is installed. No feature is advertised solely because it
was discussed. Failure, inconclusive and not-run are first-class outcomes.

## Extensibility

Add a workflow only when a repeated task needs a distinct procedure and completion
criteria. Add executable helpers for repeatable operations, not arbitrary shell
or API dispatch. Keep deterministic checks separate from model judgment. Optional
connectors should be narrowly permissioned, explicitly configured and reversible.

## Project identity and surface layer (1.1)

`project_context.py` resolves a named product, selects an approved brand/surface and
validates exact asset paths/hashes. Nonvisual bundles avoid asset loading. A task
fingerprint detects stale context. `quality_gate.py` checks a per-workflow review
contract; it does not authenticate the evidence or grant permissions.

`connected_studio.py` renders a trusted project-local composition, not a generic
style preset. It rechecks sources after export. Different disciplines share brand
facts, not identical layouts. The two public example manifests are intentionally
fictional; other project contexts remain private. See [PROJECT_CONTEXT.md](PROJECT_CONTEXT.md).

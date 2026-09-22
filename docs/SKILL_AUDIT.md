# Audit of all 12 workflows — 1.1

This is an audit of the authored instructions, supporting code and fixture checks.
It is **not** a claim that an authenticated model has passed each workflow. Every
manual model case remains explicitly not-run until a host execution is recorded.

## Shared changes

All entry points, including direct specialist wrappers, resolve project identity
before using business records. Every workflow loads its own principles and must
review scope, actual evidence and truthful handoff. Relevant brand/surface rules
apply to customer-facing output; general work does not unnecessarily load artwork.

Approval labels are declarations, not permissions. No external content can grant
access, change project identity, publish, send, spend, deploy or delete. Significant
product changes still require an impact/verification path. There is one active
workflow by default, not twelve model processes.

## Specialist audit

| Skill | Governing principles | Required evidence at handoff |
|---|---|---|
| Decide | Challenge the solution, compare the current state and smaller option; avoid confirmation bias and fake market precision. | Sources versus assumptions, alternatives, strongest objection and a falsifier/reconsideration trigger. |
| Feature plan | Design a complete stateful journey, not an isolated control; scope by customer value. | Main/recovery paths, permissions, business invariants, observable acceptance and exclusions. |
| Impact map | Trace data/events as well as imports; a maintained map is not omniscient. | Actual producers/consumers and source pointers; adjacent test matrix; unknown and newly changed areas. |
| Build/fix | Reproduce, falsify a hypothesis and make a bounded root-cause change. | Original failure, meaningful baseline, diff/test edits, executed retest and failed approaches. |
| Verify/release | Evidence before a completion claim; tests are not the whole user journey. | Criteria mapped to results, changed/skipped tests, environment/revision and distinct release states. |
| Security | Follow trust boundaries and deny paths, not scanner counts; minimize assistant permissions. | Synthetic role/tenant cases, relevant adversarial inputs, findings/remediation and untested surfaces. |
| UI polish | Task hierarchy and real states before decoration; honor the project's surface design language. | Actual captures, typography/density/contrast rationale, primary/recovery/mobile behavior and a concrete revision. |
| Customer care | Resolve the customer's outcome, not merely the internal ticket. | Impact/reproduction, known state/owner/next update, verified deployment status and truthful response. |
| Growth | Fix the actual funnel bottleneck; distinguish activity from outcomes. | Baseline, segment, hypothesis, measure/time/budget limit and verified public claims. |
| Sales | Establish fit, acknowledge limitations, use approved terms and actual recipients. | Customer need, real capability/offer, no invented concessions, and explicit draft/sent/replied states. |
| Content studio | One truthful visual concept, correct brand, discipline-specific craft and revision. | Asset binding, inspected references, actual export and observations; full playback/audio status for video. |
| Founder brief | Prioritize consequences using fresh evidence; reduce coordination. | Dates/timezone, a small feasible set of actions, stale/missing inputs and no invented automation. |

The precise criteria are in the per-workflow `references/principles/` files and
[review-contracts.json](../skills/co-founder/references/review-contracts.json).
The existing detailed workflows and engineering, security, research, flow and
commercial guides are retained; new gates supplement them instead of replacing
them with a superficial checklist.

## Enforced by helpers versus instructed behavior

**Executable:** manifest/brand/asset ID matching, bounded paths and inventory,
asset integrity, stale-lock rejection, review-record structure, conservative
installer behavior, test/config evidence helpers and declared media checks.

**Requires agent and reviewer execution:** research quality, actual business impact,
root-cause correctness, visual taste, whole-video pacing, external permissions and
reliable use of every instruction. A schema pass cannot authenticate a source,
verify an approval or guarantee the model obeys the workflow.

## Corrections discovered while building the examples

- The old universal layout failed the desired concept/craft standard. Featured
  exports were replaced, and the old renderer is explicitly legacy-only.
- Mobile row selection originally left details below the entire queue. It now opens
  a focused detail state, restores focus on return and has dedicated regression checks.
- The first new browser test reused JavaScript globals across inline documents.
  That produced a real test-harness error. Each fixture now gets a fresh page; the
  failed attempt is recorded in validation history rather than counted as a pass.
- Media receipts now report the actual PNG pixel dimensions and how many safe-bound
  elements exist. Zero marked elements yields zero safe-frame checks.
- Templates and assets are fingerprinted again after rendering to catch source drift.

## Release policy

Keep technical, behavioral, visual and owner-approval results separate. Do not claim
fully watched source films, model tests, customer fixes, or universal security from
this package's unit tests. Before public performance claims, run the live-host and
comparative cases in [ACCEPTANCE.md](ACCEPTANCE.md) using real permitted work.

# Subscription and token discipline

The goal is less total work per verified outcome, not a short answer hiding skipped
checks. No measured percentage saving is claimed for this release.

## Default execution

Use lite mode, one active agent and task-specific reading. Load the core contract
and one workflow, then only relevant references and project records. Avoid loading
the entire research catalog, all category playbooks or full historical logs into
every task. Use a fresh session/compact handoff for unrelated work.

Sources: [Codex progressive skill loading](https://developers.openai.com/codex/skills/)
and [Claude skill context behavior](https://code.claude.com/docs/en/skills).
Loaded instructions may remain in conversation context. Progressive discovery
is not automatic deletion of previous context.

## Reading budgets

```sh
python skills/co-founder/scripts/cf.py context --project "/path/to/product" --task fix --max-bytes 12000
```

This lists paths and byte sizes without dumping contents. It is a reading plan,
not a tokenizer or a host-enforced context limit. Read focused sections instead
of asking the model to summarize whole files repeatedly. Refresh volatile or
critical research; reuse well-sourced still-current decisions.

## Retry and review budgets

Two unsuccessful attempts should trigger reassessment with a compact evidence
record. Do not repeat the same patch or launch a committee. Deeper verification
remains appropriate for permission, money, inventory, tenant-isolation and schema
changes. Do not cut safety checks merely to meet a superficial token target.

## Record measured usage only

```sh
python skills/co-founder/scripts/cf.py usage --project "/path/to/product" --source "host-record-1" --input-tokens 1000 --cached-input-tokens 400 --output-tokens 300 --reasoning-tokens 100
python skills/co-founder/scripts/cf.py usage-summary --project "/path/to/product"
```

The numbers above are **syntax examples**, not package measurements. Our schema
expects input to include cached input and output to include reasoning. Map actual
provider fields correctly; leave unavailable fields unknown. Cached/reasoning
subsets are not added twice. The helper never calculates remaining subscription
quota, reads billing credentials or invents an API price equivalent.

There is no hard model-spend cap in a Markdown skill. Host-side limits and user
control remain the actual boundary. Bounded local scripts control their own work,
not the host's hidden reasoning or billing. Avoid paid API fallbacks entirely unless
the user separately requests and authorizes an optional integration.

## Project-aware reading (1.1)

Resolve identity once at a task boundary. Load the selected surface profile only
for creative work; a general bundle contains no asset media. Recheck a compact
fingerprint before a consequential handoff rather than rereading every image or
rebuilding company context every turn. Load only the selected workflow principles.
The full review-contract JSON is read by the local checker, not necessarily pasted
into the model prompt. Read relevant errors, not all reports.

Reuse an already accepted campaign direction until its project/scope/assets change.
Do not force repeated three-concept explorations for routine edits. A new visual
direction still needs genuine thought and review; a token budget is not permission
to skip security, mislabel a test or pretend to inspect a film.

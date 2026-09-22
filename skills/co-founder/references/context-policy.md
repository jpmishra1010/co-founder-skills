# Small, durable, private context

Each product gets its own `.co-founder/` directory. It is local working context,
not public source and not a source of executable authority. The initializer adds
an ignore rule. Existing tracked files are not made private by adding gitignore;
run doctor and remove/rotate exposed material through an approved process.

Read company.md first only when business context matters. Read product-map.json
for affected-module work, brand.json for creative work, claims.json for public
statements, and state.json for current tasks. Read decision/evidence records by
specific task ID. Do not concatenate everything into one system prompt.

Entries need date, source, status, and owner/review trigger when applicable.
Use verified / founder-confirmed / assumed / outdated / proposed explicitly.
The agent may suggest a correction; it cannot silently turn a hypothesis into a
released capability. Preserve superseded decisions and avoid duplicate logs.
Do not store secrets, raw mailboxes, production databases, or unnecessary personal
data. Summaries are still potentially sensitive when sent to a hosted model.

The helper's `context` command lists relevant paths and byte sizes; it does not
read file contents into its output or provide a model tokenizer. Read only what
is needed in the host. A fresh task should start from a short handoff, not a replay
of every past prompt. No vector database or autonomous memory service is required.

# Stop the speculative-fix loop

Create a compact reproduction: environment/version, role, initial state, exact
steps, actual result, expected result, and evidence. Reduce it safely; do not
remove the condition that causes the bug. Record what is not reproduced.

Keep a short hypothesis table:

| Hypothesis | Evidence that would support it | Check | Result | Next action |
|---|---|---|---|---|
| Example: route-specific stylesheet | Different loaded CSS after navigation | Inspect both routes | Not yet checked | Capture source/order |

Use one meaningful experiment at a time. Record rejected hypotheses so later
turns do not repeat them. A symptom disappearing after several simultaneous
changes does not prove which change fixed the cause.

Inspect boundaries: client/server, transaction, cache, tenant, event, clock,
network, persistent versus screen state. Compare direct load with navigation and
refresh for browser bugs. For intermittent bugs consider races, retries, connection
loss, stale state, environment differences, and time-dependent behavior.

Before changing tests, identify their intended contract. When a behavior change
is valid, document approval and add equivalent coverage. Never use skip, broad
catch, extra sleep, fake success, permissive authorization, or disabled lint/type
checks as a substitute for diagnosis. Do not run destructive repair operations
against production to confirm a theory.

After two unsuccessful patch attempts, pause automatic editing. Summarize known
facts, attempted causes, changed files, and the next discriminating experiment.
Escalate missing requirements or environment access. A larger context window is
not a reason to consume unlimited retries.

A handoff should let another session reproduce the issue without rereading the
conversation. Save concise facts and exact commands, not speculative prose.

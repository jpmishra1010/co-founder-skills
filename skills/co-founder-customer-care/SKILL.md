---
name: co-founder-customer-care
description: Use Co-founder customer-care in Claude Code or Codex to resolve customer issues beyond the code change. Reads the shared Co-founder workflow; no automatic external actions.
license: MIT
metadata:
  version: "1.1.1"
---
# Co-founder: Resolve customer issues beyond the code change

Read `../co-founder/references/core-contract.md` and
`../co-founder/references/project-identity.md`; resolve the project before acting.
Then read
`../co-founder/workflows/customer-care.md`. Both paths are relative to this skill folder.
The shared co-founder folder must be installed alongside this wrapper.
Use the existing host session and subscription. This is a workflow, not a
request to launch another agent or model process. Apply it to the user's
current request and read only relevant project context. Preserve host permissions.

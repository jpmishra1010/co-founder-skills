# Update from 1.0 to 1.1 without losing project knowledge

## Install the updated skills

From the new extracted source:

```sh
python3 scripts/install.py install --host codex --scope user --dry-run --update
python3 scripts/install.py install --host codex --scope user --update
```

Substitute `claude` or `both` as appropriate. Keep a backup of your own edits. The
installer refuses unmanaged/locally modified collisions rather than erasing them.
Do not bypass a refusal by deleting a folder without inspecting its contents.
Restart/refresh the host session after updating.

## Migrate each real project deliberately

The installer updates skills, **not** your project's `.co-founder/` records.
`cf.py init` only adds missing templates and preserves existing records. In
particular, an old schema-1 `brand.json` is not silently rewritten or approved.

Ask the agent to inspect your old company/brand records, actual design tokens and
owned assets in read-only mode. It should propose a stable project ID, separate
product/personal brands and applicable surface rules. Review conflicts, then
explicitly authorize a backup and schema-2 conversion.

Create/confirm `project.json` and `assets.json`, preserving existing business notes,
product map, decisions and state. Transfer approved old palette/typography only
when they still match the real project; missing facts remain unknown. Set approval
provenance to the real current confirmation, not the fictional fixture's author.
Register exact asset bytes/hashes. Never export customer data to a public example.

Run `project_context.py bundle` for the relevant surface. The new helper deliberately
rejects a schema-1 brand profile until migration is reviewed. Do not weaken that
check or copy the sample profile merely to silence an error.

## Creative changes

The old JSON diagram studio remains compatible but is marked legacy. Existing old
configurations are not automatically interpreted as a new brand profile. New work
should use the project-bound craft workflow and an appropriate tool/composition.
The new connected examples are reviewable fixtures, not a replacement identity.

## Verify

Use a disposable project to test correct project selection, changed-logo rejection,
missing-asset behavior, read-only requests and one bounded output in each host you
use. Run the [acceptance checklist](ACCEPTANCE.md). No live account test was performed
on your behalf. Keep the previous ZIP until your own smoke tests succeed.

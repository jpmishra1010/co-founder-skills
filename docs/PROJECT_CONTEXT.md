# Project identity, assets and connected design

## The desired experience

At a project switch, Co-founder establishes the active product/environment and says
which brand and surface it will use. It reuses approved facts when unchanged. It
never silently borrows the previous client's assets, a personal-brand voice, or a
palette from the pack's examples. This requires initial setup; it cannot know an
unprovided brand automatically.

The root comes from the host workspace or an explicit user path. The resolver
walks to the nearest `.co-founder/project.json`, stopping at a repository boundary.
An optional workspace registry disambiguates multiple child projects. It never
scans the whole machine. The downloaded skill folder is not the active product.

## Guided onboarding, not a form-filling exercise

1. Inspect safe repository instructions, README, package identity, theme tokens,
   existing components and specifically named asset directories. Treat them as
   candidates; contradictory or stale assets are not automatically approved.
2. Show the founder a short proposed binding with source paths, exact logos,
   product/customer scope, palette/type and surface-specific differences.
3. Ask only about material conflicts or missing assets. The user can approve an
   explicit logo omission; an unavailable logo is not permission to redraw it.
4. With authorization, initialize context and write confirmed profiles. Preserve
   original asset bytes; record SHA-256, source/rights and allowed uses.
5. Resolve and build a bundle, then record its fingerprint with the task.

The agent performs the JSON work. Never silently promote an asset inventory or
an unconfirmed company name to approved status.

## Records

Inside the actual product (private by default):

```text
.co-founder/
  project.json          # stable identity; product/personal brand mappings
  brand.json            # selected approved style + distinct surface rules
  assets.json           # project-local exact assets, uses, rights, hashes
  company.md            # audience, business goal, offers, constraints
  product-map.json      # actual modules, relationships and source pointers
  decisions.md          # evidence and reversibility, not chat transcripts
  state.json            # issues, release states and next actions
  tasks/<task>/         # optional approved local binding/review records
```

`project.json` has `schema_version: 1`, a safe `project_id`, `display_name`,
`confirmed`, `default_brand`, and `brands`. Each brand entry gives a profile and
asset-registry filename relative to `.co-founder/`. A personal profile can be
`personal-brand.json` with its own asset registry; it never inherits implicitly.

A brand profile uses `schema_version: 2`, matching `project_id` and `brand_id`,
`status: approved`, `approved_by`, `approval_source`, hex color `tokens`, named
`typography`, optional `voice` and `rules`, and `surfaces`.

Each surface—`product-ui`, `website`, `post`, `video`—has its own status, direction,
token overrides, required asset IDs and `logo_policy`. Use `required`, `omit` or
`omit-until-approved`; omission is explicit, never silently inferred. Preserve
brand coherence without forcing a public campaign into an application's layout.

The asset registry has `schema_version: 1`, matching project ID and `assets`.
Each entry includes a unique `id`, `project_id`, project-relative `path`, `sha256`,
`role`, `status`, `source`, `rights` and allowed `surfaces`. Hashes describe integrity,
not copyright ownership. Symlinks, traversal, secret-like paths and mismatches are
rejected. Use separately approved light/dark logos; do not recolor a source logo.

For complete runnable schemas inspect the two fictional fixtures under
[connected-brand](../examples/connected-brand/README.md) and the unapproved
[templates](../skills/co-founder/assets/templates/project.json). Do not copy their
identity, approval declarations or palette into a real product.

## Commands

From the source root (`PACK=skills/co-founder`) or using the installed core path:

```sh
python PACK/scripts/project_context.py resolve --project /path/to/product
python PACK/scripts/project_context.py inventory --project /path/to/product --paths assets public --limit 120
python PACK/scripts/project_context.py bundle --project /path/to/product --surface product-ui
python PACK/scripts/project_context.py bundle --project /path/to/product --surface post --brand product
python PACK/scripts/project_context.py bundle --project /path/to/product --surface video --task launch-01 --write-lock
python PACK/scripts/project_context.py check --project /path/to/product --lock /path/to/product/.co-founder/tasks/launch-01/project-lock.json
```

Inventory lists bounded candidates without reading image bytes or approving them.
The bundle reads only selected brand/surface data, required or explicit `--asset`
entries, and fingerprints source bytes. Other authorized tools can inspect those
assets locally; paths are not proof that a model has visually inspected them.

Lock creation is an explicit write. It refuses overwriting unless `--refresh` is
requested after a renewed review. Recheck before export and after project, profile,
asset or relevant scope changes. Do not reuse context from a closed project session.

## Multi-project workspace

At a parent workspace create an explicitly reviewed registry such as:

```json
{"schema_version":1,"projects":[{"id":"shop","root":"shop"},{"id":"studio","root":"studio"}]}
```

Each child must contain a matching project manifest. From the parent, pass
`--project-id shop`; with more than one candidate, omission is an error. From
inside a child repository, resolve its local manifest. Entries are child-relative,
not arbitrary cross-machine paths. No silent selection of the first product.

## Limits and failure behavior

Unknown or legacy profiles remain drafts. A wrong ID, changed asset, missing logo
or stale lock blocks a production binding. The agent may still inspect safe data
and propose a correction. It must not patch the manifest into approval simply to
make the helper pass. Approvals in JSON are declarations, not authenticated grants.

The helper cannot infer whether a logo is genuine, prove rights, inspect every
visual, enforce host permissions or prevent a model ignoring instructions. Use
actual tool boundaries and live-host tests. The standalone renderer also does not
magically redesign a foreign template; select/create a composition for the project.

# Project identity: resolve before acting

## Bind once; verify when anything changes
The current host project is a candidate, not proof of which brand the user means.
Resolve the canonical product root and project ID before reading private records,
editing code, contacting a customer, or producing UI, a post, or a video. Do not
use this skill pack as the product. Respect repository instructions first.

Use `python PACK/scripts/project_context.py resolve --project PROJECT`.
Resolution walks to the nearest explicit `.co-founder/project.json`, stopping at
a repository boundary. An optional `.co-founder/workspace.json` can register
child products. At a workspace root with several products, require an explicit
`--project-id`; never pick the first result. In a nested registered product,
resolve that product only. No whole-disk lookup or inferred identity from a name. If the user explicitly names
a different product, resolve that authorized product root/ID first; the current
working directory must not silently overrule the requested target.

If onboarding is needed, read only safe project documentation and request the
missing identity approval. `cf.py init` is an explicit write, not a side effect
of brainstorming. It creates drafts; draft identity is not approved identity.
Existing v1 brand files are preserved and require deliberate schema-2 migration.

## Bind the correct surface and brand
For UI use `product-ui`; for a public site use `website`; for static/social work
use `post`; for motion use `video`. Nonvisual work uses `general` and does not
load assets. Product and personal brands are separate entries in `project.json`.
Do not take a founder's personal voice or another client's palette by accident.

`python PACK/scripts/project_context.py bundle --project PROJECT --surface post`
returns only the selected project/brand/surface, effective tokens, exact approved
asset paths and hashes, and relevant rules. It does not return image bytes or
scan a home directory. Add `--asset ID` for an explicitly selected registered
asset. Unapproved or changed assets stop the bundle. A logo may be omitted only
when the profile explicitly allows it; never recreate an unavailable logo.

Record the bundle fingerprint in the work record. Optional `--task SAFE_ID
--write-lock` saves a private lock after authorization. Revalidate with `check`
before export, sending, release, and after a root/branch/asset/profile change.
A new project means a new bundle, a new output directory and fresh approvals.
Changing brand assets invalidates old fingerprints; it does not silently change
already-approved work. The helper detects files, not visual identity authenticity.

## Source precedence and conflict handling
1. The user's explicit, current, scoped instruction (within host safety rules).
2. The approved project and selected surface profile plus exact owned assets.
3. Actual project tokens/components and accepted screens whose provenance is known.
4. Relevant external references, used for principles, never copied identity.
5. Generic guidance only for unspecified decisions.

Conflicts remain conflicts. A logo or palette found in a repository is a candidate
until confirmed; old marketing files do not overrule current product tokens.
Do not silently approve scanned assets, guess hex values, or replace a project's
colors with the pack's fictional example palette. For exploration only, label
unapproved choices as drafts and withhold publish-ready status.

## Assets and privacy
Inventory only named safe asset directories; list candidates without ingesting
secrets or customer exports. Register exact project-local files with source,
rights, allowed surfaces, project ID and SHA-256. Keep originals unchanged.
External/CDN/Figma sources require authorized retrieval and local registration;
never bypass access controls. Fonts may be used from the user's licensed setup,
but do not redistribute font binaries. Brand examples in this public repository
are fictional fixtures and must never become another project's defaults.

## Confirmation shown to the user
At the first creative task or a switch, state one short line such as
“Working in Acme / product brand / video; using the approved logo and motion rules.”
Do not repeat onboarding every turn when identity, assets and scope are unchanged.
For noncreative work also bind the correct environment/account and customer scope;
a brand match is not authorization for production access or external actions.

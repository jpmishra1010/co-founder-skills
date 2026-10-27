# Start here — Co-founder 1.1.1

## 1. Keep your existing subscription

Use your current Codex or Claude Code account. Co-founder does not change login,
read authentication files or call a model-provider API. Check the host's active
login method; an API key and subscription login can have different billing.
Use `codex login status` or Claude Code's `/status`. Never paste keys into chat.
See [host documentation](docs/HOSTS.md).

## 2. Install with npx

For a fresh installation, extract the ZIP and open a terminal **inside the
extracted `co-founder` folder**. Run:

```sh
npx skills add ./skills/co-founder --agent codex claude-code --global
```

Remove `claude-code` or `codex` to target only the host you use. This command needs
Node.js/npm and the external skills CLI. It installs all 13 workflows behind the
main entry; you do not need a custom Co-founder npm package.

To install straight from the published GitHub repository instead:

```sh
npx skills add jpmishra1010/co-founder-skills --skill co-founder --agent codex claude-code --global
```

**Python 3.10+ is still needed for the bundled project-context, integrity and evidence
helpers.** Switching the installer to npx does not convert their implementation to
JavaScript. If Python is missing, the agent must report that dependency before
claiming those checks ran; it must not bypass project/asset binding.

Already installed with the Python installer? Follow the
[manager-switching procedure](docs/INSTALLATION.md#switching-from-the-python-installer)
first; preserve customizations and keep one manager per installation. For offline
installation, retain the [Python fallback](docs/INSTALLATION.md#offline-python-fallback).
Neither route changes model authentication or grants extra tool permissions.

## 3. Open your product—not this pack

Use `$co-founder` in Codex CLI/IDE, `/co-founder` in Claude Code, or the host's
skill picker. Refresh/restart the host session if it has cached the old skill.

```text
Work on the project currently open in this workspace.
Inspect its safe README, existing design tokens and asset folders in read-only mode.
Establish the product identity and show me any conflicting brands or old assets.
Do not edit code, read secrets, install tools or assume brand colors from memory.
```

The agent should propose a compact identity summary, not ask you to hand-write
JSON. If several products are present, select one explicitly. Missing assets or
conflicting palettes need a decision before a branded output is called ready.

## 4. Approve a small project profile once

After you authorize initialization, the agent can run the installed helper:

```sh
python PACK/scripts/cf.py init --project /absolute/path/to/product
```

Here `PACK` means the installed `skills/co-founder` directory, not the product root.
From the downloaded source it is `skills/co-founder`. Replace placeholders with
actual paths; quote paths containing spaces. Initialization creates drafts and an
ignore rule, preserves existing records, and does not approve unknown facts.

Confirm a project ID/name, business goal, intended customers, default brand, actual
logo assets, source design tokens, typography, language and relevant surface rules.
The agent records those exact local paths and hashes after inspecting the assets.
Use separate `product` and `personal` brand entries when needed. Do not invent a
logo, license, claim or palette because a field is empty.

[Project/context schema and examples](docs/PROJECT_CONTEXT.md)

## 5. Verify the binding

```sh
python PACK/scripts/project_context.py bundle --project /absolute/path/to/product --surface post
```

Use `product-ui`, `website`, `post`, `video` or `general`. The result identifies the
project, selected brand, surface, tokens, assets and fingerprint. General work does
not load brand assets. The first task or a project switch should begin with a short
confirmation such as “Working in Acme / product brand / video.”

## 6. Use normal requests

```text
Improve this screen using this project's approved design language.
Preserve the workflow. Inspect the result on mobile and desktop before handing off.

Prepare a post about this verified feature. Use our exact assets and post rules.
Show the concept before final production if this is a new campaign direction.

Create a video from the approved concept. Preserve object continuity, vary pacing
with the story, and report which playback/audio checks were actually performed.

Investigate this customer issue. Reproduce it, check connected modules, make the
smallest approved fix, then verify the original and adjacent behavior.
```

Approved brand directions can be reused without repeating onboarding. Changes to
assets, project, surface or scope require a fresh binding/check.

## 7. Preview and test

The new [connected examples](examples/connected-brand/README.md) open locally.
Image/video rendering is optional and requires explicit dependencies; see
[MEDIA.md](docs/MEDIA.md). Co-founder does not automatically download media dependencies or call model APIs.
The separate npx installation route can download the external skills CLI and skill source.

Run [host acceptance](docs/ACCEPTANCE.md) in a disposable project before relying on
model-driven execution. The supplied tests verify helpers and fixtures, not perfect
model compliance. Daily briefs are on demand unless you separately configure a
supported scheduler. Nothing is automatically sent, published, deployed or spent.

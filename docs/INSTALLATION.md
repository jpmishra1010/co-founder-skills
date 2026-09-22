# Installation, updates and removal

## Recommended: npx skills add

Co-founder is a standard directory-based skill collection. The recommended public
installation uses the independently maintained [skills CLI](https://github.com/vercel-labs/skills).
Vercel's [agent-skills](https://github.com/vercel-labs/agent-skills) and Remotion's
[skills](https://github.com/remotion-dev/skills) document this same distribution route.
Checked against public documentation on 2026-09-23. See [distribution validation](DISTRIBUTION_VALIDATION.md)
for what was actually executed versus checked against documentation.

### Fresh installation from this ZIP

Extract the source; open a terminal in the extracted `co-founder` folder:

```sh
npx skills add ./skills/co-founder --agent codex claude-code --global
```

Use just one agent name to target only that agent. Leave confirmation prompts
active and review destinations. `--copy` requests copies instead of links. Do not
use administrator privileges just to install user skills.

### Installation from GitHub after publication

Replace the owner/repository placeholder with a repository you have actually published:

```sh
npx skills add YOUR_GITHUB_OWNER/YOUR_REPO --skill co-founder
```

To explicitly target both hosts at user scope:

```sh
npx skills add YOUR_GITHUB_OWNER/YOUR_REPO --skill co-founder --agent codex claude-code --global
```

For a project-scoped install, run from the actual product directory, use the GitHub
source or an absolute path to the extracted `skills/co-founder` directory, and omit
`--global`. Do not accidentally choose project scope while standing in the pack
repository. Inspect resulting tracked files before committing them.

### Dependencies: installation is not execution

| Operation | Requirements |
|---|---|
| npx installation | Node.js/npm, external skills CLI (download or existing cache); Git/source access when applicable. |
| Read skill instructions | The supported host; no Python interpreter is needed just to read Markdown. |
| Execute project/brand, integrity, evidence and review helpers | Python 3.10+; this dependency was not removed or rewritten. |
| Optional browser/image/video exports | Explicit browser/media dependencies listed in [MEDIA.md](MEDIA.md). |
| Model work | Your chosen host/account; no mandatory separate model API is added by this pack. |

`npx` executes an npm-distributed CLI, which obtains skill files from the supplied
source. It does not require Co-founder itself to be published on npm. Do not use
`npm install co-founder`: this project has not published or authorized a package
under that name, and it could refer to someone else's software.

The selected skill folder contains its instructions, workflows, references, assets,
Python helpers and license. Repository-only example videos and documentation are
not required for the installed helpers. Keep the full source checkout to browse
those examples or run the full maintainer test suite.

## Main skill versus optional shortcuts

`--skill co-founder` installs the full working system with all 12 internal workflows.
It does not load all workflows into every conversation. This is the recommended
low-clutter entry point.

Optional `co-founder-*` skills are wrappers. They refer to the sibling `co-founder`
folder, and the external CLI does not automatically resolve this dependency. Always
include the main skill when installing a shortcut:

```sh
npx skills add YOUR_GITHUB_OWNER/YOUR_REPO --skill co-founder co-founder-ui-polish --agent codex claude-code --global
```

To inspect entries first:

```sh
npx skills add YOUR_GITHUB_OWNER/YOUR_REPO --list
```

Avoid `--all` as a default: the CLI documents that this selects all skills/all agents
and skips prompts. The package only documents host-specific acceptance for Codex
and Claude Code, not every host recognized by the external installer.

## Updates and removal for npx-managed installations

Use the same manager that created the install. The external CLI documents commands
such as `npx skills list`, `npx skills update` and `npx skills remove`. Review their
interactive selections and current help; back up local modifications first. Do not
assume the external tool shares this pack's Python backup/collision guarantees.

For local-path installs, re-run `skills add` from a newly extracted reviewed release;
do not assume an unpublished local directory has an upstream update source. For
GitHub installs, verify the source, target version and installed files after updating.
Updating already installed skills is not a promise that newly introduced shortcuts
will also be installed.

Skills CLI can use canonical copies and links to host locations, and path choices
can evolve. Follow its actual installation summary, not an assumed path. Check for
duplicate Co-founder entries at both project and user scope. Start a fresh host
session when required and perform [host acceptance](ACCEPTANCE.md).

## Switching from the Python installer

Do not overwrite an existing installation blindly with a different manager.

1. Close active tasks using the old skill. Back up any customized installed skill
   files. Private product `.co-founder/` context is separate and must be preserved.
2. From the old/source repository, inspect the Python manager's status with the
   same host and scope used at installation:

   ```sh
   python3 scripts/install.py status --host both --scope user --mode full
   python3 scripts/install.py uninstall --host both --scope user --mode full --dry-run
   ```

   Replace `both`/scope with what you actually used. For project scope also supply
   `--project "/absolute/path/to/product"`. Inspect unmanaged-directory errors;
   never force-delete another tool's install.
3. After confirming the plan, run the same uninstall without `--dry-run`. This
   manager backs up its managed files. If it reports local edits, preserve/reconcile
   them before deliberately using its documented options. Do not use `--force`
   casually or treat it as a way to remove unmanaged files.
4. Install with the npx command. Verify there is one intended main entry and that
   any optional wrappers can resolve it. Keep using the external CLI for that install.

The Python installer intentionally refuses linked or unmanaged destinations. It
cannot safely adopt a skills-CLI installation merely by adding `--update`.
Nothing in this procedure deletes private product records or changes host login.

## Offline Python fallback

The existing conservative installer is retained unchanged. After obtaining and
reviewing this archive, it uses only Python's standard library; it does not fetch
packages, run model calls, or change host settings.

```sh
python3 scripts/install.py install --host codex --scope user --dry-run
python3 scripts/install.py install --host codex --scope user
```

Use `claude` or `both` for this manager (the external CLI instead uses `claude-code`).
`--mode full` adds optional wrappers; lite already includes every workflow. To update
an installation owned by this Python manager, add `--update`, inspect a dry-run,
and then execute the reviewed plan. Local edits cause a refusal unless backed-up
replacement is explicitly authorized. Keep the source for updates/removal.

Python manager's fixed destinations: user/project `.agents/skills/` for Codex and
`.claude/skills/` for Claude Code. Backups use `.co-founder-backups/` outside the
skills scan directory. It rejects symlinks/junctions, including linked parent paths.
Its guarantees apply to this installer, not to a third-party CLI.

## External CLI telemetry and supply-chain note

Co-founder code has no telemetry. The skills CLI documents anonymous telemetry and
its own opt-out; these are separate. For example, on macOS/Linux:

```sh
DISABLE_TELEMETRY=1 npx skills add ./skills/co-founder --agent codex --global
```

In PowerShell, set `$env:DISABLE_TELEMETRY='1'` before the command. Review the
[CLI documentation](https://skills.sh/docs/cli). Review the npm package and source
before execution; use an explicitly reviewed CLI version for a reproducible rollout.
No registry-backed CLI execution was completed in the package-build environment.
There is no claim of a fresh live supply-chain audit.

## Troubleshooting

A visible skill is not proof all helpers can execute: check Python and optional
runtimes separately. Report a missing dependency rather than claim a check passed.
Do not bypass brand/asset integrity because installation itself succeeded.

If a skill is not discovered, inspect the install summary, duplicate scopes and
host settings. Do not expose credentials or disable host safety to fix discovery.
If the registry is inaccessible, use a permitted cached CLI or the reviewed offline
Python route; do not disable organizational network controls.

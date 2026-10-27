# Publish this pack to GitHub

This folder is the public project. Your product repository and its private
`.co-founder/` context are separate. Nothing has been uploaded on your behalf.

## Before publication

Run local validation/tests and review the included validation limitations. Inspect
Git status and the archive contents for private data. Keep LICENSE/NOTICE, original
source and attribution links. Remove environment-specific scratch files, caches,
credentials and proprietary examples. No external reference media or font files
should be added without appropriate rights.

Create a new empty repository using your GitHub account. A descriptive name such
as `co-founder-skills` may be clearer than a generic name; availability/trademark
clearance is not established here. Do not claim official provider affiliation.

From this folder, replacing the remote with your actual repository URL:

```sh
git init
git add .
git diff --cached --stat
# Review staged content before committing.
git commit -m "Initial Co-founder skill pack"
git branch -M main
git remote add origin https://github.com/jpmishra1010/co-founder-skills.git
git push -u origin main
```

For a fork, use your own repository URL instead. Alternatively use GitHub's reviewed
upload workflow, ensuring hidden files such as `.github/` and `.gitignore` are
included. Upload the extracted source, not only a ZIP, so people can inspect it.

## Set the public installation command

The public repository is `jpmishra1010/co-founder-skills`. If it is renamed, moved or forked, update
the install commands in README, START_HERE, docs/INSTALLATION.md and the landing
page in `docs/site/`. Public installation is:

```sh
npx skills add jpmishra1010/co-founder-skills --skill co-founder
```

No separate npm publication, npm token, custom installer executable, or package.json
is needed. `npx` obtains the external skills CLI; that CLI reads this GitHub skill
repository. Preserve the `skills/co-founder/SKILL.md` path and all its supporting
files. Do not place another `SKILL.md` at the root that shadows the collection.

Before announcing the command, test it from a fresh disposable directory and an
isolated user profile against the actual published repository. Record CLI/version,
discovered skills, installed paths, helper execution, update/removal and live-host
acceptance. The build environment could not reach npm, so that remote installation
is not represented as already tested. See [distribution checks](DISTRIBUTION_VALIDATION.md).

## Repository settings you must configure

Enable private vulnerability reporting where available. Choose maintainers,
review/branch rules and who may approve changes. Do not describe safeguards as
active merely because this document recommends them. The included CI runs tests
without model credentials; review action pins and allow GitHub to execute it.
No workflow with write access or `pull_request_target` is included.

## First public description (suggested)

“An open-source solo-founder skill pack for existing Codex and Claude Code sessions:
research, product flows, regression-aware changes, security review, design, support,
growth, sales and creative production. No mandatory model API or hosted service.”

Publish honest validation details. The included 24-second silent demo and original
connected examples illustrate the workflow; they are not measured evidence of user
outcomes. Do not advertise perfection, guaranteed token savings, security
certification, virality or fully watched reference films.

After live host smoke tests, attach the tested version and record any remaining
compatibility issues. Use GitHub releases for reviewed archives and checksums.
Consider a prerelease designation until external founders validate real tasks.

## Hidden synthetic manifests

Include the three exact JSON files inside each fictional example's `.co-founder/`
directory; they are required by tests and intentionally unignored. Every other
project context remains ignored. Do not replace these fixtures with actual customer
context. Hidden-file upload tools can omit them, so `git add .` plus staged-content
review is preferable. Inspect `git status --ignored` and run tests after cloning.

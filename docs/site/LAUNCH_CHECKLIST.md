# Search and launch checklist (draft for owner approval)

Nothing below has been done. Each item changes something public, so each needs the
owner's explicit approval, and the owner should do the submissions and posts
personally. Drop this file before committing if it should stay private.

**No ranking is guaranteed.** Google states that no site is guaranteed to be indexed
or ranked first ([SEO starter guide][starter]). The work below improves how clearly
search engines and AI assistants can read the project, and how many relevant places
link to it. Whether it reaches the top three for any phrase also depends on
competing pages and on real adoption, and neither is under the project's control.

Checked on 2026-10-27. The repository `jpmishra1010/jp-the-co-founder` is public, with
no description, no topics, no homepage, no Pages site and 0 stars. The first commit is
from 2026-09-23.

## 0. Blockers (resolve first, in this order)

- [x] **Decide the final repository name:** `co-founder-skills`. The docs and
  landing page now use `jpmishra1010/co-founder-skills`.
- [x] **Rename the repository** from `jp-the-co-founder` to `co-founder-skills`
  (done 2026-10-27; the old URL redirects, and the local `origin` points at the new
  one). GitHub does not redirect Pages project URLs after a rename ([renaming a
  repository][rename]), so publish the landing page only under the new name.
- [ ] **Test the public install command** from a fresh directory, as
  [PUBLISHING.md](../PUBLISHING.md) requires, before announcing it anywhere.
- [ ] **Land the finance workflow.** The README and landing page now list 13 workflows,
  including `finance`, which is still uncommitted work from another session.
- [ ] **Regenerate `FILE_MANIFEST.json`** for the release. It does not yet cover the
  new files.

## 1. GitHub repository settings

- [ ] **Description:** "Open-source Claude Code and Codex skills for solo founders: one
  co-founder skill with 13 workflows for product, releases, support, sales, finance
  and content. No hosted service or telemetry."
- [ ] **Website:** the GitHub Pages URL, once it is live.
- [ ] **Topics.** GitHub allows up to 20, using lowercase letters, numbers and
  hyphens, each 50 characters or fewer ([topics][topics]). Proposed:
  `claude-code`, `claude-code-skills`, `claude-skills`, `codex`, `codex-skills`,
  `agent-skills`, `skills`, `solo-founder`, `founders`, `indie-hacker`, `startup`,
  `ai-agents`, `developer-tools`.
- [ ] **Social preview image**, made and inspected together with the `og:image` card.

## 2. Landing page

- [ ] Approve publishing `docs/site/index.html`. A `gh-pages` branch is the
  recommended route; see the [site README](README.md).
- [ ] After it is live, verify the site in Google Search Console and request
  indexing. Google suggests Search Console for finding technical issues ([AI
  features][ai]).
- [ ] Link the page from the README and from the repository's Website field. Google
  finds most pages through links ([SEO starter guide][starter]).

## 3. Directories and lists (submit personally, one at a time)

| Where | How listing works | Fit right now |
|---|---|---|
| [skills.sh][skillssh] (Vercel) | Ranked by anonymous install telemetry from the `skills` CLI; no submission form was found ([docs][skillsdocs]). | Appears through real `npx skills add` installs. Do not generate installs artificially. |
| [travisvn/awesome-claude-skills][travisvn] | Pull request. Needs about 10 stars or it is closed automatically. The PR must not be generated or submitted with AI assistance. One skill per PR ([CONTRIBUTING][travisvn-c]). | Not yet: 0 stars. The owner must write the PR personally. |
| [hesreallyhim/awesome-claude-code][hesreallyhim] | Web UI issue form only, filed by a person. The resource must be 14 days old with active development, or have 100 stars. Factual one-line description, no sales pitch ([CONTRIBUTING][hesreallyhim-c]). | Eligible by age. The owner must file it. |
| [VoltAgent/awesome-agent-skills][voltagent] | Pull request with a description of 10 words or fewer, titled `Add skill: author/skill-name`. Requires real community adoption; brand-new skills are not accepted ([CONTRIBUTING][voltagent-c]). | Later, after adoption. |
| [ComposioHQ/awesome-claude-skills][composio-claude] | Pull request creation is restricted to collaborators. | Probably not open to outside submissions. Check before trying. |
| [ComposioHQ/awesome-codex-skills][composio-codex] | No contribution process found. | Check the repository before trying. |
| [openai/skills][openai-skills] | Its README says the repository is deprecated and points to OpenAI's plugins repository. | Not a target. |

Draft one-line entry, to reword personally: "Co-founder: one entry skill and 13
evidence-based workflows for solo founders in Claude Code and Codex."

## 4. Launch post plan

Write the posts personally. Several venues reject AI-written submissions, and every
claim must stay honest: no ranking, revenue, traffic or "proven" outcome claims.

- [ ] **Show HN.** It qualifies because people can install and try it without signing
  up. The title must start with "Show HN". Asking anyone to upvote or comment is
  not allowed ([Show HN rules][showhn]). Post only after the install command is
  tested.
- [ ] **A short write-up** (personal blog or dev.to): the problem, how one entry skill
  routes to 13 workflows, what it does not do, and what is untested in live sessions.
  This gives other sites something substantial to link to.
- [ ] **Communities** where Claude Code and Codex users gather, such as relevant
  subreddits or Discord servers. Read each venue's self-promotion rules first, post
  once, and stay to answer questions.
- [ ] **Personal channels** (X, LinkedIn): a short demo of one real workflow on the
  fictional Northline example, linking to the repository.
- [ ] Two to four weeks after launch, revisit section 3 for lists with star or
  adoption thresholds.

[starter]: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
[ai]: https://developers.google.com/search/docs/appearance/ai-features
[rename]: https://docs.github.com/en/repositories/creating-and-managing-repositories/renaming-a-repository
[topics]: https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/classifying-your-repository-with-topics
[skillssh]: https://skills.sh
[skillsdocs]: https://skills.sh/docs
[travisvn]: https://github.com/travisvn/awesome-claude-skills
[travisvn-c]: https://github.com/travisvn/awesome-claude-skills/blob/main/CONTRIBUTING.md
[hesreallyhim]: https://github.com/hesreallyhim/awesome-claude-code
[hesreallyhim-c]: https://github.com/hesreallyhim/awesome-claude-code/blob/main/CONTRIBUTING.md
[voltagent]: https://github.com/VoltAgent/awesome-agent-skills
[voltagent-c]: https://github.com/VoltAgent/awesome-agent-skills/blob/main/CONTRIBUTING.md
[composio-claude]: https://github.com/ComposioHQ/awesome-claude-skills
[composio-codex]: https://github.com/ComposioHQ/awesome-codex-skills
[openai-skills]: https://github.com/openai/skills
[showhn]: https://news.ycombinator.com/showhn.html

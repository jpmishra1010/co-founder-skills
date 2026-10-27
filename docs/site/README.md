# Landing page

`index.html` is a single static page for search engines and people who arrive
from a search. It is published from the `gh-pages` branch, which `main` does not
update automatically. It loads no web fonts, analytics or external requests. One
small inline script copies the install commands and rotates the illustrative
terminal examples. All the text is in the HTML, so the page reads fully without
the script. The terminal is labelled "Illustrative session": it shows how routing
works, not a recorded transcript.

## Before publishing

1. `index.html` assumes the repository `jpmishra1010/co-founder-skills` and the
   project-site URL `https://jpmishra1010.github.io/co-founder-skills/`. If either
   changes (for example a custom domain), update the canonical, `og:url` and JSON-LD
   together. A wrong canonical points Google at a page that does not exist.
2. Keep the visible text and the JSON-LD in step. If a workflow, version or license
   changes, update both.
3. Make and inspect a 1200×630 social card before adding `og:image`. Geometry
   checks do not establish that it looks right.
4. The page was checked in a local preview at 1280 px and 375 px wide, in light
   mode and in dark mode (forced through `data-theme="dark"`): no horizontal
   scrolling, and 16 px side gutters on phones. It respects
   `prefers-reduced-motion`. It has not been checked in Safari or on a real phone.

## How to publish on GitHub Pages

GitHub Pages can publish from the repository root or a `/docs` folder on a branch,
or from a custom GitHub Actions workflow ([GitHub Docs][pages-source]). This page
sits in `docs/site/`, so it needs one of these:

- **A `gh-pages` branch** containing only `index.html` at its root, published from
  that branch. This needs no workflow file. It is the recommended option.
- **A Pages workflow** that uploads `docs/site/`. That workflow needs `pages: write`
  and `id-token: write`, which changes the repository's current "no workflow with
  write access" stance in [PUBLISHING.md](../PUBLISHING.md). Review that first.

Publishing `/docs` from `main` is not recommended: it would publish all the
Markdown documentation under the same site.

## What the markup does and does not do

These points follow Google Search Central as checked on 2026-10-27.

- **Title and description.** Google builds title links from the `<title>` element
  and headings. It asks for descriptive, concise, distinct titles without keyword
  stuffing ([title links][title]). Snippets mostly come from page text, and the meta
  description is sometimes used ([SEO starter guide][starter]).
- **Canonical.** The canonical uses an absolute URL in `<head>`, and the page is
  self-referential, as Google recommends ([canonical URLs][canonical]).
- **No meta keywords.** Google Search does not use the keywords meta tag ([SEO
  starter guide][starter]).
- **Structured data.** `SoftwareSourceCode` is a [schema.org type][schema] that
  describes the repository, language, license and target products. Google does not
  list it in its rich result gallery ([search gallery][gallery]), so it will not
  produce a rich result. It only helps machines read the page. The "Software app"
  rich result needs a price plus a rating or review ([software app][software]).
  This pack has no ratings, so they are not invented. Google requires markup to
  match visible content and says valid markup never guarantees a feature
  ([general guidelines][policies]).
- **AI Overviews and AI Mode.** Google says there are no extra requirements, no
  special schema and no AI text files needed. Crawlable text, internal links and
  accurate structured data are what matter ([AI features][ai]).
- **No ranking guarantee.** Google says no site is guaranteed to be indexed or
  ranked. Links from other sites and real community engagement help pages get
  discovered ([SEO starter guide][starter]).

[pages-source]: https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site
[title]: https://developers.google.com/search/docs/appearance/title-link
[starter]: https://developers.google.com/search/docs/fundamentals/seo-starter-guide
[canonical]: https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls
[schema]: https://schema.org/SoftwareSourceCode
[gallery]: https://developers.google.com/search/docs/appearance/structured-data/search-gallery
[software]: https://developers.google.com/search/docs/appearance/structured-data/software-app
[policies]: https://developers.google.com/search/docs/appearance/structured-data/sd-policies
[ai]: https://developers.google.com/search/docs/appearance/ai-features

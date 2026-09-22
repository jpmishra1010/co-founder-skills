# Project-bound media and optional local rendering

Core skills/installer have no pip dependencies. The optional connected HTML exporter
uses Python Playwright/Chromium; silent MP4 export also needs FFmpeg with libx264.
No model API is called. Dependencies and external services are never installed or
activated automatically.

## Open the new examples

- [Working UI](../examples/connected-brand/previews/ui.html)
- [Campaign composition](../examples/connected-brand/previews/post.html)
- [Motion with play/scrub controls](../examples/connected-brand/previews/motion.html)
- [Rendered silent MP4](../examples/connected-brand/previews/motion.mp4)

Downloaded HTML can be opened locally. GitHub source links do not host a running
app. Source assets, profiles and templates live beside the examples. UI state is
in-memory only and resets when a fresh document opens; no backend or accounts.

## Explicit optional dependency setup

Use a trusted environment and review package/tool licenses:

```sh
python -m venv .venv
# Activate the virtual environment in your shell.
python -m pip install -r requirements-media.txt
python -m playwright install chromium
```

These are deliberate network downloads, not part of normal skill installation.
Install FFmpeg using your trusted platform workflow. Use `--browser /path/to/chromium`
for an existing browser. Fonts are read from the machine, never downloaded or
bundled by the exporter; fallback metrics may change, so inspect local renders.

## Build a project-specific composition

Create a **trusted, project-local HTML template** for the actual brief. It must
contain exactly one `__BRAND_JSON__` token. `connected_studio.py` substitutes the
resolved project ID, selected surface tokens/type and exact required approved
assets. JSON is escaped against script-tag termination; imported SVG assets use a
restricted static subset. This is not a sanitizer for arbitrary HTML/JavaScript.
Read templates before executing them. Browser request blocking is not a full
security sandbox. The host's execution controls still apply.

From this source root, a reproducible fictional example:

```sh
python skills/co-founder/scripts/connected_studio.py build --project examples/connected-brand/northline --template post.html --surface post --out rendered/post.html
python skills/co-founder/scripts/connected_studio.py export --project examples/connected-brand/northline --template post.html --surface post --out rendered/post.png
python skills/co-founder/scripts/connected_studio.py export --project examples/connected-brand/northline --template ui.html --surface product-ui --out rendered/ui.png --width 1440 --height 1000
python skills/co-founder/scripts/connected_studio.py export --project examples/connected-brand/northline --template motion.html --surface video --out rendered/motion.mp4
```

Outputs must be new unless `--overwrite` is explicitly passed. For a real project,
use its own root and authored template—not this fictional sample's brand or claims.
Before export, identity, profile, allowed asset uses and SHA-256 are checked. Before
handoff, the helper rechecks whether the brand/assets/template changed while it
rendered. No receipt can prove a visual concept is good or a brand owner approved it.

## Video contract and checks

A video template exposes `window.motionSpec` with fps, seconds, width and height,
and deterministic `window.renderAt(seconds)`. An artboard uses `id="stage"`.
`[data-safe]` marks elements for bounding-box checks. Decorative overscan can be
intentional; mark content, not every effect. Receipts report how many marked
items were checked. **No markers means zero safe-frame checks**, not a vacuous
quality pass. UI behavior/contrast and full audiovisual review are separate work.

The sample has 24 seconds at 1280×720 and 30 fps, with 720 deterministic frames.
It is silent. It contains no copied product screens or reference-film assets.
Add only authorized audio, retime captions and review the final combined export.
A successful ffmpeg command is not evidence that anyone watched the film.

## Optional browser tests

```sh
python scripts/connected_browser_smoke.py --out NEW_TEST_FOLDER
```

The new test runs explicitly in inline-document mode, without a live URL. It
checks UI interactions, responsive layout, two-brand separation and movie-state
checkpoints. Live navigation, origin-backed reload, backend authorization and
model behavior are **not** tested. Use a fresh browser document between fixtures
to avoid JavaScript globals from one fixture leaking into another.

The older `scripts/browser_smoke.py` and `media.py` remain compatibility helpers.
Old diagram-style exports are deprecated, not recommended creative defaults.
For richer formats use an already authorized design/video tool or project; see
[Remotion's official skills](https://www.remotion.dev/docs/ai/skills) and its current
license before adding it. No Remotion, voice API, paid rendering or cloud account
is required by Co-founder.

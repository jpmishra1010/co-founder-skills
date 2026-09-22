# Release validation — Co-founder 1.1.1

The new distribution-only checks are in [DISTRIBUTION_VALIDATION.md](DISTRIBUTION_VALIDATION.md).
The following is retained **1.1.0 historical evidence**, not a claim that browser/media
checks were repeated for this documentation patch. The new unit suite is rerun and
reported separately. All example source/media are compared byte-for-byte to 1.1.0.

## Preserved 1.1.0 validation record

Prepared 2026-09-23. Actual execution timestamps are recorded in UTC in receipts.
These measurements concern the authored package and fictional examples—not a live
customer product. [Machine-readable record](validation.json).

## Executed results

| Area | Result | Exact scope |
|---|---|---|
| Core unit suite | **210 passed; 0 failed** | Installer, runtime, project resolution, asset integrity, stale context, review contracts, media input and public-pack checks. |
| Project upgrade | **11 checks passed** | v1→v1.1 full-mode update, clean lite installation, both host directories, removal, additive init and Git privacy rules in disposable paths. |
| New browser fixture | **42 passed; 0 failed** | Inline UI interactions, 3 viewports, mobile detail/back/focus, 2-brand separation, deliberate overflow detection and 4 movie-state checkpoints. |
| Post | **1080×1350 PNG produced** | Exact selected project assets; marked-bound geometry and JS/network checks. |
| UI captures | **1440, 768 and 390px viewport widths** | Actual desktop/tablet/mobile queue plus mobile detail; captures include full-page height. |
| Silent motion | **24s, 1280×720, 30 fps, 720 frames** | Ten marked safe-bound elements checked over every rendered frame; encoded stream decodes without error. |
| Source validation | **Passed** | Syntax, JSON, metadata, local links, 12 principle/contract routes, private-context allowlist and forbidden font/credential-like file extensions. |

Raw [unit output](evidence/unit-tests.txt), [upgrade checks](upgrade-test.json),
[browser checks](../examples/connected-brand/checks-final/browser-report.json),
[movie render receipt](../examples/connected-brand/previews/motion.render.json), and
[encoded-video integrity](../examples/connected-brand/previews/video-integrity.json).

The pack contains 13 skill entries, 12 workflows, 17 category guides, 53 research
source/access records and 52 manual model-behavior scenarios. The scenarios are
**specifications, not passed model tests**. Lite retains every workflow.

## Visual review is a separate result

Desktop/mobile captures and the post were actually inspected. The mobile detail
problem found during inspection was corrected and retested. Seven encoded movie
styleframes were inspected; state and geometry checks are not full real-time
viewing. The movie is silent. No end-user acceptance or external design-panel
approval is claimed. See the [craft review](../examples/connected-brand/CRAFT_REVIEW.md).

The example review gate returns ready-for-human-review for UI/post and inconclusive
for motion because full playback has not been reviewed. That is an honest status,
not a publication permission. A successful render is not a quality certificate.

## Failures found and corrected

The initial new browser harness reused a page between inline documents. JavaScript
globals survived, causing a real redeclaration/missing-function error. The harness
now creates a fresh page per document. That initial run was not counted as passed.

The mobile detail previously sat below the whole queue; it now becomes a focused
state with a back action and focus restoration. Three additional regression checks
cover this correction. Receipts also distinguish viewport size from full PNG size
and zero safe markers from a real safe-frame check.

## What remains unverified

No authenticated Codex/Claude session, model obedience, real subscription usage,
production bug fix, customer outcome, external account action or security assessment
was tested. The installer integration touches disposable host directories, not a
logged-in account. Follow [ACCEPTANCE.md](ACCEPTANCE.md) in your own host.

Browser testing used inline documents. Live URL navigation, real-origin reload
persistence and backend/tenant controls were not run. Host navigation restrictions
were not bypassed. Windows/macOS and GitHub Actions are configured, not executed
here. Local font fallbacks may change layout; inspect renders on your machine.

Reference research includes some directly inspected images and primary page text,
not fully watched external films or exhaustive category/social-feed audits. No
third-party images, films or fonts are bundled. [Research record](RESEARCH.md).

## Reproduce

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
# Optional, after explicit browser setup:
python scripts/connected_browser_smoke.py --out NEW_TEST_FOLDER
```

See [MEDIA.md](MEDIA.md) for rendering commands and explicit optional dependencies.
Archive integrity/checksum is separate from publisher authentication or security.

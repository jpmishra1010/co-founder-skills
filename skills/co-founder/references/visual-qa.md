# Actual visual and interaction QA

Record page/route, commit, viewport, device scale, theme, locale, data state, and
browser before comparing screenshots. Use synthetic stable content and avoid
screenshots containing customer data. Capture both the relevant viewport and
important lower sections; a hero-only review misses most workflows.

For an existing UI capture before editing, then after. For a new direction compare
to the approved brief. Do not judge screenshot pixel differences as inherently
bad: typography rasterization, content, and intentional changes can differ.

## Required review passes
1. Task: main action is findable, actual behavior works, feedback is truthful.
2. Layout: alignment, gutters, density, line breaks, section rhythm, hierarchy.
3. Components: consistent states, menus/dialogs, clear labels, focus/keyboard.
4. Content: exact logo/text, real proof, long/empty/error/loading data.
5. Responsive: narrow phone, intermediate/tablet, desktop; content-driven breakpoints.
6. Navigation: direct URL, internal navigation, refresh, shared header/footer.
7. Accessibility: contrast, zoom/reflow, focus, names, reduced motion, errors.
8. Performance: required media, shifts, broken assets, console/network failures.

Suggested widths such as 390, 768, and 1440 CSS pixels are starting points, not
proof of every device. Include actual supported devices/browser engines when
risk warrants. A Chromium screenshot is not native iOS or Flutter verification.
Automated checks supplement, not replace, manual accessible interaction testing.

## Review rubric (project heuristic)
Evaluate hierarchy, typography, spacing, brand coherence, content credibility,
interaction, responsive behavior, and accessibility with pass / revise / not-checked.
Record concrete evidence and next change for each revision. Block delivery for
unreadable/clipped primary content, broken actions, incorrect brand/claims, known
critical access failures, or major layout regression. A visual score cannot overrule
a blocking functional issue.

## Static creative
Inspect at export resolution and at the size someone sees in a feed. Check text
bounds, stroke detail, brand safe space, line breaks, contrast, and crop variants.
Exporting one square and auto-cropping it is not a multi-format design review.

## Motion
Inspect first/last frames, transition midpoints, every text hold, source-asset
integrity, audio/caption alignment, safe areas, and playback. Sampled frames alone
cannot establish temporal smoothness or audio quality. Label the actual review
mode. The bundled render helper checks bounds at selected frames; a human still
reviews the complete playback and story before publication.

## Optional executable capture
`python PACK/scripts/ui_audit.py --base http://127.0.0.1:3000 --paths / --out NEW_FOLDER`
captures approved direct-load pages with basic DOM observations. `--html FILE`
is explicitly offline inline rendering; it cannot establish live navigation,
authentication or persistence. Inspect the actual screenshots and report blocked
resources. Neither mode is a complete visual, accessibility or security audit.

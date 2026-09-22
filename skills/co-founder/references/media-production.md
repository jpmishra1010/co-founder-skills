# Choose production for the project—not a universal template

Bind the project and surface first, then apply `craft-gates.md`. Inspect approved
assets and references. Select/create a composition that expresses the actual idea.
An existing project design system, trusted local HTML, an approved scene/video
project or an explicitly authorized design connector may be the appropriate tool.
Do not force every post into headline + boxes or every video into equal slides.

## Optional connected local renderer

`connected_studio.py` can build a trusted project-local HTML composition using its
approved profile/assets. It substitutes a single `__BRAND_JSON__` slot, preserves
approved source artwork bytes, records the binding fingerprint and rejects changed
assets. Selected SVG imports are restricted to static vector elements; no scripts,
external image references or font files. Templates themselves execute JavaScript:
review them and use the host's sandbox. Network blocking is not a full sandbox.

Build/export example (replace placeholders with the actual paths):

```sh
python PACK/scripts/connected_studio.py build --project PROJECT --template campaign/post.html --surface post --out OUTPUT/post.html
python PACK/scripts/connected_studio.py export --project PROJECT --template campaign/post.html --surface post --out OUTPUT/post.png
```

`build` requires only Python. `export` requires explicitly installed Playwright and
Chromium; MP4 also needs FFmpeg. Never install dependencies or invoke a paid service
without permission. Keep output private unless publishing is separately authorized.
Actual exports require actual paths and inspection; an HTML source is not a PNG.

The helper records marked-element geometry, errors and exact source fingerprints.
It cannot grade composition, inspect claims, guarantee accessibility or certify
full playback. Complete the relevant review and retain not-checked statuses.

The v1 `media.py` JSON/diagram renderer is retained for compatibility and smoke tests.
It is not a creative default or quality benchmark. The fictional connected examples
illustrate continuity across media, not the correct look for every project.

For motion, use meaningful object continuity, deliberate holds and genuine visual
storytelling. Show an approved storyboard/style frame before expensive rendering
when the direction is new. Add authorized audio/captions in an appropriate tool;
a silent sample is silent, not sound-designed. Optional richer tools such as
Remotion require current dependency/license review and explicit installation.

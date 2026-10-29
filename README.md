# Bauhausian

**Flat grids. Geometric type. Color with a job.**

A standalone design system for dense tools and inspectable workflows.
White surfaces, orange framing, blue action, hard black rules and square
controls. Maintained by Alex Selig.

## Implemented screens first

**[Browse the Ship a Skill screen references](references/ship-a-skill/README.md)**,
or open [`references/ship-a-skill/index.html`](references/ship-a-skill/index.html)
locally for the visual gallery. These are captures of the deployed application's
public demo, with synthetic records, source revision, viewport, date and hashes.
They are not redesigned or reconstructed screens.

![Actual Ship a Skill dashboard captured from the live public demo](references/ship-a-skill/2026-10-29T18-44-10-888Z-eb9560e/dashboard-1440.png)

The component specimen below is a generic interpretation, **not an extraction
of Ship a Skill**. Use the reference gallery as the visual authority for the
actual shell, stage rail, blue title bands, forms and task layouts.

<details>
<summary>Generic component specimen (not an application screen)</summary>

![Generic Bauhausian component specimen, not a Ship a Skill screen capture](preview.png)

</details>

## Start here

- [`DESIGN.md`](DESIGN.md) - principles, canonical tokens, layout and behavior.
- [`bauhausian-tokens.css`](bauhausian-tokens.css) - generated CSS variables,
  without global resets or network requests.
- [`components.css`](components.css) - small, framework-independent primitives.
- [`index.html`](index.html) - responsive showcase with working search, filter,
  review dialog and an explicit fictional dataset.
- [`fonts.css`](fonts.css) - optional Google Fonts loading, separate from tokens.

Open `index.html` directly, or serve this directory locally:

```bash
python3 -m http.server 8080 --bind 127.0.0.1
```

Then visit `http://127.0.0.1:8080`. No package install or application server is
needed. No fonts are loaded remotely by default. For the intended League
Spartan / Figtree / JetBrains Mono typography, include `fonts.css` before
`components.css`, or provide approved self-hosted faces.

## Use in a project

```html
<link rel="stylesheet" href="bauhausian-tokens.css">
<link rel="stylesheet" href="components.css">
<main class="bh" aria-labelledby="title">
  <h1 id="title" class="bh-title">Review queue</h1>
  <button class="bh-button bh-button--primary">Review item</button>
  <span class="bh-status bh-status--success">Verified</span>
</main>
```

The component rules are scoped to `.bh` or `bh-` classes. The tokens use the
established names in `:root`; do not combine this palette with another system
in the same scope without an explicit boundary.

## Update and validate

Python 3.9+ is sufficient:

```bash
python3 build-tokens.py
python3 build-tokens.py --check
python3 -B -m unittest discover -s tests -v
```

Edit the frontmatter in `DESIGN.md`, then regenerate. Unresolved token references
fail the build. `--check` exits nonzero when committed CSS is stale.

Optional browser checks use an existing Playwright installation with Chromium:
`node tests/browser.cjs`. If it is installed outside this repository, set
`PLAYWRIGHT_MODULE` to that installation's absolute module path. These checks
exercise the offline showcase at five widths, filtering, keyboard focus,
dialogs and reduced motion. Screenshots go to the ignored `test-results/`.
Playwright is test-only; the design package itself has no runtime dependencies.

## Scope

This preserves an existing Bauhausian application design language, not its
application implementation. The specimen examples are original and fictional.
The reference screenshots are from the deployed public demo with its existing
synthetic records and visible branding, not authenticated production sessions.
There are no customer records, credentials, application source files or extracted
application assets.
This repository is a design reference, not a historical Bauhaus reproduction
or a fully accessibility-certified component library.

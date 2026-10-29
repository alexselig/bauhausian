#!/usr/bin/env python3
"""Verify a completed capture and generate a static, offline reference gallery."""

import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "references" / "ship-a-skill"


def validate(snapshot, manifest):
    source = manifest.get("source", {})
    if source.get("mode") != "live-public-demo" or source.get("authenticated") is not False:
        raise ValueError("Only unauthenticated public demo reference captures are allowed.")
    if not re.fullmatch(r"[a-f0-9]{40}", source.get("commitSha", "")):
        raise ValueError("Missing source commit.")
    if not manifest.get("verifiedAt"):
        raise ValueError("Capture is incomplete or live build was not rechecked.")
    viewports = {(item["width"], item["height"]) for item in manifest["viewports"]}
    if not viewports:
        raise ValueError("No viewports recorded.")
    records = manifest.get("screens", [])
    if not records:
        raise ValueError("No screenshots recorded.")
    ids, groups = set(), {}
    for record in records:
        if record["id"] in ids:
            raise ValueError(f"Duplicate screenshot: {record['id']}")
        ids.add(record["id"])
        if not re.fullmatch(r"[a-z0-9-]+\.png", record["file"]):
            raise ValueError("Unsafe screenshot filename.")
        file = snapshot / record["file"]
        if file.is_symlink():
            raise ValueError("Screenshot cannot be a symlink.")
        image = file.read_bytes()
        if image[:8] != b"\x89PNG\r\n\x1a\n" or image[12:16] != b"IHDR":
            raise ValueError(f"Invalid PNG: {record['file']}")
        dimensions = (int.from_bytes(image[16:20], "big"), int.from_bytes(image[20:24], "big"))
        if dimensions != (record["width"], record["height"]):
            raise ValueError(f"Screenshot dimensions differ: {record['file']}")
        if hashlib.sha256(image).hexdigest() != record["sha256"]:
            raise ValueError(f"Screenshot hash differs: {record['file']}")
        if dimensions not in viewports:
            raise ValueError("Unexpected viewport.")
        groups.setdefault(record["screen"], []).append(record)
    for name, group in groups.items():
        if {(item["width"], item["height"]) for item in group} != viewports or len(group) != len(viewports):
            raise ValueError(f"Incomplete viewport coverage for {name}.")
    return groups


def render(snapshot, manifest):
    groups = validate(snapshot, manifest)
    version = snapshot.name
    escape = html.escape
    sha = manifest["source"]["commitSha"]
    date = manifest["capturedAt"][:10]
    widths = [item["width"] for item in manifest["viewports"]]
    options = "".join(f'<option value="{width}">{width}px</option>' for width in widths)
    figures = []
    table = []
    for name, records in groups.items():
        images = []
        links = []
        for record in records:
            href = f'{version}/{record["file"]}'
            hidden = " hidden" if record["width"] != widths[0] else ""
            images.append(
                f'<a class="capture" data-width="{record["width"]}" href="{escape(href)}"{hidden}>'
                f'<img src="{escape(href)}" alt="{escape(record["title"])} at '
                f'{record["width"]} by {record["height"]} pixels" width="{record["width"]}" '
                f'height="{record["height"]}" loading="lazy"></a>')
            links.append(f'[{record["width"]}px]({href})')
        title = records[0]["title"]
        figures.append(
            f'<figure id="{escape(name)}">{"".join(images)}'
            f'<figcaption><h2>{escape(title)}</h2><p>Live public demo · {escape(date)}</p>'
            f'<p class="route">{escape(records[0]["path"])}</p>'
            '<p>Click the image for original-size pixels.</p></figcaption></figure>')
        table.append(f'| {title} | {" · ".join(links)} |')
    overflow = [r["id"] for r in manifest["screens"] if r.get("pageOverflow")]
    overflow_note = (
        "Observed page-level overflow is recorded, not corrected, in: " + ", ".join(overflow)
        if overflow else "No page-level horizontal overflow was observed in the captured states."
    )
    document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="referrer" content="no-referrer"><title>Ship a Skill / Implemented screen references</title>
<link rel="stylesheet" href="../../bauhausian-tokens.css"><link rel="stylesheet" href="reference.css">
</head><body>
<header><a href="../../index.html">Bauhausian library</a><span>Implemented screens / not mockups</span></header>
<main><p class="eyebrow">Ship a Skill · captured {escape(date)}</p><h1>The implemented screens.</h1>
<p>These are direct screenshots of the deployed application's public demo, not reconstructions
from the design tokens. All records are the site's built-in sample data. No authenticated session was used.</p>
<p><strong>{len(groups)} screens · {len(manifest["screens"])} captures</strong> · source revision
<code>{sha}</code>. Demo badges, sandbox footer and existing layout are deliberately retained.</p>
<p>The original component showcase is a generic specimen, not an extracted screen. Use these
references for the actual shell, stage rail, blue title bands, forms and task layouts.</p>
<p><a href="{escape(version)}/manifest.json">Capture manifest and image hashes</a> ·
<a href="README.md">Coverage, differences and reproduction instructions</a></p>
<div class="controls"><label for="viewport">Captured viewport</label><select id="viewport">{options}</select>
<span id="selection" role="status">{widths[0]}px references</span></div>
<div class="gallery">{"".join(figures)}</div>
<aside><h2>Scope and limitations</h2><p>These are viewport captures. The app's inner scrollers
remain intact; below-the-fold content is not expanded into artificial full-page layouts.
External services are simulated by the public demo. This is visual evidence, not integration evidence.</p>
<p>{escape(overflow_note)}</p></aside></main>
<script>
const selector = document.querySelector("#viewport");
selector.addEventListener("change", () => {{
  for (const capture of document.querySelectorAll(".capture")) {{
    capture.hidden = capture.dataset.width !== selector.value;
  }}
  document.querySelector("#selection").textContent = selector.value + "px references";
}});
</script></body></html>
"""
    readme = f"""# Ship a Skill: implemented screen references

**These are actual live-site captures, not recreated designs.**

Captured **{date}** from the deployed application's unauthenticated public demo
at source revision **`{sha}`**. The build identifier was checked before and after
the capture. Only the site's synthetic sample records were loaded.

Open [the visual gallery](index.html) locally to switch between desktop, tablet
and mobile references. On GitHub, use the direct image links below.

## What changed from the initial library

- The original `index.html` and `preview.png` are generic component specimens,
  not extracted application screens. They are now explicitly labeled.
- The implemented application uses **JetBrains Mono**, not the initially
  documented IBM Plex Mono. The library's font token and optional font loader
  now match. Display/body are League Spartan and Figtree.
- Workflow screens use a **blue stage-title band and left stage rail**.
  Orange is the overview/title treatment, not the template for every screen.
- Stage headings are sentence case; dashboard poster type and navigation are
  uppercase. A global uppercase title convention is not an exact reproduction.
- The app has a **viewport-height shell, inner scrolling and persistent footer**.
  The specimen document's natural page scroll is not the application layout.

## Coverage

{len(groups)} states, {len(manifest["screens"])} screenshots, at
{", ".join(f'{v["width"]} × {v["height"]}' for v in manifest["viewports"])}.

| Implemented screen | Original screenshots |
| --- | --- |
{chr(10).join(table)}

## Visual authority and provenance

- [Manifest]({version}/manifest.json): exact source revision, origin, capture
  times, viewport dimensions, SHA-256 per image, routes, loaded font families
  and computed heading styles.
- PNGs are unmodified viewport screenshots. No content replacement, masking,
  CSS rewrite or reconstructed markup was applied.
- The public demo shares the implemented application views but simulates
  external integrations. Its ADMIN/DEMO badges and sandbox footer are retained.
- Sample identities and records belong to the site's public demo; no real
  account cookies or production records were used. These are not signed-in
  production-session captures.
- The set covers the listed states, not every possible empty, error, permission
  or loading state. Fixed-shell captures do not expand content below the fold.
- {overflow_note}
- A future deployment may differ. Never relabel these images as a newer build.
  Capture a new immutable directory and update the gallery.

## Reproduce safely

Use an existing Playwright installation with Chromium. The capture script
requires explicit target origin and exact expected deployed SHA:

```bash
REFERENCE_BASE_URL=https://YOUR_APPROVED_PUBLIC_DEMO_HOST \\
REFERENCE_EXPECTED_SHA=EXPECTED_40_CHARACTER_DEPLOYED_SHA \\
node scripts/capture-reference.cjs
```

Set `PLAYWRIGHT_MODULE` to an existing absolute Playwright module path if it is
not available in this repository. Do not copy tokens or browser cookies.
The source must expose this demo's known routes; this is not a generic crawler.
The script uses a new unauthenticated context, permits only public-page/static
GET requests, blocks authenticated/API/mutating requests, and makes no saves.
The selectors describe this deployed revision; if a new revision changes them,
review and update the capture expectations rather than suppressing failures.

From the repository root, validate the resulting completed snapshot and build
the static gallery:

```bash
python3 scripts/build-references.py references/ship-a-skill/{version}
python3 -B -m unittest discover -s tests -v
```

Use `--check` with the builder to verify generated gallery files are current.
The generator rejects incomplete captures, unsafe filenames, wrong image
dimensions, changed hashes and missing viewport variants. Inspect the screenshots
for unintended data before publication. Incomplete runs are not reference sets.
"""
    return document, readme


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        snapshot = args.snapshot.resolve()
        if snapshot.parent != LIBRARY.resolve():
            raise ValueError("Snapshot must be a direct child of references/ship-a-skill.")
        manifest = json.loads((snapshot / "manifest.json").read_text())
        document, readme = render(snapshot, manifest)
        for file, text in [(LIBRARY / "index.html", document), (LIBRARY / "README.md", readme)]:
            if args.check:
                if not file.exists() or file.read_text() != text:
                    raise ValueError(f"Generated reference file is stale: {file.name}")
            else:
                file.write_text(text, encoding="utf-8")
        print(f"Verified {len(manifest['screens'])} references; gallery {'matches' if args.check else 'generated'}.")
    except (OSError, ValueError, KeyError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

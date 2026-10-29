---
{
  "name": "Bauhausian",
  "version": "1.0.0",
  "tokens": {
    "surface": "#ffffff",
    "surface-alt": "#f5f3ee",
    "surface-hover": "#fbfaf7",
    "line": "#e3e5e9",
    "line-strong": "#7d828b",
    "ink": "#141414",
    "ink-muted": "#5b5f66",
    "bauhaus-orange": "#ed6c47",
    "on-orange": "#141414",
    "orange-soft": "#fff3ed",
    "orange-text": "#b4410b",
    "orange-line": "#f7c6ad",
    "bauhaus-blue": "#1b6fa8",
    "on-blue": "#ffffff",
    "blue-soft": "#e8f2f9",
    "blue-line": "#c4dcee",
    "blue-rule": "#4a8cbd",
    "bauhaus-yellow": "#f2b33d",
    "on-yellow": "#141414",
    "success": "#17634d",
    "success-soft": "#eaf5f0",
    "success-line": "#bfe0d2",
    "warning": "#9a4b18",
    "warning-soft": "#fff0e5",
    "destructive": "#b42318",
    "destructive-soft": "#fff0ee",
    "destructive-line": "#f3c2bd",
    "draft-line": "#d9d6cf",
    "rule-frame": "2px solid var(--ink)",
    "rule-region": "1px solid var(--ink)",
    "rule-row": "1px solid var(--line)",
    "radius-none": "0",
    "radius-pill": "999px",
    "radius-circle": "50%",
    "space-1": "4px",
    "space-2": "8px",
    "space-3": "16px",
    "space-4": "24px",
    "space-5": "32px",
    "space-6": "48px",
    "space-7": "96px",
    "space-8": "144px",
    "shadow-none": "none",
    "shadow-active-inset": "inset 0 -4px var(--bauhaus-blue)",
    "shadow-illustrative-offset": "7px 7px 0 var(--ink)",
    "fast": "160ms",
    "standard": "320ms",
    "size-sheet": "1680px",
    "size-touch": "44px",
    "size-evidence-sheet": "540px",
    "size-header": "64px",
    "size-footer": "36px",
    "size-title-cell": "400px",
    "size-stage-rail": "260px",
    "size-control": "48px",
    "size-control-inline": "36px",
    "font-display": "\"League Spartan\", Futura, \"Avenir Next\", system-ui, sans-serif",
    "font-sans": "Figtree, \"Avenir Next\", system-ui, sans-serif",
    "font-mono": "\"JetBrains Mono\", \"SFMono-Regular\", Consolas, monospace",
    "type-poster": "800 84px/0.85 var(--font-display)",
    "type-stage-title": "800 64px/0.9 var(--font-display)",
    "type-title": "700 32px/1.1 var(--font-display)",
    "type-heading": "700 20px/1.2 var(--font-display)",
    "type-body": "400 15px/1.5 var(--font-sans)",
    "type-small": "400 13px/1.45 var(--font-sans)",
    "type-eyebrow": "700 11px/1 var(--font-display)",
    "type-pill": "700 11px/1 var(--font-display)",
    "type-mono": "400 12px/1.4 var(--font-mono)"
  }
}
---

# Bauhausian

A functional design language for dense, inspectable tools. White work surfaces,
geometric headings, an orange title field, blue action, black structural rules.
The interface is a workbench, not a collection of floating cards.

## Authority and provenance

This is a standalone expression of Alex's existing Bauhausian design language.
The palette and component proportions follow the application-style workbench,
not the editorial security guide. [Implemented screen references](references/ship-a-skill/README.md)
are the visual authority for reproducing the application. The generic component
showcase is an interpretation, not a screen extraction. The established Bauhausian specification
provides the principles; the workbench refines blue tints, frame weights,
typographic scale and shell dimensions. This is not a new theme or a historical
reconstruction of the Bauhaus school.

It is a sibling of other design systems, not a variant. Do not mix in their
colors, typography or component conventions. Only design primitives and
original, fictional examples belong here, together with the explicitly requested
live public-demo screenshots. Those screenshots retain the application's visible
branding and synthetic records; they do not redistribute its source or assets.
Do not add application logic, customer data, authenticated screens, credentials
or operational documentation.

The frontmatter is the token source of truth. It is JSON, a valid YAML 1.2
subset, so the generator uses only Python's standard library. Edit this file
and run `python3 build-tokens.py`; never hand-edit `bauhausian-tokens.css`.

## The visual signature

The overview uses an orange title cell beside white lifecycle counters.
Workflow screens instead use a large blue stage-title band beside a persistent
stage rail, with white task sections below. Blue also marks active navigation.
Do not turn every page into an orange poster: the dominant field depends on the
screen's job. The signature comes from proportion and type, not decoration.

```text
+-------------------+----------------------+--------------------+
| wordmark          | active navigation    | utility            |
+-------------------+----------------------+--------------------+
| ORANGE TITLE      | measure              | measure            |
| large, condensed  | tabular value        | tabular value      |
+-------------------+----------------------+--------------------+
| task heading / search / primary action                       |
+--------------------------------------------------------------+
| evidence or records                    | optional review rail |
+--------------------------------------------------------------+
| explicit state / status                                       |
+--------------------------------------------------------------+
```

Use the full workbench when there is genuine information to organize. A short
form can be a single column; do not manufacture metrics to fill a grid.

```text
+-------------------+----------------------+--------------------+
| product           | navigation           | identity           |
+-------------------+-------------------------------------------+
| skill identity    | BLUE STAGE TITLE             progress      |
| stage rail        +-------------------------------------------+
| current step      | task sections / evidence                   |
| next steps        | independent inner scrolling                |
+-------------------+-------------------------------------------+
| persistent capability and utility footer                      |
+--------------------------------------------------------------+
```

The implemented application uses a viewport-height shell with an inner scroller,
a 260px desktop stage rail and a persistent footer. The standalone showcase is
a scrolling specimen document; its page geometry is not the application shell.

## Color has a job

| Role | Token | Use |
| --- | --- | --- |
| Work surface | `--surface` | Primary white cells |
| Secondary surface | `--surface-alt` | Quiet support regions |
| Main text | `--ink` | Content, headings and frame rules |
| Secondary text | `--ink-muted` | Supporting copy, never disabled-looking instructions |
| Action | `--bauhaus-blue` | Primary action, active navigation, focus |
| Frame | `--bauhaus-orange` | Overview title/framing region, not every stage |
| Accent | `--bauhaus-yellow` | Small, tertiary emphasis |
| Verified | `--success` | Confirmed successful state with a text label |
| Warning | `--warning` | A condition that needs attention |
| Destructive | `--destructive` | Irreversible action or failure |

Use `--on-blue` on blue and dark `--on-orange` on orange. Do not put small white
text on orange or yellow. Pale state surfaces need dark state text; color is
never the only signal. Orange framing is not automatically an error.
`--line` is a decorative separator, not a sufficient input boundary. Inputs use
`--line-strong` or ink. No gradients, glass, soft shadows or arbitrary accent
colors. Do not introduce the optional bright approval-green as body text.

## Typography

| Role | Family | Treatment |
| --- | --- | --- |
| Display and chrome | League Spartan | Bold and compact; case follows the role |
| Content and forms | Figtree | Sentence case, 15px/1.5 baseline |
| Counts and technical data | JetBrains Mono | Tabular numbers, restrained use |

This corrects the initial library's IBM Plex Mono substitution. The deployed
application loads League Spartan, Figtree and JetBrains Mono; actual loaded
families and computed heading styles are recorded with each reference capture.
Dashboard poster labels and navigation are uppercase. Stage headings such as
"Create" and "Provide evals" are sentence case; do not uppercase them globally.

The stacks contain local fallbacks. Fonts are not bundled. The optional
`fonts.css` loads those families from Google Fonts; omit it in offline/private
deployments, or supply licensed self-hosted faces through your approved pipeline.
Do not silently enable external font requests in an application.

Poster headings use `--type-poster` at wide widths and a fluid 48-84px scale
on small screens. Stage titles use 64px; ordinary titles use 32px; section
headings use 20px. Small supporting copy is 13px. Eleven-pixel uppercase
eyebrows are for short secondary labels, never instructions or long prose.
Keep reading lines within 68ch. Use sentence case for actions and content.

## Grid, rules and spacing

- Frame: 2px ink; regional division: 1px ink; row separator: 1px pale line.
- Sheet cap: 1680px. Beyond it, a neutral drafting-board backdrop is visible.
- Header: 64px. Controls: 48px; inline controls: 36px on desktop only.
- Spacing scale: 4, 8, 16, 24, 32, 48, 96, 144px. Small optical offsets are
  allowed where type meets a rule, not as a second spacing system.
- All controls, dialogs and panels have square corners. Rounded shapes are
  reserved for status pills and genuinely circular semantic objects.
- No elevation by default. An inset active rule is an indicator, not a shadow.
  The offset shadow token is reserved for one illustration-like CTA in an
  otherwise empty view; do not use it for cards or normal controls.

## Component contracts

**Shell and navigation.** Name the product, expose the current section and
separate utilities. Active navigation is blue with white text and
`aria-current`. Use links for destinations, not fake tabs.

**Buttons.** One primary action per task region. Secondary actions are white
with an ink border. Text explains the outcome: "Review item", not "Submit".
Disabled controls expose a reason nearby. Hover is supplemental; keyboard
focus must be visible against every surrounding color.

**Forms.** Persistent labels above square inputs. Provide hints before errors
are possible. Put validation next to the relevant field and connect it with
`aria-describedby`; preserve entered values after a failure.

**Tables and lists.** Headers are compact uppercase; content is sentence case.
Use real table semantics for tabular data. On narrow screens retain important
columns or use explicit labeled rows; do not hide the primary task. If a truly
wide table needs scrolling, constrain it to a named focusable region rather
than overflowing the page.

**Status.** Pair text with a dot or symbol. State is not conveyed by hue alone.
Unknown, pending and stale are not success. Empty and no-results states are
different: the latter offers a way to clear the filter.

**Dialogs and review sheets.** Use native modal behavior for short
confirmations; long evidence review may use an edge-attached sheet capped at
540px. Provide a visible close control, Escape support and focus restoration.
Do not implement overlays using a decorative div without focus management.

**Trust and recovery.** Separate suggested from confirmed results. Automation
must remain inspectable and editable; unavailable optional automation must not
disable the manual task. Recovery preserves completed work.

## Responsive behavior

Validate at 390, 768, 1024, 1440 and 1920px. Below 720px, stack the title and
content, wrap utilities and give visible actions at least 44px in height.
At 720-819px use one or two legible columns; at 820-1199px retain the board
structure without cramming navigation. At 1200px and above use the full
workbench. The sheet stops growing at 1680px.

No page-level horizontal scrolling. Do not hide overflow to conceal a broken
layout. Use dynamic viewport units for full-height workbenches and sheets;
the showcase itself is a naturally scrolling document.

## Motion, accessibility and finishing

Local feedback may use 160ms; structural transitions may use 320ms. Respect
`prefers-reduced-motion`. Focus is a 2px blue outline with 2px offset on light
surfaces; invert it where necessary on colored regions.

Check text contrast, 200% zoom, keyboard order, clear names, touch targets,
short-height dialogs, error states, no-results states and reduced motion.
Avoid animations that move work while somebody is reading it.

## What this system is not

Not a rainbow of primary colors, not decorative circles and triangles, not a
marketing landing-page template, and not a rounded-card dashboard with a new
font. A correct implementation feels ordered, direct and useful.

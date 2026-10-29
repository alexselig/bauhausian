# Working on Bauhausian

- Read DESIGN.md first. Preserve the existing visual language; do not invent
  another theme or mix in a sibling system's tokens.
- For application fidelity, use references/ship-a-skill/README.md and the
  completed screenshot manifests. The root showcase is a generic specimen,
  not an extracted application screen.
- Edit tokens only in DESIGN.md frontmatter, then run `python3 build-tokens.py`.
- Run `python3 build-tokens.py --check` and
  `python3 -B -m unittest discover -s tests -v`.
- Check the showcase at 390, 768, 1024, 1440 and 1920px, including keyboard
  navigation, filtering, empty results and dialog open/close.
- Keep examples fictional. Do not add internal product code, credentials,
  operational identifiers or real customer content.
- Reference captures must use the unauthenticated public demo with synthetic
  records, retain provenance and hashes, and preserve the rendered layout.
  Never replace screenshot content or relabel an old capture as a newer build.
- No mandatory remote assets, runtime dependencies or build framework.
- Fonts are optional; do not bundle font files without their license.

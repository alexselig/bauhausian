#!/usr/bin/env python3
"""Generate CSS variables from DESIGN.md's JSON-compatible YAML frontmatter."""

import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parent
REFERENCE = re.compile(r"var\(--([a-z0-9-]+)\)")


def read_tokens(source):
    match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", source, re.DOTALL)
    if not match:
        raise ValueError("DESIGN.md must start with JSON-compatible YAML frontmatter.")
    document = json.loads(match.group(1))
    tokens = document.get("tokens") if isinstance(document, dict) else None
    if not isinstance(tokens, dict) or not tokens:
        raise ValueError("Frontmatter must contain a nonempty tokens object.")
    for name, value in tokens.items():
        if not re.fullmatch(r"[a-z][a-z0-9-]*", name):
            raise ValueError(f"Invalid CSS token name: {name}")
        if not isinstance(value, str) or not value.strip() or re.search(r"[;{}\r\n]", value):
            raise ValueError(f"Invalid CSS token value: {name}")
    dependencies = {name: set(REFERENCE.findall(value)) for name, value in tokens.items()}
    for name, refs in dependencies.items():
        if refs - tokens.keys():
            raise ValueError(f"{name} references unknown tokens: {sorted(refs - tokens.keys())}")
    complete = set()

    def visit(name, active):
        if name in active:
            raise ValueError(f"Cyclic token reference: {name}")
        if name in complete:
            return
        for dependency in dependencies[name]:
            visit(dependency, active | {name})
        complete.add(name)

    for name in tokens:
        visit(name, set())
    return tokens


def render(source):
    tokens = read_tokens(source)
    properties = "\n".join(f"  --{name}: {value};" for name, value in tokens.items())
    return f"/* Generated from DESIGN.md. Run python3 build-tokens.py; do not edit. */\n:root {{\n{properties}\n}}\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Fail if committed CSS differs.")
    args = parser.parse_args()
    target = ROOT / "bauhausian-tokens.css"
    try:
        css = render((ROOT / "DESIGN.md").read_text(encoding="utf-8"))
        if args.check:
            if not target.exists() or target.read_text(encoding="utf-8") != css:
                raise ValueError("Token CSS is stale. Run python3 build-tokens.py.")
            print("Token CSS matches DESIGN.md.")
        else:
            target.write_text(css, encoding="utf-8")
            print(f"Generated {target.name}.")
    except (OSError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

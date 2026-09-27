#!/usr/bin/env python3
"""Keep the code in the skill references identical to the verified recipe sources in tests/web.

Part of the Apple Design Language package — Created by Edison Augustin X.

A reference marks a code block as coming from a tested file with an HTML comment on the line before it:

    <!-- source: tests/web/react/src/Button.tsx -->
    ```tsx
    …replaced with the file's contents…
    ```

Usage:
    python3 tests/web/sync_docs.py          # rewrite the marked blocks from the source files
    python3 tests/web/sync_docs.py --check  # exit 2 if any block differs from its source (CI)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "skills" / "apple-design-language" / "references"
MARKER = re.compile(r"^<!-- source: (?P<path>tests/web/\S+) -->\n```(?P<lang>[\w-]*)\n.*?^```$", re.M | re.S)
LANG = {".tsx": "tsx", ".ts": "ts", ".vue": "vue", ".svelte": "svelte", ".css": "css", ".html": "html"}


def render(text: str, errors: list[str], doc: Path) -> str:
    def replace(m: re.Match) -> str:
        source = ROOT / m.group("path")
        if not source.is_file():
            errors.append(f"{doc.relative_to(ROOT)}: missing source {m.group('path')}")
            return m.group(0)
        lang = LANG.get(source.suffix, m.group("lang"))
        return f"<!-- source: {m.group('path')} -->\n```{lang}\n{source.read_text(encoding='utf-8').rstrip()}\n```"

    return MARKER.sub(replace, text)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="fail if a marked block differs from its source")
    args = ap.parse_args()

    errors: list[str] = []
    stale: list[str] = []
    blocks = 0
    for doc in sorted(REFERENCES.glob("*.md")):
        text = doc.read_text(encoding="utf-8")
        blocks += len(MARKER.findall(text))
        new = render(text, errors, doc)
        if new != text:
            stale.append(str(doc.relative_to(ROOT)))
            if not args.check:
                doc.write_text(new, encoding="utf-8")
    if errors:
        print("✗ " + "\n✗ ".join(errors), file=sys.stderr)
        return 1
    if args.check and stale:
        print(f"✗ out of sync with tests/web: {', '.join(stale)} — run python3 tests/web/sync_docs.py", file=sys.stderr)
        return 2
    verb = "up to date" if args.check or not stale else f"updated {', '.join(stale)}"
    print(f"✓ {blocks} recipe blocks match tests/web ({verb})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

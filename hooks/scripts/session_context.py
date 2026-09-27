#!/usr/bin/env python3
"""SessionStart hook — give Claude a compact Apple design brief in Apple/web UI projects.

Part of the Apple Design Language package — Created by Edison Augustin X.

Claude Code adds a SessionStart hook's plain-text stdout to Claude's context. To avoid
duplicating instructions, this hook prints nothing when:
  - the project's CLAUDE.md / AGENTS.md already load the Apple Design Language instructions, or
  - the project doesn't look like an Apple-platform or web UI project, or
  - HIG_LINT=off.
Always exits 0.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
MARKER = "Apple Design Language"
INSTRUCTION_FILES = ["CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md", "AGENTS.md", ".claude/AGENTS.md"]
PROJECT_SIGNALS = ("Package.swift", "package.json", "Podfile", "project.yml", "app.json")
PROJECT_SUFFIXES = (".xcodeproj", ".xcworkspace", ".swift", ".html", ".css", ".tsx", ".jsx", ".vue", ".svelte")


def already_instructed(project: Path) -> bool:
    for name in INSTRUCTION_FILES:
        f = project / name
        try:
            if f.is_file() and MARKER in f.read_text(encoding="utf-8", errors="ignore"):
                return True
        except OSError:
            continue
    return False


def looks_like_ui_project(project: Path, max_entries: int = 400) -> bool:
    seen = 0
    for dirpath, dirnames, filenames in os.walk(project):
        depth = Path(dirpath).relative_to(project).parts
        dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in {"node_modules", "build", "DerivedData", "Pods"}]
        if len(depth) >= 2:
            dirnames[:] = []
        for name in dirnames + filenames:
            seen += 1
            if name in PROJECT_SIGNALS or name.endswith(PROJECT_SUFFIXES):
                return True
            if seen > max_entries:
                return False
    return False


def brief() -> str:
    skill = PACKAGE_ROOT / "skills" / "apple-design-language" / "SKILL.md"
    rules = PACKAGE_ROOT / "rules" / "README.md"
    lint = PACKAGE_ROOT / "hooks" / "scripts" / "hig_lint.py"
    return "\n".join([
        f"{MARKER} (Created by Edison Augustin X.) is available for this project.",
        f"- For Apple-platform UI work in any stack (SwiftUI, React, Next.js, HTML/CSS, Tailwind, Vue, Svelte, React Native), use the apple-design-language skill: {skill}",
        f"- Rules with IDs (MUST = error, SHOULD = warning): {rules}",
        "- Non-negotiables: layout from size classes, never device checks (LAY-01); glass only on controls/navigation (GLS-01);"
        " system colors via APIs (COL-01) and follow the system appearance (COL-07); text styles with Dynamic Type (TYP-01),"
        " never below 11 pt on iOS (TYP-02); ≥44 pt targets (A11Y-01); label icon-only controls (A11Y-03); honor Reduce Motion (MOT-02).",
        "- Web and React Native: same rules on every stack (STK-01); native elements, not clickable divs (STK-03); no SF Symbols on the web (STK-02).",
        f"- After editing UI files a checker reports rule violations; run it manually with: python3 {lint} <files>",
        "- Design for Apple platforms; never clone Apple devices, apps, logos, or system UI (BRD-01 – BRD-04).",
    ])


def main() -> int:
    try:
        if os.environ.get("HIG_LINT", "").lower() in {"off", "0", "false", "no"}:
            return 0
        try:
            payload = json.load(sys.stdin)
        except ValueError:
            payload = {}
        project = Path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())
        if already_instructed(project) or not looks_like_ui_project(project):
            return 0
        print(brief())
    except Exception as exc:
        print(f"apple-design-language session hook error: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""UserPromptSubmit hook — route Apple-platform UI requests to the right skill references.

Part of the Apple Design Language package — Created by Edison Augustin X.

When a prompt is clearly about Apple-platform (or Apple-device web) interface work, print a
short plain-text note that Claude Code adds to Claude's context: use the apple-design-language
skill and read these specific references. Prints nothing for unrelated prompts. Never blocks
a prompt. Always exits 0.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
REFS = PACKAGE_ROOT / "skills" / "apple-design-language" / "references"

# A prompt must mention an Apple platform/technology before any routing happens
# (plain "apple" is excluded on purpose — it's also a fruit and a company name in unrelated contexts).
APPLE_CONTEXT = re.compile(
    r"\b(swiftui|uikit|appkit|xcode|ios|ipados|macos|watchos|tvos|visionos|iphone|ipad|mac\s?app|apple\s+watch|apple\s+tv|"
    r"vision\s+pro|iphone\s+duo|human\s+interface\s+guidelines|hig|liquid\s+glass|sf\s+symbols?|dynamic\s+type|"
    r"apple\s+(?:platforms?|devices?|ecosystem|design|style)|app\s+store)\b",
    re.I,
)

TOPICS = [
    ("platforms", r"\b(ipad|mac|macos|watch|watchos|tvos|apple\s+tv|visionos|vision\s+pro|iphone\s+duo|multi-?platform|cross-?platform|every\s+(?:apple\s+)?device|all\s+(?:apple\s+)?devices)\b",
     "platforms.md", "container per platform and what stays identical (SYNC-01 – SYNC-07)"),
    ("navigation", r"\b(tab\s?bar|tabview|sidebar|split\s?view|navigation(?:\s?bar|stack|splitview)?|toolbar|search(?:\s?(?:bar|field|tab))?)\b",
     "navigation.md", "NAV-01 tabs never act · NAV-11 one prominent trailing action"),
    ("glass", r"\b(liquid\s+glass|glass(?:\s?effect)?|material|translucen\w*|blur)\b",
     "liquid-glass.md", "GLS-01 no glass in content · GLS-08 GlassEffectContainer"),
    ("components", r"\b(button|alert|sheet|popover|menu|context\s?menu|list|table|form|picker|toggle|switch|slider|segmented|progress|empty\s+state|onboarding|settings)\b",
     "components.md", "CMP-07 one modal at a time · CMP-12/13 alert titles and buttons"),
    ("tokens", r"\b(colou?rs?|palette|dark\s+mode|contrast|accent|font|typography|text\s+size|dynamic\s+type|spacing|sizes?|tokens?|app\s+icon)\b",
     "design-tokens.md", "COL-01 system colors via API · TYP-01/02 text styles and minimum sizes"),
    ("accessibility", r"\b(accessib\w*|a11y|voiceover|reduce\s+motion|screen\s+reader|contrast|larger\s+text)\b",
     "accessibility.md", "A11Y-01 ≥44 pt targets · A11Y-03 labels · MOT-02 Reduce Motion"),
    ("writing", r"\b(copy|wording|microcopy|label\s+text|error\s+messages?|alert\s+text|button\s+(?:text|labels?)|purpose\s+string|localiz\w*|rtl|right-to-left)\b",
     "writing.md", "WRT-01 verb labels · WRT-07 helpful errors"),
    ("swiftui", r"\b(swiftui|swift\s?ui)\b",
     "swiftui-recipes.md", "anti-pattern → fix table"),
    ("web", r"\b(css|html|react|next\.?js|vue|svelte|web\s?app|website|web\s+page|safari|pwa|tailwind)\b",
     "web-adaptation.md", "TYP-04 never bundle SF fonts · A11Y-05 keep zoom"),
    ("review", r"\b(review|audit|critique|check\s+(?:my|this|the)|feedback\s+on)\b",
     "review-checklist.md", "report template; errors first"),
]


def route(prompt: str) -> str:
    if not APPLE_CONTEXT.search(prompt):
        return ""
    picks = []
    for name, pattern, ref, hint in TOPICS:
        if re.search(pattern, prompt, re.I):
            picks.append((name, ref, hint))
    if not picks:
        picks.append(("platforms", "platforms.md", "start with the platform playbook"))
    lines = ["Apple Design Language: this request involves Apple-platform UI. Use the apple-design-language skill "
             f"({PACKAGE_ROOT / 'skills' / 'apple-design-language' / 'SKILL.md'}) and read only these references:"]
    for _, ref, hint in picks[:5]:
        lines.append(f"- {REFS / ref} — {hint}")
    lines.append("Cite rule IDs for non-obvious decisions; research Apple’s docs before asserting anything not in the package.")
    return "\n".join(lines)


def main() -> int:
    try:
        if os.environ.get("HIG_LINT", "").lower() in {"off", "0", "false", "no"}:
            return 0
        payload = json.load(sys.stdin)
        note = route(str(payload.get("prompt", "")))
        if note:
            print(note)
    except Exception as exc:
        print(f"apple-design-language prompt hook error: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

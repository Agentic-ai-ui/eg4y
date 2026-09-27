#!/usr/bin/env python3
"""hig_lint — check UI source files against the Apple Design Language rules marked `Check: hook`.

Covers Swift; CSS/SCSS; HTML; JavaScript/TypeScript and JSX/TSX (React, Next.js, React Native);
Vue, Svelte, and Astro components; Tailwind classes; plists, .strings, and font files.

Part of the Apple Design Language package — Created by Edison Augustin X.

Rule metadata (title, level, severity) comes from rules/rules.json, so this script and the
rules can never drift apart: every `hook` rule needs a detector here, and the test suite
enforces it.

CLI:
    python3 hooks/scripts/hig_lint.py [--format text|json] [--min-severity info|warning|error] PATH...
        PATH may be a file or a directory (scanned recursively). Exit 1 if any error is found.
    python3 hooks/scripts/hig_lint.py --list-rules

Claude Code hook (PostToolUse on Write|Edit|MultiEdit):
    python3 hooks/scripts/hig_lint.py --hook
        Reads the hook JSON from stdin and lints tool_input.file_path. Errors are returned as
        {"decision": "block", "reason": ...} so Claude sees them next to the tool result;
        warnings are returned as additionalContext. Always exits 0.

Environment:
    HIG_LINT=off                  disable the hook
    HIG_LINT_MIN_SEVERITY=...     lowest severity reported in hook mode (default: warning)

Suppress a deliberate exception on the same line or the line above — a reason is required:
    .preferredColorScheme(.dark) // hig-ignore: COL-07 — immersive video player stays dark
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable

PACKAGE_ROOT = Path(__file__).resolve().parents[2]
RULES_JSON = PACKAGE_ROOT / "rules" / "rules.json"
TOKENS_JSON = PACKAGE_ROOT / "skills" / "apple-design-language" / "assets" / "tokens.json"

SEVERITY_ORDER = {"info": 0, "warning": 1, "error": 2}
HOOK_OUTPUT_LIMIT = 9500  # Claude Code caps hook context strings at 10,000 characters

SWIFT_EXT = {".swift"}
STYLE_EXT = {".css", ".scss", ".sass", ".less"}
MARKUP_EXT = {".html", ".htm", ".vue", ".svelte", ".astro"}
COMPONENT_EXT = {".vue", ".svelte", ".astro"}
SCRIPT_EXT = {".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs"}
PLIST_EXT = {".plist"}
STRINGS_EXT = {".strings", ".xcstrings"}
FONT_EXT = {".otf", ".ttf", ".woff", ".woff2"}
SUPPORTED_EXT = SWIFT_EXT | STYLE_EXT | MARKUP_EXT | SCRIPT_EXT | PLIST_EXT | STRINGS_EXT | FONT_EXT
SKIP_DIRS = {".git", "node_modules", ".build", "build", "DerivedData", "Pods", "dist", ".next", "__pycache__", "vendor"}

APPLE_FONT_NAME = r"(?:SF[\s_-]?Pro(?:[\s_-]?(?:Text|Display|Rounded))?|SF[\s_-]?Compact(?:[\s_-]?(?:Text|Display|Rounded))?|SF[\s_-]?Mono|San[\s_-]?Francisco|New[\s_-]?York(?:[\s_-]?(?:Small|Medium|Large|ExtraLarge))?)"
APPLE_FONT_FILE = re.compile(r"^(?:SF-?Pro|SFPro|SF-?Compact|SFCompact|SF-?Mono|SFMono|SF-?NS|SFNS|NewYork)[\w-]*\.(?:otf|ttf|woff2?)$", re.I)
SUPPRESS_RE = re.compile(r"hig-ignore:\s*(?P<ids>[A-Z0-9-]+(?:\s*,\s*[A-Z0-9-]+)*)\s*(?:—|–|-{1,2}|:)\s*(?P<reason>\S.*)")


# ---------------------------------------------------------------------------- model

@dataclass
class Finding:
    rule: str
    path: str
    line: int
    message: str
    fix: str
    severity: str = ""
    level: str = ""
    title: str = ""
    link: str = ""


def github_slug(heading: str) -> str:
    out = []
    for ch in heading.strip().lower():
        if ch == " ":
            out.append("-")
        elif ch in "-_" or ch.isalnum() or unicodedata.category(ch).startswith(("L", "N")):
            out.append(ch)
    return "".join(out)


def load_rules() -> dict[str, dict]:
    data = json.loads(RULES_JSON.read_text(encoding="utf-8"))
    return {r["id"]: r for r in data["rules"]}


def load_system_hex() -> dict[str, str]:
    """Map uppercase hex → token name for every documented system color value."""
    try:
        tokens = json.loads(TOKENS_JSON.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}
    out: dict[str, str] = {}
    for group in ("system", "gray"):
        for key, c in tokens.get("color", {}).get(group, {}).items():
            for variant in ("light", "dark", "lightIncreasedContrast", "darkIncreasedContrast"):
                out.setdefault(c[variant].upper(), key)
    return out


# ---------------------------------------------------------------------------- helpers

class Source:
    """A file's text with helpers for line lookups and comment-insensitive scanning."""

    def __init__(self, path: Path, text: str):
        self.path = path
        self.text = text
        self.lines = text.splitlines()
        self._line_starts = [0]
        for m in re.finditer(r"\n", text):
            self._line_starts.append(m.end())

    def line_of(self, offset: int) -> int:
        lo, hi = 0, len(self._line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if self._line_starts[mid] <= offset:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    def window(self, line: int, before: int, after: int) -> str:
        start = max(0, line - 1 - before)
        return "\n".join(self.lines[start: line + after])


def strip_swift_comments(text: str) -> str:
    """Blank out // and /* */ comments while preserving offsets (strings kept)."""
    out = list(text)
    i, n = 0, len(text)
    in_str = False
    while i < n:
        c = text[i]
        if in_str:
            if c == "\\":
                i += 2
                continue
            if c == '"' or c == "\n":
                in_str = False
            i += 1
            continue
        if c == '"':
            in_str = True
            i += 1
        elif text.startswith("//", i):
            j = text.find("\n", i)
            j = n if j == -1 else j
            for k in range(i, j):
                out[k] = " "
            i = j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            j = n if j == -1 else j + 2
            for k in range(i, j):
                if out[k] != "\n":
                    out[k] = " "
            i = j
        else:
            i += 1
    return "".join(out)


def strip_css_comments(text: str) -> str:
    return re.sub(r"/\*.*?\*/", lambda m: re.sub(r"[^\n]", " ", m.group(0)), text, flags=re.S)


def num(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None


def imports_appkit_only(code: str) -> bool:
    return bool(re.search(r"^\s*import\s+AppKit\b", code, re.M)) and not re.search(r"^\s*import\s+(UIKit|SwiftUI)\b", code, re.M)


# ---------------------------------------------------------------------------- Swift detectors

def swift_detectors(src: Source) -> Iterable[Finding]:
    code = strip_swift_comments(src.text)
    p = str(src.path)
    appkit_only = imports_appkit_only(code)
    min_text = 10 if appkit_only else 11
    platform = "macOS" if appkit_only else "iOS/iPadOS"

    def at(m: re.Match) -> int:
        return src.line_of(m.start())

    # LAY-01 — device/orientation-driven layout
    for m in re.finditer(r"UIDevice\.current\.userInterfaceIdiom|UIScreen\.main\.(?:bounds|nativeBounds)|UIDevice\.current\.orientation|UIApplication\.shared\.statusBarOrientation", code):
        yield Finding("LAY-01", p, at(m), f"`{m.group(0)}` ties layout to a device, screen, or orientation.",
                      "Decide layout from @Environment(\\.horizontalSizeClass) / trait collections, available space (GeometryReader, ViewThatFits), or containerRelativeFrame.")

    # GLS-02 / GLS-08 — custom glass volume and grouping
    glass = list(re.finditer(r"\.glassEffect\s*\(", code))
    if len(glass) > 3:
        yield Finding("GLS-02", p, at(glass[3]), f"{len(glass)} custom Liquid Glass effects in one file.",
                      "Prefer standard components and `.buttonStyle(.glass)`; keep custom glass to the few most important functional elements.")
    if len(glass) >= 2 and "GlassEffectContainer" not in code:
        yield Finding("GLS-08", p, at(glass[1]), "Multiple `.glassEffect` views without a `GlassEffectContainer`.",
                      "Wrap related glass views in `GlassEffectContainer(spacing:)` for performance and morphing.")

    # GLS-04 — custom bar / sheet / popover backgrounds
    for m in re.finditer(r"\.toolbarBackground\s*\(\s*(?!\.(?:hidden|visible|automatic)\b)([^,)]+)", code):
        yield Finding("GLS-04", p, at(m), f"Custom toolbar background `{m.group(1).strip()}`.",
                      "Remove it and let Liquid Glass and the scroll edge effect render the bar; express brand color in the content layer.")
    for m in re.finditer(r"\.presentationBackground\s*\(", code):
        yield Finding("GLS-04", p, at(m), "Custom sheet/popover background.",
                      "Remove `.presentationBackground` so sheets and popovers use the system Liquid Glass appearance.")
    for m in re.finditer(r"configureWithOpaqueBackground\s*\(\s*\)|(?:UINavigationBarAppearance|UITabBarAppearance|UIToolbarAppearance)\b[^\n]*\n?[^\n]*\.backgroundColor\s*=", code):
        yield Finding("GLS-04", p, at(m), "Opaque/custom UIKit bar appearance.",
                      "Remove custom bar backgrounds so the system can render Liquid Glass (Adopting Liquid Glass).")

    # COL-01 — hard-coded color values in views
    if not re.search(r"(?:Color|Colour|Palette|Theme|Token)s?\.swift$", src.path.name):
        for m in re.finditer(r"\b(?:Color|UIColor|NSColor)\s*\(\s*(?:\.sRGB\s*,\s*|\.displayP3\s*,\s*)?(?:red|calibratedRed|srgbRed|displayP3Red|hue|white)\s*:|#colorLiteral\s*\(|\b(?:Color|UIColor|NSColor)\s*\(\s*hex\s*:", code):
            yield Finding("COL-01", p, at(m), "Hard-coded color value in view code.",
                          "Use a system/semantic color (`.blue`, `.primary`, `Color(.systemBackground)`) or a named asset-catalog Color Set with light, dark, and increased-contrast variants.")

    # COL-07 — forcing appearance
    for m in re.finditer(r"\.preferredColorScheme\s*\(|overrideUserInterfaceStyle\s*=", code):
        yield Finding("COL-07", p, at(m), "Forces a color scheme instead of following the system appearance.",
                      "Remove it and support light, dark, and Auto. Only immersive media views may stay dark (annotate with hig-ignore and a reason).")

    # TYP-01 / TYP-02 — fixed sizes and minimum size
    for m in re.finditer(r"(?:\.font\s*\(\s*)?(?:Font)?\.system\s*\(\s*size\s*:\s*([0-9.]+)|UIFont\.(?:systemFont|boldSystemFont|italicSystemFont|monospacedSystemFont|monospacedDigitSystemFont)\s*\(\s*ofSize\s*:\s*([0-9.]+)", code):
        size = num(m.group(1) or m.group(2) or "")
        if not appkit_only:
            yield Finding("TYP-01", p, at(m), "Fixed point size doesn't scale with Dynamic Type.",
                          "Use a text style: `.font(.body)`, `.headline`, `.caption`… or `UIFont.preferredFont(forTextStyle:)`.")
        if size is not None and size < min_text:
            yield Finding("TYP-02", p, at(m), f"Text is {size:g} pt — below the {min_text} pt minimum on {platform}.",
                          f"Use at least {min_text} pt (on iOS, `.caption2` is 11 pt).")
    for m in re.finditer(r"\.custom\s*\(\s*\"[^\"]*\"\s*,\s*(?:size|fixedSize)\s*:\s*([0-9.]+)[^)]*\)|UIFont\s*\(\s*name\s*:[^,]+,\s*size\s*:\s*([0-9.]+)", code):
        size = num(m.group(1) or m.group(2) or "")
        snippet = m.group(0)
        scales = "relativeTo" in snippet or ("UIFont(" in snippet and "UIFontMetrics" in code)
        if not scales and not appkit_only:
            yield Finding("TYP-05", p, at(m), "Custom font doesn't scale with Dynamic Type.",
                          "Use `Font.custom(_:size:relativeTo:)` or scale with `UIFontMetrics(forTextStyle:).scaledFont(for:)`; verify Bold Text.")
        if size is not None and size < min_text:
            yield Finding("TYP-02", p, at(m), f"Text is {size:g} pt — below the {min_text} pt minimum on {platform}.",
                          f"Use at least {min_text} pt.")

    # TYP-03 — light weights
    for m in re.finditer(r"(?:fontWeight\s*\(\s*|weight\s*:\s*)(?:Font\.Weight|UIFont\.Weight|NSFont\.Weight)?\.(ultraLight|thin|light)\b", code):
        yield Finding("TYP-03", p, at(m), f"`.{m.group(1)}` weight is hard to read in interface text.",
                      "Prefer .regular, .medium, .semibold, or .bold.")

    # TYP-04 — bundling system fonts
    for m in re.finditer(r"\.custom\s*\(\s*\"" + APPLE_FONT_NAME + r"|UIFont\s*\(\s*name\s*:\s*\"" + APPLE_FONT_NAME + r"|NSFont\s*\(\s*name\s*:\s*\"" + APPLE_FONT_NAME, code, re.I):
        yield Finding("TYP-04", p, at(m), "Loads an Apple system font by name, which implies bundling it.",
                      "Use the system font through `Font.Design` (.default, .serif, .rounded, .monospaced) — never embed SF or New York.")

    # TYP-08 — single-line truncation
    for m in re.finditer(r"\.lineLimit\s*\(\s*1\s*\)", code):
        yield Finding("TYP-08", p, at(m), "`.lineLimit(1)` truncates text at larger Dynamic Type sizes.",
                      "Allow more lines (or none) for meaningful text, or offer a way to read the full content.")

    # MOT-02 — animation without Reduce Motion handling
    anim = re.search(r"\bwithAnimation\s*\(|\.animation\s*\(|\.transition\s*\(|UIView\.animate\s*\(|\.phaseAnimator\s*\(|\.keyframeAnimator\s*\(|NSAnimationContext\.runAnimationGroup", code)
    if anim and not re.search(r"accessibilityReduceMotion|isReduceMotionEnabled|accessibilityDisplayShouldReduceMotion", code):
        yield Finding("MOT-02", p, at(anim), "Custom animation without a Reduce Motion check.",
                      "Read `@Environment(\\.accessibilityReduceMotion)` (or `UIAccessibility.isReduceMotionEnabled`) and replace movement with fades or no animation.")

    # A11Y-01 — small tap targets
    for m in re.finditer(r"\.frame\s*\(\s*width\s*:\s*([0-9.]+)\s*,\s*height\s*:\s*([0-9.]+)\s*\)", code):
        w, h = num(m.group(1)), num(m.group(2))
        if w is None or h is None:
            continue
        target = 28 if appkit_only else 44
        if min(w, h) >= target:
            continue
        line = at(m)
        ctx = src.window(line, 6, 4)
        if re.search(r"\bButton\b|\.onTapGesture|\bToggle\b|\bLink\b|\bMenu\b", ctx) and not re.search(r"\.contentShape|minWidth\s*:\s*(?:4[4-9]|[5-9]\d)|minHeight\s*:\s*(?:4[4-9]|[5-9]\d)|\.padding", ctx):
            yield Finding("A11Y-01", p, line, f"Tappable element is {w:g}×{h:g} pt — below the {target}×{target} pt minimum hit region.",
                          f"Give it at least {target}×{target} pt: `.frame(minWidth: {target}, minHeight: {target})` plus `.contentShape(Rectangle())`, keeping the visual size if needed.")

    # A11Y-03 — icon-only controls without labels
    for m in re.finditer(r"Image\s*\(\s*systemName\s*:\s*\"([^\"]+)\"\s*\)", code):
        line = at(m)
        after = src.window(line, 0, 6)
        in_button = icon_is_button_label(src, line, m.start() - src._line_starts[line - 1])
        tappable = re.search(r"\.onTapGesture", after)
        labelled = re.search(r"accessibilityLabel|accessibilityHidden|\bText\s*\(|\bLabel\s*\(", after)
        if (in_button or tappable) and not labelled:
            yield Finding("A11Y-03", p, line, f"Icon-only control `{m.group(1)}` has no accessibility label.",
                          f"Use `Button(\"<Action>\", systemImage: \"{m.group(1)}\")` with `.labelStyle(.iconOnly)`, or add `.accessibilityLabel(\"<Action>\")`.")

    # A11Y-04 — asset images without description or decorative marking
    for m in re.finditer(r"(?<![\w.])Image\s*\(\s*\"([^\"]+)\"\s*\)", code):
        line = at(m)
        before = src.window(line, 2, 0)
        after = src.window(line, 0, 6)
        if re.search(r"\bLabel\s*\{|\bLabel\s*\(|\bButton\b", before):
            continue
        if not re.search(r"accessibilityLabel|accessibilityHidden|accessibilityElement|accessibilityRepresentation", after):
            yield Finding("A11Y-04", p, line, f"Image `{m.group(1)}` has no description and isn't marked decorative.",
                          f"Add `.accessibilityLabel(\"…\")` if it conveys meaning, or use `Image(decorative: \"{m.group(1)}\")`.")

    # WRT-02 — vague link text
    yield from click_here(src, p)

    # NAV-09 — text Back/Close buttons
    for m in re.finditer(r"\bButton\s*\(\s*\"(?:[‹<←]\s*)?(Back|Close)\"|(?:\bButton\s*\{|label\s*:\s*\{)\s*Text\s*\(\s*\"(?:[‹<←]\s*)?(Back|Close)\"", code, re.S):
        word = m.group(1) or m.group(2)
        yield Finding("NAV-09", p, at(m), f"Text button labeled “{word}”.",
                      "Use the system back button (NavigationStack) or `Button(role: .close) { dismiss() }` (26+) / the standard Close symbol instead of a text label.")

    # CMP-13 — Yes/No buttons
    for m in re.finditer(r"\bButton\s*\(\s*\"(Yes|No)\"|UIAlertAction\s*\(\s*title\s*:\s*\"(Yes|No)\"", code):
        yield Finding("CMP-13", p, at(m), f"Button titled “{m.group(1) or m.group(2)}”.",
                      "Title alert buttons with a verb that names the result (“Delete”, “Keep Editing”) and use “Cancel” to cancel.")

    # CMP-21 — password in a plain text field
    for m in re.finditer(r"\bTextField\s*\(\s*\"([^\"]*(?:password|passcode|passwort|contraseña|mot de passe)[^\"]*)\"", code, re.I):
        yield Finding("CMP-21", p, at(m), f"Sensitive field “{m.group(1)}” uses TextField.",
                      "Use `SecureField` with `.textContentType(.password)` (or `.newPassword`), and never prefill it.")


def icon_is_button_label(src: Source, line: int, col: int) -> bool:
    """True when an Image(systemName:) is the whole label of a Button (no Text/Label beside it)."""
    same_line = src.lines[line - 1][:col]
    if re.search(r"\bButton\b[^\n]*\{\s*$|label\s*:\s*\{\s*$", same_line):
        return not re.search(r"\bText\s*\(|\bLabel\s*\(", same_line.split("Button")[-1])
    for back in range(1, 4):
        idx = line - 1 - back
        if idx < 0:
            break
        prev = src.lines[idx]
        if re.search(r"\bText\s*\(|\bLabel\s*\(", prev):
            return False
        if re.search(r"\bButton\b[^\n]*\{\s*$|label\s*:\s*\{\s*$", prev):
            return True
        if prev.strip().endswith("}"):
            return False
    return False


def click_here(src: Source, p: str) -> Iterable[Finding]:
    for m in re.finditer(r"click\s+here", src.text, re.I):
        yield Finding("WRT-02", p, src.line_of(m.start()), "Vague link text “click here”.",
                      "Describe the destination (“Learn more about sharing”); it also avoids the wrong gesture word on touch devices.")


# ---------------------------------------------------------------------------- CSS detectors

CSS_BLOCK = re.compile(r"(?P<sel>[^{}]+)\{(?P<body>[^{}]*)\}")
INTERACTIVE_SEL = re.compile(r"(?:^|[\s,>+~(])(?:button|a|input|select|summary|\[role=[\"']?(?:button|link|tab|menuitem|checkbox|switch)[\"']?\]|\.(?:btn|button)[\w-]*)(?=$|[\s,:.#\[>+~)])", re.I)


def css_len_to_px(value: str, unit: str) -> float | None:
    v = num(value)
    if v is None:
        return None
    unit = unit.lower()
    return {"px": v, "pt": v * 4 / 3, "rem": v * 16, "em": v * 16}.get(unit)


def style_detectors(src: Source, css: str, line_offset: int = 0, system_hex: dict[str, str] | None = None) -> Iterable[Finding]:
    p = str(src.path)
    code = strip_css_comments(css)
    is_tokens_file = src.path.name == "tokens.css"

    def line_at(offset: int) -> int:
        return src.line_of(line_offset + offset)

    # TYP-02 — tiny text
    for m in re.finditer(r"font-size\s*:\s*([0-9.]+)(px|pt|rem|em)\b", code, re.I):
        px = css_len_to_px(m.group(1), m.group(2))
        if px is not None and px < 11:
            yield Finding("TYP-02", p, line_at(m.start()), f"font-size {m.group(1)}{m.group(2)} (≈{px:g}px) is below the 11 pt iOS minimum.",
                          "Use at least 11px (0.6875rem); prefer the .adl-text-* styles from tokens.css.")

    # TYP-03 — light weights
    for m in re.finditer(r"font-weight\s*:\s*(100|200|300|lighter)\b", code, re.I):
        yield Finding("TYP-03", p, line_at(m.start()), f"font-weight {m.group(1)} is hard to read in interface text.",
                      "Use 400–700.")

    # TYP-04 — bundling Apple fonts
    for m in re.finditer(r"@font-face\s*\{[^}]*\}", code, re.I | re.S):
        if re.search(APPLE_FONT_NAME, m.group(0), re.I):
            yield Finding("TYP-04", p, line_at(m.start()), "@font-face bundles an Apple system font.",
                          "Remove it; use `-apple-system, system-ui, …` (see --adl-font-text in tokens.css).")

    # COL-07 — forcing one appearance
    for m in re.finditer(r"color-scheme\s*:\s*([^;}\n]+)", code, re.I):
        val = m.group(1).strip().lower()
        if "light" in val and "dark" not in val or ("dark" in val and "light" not in val and "only" in val):
            yield Finding("COL-07", p, line_at(m.start()), f"`color-scheme: {val}` locks the page to one appearance.",
                          "Use `color-scheme: light dark` and support both appearances.")

    # COL-01 — hard-coded Apple system color values
    if system_hex and not is_tokens_file:
        for m in re.finditer(r"#([0-9a-fA-F]{6})\b", code):
            hexv = "#" + m.group(1).upper()
            if hexv in system_hex:
                yield Finding("COL-01", p, line_at(m.start()), f"Hard-coded Apple system color value {hexv}.",
                              f"Use the token `var(--adl-{re.sub(r'(?<!^)(?=[A-Z])', '-', system_hex[hexv]).lower()})`, which adapts to dark mode and Increase Contrast.")

    # MOT-02 — animation without prefers-reduced-motion
    if not is_tokens_file:
        anim = re.search(r"@keyframes|animation(?:-name)?\s*:\s*(?!none)|transition\s*:\s*(?!none)", code, re.I)
        if anim and "prefers-reduced-motion" not in code:
            yield Finding("MOT-02", p, line_at(anim.start()), "Animation or transition without a `prefers-reduced-motion` alternative.",
                          "Add `@media (prefers-reduced-motion: reduce) { … }` that removes movement (keep short fades).")

    # A11Y-01 — small interactive targets
    for block in CSS_BLOCK.finditer(code):
        sel = block.group("sel").strip().split("}")[-1]
        if not INTERACTIVE_SEL.search(" " + sel):
            continue
        body = block.group("body")
        if re.search(r"min-(?:width|height)\s*:\s*(?:4[4-9]|[5-9]\d|\d{3,})px|min-(?:width|height)\s*:\s*var\(--adl-control-size\)", body):
            continue
        for m in re.finditer(r"(?<![-\w])(width|height)\s*:\s*([0-9.]+)(px|pt|rem|em)\b", body, re.I):
            px = css_len_to_px(m.group(2), m.group(3))
            if px is not None and px < 44:
                yield Finding("A11Y-01", p, line_at(block.start("body") + m.start()),
                              f"Interactive element `{sel[:60].strip()}` is {m.group(2)}{m.group(3)} {m.group(1)} — below the 44px touch minimum.",
                              "Ensure at least 44×44 px (e.g., `min-width/min-height: var(--adl-control-size)`), expanding the hit area with padding if the visual must stay small.")
                break


# ---------------------------------------------------------------------------- markup / script detectors

def markup_detectors(src: Source, system_hex: dict[str, str]) -> Iterable[Finding]:
    p = str(src.path)
    text = src.text

    # Inline <style> blocks
    for m in re.finditer(r"<style[^>]*>(.*?)</style>", text, re.I | re.S):
        yield from style_detectors(src, m.group(1), m.start(1), system_hex)

    if src.path.suffix.lower() in COMPONENT_EXT:
        yield from js_detectors(src, p, text, system_hex)
    yield from shared_markup_and_script(src, p, text)


def script_detectors(src: Source, system_hex: dict[str, str]) -> Iterable[Finding]:
    p = str(src.path)
    text = src.text
    yield from js_detectors(src, p, text, system_hex)

    if src.path.suffix.lower() in {".jsx", ".tsx"}:
        yield from shared_markup_and_script(src, p, text)
    else:
        yield from click_here(src, p)


TOKEN_FILES = {"tokens.css", "tokens.ts", "tokens.native.ts", "tailwind.css"}
TW_SPACING_PX = 4  # Tailwind v4 default --spacing: 0.25rem


def js_detectors(src: Source, p: str, text: str, system_hex: dict[str, str]) -> Iterable[Finding]:
    """Checks for JavaScript/TypeScript, JSX, Vue and Svelte components, Tailwind classes, and React Native."""

    # LAY-01 — user-agent sniffing for Apple devices
    for m in re.finditer(r"navigator\.(?:userAgent|platform)[^\n;]{0,80}(?:iPhone|iPad|iPod|Macintosh|MacIntel)|/(?:[^/\n]*\|)?(?:iPhone|iPad|iPod)(?:\|[^/\n]*)?/i?\.test\(\s*navigator\.(?:userAgent|platform)", text):
        yield Finding("LAY-01", p, src.line_of(m.start()), "Layout branches on the user agent / device.",
                      "Adapt to available space with media or container queries instead of detecting devices.")

    # Inline style objects in JSX/TSX
    for m in re.finditer(r"fontSize\s*:\s*['\"]?([0-9.]+)(px)?['\"]?", text):
        size = num(m.group(1))
        if size is not None and size < 11:
            yield Finding("TYP-02", p, src.line_of(m.start()), f"fontSize {m.group(1)} is below the 11 px minimum.",
                          "Use at least 11px; prefer the .adl-text-* classes.")
    for m in re.finditer(r"fontWeight\s*:\s*['\"]?(100|200|300|lighter)['\"]?", text):
        yield Finding("TYP-03", p, src.line_of(m.start()), f"fontWeight {m.group(1)} is hard to read in interface text.", "Use 400–700.")

    # CSS-in-JS template literals (styled-components, css``)
    for m in re.finditer(r"(?:styled\.[\w]+|styled\([^)]*\)|css|createGlobalStyle|keyframes)`(.*?)`", text, re.S):
        yield from style_detectors(src, m.group(1), m.start(1), system_hex)

    at = lambda m: src.line_of(m.start())  # noqa: E731

    # COL-01 — Apple system color values in strings, style objects, and Tailwind arbitrary values
    if system_hex and src.path.name not in TOKEN_FILES:
        for m in re.finditer(r"[\"'`\[]#([0-9a-fA-F]{6})\b", text):
            hexv = "#" + m.group(1).upper()
            if hexv in system_hex:
                yield Finding("COL-01", p, src.line_of(m.start() + 1), f"Hard-coded Apple system color value {hexv}.",
                              f"Use the token `var(--adl-{re.sub(r'(?<!^)(?=[A-Z])', '-', system_hex[hexv]).lower()})` "
                              "(Tailwind: the generated theme; React Native: `systemColor()`), which adapts to dark mode and Increase Contrast.")

    # TYP-02 / TYP-03 — Tailwind arbitrary text sizes and light weights
    for m in re.finditer(r"(?<![\w-])text-\[([0-9.]+)(px|rem)\]", text):
        px = css_len_to_px(m.group(1), m.group(2))
        if px is not None and px < 11:
            yield Finding("TYP-02", p, at(m), f"`{m.group(0)}` (≈{px:g}px) is below the 11 pt iOS minimum.",
                          "Use `text-caption2` or larger from the generated Tailwind theme.")
    for m in re.finditer(r"(?<![\w-])font-(thin|extralight|light)(?![\w-])", text):
        yield Finding("TYP-03", p, at(m), f"`font-{m.group(1)}` is hard to read in interface text.", "Use `font-normal` … `font-bold`.")

    # A11Y-01 — Tailwind size classes below 44 px on buttons and links
    for m in re.finditer(r"<(button|a)\b(" + TAG_ATTRS + r")>", text, re.I):
        cls = re.search(r"\bclass(?:Name)?\s*=\s*[\"'{`]([^\"'`}]*)", m.group(2))
        if not cls or re.search(r"min-(?:h|w)-(?:control|1[1-9]|[2-9]\d|\[(?:4[4-9]|[5-9]\d)px\])|size-control", cls.group(1)):
            continue
        sizes = [float(v) * TW_SPACING_PX for v in re.findall(r"(?<![\w-])(?:size|h|w)-(\d+(?:\.\d+)?)(?![\w.-])", cls.group(1))]
        if sizes and min(sizes) < 44:
            yield Finding("A11Y-01", p, at(m), f"<{m.group(1)}> is sized to {min(sizes):g}px — below the 44px touch minimum.",
                          "Add `min-h-control min-w-control` (44 px) from the generated Tailwind theme, keeping the icon small if needed.")

    # A11Y-05 — React Native text that can't scale; Next.js viewport that blocks zoom
    for m in re.finditer(r"allowFontScaling\s*(?:=\s*\{\s*false\s*\}|:\s*false)|maxFontSizeMultiplier\s*(?:=\s*\{\s*|:\s*)(?:0?\.\d+|1(?:\.0+)?)\b(?!\.\d*[1-9])", text):
        yield Finding("A11Y-05", p, at(m), "Text is prevented from scaling with the system text size.",
                      "Leave `allowFontScaling` on and don't cap `maxFontSizeMultiplier` at 1; use `dynamicTypeRamp` so text follows Dynamic Type.")
    for m in re.finditer(r"\b(?:maximumScale\s*:\s*1(?:\.0+)?\b|userScalable\s*:\s*(?:false|[\"']no[\"']))", text):
        yield Finding("A11Y-05", p, at(m), f"Viewport setting `{m.group(0)}` disables zoom.",
                      "Remove `maximumScale` and `userScalable` from the viewport export; keep `viewportFit: \"cover\"`.")

    # COL-07 — React Native forcing an appearance
    for m in re.finditer(r"Appearance\.setColorScheme\s*\(\s*[\"'](?:light|dark)[\"']", text):
        yield Finding("COL-07", p, at(m), "Forces a color scheme instead of following the system appearance.",
                      "Remove it and support light and dark with `PlatformColor` / `systemColor()`.")

    # LAY-01 — React Native device checks
    for m in re.finditer(r"\bPlatform\.isPad\b|\bDeviceInfo\.isTablet\s*\(", text):
        yield Finding("LAY-01", p, at(m), f"`{m.group(0)}` ties layout to a device type.",
                      "Decide layout from `useWindowDimensions()` — iPad and Mac windows resize.")

    # A11Y-03 — React Native pressables with no text and no label
    for m in re.finditer(r"<(Pressable|TouchableOpacity|TouchableHighlight|TouchableWithoutFeedback)\b(" + TAG_ATTRS + r")>(.*?)</\1>", text, re.S):
        attrs, inner = m.group(2), m.group(3)
        if re.search(r"accessibilityLabel\s*=|aria-label\s*=|accessibilityLabelledBy\s*=|aria-labelledby\s*=", attrs) or re.search(r"<Text\b", inner):
            continue
        yield Finding("A11Y-03", p, at(m), f"<{m.group(1)}> has no text and no accessibility label.",
                      "Add `accessibilityLabel=\"<Action>\"` (and `role=\"button\"`).")


def shared_markup_and_script(src: Source, p: str, text: str) -> Iterable[Finding]:
    # A11Y-05 — zoom disabled
    for m in re.finditer(r"<meta[^>]+name=[\"']viewport[\"'][^>]*>", text, re.I):
        tag = m.group(0)
        if re.search(r"user-scalable\s*=\s*(?:no|0)|maximum-scale\s*=\s*1(?:\.0+)?(?![\d.])", tag, re.I):
            yield Finding("A11Y-05", p, src.line_of(m.start()), "Viewport disables zoom.",
                          "Remove `user-scalable=no` and `maximum-scale=1`; use `width=device-width, initial-scale=1, viewport-fit=cover`.")

    # COL-07 — color-scheme meta locked to one appearance
    for m in re.finditer(r"<meta[^>]+name=[\"']color-scheme[\"'][^>]*content=[\"']([^\"']+)[\"']", text, re.I):
        val = m.group(1).lower()
        if not ("light" in val and "dark" in val):
            yield Finding("COL-07", p, src.line_of(m.start()), f"color-scheme meta `{val}` locks one appearance.",
                          "Use `<meta name=\"color-scheme\" content=\"light dark\">`.")

    # TYP-04 — preloading/linking Apple font files
    for m in re.finditer(r"(?:href|src)=[\"'][^\"']*" + APPLE_FONT_NAME + r"[^\"']*\.(?:otf|ttf|woff2?)[\"']", text, re.I):
        yield Finding("TYP-04", p, src.line_of(m.start()), "Loads an Apple system font file.",
                      "Remove it; reference system fonts by family name (`-apple-system, system-ui`).")

    # A11Y-04 — images without alt
    for m in re.finditer(r"<img\b(?![^>]*\balt\s*=)[^>]*>", text, re.I):
        yield Finding("A11Y-04", p, src.line_of(m.start()), "<img> without an alt attribute.",
                      "Add `alt=\"…\"` describing the image, or `alt=\"\"` if purely decorative.")

    # A11Y-03 — buttons/links with no accessible name
    for m in re.finditer(r"<(button|a)\b(" + TAG_ATTRS + r")>(.*?)</\1>", text, re.I | re.S):
        attrs, inner = m.group(2), m.group(3)
        if re.search(r"aria-label(?:ledby)?\s*=|title\s*=", attrs, re.I):
            continue
        if not has_accessible_text(inner):
            yield Finding("A11Y-03", p, src.line_of(m.start()), f"<{m.group(1)}> has no accessible name.",
                          "Add visible text, `aria-label=\"…\"`, or visually hidden text for icon-only controls.")

    # STK-03 — click handlers on non-interactive elements
    for m in re.finditer(r"<(div|span|li|p|img|section|article)\b(" + TAG_ATTRS + r")>", text, re.I):
        attrs = m.group(2)
        if re.search(r"(?<![\w-])(?:onClick|onclick|@click|v-on:click|on:click)\s*=", attrs) and not re.search(r"\brole\s*=", attrs):
            yield Finding("STK-03", p, src.line_of(m.start()), f"<{m.group(1)}> has a click handler but no role or keyboard support.",
                          "Use a `<button type=\"button\">` (or `<a href>` for navigation); it brings the role, focus, and keyboard activation.")

    # CMP-21 — password inputs not typed as password
    for m in re.finditer(r"<input\b[^>]*>", text, re.I):
        tag = m.group(0)
        if re.search(r"(?:name|id|placeholder|autocomplete)\s*=\s*[\"'{][^\"'}]*(?:password|passcode)", tag, re.I) and not re.search(r"type\s*=\s*[\"']password[\"']", tag, re.I):
            yield Finding("CMP-21", p, src.line_of(m.start()), "Password input isn't `type=\"password\"`.",
                          "Use `type=\"password\"` with `autocomplete=\"current-password\"` or `\"new-password\"`, and never prefill it.")

    yield from click_here(src, p)


# Attributes of an HTML/JSX start tag, allowing `>` inside {…} expressions such as onClick={() => f()}.
TAG_ATTRS = r"(?:[^>{]|\{(?:[^{}]|\{[^{}]*\})*\})*"
ICON_EXPR = re.compile(r"^\{\s*[\w.]*icon[\w.]*\s*\}$", re.I)


def has_accessible_text(inner: str) -> bool:
    """True when element content can supply an accessible name: visible text, a labelled child, or a
    JSX/Vue/Svelte expression that isn't obviously an icon. Content inside aria-hidden elements doesn't count."""
    if re.search(r"aria-label(?:ledby)?\s*=|<title>|\balt\s*=\s*[\"'][^\"']+", inner, re.I):
        return True
    hidden = re.compile(r"<(\w+)\b[^>]*aria-hidden\s*=\s*(?:[\"']true[\"']|\{true\})[^>]*>.*?</\1>", re.I | re.S)
    inner = hidden.sub("", inner)
    inner = re.sub(r"<[^>]+/>", "", inner)          # self-closing elements (icons)
    inner = re.sub(r"<[^>]+>", "", inner)           # remaining tags; keep their text
    for expr in re.findall(r"\{\{.*?\}\}|\{[^{}]*\}", inner, re.S):
        body = expr.strip("{} \n")
        if body and not ICON_EXPR.match("{" + body + "}") and not body.startswith("/*"):
            return True
    visible = re.sub(r"\{\{.*?\}\}|\{[^{}]*\}|&nbsp;|\s", "", inner, flags=re.S)
    return bool(visible)


def plist_detectors(src: Source) -> Iterable[Finding]:
    p = str(src.path)
    block = re.search(r"<key>UIAppFonts</key>\s*<array>(.*?)</array>", src.text, re.S)
    if block:
        for m in re.finditer(r"<string>([^<]+)</string>", block.group(1)):
            if APPLE_FONT_FILE.match(Path(m.group(1)).name) or re.search(APPLE_FONT_NAME, m.group(1), re.I):
                yield Finding("TYP-04", p, src.line_of(block.start(1) + m.start()), f"UIAppFonts bundles Apple system font `{m.group(1)}`.",
                              "Remove the font file and entry; use the system font via `Font.Design`.")


def font_file_detectors(path: Path) -> Iterable[Finding]:
    if APPLE_FONT_FILE.match(path.name):
        yield Finding("TYP-04", str(path), 1, f"Apple system font file `{path.name}` is bundled in the project.",
                      "Delete it; Apple system fonts must not be embedded. Use system font APIs or `system-ui`.")


# ---------------------------------------------------------------------------- engine

DETECTED_RULES = {
    "LAY-01", "GLS-02", "GLS-04", "GLS-08", "COL-01", "COL-07", "TYP-01", "TYP-02", "TYP-03", "TYP-04",
    "TYP-05", "TYP-08", "MOT-02", "A11Y-01", "A11Y-03", "A11Y-04", "A11Y-05", "WRT-02", "NAV-09", "CMP-13", "CMP-21",
    "STK-03",
}


def suppressed(src: Source | None, finding: Finding) -> bool:
    if src is None:
        return False
    for ln in (finding.line, finding.line - 1):
        if 1 <= ln <= len(src.lines):
            m = SUPPRESS_RE.search(src.lines[ln - 1])
            if m and finding.rule in [i.strip() for i in m.group("ids").split(",")]:
                return True
    return False


def lint_file(path: Path, rules: dict[str, dict], system_hex: dict[str, str]) -> list[Finding]:
    ext = path.suffix.lower()
    if ext not in SUPPORTED_EXT:
        return []
    if ext in FONT_EXT:
        raw: list[Finding] = list(font_file_detectors(path))
        src = None
    else:
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return []
        src = Source(path, text)
        if ext in SWIFT_EXT:
            raw = list(swift_detectors(src))
        elif ext in STYLE_EXT:
            raw = list(style_detectors(src, text, 0, system_hex))
        elif ext in MARKUP_EXT:
            raw = list(markup_detectors(src, system_hex))
        elif ext in SCRIPT_EXT:
            raw = list(script_detectors(src, system_hex))
        elif ext in PLIST_EXT:
            raw = list(plist_detectors(src))
        else:  # .strings / .xcstrings
            raw = list(click_here(src, str(path)))

    out: list[Finding] = []
    seen: set[tuple] = set()
    for f in raw:
        rule = rules.get(f.rule)
        if rule is None or rule.get("check") != "hook":
            raise RuntimeError(f"detector emitted {f.rule}, which isn't a `Check: hook` rule in rules.json")
        key = (f.rule, f.path, f.line, f.message)
        if key in seen or suppressed(src, f):
            continue
        seen.add(key)
        f.severity, f.level, f.title = rule["severity"], rule["level"], rule["title"]
        f.link = f"{rule['file']}#{github_slug(rule['id'] + ' · ' + rule['title'])}"
        out.append(f)
    out.sort(key=lambda f: (-SEVERITY_ORDER[f.severity], f.path, f.line, f.rule))
    return out


def iter_paths(paths: Iterable[str]) -> Iterable[Path]:
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            for dirpath, dirnames, filenames in os.walk(p):
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.endswith((".xcassets", ".xcodeproj", ".xcworkspace"))]
                for name in sorted(filenames):
                    fp = Path(dirpath) / name
                    if fp.suffix.lower() in SUPPORTED_EXT:
                        yield fp
        elif p.exists():
            yield p


def format_text(findings: list[Finding], files_checked: int) -> str:
    counts = {s: sum(f.severity == s for f in findings) for s in ("error", "warning", "info")}
    if not findings:
        return f"hig-lint: {files_checked} file(s) checked — no issues found."
    lines = [f"hig-lint: {counts['error']} error(s), {counts['warning']} warning(s), {counts['info']} info in {files_checked} file(s) checked"]
    for f in findings:
        lines.append(f"  {f.severity:<7} {f.rule:<8} {f.path}:{f.line}  {f.message}")
        lines.append(f"          fix: {f.fix}")
        lines.append(f"          rule: {f.level} — {f.title} ({f.link})")
    lines.append("Suppress a deliberate exception with `hig-ignore: RULE-ID — reason` on the line or the line above.")
    return "\n".join(lines)


def run_cli(args: argparse.Namespace) -> int:
    rules = load_rules()
    if args.list_rules:
        hook_rules = [r for r in rules.values() if r["check"] == "hook"]
        for r in hook_rules:
            status = "ok" if r["id"] in DETECTED_RULES else "MISSING DETECTOR"
            print(f"{r['id']:<8} {r['severity']:<7} {status:<16} {r['title']}")
        return 0 if all(r["id"] in DETECTED_RULES for r in hook_rules) else 1

    system_hex = load_system_hex()
    minimum = SEVERITY_ORDER[args.min_severity]
    files = list(iter_paths(args.paths))
    findings = [f for fp in files for f in lint_file(fp, rules, system_hex) if SEVERITY_ORDER[f.severity] >= minimum]
    if args.format == "json":
        print(json.dumps({"files_checked": len(files), "findings": [asdict(f) for f in findings]}, indent=2, ensure_ascii=False))
    else:
        print(format_text(findings, len(files)))
    return 1 if any(f.severity == "error" for f in findings) else 0


def run_hook() -> int:
    """PostToolUse handler. Always exits 0; decisions travel in JSON on stdout."""
    try:
        if os.environ.get("HIG_LINT", "").lower() in {"off", "0", "false", "no"}:
            return 0
        payload = json.load(sys.stdin)
        tool_input = payload.get("tool_input") or {}
        file_path = tool_input.get("file_path") or tool_input.get("path")
        if not file_path:
            return 0
        path = Path(file_path)
        if not path.is_absolute():
            path = Path(payload.get("cwd") or os.getcwd()) / path
        if path.suffix.lower() not in SUPPORTED_EXT or not path.exists():
            return 0
        minimum = SEVERITY_ORDER.get(os.environ.get("HIG_LINT_MIN_SEVERITY", "warning").lower(), 1)
        findings = [f for f in lint_file(path, load_rules(), load_system_hex()) if SEVERITY_ORDER[f.severity] >= minimum]
        if not findings:
            return 0
        report = format_text(findings, 1)
        if len(report) > HOOK_OUTPUT_LIMIT:
            report = report[:HOOK_OUTPUT_LIMIT] + "\n… (truncated — run hooks/scripts/hig_lint.py on the file for the full list)"
        header = "Apple Design Language check (rules/README.md). "
        if any(f.severity == "error" for f in findings):
            out = {"decision": "block",
                   "reason": header + "Fix these errors before continuing; fix warnings or annotate deliberate exceptions.\n" + report}
        else:
            out = {"hookSpecificOutput": {"hookEventName": "PostToolUse",
                                          "additionalContext": header + "Warnings — fix them or annotate a deliberate exception with a reason.\n" + report}}
        print(json.dumps(out, ensure_ascii=False))
        return 0
    except Exception as exc:  # never break the editing loop because of the checker itself
        print(f"hig-lint hook error: {exc}", file=sys.stderr)
        return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Check UI files against the Apple Design Language hook rules.")
    ap.add_argument("paths", nargs="*", help="files or directories to check")
    ap.add_argument("--hook", action="store_true", help="run as a Claude Code PostToolUse hook (reads JSON on stdin)")
    ap.add_argument("--format", choices=["text", "json"], default="text")
    ap.add_argument("--min-severity", choices=list(SEVERITY_ORDER), default="info")
    ap.add_argument("--list-rules", action="store_true", help="list hook rules and detector coverage")
    args = ap.parse_args(argv)
    if args.hook:
        return run_hook()
    if not args.paths and not args.list_rules:
        ap.error("provide at least one path, --hook, or --list-rules")
    return run_cli(args)


if __name__ == "__main__":
    sys.exit(main())

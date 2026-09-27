#!/usr/bin/env python3
"""Validate assets/tokens.json and generate assets/tokens.css + references/design-tokens.md.

Part of the Apple Design Language skill — Created by Edison Augustin X.

tokens.json is the single source of truth for every value in this skill. Values come from
Apple's Human Interface Guidelines; this script keeps the CSS and Markdown renderings in sync.

Usage:
    python3 scripts/build_tokens.py          # validate and regenerate
    python3 scripts/build_tokens.py --check  # validate; exit 2 if generated files are stale
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
TOKENS = SKILL / "assets" / "tokens.json"
CSS_OUT = SKILL / "assets" / "tokens.css"
MD_OUT = SKILL / "references" / "design-tokens.md"

HEX = re.compile(r"^#[0-9A-F]{6}$")
PLATFORMS = ["ios", "ipados", "macos", "tvos", "visionos", "watchos"]
PLATFORM_LABEL = {"ios": "iOS", "ipados": "iPadOS", "macos": "macOS", "tvos": "tvOS", "visionos": "visionOS", "watchos": "watchOS"}
COLOR_VARIANTS = ["light", "dark", "lightIncreasedContrast", "darkIncreasedContrast"]
IOS_DYNAMIC_TYPE = ["xSmall", "Small", "Medium", "Large (default)", "xLarge", "xxLarge", "xxxLarge", "AX1", "AX2", "AX3", "AX4", "AX5"]
TEXT_STYLE_SLUG = {
    "Large Title": "large-title", "Title 1": "title1", "Title 2": "title2", "Title 3": "title3",
    "Headline": "headline", "Body": "body", "Callout": "callout", "Subhead": "subheadline",
    "Footnote": "footnote", "Caption 1": "caption1", "Caption 2": "caption2",
}
# WebKit Dynamic Type font keywords (https://webkit.org/blog/3709/using-the-system-font-in-web-content/)
WEBKIT_DYNAMIC_TYPE = {
    "headline": "-apple-system-headline", "body": "-apple-system-body", "subheadline": "-apple-system-subheadline",
    "footnote": "-apple-system-footnote", "caption1": "-apple-system-caption1", "caption2": "-apple-system-caption2",
}
WEIGHT = {"Ultralight": 100, "Thin": 200, "Light": 300, "Regular": 400, "Medium": 500, "Semibold": 600, "Bold": 700, "Heavy": 800, "Black": 900}


# ---------------------------------------------------------------------------- validation

def validate(t: dict) -> list[str]:
    errors: list[str] = []

    def need(path: str):
        node = t
        for key in path.split("."):
            if not isinstance(node, dict) or key not in node:
                errors.append(f"missing key: {path}")
                return None
            node = node[key]
        return node

    for group in ("system", "gray"):
        colors = need(f"color.{group}") or {}
        if group == "system" and len(colors) != 12:
            errors.append(f"color.system must list the 12 HIG system colors, found {len(colors)}")
        for key, c in colors.items():
            for v in COLOR_VARIANTS:
                if not HEX.match(str(c.get(v, ""))):
                    errors.append(f"color.{group}.{key}.{v} is not an uppercase #RRGGBB hex value")
            if not c.get("api", {}).get("uikit"):
                errors.append(f"color.{group}.{key} missing api.uikit")

    sizes = need("typography.platformSizes") or {}
    for p in PLATFORMS:
        s = sizes.get(p)
        if not s:
            errors.append(f"typography.platformSizes.{p} missing")
        elif not s["minimum"] < s["default"]:
            errors.append(f"typography.platformSizes.{p}: minimum must be below default")

    ios = (need("typography.textStyles.ios.sizes") or {})
    if list(ios) != IOS_DYNAMIC_TYPE:
        errors.append(f"iOS Dynamic Type sizes must be {IOS_DYNAMIC_TYPE}")
    for size_name, styles in ios.items():
        if [s["style"] for s in styles] != list(TEXT_STYLE_SLUG):
            errors.append(f"iOS size {size_name}: unexpected text style order")
        for s in styles:
            if s["weight"] not in WEIGHT or s["emphasized"] not in WEIGHT:
                errors.append(f"iOS size {size_name} {s['style']}: unknown weight")
            if s["leading"] < s["size"]:
                errors.append(f"iOS size {size_name} {s['style']}: leading below size")
    large = {s["style"]: s for s in ios.get("Large (default)", [])}
    if large and large["Body"]["size"] != sizes.get("ios", {}).get("default"):
        errors.append("iOS Large Body size must equal the iOS default text size")
    if ios:
        smallest = min(s["size"] for styles in ios.values() for s in styles)
        if smallest < sizes["ios"]["minimum"]:
            errors.append("an iOS text style is below the iOS minimum text size")

    controls = need("accessibility.controlSize") or {}
    for p in PLATFORMS:
        c = controls.get(p)
        if not c:
            errors.append(f"accessibility.controlSize.{p} missing")
        elif not c["minimum"] <= c["default"]:
            errors.append(f"accessibility.controlSize.{p}: minimum must not exceed default")
    return errors


# ---------------------------------------------------------------------------- CSS

def css_var(name: str) -> str:
    return "--adl-" + re.sub(r"(?<!^)(?=[A-Z])", "-", name).lower()


def render_css(t: dict) -> str:
    sysc, gray = t["color"]["system"], t["color"]["gray"]
    ios_large = {TEXT_STYLE_SLUG[s["style"]]: s for s in t["typography"]["textStyles"]["ios"]["sizes"]["Large (default)"]}
    ctl = t["accessibility"]["controlSize"]
    pad = t["accessibility"]["controlPadding"]

    def color_block(variant: str) -> list[str]:
        out = [f"  {css_var(k)}: {v[variant]};" for k, v in sysc.items()]
        out += [f"  {css_var(k)}: {v[variant]};" for k, v in gray.items()]
        return out

    L = []
    L.append("/*")
    L.append(" * Apple Design Language — web adaptation tokens")
    L.append(" * Created by Edison Augustin X.")
    L.append(" *")
    L.append(" * GENERATED by skills/apple-design-language/scripts/build_tokens.py from assets/tokens.json.")
    L.append(" * Do not edit by hand. Color and type values: Apple Human Interface Guidelines")
    L.append(f" * ({t['$meta']['verifiedAgainst']}).")
    L.append(" *")
    L.append(" * For WEB projects only. Native apps must use system APIs (Color.blue, .font(.body), …).")
    L.append(" * Values marked “project default” are NOT Apple specifications; tune them and re-check contrast.")
    L.append(" * Browser support notes: see references/web-adaptation.md.")
    L.append(" */")
    L.append("")
    L.append(":root {")
    L.append("  color-scheme: light dark;")
    L.append("")
    L.append("  /* System colors — light (HIG default light values) */")
    L += color_block("light")
    L.append("")
    L.append("  /* Semantic roles (web adaptation). CSS system colors follow the user's appearance. */")
    L.append("  --adl-accent: var(--adl-blue);")
    L.append("  --adl-destructive: var(--adl-red);")
    L.append("  --adl-background: Canvas;")
    L.append("  --adl-label: CanvasText;")
    L.append("  --adl-background-grouped: var(--adl-system-gray6);")
    L.append("  --adl-separator: var(--adl-system-gray4);")
    L.append("")
    L.append("  /* Typography — system font stacks (never bundle Apple system fonts; TYP-04) */")
    L.append("  --adl-font-text: -apple-system, system-ui, BlinkMacSystemFont, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, sans-serif;")
    L.append("  --adl-font-rounded: ui-rounded, -apple-system, system-ui, sans-serif;")
    L.append("  --adl-font-serif: ui-serif, Georgia, \"Times New Roman\", serif;")
    L.append("  --adl-font-mono: ui-monospace, Menlo, Consolas, \"Liberation Mono\", monospace;")
    L.append("")
    L.append("  /* iOS text styles at the Large (default) Dynamic Type size, in rem so browser text settings scale them */")
    for slug, s in ios_large.items():
        L.append(f"  --adl-text-{slug}-size: {s['size'] / 16:g}rem; /* {s['size']} pt */")
        L.append(f"  --adl-text-{slug}-line-height: {s['leading'] / 16:g}rem; /* {s['leading']} pt leading */")
        L.append(f"  --adl-text-{slug}-weight: {WEIGHT[s['weight']]};")
    L.append(f"  --adl-text-minimum-size: {t['typography']['platformSizes']['ios']['minimum'] / 16:g}rem; /* iOS minimum {t['typography']['platformSizes']['ios']['minimum']} pt (TYP-02) */")
    L.append("")
    L.append("  /* Hit targets and spacing (A11Y-01, A11Y-02) */")
    L.append(f"  --adl-control-size: {ctl['ios']['default']}px;          /* iOS/iPadOS default */")
    L.append(f"  --adl-control-size-minimum: {ctl['ios']['minimum']}px;  /* iOS/iPadOS minimum */")
    L.append(f"  --adl-control-size-pointer: {ctl['macos']['default']}px; /* macOS default — only for pointer-only surfaces you control */")
    L.append(f"  --adl-control-padding-bezeled: {pad['bezeled']}px;")
    L.append(f"  --adl-control-padding-plain: {pad['nonBezeled']}px;")
    L.append("")
    L.append("  /* Safe areas (requires <meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">) */")
    for edge in ("top", "right", "bottom", "left"):
        L.append(f"  --adl-safe-{edge}: env(safe-area-inset-{edge}, 0px);")
    L.append("")
    L.append("  /* Glass approximation — project defaults, NOT Apple values. Real Liquid Glass is native-only. */")
    L.append("  --adl-glass-fill: rgb(255 255 255 / 0.72);")
    L.append("  --adl-glass-blur: 20px;")
    L.append("  --adl-glass-stroke: rgb(0 0 0 / 0.08);")
    L.append("")
    L.append("  /* Motion — project defaults, NOT Apple values (MOT-01, MOT-02) */")
    L.append("  --adl-motion-duration: 250ms;")
    L.append("  --adl-motion-easing: cubic-bezier(0.2, 0, 0, 1);")
    L.append("}")
    L.append("")
    L.append("@media (prefers-color-scheme: dark) {")
    L.append("  :root {")
    L += ["  " + line for line in color_block("dark")]
    L.append("    --adl-glass-fill: rgb(30 30 30 / 0.6);")
    L.append("    --adl-glass-stroke: rgb(255 255 255 / 0.12);")
    L.append("  }")
    L.append("}")
    L.append("")
    L.append("/* Increase Contrast → HIG increased-contrast values (COL-02, COL-06) */")
    L.append("@media (prefers-contrast: more) {")
    L.append("  :root {")
    L += ["  " + line for line in color_block("lightIncreasedContrast")]
    L.append("  }")
    L.append("}")
    L.append("@media (prefers-contrast: more) and (prefers-color-scheme: dark) {")
    L.append("  :root {")
    L += ["  " + line for line in color_block("darkIncreasedContrast")]
    L.append("  }")
    L.append("}")
    L.append("")
    L.append("/* Base */")
    L.append("html { -webkit-text-size-adjust: 100%; text-size-adjust: 100%; }")
    L.append("body {")
    L.append("  margin: 0;")
    L.append("  background: var(--adl-background);")
    L.append("  color: var(--adl-label);")
    L.append("  font-family: var(--adl-font-text);")
    L.append("  font-size: var(--adl-text-body-size);")
    L.append("  line-height: var(--adl-text-body-line-height);")
    L.append("}")
    L.append("")
    L.append("/* Text styles. Where WebKit supports its Dynamic Type keywords, the second `font` declaration")
    L.append("   follows the iOS text size setting; other browsers ignore it and keep the fallback. */")
    for slug, s in ios_large.items():
        L.append(f".adl-text-{slug} {{")
        L.append(f"  font: var(--adl-text-{slug}-weight) var(--adl-text-{slug}-size)/var(--adl-text-{slug}-line-height) var(--adl-font-text);")
        if slug in WEBKIT_DYNAMIC_TYPE:
            L.append(f"  font: {WEBKIT_DYNAMIC_TYPE[slug]};")
        L.append("}")
    L.append("")
    L.append("/* Controls: never smaller than the platform default hit region (A11Y-01) */")
    L.append(".adl-control {")
    L.append("  min-width: var(--adl-control-size);")
    L.append("  min-height: var(--adl-control-size);")
    L.append("}")
    L.append("/* The 44 pt touch default applies everywhere: hybrid devices (iPad + trackpad) report fine pointers too. */")
    L.append("")
    L.append("/* Visible keyboard focus (A11Y-07) */")
    L.append(":focus-visible { outline: 3px solid var(--adl-accent); outline-offset: 2px; }")
    L.append("")
    L.append("/* Floating bars (web analog of the functional layer). Keep content legible beneath (LAY-08). */")
    L.append(".adl-glass {")
    L.append("  background: var(--adl-glass-fill);")
    L.append("  -webkit-backdrop-filter: blur(var(--adl-glass-blur)) saturate(180%);")
    L.append("  backdrop-filter: blur(var(--adl-glass-blur)) saturate(180%);")
    L.append("  border: 1px solid var(--adl-glass-stroke);")
    L.append("}")
    L.append("/* Opaque fallbacks: Increase Contrast everywhere; Reduce Transparency where the browser exposes it. */")
    L.append("@media (prefers-contrast: more), (prefers-reduced-transparency: reduce) {")
    L.append("  .adl-glass { background: var(--adl-background); -webkit-backdrop-filter: none; backdrop-filter: none; }")
    L.append("}")
    L.append("@supports not ((backdrop-filter: blur(1px)) or (-webkit-backdrop-filter: blur(1px))) {")
    L.append("  .adl-glass { background: var(--adl-background); }")
    L.append("}")
    L.append("")
    L.append("/* Reduce Motion: replace movement with short fades rather than removing feedback (MOT-02) */")
    L.append("@media (prefers-reduced-motion: reduce) {")
    L.append("  :root { --adl-motion-duration: 1ms; }")
    L.append("  *, *::before, *::after { scroll-behavior: auto !important; }")
    L.append("}")
    L.append("")
    return "\n".join(L)


# ---------------------------------------------------------------------------- Markdown

def relative_luminance(hex_color: str) -> float:
    def channel(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5))
    return 0.2126 * channel(r) + 0.7152 * channel(g) + 0.0722 * channel(b)


def contrast_ratio(fg: str, bg: str) -> float:
    hi, lo = sorted((relative_luminance(fg), relative_luminance(bg)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)


def contrast_cell(fg: str, bg: str) -> str:
    ratio = contrast_ratio(fg, bg)
    mark = "✓" if ratio >= 4.5 else "◐" if ratio >= 3 else "✗"
    return f"{ratio:.2f} {mark}"


def render_md(t: dict) -> str:
    m = t["$meta"]
    L = [
        "# Design tokens",
        "",
        "> **Created by Edison Augustin X.** · GENERATED from [`../assets/tokens.json`](../assets/tokens.json) by `scripts/build_tokens.py` — do not edit by hand.",
        f"> Verified against: {m['verifiedAgainst']}.",
        "",
        "**How to use these values:** in native apps, use the system API column — never hard-code these values (COL-01, TYP-01). "
        "Use the numbers for mockups, validation, reviews, and web adaptation ([`../assets/tokens.css`](../assets/tokens.css)).",
        "",
        "## Contents",
        "1. [System colors](#system-colors)",
        "2. [System grays](#system-grays)",
        "3. [Platform text sizes](#platform-text-sizes)",
        "4. [iOS and iPadOS Dynamic Type](#ios-and-ipados-dynamic-type)",
        "5. [macOS text styles](#macos-text-styles)",
        "6. [tvOS text styles](#tvos-text-styles)",
        "7. [watchOS Dynamic Type](#watchos-dynamic-type)",
        "8. [Contrast of system colors](#contrast-of-system-colors)",
        "9. [Accessibility metrics](#accessibility-metrics)",
        "10. [Layout specifications](#layout-specifications)",
        "11. [App icons and images](#app-icons-and-images)",
        "",
        "## System colors",
        "",
        t["color"]["note"],
        "",
        "| Color | SwiftUI | UIKit | AppKit | Light | Dark | Light (increased contrast) | Dark (increased contrast) |",
        "|---|---|---|---|---|---|---|---|",
    ]
    for c in t["color"]["system"].values():
        a = c["api"]
        L.append(f"| {c['name']} | `{a['swiftui']}` | `{a['uikit']}` | `{a['appkit']}` | `{c['light']}` | `{c['dark']}` | `{c['lightIncreasedContrast']}` | `{c['darkIncreasedContrast']}` |")
    L += ["", "## System grays", "", "iOS and iPadOS. `systemGray2`–`systemGray6` are UIKit colors; SwiftUI reaches them through `Color(uiColor:)`.", "",
          "| Gray | SwiftUI | UIKit | Light | Dark | Light (increased contrast) | Dark (increased contrast) |", "|---|---|---|---|---|---|---|"]
    for c in t["color"]["gray"].values():
        a = c["api"]
        L.append(f"| {c['name']} | `{a['swiftui']}` | `{a['uikit']}` | `{c['light']}` | `{c['dark']}` | `{c['lightIncreasedContrast']}` | `{c['darkIncreasedContrast']}` |")

    ps = t["typography"]["platformSizes"]
    fam = t["typography"]["families"]
    L += ["", "## Platform text sizes", "", "| Platform | Default | Minimum | System family |", "|---|---|---|---|"]
    for p in PLATFORMS:
        L.append(f"| {PLATFORM_LABEL[p]} | {ps[p]['default']} pt | {ps[p]['minimum']} pt | {fam[p]} |")
    L += ["", f"Serif family: {fam['serif']} · watchOS complications: {fam['watchosComplications']} · text enlargement target: {t['typography']['textEnlargementTarget']['default']} ({t['typography']['textEnlargementTarget']['watchos']} on watchOS)."]

    def style_table(styles, lead="Leading"):
        out = [f"| Style | Weight | Size (pt) | {lead} (pt) | Emphasized |", "|---|---|---|---|---|"]
        out += [f"| {s['style']} | {s['weight']} | {s['size']} | {s['leading']} | {s['emphasized']} |" for s in styles]
        return out

    L += ["", "## iOS and iPadOS Dynamic Type", "", t["typography"]["textStyles"]["ios"]["note"], ""]
    ios = t["typography"]["textStyles"]["ios"]["sizes"]
    names = list(ios)
    L.append("**Body size across all sizes:** " + " · ".join(f"{n.split(' (')[0]} {next(s['size'] for s in ios[n] if s['style']=='Body')}" for n in names))
    for n in names:
        L += ["", f"### iOS {n}", ""] + style_table(ios[n])

    L += ["", "## macOS text styles", "", t["typography"]["textStyles"]["macos"]["note"], ""] + style_table(t["typography"]["textStyles"]["macos"]["styles"], "Line height")
    L += ["", "## tvOS text styles", "", t["typography"]["textStyles"]["tvos"]["note"], ""] + style_table(t["typography"]["textStyles"]["tvos"]["styles"])
    L += ["", "## watchOS Dynamic Type", "", t["typography"]["textStyles"]["watchos"]["note"]]
    for n, styles in t["typography"]["textStyles"]["watchos"]["sizes"].items():
        L += ["", f"### watchOS {n}", ""] + style_table(styles)

    L += ["", "## Contrast of system colors", "",
          "WCAG 2 contrast ratio of each system color used as a foreground on pure white (light) or pure black (dark), "
          "computed by `scripts/build_tokens.py` from the values above. ✓ = meets 4.5:1 (small text); ◐ = meets 3:1 (large or bold text, icons); ✗ = below 3:1.", "",
          "| Color | Light on white | Dark on black | Light increased contrast on white | Dark increased contrast on black |", "|---|---|---|---|---|"]
    for c in t["color"]["system"].values():
        cells = [contrast_cell(c[v], "#FFFFFF" if v.startswith("light") else "#000000") for v in COLOR_VARIANTS]
        L.append(f"| {c['name']} | " + " | ".join(cells) + " |")
    L += ["", "Takeaway: default light-mode system colors (except indigo) are for fills, icons, tints, and large/bold text; "
          "small text needs the label color or an increased-contrast variant (COL-06)."]

    a = t["accessibility"]
    L += ["", "## Accessibility metrics", "", "**Minimum contrast (WCAG AA, as used by Accessibility Inspector)**", "", "| Text size | Weight | Minimum ratio |", "|---|---|---|"]
    L += [f"| {c['textSize']} | {c['weight']} | {c['minimumRatio']} |" for c in a["contrast"]]
    L += ["", f"Custom foreground/background pairs: strive for {a['contrastCustomColorTarget']}.", "", "**Control sizes**", "", "| Platform | Default | Minimum |", "|---|---|---|"]
    L += [f"| {PLATFORM_LABEL[p]} | {a['controlSize'][p]['default']}×{a['controlSize'][p]['default']} pt | {a['controlSize'][p]['minimum']}×{a['controlSize'][p]['minimum']} pt |" for p in PLATFORMS]
    L += ["", f"Padding around controls: about {a['controlPadding']['bezeled']} pt for bezeled elements, about {a['controlPadding']['nonBezeled']} pt for non-bezeled elements."]

    ly = t["layout"]
    tv = ly["tvos"]
    vis = ly["visionos"]
    L += ["", "## Layout specifications", "",
          "| Spec | Value |", "|---|---|",
          f"| tvOS safe area | {tv['safeArea']['top']} pt top/bottom · {tv['safeArea']['leading']} pt sides |",
          f"| tvOS grid spacing | {tv['grid']['horizontalSpacing']} pt horizontal · ≥ {tv['grid']['minimumVerticalSpacing']} pt vertical |",
          "| tvOS unfocused widths | " + " · ".join(f"{k}-col {v}" for k, v in tv['grid']['unfocusedContentWidth'].items()) + " pt |",
          f"| tvOS tab bar | {tv['tabBar']['height']} pt tall, top edge {tv['tabBar']['topInset']} pt from screen top |",
          f"| visionOS spacing | button centers ≥ {vis['minimumButtonCenterSpacing']} pt apart or ≥ {vis['minimumInteractiveMargin']} pt margin |",
          f"| visionOS default window | {vis['defaultWindow']['width']}×{vis['defaultWindow']['height']} pt |",
          f"| visionOS reading distance | ≥ {vis['comfortableReadingDistanceMeters']} m |",
          "| visionOS button sizes | " + " · ".join(f"{k} {v}" for k, v in vis['buttonSizes'].items()) + " pt |",
          f"| visionOS alert accessory | ≤ {vis['alertAccessoryView']['maxHeight']} pt tall, {vis['alertAccessoryView']['cornerRadius']} pt corner radius |",
          f"| watchOS buttons per row | ≤ {ly['watchos']['maxGlyphButtonsPerRow']} glyph or ≤ {ly['watchos']['maxTextButtonsPerRow']} text |",
          f"| watchOS action sheet | ≤ {ly['watchos']['maxActionSheetButtons']} buttons incl. Cancel |",
          f"| macOS menu bar height | {ly['macos']['menuBarHeight']} pt |",
          f"| macOS split view thin divider | {ly['macos']['splitViewThinDivider']} pt |",
          f"| iPhone segmented control | ≤ {ly['ios']['maxSegmentsIphone']} segments |",
          f"| Toolbar | title < {ly['toolbar']['maxTitleCharacters']} characters · ≤ {ly['toolbar']['maxGroups']} groups · ≤ {ly['toolbar']['maxProminentActions']} prominent action |",
          f"| Alert | ≤ {ly['alert']['maxButtons']} buttons · title ≤ {ly['alert']['maxTitleLines']} lines |",
          f"| Buttons | ≤ {ly['button']['maxProminentPerView']} prominent per view |",
          f"| Sidebar | ≤ {ly['sidebar']['maxHierarchyLevels']} hierarchy levels |",
          f"| Clear Liquid Glass over bright content | {int(t['materials']['clearGlassDimmingOpacity'] * 100)}% dark dimming layer |",
          f"| RTL beside uppercase Latin | Arabic/Hebrew about +{ly['rightToLeft']['rtlFontSizeIncreaseBesideUppercaseLatin']} pt |",
          f"| visionOS oscillation to avoid | ~{t['motion']['visionosAvoidOscillationHz']} Hz |",
          f"| Game frame rate | {t['motion']['gameFrameRate']['min']}–{t['motion']['gameFrameRate']['max']} fps |"]

    L += ["", "## App icons and images", "", "| Platform | Canvas | Layout shape | After masking | Notes |", "|---|---|---|---|---|"]
    for p, v in t["appIcon"].items():
        if p == "colorSpaces":
            continue
        notes = ", ".join(v.get("appearances", [])) or v.get("layers", "")
        L.append(f"| {PLATFORM_LABEL[p]} | {v['canvas']} | {v['shape']} | {v['masked']} | {notes} |")
    L += ["", "Icon color spaces: " + ", ".join(t["appIcon"]["colorSpaces"]) + ".", "", "| Platform | Image scale factors |", "|---|---|"]
    L += [f"| {PLATFORM_LABEL[p]} | {', '.join(v)} |" for p, v in t["imageScale"].items()]
    L += ["", "## Sources", ""] + [f"- [{k}]({v})" for k, v in m["sources"].items()] + [""]
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="fail if generated files are out of date")
    args = ap.parse_args()

    tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
    errors = validate(tokens)
    if errors:
        print(f"✗ {len(errors)} token error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    outputs = {CSS_OUT: render_css(tokens), MD_OUT: render_md(tokens)}
    if args.check:
        stale = [p.name for p, text in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
        if stale:
            print(f"✗ out of date: {', '.join(stale)} — run python3 scripts/build_tokens.py", file=sys.stderr)
            return 2
        print("✓ tokens valid; generated files up to date")
        return 0
    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")
    print(f"✓ tokens valid; wrote {CSS_OUT.relative_to(SKILL)} and {MD_OUT.relative_to(SKILL)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

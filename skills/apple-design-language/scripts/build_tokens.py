#!/usr/bin/env python3
"""Validate assets/tokens.json and generate the per-stack token files and references/design-tokens.md.

Part of the Apple Design Language skill — Created by Edison Augustin X.

tokens.json is the single source of truth for every value in this skill. Values come from
Apple's Human Interface Guidelines; this script keeps every rendering in sync:

    assets/tokens.css         CSS custom properties (HTML + CSS, React, Next.js, Vue, Svelte)
    assets/tokens.ts          typed values and CSS-variable references for JS/TS frameworks
    assets/tailwind.css       Tailwind CSS v4 theme mapped onto tokens.css
    assets/tokens.native.ts   React Native: PlatformColor on iOS, Dynamic Type ramps
    references/design-tokens.md

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
TS_OUT = SKILL / "assets" / "tokens.ts"
TAILWIND_OUT = SKILL / "assets" / "tailwind.css"
NATIVE_OUT = SKILL / "assets" / "tokens.native.ts"
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
    L.append("  --adl-background-grouped: var(--adl-system-gray6);      /* inset-grouped page */")
    L.append("  --adl-background-grouped-row: var(--adl-background);    /* rows on a grouped page */")
    L.append("  --adl-separator: var(--adl-system-gray4);")
    L.append("  /* Project values mixed from the tokens above (NOT Apple values): */")
    L.append("  --adl-secondary-label: color-mix(in srgb, CanvasText 62%, Canvas); /* ≥ 4.5:1 on background and grouped rows */")
    L.append("  --adl-fill: color-mix(in srgb, var(--adl-system-gray) 18%, transparent); /* control and field fills */")
    L.append("  --adl-on-accent: white;  /* label on --adl-accent-fill */")
    L.append("  /* Text and fill variants chosen so web text meets WCAG 2.2 AA (4.5:1), which is stricter than the")
    L.append("     HIG's 3:1 for bold text. They use HIG increased-contrast variants where the default fails. */")
    L.append(f"  --adl-accent-text: {sysc['blue']['lightIncreasedContrast']};      /* {contrast_ratio(sysc['blue']['lightIncreasedContrast'], '#FFFFFF'):.2f}:1 on white */")
    L.append(f"  --adl-destructive-text: {sysc['red']['lightIncreasedContrast']}; /* {contrast_ratio(sysc['red']['lightIncreasedContrast'], '#FFFFFF'):.2f}:1 on white */")
    L.append(f"  --adl-accent-fill: {sysc['blue']['lightIncreasedContrast']};      /* white label: {contrast_ratio('#FFFFFF', sysc['blue']['lightIncreasedContrast']):.2f}:1 in every appearance */")
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
    L.append("    --adl-background-grouped: var(--adl-background);")
    L.append("    --adl-background-grouped-row: var(--adl-system-gray6);")
    L.append(f"    --adl-accent-text: {sysc['blue']['dark']};")
    L.append(f"    --adl-destructive-text: {sysc['red']['dark']};")
    L.append("    --adl-glass-fill: rgb(30 30 30 / 0.6);")
    L.append("    --adl-glass-stroke: rgb(255 255 255 / 0.12);")
    L.append("  }")
    L.append("}")
    L.append("")
    L.append("/* Increase Contrast → HIG increased-contrast values (COL-02, COL-06) */")
    L.append("@media (prefers-contrast: more) {")
    L.append("  :root {")
    L += ["  " + line for line in color_block("lightIncreasedContrast")]
    L.append("    --adl-secondary-label: color-mix(in srgb, CanvasText 80%, Canvas);")
    L.append("    --adl-separator: var(--adl-system-gray);")
    L.append("  }")
    L.append("}")
    L.append("@media (prefers-contrast: more) and (prefers-color-scheme: dark) {")
    L.append("  :root {")
    L += ["  " + line for line in color_block("darkIncreasedContrast")]
    L.append(f"    --adl-accent-text: {sysc['blue']['darkIncreasedContrast']};")
    L.append(f"    --adl-destructive-text: {sysc['red']['darkIncreasedContrast']};")
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
    L.append("/* Hidden visually, still read by VoiceOver (labels for icon-only controls, A11Y-03) */")
    L.append(".adl-visually-hidden {")
    L.append("  position: absolute !important;")
    L.append("  width: 1px; height: 1px;")
    L.append("  margin: -1px; padding: 0; border: 0;")
    L.append("  overflow: hidden; clip-path: inset(50%); white-space: nowrap;")
    L.append("}")
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


# ---------------------------------------------------------------------------- JS / TS, Tailwind, React Native

# Semantic roles defined in tokens.css (web adaptation; see render_css).
SEMANTIC_ROLES = ["accent", "destructive", "background", "label", "secondaryLabel", "backgroundGrouped",
                  "backgroundGroupedRow", "separator", "fill", "onAccent", "accentText", "destructiveText", "accentFill"]
# React Native dynamicTypeRamp values (https://reactnative.dev/docs/text#dynamictyperamp-ios)
RN_RAMP = {
    "large-title": "largeTitle", "title1": "title1", "title2": "title2", "title3": "title3", "headline": "headline",
    "body": "body", "callout": "callout", "subheadline": "subheadline", "footnote": "footnote",
    "caption1": "caption1", "caption2": "caption2",
}
# UIKit UI element colors exposed through React Native PlatformColor (iOS only). Apple publishes no values for
# these, so other platforms fall back to published system grays, black, or white (project fallbacks, NOT Apple's
# values for the semantic colors). Each fallback: (UIKit name, light source, dark source).
RN_SEMANTIC = {
    "label": ("label", "#000000", "#FFFFFF"),
    "secondaryLabel": ("secondaryLabel", "gray.systemGray", "gray.systemGray"),
    "background": ("systemBackground", "#FFFFFF", "#000000"),
    "secondaryBackground": ("secondarySystemBackground", "gray.systemGray6", "gray.systemGray6"),
    "groupedBackground": ("systemGroupedBackground", "gray.systemGray6", "#000000"),
    "separator": ("separator", "gray.systemGray4", "gray.systemGray4"),
    "link": ("link", "system.blue", "system.blue"),
}


def camel(slug: str) -> str:
    return re.sub(r"-(\w)", lambda m: m.group(1).upper(), slug)


def generated_header(t: dict, comment: str, lines: list[str]) -> list[str]:
    head = [
        "Apple Design Language — " + lines[0],
        "Created by Edison Augustin X.",
        "",
        "GENERATED by skills/apple-design-language/scripts/build_tokens.py from assets/tokens.json.",
        f"Do not edit by hand. Values: {t['$meta']['verifiedAgainst']}.",
        *lines[1:],
    ]
    if comment == "//":
        return [("// " + x).rstrip() for x in head]
    return ["/*"] + [(" * " + x).rstrip() for x in head] + [" */"]


def ios_large(t: dict) -> dict:
    return {TEXT_STYLE_SLUG[s["style"]]: s for s in t["typography"]["textStyles"]["ios"]["sizes"]["Large (default)"]}


def render_ts(t: dict) -> str:
    sysc, gray = t["color"]["system"], t["color"]["gray"]
    names = list(sysc) + list(gray)
    L = generated_header(t, "//", [
        "tokens for JavaScript and TypeScript (React, Next.js, Vue, Svelte, plain JS)",
        "",
        "Import tokens.css once; then use `color`, `text`, … in inline styles or CSS-in-JS. They are CSS variable",
        "references, so light, dark, and Increase Contrast switch automatically (COL-01, COL-02, COL-07).",
        "Use `resolveSystemColor` only where CSS variables can't reach (canvas, WebGL, generated images).",
    ])
    L += ["", "export type ColorVariants = {", "  light: string;", "  dark: string;", "  lightIncreasedContrast: string;", "  darkIncreasedContrast: string;", "};", ""]
    L.append("export const systemColorNames = [" + ", ".join(f'"{n}"' for n in names) + "] as const;")
    L.append("export type SystemColorName = (typeof systemColorNames)[number];")
    L += ["", "/** HIG system color values: light, dark, and increased-contrast variants. */", "export const systemColors: Record<SystemColorName, ColorVariants> = {"]
    for k, v in {**sysc, **gray}.items():
        L.append(f'  {k}: {{ light: "{v["light"]}", dark: "{v["dark"]}", lightIncreasedContrast: "{v["lightIncreasedContrast"]}", darkIncreasedContrast: "{v["darkIncreasedContrast"]}" }},')
    L += ["};", ""]
    L.append("/** CSS variable references from tokens.css — they follow the system appearance and contrast settings. */")
    L.append("export const color = {")
    for n in names + SEMANTIC_ROLES:
        L.append(f'  {n}: "var({css_var(n)})",')
    L += ["} as const;", "export type ColorToken = keyof typeof color;", ""]
    L += ["/** System font stacks. Never bundle Apple system fonts (TYP-04). */", "export const font = {"]
    for n in ("text", "rounded", "serif", "mono"):
        L.append(f'  {n}: "var(--adl-font-{n})",')
    L += ["} as const;", ""]
    large = ios_large(t)
    L.append("/** iOS text styles at the Large (default) Dynamic Type size, as style objects (rem-based, so they scale). */")
    L.append("export const text = {")
    for slug in large:
        L.append(f'  {camel(slug)}: {{ fontSize: "var(--adl-text-{slug}-size)", lineHeight: "var(--adl-text-{slug}-line-height)", fontWeight: "var(--adl-text-{slug}-weight)" }},')
    L += ["} as const;", "export type TextStyle = keyof typeof text;", ""]
    L.append("/** The same text styles in points (1 CSS px ≈ 1 pt on Apple devices at default zoom). */")
    L.append("export const textStylePoints: Record<TextStyle, { size: number; leading: number; weight: number; emphasizedWeight: number }> = {")
    for slug, s in large.items():
        L.append(f"  {camel(slug)}: {{ size: {s['size']}, leading: {s['leading']}, weight: {WEIGHT[s['weight']]}, emphasizedWeight: {WEIGHT[s['emphasized']]} }},")
    L += ["};", ""]
    L.append("/** Default and minimum text sizes per platform, in points (TYP-02). */")
    L.append("export const textSize = {")
    for p, v in t["typography"]["platformSizes"].items():
        L.append(f"  {p}: {{ default: {v['default']}, minimum: {v['minimum']} }},")
    L += ["} as const;", ""]
    L.append("/** Hit targets per platform, in points (A11Y-01). Web default: 44 px everywhere. */")
    L.append("export const hitTarget = {")
    for p, v in t["accessibility"]["controlSize"].items():
        L.append(f"  {p}: {{ default: {v['default']}, minimum: {v['minimum']} }},")
    L += ["} as const;", ""]
    L += [
        "/** Layout variables from tokens.css. */",
        "export const layout = {",
        '  controlSize: "var(--adl-control-size)",',
        '  safeTop: "var(--adl-safe-top)",',
        '  safeRight: "var(--adl-safe-right)",',
        '  safeBottom: "var(--adl-safe-bottom)",',
        '  safeLeft: "var(--adl-safe-left)",',
        "} as const;",
        "",
        "/** Motion variables from tokens.css (1 ms under Reduce Motion — MOT-02). Project defaults, not Apple values. */",
        "export const motion = {",
        '  duration: "var(--adl-motion-duration)",',
        '  easing: "var(--adl-motion-easing)",',
        "} as const;",
        "",
        "/** Hex value of a system color for an appearance — for canvas, WebGL, and image generation only. */",
        "export function resolveSystemColor(",
        "  name: SystemColorName,",
        "  options: { dark?: boolean; increasedContrast?: boolean } = {},",
        "): string {",
        "  const c = systemColors[name];",
        "  if (options.increasedContrast) return options.dark ? c.darkIncreasedContrast : c.lightIncreasedContrast;",
        "  return options.dark ? c.dark : c.light;",
        "}",
        "",
    ]
    return "\n".join(L)


def render_tailwind(t: dict) -> str:
    sysc, gray = t["color"]["system"], t["color"]["gray"]
    L = generated_header(t, "/*", [
        "Tailwind CSS v4 theme",
        "",
        "Usage (Tailwind v4):   @import \"tailwindcss\";   @import \"./tailwind.css\";",
        "Keep tokens.css next to this file. Utilities such as bg-background, text-label, text-blue, text-body,",
        "font-rounded, and min-h-control read tokens.css variables, so they follow light, dark, and Increase",
        "Contrast automatically — no dark: or contrast-more: variants needed for these colors.",
        "`inline` is required because the theme variables reference other variables (tailwindcss.com/docs/theme).",
    ])
    L += ["", '@import "./tokens.css" layer(base);', "", "@theme inline {", "  /* System colors (HIG) and semantic roles */"]
    for n in list(sysc) + list(gray) + SEMANTIC_ROLES:
        L.append(f"  --color-{css_var(n)[6:]}: var({css_var(n)});")
    L += ["", "  /* System font stacks — never bundle Apple system fonts (TYP-04) */"]
    L.append("  --font-sans: var(--adl-font-text);")
    for n in ("rounded", "serif", "mono"):
        L.append(f"  --font-{n}: var(--adl-font-{n});")
    L += ["", "  /* iOS text styles, Large (default) Dynamic Type size */"]
    for slug in ios_large(t):
        L.append(f"  --text-{slug}: var(--adl-text-{slug}-size);")
        L.append(f"  --text-{slug}--line-height: var(--adl-text-{slug}-line-height);")
        L.append(f"  --text-{slug}--font-weight: var(--adl-text-{slug}-weight);")
    L += ["", "  /* Hit targets (A11Y-01): min-h-control, min-w-control, size-control */", "  --spacing-control: var(--adl-control-size);", "}", ""]
    return "\n".join(L)


def render_native(t: dict) -> str:
    sysc, gray = t["color"]["system"], t["color"]["gray"]
    names = list(sysc) + list(gray)
    L = generated_header(t, "//", [
        "tokens for React Native",
        "",
        "On iOS, colors are PlatformColor references to UIKit system colors: they adapt to light, dark, and",
        "Increase Contrast natively, like a SwiftUI or UIKit app (COL-01, COL-02). Elsewhere (Android, web) the",
        "system palette falls back to the HIG hex values for the current color scheme; semantic fallbacks are",
        "neutral project values, NOT Apple values. Text styles follow iOS Dynamic Type via dynamicTypeRamp.",
    ])
    L += ["", 'import { Platform, PlatformColor, useColorScheme, type ColorValue, type TextProps, type TextStyle } from "react-native";', ""]
    L.append("const palette = {")
    for k, v in {**sysc, **gray}.items():
        uikit = v["api"]["uikit"].split(".")[-1]
        L.append(f'  {k}: {{ ios: "{uikit}", light: "{v["light"]}", dark: "{v["dark"]}" }},')
    def fallback(src: str, variant: str) -> str:
        if src.startswith("#"):
            return src
        group, key = src.split(".")
        return t["color"][group][key][variant]

    for k, (ios, light, dark) in RN_SEMANTIC.items():
        L.append(f'  {k}: {{ ios: "{ios}", light: "{fallback(light, "light")}", dark: "{fallback(dark, "dark")}" }},')
    L += ["} as const;", "", "export type NativeColorName = keyof typeof palette;", ""]
    L += [
        "/** A system color: PlatformColor on iOS, the light or dark fallback elsewhere. */",
        "export function systemColor(name: NativeColorName, scheme: \"light\" | \"dark\" = \"light\"): ColorValue {",
        "  const c = palette[name];",
        "  return Platform.OS === \"ios\" ? PlatformColor(c.ios) : c[scheme];",
        "}",
        "",
        "/** Every system color for the current appearance. On iOS the values adapt natively without re-rendering. */",
        "export function useSystemColors(): Record<NativeColorName, ColorValue> {",
        "  const scheme = useColorScheme() === \"dark\" ? \"dark\" : \"light\";",
        "  const out = {} as Record<NativeColorName, ColorValue>;",
        "  for (const name of Object.keys(palette) as NativeColorName[]) out[name] = systemColor(name, scheme);",
        "  return out;",
        "}",
        "",
    ]
    large = ios_large(t)
    L.append("/** iOS text styles (Large default size). Keep allowFontScaling on (the default) so Dynamic Type applies (TYP-01). */")
    L.append("export const textStyles = {")
    for slug, s in large.items():
        L.append(f'  {camel(slug)}: {{ fontSize: {s["size"]}, lineHeight: {s["leading"]}, fontWeight: "{WEIGHT[s["weight"]]}" }},')
    L += ["} satisfies Record<string, TextStyle>;", "", "export type TextStyleName = keyof typeof textStyles;", ""]
    L.append("/** The matching iOS Dynamic Type ramp for each text style — pass it as <Text dynamicTypeRamp={…}>. */")
    L.append("export const dynamicTypeRamp = {")
    for slug in large:
        L.append(f'  {camel(slug)}: "{RN_RAMP[slug]}",')
    L += ['} as const satisfies Record<TextStyleName, NonNullable<TextProps["dynamicTypeRamp"]>>;', ""]
    ctl = t["accessibility"]["controlSize"]
    L += [
        f"/** Minimum hit target in points (A11Y-01): {ctl['ios']['default']} on iPhone and iPad; use hitSlop to reach it around small visuals. */",
        f"export const minimumHitTarget = {ctl['ios']['default']};",
        f"/** Minimum text size on iOS, in points (TYP-02). */",
        f"export const minimumTextSize = {t['typography']['platformSizes']['ios']['minimum']};",
        "",
    ]
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
        "Use the numbers for mockups, validation, and reviews. Code gets them generated: [`tokens.css`](../assets/tokens.css) (web), [`tokens.ts`](../assets/tokens.ts) (JavaScript/TypeScript), [`tailwind.css`](../assets/tailwind.css) (Tailwind v4), and [`tokens.native.ts`](../assets/tokens.native.ts) (React Native) — see [`stack-map.md`](stack-map.md).",
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

    outputs = {
        CSS_OUT: render_css(tokens),
        TS_OUT: render_ts(tokens),
        TAILWIND_OUT: render_tailwind(tokens),
        NATIVE_OUT: render_native(tokens),
        MD_OUT: render_md(tokens),
    }
    if args.check:
        stale = [p.name for p, text in outputs.items() if not p.exists() or p.read_text(encoding="utf-8") != text]
        if stale:
            print(f"✗ out of date: {', '.join(stale)} — run python3 scripts/build_tokens.py", file=sys.stderr)
            return 2
        print("✓ tokens valid; generated files up to date")
        return 0
    for path, text in outputs.items():
        path.write_text(text, encoding="utf-8")
    print("✓ tokens valid; wrote " + ", ".join(str(p.relative_to(SKILL)) for p in outputs))
    return 0


if __name__ == "__main__":
    sys.exit(main())

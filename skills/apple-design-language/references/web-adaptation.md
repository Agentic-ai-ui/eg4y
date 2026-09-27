# Web adaptation: web apps that feel at home on Apple devices

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> Tokens: [`../assets/tokens.css`](../assets/tokens.css) (generated from `tokens.json`) · Rules still apply: TYP-04, A11Y-01/03/04/05, MOT-02, COL-01/03/06, BRD-*

The HIG targets native apps. When the deliverable is a **website or web app** used on iPhone, iPad, Mac, or Vision Pro, apply the same principles — hierarchy, legibility, system typography, semantic color, accessibility, restraint — through web standards. Don’t imitate native chrome pixel-for-pixel (BRD-04); don’t claim a web page *is* Liquid Glass.

## Contents
1. [Principles for the web](#1-principles-for-the-web)
2. [Browser support (verified)](#2-browser-support-verified)
3. [Setup](#3-setup)
4. [Typography and Dynamic Type](#4-typography-and-dynamic-type)
5. [Color, appearance, contrast](#5-color-appearance-contrast)
6. [Layout, safe areas, touch targets](#6-layout-safe-areas-touch-targets)
7. [Glass-like surfaces (approximation)](#7-glass-like-surfaces-approximation)
8. [Motion](#8-motion)
9. [Accessibility checklist for web](#9-accessibility-checklist-for-web)
10. [What not to do](#10-what-not-to-do)

---

## 1. Principles for the web

| Native principle | Web translation |
|---|---|
| System font, Dynamic Type (TYP-01) | `-apple-system`/`system-ui` stack; `rem` sizing; WebKit `font: -apple-system-body` keywords |
| Never embed system fonts (TYP-04) | Reference system families by name; never `@font-face` SF Pro / New York files |
| Semantic colors adapt to appearance (COL-01, COL-07) | `color-scheme: light dark`, CSS system colors (`Canvas`, `CanvasText`), `prefers-color-scheme` |
| Increase Contrast (COL-06) | `prefers-contrast: more` → HIG increased-contrast values |
| Safe areas (LAY-02) | `viewport-fit=cover` + `env(safe-area-inset-*)` |
| 44 pt targets (A11Y-01) | ≥ 44 CSS px interactive areas (1 CSS px ≈ 1 pt on Apple devices at default zoom) |
| Reduce Motion (MOT-02) | `prefers-reduced-motion: reduce` |
| Controls float above content (LAY-08) | Translucent bars with `backdrop-filter`, opaque fallbacks |
| VoiceOver (A11Y-03) | Semantic HTML, accessible names, ARIA only when needed |

## 2. Browser support (verified)

Source: MDN browser-compat-data **8.1.3** (Safari = macOS, iOS = Safari on iOS/iPadOS).

| Feature | Safari | iOS Safari | Chrome | Firefox | Use |
|---|---|---|---|---|---|
| `prefers-color-scheme` | 12.1 | 13 | 76 | 67 | ✅ |
| `color-scheme` property | 13 | 13 | 81 | 96 | ✅ |
| `light-dark()` | 17.5 | 17.5 | 123 | 120 | Optional (media queries are broader) |
| `prefers-contrast` | 14.1 | 14.5 | 96 | 101 | ✅ |
| `prefers-reduced-motion` | 10.1 | 10.3 | 74 | 63 | ✅ |
| `prefers-reduced-transparency` | **No** | **No** | 118 | flag | ⚠️ Not a reliable fallback on Apple devices |
| `env()` safe areas | 11.1 | 11.3 | 69 | 65 | ✅ |
| `backdrop-filter` | 18 (prefixed `-webkit-` since 9) | 18 (prefixed since 9) | 76 | 103 | ✅ with `-webkit-` prefix too |
| `system-ui` | 11 | 11 | 56 | 92 | ✅ |
| `ui-rounded` / `ui-serif` / `ui-monospace` | 13.1 | 13.4 | No | No | ✅ with fallbacks |
| Dynamic viewport units (`dvh`) | 15.4 | 15.4 | 108 | 101 | ✅ |
| `:focus-visible` | 15.4 | 15.4 | 86 | 85 | ✅ |
| `forced-colors` | 16 | 16 | 89 | 89 | ✅ |
| `-webkit-text-size-adjust` | — | prefixed | 54 | No | Set to `100%` |

WebKit Dynamic Type font keywords (`font: -apple-system-body`, `-apple-system-headline`, `-apple-system-subheadline`, `-apple-system-caption1`, `-apple-system-caption2`, `-apple-system-footnote`, and short/tall variants) are documented by WebKit ([Using the System Font in Web Content](https://webkit.org/blog/3709/using-the-system-font-in-web-content/)); they are nonstandard and absent from MDN’s dataset. Other browsers ignore them, so always declare a fallback first.

## 3. Setup

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
<link rel="stylesheet" href="tokens.css">
```

- **Never** add `user-scalable=no` or `maximum-scale=1` — it blocks zoom (A11Y-05).
- `tokens.css` defines `--adl-*` variables, base styles, `.adl-text-*` text styles, `.adl-control`, `.adl-glass`, focus and motion handling. Tested in Chromium: colors switch for dark, increased contrast, and both combined; body text computes to 17 px / 22 px; controls to 44 px minimum.

## 4. Typography and Dynamic Type

```css
body { font-family: var(--adl-font-text); font-size: var(--adl-text-body-size); line-height: var(--adl-text-body-line-height); }

.article-body {
  font: 400 1.0625rem/1.375rem var(--adl-font-text);  /* fallback: iOS Body 17/22 pt */
  font: -apple-system-body;                            /* WebKit: follows the iOS text size setting */
}
```

- Size text in `rem` so browser and OS text settings scale it; never go below 11 px for iOS-targeted text (TYP-02).
- Use the `.adl-text-*` classes (Large Title … Caption 2) mapped from the HIG iOS Large (default) table.
- Weights: 400–700; avoid 100–300 for UI text (TYP-03).
- Serif/rounded/mono: `ui-serif`, `ui-rounded`, `ui-monospace` with fallbacks (Safari only).

## 5. Color, appearance, contrast

```css
:root { color-scheme: light dark; }                  /* native form controls and scrollbars follow appearance */
.card { background: var(--adl-background-grouped); color: var(--adl-label); }
.delete { color: var(--adl-destructive); }
@media (prefers-contrast: more) { .card { border: 1px solid CanvasText; } }
```

- `tokens.css` switches all 12 system colors and 6 grays between the HIG’s light, dark, and increased-contrast values automatically.
- Semantic web roles (`--adl-background` = `Canvas`, `--adl-label` = `CanvasText`) use CSS system colors. Apple doesn’t publish values for native semantic colors like `label` or `systemBackground`, so don’t hard-code guesses of them.
- **Check contrast** (computed in [`design-tokens.md`](design-tokens.md#contrast-of-system-colors)): in light mode, only indigo reaches 4.5:1 as text on white — blue is 3.52:1 and yellow 1.51:1. All increased-contrast variants reach ≥ 4.5:1, and every dark-mode value passes on black. For small text, use the label color or an increased-contrast variant; use vivid colors for fills, icons, and large or bold text (≥ 3:1) (COL-06, COL-03).

## 6. Layout, safe areas, touch targets

```css
.app-header { padding-top: max(12px, var(--adl-safe-top)); padding-inline: max(16px, var(--adl-safe-left)) max(16px, var(--adl-safe-right)); }
.tab-bar    { position: fixed; inset-inline: 0; bottom: 0; padding-bottom: var(--adl-safe-bottom); }
.screen     { min-height: 100dvh; }        /* dynamic viewport height tracks Safari’s collapsing toolbars */
button, a.button { min-width: var(--adl-control-size); min-height: var(--adl-control-size); }   /* 44px (A11Y-01) */
```

- Layout by container/viewport width (media or container queries), never user-agent sniffing (LAY-01).
- Keep the 44 px minimum on every device: iPads with trackpads report fine pointers too.
- Keep functionality identical at every width; collapse into menus rather than removing features (SYNC-01).

## 7. Glass-like surfaces (approximation)

Real Liquid Glass (refraction, specular highlights, adaptive tinting) is native-only. On the web, a translucent blurred bar is a reasonable *approximation* for floating navigation — keep it to bars and controls, never content (GLS-01).

```html
<nav class="adl-glass tab-bar" aria-label="Primary">…</nav>
```

- `.adl-glass` uses `rgb(… / 0.72)` fill + `backdrop-filter: blur(20px) saturate(180%)` — **project defaults, not Apple values**; tune and re-verify text contrast over your actual content.
- Opaque fallback under `prefers-contrast: more` (works in Safari) and `prefers-reduced-transparency: reduce` (not supported in Safari — so contrast mode is the only automatic fallback on Apple devices), and when `backdrop-filter` is unsupported.
- Consider offering an in-app “Reduce transparency” preference if translucency could hurt legibility — Safari doesn’t expose the system setting.

## 8. Motion

- Animate only to explain change; keep it brief; make it interruptible (MOT-01, MOT-04).
- Under `prefers-reduced-motion: reduce`, replace movement and zoom with short fades — don’t just delete all feedback (MOT-02). `tokens.css` sets `--adl-motion-duration: 1ms` and disables smooth scrolling in that mode; use the variable in your transitions.

```css
.sheet { transition: transform var(--adl-motion-duration) var(--adl-motion-easing), opacity var(--adl-motion-duration); }
@media (prefers-reduced-motion: reduce) { .sheet { transform: none !important; } }
```

## 9. Accessibility checklist for web

- [ ] Semantic elements (`<button>`, `<nav>`, `<main>`, headings in order); ARIA only to fill gaps.
- [ ] Every icon-only button has an accessible name (`aria-label` or visually hidden text) (A11Y-03).
- [ ] Meaningful images have `alt` text; decorative images `alt=""` (A11Y-04).
- [ ] No `user-scalable=no` / `maximum-scale=1`; text in `rem` (A11Y-05).
- [ ] Visible `:focus-visible` styles; logical tab order; no keyboard traps (A11Y-07).
- [ ] Contrast ≥ 4.5:1 body text, ≥ 3:1 large/bold, in light and dark (COL-06).
- [ ] Color never the only signal (COL-03).
- [ ] `prefers-reduced-motion` honored (MOT-02); no autoplaying media without controls (A11Y-10).
- [ ] Test with VoiceOver on iOS and macOS Safari, at 200% text/zoom, dark mode, and Increase Contrast.

## 10. What not to do

| Don’t | Why | Rule |
|---|---|---|
| `@font-face { font-family: "SF Pro"; src: url(SF-Pro.otf) }` | Apple system fonts must not be embedded/bundled | TYP-04 |
| Recreate iOS status bars, home indicators, or system alerts in HTML | Imitates system UI; confuses people | BRD-04 |
| Show Apple device frames or Apple logos as decoration | Trademark and hardware-replica restrictions | BRD-01, BRD-02 |
| Use SF Symbols artwork as your logo or app icon | SF Symbols license prohibits it | BRD-03 |
| Hard-code dark text on a custom dark background “because Safari” | Breaks appearance switching | COL-07 |
| Fixed `px` font sizes and disabled zoom | Blocks text enlargement | A11Y-05, TYP-01 |

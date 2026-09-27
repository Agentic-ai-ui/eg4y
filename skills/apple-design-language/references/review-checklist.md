# Design review checklist and report format

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> Rules: [`rules/README.md`](../../../rules/README.md) · Machine-readable: [`rules/rules.json`](../../../rules/rules.json) · Quick checklist: [`GUIDELINES.md` §19](../../../GUIDELINES.md#19-agent-review-checklist)

Use this to review a design, screenshot description, SwiftUI/UIKit/AppKit code, web UI (React, Next.js, Vue, Svelte, HTML/CSS, Tailwind), or React Native code against the Apple design language — your own work before presenting it, or someone else’s on request. The rules are the same on every stack; [`stack-map.md`](stack-map.md) shows how each is implemented.

## Contents
1. [Review procedure](#1-review-procedure)
2. [Full checklist by area](#2-full-checklist-by-area)
3. [Severity and prioritization](#3-severity-and-prioritization)
4. [Report template](#4-report-template)
5. [Example finding](#5-example-finding)

---

## 1. Review procedure

1. **Establish scope** — platforms, OS minimum, surface (SwiftUI/UIKit/AppKit/web), screens under review.
2. **Run the automated checker** when code is available. The hooks in `hooks/` flag the `Check: hook` rules (hard-coded colors, fixed font sizes, missing labels, small targets, Reduce Motion, embedded system fonts, and more). Fix or justify every finding (`hig-ignore: RULE-ID — reason`).
3. **Walk the checklist** below for the `review` rules — they need judgment.
4. **Test the states** — light/dark, Increase Contrast, Reduce Transparency, Reduce Motion, AX5 text, VoiceOver, RTL, compact/regular widths, every target platform.
5. **Report** using the template: errors first, then warnings, each with rule ID, location, why it matters, and a concrete fix.

## 2. Full checklist by area

**Structure and sync**
- [ ] Standard components used wherever one exists (SYS-01)
- [ ] Same features, terms, color meanings, symbols, toolbar groupings on every platform (SYNC-01 – SYNC-07)
- [ ] Platform-appropriate navigation container (NAV-06, SYNC-08)
- [ ] State restored on relaunch; multitasking-safe (SYS-04, SYS-05)

**Layout**
- [ ] Size classes and available space — no device/orientation checks (LAY-01)
- [ ] Safe areas and layout guides respected (LAY-02)
- [ ] Works at every size-class combination and window size (LAY-03)
- [ ] Layout adapts at AX sizes: stacks, rows grow, fewer columns (LAY-04)
- [ ] Clear hierarchy: importance order, alignment, grouping, progressive disclosure (LAY-05 – LAY-07)
- [ ] Platform specs: tvOS safe area/grid, visionOS 60 pt spacing, watchOS ≤ 3/2 buttons per row (LAY-13 – LAY-16)

**Liquid Glass and materials**
- [ ] Glass only on controls/navigation; none in content; no glass-on-glass (GLS-01, GLS-03, LAY-08)
- [ ] Custom glass rare and grouped in a container (GLS-02, GLS-08)
- [ ] No custom bar/sheet/popover backgrounds (GLS-04)
- [ ] Regular vs clear variant correct; dimming over bright media (GLS-05)
- [ ] Only the primary action tinted (GLS-09)
- [ ] Verified with Reduce Transparency, Increase Contrast, Reduce Motion (GLS-06)

**Color and appearance**
- [ ] System/semantic colors via API or asset Color Sets; no literals (COL-01, COL-02)
- [ ] Color never the only signal; one meaning per color (COL-03, COL-04)
- [ ] Contrast ≥ 4.5:1 / 3:1 in both appearances (COL-06)
- [ ] Follows system appearance; no forced scheme (COL-07)
- [ ] Accent reserved for primary actions, status, selection (COL-09)

**Typography**
- [ ] Text styles with Dynamic Type; custom fonts scale and support Bold Text (TYP-01, TYP-05)
- [ ] Nothing below the platform minimum; no light weights (TYP-02, TYP-03)
- [ ] No embedded system fonts (TYP-04)
- [ ] Minimal truncation; hierarchy preserved at large sizes (TYP-07, TYP-08)

**Icons and images**
- [ ] SF Symbols; standard symbols for standard actions (ICN-01, ICN-02)
- [ ] Consistent icon weight/size; vectors for custom icons (ICN-03, ICN-04)
- [ ] App icon: unmasked layers, consistent across appearances and platforms, simple (ICN-09 – ICN-12, SYNC-04)

**Interaction and components**
- [ ] Hit targets ≥ platform default (A11Y-01)
- [ ] ≤ 2 prominent buttons; style not size for preference; press states; no destructive primary (CMP-01 – CMP-04)
- [ ] Tab bar navigation-only, visible, never disabled; ≤ 5 tabs by default (NAV-01 – NAV-04)
- [ ] Standard Back/Close; short titles; one trailing prominent toolbar action; ≤ 3 groups (NAV-09 – NAV-12)
- [ ] Modality justified; one at a time; obvious dismissal; Done + Cancel (CMP-06 – CMP-10)
- [ ] Alerts rare, specific, ≤ 3 buttons, verb labels, “Cancel” (CMP-11 – CMP-14)
- [ ] Action sheets for intentional-action choices; popovers not in compact width (CMP-15, CMP-16)
- [ ] Menus and context menus organized; context items also in main UI (CMP-17, CMP-18)
- [ ] Inputs: secure fields, right keyboard, switches only in list rows, segment limits (CMP-21 – CMP-26)
- [ ] Gestures have on-screen alternatives; no system-gesture conflicts; standard shortcuts intact (A11Y-06, INP-01 – INP-06)

**Motion and haptics**
- [ ] Purposeful, brief, interruptible motion; Reduce Motion honored (MOT-01 – MOT-05)
- [ ] Haptics match documented meanings and visuals (HAP-01, HAP-02)

**Accessibility**
- [ ] Labels for every control; images described or hidden (A11Y-03, A11Y-04)
- [ ] Headings, grouping, order, announcements (A11Y-08)
- [ ] No timed UI; media controllable; captions (A11Y-09 – A11Y-11)
- [ ] Accessibility Inspector clean; VoiceOver and Full Keyboard Access pass (A11Y-07, A11Y-13)

**Writing and localization**
- [ ] Verb labels, descriptive links, correct gesture words, consistent capitalization, ellipses (WRT-01 – WRT-05)
- [ ] No “we”; helpful errors; empty states with a next step (WRT-06 – WRT-08)
- [ ] Strings externalized; RTL mirroring correct; no text in images (L10N-01 – L10N-05)

**Patterns, privacy, AI**
- [ ] Launch screen ≈ first screen, no branding; onboarding optional (PAT-01, PAT-02)
- [ ] Permissions in context; specific purpose strings; honest pre-alert screens (PRV-01 – PRV-04)
- [ ] AI disclosed, controllable, confirmed before significant actions (AI-01 – AI-06)

**Platform specifics** — apply the matching `PLT-*` rules ([`platforms.md`](platforms.md)).

**Web stacks (React, Next.js, Vue, Svelte, HTML/CSS, Tailwind)** — [`web-adaptation.md`](web-adaptation.md)
- [ ] Viewport has `viewport-fit=cover` and no `maximum-scale` / `user-scalable=no`; `color-scheme: light dark` (LAY-02, A11Y-05, COL-07)
- [ ] Colors come from `tokens.css` / `tokens.ts` / the Tailwind theme — no hex literals; colored text sits on the page background or a list row (COL-01, COL-06)
- [ ] One navigation list rendered as tab bar ⇄ sidebar by available width; links with `aria-current="page"` (NAV-01, NAV-06, LAY-01)
- [ ] Native elements first: `<button>`, `<a>`, `<dialog>`, `popover`, radios, `role="switch"` checkboxes (A11Y-03, A11Y-07)
- [ ] Icon-only controls have `aria-label`; icons are open-licensed, never SF Symbols (A11Y-03, BRD-03)
- [ ] axe-core clean (WCAG 2.2 AA) in light, dark, Increase Contrast; Reduce Motion honored (COL-06, MOT-02)

**React Native** — [`react-native.md`](react-native.md)
- [ ] `PlatformColor` / `DynamicColorIOS` (via `tokens.native.ts`), no hex in components (COL-01, COL-02)
- [ ] Text scales: `allowFontScaling` left on, `dynamicTypeRamp` set, no tight `maxFontSizeMultiplier` (TYP-01, A11Y-05)
- [ ] Native tabs, stacks, `Switch`, `Alert`, `ActionSheetIOS` instead of JavaScript look-alikes (SYS-01, BRD-04)
- [ ] `accessibilityLabel` and `role` on custom pressables; 44 pt targets with `hitSlop` where needed (A11Y-01, A11Y-03)
- [ ] Reduce Motion read from `AccessibilityInfo`; glass only on floating controls (MOT-02, GLS-01)

**Brand and legal**
- [ ] No Apple trademarks, hardware replicas, SF Symbols in logos/icons, or imitated system UI (BRD-01 – BRD-04)

## 3. Severity and prioritization

| Severity | Level | Handling |
|---|---|---|
| **error** | MUST / MUST NOT | Blocks shipping. Fix before presenting. |
| **warning** | SHOULD / SHOULD NOT | Fix by default; keep only with an explicit reason naming a design principle (SYS-06). |
| **info** | MAY | Suggestion. |

Order findings: errors → warnings → info; within a severity, accessibility and data-loss issues first, then cross-platform consistency, then polish.

## 4. Report template

```markdown
## Apple design review — <screen or feature>

**Scope:** <platforms> · <OS minimum> · <SwiftUI | UIKit | AppKit | Web>
**Result:** <N> errors · <N> warnings · <N> info — <Ready | Needs changes>

### Errors
| # | Rule | Location | Finding | Fix |
|---|---|---|---|---|
| 1 | A11Y-03 | `TripRow.swift:42` | Icon-only “star” button has no accessibility label | `Button("Add to Favorites", systemImage: "star")` + `.labelStyle(.iconOnly)` |

### Warnings
| # | Rule | Location | Finding | Fix |
|---|---|---|---|---|

### Kept deviations
| Rule | Location | Reason (principle) |
|---|---|---|

### Tested states
- [x] Light · [x] Dark · [ ] Increase Contrast · [ ] Reduce Transparency · [ ] Reduce Motion · [ ] AX5 · [ ] VoiceOver · [ ] RTL · [ ] compact · [ ] regular
```

## 5. Example finding

> **COL-07 (error)** · `RootView.swift:12` — `.preferredColorScheme(.light)` forces light mode for the whole app. People who choose Dark Mode system-wide expect every app to follow it, and the system’s base/elevated backgrounds, glass adaptation, and increased-contrast colors depend on it. **Fix:** remove the modifier and make sure custom colors are asset-catalog Color Sets with dark and increased-contrast variants (COL-02). If this is a full-screen media viewer that should stay dark, scope the modifier to that view and annotate it: `// hig-ignore: COL-07 — immersive video player stays dark`.

---
name: apple-design-language
description: Design and build app interfaces that feel native across the Apple ecosystem — iPhone, iPad, iPhone Duo, Mac, Apple TV, Apple Vision Pro, and Apple Watch — following Apple's Human Interface Guidelines and Liquid Glass. Use this skill whenever the task involves designing, building, reviewing, or refactoring UI for iOS, iPadOS, macOS, tvOS, visionOS, or watchOS (SwiftUI, UIKit, AppKit), or a web app meant to feel at home on Apple devices; when choosing navigation (tab bar, sidebar, split view, toolbar), colors, typography, SF Symbols, app icons, motion, haptics, or accessibility for Apple platforms; when adapting one app across several Apple devices; or when the user says "Apple style", "HIG", "native iOS look", "Liquid Glass", "make it feel like an Apple app", even if they don't name the guidelines. Not for cloning Apple's devices, apps, logos, or branding.
---

# Apple Design Language

> Created by Edison Augustin X. · Researched against Apple’s Human Interface Guidelines and Developer Documentation (current through September 2026).

This skill helps you design apps **for** the Apple ecosystem — so they feel at home on every Apple device and stay consistent across them. It is not for reproducing Apple’s hardware, Apple’s own apps, logos, or branding; those are off-limits (see the brand rules below).

The package has three layers. Use them in this order when something is unclear:

| Layer | What it gives you | Where |
|---|---|---|
| **Guidelines** | What the design language is and why (the full narrative, with Apple sources) | [`../../GUIDELINES.md`](../../GUIDELINES.md) |
| **Rules** | 239 enforceable rules with IDs (e.g., `COL-01`), levels, and platforms | [`../../rules/`](../../rules/README.md), [`rules.json`](../../rules/rules.json) |
| **This skill** | Workflow, decision guides, specs, code recipes, tokens | `references/`, `assets/`, `scripts/` |

## Workflow

Follow these steps for any design or UI-building task. They’re ordered so that structural decisions (which are expensive to change) come before visual polish.

### 1. Frame the task
Identify the **target platforms**, the **surface** (SwiftUI preferred; UIKit, AppKit, or web), and the **minimum OS**. Liquid Glass APIs need the 26 SDKs; guard with `if #available` for earlier releases. If platforms aren’t stated, ask — or assume iPhone + iPad and say so. Read [`references/platforms.md`](references/platforms.md) whenever more than one device is involved.

### 2. Map one information architecture onto each platform
List the top-level sections, objects, and actions once. Then pick each platform’s navigation container — floating tab bar (iPhone), tab bar ⇄ sidebar (iPad), sidebar + menu bar (Mac), top tab bar + focus (tvOS), vertical tab bar in a glass window (visionOS), list/pages (watchOS). Features, terms, symbols, and color meanings stay identical everywhere (SYNC-01 – SYNC-07); only the container and density adapt. See [`references/navigation.md`](references/navigation.md).

### 3. Build with system components first
Standard components give you Liquid Glass, Dark Mode, Dynamic Type, accessibility, and right-to-left behavior for free; custom UI has to re-create all of it. Reach for a standard component, then customize, and only then build from scratch (SYS-01). Use [`references/components.md`](references/components.md) to choose the right component and [`references/swiftui-recipes.md`](references/swiftui-recipes.md) for idiomatic code.

### 4. Apply the visual system
- **Layers:** content on system backgrounds/standard materials; controls and navigation in the Liquid Glass layer — [`references/liquid-glass.md`](references/liquid-glass.md).
- **Color & type:** semantic system colors and text styles via APIs; exact values live in [`references/design-tokens.md`](references/design-tokens.md) for mockups, validation, and web.
- **Words:** labels, alerts, errors, empty states, purpose strings — [`references/writing.md`](references/writing.md).
- **Web deliverables:** [`references/web-adaptation.md`](references/web-adaptation.md) + [`assets/tokens.css`](assets/tokens.css).

### 5. Make it accessible while you build
Hit targets, labels, Dynamic Type, contrast, Reduce Motion — build them in, don’t bolt them on. [`references/accessibility.md`](references/accessibility.md) maps every requirement to SwiftUI, UIKit, AppKit, and web APIs.

### 6. Review before presenting
Run the automated checker if the repository has one (`python3 hooks/scripts/hig_lint.py <files>` in this package), then walk [`references/review-checklist.md`](references/review-checklist.md). Fix every error. Keep a warning only with a stated reason that names a design principle (SYS-06), or annotate the code: `// hig-ignore: RULE-ID — reason`.

### 7. Explain your decisions
When you present work, cite rule IDs for non-obvious choices and list any deviations with their reasons. For reviews, use the report template in the checklist reference.

## Non-negotiables (errors)

These come up constantly. Each is a MUST/MUST NOT rule; details and sources are in `rules/`.

| Area | Rule | ID |
|---|---|---|
| Layout | Decide layout from size classes and available space, never device type or orientation; respect safe areas | LAY-01, LAY-02 |
| Glass | Controls/navigation in Liquid Glass; **no glass in the content layer**; no glass-on-glass | LAY-08, GLS-01, GLS-03 |
| Color | Use system colors through APIs; never color alone; follow the system appearance; meet 4.5:1 / 3:1 contrast | COL-01, COL-03, COL-07, COL-06 |
| Type | Text styles with Dynamic Type; never below the platform minimum (iOS 11 pt, macOS 10 pt, tvOS 23 pt, visionOS/watchOS 12 pt); never embed system fonts | TYP-01, TYP-02, TYP-04 |
| Targets | ≥ 44×44 pt (iOS, iPadOS, watchOS), 60×60 pt (visionOS), 28×28 pt (macOS), 66×66 pt (tvOS) | A11Y-01 |
| Labels | Every control — especially icon-only — has an accessibility label | A11Y-03 |
| Motion | Honor Reduce Motion; motion never the only channel | MOT-02, MOT-03 |
| Navigation | Tab bars navigate, never act; never disable tabs; one prominent toolbar action, trailing | NAV-01, NAV-03, NAV-11 |
| Modality | One modal at a time; always an obvious dismissal; ≤ 3 alert buttons with specific titles | CMP-07, CMP-08, CMP-12 |
| Safety | Secure fields for passwords; never mislead around permission prompts; never impersonate humans with AI | CMP-21, PRV-03, PRV-04, AI-01 |
| Sync | Functionality identical across platforms and sizes | SYNC-01 |
| Mac | Every command in the menu bar; every toolbar item also a menu command | PLT-MAC-01, PLT-MAC-02 |
| Brand | No Apple trademarks, hardware replicas, SF Symbols in logos/icons, or imitated system UI | BRD-01 – BRD-04 |

## Reference guide

Read only what the task needs:

| Read | When |
|---|---|
| [`references/platforms.md`](references/platforms.md) | Any multi-device task; platform metrics; mapping one IA to every platform |
| [`references/navigation.md`](references/navigation.md) | Tab bars, sidebars, split views, toolbars, search, sheets |
| [`references/components.md`](references/components.md) | Choosing a component; buttons, alerts, menus, lists, inputs, progress, UX patterns |
| [`references/liquid-glass.md`](references/liquid-glass.md) | Anything about glass, materials, scroll edge effects, custom glass APIs |
| [`references/design-tokens.md`](references/design-tokens.md) | Exact colors (with computed contrast), full Dynamic Type tables, control sizes, layout specs, icon specs |
| [`references/accessibility.md`](references/accessibility.md) | Implementing or testing accessibility on any surface |
| [`references/writing.md`](references/writing.md) | Any user-facing text: labels, alerts, errors, empty states, permissions |
| [`references/swiftui-recipes.md`](references/swiftui-recipes.md) | Writing SwiftUI; anti-pattern → fix table |
| [`references/web-adaptation.md`](references/web-adaptation.md) | Web apps for Apple devices; verified browser support |
| [`references/review-checklist.md`](references/review-checklist.md) | Reviewing work; report format |

## Assets and scripts

| File | Purpose |
|---|---|
| [`assets/tokens.json`](assets/tokens.json) | Single source of truth for every value in this skill (HIG-derived) |
| [`assets/tokens.css`](assets/tokens.css) | Generated web tokens: colors with dark and increased-contrast variants, text styles, targets, safe areas, glass approximation, motion |
| [`scripts/build_tokens.py`](scripts/build_tokens.py) | Validates `tokens.json`; regenerates `tokens.css` and `references/design-tokens.md` (`--check` for CI) |

## Keep in mind

- **Apple’s documentation wins.** Values here are verified references, but Apple revises them between releases; native code must use system APIs rather than the numbers. If something looks outdated, check the linked HIG page and update `GUIDELINES.md` first, then `rules/`, then this skill.
- **SwiftUI snippets were checked against Apple’s API declarations, not compiled here** — build with the current Xcode.
- **Design for everyone and every device.** When a trade-off is unclear, choose the option that keeps the app accessible, consistent across platforms, and familiar to people who already use Apple devices.

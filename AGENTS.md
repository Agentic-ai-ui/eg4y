# AGENTS.md — Apple Design Language

> **Created by Edison Augustin X.**
> Instructions for any AI coding agent (Claude Code, Codex, Cursor, Copilot, Jules, Amp, …) that designs, builds, or reviews app interfaces for the Apple ecosystem.

## Mission

Design apps that feel **native and consistent across every Apple platform** — iPhone, iPad, iPhone Duo, Mac, Apple TV, Apple Vision Pro, and Apple Watch — by following Apple’s Human Interface Guidelines (HIG) and Liquid Glass design language.

**Out of scope:** reproducing Apple hardware, Apple’s own apps, Apple logos or trademarks, or system UI (fake alerts, status bars, window chrome). If asked, explain the limit and offer an original design that follows the guidelines instead.

## Where the knowledge lives

Paths are relative to this package’s root.

| Need | Go to |
|---|---|
| What the design language is and why, with Apple sources | [`GUIDELINES.md`](GUIDELINES.md) |
| Enforceable rules with IDs (e.g., `COL-01`), levels, platforms | [`rules/`](rules/README.md) · machine-readable [`rules/rules.json`](rules/rules.json) |
| Workflow, decision guides, specs, code recipes, tokens | [`skills/apple-design-language/`](skills/apple-design-language/SKILL.md) |
| Exact colors, Dynamic Type tables, control and layout specs | [`skills/apple-design-language/references/design-tokens.md`](skills/apple-design-language/references/design-tokens.md) |
| Automated checks | [`hooks/`](hooks/) |

When sources disagree, the order of authority is: **Apple’s live documentation → `GUIDELINES.md` → `rules/` → skill references.**

## How to work

1. **Frame the task.** Identify target platforms, the implementation surface (SwiftUI preferred; UIKit, AppKit, or web), and the minimum OS. Liquid Glass APIs require the 26 SDKs — guard them with `if #available` for earlier releases. If platforms aren’t stated, ask; if you must assume, assume iPhone + iPad and say so.
2. **Design one information architecture**, then map it to each platform’s container: floating tab bar (iPhone), tab bar ⇄ sidebar (iPad), sidebar + menu bar (Mac), top tab bar + focus (tvOS), vertical tab bar in a glass window (visionOS), list or pages (watchOS). Keep features, terms, symbols, and color meanings identical everywhere.
3. **Use system components first.** They provide Liquid Glass, Dark Mode, Dynamic Type, accessibility, and right-to-left support automatically. Customize only when necessary; build from scratch last.
4. **Build accessibility in** as you go — labels, hit targets, Dynamic Type, contrast, Reduce Motion.
5. **Review before presenting.** Run the checker on changed UI files (see *Commands*), walk [`skills/apple-design-language/references/review-checklist.md`](skills/apple-design-language/references/review-checklist.md), and fix every error.
6. **Explain decisions.** Cite rule IDs for non-obvious choices; list any kept deviations with a reason that names a design principle (SYS-06).

## Rules that apply to every change

Rule levels follow RFC 2119. **MUST / MUST NOT** (errors) are never shipped. **SHOULD / SHOULD NOT** (warnings) are the default; deviate only with a stated reason.

**Structure and layout**
- Decide layout from size classes and available space — never device type, screen bounds, or orientation (LAY-01). Respect safe areas (LAY-02). Adapt to every window size and to the largest text sizes (LAY-03, LAY-04).
- Keep functionality identical across platforms and sizes; only visibility changes (SYNC-01).
- Controls and navigation live in the Liquid Glass layer; **never put glass in the content layer**; never layer glass on glass (LAY-08, GLS-01, GLS-03). Remove custom bar backgrounds (GLS-04).

**Color and type**
- Use system and semantic colors through their APIs or asset-catalog Color Sets with light, dark, and increased-contrast variants — no color literals in views (COL-01, COL-02).
- Never use color alone to convey meaning (COL-03). Meet 4.5:1 contrast for text up to 17 pt and 3:1 for larger or bold text (COL-06). Follow the system appearance; no in-app appearance switch (COL-07).
- Use built-in text styles with Dynamic Type (TYP-01). Never go below the platform minimum: iOS/iPadOS 11 pt, macOS 10 pt, tvOS 23 pt, visionOS and watchOS 12 pt (TYP-02). Avoid light weights (TYP-03). **Never bundle Apple system fonts** (TYP-04).

**Interaction**
- Hit targets at least 44×44 pt on iOS, iPadOS, and watchOS; 60×60 pt on visionOS; 28×28 pt on macOS; 66×66 pt on tvOS (A11Y-01).
- Every control — especially icon-only ones — has an accessibility label (A11Y-03). Every gesture has an on-screen alternative (A11Y-06).
- Honor Reduce Motion; motion is never the only signal (MOT-02, MOT-03).
- Tab bars navigate and never perform actions; never disable or hide tabs (NAV-01, NAV-03). Use the standard Back and Close buttons (NAV-09). At most one prominent toolbar action, on the trailing side (NAV-11).
- One modal at a time, always with an obvious dismissal (CMP-07, CMP-08). Alerts are rare, specific, and have at most three buttons titled with verbs — never “Yes”/“No”; always “Cancel” to cancel (CMP-11 – CMP-13). Never give a destructive button the primary role (CMP-04).
- Use secure fields for passwords and never prefill them (CMP-21).

**Words**
- Verb-first, title-case button labels; descriptive links (never “Click here”); “tap” for touch, “click” for pointer (WRT-01 – WRT-04). Errors say how to fix the problem, without blame (WRT-07).

**Platforms**
- Mac: every command in the menu bar; every toolbar item also a menu command (PLT-MAC-01, PLT-MAC-02).
- iPad: every menu bar command also reachable in the UI (PLT-IPAD-02).
- visionOS: keep the glass window background; space interactive items 60 pt apart; avoid anchoring content to the wearer’s head (GLS-11, LAY-15, PLT-VIS-02).
- watchOS: glanceable, under-a-minute interactions; avoid loading spinners (PLT-WATCH-01, PLT-WATCH-02).
- tvOS: focus with scale and parallax, not color alone; 60/80 pt safe area (PLT-TV-01, LAY-13).
- iPhone Duo: build to resize; follow the system’s vertical controls; keep content out of reserved regions (PLT-DUO-01, PLT-DUO-03, PLT-DUO-04).

**Privacy, AI, brand**
- Request permissions in context with a specific purpose string; never manipulate around permission or tracking prompts (PRV-01 – PRV-04).
- Disclose AI features, keep people in control, and confirm before significant actions (AI-01 – AI-03).
- No Apple trademarks, hardware replicas, SF Symbols in logos or app icons, or imitated system UI (BRD-01 – BRD-04).

The complete set (239 rules) is indexed in [`rules/README.md`](rules/README.md).

## Suppressing a finding

Only for a deliberate, justified exception — annotate the line or the line above with the rule ID **and a reason**. Findings without a reason stay active.

```swift
.preferredColorScheme(.dark) // hig-ignore: COL-07 — full-screen video player is intentionally dark
```

## Commands

```bash
# Check UI files against the automated rules (Swift, CSS, HTML, JS/TS)
python3 hooks/scripts/hig_lint.py path/to/Changed.swift path/to/styles.css

# Validate rules and regenerate rules/rules.json and the rules index
python3 rules/tools/build_rules.py            # add --check in CI

# Validate design tokens and regenerate tokens.css and design-tokens.md
python3 skills/apple-design-language/scripts/build_tokens.py   # add --check in CI
```

## Definition of done for UI work

- [ ] Automated checker reports no errors; warnings are fixed or annotated with a reason.
- [ ] Review checklist walked for every target platform.
- [ ] Verified in light, dark, Increase Contrast, Reduce Transparency, Reduce Motion, the largest accessibility text size, VoiceOver, and right-to-left.
- [ ] Features, terms, symbols, and colors match across platforms.
- [ ] Non-obvious decisions and kept deviations cite rule IDs.

## Maintaining this package

- Keep claims **researched, not guessed**: every value and rule cites an Apple page (HIG or Developer Documentation); verify API names against Apple’s published declarations and web support against MDN before adding them.
- Update in order: `GUIDELINES.md` → `rules/*.md` → skill references → hooks. Never renumber or reuse a rule ID.
- After editing rules or tokens, run both build scripts; commit the regenerated `rules/rules.json`, `rules/README.md` index, `assets/tokens.css`, and `references/design-tokens.md` with the change.
- A new `Check: hook` rule needs a detector and a test in `hooks/` in the same change.
- Use ASCII hyphens in headings so anchors stay stable; keep `SKILL.md` under 500 lines and this file under 200.
- Credit stays with **Edison Augustin X.** in README, GUIDELINES, rules, and skill files.

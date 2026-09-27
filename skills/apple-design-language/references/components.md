# Components: choosing and specifying

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> Source of truth: [`GUIDELINES.md` §13–§14](../../../GUIDELINES.md#13-components) · Rules: [`rules/11-components.md`](../../../rules/11-components.md), [`rules/12-patterns.md`](../../../rules/12-patterns.md)

Use this when deciding **which** component fits a need and **how** to configure it. Navigation containers are in [`navigation.md`](navigation.md); code in [`swiftui-recipes.md`](swiftui-recipes.md).

## Contents
1. [Which component?](#1-which-component)
2. [Buttons](#2-buttons)
3. [Communicating with people: alerts, action sheets, sheets, popovers, feedback](#3-communicating-with-people)
4. [Menus and context menus](#4-menus-and-context-menus)
5. [Lists, tables, collections, scroll views](#5-lists-tables-collections-scroll-views)
6. [Input controls](#6-input-controls)
7. [Status and progress](#7-status-and-progress)
8. [Experience patterns](#8-experience-patterns)

---

## 1. Which component?

| I need to… | Use | Not | Rules |
|---|---|---|---|
| Switch between top-level sections | Tab bar / sidebar | Segmented control | NAV-01, CMP-24 |
| Switch between closely related subviews of one screen | Segmented control (≤ 5 on iPhone) | Tab bar | CMP-24 |
| Perform an action on the current view | Toolbar button | Tab bar item | NAV-01 |
| Offer choices about an action someone just initiated | Action sheet (`confirmationDialog`) | Alert, menu | CMP-15 |
| Tell people something critical they must act on | Alert (≤ 3 buttons) | Popover, toast | CMP-11, CMP-12 |
| Report status that doesn’t need action | Inline status/label in context | Alert | PAT-04, CMP-11 |
| Run a scoped task related to the current context | Sheet | Push inside a modal hierarchy | CMP-06 |
| Show a little functionality in wide layouts | Popover | Popover in compact width | CMP-16 |
| Show item-specific actions | Context menu (+ same actions in main UI) | Context menu only | CMP-18 |
| Pick one from a short list | Pull-down / pop-up button, menu | Picker wheel | CMP-25 |
| Pick from a medium-to-long list | Picker | Segmented control | CMP-25 |
| Pick from a very long list | List/table (+ index) | Picker | CMP-25 |
| Turn a setting on/off (iOS list) | Switch in a list row | Switch floating in layout | CMP-23 |
| Turn a mode on/off outside lists (iOS) | Toggle-style button | Switch | CMP-23 |
| Choose among 2–5 exclusive options (macOS) | Radio buttons | Many checkboxes | CMP-23 |
| Enter a small amount of text | Text field (+ label, hint, keyboard type) | Text view | CMP-22, WRT-11 |
| Enter a password | Secure field | Text field | CMP-21 |
| Adjust a continuous value | Slider (+ optional field/stepper) | Slider for iOS volume | CMP-26 |
| Show an empty section | `ContentUnavailableView` with a next step | Disabled tab, blank screen | WRT-08, NAV-03 |
| Show loading | Placeholder content → determinate progress | Blank screen, vague “Loading…” | PAT-03, CMP-27 |

## 2. Buttons

| Spec | Value | Rule |
|---|---|---|
| Hit region | ≥ 44×44 pt (visionOS 60×60, macOS 28×28, tvOS 66×66) | A11Y-01 |
| Prominent buttons | ≤ 1–2 per view, for the most likely action | CMP-01 |
| Preferred option | Distinguish by style, keep sizes equal | CMP-02 |
| Custom button | Must show a press state | CMP-03 |
| Primary role | Never on a destructive action | CMP-04 |
| Roles | primary (accent, Return), cancel (Escape), destructive (red) | CMP-05 |
| Label | Verb-first, title case (“Add to Cart”); familiar symbol for familiar action | WRT-01, ICN-02 |
| Opens more input | Trailing ellipsis (“Export As…”) | WRT-05 |
| Pending action (iOS) | Activity indicator inside the button with an updated label (“Checking out…”) | — |

SwiftUI styles: `.glass`, `.glassProminent` (26+), `.bordered`, `.borderedProminent`, `.borderless`, `.plain`; sizes via `.controlSize(_:)`; shape via `.buttonBorderShape(_:)`.

Platform shapes: visionOS icon-only → circle, text → capsule or rounded rectangle, icon+text → capsule; watchOS inline buttons are capsules and primary buttons span the width.

## 3. Communicating with people

**Alert** (CMP-11 – CMP-14)

```
Title:    Specific situation, ≤ 2 lines. Fragment → Title Case, no period. Sentence → sentence case + period.
Message:  Optional. Short, complete sentences. Only if it adds value.
Buttons:  ≤ 3. Verbs describing the result (“Delete”, “Keep Editing”).
          “OK” only for purely informational alerts. Never “Yes”/“No”. Always “Cancel” to cancel.
          Default button trailing (or top of stack); Cancel leading (or bottom); Cancel never default.
          Destructive style only for destructive actions people didn’t deliberately choose.
```

Don’t alert: at launch, for information only, for common undoable actions (delete email), with a scrolling message.

**Action sheet / confirmation dialog** (CMP-15): for choices about an intentional action (e.g., discard vs save draft). Short one-line title, message only if needed, destructive choices at top with destructive style, Cancel at bottom, no scrolling, anchored to the source control. watchOS ≤ 4 buttons incl. Cancel; not on visionOS.

**Sheet** (CMP-09, CMP-10): Cancel leading + Done trailing (iOS); pair Done with Cancel or Back; never all three. iPhone: medium detent for progressive disclosure, grabber when resizable, swipe to dismiss with a save/discard confirmation for unsaved changes. iPad: page/form sheet styles. macOS: reasonable default size; use a panel for repeated input. visionOS: centered, not covering the whole window.

**Popover** (CMP-16): small, related functionality; arrow to its source; auto-close saves work; one at a time; never for warnings; sheet instead in compact width.

**Feedback** (PAT-04): inline status first; warn only about unexpected, irreversible loss; confirm significant completions (e.g., payments); explain why a command can’t run; combine visual + text + haptics + sound.

## 4. Menus and context menus

| Menus (CMP-17) | Context menus (CMP-18) |
|---|---|
| Title-case verb labels, no articles | Same labeling |
| Most-used first; groups with separators | Most-used nearest the touch/pointer; ≤ ~3 groups |
| Dim unavailable items (menu stays openable) | **Hide** unavailable items |
| Submenus: 1 level, ≤ ~5 items | Submenus: 1 level |
| Show keyboard shortcuts (menu bar) | No keyboard shortcuts |
| Icons: all items in a group or none | Destructive items **last**, destructive style |
| iOS layouts: small (4 icons), medium (3 icon+label), large (list) | Every item also available in main UI (MUST) |

Toggled items: changeable label (“Show Map”/“Hide Map”) or a checkmark. iOS: provide either a context menu or an edit menu for an item, not both.

## 5. Lists, tables, collections, scroll views

- Text-heavy data → list/table; varied-size or image-heavy → collection.
- Navigation lists keep the selected row highlighted; option lists flash then show a checkmark.
- iOS/iPadOS/visionOS: disclosure indicator to drill in; info button only for details; no index alongside trailing accessories (CMP-19). Grouped style + grouped background colors for settings-like content (COL-08).
- Section headers use **title-style capitalization** (no longer rendered all caps) (WRT-04).
- macOS tables: sortable columns (click again reverses), resizable columns, alternating rows for wide tables, outline views for hierarchy.
- Scroll views: show partial content to hint at more; never nest same-axis scroll views (CMP-20); page-by-page with a page control (not also a scroll indicator); auto-scroll only as much as needed.

## 6. Input controls

| Control | Specify |
|---|---|
| Text field | Label + placeholder hint; `keyboardType`, `textContentType`, `submitLabel`; size to expected input; vertical stacks with consistent widths; logical tab order; validate at the right moment; Clear button (iOS) |
| Secure field | Always for passwords/sensitive data; never prefilled (CMP-21) |
| Toggle | iOS switch only in list rows; states differ by more than color (CMP-23) |
| Segmented control | ≤ 5 segments on iPhone (5–7 wide); equal widths; text **or** images; noun labels (CMP-24) |
| Picker / date picker | Predictable order; in context; iOS styles compact / inline / wheels / automatic; coarser minute intervals when useful |
| Slider | Min leading, max trailing; optional field + stepper; never for iOS volume (CMP-26) |
| Stepper | Small, precise increments; pair with a visible value |

## 7. Status and progress

- Determinate whenever duration is knowable; switch indeterminate → determinate when possible; never spinner ↔ bar (CMP-27).
- Honest pace, keep it moving, consistent location, Cancel/Pause if safe, confirm destructive cancellation.
- Specific text (“Uploading 3 photos”), not “Loading…”. For generative AI: describe what’s happening (“Summarizing key themes from your notes”) (AI-06).
- iOS refresh control plus automatic refresh; refresh title only if it adds information (e.g., last update time).
- watchOS: avoid indeterminate indicators (PLT-WATCH-02).

## 8. Experience patterns

| Pattern | Key rules |
|---|---|
| Launch | Instant; restore state (SYS-04); launch screen ≈ first screen, no text, no branding (PAT-01) |
| Onboarding | Interactive, brief, skippable; contextual tips (TipKit); postpone setup; ask for ratings later (PAT-02) |
| Loading | Placeholders immediately; keep app usable; background downloads (PAT-03) |
| Settings | Great defaults; few settings; ⌘,; task options inline; never duplicate system settings (PAT-05, SYS-03) |
| Undo | Multiple levels; describe (“Undo Typing”); reveal off-screen results (PAT-06) |
| Data entry | Pull from system; choices over typing; paste/drag; validate live; enable Continue when ready (PAT-07) |
| Permissions | In context; specific purpose string; pre-alert screen with one “Continue” button; never manipulate (PRV-01 – PRV-04) |
| Authentication | Passkeys, Sign in with Apple, Password AutoFill, biometrics; keychain (PRV-05) |
| Generative AI | Disclose; keep people in control; confirm significant actions; privacy; specific progress; fallback (AI-01 – AI-06) |
| Full screen | People choose when to enter/exit; essential controls reachable; resume state (PAT-08) |

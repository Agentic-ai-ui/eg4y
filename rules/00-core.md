# 00 · Core rules (`SYS`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §0–§1. Format and severities: [`README.md`](README.md).

These rules apply to every screen on every Apple platform. They encode Apple’s “use the system first” model and the design principles.

---

### SYS-01 · Prefer standard system components
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD build with standard SwiftUI, UIKit, or AppKit components before customizing, and customize before building from scratch.
- **Why:** Standard components adopt Liquid Glass, Dark Mode, Dynamic Type, accessibility, right-to-left layout, and platform behavior automatically.
- **Do:** Use `NavigationSplitView`, `TabView`, `.toolbar`, `List`, `Form`, `Button` with system styles.
- **Don't:** Rebuild a tab bar, navigation bar, or sheet from primitive shapes.
- **Source:** [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §0](../GUIDELINES.md#0-the-mental-model)

### SYS-02 · Make actions recoverable
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD build forgiveness in: prefer undo and reversible actions over confirmation prompts, and make guided flows easy to skip or escape.
- **Why:** Agency — people explore freely when they know they can reverse an action.
- **Source:** [HIG › Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles) · [GUIDELINES §1](../GUIDELINES.md#1-design-principles)

### SYS-03 · Respect systemwide settings
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT duplicate systemwide settings (appearance, accessibility accommodations, scrolling behavior, authentication) inside the app; the app must follow the person’s system choices.
- **Source:** [HIG › Settings](https://developer.apple.com/design/human-interface-guidelines/settings) · [HIG › Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### SYS-04 · Restore state on relaunch
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD restore the previous state — navigation location, scroll position, window size and position — so people continue where they left off.
- **Source:** [HIG › Launching](https://developer.apple.com/design/human-interface-guidelines/launching) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### SYS-05 · Work well with multitasking
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, tvOS, visionOS
- **Check:** review
- **Rule:** MUST work with multitasking: save and restore context at any time, pause activities that need attention when people switch away, handle audio interruptions, and finish user-initiated tasks in the background.
- **Source:** [HIG › Multitasking](https://developer.apple.com/design/human-interface-guidelines/multitasking) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### SYS-06 · Name the principle behind non-obvious decisions
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD state which design principle (Purpose, Agency, Responsibility, Familiarity, Flexibility, Simplicity, Craft, Delight) justifies any non-obvious design decision or deviation from a SHOULD rule.
- **Why:** Makes agent output reviewable and keeps trade-offs explicit.
- **Source:** [HIG › Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles) · [GUIDELINES §1](../GUIDELINES.md#1-design-principles)

### SYS-07 · Don’t decorate in the name of delight
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD NOT add decoration, motion, or effects that get in the way of the task; include only what’s necessary and let every element earn its place.
- **Source:** [HIG › Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles) · [GUIDELINES §1](../GUIDELINES.md#1-design-principles)

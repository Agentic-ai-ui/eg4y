# 06 · Iconography (`ICN`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §8. Format and severities: [`README.md`](README.md).
> Trademark and SF Symbols usage restrictions live in [`15-brand-legal.md`](15-brand-legal.md).

---

### ICN-01 · Prefer SF Symbols for interface icons
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD use SF Symbols for interface icons wherever a suitable symbol exists; create a custom symbol from an exported template when none does.
- **Source:** [HIG › SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) · [HIG › Icons](https://developer.apple.com/design/human-interface-guidelines/icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-02 · Use standard icons for standard actions
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD use Apple’s standard symbols for common actions — e.g., Share `square.and.arrow.up`, Copy `document.on.document`, Delete `trash`, Add `plus`, More `ellipsis`, Search `magnifyingglass`, Filter `line.3.horizontal.decrease`, Done `checkmark`, Cancel `xmark`.
- **Source:** [HIG › Icons](https://developer.apple.com/design/human-interface-guidelines/icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-03 · Keep interface icons visually consistent
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST give all interface icons a consistent size, level of detail, stroke weight, and perspective, and SHOULD match icon weight to adjacent text.
- **Source:** [HIG › Icons](https://developer.apple.com/design/human-interface-guidelines/icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-04 · Ship custom icons as vectors
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST provide custom interface icons as vector PDF/SVG or custom SF Symbols (not single-resolution PNGs), optically centered with any needed padding baked into the asset.
- **Source:** [HIG › Icons](https://developer.apple.com/design/human-interface-guidelines/icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-05 · Pick the right rendering mode and variant
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD choose a symbol rendering mode (monochrome, hierarchical, palette, multicolor) that stays legible in context; use outline variants in toolbars and lists, fill variants for iOS tab bars, swipe actions, and selection, and slash variants for unavailable states.
- **Source:** [HIG › SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-06 · Variable color means change, not depth
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT use variable color to convey depth; use it only for values that change (level, strength, progress) and use hierarchical rendering for depth.
- **Source:** [HIG › SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-07 · Animate symbols with purpose
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD apply symbol animations (Bounce, Pulse, Replace, Draw On/Off, etc.) judiciously, only when each communicates a clear meaning consistent with the app’s tone.
- **Source:** [HIG › SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-08 · No custom selected states for standard bars
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD NOT supply selected-state icon variants for standard toolbars, tab bars, and buttons — the system renders selection.
- **Source:** [HIG › Icons](https://developer.apple.com/design/human-interface-guidelines/icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-09 · Build app icons from unmasked layers
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST provide app icon layers unmasked at the platform canvas size — 1024×1024 px square (iOS, iPadOS, macOS, visionOS), 1088×1088 px square (watchOS), 800×480 px rectangle (tvOS) — and let the system apply the mask; compose iOS/iPadOS/macOS/watchOS icons in Icon Composer.
- **Source:** [HIG › App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-10 · Consistent icon across appearances
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS
- **Check:** review
- **Rule:** MUST keep the app icon’s core features the same in default, dark, clear, and tinted appearances; base the dark icon on the light icon.
- **Source:** [HIG › App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-11 · Keep app icons simple
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD design app icons around one simple concept with minimal shapes and a simple background; prefer illustrations to photos; avoid replicating UI or screenshots; include text only when essential (never “Watch”, “Play”, “New”, “For visionOS”).
- **Source:** [HIG › App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-12 · Let the system add icon effects
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD NOT bake highlights, shadows, bevels, blurs, or glows into app icon layers; if custom effects are essential, use them intentionally and test them in Icon Composer and on device.
- **Source:** [HIG › App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-13 · Platform-specific app icon constraints
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** tvOS, visionOS, watchOS
- **Check:** review
- **Rule:** SHOULD keep a safe zone in tvOS icons, avoid hole-like shapes in visionOS background layers, and avoid black backgrounds in watchOS icons.
- **Source:** [HIG › App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### ICN-14 · Provide high-resolution image assets
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST provide bitmap assets at every required scale factor — iOS @2x and @3x; iPadOS and watchOS @2x; macOS and tvOS @1x and @2x; visionOS @2x or higher (prefer vectors) — with embedded color profiles.
- **Source:** [HIG › Images](https://developer.apple.com/design/human-interface-guidelines/images) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

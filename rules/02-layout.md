# 02 · Layout (`LAY`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §3. Format and severities: [`README.md`](README.md).

---

### LAY-01 · Decide layout from size classes, not device or orientation
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, tvOS, visionOS
- **Check:** hook
- **Rule:** MUST base layout decisions on horizontal/vertical size classes and available space, not on device type (idiom), screen bounds, or orientation.
- **Do:** Read `@Environment(\.horizontalSizeClass)` or `UITraitCollection.horizontalSizeClass`.
- **Don't:** Branch on `UIDevice.current.userInterfaceIdiom`, `UIScreen.main.bounds`, or `UIDevice.current.orientation` to pick a layout.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-02 · Respect safe areas and layout guides
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST keep controls and essential content inside system safe areas, margins, and layout guides; only full-bleed backgrounds may extend beyond them.
- **Why:** Hardware features (Dynamic Island, camera housings, reserved regions) and system bars must never obscure content.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-03 · Adapt to every size-class combination
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** MUST produce a usable layout for every combination of compact/regular width and height, arbitrary window sizes (iPad, Mac, visionOS, iPhone Duo), external displays, and Display Zoom — without fixed widths tied to one screen.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-04 · Make layout respond to text size
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, tvOS, visionOS, watchOS
- **Check:** review
- **Rule:** MUST adapt layout to larger text: stack horizontally adjacent views vertically, let rows grow in height, allow multiple lines, and reduce column counts at accessibility sizes.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### LAY-05 · Order content by importance
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD place the most important content near the top and leading side, following reading order.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-06 · Align, indent, and group deliberately
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD align related elements, use indentation to show subordination, and group related items with negative space, container shapes, or separators.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-07 · Use progressive disclosure
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD reduce initial content with disclosure controls, menus, nested views, or scrollable sections instead of showing every option at once.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-08 · Separate controls from content with Liquid Glass
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, tvOS, watchOS
- **Check:** review
- **Rule:** MUST distinguish controls from content by placing them in the Liquid Glass layer and using a scroll edge effect — not by adding solid or semi-opaque backgrounds beneath controls.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [HIG › Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-09 · Extend backgrounds beneath bars
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS
- **Check:** review
- **Rule:** SHOULD extend full-screen background content beneath sidebars, toolbars, and tab bars; use a background extension effect when a sidebar or inspector would cover important imagery.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [HIG › Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-10 · Scale artwork, never distort it
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD scale background artwork to fill the display when the aspect ratio changes, never stretching it or changing its aspect ratio.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-11 · Nest corners concentrically
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS
- **Check:** review
- **Rule:** SHOULD give custom components corner radii that are concentric with their container (bars, sheets, windows, hardware), using the system concentric shape APIs.
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §4](../GUIDELINES.md#4-materials-and-liquid-glass)

### LAY-12 · macOS: keep critical items off the window bottom
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** macOS
- **Check:** review
- **Rule:** SHOULD NOT place controls or critical information at the bottom of a window or sidebar, or behind the camera housing.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [HIG › Windows](https://developer.apple.com/design/human-interface-guidelines/windows) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-13 · tvOS: honor the safe area
- **Level:** MUST
- **Severity:** error
- **Platforms:** tvOS
- **Check:** review
- **Rule:** MUST inset primary content 60 pt from the top and bottom and 80 pt from the sides of the screen.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-14 · tvOS: use grid specifications
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** tvOS
- **Check:** review
- **Rule:** SHOULD use 40 pt horizontal spacing and at least 100 pt vertical spacing in grids, with Apple’s unfocused content widths (2-col 860 pt … 9-col 160 pt), consistent spacing, and symmetric partially hidden items.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

### LAY-15 · visionOS: space interactive items for eyes
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** visionOS
- **Check:** review
- **Rule:** SHOULD place interactive items so their centers are at least 60 pt apart (or keep at least 16 pt of space around each), so the hover effect never crowds neighbors.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [HIG › Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

### LAY-16 · watchOS: limit controls per row
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** watchOS
- **Check:** review
- **Rule:** SHOULD NOT place more than three glyph buttons or two text buttons side by side.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §3](../GUIDELINES.md#3-layout)

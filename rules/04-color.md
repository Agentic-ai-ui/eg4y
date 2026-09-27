# 04 · Color and Dark Mode (`COL`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §5–§6. Format and severities: [`README.md`](README.md).

---

### COL-01 · Use system colors through their APIs
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** hook
- **Rule:** MUST NOT hard-code system or semantic color values in views; reference them through the system API (`Color.blue`, `Color(.label)`, `UIColor.systemBackground`, `NSColor.labelColor`) or a named asset-catalog Color Set.
- **Why:** Apple documents values for design reference only; they change between releases and adapt to appearance and accessibility settings.
- **Don't:** `Color(red: 0, green: 0.53, blue: 1)`, `UIColor(hex:)`, `#colorLiteral(...)`, raw hex in view code.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [GUIDELINES §5](../GUIDELINES.md#5-color)

### COL-02 · Give every custom color all its variants
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, tvOS
- **Check:** review
- **Rule:** MUST define each custom color with light and dark variants, each with an increased-contrast option — even if the app ships in one appearance.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [HIG › Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode) · [GUIDELINES §5](../GUIDELINES.md#5-color)

### COL-03 · Never rely on color alone
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT use color as the only way to convey information, interactivity, status, selection, or focus; pair it with text, shape, or a symbol.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [GUIDELINES §5](../GUIDELINES.md#5-color)

### COL-04 · One meaning per color
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT use the same color to mean different things (for example, an interactive tint also applied to non-interactive text).
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [GUIDELINES §5](../GUIDELINES.md#5-color)

### COL-05 · Don’t repurpose semantic colors
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, tvOS, visionOS
- **Check:** review
- **Rule:** MUST NOT redefine dynamic system colors’ meanings — for example, separator as text color or secondary label as a background.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [GUIDELINES §5](../GUIDELINES.md#5-color)

### COL-06 · Meet contrast minimums
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST meet at least 4.5:1 contrast for text up to 17 pt and 3:1 for text 18 pt and larger or bold, in both appearances; strive for 7:1 for custom foreground/background pairs in small text. If defaults can’t meet this, MUST provide a higher-contrast scheme when Increase Contrast is on.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [HIG › Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### COL-07 · Follow the system appearance
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, tvOS
- **Check:** hook
- **Rule:** MUST NOT offer an app-specific appearance setting or force a color scheme; support light, dark, and Auto. Rare exception: immersive media experiences may stay permanently dark.
- **Don't:** Apply `.preferredColorScheme(.light)` or `overrideUserInterfaceStyle` to the whole app.
- **Source:** [HIG › Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode) · [GUIDELINES §6](../GUIDELINES.md#6-dark-mode)

### COL-08 · Prefer system background colors
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS
- **Check:** review
- **Rule:** SHOULD use the system background set (or the grouped set for grouped tables and forms) at primary, secondary, and tertiary levels so the system can switch between base and elevated colors in Dark Mode.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [HIG › Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode) · [GUIDELINES §5](../GUIDELINES.md#5-color)

### COL-09 · Apply the accent color judiciously
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD reserve the brand/accent color for primary actions, status indicators, and selection (such as the selected tab), and move broader brand color into the content layer.
- **Source:** [HIG › Branding](https://developer.apple.com/design/human-interface-guidelines/branding) · [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [GUIDELINES §5](../GUIDELINES.md#5-color)

### COL-10 · Keep bars legible over colorful content
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS
- **Check:** review
- **Rule:** SHOULD prefer monochromatic toolbars and tab bars over colorful content, avoid control label colors similar to content colors, and keep the resting state (top of scroll) legible.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [HIG › Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) · [GUIDELINES §5](../GUIDELINES.md#5-color)

### COL-11 · Tame white images in Dark Mode
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, tvOS
- **Check:** review
- **Rule:** SHOULD slightly darken content images with white backgrounds in Dark Mode, and provide separate light/dark icon or image assets when one asset doesn’t work in both.
- **Source:** [HIG › Dark Mode](https://developer.apple.com/design/human-interface-guidelines/dark-mode) · [GUIDELINES §6](../GUIDELINES.md#6-dark-mode)

### COL-12 · Manage color spaces
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD embed color profiles in images, and when using Display P3 provide sRGB variants where colors or gradients would clip or become indistinguishable.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [GUIDELINES §5](../GUIDELINES.md#5-color)

### COL-13 · Consider cultural color meaning
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD verify that colors communicate the intended meaning in every locale the app supports.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [HIG › Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion) · [GUIDELINES §5](../GUIDELINES.md#5-color)

### COL-14 · Use system color pickers
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD use the system color picker (`ColorPicker`, color wells) when people choose colors.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [GUIDELINES §5](../GUIDELINES.md#5-color)

# 05 · Typography (`TYP`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §7. Format and severities: [`README.md`](README.md).

**Platform text sizes (default / minimum):** iOS & iPadOS 17 / 11 pt · macOS 13 / 10 pt · tvOS 29 / 23 pt · visionOS 17 / 12 pt · watchOS 16 / 12 pt.

---

### TYP-01 · Use built-in text styles
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, tvOS, visionOS, watchOS
- **Check:** hook
- **Rule:** MUST set text with system text styles (`.largeTitle` … `.caption2`) so it supports Dynamic Type and larger accessibility sizes; fixed point sizes that don’t scale are not allowed.
- **Do:** `.font(.body)`, `.font(.headline)`, `UIFont.preferredFont(forTextStyle: .body)`.
- **Don't:** `.font(.system(size: 17))`, `UIFont.systemFont(ofSize: 17)` for body text.
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### TYP-02 · Never go below the platform minimum size
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** hook
- **Rule:** MUST NOT display text smaller than the platform minimum (11 pt iOS/iPadOS, 10 pt macOS, 23 pt tvOS, 12 pt visionOS and watchOS), for system or custom fonts.
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### TYP-03 · Avoid light font weights
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** hook
- **Rule:** SHOULD NOT use Ultralight, Thin, or Light weights for interface text; prefer Regular, Medium, Semibold, or Bold, and enlarge thin custom fonts.
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### TYP-04 · Don’t embed system fonts
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** hook
- **Rule:** MUST NOT bundle San Francisco or New York font files in an app or web page; access system fonts through `Font.Design` (`.default`, `.serif`, `.rounded`, `.monospaced`) or, on the web, the `system-ui` / `ui-serif` / `ui-rounded` / `ui-monospace` families.
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §18](../GUIDELINES.md#18-brand-and-legal-boundaries)

### TYP-05 · Custom fonts must scale and respect Bold Text
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, tvOS, visionOS, watchOS
- **Check:** hook
- **Rule:** MUST make custom fonts legible at recommended sizes and implement Dynamic Type (for example `Font.custom(_:size:relativeTo:)` or `UIFontMetrics`) and Bold Text support.
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### TYP-06 · Minimize typefaces
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD minimize the number of typefaces; when branding requires a custom font, use it for headlines and subheadings and the system font for body and captions.
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [HIG › Branding](https://developer.apple.com/design/human-interface-guidelines/branding) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### TYP-07 · Preserve hierarchy at every text size
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD express hierarchy with weight, size, and color, keep that hierarchy intact as text size changes, and keep primary elements near the top at large sizes.
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### TYP-08 · Minimize truncation
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, tvOS, visionOS, watchOS
- **Check:** hook
- **Rule:** SHOULD show as much useful text at the largest accessibility size as at the largest standard size; avoid single-line limits and truncation in scrollable regions unless people can open the full content.
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### TYP-09 · Scale meaningful icons with text
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, tvOS, visionOS, watchOS
- **Check:** review
- **Rule:** SHOULD enlarge interface icons that carry meaning as the text size grows (SF Symbols scale automatically).
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### TYP-10 · Prioritize what grows
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, tvOS, visionOS, watchOS
- **Check:** review
- **Rule:** SHOULD prioritize enlarging the content people care about rather than every string (for example, not tab titles or transient values).
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### TYP-11 · Avoid tight leading for long text
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD NOT use tight leading for three or more lines of text; use loose leading for wide columns and long passages.
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### TYP-12 · Use platform text style tables
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD match the platform’s built-in text style specifications (e.g., iOS Body 17/22 pt, macOS Body 13/16 pt, tvOS Body 29/36 pt, watchOS Body 16/18.5 pt) when mocking up or implementing custom type.
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

### TYP-13 · visionOS: keep text flat, bold, and facing people
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** visionOS
- **Check:** review
- **Rule:** SHOULD prefer 2D text, maximize contrast with its background, make free-floating text bold instead of adding shadows, and billboard labels attached to 3D objects.
- **Source:** [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §7](../GUIDELINES.md#7-typography)

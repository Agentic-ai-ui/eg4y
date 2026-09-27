# 03 · Materials and Liquid Glass (`GLS`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §4. Format and severities: [`README.md`](README.md).

---

### GLS-01 · No Liquid Glass in the content layer
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, tvOS, watchOS
- **Check:** review
- **Rule:** MUST NOT apply Liquid Glass to content-layer elements such as app backgrounds, list rows, or cards; use standard materials there. Exception: transient interactive elements (slider and toggle knobs) that take on glass while being manipulated.
- **Source:** [HIG › Materials](https://developer.apple.com/design/human-interface-guidelines/materials) · [GUIDELINES §4](../GUIDELINES.md#4-materials-and-liquid-glass)

### GLS-02 · Use custom glass sparingly
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, tvOS, watchOS
- **Check:** hook
- **Rule:** SHOULD rely on standard components for Liquid Glass and apply custom glass effects only to the few most important functional elements.
- **Source:** [HIG › Materials](https://developer.apple.com/design/human-interface-guidelines/materials) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §4](../GUIDELINES.md#4-materials-and-liquid-glass)

### GLS-03 · No glass on glass
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, tvOS, watchOS
- **Check:** review
- **Rule:** MUST NOT layer Liquid Glass elements on top of each other or overcrowd them; keep standard spacing metrics.
- **Source:** [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §4](../GUIDELINES.md#4-materials-and-liquid-glass)

### GLS-04 · Remove custom bar and sheet backgrounds
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS
- **Check:** hook
- **Rule:** SHOULD remove custom backgrounds and tints from navigation bars, tab bars, toolbars, split views, sheets, and popovers so the system can render Liquid Glass and scroll edge effects.
- **Don't:** Set opaque `UINavigationBarAppearance` backgrounds, `.toolbarBackground(...)` colors, or visual effect views inside popovers.
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §4](../GUIDELINES.md#4-materials-and-liquid-glass)

### GLS-05 · Choose the right glass variant
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, tvOS, watchOS
- **Check:** review
- **Rule:** MUST use the regular variant by default and for text-heavy components; use the clear variant only over visually rich media, adding a 35% dark dimming layer when the content underneath is bright.
- **Source:** [HIG › Materials](https://developer.apple.com/design/human-interface-guidelines/materials) · [GUIDELINES §4](../GUIDELINES.md#4-materials-and-liquid-glass)

### GLS-06 · Test glass with accessibility and display settings
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST verify custom glass, colors, and animations with Reduce Transparency, Increase Contrast, Reduce Motion, and the person’s preferred Liquid Glass look.
- **Source:** [HIG › Materials](https://developer.apple.com/design/human-interface-guidelines/materials) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §4](../GUIDELINES.md#4-materials-and-liquid-glass)

### GLS-07 · Use scroll edge effects correctly
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS
- **Check:** review
- **Rule:** SHOULD use a scroll edge effect only where scrolling content passes behind floating UI, apply one per view (one per pane in split views, with matching heights), and prefer the automatic style.
- **Source:** [HIG › Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views) · [GUIDELINES §4](../GUIDELINES.md#4-materials-and-liquid-glass)

### GLS-08 · Group custom glass in a container
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, tvOS, watchOS
- **Check:** hook
- **Rule:** SHOULD combine multiple custom glass effects inside one `GlassEffectContainer` for rendering performance and fluid morphing, applying `glassEffect` after other appearance modifiers.
- **Source:** [Applying Liquid Glass to custom views](https://developer.apple.com/documentation/swiftui/applying-liquid-glass-to-custom-views) · [GUIDELINES §4](../GUIDELINES.md#4-materials-and-liquid-glass)

### GLS-09 · Color on glass: only the primary action
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, tvOS, watchOS
- **Check:** review
- **Rule:** MUST NOT tint the backgrounds of multiple controls; reserve color on Liquid Glass for status or the primary action, and tint its background rather than its symbol or text.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [GUIDELINES §5](../GUIDELINES.md#5-color)

### GLS-10 · Vibrant colors on standard materials
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** MUST use system vibrant label, fill, and separator colors on standard materials; choose materials by semantic purpose; avoid quaternary label vibrancy on thin and ultra-thin materials.
- **Source:** [HIG › Materials](https://developer.apple.com/design/human-interface-guidelines/materials) · [GUIDELINES §4](../GUIDELINES.md#4-materials-and-liquid-glass)

### GLS-11 · visionOS: keep the glass window background
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** visionOS
- **Check:** review
- **Rule:** SHOULD retain the system glass background of windows and prefer translucency over opaque color.
- **Source:** [HIG › Windows](https://developer.apple.com/design/human-interface-guidelines/windows) · [HIG › Materials](https://developer.apple.com/design/human-interface-guidelines/materials) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

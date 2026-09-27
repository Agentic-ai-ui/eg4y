# 16 · Implementation stacks (`STK`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §17 (Other implementation surfaces) and §18. Format and severities: [`README.md`](README.md).

Every other rule in this folder is stack-neutral. These rules cover what changes when the app is built with web technology (React, Next.js, HTML + CSS, Tailwind CSS, Vue, Svelte) or React Native instead of SwiftUI, UIKit, or AppKit. Equivalents per stack: [`skills/apple-design-language/references/stack-map.md`](../skills/apple-design-language/references/stack-map.md).

---

### STK-01 · Apply the same rules on every stack
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD apply every rule in this set whatever the implementation — SwiftUI, UIKit, AppKit, a web framework, or React Native — translating it through the stack’s own mechanism instead of dropping rules the stack makes harder.
- **Why:** People judge the interface, not the framework; an app is only consistent across Apple devices if every build follows the same rules (SYNC-01).
- **Do:** Map system colors to `tokens.css` variables or `PlatformColor`, text styles to `rem` styles or Dynamic Type ramps, and Reduce Motion to `prefers-reduced-motion` or `AccessibilityInfo`.
- **Don't:** Skip safe areas, Dynamic Type, or labels because “it’s just a web app.”
- **Source:** [HIG › Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios) · [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [GUIDELINES §17](../GUIDELINES.md#other-implementation-surfaces-web-and-react-native)

### STK-02 · Keep SF Symbols inside apps for Apple platforms
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT ship SF Symbols — as exported SVGs, fonts, or images — in websites, web apps, or builds for non-Apple platforms; use an open-licensed icon set there. Apps running on Apple platforms, including React Native apps on iOS, may draw SF Symbols through the system.
- **Why:** Apple licenses these system-provided images solely for developing apps for Apple-branded products that run on the system they were provided for (Xcode and Apple SDKs Agreement §2.10).
- **Do:** Lucide (ISC), Phosphor (MIT), Heroicons (MIT), or Material Symbols (Apache 2.0) on the web; `SymbolView` with SF Symbols on iOS and Material Symbols elsewhere in React Native.
- **Source:** [HIG › SF Symbols](https://developer.apple.com/design/human-interface-guidelines/sf-symbols) · [Xcode and Apple SDKs Agreement](https://www.apple.com/legal/sla/docs/xcode.pdf) · [GUIDELINES §18](../GUIDELINES.md#18-brand-and-legal-boundaries)

### STK-03 · Build web controls from native elements
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** hook
- **Rule:** SHOULD build web controls from native elements — `<button>`, `<a href>`, `<dialog>`, `<input>`, `<select>`, `popover` — and SHOULD NOT attach click handlers to `<div>` or `<span>` elements, which have no role, focus, or keyboard support.
- **Why:** Native elements are the web’s system components: they bring the role VoiceOver announces, keyboard focus, and activation behavior for free (SYS-01, A11Y-03, A11Y-07).
- **Do:** `<button type="button" onClick={add}>Add Book</button>`
- **Don't:** `<div onClick={add}>Add Book</div>`
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [HIG › Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) · [WAI-ARIA Authoring Practices](https://www.w3.org/WAI/ARIA/apg/) · [GUIDELINES §17](../GUIDELINES.md#other-implementation-surfaces-web-and-react-native)

### STK-04 · Meet WCAG 2.2 AA contrast on the web
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD meet WCAG 2.2 AA contrast in web builds in addition to COL-06 — 4.5:1 for text below 24 px, or below 18.66 px when bold — using the increased-contrast variants of system colors for colored text where the default variants fall short.
- **Why:** WCAG is the accessibility baseline for the web and is stricter than the HIG for small bold text; blue on white is 3.52:1, while the increased-contrast blue is 4.57:1.
- **Do:** `color: var(--adl-accent-text)`; colored text on the page background or a list row.
- **Don't:** Blue or red text on a gray fill in light mode.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [WCAG 2.2](https://www.w3.org/TR/WCAG22/) · [GUIDELINES §17](../GUIDELINES.md#other-implementation-surfaces-web-and-react-native)

### STK-05 · Generate every stack’s tokens from one source
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD generate colors, text styles, and sizes for every stack in a product from one token source instead of maintaining parallel values per platform or framework.
- **Why:** Hand-copied values drift, and drift breaks the cross-platform consistency people rely on (SYNC-03).
- **Do:** Edit `tokens.json`, run `build_tokens.py`, and ship the generated `tokens.css`, `tokens.ts`, `tailwind.css`, and `tokens.native.ts`.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [HIG › Typography](https://developer.apple.com/design/human-interface-guidelines/typography) · [GUIDELINES §17](../GUIDELINES.md#other-implementation-surfaces-web-and-react-native)

### STK-06 · Use native views in React Native
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS
- **Check:** review
- **Rule:** SHOULD use native views in React Native — the system tab bar and navigation stack, `Switch`, `Alert` and `ActionSheetIOS`, `PlatformColor`, and Dynamic Type ramps — instead of JavaScript re-creations of system components.
- **Why:** Native views bring Liquid Glass, Dynamic Type, VoiceOver, and future system changes for free; look-alikes must re-create and maintain all of it (SYS-01).
- **Do:** Expo Router native tabs; a native stack with `headerLargeTitleEnabled`.
- **Don't:** A custom JavaScript tab bar styled to look like iOS.
- **Source:** [HIG › Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) · [HIG › Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios) · [GUIDELINES §17](../GUIDELINES.md#other-implementation-surfaces-web-and-react-native)

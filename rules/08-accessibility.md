# 08 · Accessibility (`A11Y`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §11. Format and severities: [`README.md`](README.md).
> Contrast is COL-06; Reduce Motion is MOT-02; text sizing is TYP-01/TYP-02.

**Control sizes (default / minimum):** iOS & iPadOS 44×44 / 28×28 pt · macOS 28×28 / 20×20 pt · tvOS 66×66 / 56×56 pt · visionOS 60×60 / 28×28 pt · watchOS 44×44 / 28×28 pt.

---

### A11Y-01 · Size controls for every input
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** hook
- **Rule:** MUST give every tappable or clickable control a hit region of at least the platform default size (44×44 pt on iOS, iPadOS, and watchOS; 60×60 pt on visionOS; 28×28 pt on macOS; 66×66 pt on tvOS) and never smaller than the platform minimum.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [HIG › Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-02 · Space controls apart
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD leave about 12 pt of padding around bezeled elements and about 24 pt around the visible edges of non-bezeled elements.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-03 · Label every control for VoiceOver
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** hook
- **Rule:** MUST give every key interface element — especially icon-only buttons, toolbar items, and custom controls — a descriptive accessibility label, and keep labels current as content changes.
- **Do:** `Button { … } label: { Label("Share", systemImage: "square.and.arrow.up") }` or `.accessibilityLabel("Share")`.
- **Source:** [HIG › VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-04 · Describe meaningful images, hide decorative ones
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** hook
- **Rule:** MUST provide descriptions for meaningful images and infographics and exclude purely decorative images from assistive technologies.
- **Do:** `Image(decorative:)`, `.accessibilityHidden(true)`, `alt=""` for decorative web images; real descriptions otherwise.
- **Source:** [HIG › VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-05 · Let people enlarge text
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** hook
- **Rule:** SHOULD let people enlarge text by at least 200% (140% on watchOS), ideally through Dynamic Type; on the web, never disable browser zoom.
- **Don't:** `<meta name="viewport" content="…user-scalable=no">` or `maximum-scale=1`.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-06 · Offer alternatives to gestures
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST make every gesture-driven action also available through an on-screen control (for example, a button as well as swipe-to-dismiss), and use the simplest gesture for frequent actions.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [HIG › Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-07 · Support keyboard-only use
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD let people navigate and operate the whole app with Full Keyboard Access, and support Voice Control, Switch Control, AssistiveTouch, and Pointer Control with properly labeled elements.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [HIG › Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-08 · Structure content for navigation
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD give each screen a unique title, mark section headings, group related elements, set a logical reading order, announce content and layout changes, and support the VoiceOver rotor.
- **Source:** [HIG › VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-09 · Avoid timed interfaces
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD NOT auto-dismiss views or controls on a timer; prefer explicit dismissal.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-10 · Let people control media
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST provide discoverable controls to start and stop any audio or video, avoid autoplay without controls, and respond to the Dim Flashing Lights setting in video playback.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-11 · Provide text alternatives for media
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD provide captions, subtitles, audio descriptions, or transcripts as appropriate, with customizable presentation.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-12 · Optimize for Assistive Access
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS
- **Check:** review
- **Rule:** SHOULD, when Assistive Access is on, show core functionality only, one interaction per screen, and confirm hard-to-undo actions twice.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-13 · Audit with Accessibility Inspector
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD audit every screen with Accessibility Inspector and test with VoiceOver, the largest accessibility text size, Increase Contrast, Reduce Transparency, and Reduce Motion before shipping.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-14 · visionOS: keep people comfortable
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** visionOS
- **Check:** review
- **Rule:** SHOULD keep UI within the field of view (prefer horizontal layouts), never anchor content to the wearer’s head, reduce animation speed and intensity in the periphery, and minimize large or repetitive gestures.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [HIG › Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### A11Y-15 · Games: offer difficulty accommodations
- **Level:** MAY
- **Severity:** info
- **Platforms:** All
- **Check:** review
- **Rule:** MAY let players customize difficulty, reaction time, or control assistance.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

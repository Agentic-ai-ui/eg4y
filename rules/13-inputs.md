# 13 · Inputs: gestures, keyboards, focus, eyes (`INP`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §15. Format and severities: [`README.md`](README.md).
> Gesture alternatives are A11Y-06; visionOS spacing is LAY-15.

---

### INP-01 · Standard gestures do standard things
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD NOT use a familiar gesture (tap, swipe, drag) for an app-unique action, or invent a gesture for a standard action like activating a button or scrolling.
- **Source:** [HIG › Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

### INP-02 · Custom gestures are never the only way
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST make custom gestures discoverable, easy to perform, distinct from other gestures, and never the only way to perform an important action; shortcut gestures supplement standard controls such as the Back button.
- **Source:** [HIG › Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

### INP-03 · Don’t collide with system gestures
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** iOS, iPadOS, visionOS, watchOS
- **Check:** review
- **Rule:** SHOULD NOT define gestures that conflict with system gestures (three-finger undo/redo and copy/paste, shake to undo, iPad four-finger app switching, edge swipes, visionOS palm and hand-roll overlays).
- **Source:** [HIG › Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) · [HIG › Undo and redo](https://developer.apple.com/design/human-interface-guidelines/undo-and-redo) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

### INP-04 · Respond to gestures immediately
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD give immediate feedback during gestures and clearly indicate when a gesture isn’t available (for example, a locked object that can’t be dragged).
- **Source:** [HIG › Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

### INP-05 · Keep standard keyboard shortcuts
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD NOT repurpose standard shortcuts (⌘C, ⌘V, ⌘X, ⌘Z, ⇧⌘Z, ⌘A, ⌘F, ⌘N, ⌘O, ⌘P, ⌘S, ⌘W, ⌘Q, ⌘, ⌘? and others); only reassign one whose action makes no sense in the app.
- **Source:** [HIG › Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

### INP-06 · Build custom shortcuts the Apple way
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD add custom shortcuts only for frequent commands, use Command as the main modifier and Shift as secondary, use Option sparingly, avoid Control, list modifiers in the order Control, Option, Shift, Command, and not add Shift for a key’s upper character.
- **Source:** [HIG › Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

### INP-07 · Let the system own focus
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** iPadOS, macOS, tvOS, visionOS
- **Check:** review
- **Rule:** SHOULD NOT move focus without people’s interaction (except when the focused item disappears during directional navigation); rely on system focus effects, using a focus ring for text fields and a highlight for list rows.
- **Source:** [HIG › Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

### INP-08 · tvOS: design for directional focus
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** tvOS
- **Check:** review
- **Rule:** SHOULD make every element reachable by directional focus, avoid a free pointer in menus, design all five focus states, and supply assets sized for the enlarged focused state.
- **Source:** [HIG › Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

### INP-09 · visionOS: indirect gestures first
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** visionOS
- **Check:** review
- **Rule:** SHOULD prefer indirect gestures (look and tap) for UI, reserve direct touch for nearby objects used briefly, avoid requiring specific body positions or a specific hand, and give interactive items rounded shapes with a single containing highlight region.
- **Source:** [HIG › Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) · [HIG › Eyes](https://developer.apple.com/design/human-interface-guidelines/eyes) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

### INP-10 · watchOS: respect double tap
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** watchOS
- **Check:** review
- **Rule:** SHOULD NOT set a primary double-tap action in views with lists, scroll views, or vertical tabs; in nonscrolling views, assign it to the most-used button.
- **Source:** [HIG › Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

### INP-11 · iPadOS: keyboard navigation for content, not controls
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** iPadOS
- **Check:** review
- **Rule:** SHOULD NOT add custom keyboard navigation to buttons, segmented controls, or switches; support it for text fields, text views, sidebars, and collections, and let Full Keyboard Access handle controls.
- **Source:** [HIG › Keyboards](https://developer.apple.com/design/human-interface-guidelines/keyboards) · [HIG › Focus and selection](https://developer.apple.com/design/human-interface-guidelines/focus-and-selection) · [GUIDELINES §15](../GUIDELINES.md#15-inputs)

# 07 · Motion and haptics (`MOT`, `HAP`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §9–§10. Format and severities: [`README.md`](README.md).

---

## Motion

### MOT-01 · Add motion only with purpose
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD add motion only when it supports the experience (status, feedback, instruction), keeping feedback animations brief and precise.
- **Source:** [HIG › Motion](https://developer.apple.com/design/human-interface-guidelines/motion) · [GUIDELINES §9](../GUIDELINES.md#9-motion)

### MOT-02 · Respect Reduce Motion
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** hook
- **Rule:** MUST reduce automatic and repetitive animation when Reduce Motion is on: tighten springs, track gestures directly, avoid z-axis depth animation, replace x/y/z transitions with fades, and avoid animating into or out of blurs.
- **Do:** Read `@Environment(\.accessibilityReduceMotion)` / `UIAccessibility.isReduceMotionEnabled`; on the web, honor `prefers-reduced-motion`.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [HIG › Motion](https://developer.apple.com/design/human-interface-guidelines/motion) · [GUIDELINES §9](../GUIDELINES.md#9-motion)

### MOT-03 · Motion is never the only channel
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST supplement any information conveyed through motion with text, haptics, or audio — motion is never the only channel.
- **Source:** [HIG › Motion](https://developer.apple.com/design/human-interface-guidelines/motion) · [GUIDELINES §9](../GUIDELINES.md#9-motion)

### MOT-04 · Let people cancel motion
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST keep animations interruptible so people never have to wait for one to finish before acting.
- **Source:** [HIG › Motion](https://developer.apple.com/design/human-interface-guidelines/motion) · [GUIDELINES §9](../GUIDELINES.md#9-motion)

### MOT-05 · Don’t animate frequent interactions
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD NOT add custom motion to UI interactions that happen frequently; system components already animate subtly.
- **Source:** [HIG › Motion](https://developer.apple.com/design/human-interface-guidelines/motion) · [GUIDELINES §9](../GUIDELINES.md#9-motion)

### MOT-06 · Make feedback motion realistic
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD make motion follow people’s gestures and expectations — a view revealed by sliding down dismisses by sliding up, not sideways.
- **Source:** [HIG › Motion](https://developer.apple.com/design/human-interface-guidelines/motion) · [GUIDELINES §9](../GUIDELINES.md#9-motion)

### MOT-07 · visionOS: protect visual comfort
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** visionOS
- **Check:** review
- **Rule:** SHOULD avoid motion at the edges of the field of view, fade objects to relocate them, never rotate the virtual world, give a stationary frame of reference, make large moving objects translucent or low contrast, and avoid sustained oscillation (especially near 0.2 Hz).
- **Source:** [HIG › Motion](https://developer.apple.com/design/human-interface-guidelines/motion) · [GUIDELINES §9](../GUIDELINES.md#9-motion)

### MOT-08 · Games: steady frame rate
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD keep games at a consistent 30–60 fps by default on each platform and let people trade visual quality for performance or battery life.
- **Source:** [HIG › Motion](https://developer.apple.com/design/human-interface-guidelines/motion) · [GUIDELINES §9](../GUIDELINES.md#9-motion)

## Haptics

### HAP-01 · Use system haptics for their documented meanings
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, macOS, watchOS
- **Check:** review
- **Rule:** MUST use system haptic patterns (notification, impact, selection on iOS; alignment, level change, generic on macOS; notification, up, down, success, failure, retry, start, stop, click on watchOS) only for their documented meanings.
- **Source:** [HIG › Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics) · [GUIDELINES §10](../GUIDELINES.md#10-haptics)

### HAP-02 · Consistent, complementary, sparing, optional
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, tvOS, watchOS
- **Check:** review
- **Rule:** SHOULD tie each haptic to one cause, match its intensity and sharpness to the accompanying visuals and sound, prefer short haptics for discrete events, avoid overuse, and let people turn haptics off.
- **Source:** [HIG › Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics) · [GUIDELINES §10](../GUIDELINES.md#10-haptics)

### HAP-03 · Pair audio cues with haptics and visuals
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD pair audio cues with matching haptics and visual indicators for people who can’t hear or have audio off.
- **Source:** [HIG › Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [GUIDELINES §11](../GUIDELINES.md#11-accessibility)

### HAP-04 · Don’t disrupt sensors
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** iOS, iPadOS, watchOS
- **Check:** review
- **Rule:** SHOULD NOT play haptics that disturb camera, gyroscope, or microphone use.
- **Source:** [HIG › Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics) · [GUIDELINES §10](../GUIDELINES.md#10-haptics)

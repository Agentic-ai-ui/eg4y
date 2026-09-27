# 09 · Writing, inclusion, and localization (`WRT`, `L10N`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §12. Format and severities: [`README.md`](README.md).
> Alert copy is CMP-12/CMP-13; permission purpose strings are PRV-02.

---

## Writing

### WRT-01 · Label actions with verbs
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD label buttons and action menu items with a verb or verb phrase (“Send”, “Add to Cart”) and avoid cute or clever labels (“Let’s do it!”).
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [HIG › Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-02 · Write descriptive link text
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** hook
- **Rule:** SHOULD NOT use “Click here” or similar vague link text; describe the destination (“Learn more about UX writing”).
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-03 · Describe gestures correctly for the device
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST use the gesture word that matches the device — “tap” for touch, “click” for pointer — or the device-neutral “choose” where the input method varies (as in alerts).
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [HIG › Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-04 · Apply capitalization consistently
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD use title-style capitalization for buttons, menu items and titles, segment labels, column headings, and list/form section headers, and sentence-style for messages, descriptions, and purpose strings — consistently per element type.
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [HIG › Menus](https://developer.apple.com/design/human-interface-guidelines/menus) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-05 · Use an ellipsis when more input is needed
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD append an ellipsis (…) to menu items and buttons whose action requires more input before completing (e.g., “Rename…”, “Export As…”).
- **Source:** [HIG › Menus](https://developer.apple.com/design/human-interface-guidelines/menus) · [HIG › Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-06 · Address people directly, avoid “we”
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD address people as “you” (not “the user”), avoid “we” in interface copy, and use possessives like “my” and “your” sparingly and consistently.
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [HIG › Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-07 · Write helpful error messages
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD show errors next to the problem, without blame, stating how to fix it (“Choose a password with at least 8 characters”); avoid “Oops!” and robotic messages like “Invalid name”.
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-08 · Give empty states a next step
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD explain what to do next on empty screens and offer a button or link to do it, without placing crucial information there.
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-09 · Use plain, inclusive language
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD write concise, plain language without jargon, undefined technical terms, colloquialisms, or unnecessary gender references, and consider humor carefully.
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [HIG › Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-10 · Keep multistep language consistent
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD start flows with language like “Get Started”, advance with one consistent term (“Continue” or “Next”), and finish with “Done”.
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-11 · Label fields and show hints
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD give every text field a label and a placeholder hint (“name@example.com”), and don’t rely on placeholder text alone since it disappears while typing.
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [HIG › Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-12 · Keep settings labels practical
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD label settings plainly, describe what happens when a setting is on, and link directly to a setting rather than describing its location.
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### WRT-13 · Represent people inclusively
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD use gender-neutral figures, portray diverse people without stereotypes, write about disability people-first, and offer inclusive options (nonbinary, self-identify, decline to state) if gender is required.
- **Source:** [HIG › Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

## Localization and right-to-left

### L10N-01 · Internationalize everything
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD externalize all user-facing strings, let the system format dates, times, numbers, and currency, and allow for text expansion.
- **Source:** [HIG › Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion) · [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### L10N-02 · Mirror directional UI in right-to-left
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD flip progress controls, sliders, back/forward navigation, and icons that depict text or forward motion in RTL contexts, and reverse numerals that show progress or sequence.
- **Source:** [HIG › Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### L10N-03 · Never mirror what must stay fixed
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT reverse the digits within a number or flip logos, universal marks (such as the checkmark), photos, or controls that refer to an actual direction.
- **Source:** [HIG › Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### L10N-04 · Align text by context and language
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD align one- and two-line text to the interface direction, align paragraphs (three or more lines) to their own language, align all list items consistently, and enlarge Arabic or Hebrew about 2 pt beside uppercase Latin text.
- **Source:** [HIG › Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

### L10N-05 · Keep text out of images
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD avoid text in icons, images, and launch screens; localize any characters that must appear in an icon.
- **Source:** [HIG › Icons](https://developer.apple.com/design/human-interface-guidelines/icons) · [HIG › Launching](https://developer.apple.com/design/human-interface-guidelines/launching) · [GUIDELINES §12](../GUIDELINES.md#12-inclusion-and-writing)

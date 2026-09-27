# 11 · Components (`CMP`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §13. Format and severities: [`README.md`](README.md).
> Hit targets are A11Y-01; navigation containers are in [`10-navigation.md`](10-navigation.md).

---

## Buttons

### CMP-01 · At most two prominent buttons per view
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD give the most likely action a prominent style and keep prominent buttons to one or two per view.
- **Source:** [HIG › Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-02 · Distinguish choices by style, not size
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD present a set of options as equally sized buttons and highlight the preferred one with a more prominent style.
- **Source:** [HIG › Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-03 · Custom buttons need a press state
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST give every custom button a visible press (highlighted) state.
- **Source:** [HIG › Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-04 · Never make a destructive button primary
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT assign the primary (default) role to a button that performs a destructive action, even if it’s the most likely choice.
- **Source:** [HIG › Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-05 · Assign semantic button roles
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD assign system roles — primary for the most likely nondestructive action, cancel for canceling, destructive for data-destroying actions — so the system applies accent or red styling and Return/Escape behavior.
- **Source:** [HIG › Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) · [GUIDELINES §13](../GUIDELINES.md#13-components)

## Modality, sheets, alerts, action sheets, popovers

### CMP-06 · Use modality only with clear benefit
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD present content modally only when it helps people focus or make a critical choice, keep modal tasks short with a single path, and title the modal view with its task.
- **Source:** [HIG › Modality](https://developer.apple.com/design/human-interface-guidelines/modality) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-07 · One modal presentation at a time
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT display more than one alert at a time, and SHOULD NOT stack sheets, popovers, or other modal views — dismiss one before presenting the next.
- **Source:** [HIG › Modality](https://developer.apple.com/design/human-interface-guidelines/modality) · [HIG › Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets) · [HIG › Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-08 · Always provide an obvious dismissal
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST give every modal view an obvious way to dismiss it using platform conventions, and confirm before dismissal would discard user-generated content.
- **Source:** [HIG › Modality](https://developer.apple.com/design/human-interface-guidelines/modality) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-09 · Pair Done with Cancel or Back
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD pair a sheet’s Done button with Cancel (or Back in multistep flows), place Cancel on the leading edge and Done on the trailing edge on iOS/iPadOS, and avoid showing Cancel, Done, and Back together.
- **Source:** [HIG › Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-10 · Resizable sheets behave like the system
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS
- **Check:** review
- **Rule:** SHOULD include a grabber in resizable sheets, support the medium detent for progressive disclosure when useful, support swipe to dismiss (confirming with an action sheet if changes are unsaved), and prefer page or form sheet styles on iPad.
- **Source:** [HIG › Sheets](https://developer.apple.com/design/human-interface-guidelines/sheets) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-11 · Use alerts sparingly
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD NOT show alerts that are merely informational, appear at launch, or confirm common undoable actions; reserve alerts for critical, actionable information.
- **Source:** [HIG › Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) · [HIG › Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-12 · Write specific, short alerts
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST limit alerts to a title, optional short message, and at most three buttons; the title MUST describe the situation specifically (never just “Error”) in no more than two lines.
- **Source:** [HIG › Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-13 · Title alert buttons with outcomes
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** hook
- **Rule:** SHOULD title alert buttons with one- or two-word verbs describing the result, use “OK” only in purely informational alerts, never use “Yes”/“No”, always title the cancel button “Cancel”, never make Cancel the default, and place the default button on the trailing side (or top of a stack).
- **Source:** [HIG › Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-14 · Use destructive styling precisely
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD apply the destructive style only to destructive actions people didn’t deliberately choose, and include a Cancel button whenever an alert offers a destructive action.
- **Source:** [HIG › Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-15 · Action sheets for choices about an intentional action
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, tvOS, watchOS
- **Check:** review
- **Rule:** SHOULD use an action sheet (confirmation dialog), not an alert or menu, for choices related to an action people initiated; anchor it to its source control, put destructive choices at the top, Cancel at the bottom, and avoid scrolling (watchOS: at most four buttons including Cancel).
- **Source:** [HIG › Action sheets](https://developer.apple.com/design/human-interface-guidelines/action-sheets) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-16 · Keep popovers small and single
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD use popovers for small amounts of related functionality, point them at their source, save work when they auto-close, never cascade them, never use them for warnings, and use a sheet instead in compact widths.
- **Source:** [HIG › Popovers](https://developer.apple.com/design/human-interface-guidelines/popovers) · [GUIDELINES §13](../GUIDELINES.md#13-components)

## Menus and lists

### CMP-17 · Organize menus predictably
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD label menu items with title-case verbs without articles, list frequent items first, group related items with separators, dim (not hide) unavailable items in regular menus, limit submenus to one level of about five items, and give icons to all items in a group or none.
- **Source:** [HIG › Menus](https://developer.apple.com/design/human-interface-guidelines/menus) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-18 · Context menus mirror the main UI
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** MUST make every context menu item available elsewhere in the main interface, and SHOULD keep context menus short and relevant, hide unavailable items, omit keyboard shortcuts, and list destructive items last with destructive styling.
- **Source:** [HIG › Context menus](https://developer.apple.com/design/human-interface-guidelines/context-menus) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-19 · Use list accessories correctly
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, visionOS
- **Check:** review
- **Rule:** SHOULD use a disclosure indicator to drill into a row, an info (detail disclosure) button only to reveal more information, and no alphabetical index alongside trailing accessories.
- **Source:** [HIG › Lists and tables](https://developer.apple.com/design/human-interface-guidelines/lists-and-tables) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-20 · Don’t nest same-axis scroll views
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD NOT place a scroll view inside another scroll view with the same orientation; horizontal-in-vertical (or the reverse) is fine.
- **Source:** [HIG › Scroll views](https://developer.apple.com/design/human-interface-guidelines/scroll-views) · [GUIDELINES §13](../GUIDELINES.md#13-components)

## Input controls

### CMP-21 · Secure sensitive text entry
- **Level:** MUST
- **Severity:** error
- **Platforms:** All
- **Check:** hook
- **Rule:** MUST use a secure text field for passwords and other sensitive data, and MUST NOT prefill password fields.
- **Source:** [HIG › Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields) · [HIG › Entering data](https://developer.apple.com/design/human-interface-guidelines/entering-data) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-22 · Configure text fields for their content
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, tvOS, visionOS
- **Check:** review
- **Rule:** SHOULD show the keyboard type that matches the content, size fields to the expected text, stack multiple fields vertically with consistent widths and logical tab order, validate at the right moment, and offer a Clear button on iOS.
- **Source:** [HIG › Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-23 · Use switches only in list rows (iOS)
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS
- **Check:** review
- **Rule:** SHOULD use the switch toggle style only in list rows; elsewhere use a button that behaves like a toggle, and make on/off states differ by more than color.
- **Source:** [HIG › Toggles](https://developer.apple.com/design/human-interface-guidelines/toggles) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-24 · Keep segmented controls tight
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, tvOS, visionOS
- **Check:** review
- **Rule:** SHOULD limit segmented controls to about five segments on iPhone (five to seven in wide layouts), keep segments equal in width, use text or images but not both, label with nouns, and never use them to switch app sections.
- **Source:** [HIG › Segmented controls](https://developer.apple.com/design/human-interface-guidelines/segmented-controls) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-25 · Pick the right selection control
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD use a pull-down button for short lists, a picker for medium-to-long lists with predictable ordering shown in context, and a list or table for very long lists.
- **Source:** [HIG › Pickers](https://developer.apple.com/design/human-interface-guidelines/pickers) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-26 · Sliders follow platform direction
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, visionOS, watchOS
- **Check:** review
- **Rule:** MUST NOT use a slider for audio volume on iOS/iPadOS (use the system volume view); SHOULD put minimum values on the leading (or bottom) side and maximum on the trailing (or top) side.
- **Source:** [HIG › Sliders](https://developer.apple.com/design/human-interface-guidelines/sliders) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-27 · Report progress honestly
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD prefer determinate progress, advance it accurately, keep indicators moving, use specific descriptions (not “Loading”), keep them in a consistent location, allow Cancel/Pause when safe, and never switch between a spinner and a bar.
- **Source:** [HIG › Progress indicators](https://developer.apple.com/design/human-interface-guidelines/progress-indicators) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### CMP-28 · Let people copy useful labels
- **Level:** MAY
- **Severity:** info
- **Platforms:** All
- **Check:** review
- **Rule:** MAY make useful label text (error messages, addresses, IP addresses) selectable so people can copy it.
- **Source:** [HIG › Labels](https://developer.apple.com/design/human-interface-guidelines/labels) · [GUIDELINES §13](../GUIDELINES.md#13-components)

# 14 · Platform rules (`PLT-*`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §16. Format and severities: [`README.md`](README.md).
> Rules here apply **in addition to** every cross-platform rule.

---

## iOS (iPhone)

### PLT-IOS-01 · Put frequent controls within reach
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS
- **Check:** review
- **Rule:** SHOULD place frequently used controls in the middle or bottom of the screen, limit on-screen controls, and support swipe to navigate back and swipe actions in list rows.
- **Source:** [HIG › Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-IOS-02 · Use device capabilities instead of data entry
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS
- **Check:** review
- **Rule:** SHOULD, with permission, use platform capabilities (Apple Pay, biometric authentication, location) rather than asking people to type information.
- **Source:** [HIG › Designing for iOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ios) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

## iPadOS

### PLT-IPAD-01 · Keep toolbar items clear of window controls
- **Level:** MUST
- **Severity:** error
- **Platforms:** iPadOS
- **Check:** review
- **Rule:** MUST make sure leading toolbar items move inward when windowed-mode window controls appear, so the controls never hide them.
- **Source:** [HIG › Windows](https://developer.apple.com/design/human-interface-guidelines/windows) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-IPAD-02 · Every menu bar command is also in the UI
- **Level:** MUST
- **Severity:** error
- **Platforms:** iPadOS
- **Check:** review
- **Rule:** MUST ensure every function in the iPadOS menu bar (including dynamic menu items) is also reachable through the app’s interface, since the menu bar is hidden until revealed.
- **Source:** [HIG › The menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-IPAD-03 · Support fluid window resizing
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iPadOS
- **Check:** review
- **Rule:** SHOULD support arbitrary window sizes with split views that reflow fluidly, minimize modality and full-screen transitions, and size density to viewing distance and input mode.
- **Source:** [HIG › Designing for iPadOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-ipados) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

## iPhone Duo

### PLT-DUO-01 · Build to resize
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS
- **Check:** review
- **Rule:** MUST lay out with size classes (compact on the outer display, regular on the inner), layout margins, and safe-area insets, with no fixed widths or display-specific dependencies.
- **Source:** [HIG › Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-DUO-02 · Same functionality across displays and poses
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS
- **Check:** review
- **Rule:** MUST keep functionality, element state, and access to controls the same across displays and device poses; MAY show one additional level of hierarchy on the inner display.
- **Source:** [HIG › Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-DUO-03 · Follow the system’s vertical controls
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** iOS
- **Check:** review
- **Rule:** SHOULD NOT override the default side placement of toolbars, tab bars, and navigation controls; keep relative control positions consistent across poses and account for asymmetric content areas.
- **Source:** [HIG › Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-DUO-04 · Keep important content out of reserved regions
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS
- **Check:** review
- **Rule:** SHOULD keep important elements clear of the cameras and the folding region (using `ReservedRegion` for custom UI), prefer containers that adapt to the fold and even-numbered grid columns, and avoid extreme layout changes as the device folds.
- **Source:** [HIG › Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-DUO-05 · Configure toolbar items for the vertical axis
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS
- **Check:** review
- **Rule:** SHOULD give every non-text toolbar item both a title and a symbol, put Back/Close first then prominent actions, set visibility priorities, group items with system groups instead of manual spacing, and use the system overflow menu (reserving the ellipsis for it).
- **Source:** [HIG › Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-DUO-06 · Keep navigation outside arrangement views
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS
- **Check:** review
- **Rule:** SHOULD use arrangement views (split or overlay) for two-view layouts and place navigation containers around them, not inside.
- **Source:** [HIG › Designing for iPhone Duo](https://developer.apple.com/design/human-interface-guidelines/designing-for-iphone-duo) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

## macOS

### PLT-MAC-01 · The menu bar holds every command
- **Level:** MUST
- **Severity:** error
- **Platforms:** macOS
- **Check:** review
- **Rule:** MUST list every app command in the menu bar in the standard order (App, File, Edit, Format, View, app-specific, Window, Help), always show the same items (disable rather than hide), and support standard shortcuts.
- **Source:** [HIG › The menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-MAC-02 · Every toolbar item is also a menu command
- **Level:** MUST
- **Severity:** error
- **Platforms:** macOS
- **Check:** review
- **Rule:** MUST make every toolbar item available as a menu bar command, because people can customize or hide the toolbar.
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-MAC-03 · Use system windows and their states
- **Level:** MUST
- **Severity:** error
- **Platforms:** macOS
- **Check:** review
- **Rule:** MUST use system window frames and the system main/key/inactive appearances; let people resize, move, and take windows full screen; and keep critical information out of bottom bars.
- **Source:** [HIG › Windows](https://developer.apple.com/design/human-interface-guidelines/windows) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-MAC-04 · Follow settings window conventions
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** macOS
- **Check:** review
- **Rule:** SHOULD open settings from the App menu’s Settings… item (⌘,), dim the minimize and zoom buttons, use a noncustomizable toolbar that shows the active pane, title the window with the pane name, and reopen the last pane.
- **Source:** [HIG › Settings](https://developer.apple.com/design/human-interface-guidelines/settings) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

### PLT-MAC-05 · Menu bar extras stay optional
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** macOS
- **Check:** review
- **Rule:** SHOULD represent a menu bar extra with a symbol, show a menu (not a popover) when clicked, let people decide whether to show it, and expose the same functionality elsewhere (e.g., a Dock menu).
- **Source:** [HIG › The menu bar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

## tvOS

### PLT-TV-01 · Embrace the focus system
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** tvOS
- **Check:** review
- **Rule:** SHOULD communicate focus with scale, parallax, and illumination — not color alone — and pad items so focused growth never overlaps content.
- **Source:** [HIG › Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos) · [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-TV-02 · Use layered images for the app icon
- **Level:** MUST
- **Severity:** error
- **Platforms:** tvOS
- **Check:** review
- **Rule:** MUST use a layered image (two to five layers, opaque background layer) for the tvOS app icon, and SHOULD use layered images for other focusable artwork.
- **Source:** [HIG › Images](https://developer.apple.com/design/human-interface-guidelines/images) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-TV-03 · Minimize typing and sign-in friction
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** tvOS
- **Check:** review
- **Rule:** SHOULD minimize text entry, make sign-in easy and infrequent, support shared sign-in and profile switching, and provide search suggestions.
- **Source:** [HIG › Designing for tvOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-tvos) · [HIG › Text fields](https://developer.apple.com/design/human-interface-guidelines/text-fields) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

## visionOS

### PLT-VIS-01 · Choose the minimum immersion
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** visionOS
- **Check:** review
- **Rule:** SHOULD use windows for familiar UI, volumes for bounded 3D content, and immersive spaces only for moments that need them, launching in the Shared Space.
- **Source:** [HIG › Designing for visionOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-visionos) · [HIG › Launching](https://developer.apple.com/design/human-interface-guidelines/launching) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-VIS-02 · Anchor content in space, not to the head
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** visionOS
- **Check:** review
- **Rule:** SHOULD NOT anchor content to the wearer’s head; keep important content centered in the field of view and support use with minimal physical movement.
- **Source:** [HIG › Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-VIS-03 · Size windows for their content
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** visionOS
- **Check:** review
- **Rule:** SHOULD pick an initial window size and shape that fits the content (default 1280×720 pt) with minimal empty space, set minimum and maximum sizes, and avoid opening too many windows.
- **Source:** [HIG › Windows](https://developer.apple.com/design/human-interface-guidelines/windows) · [HIG › Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-VIS-04 · Use depth sparingly and never on text
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** visionOS
- **Check:** review
- **Rule:** SHOULD NOT add depth to text; use depth to communicate hierarchy on large, important elements only, with accurate visual cues.
- **Source:** [HIG › Spatial layout](https://developer.apple.com/design/human-interface-guidelines/spatial-layout) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-VIS-05 · Keep bars where people expect them
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** visionOS
- **Check:** review
- **Rule:** SHOULD NOT create vertical toolbars or pull-down menus in toolbars; use the system bottom toolbar and vertical leading tab bar, ornaments for app controls, and adjacent windows (not ornaments) for supplemental content.
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

## watchOS

### PLT-WATCH-01 · Design for a glance
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** watchOS
- **Check:** review
- **Rule:** SHOULD support quick, single-screen interactions that finish in under a minute, with shallow navigation driven by the Digital Crown.
- **Source:** [HIG › Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-WATCH-02 · Avoid loading indicators
- **Level:** SHOULD NOT
- **Severity:** warning
- **Platforms:** watchOS
- **Check:** review
- **Rule:** SHOULD NOT show indeterminate loading indicators; display content immediately and notify people when longer tasks complete.
- **Source:** [HIG › Loading](https://developer.apple.com/design/human-interface-guidelines/loading) · [HIG › Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-WATCH-03 · Full-width primary buttons
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** watchOS
- **Check:** review
- **Rule:** SHOULD use full-width buttons for primary actions, equal heights for stacked and side-by-side buttons, and toolbar buttons for corner actions.
- **Source:** [HIG › Buttons](https://developer.apple.com/design/human-interface-guidelines/buttons) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-WATCH-04 · Complications, notifications, independence
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** watchOS
- **Check:** review
- **Rule:** SHOULD provide useful complications and actionable notifications, and let the app function independently of iPhone.
- **Source:** [HIG › Designing for watchOS](https://developer.apple.com/design/human-interface-guidelines/designing-for-watchos) · [GUIDELINES §16](../GUIDELINES.md#16-platform-guides)

### PLT-WATCH-05 · No settings bundle in the Settings app
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** watchOS
- **Check:** review
- **Rule:** MUST NOT rely on adding custom settings to the watchOS Settings app; place a few essential options at the bottom of the main view or in a More menu.
- **Source:** [HIG › Settings](https://developer.apple.com/design/human-interface-guidelines/settings) · [GUIDELINES §14](../GUIDELINES.md#14-patterns)

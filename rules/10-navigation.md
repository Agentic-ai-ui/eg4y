# 10 · Navigation: tab bars, sidebars, toolbars, search (`NAV`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §13.2–§13.5. Format and severities: [`README.md`](README.md).

---

### NAV-01 · Tab bars navigate; they never act
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iOS, iPadOS, tvOS, visionOS
- **Check:** review
- **Rule:** MUST NOT use a tab bar item to perform an action (compose, add, share); tab bars switch between top-level sections — use a toolbar for actions.
- **Source:** [HIG › Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-02 · Keep the tab bar visible
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, visionOS
- **Check:** review
- **Rule:** MUST keep the tab bar visible as people navigate within sections; only a modal view may cover it.
- **Source:** [HIG › Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-03 · Never disable or hide tabs
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iOS, iPadOS, tvOS, visionOS
- **Check:** review
- **Rule:** MUST NOT disable or hide tab bar items when their content is unavailable; show the section and explain why it’s empty.
- **Source:** [HIG › Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-04 · Keep tabs few and labeled
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, tvOS, visionOS
- **Check:** review
- **Rule:** SHOULD use only as many tabs as needed, avoid the overflow More tab, give each tab a single-word label and a filled SF Symbol, and default to five or fewer tabs when tabs are customizable.
- **Source:** [HIG › Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-05 · Reserve badges for critical information
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD show badges on tabs only for new or updated information that warrants attention.
- **Source:** [HIG › Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-06 · Use the platform’s navigation container
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD use the floating bottom tab bar on iPhone; a top tab bar (optionally `sidebarAdaptable`) on iPad; a sidebar or split view plus the menu bar on Mac; the vertical leading tab bar in visionOS windows; the top tab bar on tvOS; and lists or vertical pages on watchOS.
- **Source:** [HIG › Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) · [HIG › Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars) · [GUIDELINES §2](../GUIDELINES.md#2-cross-platform-design-sync)

### NAV-07 · Keep sidebars shallow and discoverable
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD show no more than two levels of hierarchy in a sidebar (add a content list in a split view for deeper data), let people customize and hide it with familiar interactions, and not hide it by default.
- **Source:** [HIG › Sidebars](https://developer.apple.com/design/human-interface-guidelines/sidebars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-08 · Highlight the path in split views
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, tvOS, visionOS
- **Check:** review
- **Rule:** SHOULD persistently highlight the selection in each pane that leads to the detail view, use split views only in regular width on iPhone, and support narrow, compact, and intermediate widths on iPad.
- **Source:** [HIG › Split views](https://developer.apple.com/design/human-interface-guidelines/split-views) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-09 · Use the standard Back and Close buttons
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, visionOS, watchOS
- **Check:** hook
- **Rule:** MUST NOT replace the standard Back and Close buttons with text labels reading “Back” or “Close”; use the system buttons and symbols (or custom versions that look and behave identically).
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-10 · Write useful, short titles
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** MUST NOT title windows or views with the app name; use a word or short phrase (under 15 characters) that describes the current content.
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-11 · One prominent toolbar action, on the trailing side
- **Level:** MUST
- **Severity:** error
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** MUST specify at most one prominent primary action (such as Done or Submit) in a toolbar and place it on the trailing side.
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-12 · Group toolbar items deliberately
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD group toolbar items by function and frequency into at most three groups, keep navigation and critical actions in distinct familiar groups, separate text-labeled buttons with fixed space, and not mix text and icons within one group.
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-13 · Prefer borderless system symbols in toolbars
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD use recognizable, borderless system symbols for toolbar items (text only for actions like Edit that symbols don’t represent well), and hide an item itself rather than its contents.
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-14 · Let the system manage toolbar overflow
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** iPadOS, macOS
- **Check:** review
- **Rule:** MUST NOT add a manual overflow menu in iPadOS or macOS toolbars (the system adds one), and SHOULD avoid layouts that overflow by default; add a More menu only for genuinely secondary actions.
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-15 · Use large titles on iOS
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS
- **Check:** review
- **Rule:** SHOULD use large titles that collapse into standard titles on scroll to keep people oriented.
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-16 · Place search where the platform expects it
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, tvOS, watchOS
- **Check:** review
- **Rule:** SHOULD place iOS search as a search tab (`Tab(role: .search)`), in a bottom toolbar when there’s room, in the top toolbar when bottom content must stay visible, or inline above the list it filters; on iPad and Mac, at the trailing end of the toolbar or top of the sidebar.
- **Source:** [HIG › Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields) · [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### NAV-17 · Make search responsive and scoped
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD use informative placeholder text, search as people type, show recent and suggested searches, rank the most relevant results first, and offer scope bars (defaulting to the broadest scope) and tokens.
- **Source:** [HIG › Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields) · [GUIDELINES §13](../GUIDELINES.md#13-components)

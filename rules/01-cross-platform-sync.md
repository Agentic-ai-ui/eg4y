# 01 · Cross-platform design sync (`SYNC`)

> Part of the **Apple Design Language** rule set — Created by Edison Augustin X.
> Derived from [`GUIDELINES.md`](../GUIDELINES.md) §2. Format and severities: [`README.md`](README.md).

One app, one identity, one information architecture — expressed in each platform’s idiom. These rules decide **what must stay identical** across iPhone, iPad, iPhone Duo, Mac, Apple TV, Apple Vision Pro, and Apple Watch.

---

### SYNC-01 · Keep functionality the same everywhere
- **Level:** MUST NOT
- **Severity:** error
- **Platforms:** All
- **Check:** review
- **Rule:** MUST NOT change the app’s functionality based on the space it occupies or the device it runs on; only the amount of functionality visible at once may change.
- **Do:** Move items into an overflow menu or a sidebar as space shrinks or grows.
- **Don't:** Drop a feature on iPad because the iPhone layout didn’t fit it.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §2](../GUIDELINES.md#2-cross-platform-design-sync)

### SYNC-02 · One glossary for every platform
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD maintain a single list of terms and use the same words for the same objects and actions on every platform.
- **Source:** [HIG › Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [GUIDELINES §2](../GUIDELINES.md#2-cross-platform-design-sync)

### SYNC-03 · Same color meanings everywhere
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD give each color (accent, status, destructive) the same meaning on every platform and use the same accent color.
- **Source:** [HIG › Color](https://developer.apple.com/design/human-interface-guidelines/color) · [GUIDELINES §2](../GUIDELINES.md#2-cross-platform-design-sync)

### SYNC-04 · Visually consistent app icon across platforms
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD provide a visually consistent app icon on every platform the app supports so people never mistake it for multiple apps.
- **Source:** [HIG › App icons](https://developer.apple.com/design/human-interface-guidelines/app-icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### SYNC-05 · Same symbols for the same actions
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD represent each action with the same standard SF Symbol on every platform (see ICN-02).
- **Source:** [HIG › Icons](https://developer.apple.com/design/human-interface-guidelines/icons) · [GUIDELINES §8](../GUIDELINES.md#8-iconography)

### SYNC-06 · Consistent toolbar groupings and placement
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD keep toolbar item groupings and their leading/center/trailing placement consistent across platforms.
- **Source:** [HIG › Toolbars](https://developer.apple.com/design/human-interface-guidelines/toolbars) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### SYNC-07 · Consistent search between iPad and Mac
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iPadOS, macOS
- **Check:** review
- **Rule:** SHOULD keep search placement and behavior as consistent as possible between the iPad and Mac versions of the app.
- **Source:** [HIG › Search fields](https://developer.apple.com/design/human-interface-guidelines/search-fields) · [GUIDELINES §13](../GUIDELINES.md#13-components)

### SYNC-08 · Adapt the container, keep the architecture
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD choose the platform’s own navigation container (tab bar, sidebar, menu bar, vertical tab bar, pages) while keeping the same sections and hierarchy, and keep the layout recognizable and familiar to the platform idiom when windows resize.
- **Source:** [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [HIG › Tab bars](https://developer.apple.com/design/human-interface-guidelines/tab-bars) · [GUIDELINES §2](../GUIDELINES.md#2-cross-platform-design-sync)

### SYNC-09 · Give every platform the same care
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** All
- **Check:** review
- **Rule:** SHOULD design, preview, and test on every supported platform and configuration (size classes, localizations, text sizes, appearances) instead of porting one platform’s layout.
- **Source:** [HIG › Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles) · [HIG › Layout](https://developer.apple.com/design/human-interface-guidelines/layout) · [GUIDELINES §2](../GUIDELINES.md#2-cross-platform-design-sync)

### SYNC-10 · Match context menu actions to swipe actions
- **Level:** SHOULD
- **Severity:** warning
- **Platforms:** iOS, iPadOS, macOS, visionOS
- **Check:** review
- **Rule:** SHOULD surface the same top actions in an item’s context menu as in its swipe actions.
- **Source:** [Adopting Liquid Glass](https://developer.apple.com/documentation/technologyoverviews/adopting-liquid-glass) · [GUIDELINES §13](../GUIDELINES.md#13-components)

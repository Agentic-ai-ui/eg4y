# Accessibility implementation

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> Source of truth: [`GUIDELINES.md` §11](../../../GUIDELINES.md#11-accessibility) · Rules: [`rules/08-accessibility.md`](../../../rules/08-accessibility.md), COL-06, MOT-02, TYP-01/02
> Apple sources: [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) · [VoiceOver](https://developer.apple.com/design/human-interface-guidelines/voiceover) · [Typography › Supporting Dynamic Type](https://developer.apple.com/design/human-interface-guidelines/typography)

An accessible interface is **intuitive, perceivable, and adaptable**. Build it in from the first screen; retrofitting is harder and usually incomplete.

## Contents
1. [Requirements at a glance](#1-requirements-at-a-glance)
2. [API map: SwiftUI · UIKit · AppKit · Web](#2-api-map) — plus [React · Vue · Svelte · React Native](#javascript-stacks)
3. [Dynamic Type and text scaling](#3-dynamic-type-and-text-scaling)
4. [VoiceOver: labels, structure, announcements](#4-voiceover)
5. [Reduce Motion, Reduce Transparency, Increase Contrast](#5-display-accommodations)
6. [Test procedure](#6-test-procedure)

---

## 1. Requirements at a glance

| Area | Requirement | Rule |
|---|---|---|
| Hit targets | ≥ 44×44 pt iOS/iPadOS/watchOS, 60×60 visionOS, 28×28 macOS, 66×66 tvOS | A11Y-01 |
| Spacing | ~12 pt around bezeled, ~24 pt around non-bezeled controls | A11Y-02 |
| Contrast | 4.5:1 (≤ 17 pt), 3:1 (≥ 18 pt or bold); both appearances; Increase Contrast scheme | COL-06 |
| Color | Never the only signal | COL-03 |
| Text size | Text styles + Dynamic Type; ≥ 200% enlargement (140% watchOS); never below platform minimum | TYP-01, TYP-02, A11Y-05 |
| Labels | Every key element, especially icon-only controls | A11Y-03 |
| Images | Describe meaningful; hide decorative | A11Y-04 |
| Gestures | On-screen alternative for every gesture | A11Y-06 |
| Keyboard | Full Keyboard Access; don’t override system shortcuts | A11Y-07, INP-05 |
| Structure | Titles, headings, grouping, order, announcements, rotor | A11Y-08 |
| Time | No auto-dismissing UI | A11Y-09 |
| Media | Start/stop controls; no uncontrolled autoplay; Dim Flashing Lights; captions | A11Y-10, A11Y-11 |
| Motion | Honor Reduce Motion | MOT-02 |
| Cognitive | Assistive Access: core features, one step per screen, double confirmation | A11Y-12 |

## 2. API map

| Need | SwiftUI | UIKit | AppKit | Web |
|---|---|---|---|---|
| Label | `.accessibilityLabel(_:)`, `Label`, `Button(_:systemImage:action:)` | `accessibilityLabel` | `setAccessibilityLabel(_:)` | Visible text, `aria-label` |
| Hint | `.accessibilityHint(_:)` | `accessibilityHint` | `setAccessibilityHelp(_:)` | `aria-describedby` |
| Value | `.accessibilityValue(_:)` | `accessibilityValue` | `setAccessibilityValue(_:)` | `aria-valuenow`/`aria-valuetext` |
| Traits / role | `.accessibilityAddTraits(.isHeader)` | `accessibilityTraits` | `setAccessibilityRole(_:)` | Semantic HTML, `role` |
| Heading | `.accessibilityHeading(.h1)` / `.isHeader` | `.header` trait | role | `<h1>`–`<h6>` |
| Group | `.accessibilityElement(children: .combine)` | `shouldGroupAccessibilityChildren` | — | Group in one element |
| Hide decorative | `Image(decorative:)`, `.accessibilityHidden(true)` | `isAccessibilityElement = false` | `setAccessibilityElement(false)` | `alt=""`, `aria-hidden="true"` |
| Custom action | `.accessibilityAction(named:_:)` | `accessibilityCustomActions` | `accessibilityCustomActions` | Visible buttons |
| Rotor | `accessibilityRotor` | `UIAccessibilityCustomRotor` | `NSAccessibilityCustomRotor` | Landmarks, headings |
| Announce change | `AccessibilityNotification.Announcement` (Accessibility framework) | `UIAccessibility.post(notification:argument:)` | `NSAccessibility.post(element:notification:)` | `aria-live` |
| Reduce Motion | `@Environment(\.accessibilityReduceMotion)` | `UIAccessibility.isReduceMotionEnabled` | `NSWorkspace.shared.accessibilityDisplayShouldReduceMotion` | `@media (prefers-reduced-motion: reduce)` |
| Reduce Transparency | `@Environment(\.accessibilityReduceTransparency)` | `UIAccessibility.isReduceTransparencyEnabled` | `accessibilityDisplayShouldReduceTransparency` | `prefers-reduced-transparency` (not in Safari — see web-adaptation) |
| Increase Contrast | `@Environment(\.colorSchemeContrast)` | `traitCollection.accessibilityContrast` | `accessibilityDisplayShouldIncreaseContrast` | `@media (prefers-contrast: more)` |
| Text size | Text styles, `@ScaledMetric`, `Font.custom(_:size:relativeTo:)`, `dynamicTypeSize.isAccessibilitySize` | `UIFont.preferredFont(forTextStyle:)`, `UIFontMetrics`, `adjustsFontForContentSizeCategory` | Text styles (no Dynamic Type) | `rem` units; WebKit `font: -apple-system-body` |
| Tooltip / help | `.help(_:)` | — | `toolTip` | `title` (supplementary only) |

### JavaScript stacks

The web columns apply to React, Next.js, Vue, and Svelte alike; the framework only changes how you bind attributes. React Native maps to UIKit accessibility on iOS. Verified code: [`react-recipes.md`](react-recipes.md), [`vue-svelte.md`](vue-svelte.md), [`react-native.md`](react-native.md).

| Need | React / Next.js | Vue / Svelte | React Native |
|---|---|---|---|
| Label | Visible text, `aria-label={…}`, `<label htmlFor>` | `:aria-label` / `aria-label={…}`, `<label for>` | `accessibilityLabel` |
| Role | Native element first (`<button>`, `<a>`, `<dialog>`), then `role` | same | `role` / `accessibilityRole` |
| State | `aria-checked`, `aria-current="page"`, `aria-expanded`, `disabled` | same | `accessibilityState`, `aria-checked`, `aria-selected` |
| Hide decorative | `aria-hidden="true"` on icons; `alt=""` | same | `aria-hidden`, `accessibilityElementsHidden` |
| Ids for relationships | `useId()` | `useId()` (Vue 3.5) / `$props.id()` (Svelte 5.20) | `nativeID` |
| Modal focus | `<dialog>` + `showModal()` | same | `Modal`, `accessibilityViewIsModal` |
| Announce change | `aria-live="polite"` region | same | `AccessibilityInfo.announceForAccessibility()` |
| Reduce Motion | `usePrefersReducedMotion()` (useSyncExternalStore) or CSS | `useMediaQuery` / `prefersReducedMotion` (svelte/motion) | `AccessibilityInfo.isReduceMotionEnabled()` |
| Increase Contrast | CSS via `tokens.css`; `usePrefersMoreContrast()` | CSS; `MediaQuery("prefers-contrast: more")` | Automatic with `PlatformColor` |
| Text size | `rem` text styles (`text.*` from tokens.ts) | same | `allowFontScaling` (default) + `dynamicTypeRamp` |
| Hit target | `min-height: var(--adl-control-size)` | same | `minHeight: 44`, `hitSlop` |

## 3. Dynamic Type and text scaling

```swift
struct TripRow: View {
    let trip: Trip
    @Environment(\.dynamicTypeSize) private var typeSize
    @ScaledMetric(relativeTo: .body) private var thumbnailSize = 44   // scales with text (TYP-09)

    var body: some View {
        let layout = typeSize.isAccessibilitySize
            ? AnyLayout(VStackLayout(alignment: .leading, spacing: 8))   // stack at AX sizes (LAY-04)
            : AnyLayout(HStackLayout(spacing: 12))
        layout {
            TripThumbnail(trip: trip).frame(width: thumbnailSize, height: thumbnailSize)
            VStack(alignment: .leading) {
                Text(trip.title).font(.headline)                        // text styles (TYP-01)
                Text(trip.dates).font(.subheadline).foregroundStyle(.secondary)
            }
        }
    }
}
```

- No fixed heights on text containers; let rows grow.
- Avoid `.lineLimit(1)` for meaningful text; if space is tight, allow more lines or open a detail view (TYP-08).
- Custom fonts: `Font.custom("Brand-Bold", size: 28, relativeTo: .title)` — scales and respects Bold Text (TYP-05).
- Keep primary content near the top at AX sizes; reduce columns (TYP-07).

## 4. VoiceOver

```swift
// Icon-only control: the Label title becomes the accessibility label (A11Y-03)
Button("Add to Favorites", systemImage: "star") { toggleFavorite() }
    .labelStyle(.iconOnly)

// Decorative image: excluded (A11Y-04)
Image(decorative: "confetti")

// Meaningful image: described
Image("trip-cover").accessibilityLabel("Sunset over Lisbon’s Alfama district")

// Card read as one element, with the primary action exposed
TripCard(trip: trip)
    .accessibilityElement(children: .combine)
    .accessibilityAction(named: "Share") { share(trip) }

// Section heading
Text("Upcoming").font(.title2).accessibilityAddTraits(.isHeader)
```

- Unique screen titles; accurate headings; group related elements; logical order (A11Y-08).
- Announce content changes that aren’t otherwise obvious (e.g., “3 results”).
- Charts: provide a concise summary and accessible interactions.
- visionOS: custom gestures don’t receive hand input while VoiceOver is on unless Direct Gesture mode is enabled.

## 5. Display accommodations

| Setting | Response |
|---|---|
| **Reduce Motion** | Tighten springs, track gestures directly, avoid z-axis depth animation, replace x/y/z transitions with fades, avoid blur animation, stop auto-playing repetitive motion (MOT-02) |
| **Reduce Transparency** | Glass and materials become more opaque; don’t rely on see-through content (GLS-06) |
| **Increase Contrast** | Use increased-contrast color variants; strengthen borders (COL-02, COL-06) |
| **Bold Text** | System and correctly implemented custom fonts thicken (TYP-05) |
| **Dim Flashing Lights** | Video playback mitigates flashes (A11Y-10) |
| **Differentiate Without Color** | Shapes/symbols/text carry meaning (COL-03) |

```swift
@Environment(\.accessibilityReduceMotion) private var reduceMotion
…
.transition(reduceMotion ? .opacity : .move(edge: .bottom).combined(with: .opacity))
.animation(reduceMotion ? nil : .spring, value: isPresented)
```

## 6. Test procedure

Run on every primary screen before presenting work (A11Y-13):

1. **Accessibility Inspector** audit — fix every warning.
2. **VoiceOver** — navigate the screen start to end; every control announces a useful label, role, and value; order matches visual order.
3. **Largest accessibility text size (AX5)** — nothing clipped, overlapped, or truncated without recourse; layout stacks.
4. **Increase Contrast + Dark Mode** — text meets contrast; custom colors switch.
5. **Reduce Transparency** — glass/material surfaces remain legible.
6. **Reduce Motion** — no large movement, zooms, or parallax.
7. **Full Keyboard Access** (iPad/Mac) — every control reachable and operable; visible focus.
8. **Voice Control** — “Show names” reveals meaningful names for every control.
9. **Grayscale / color filters** — status still distinguishable.

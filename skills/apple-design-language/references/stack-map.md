# Stack map: one design, every implementation surface

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> The rules are stack-neutral: they say **what** the interface must do. This page says **how**, per stack. Details and verified code: [SwiftUI](swiftui-recipes.md) · [React](react-recipes.md) · [HTML + CSS](html-css-recipes.md) · [Tailwind](tailwind.md) · [Vue and Svelte](vue-svelte.md) · [Next.js](nextjs.md) · [React Native](react-native.md) · web foundations in [`web-adaptation.md`](web-adaptation.md).

## Choosing the stack

Use the stack the project already uses. For a new project, choose by where the app runs:

| The app runs… | Choose | Why |
|---|---|---|
| Only on Apple platforms, native | **SwiftUI** (UIKit/AppKit where needed) | Full Liquid Glass, every system component, best accessibility |
| On iOS/iPadOS (and Android) from one JavaScript codebase | **React Native** (Expo) | Real UIKit views: native tab bar, alerts, switches, PlatformColor, Dynamic Type |
| In the browser, used on Apple devices | **React** (with **Next.js** for a full app), or **Vue**, **Svelte**, **plain HTML + CSS** | Web standards; the shared `tokens.css` + `components.css` give every web stack the same design |
| Styled with utilities | Any web stack + **Tailwind** (`tailwind.css` theme) | Same tokens, utility syntax |

Web pages can adopt the design language but not system chrome: no real Liquid Glass, no SF Symbols (license), no imitation status bars or alerts (BRD-03, BRD-04).

## Foundations

| Concept (rule) | SwiftUI | React / Next.js | HTML + CSS | Vue / Svelte | Tailwind | React Native |
|---|---|---|---|---|---|---|
| System colors (COL-01) | `.blue`, `Color(.label)` | `color.blue` from `tokens.ts` | `var(--adl-blue)` | `var(--adl-blue)` | `text-blue`, `bg-background` | `systemColor("blue")` → `PlatformColor` |
| Custom color, 4 variants (COL-02) | Asset-catalog Color Set | Add to `tokens.css` media blocks | same | same | Add to `@theme` via a token | `DynamicColorIOS({ light, dark, highContrast… })` |
| Follow appearance (COL-07) | Default; no `.preferredColorScheme` | `color-scheme: light dark` | `<meta name="color-scheme">` | same | Default `dark:` behavior | Default; no `Appearance.setColorScheme` |
| Increase Contrast (COL-06) | Automatic with system colors | `prefers-contrast: more` (in tokens) | same | same | `contrast-more:` | Automatic with `PlatformColor` |
| Text styles (TYP-01) | `.font(.body)` | `text.body` / `.adl-text-body` | `.adl-text-*`, `font: -apple-system-body` | same | `text-body` | `textStyles.body` + `dynamicTypeRamp` |
| Minimum size (TYP-02) | 11 pt iOS | 11 px | 11 px | 11 px | ≥ `text-caption2` | 11 pt |
| System font (TYP-04) | Default | `var(--adl-font-text)` | `-apple-system, system-ui` | same | `font-sans` | Leave `fontFamily` unset |
| Layout from space (LAY-01) | Size classes, `ViewThatFits` | Container/media queries | same | same | `@3xl:` container variants | `useWindowDimensions()` |
| Safe areas (LAY-02) | Automatic; `.safeAreaInset` | `env(safe-area-inset-*)` + `viewport-fit=cover` | same | same | `pb-[env(safe-area-inset-bottom)]` | `contentInsetAdjustmentBehavior`, safe-area-context |
| Hit targets (A11Y-01) | `.frame(minWidth: 44, minHeight: 44)` | `min-height: var(--adl-control-size)` | same | same | `min-h-control` | `minHeight: 44`, `hitSlop` |
| Labels (A11Y-03) | `.accessibilityLabel` | `aria-label` | `aria-label`, visible text | same | same | `accessibilityLabel` |
| Reduce Motion (MOT-02) | `@Environment(\.accessibilityReduceMotion)` | `usePrefersReducedMotion()` | `prefers-reduced-motion` | `useMediaQuery` / `prefersReducedMotion` | `motion-reduce:` | `AccessibilityInfo.isReduceMotionEnabled()` |
| Glass (LAY-08, GLS-01) | `.glassEffect()`, system bars | `.adl-glass` (approximation) on bars only | same | same | `adl-glass` | Native bars; `GlassView` (iOS 26) |
| Icons (BRD-03) | SF Symbols | Open-licensed set (Lucide, Phosphor…) | same | same | same | `SymbolView` (SF on iOS, Material elsewhere) |

## Components

| Component (rule) | SwiftUI | Web (React, Vue, Svelte, HTML) | React Native |
|---|---|---|---|
| Tab bar ⇄ sidebar (NAV-01, NAV-06) | `TabView` + `.tabViewStyle(.sidebarAdaptable)` | `<nav>` + links + `aria-current="page"`, `.adl-nav` (container query) | Expo Router native tabs |
| Navigation stack, large title (NAV-15) | `NavigationStack`, `.navigationTitle` | Router + `.adl-large-title` | Native stack, `headerLargeTitleEnabled` |
| Toolbar (NAV-11) | `.toolbar { ToolbarItem(placement:) }` | `<header class="adl-toolbar">` | Stack `headerRight` / `headerLeft` |
| Button styles (CMP-01 – CMP-04) | `.buttonStyle(.borderedProminent / .bordered / .glass)` | `.adl-button--prominent / (bordered) / --plain` | `Pressable` + tokens |
| Destructive action (CMP-14) | `Button(role: .destructive)` | Red text row or hairline button | `Alert` / `ActionSheetIOS` destructive style |
| List (CMP-19) | `List { Section }.listStyle(.insetGrouped)` | `.adl-grouped`, `.adl-list`, `.adl-list__row` | `ScrollView` + rows, or `SectionList` |
| Switch (CMP-23) | `Toggle` | `input[type=checkbox][role=switch]` in a label row | `Switch` (UISwitch) |
| Segmented control (CMP-24) | `Picker(...).pickerStyle(.segmented)` | Radios in a `fieldset`, `.adl-segmented` (tabs pattern if it switches views) | `@react-native-segmented-control/segmented-control` or buttons with `role="radio"` |
| Text field / secure field (CMP-21, CMP-22) | `TextField`, `SecureField`, `.textContentType` | `<input>` with `type`, `autocomplete`, `.adl-field` | `TextInput` with `textContentType`, `secureTextEntry` |
| Sheet (CMP-07 – CMP-10) | `.sheet`, `.presentationDetents` | `<dialog>` + `showModal()`, `.adl-sheet` | Stack `presentation: "formSheet"` or `Modal` |
| Alert (CMP-11 – CMP-13) | `.alert` | `<dialog role="alertdialog">`, `.adl-alert` | `Alert.alert` |
| Menu (CMP-16, CMP-17) | `Menu` | `[popover]` + `popovertarget`, `.adl-menu` | `ActionSheetIOS`, or a native menu library |
| Search (NAV-16) | `.searchable` | `<search>` + `input[type=search]` | Native tabs search role, `headerSearchBarOptions` |
| Empty state (NAV-03) | `ContentUnavailableView` | `.adl-empty` | Text + button in a centered `View` |

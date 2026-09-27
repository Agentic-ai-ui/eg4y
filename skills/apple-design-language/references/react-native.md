# React Native recipes

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> React Native 0.87 · Expo SDK 57 (expo-router, expo-symbols, expo-glass-effect) · Tokens: [`../assets/tokens.native.ts`](../assets/tokens.native.ts) · Rules and principles are the same as for SwiftUI.

React Native renders **real UIKit views** on iPhone and iPad, so it can feel native in ways a web page can’t: system colors that adapt to Increase Contrast, Dynamic Type ramps, the native tab bar and navigation bar with Liquid Glass, SF Symbols, UISwitch, and system alerts. Prefer those native pieces over JavaScript re-creations — the same “system components first” rule as SwiftUI (SYS-01). Every recipe below was type-checked (TypeScript strict) against React Native 0.87 and the Expo SDK 57 packages and passes the package’s checker; run it on a device or simulator to see the native rendering.

## Contents
1. [Setup](#1-setup)
2. [Color](#2-color)
3. [Typography](#3-typography)
4. [Navigation: native tabs and stacks](#4-navigation-native-tabs-and-stacks)
5. [Lists and rows](#5-lists-and-rows)
6. [Controls, alerts, and action sheets](#6-controls-alerts-and-action-sheets)
7. [Liquid Glass and symbols](#7-liquid-glass-and-symbols)
8. [Accessibility](#8-accessibility)
9. [A complete screen](#9-a-complete-screen)
10. [Anti-patterns → fixes](#10-anti-patterns--fixes)

---

## 1. Setup

Copy [`tokens.native.ts`](../assets/tokens.native.ts) to `theme/tokens.native.ts`. It exports:

| Export | What it is |
|---|---|
| `systemColor(name, scheme?)` | `PlatformColor` for the UIKit system color on iOS; the HIG hex for light or dark elsewhere |
| `useSystemColors()` | All colors for the current appearance |
| `textStyles`, `dynamicTypeRamp` | iOS text styles (Large default size) and the matching Dynamic Type ramp for each |
| `minimumHitTarget`, `minimumTextSize` | 44 pt and 11 pt (A11Y-01, TYP-02) |

Install the native pieces with `npx expo install expo-router expo-symbols expo-glass-effect react-native-safe-area-context`. React Native’s own `SafeAreaView` is deprecated; use `react-native-safe-area-context`, or let native navigation inset scroll views (`contentInsetAdjustmentBehavior="automatic"`).

## 2. Color

On iOS, `systemColor("blue")` is `PlatformColor("systemBlue")` — the live UIKit color, including its dark and increased-contrast variants, with no re-render needed (COL-01, COL-02). Semantic colors such as `label`, `secondaryLabel`, `systemBackground`, and `separator` come from UIKit the same way; Apple doesn’t publish their values, so other platforms get neutral fallbacks built from published grays.

For brand colors, give all four variants — the React Native equivalent of an asset-catalog Color Set:

```ts
import { DynamicColorIOS, Platform, type ColorValue } from "react-native";

// A brand color with all four variants, like an asset-catalog Color Set (COL-02).
// Check every variant for 4.5:1 against the backgrounds it sits on (COL-06).
export const brandTint: ColorValue =
  Platform.OS === "ios"
    ? DynamicColorIOS({
        light: "#8A3FFC",
        dark: "#A56EFF",
        highContrastLight: "#6929C4",
        highContrastDark: "#BE95FF",
      })
    : "#8A3FFC";
```

Follow the system appearance: don’t call `Appearance.setColorScheme()` to force light or dark (COL-07).

## 3. Typography

React Native scales text with the system text size by default (`allowFontScaling` is `true`). `dynamicTypeRamp` makes each style scale along its own iOS Dynamic Type curve, so a caption and a title grow the way they do in native apps (TYP-01). Keep text at 11 pt or larger (TYP-02), avoid light weights (TYP-03), and never ship SF Pro files — `fontFamily` left unset *is* the system font (TYP-04). Don’t cap `maxFontSizeMultiplier` on body text; people who enlarge text need it (A11Y-05).

```tsx
<Text style={[textStyles.headline, { color: systemColor("label") }]} dynamicTypeRamp={dynamicTypeRamp.headline}>
  Reading Now
</Text>
```

## 4. Navigation: native tabs and stacks

Expo Router’s native tabs render the system tab bar (`UITabBarController` on iOS), so the floating Liquid Glass tab bar, the search tab, badges, and accessibility come from iOS. SF Symbols go in `sf`, Material Symbols in `md` for Android. SDK 54–57 import from `expo-router/unstable-native-tabs`; SDK 58 renames it to `expo-router/native-tabs`. On iPad the system shows its tab bar at the top; Expo’s documentation doesn’t describe a sidebar mode, so for a sidebar-first iPad or Mac layout, check the current docs before promising one (NAV-06).

```tsx
import { NativeTabs } from "expo-router/unstable-native-tabs"; // "expo-router/native-tabs" from SDK 58

// Native tab bar: UITabBarController on iOS, so Liquid Glass, Dynamic Type, and VoiceOver come from the system.
// SF Symbols on iOS (`sf`), Material Symbols elsewhere (`md`). Tabs navigate; they never act (NAV-01).
export default function RootLayout() {
  return (
    <NativeTabs>
      <NativeTabs.Trigger name="index">
        <NativeTabs.Trigger.Icon sf="house.fill" md="home" />
        <NativeTabs.Trigger.Label>Home</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="library">
        <NativeTabs.Trigger.Icon sf="books.vertical.fill" md="library_books" />
        <NativeTabs.Trigger.Label>Library</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="search" role="search">
        <NativeTabs.Trigger.Label>Search</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>
      <NativeTabs.Trigger name="settings">
        <NativeTabs.Trigger.Icon sf="gearshape.fill" md="settings" />
        <NativeTabs.Trigger.Label>Settings</NativeTabs.Trigger.Label>
      </NativeTabs.Trigger>
    </NativeTabs>
  );
}
```

Each tab hosts a native stack. `headerLargeTitleEnabled` (the older `headerLargeTitle` is deprecated) gives the collapsing large title; leave the header background and blur alone so iOS draws its glass and scroll edge effect (NAV-15, GLS-04).

```tsx
import { Stack } from "expo-router";

// Native navigation stack with a large title that collapses on scroll (NAV-15).
// Leave the header background alone so the system renders its glass and scroll edge effect (GLS-04).
export default function LibraryLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: "Library", headerLargeTitleEnabled: true }} />
    </Stack>
  );
}
```

## 5. Lists and rows

Rows are at least 44 pt tall, use semantic colors and Dynamic Type, and announce as links or buttons (A11Y-01, A11Y-03, CMP-19).

```tsx
import { Pressable, StyleSheet, Text, View } from "react-native";
import { SymbolView } from "expo-symbols";
import { dynamicTypeRamp, minimumHitTarget, systemColor, textStyles } from "../theme/tokens.native";

/** A navigation row: 44 pt minimum height, system colors, Dynamic Type, a VoiceOver-friendly role. */
export function LinkRow({ title, value, onPress }: { title: string; value?: string; onPress: () => void }) {
  return (
    <Pressable
      role="link"
      accessibilityLabel={value ? `${title}, ${value}` : title}
      onPress={onPress}
      style={({ pressed }) => [styles.row, pressed && { backgroundColor: systemColor("systemGray5") }]}
    >
      <Text style={[textStyles.body, styles.title]} dynamicTypeRamp={dynamicTypeRamp.body}>{title}</Text>
      {value ? (
        <Text style={[textStyles.body, { color: systemColor("secondaryLabel") }]} dynamicTypeRamp={dynamicTypeRamp.body}>
          {value}
        </Text>
      ) : null}
      <SymbolView
        name={{ ios: "chevron.forward", android: "chevron_right", web: "chevron_right" }}
        size={14}
        tintColor={systemColor("systemGray3")}
      />
    </Pressable>
  );
}

/** A destructive action row, such as “Delete All” (CMP-14). */
export function DestructiveRow({ title, onPress }: { title: string; onPress: () => void }) {
  return (
    <Pressable role="button" onPress={onPress} style={styles.row}>
      <Text style={[textStyles.body, { color: systemColor("red") }]} dynamicTypeRamp={dynamicTypeRamp.body}>{title}</Text>
    </Pressable>
  );
}

export function ListSection({ header, children }: { header?: string; children: React.ReactNode }) {
  return (
    <View style={styles.section}>
      {header ? (
        <Text role="heading" style={[textStyles.footnote, styles.header]} dynamicTypeRamp={dynamicTypeRamp.footnote}>
          {header}
        </Text>
      ) : null}
      <View style={styles.group}>{children}</View>
    </View>
  );
}

const styles = StyleSheet.create({
  section: { marginBottom: 24 },
  header: { paddingHorizontal: 16, paddingBottom: 6, fontWeight: "600", color: systemColor("secondaryLabel") },
  group: { borderRadius: 12, overflow: "hidden", backgroundColor: systemColor("secondaryBackground") },
  row: {
    minHeight: minimumHitTarget,
    flexDirection: "row",
    alignItems: "center",
    gap: 12,
    paddingHorizontal: 16,
    paddingVertical: 10,
  },
  title: { flex: 1, color: systemColor("label") },
});
```

## 6. Controls, alerts, and action sheets

- **Switch:** React Native’s `Switch` is `UISwitch` on iOS — use it in list rows (CMP-23) and give it an `accessibilityLabel`.
- **Alerts:** `Alert.alert` presents a native alert. Buttons take `style: "cancel" | "destructive" | "default"` and `isPreferred` on iOS; title them with verbs and use “Cancel” (CMP-12, CMP-13).
- **Action sheets:** `ActionSheetIOS.showActionSheetWithOptions` with `cancelButtonIndex` and `destructiveButtonIndex` for choices about an intentional action (CMP-15).
- **Hit targets:** `hitSlop` extends a small visual to 44 pt without changing layout (A11Y-01).

## 7. Liquid Glass and symbols

Native tabs, navigation bars, and alerts adopt Liquid Glass automatically on iOS 26. For a custom floating control, `GlassView` from `expo-glass-effect` renders the system effect on iOS 26 and falls back to a plain view elsewhere — use it only for controls in the functional layer, never for content, and never stack glass on glass (GLS-01, GLS-03, LAY-08).

```tsx
import { Pressable, StyleSheet, View } from "react-native";
import { GlassView, isGlassEffectAPIAvailable } from "expo-glass-effect";
import { SymbolView, type SFSymbol } from "expo-symbols";
import { minimumHitTarget, systemColor } from "../theme/tokens.native";

/**
 * A floating control in the Liquid Glass layer (iOS 26+), with a plain fallback elsewhere.
 * Glass belongs to controls and navigation only — never to content (GLS-01) — and never stacks on glass (GLS-03).
 */
export function FloatingButton({ label, symbol, onPress }: { label: string; symbol: SFSymbol; onPress: () => void }) {
  const Surface = isGlassEffectAPIAvailable() ? GlassView : View;
  return (
    <Surface style={[styles.surface, !isGlassEffectAPIAvailable() && { backgroundColor: systemColor("secondaryBackground") }]}>
      <Pressable role="button" accessibilityLabel={label} onPress={onPress} hitSlop={8} style={styles.button}>
        <SymbolView name={{ ios: symbol, android: "add", web: "add" }} size={22} tintColor={systemColor("blue")} />
      </Pressable>
    </Surface>
  );
}

const styles = StyleSheet.create({
  surface: { borderRadius: 999, overflow: "hidden" },
  button: { minWidth: minimumHitTarget + 8, minHeight: minimumHitTarget + 8, alignItems: "center", justifyContent: "center" },
});
```

`SymbolView` from `expo-symbols` draws SF Symbols on iOS — permitted, because the app runs on an Apple platform (Xcode and Apple SDKs Agreement §2.10) — and Material Symbols on Android and web. Never use SF Symbols in your app icon or logo (BRD-03).

## 8. Accessibility

| Need | React Native | Rule |
|---|---|---|
| Name and role | `accessibilityLabel`, `role` (or `accessibilityRole`) | A11Y-03 |
| State | `accessibilityState` / `aria-checked`, `aria-selected`, `aria-disabled` | A11Y-03 |
| Hide decoration | `accessibilityElementsHidden` / `aria-hidden` | A11Y-04 |
| Reduce Motion | `AccessibilityInfo.isReduceMotionEnabled()` + `reduceMotionChanged` (hook below) | MOT-02 |
| Reduce Transparency | `AccessibilityInfo.isReduceTransparencyEnabled()` | GLS-06 |
| Bold Text | `AccessibilityInfo.isBoldTextEnabled()` | TYP-01 |
| Announcements | `AccessibilityInfo.announceForAccessibility()` | A11Y-03 |
| Modal focus | `accessibilityViewIsModal` / `aria-modal` on custom overlays | CMP-08 |
| Large Content Viewer | `accessibilityShowsLargeContentViewer` on icon-only bar items | A11Y-05 |

```ts
import { useEffect, useState } from "react";
import { AccessibilityInfo } from "react-native";

/** The system Reduce Motion setting, kept up to date (MOT-02). */
export function useReduceMotion(): boolean {
  const [reduced, setReduced] = useState(false);
  useEffect(() => {
    AccessibilityInfo.isReduceMotionEnabled().then(setReduced);
    const sub = AccessibilityInfo.addEventListener("reduceMotionChanged", setReduced);
    return () => sub.remove();
  }, []);
  return reduced;
}
```

## 9. A complete screen

```tsx
import { useState } from "react";
import { Alert, ScrollView, StyleSheet, Switch, Text, View } from "react-native";
import { router } from "expo-router";
import { DestructiveRow, LinkRow, ListSection } from "../../components/ListRow";
import { FloatingButton } from "../../components/FloatingButton";
import { useReduceMotion } from "../../components/useReduceMotion";
import { dynamicTypeRamp, minimumHitTarget, systemColor, textStyles } from "../../theme/tokens.native";

export default function LibraryScreen() {
  const [sync, setSync] = useState(true);
  const reduceMotion = useReduceMotion();

  // A native alert: specific title, verb buttons, "Cancel" to cancel, destructive style (CMP-12 – CMP-14).
  const confirmDeleteAll = () =>
    Alert.alert("Delete all books?", "This removes 128 books from this device.", [
      { text: "Cancel", style: "cancel" },
      { text: "Delete", style: "destructive", onPress: () => {} },
    ]);

  return (
    <View style={styles.screen}>
      {/* "automatic" lets the large title and tab bar inset the content (LAY-02) */}
      <ScrollView contentInsetAdjustmentBehavior="automatic" contentContainerStyle={styles.content}>
        <ListSection header="Collections">
          <LinkRow title="All Books" value="128" onPress={() => router.push("/library/all")} />
          <LinkRow title="Reading Now" value="3" onPress={() => router.push("/library/reading")} />
        </ListSection>
        <ListSection header="Options">
          <View style={styles.switchRow}>
            <Text style={[textStyles.body, styles.flex]} dynamicTypeRamp={dynamicTypeRamp.body}>
              iCloud Sync
            </Text>
            <Switch value={sync} onValueChange={setSync} accessibilityLabel="iCloud Sync" />
          </View>
        </ListSection>
        <ListSection>
          <DestructiveRow title="Delete All" onPress={confirmDeleteAll} />
        </ListSection>
        {reduceMotion ? null : <Text style={styles.hint}>Tip: pull down to refresh.</Text>}
      </ScrollView>
      <View style={styles.floating}>
        <FloatingButton label="Add Book" symbol="plus" onPress={() => router.push("/library/new")} />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, backgroundColor: systemColor("groupedBackground") },
  content: { padding: 16 },
  switchRow: { minHeight: minimumHitTarget, flexDirection: "row", alignItems: "center", paddingHorizontal: 16, paddingVertical: 8 },
  flex: { flex: 1, color: systemColor("label") },
  hint: { ...textStyles.footnote, color: systemColor("secondaryLabel"), paddingHorizontal: 16 },
  floating: { position: "absolute", right: 16, bottom: 16 },
});
```

## 10. Anti-patterns → fixes

| Don’t | Do | Rule |
|---|---|---|
| `color: "#007AFF"` | `systemColor("blue")` or a `DynamicColorIOS` brand color | COL-01, COL-02 |
| A JavaScript tab bar that imitates iOS | Native tabs (`expo-router` native tabs) | SYS-01, BRD-04 |
| `allowFontScaling={false}` or a tight `maxFontSizeMultiplier` | Let Dynamic Type scale text | TYP-01, A11Y-05 |
| `fontFamily: "SF Pro"` with bundled font files | Leave `fontFamily` unset | TYP-04 |
| Choosing layouts with `Platform.isPad` | `useWindowDimensions()` width — windows resize on iPad and Mac | LAY-01 |
| `Animated` motion with no Reduce Motion branch | `useReduceMotion()`; cross-fade instead | MOT-02 |
| `GlassView` behind a list or card | Plain background; glass only for floating controls | GLS-01 |
| A custom modal `View` without `accessibilityViewIsModal` | Native `Modal`, a stack modal, or the prop | CMP-08 |

# SwiftUI recipes

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> Rules are cited inline by ID ([`rules/`](../../../rules/README.md)). API names were checked against Apple’s published declarations (September 2026); the snippets weren’t compiled in this repository. Liquid Glass APIs require the 26 SDKs — guard with `if #available` when supporting earlier releases.

Each recipe shows the idiomatic, rule-compliant way to build a common screen element. Prefer these patterns over hand-rolled equivalents.

## Contents
1. [App structure that adapts to every platform](#1-app-structure)
2. [Adaptive layout without device checks](#2-adaptive-layout)
3. [Typography and color](#3-typography-and-color)
4. [Lists, swipe actions, context menus, empty states](#4-lists)
5. [Editing in a sheet with safe dismissal](#5-editing-sheet)
6. [Alerts and confirmation dialogs](#6-alerts-and-confirmation-dialogs)
7. [Forms and secure input](#7-forms)
8. [Feedback: haptics and symbol effects](#8-feedback)
9. [Mac: menu bar commands and keyboard shortcuts](#9-mac-commands)
10. [visionOS specifics](#10-visionos)
11. [Anti-pattern → fix](#11-anti-pattern--fix)

---

## 1. App structure

```swift
@main
struct TripsApp: App {
    var body: some Scene {
        WindowGroup {
            RootView()
        }
        #if os(macOS)
        .commands { TripCommands() }        // every command in the menu bar (PLT-MAC-01), see §9
        #endif
        #if os(macOS)
        Settings { SettingsView() }         // App menu › Settings… (⌘,) (PLT-MAC-04)
        #endif
    }
}

struct RootView: View {
    var body: some View {
        TabView {                                                          // NAV-06
            Tab("Trips", systemImage: "suitcase") { TripsView() }
            Tab("Explore", systemImage: "map") { ExploreView() }
            Tab("Saved", systemImage: "bookmark") { SavedView() }
            Tab(role: .search) { SearchView() }                            // NAV-16
        }
        .tabViewStyle(.sidebarAdaptable)   // tab bar on iPhone, tab bar ⇄ sidebar on iPad, sidebar on Mac
    }
}
```

One structure serves iPhone, iPad, iPhone Duo, Mac, and visionOS; the system picks the container (SYNC-08). Same tabs, labels, and symbols everywhere (SYNC-02, SYNC-05).

## 2. Adaptive layout

```swift
struct TripDetail: View {
    @Environment(\.horizontalSizeClass) private var widthClass   // LAY-01: size class, not device

    var body: some View {
        ScrollView {
            if widthClass == .compact {
                VStack(alignment: .leading, spacing: 16) { summary; itinerary }
            } else {
                HStack(alignment: .top, spacing: 24) { summary; itinerary }
            }
        }
        .navigationTitle("Lisbon")                                // concise title (NAV-10)
    }
    private var summary: some View { TripSummary() }
    private var itinerary: some View { Itinerary() }
}

// Or let SwiftUI choose the first layout that fits — works for Dynamic Type too (LAY-04)
ViewThatFits(in: .horizontal) {
    HStack { primaryActions }
    VStack(alignment: .leading) { primaryActions }
}
```

Never branch on `UIDevice.current.userInterfaceIdiom`, `UIScreen.main.bounds`, or orientation to choose layouts (LAY-01, LAY-03).

## 3. Typography and color

```swift
VStack(alignment: .leading, spacing: 4) {
    Text("Lisbon Trip").font(.title2).bold()                  // text style + symbolic trait (TYP-01)
    Text("May 12 – 18").font(.subheadline)
        .foregroundStyle(.secondary)                          // semantic hierarchy (COL-01)
    Text("Brand headline").font(.custom("BrandSerif-Bold", size: 28, relativeTo: .title)) // TYP-05
}
.tint(.blue)          // app accent via system color; custom accent belongs in the asset catalog (COL-01, COL-02)
```

- Colors: `Color.primary/.secondary`, `.foregroundStyle(.secondary)`, system colors (`.red`, `.blue`…), `Color(.systemBackground)` / `Color(uiColor: .secondarySystemGroupedBackground)` on iOS, and named asset-catalog Color Sets with light/dark/high-contrast variants (COL-02). Never `Color(red:green:blue:)` literals in views (COL-01).
- Don’t force appearance: no app-wide `.preferredColorScheme(_:)` (COL-07).
- Avoid `.fontWeight(.ultraLight/.thin/.light)` for UI text (TYP-03); never `.font(.system(size:))` for body copy (TYP-01).

## 4. Lists

```swift
struct TripsView: View {
    @State private var trips: [Trip] = []

    var body: some View {
        NavigationStack {
            List {
                ForEach(trips) { trip in
                    NavigationLink(value: trip) { TripRow(trip: trip) }   // disclosure indicator drills in (CMP-19)
                        .swipeActions {
                            Button("Delete", systemImage: "trash", role: .destructive) { delete(trip) }
                            Button("Share", systemImage: "square.and.arrow.up") { share(trip) }
                        }
                        .contextMenu {                                     // same top actions as swipe (SYNC-10)
                            Button("Share", systemImage: "square.and.arrow.up") { share(trip) }
                            Button("Duplicate", systemImage: "plus.square.on.square") { duplicate(trip) }
                            Button("Delete", systemImage: "trash", role: .destructive) { delete(trip) } // last (CMP-18)
                        }
                }
            }
            .overlay {
                if trips.isEmpty {
                    ContentUnavailableView {                               // empty state with next step (WRT-08)
                        Label("No Trips Yet", systemImage: "suitcase")
                    } description: {
                        Text("Trips you create or are invited to appear here.")
                    } actions: {
                        Button("New Trip") { createTrip() }
                    }
                }
            }
            .refreshable { await reload() }                               // plus automatic refresh (CMP-27)
            .navigationTitle("Trips")
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("New Trip", systemImage: "plus") { createTrip() }   // labeled icon (A11Y-03)
                }
            }
            .navigationDestination(for: Trip.self) { TripDetail(trip: $0) }
        }
    }
}
```

Deleting from a list is common and undoable — don’t add a confirmation alert (CMP-11); support undo instead (SYS-02).

## 5. Editing sheet

```swift
struct TripsScreen: View {
    @State private var isEditing = false
    @State private var draft = TripDraft()
    @State private var confirmDiscard = false

    var body: some View {
        TripsView()
            .sheet(isPresented: $isEditing) {
                NavigationStack {
                    TripForm(draft: $draft)
                        .navigationTitle("Edit Trip")
                        .toolbar {
                            ToolbarItem(placement: .cancellationAction) {
                                Button("Cancel", role: .cancel) {                 // CMP-09
                                    if draft.hasChanges { confirmDiscard = true } else { isEditing = false }
                                }
                            }
                            ToolbarItem(placement: .confirmationAction) {
                                Button("Done") { save(); isEditing = false }      // single prominent action (NAV-11)
                            }
                        }
                        .confirmationDialog("Discard your changes?",               // action sheet for intentional action (CMP-15)
                                            isPresented: $confirmDiscard, titleVisibility: .visible) {
                            Button("Discard Changes", role: .destructive) { isEditing = false }
                            Button("Keep Editing", role: .cancel) { }
                        }
                }
                .presentationDetents([.medium, .large])                          // CMP-10
                .presentationDragIndicator(.visible)
                .interactiveDismissDisabled(draft.hasChanges)                    // protect user content (CMP-08)
            }
    }
}
```

## 6. Alerts and confirmation dialogs

```swift
.alert("Delete “\(trip.name)”?", isPresented: $confirmDelete) {       // specific title (CMP-12)
    Button("Delete", role: .destructive) { deletePermanently(trip) }   // uncommon, irreversible → alert is justified
    Button("Cancel", role: .cancel) { }                                // always “Cancel”, never default (CMP-13)
} message: {
    Text("Its photos and notes will also be deleted. You can’t undo this action.")
}
```

Never “Yes”/“No”; “OK” only for purely informational alerts (CMP-13). No alerts at launch (CMP-11).

## 7. Forms

```swift
Form {
    Section("Account") {                                      // title-style section header (WRT-04)
        TextField("Email", text: $email, prompt: Text("name@example.com"))   // label + hint (WRT-11)
            .textContentType(.emailAddress)
            .keyboardType(.emailAddress)                      // matching keyboard (CMP-22)
            .textInputAutocapitalization(.never)
            .submitLabel(.next)
        SecureField("Password", text: $password)             // secure, never prefilled (CMP-21)
            .textContentType(.password)
    }
    Section {
        Toggle("Trip Reminders", isOn: $reminders)            // switch inside a list row (CMP-23)
    } footer: {
        Text("Get a notification the day before each trip.")  // describe the “on” state (WRT-12)
    }
}
```

Prefer passkeys, Sign in with Apple, and Password AutoFill over custom authentication (PRV-05).

## 8. Feedback

```swift
@State private var savedCount = 0
@Environment(\.accessibilityReduceMotion) private var reduceMotion

Button("Save", systemImage: "bookmark") { save(); savedCount += 1 }
    .symbolEffect(.bounce, value: savedCount)                  // purposeful symbol animation (ICN-07)
    .sensoryFeedback(.success, trigger: savedCount)            // documented meaning: success (HAP-01)

// Motion that respects Reduce Motion (MOT-02)
DetailCard()
    .transition(reduceMotion ? .opacity : .move(edge: .bottom).combined(with: .opacity))
```

`SensoryFeedback` includes `.success`, `.warning`, `.error`, `.selection`, `.impact`, `.increase`, `.decrease`, `.start`, `.stop`, `.alignment`, `.levelChange`, `.pathComplete` — use each only for its meaning (HAP-01) and pair with visual feedback (MOT-03).

## 9. Mac commands

```swift
struct TripCommands: Commands {
    var body: some Commands {
        CommandMenu("Trip") {                                           // app-specific menu (PLT-MAC-01)
            Button("New Trip") { AppActions.newTrip() }
                .keyboardShortcut("n")                                  // ⌘N standard meaning: new document
            Button("Duplicate Trip") { AppActions.duplicate() }
                .keyboardShortcut("d", modifiers: [.command, .shift])   // Command first; Shift secondary (INP-06)
            Divider()
            Button("Share Trip…") { AppActions.share() }                // ellipsis: more input follows (WRT-05)
        }
    }
}
```

Every toolbar item must also appear as a menu command (PLT-MAC-02). Don’t repurpose standard shortcuts (INP-05). Use `.help(_:)` to add tooltips to icon buttons.

## 10. visionOS

```swift
WindowGroup {
    TripsView()                         // keep the system glass window background (GLS-11)
        .ornament(attachmentAnchor: .scene(.bottom)) {
            PlaybackControls()          // app controls in an ornament; supplemental content → adjacent window
                .padding()
                .glassBackgroundEffect()
        }
}
.defaultSize(width: 1280, height: 720)  // default size; pick a shape that fits the content (PLT-VIS-03)
```

- Buttons: ≥ 60 pt targets, centers ≥ 60 pt apart; prefer circular or capsule shapes (LAY-15, INP-09).
- Use `.hoverEffect(_:isEnabled:)` sparingly for special moments; standard components already respond to gaze.
- No `glassEffect` on visionOS — system glass applies to windows.

## 11. Anti-pattern → fix

| Anti-pattern | Fix | Rule |
|---|---|---|
| `if UIDevice.current.userInterfaceIdiom == .pad { … }` | `@Environment(\.horizontalSizeClass)` / `ViewThatFits` | LAY-01 |
| `.font(.system(size: 15))` | `.font(.subheadline)` | TYP-01 |
| `.font(.system(size: 9))` | ≥ 11 pt on iOS; use `.caption2` | TYP-02 |
| `Color(red: 0, green: 0.53, blue: 1)` | `Color.blue` or an asset-catalog Color Set | COL-01 |
| `.preferredColorScheme(.light)` on the root | Support light and dark | COL-07 |
| `Image(systemName: "trash")` as a button label | `Button("Delete", systemImage: "trash")` | A11Y-03 |
| `.frame(width: 24, height: 24)` on a tappable icon | ≥ 44×44 pt hit region (`.frame(minWidth: 44, minHeight: 44)` / `.contentShape`) | A11Y-01 |
| `.animation(.spring, value: x)` with no Reduce Motion check | Gate with `accessibilityReduceMotion` | MOT-02 |
| `Button("Back") { dismiss() }` in a toolbar | System back button / standard Close | NAV-09 |
| `TextField("Password", …)` | `SecureField` | CMP-21 |
| `.toolbarBackground(Color.blue, for: .navigationBar)` | Remove; let Liquid Glass render | GLS-04 |
| Several `.glassEffect()` views without a container | `GlassEffectContainer` | GLS-08 |
| `.glassEffect()` on list rows or cards | Standard materials / system backgrounds | GLS-01 |
| Alert buttons “Yes” / “No” | Verb + Cancel | CMP-13 |

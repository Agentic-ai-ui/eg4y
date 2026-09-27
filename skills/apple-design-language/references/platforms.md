# Platform playbook

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> Source of truth: [`GUIDELINES.md` §2 and §16](../../../GUIDELINES.md#16-platform-guides) · Rules: [`rules/01-cross-platform-sync.md`](../../../rules/01-cross-platform-sync.md), [`rules/14-platforms.md`](../../../rules/14-platforms.md)

Read this first when a task names a device or targets more than one platform. It tells you which container, input model, and metrics to design for, and what must stay identical everywhere.

## Contents
1. [Decide the platform set](#1-decide-the-platform-set)
2. [One matrix for every platform](#2-one-matrix-for-every-platform)
3. [What never changes across platforms](#3-what-never-changes-across-platforms)
4. [Per-platform briefs](#4-per-platform-briefs)
5. [Mapping one information architecture to every platform](#5-mapping-one-information-architecture-to-every-platform)

---

## 1. Decide the platform set

Before designing, write down:

1. **Target platforms** — iPhone, iPad, iPhone Duo, Mac, Apple TV, Apple Vision Pro, Apple Watch. If the task doesn’t say, ask; if you must assume, assume iPhone + iPad (the most common pair) and say so.
2. **Implementation surface** — SwiftUI (preferred; one codebase, system behavior for free), UIKit, AppKit, or a **web** app that should feel at home on Apple devices (see [`web-adaptation.md`](web-adaptation.md)).
3. **Minimum OS** — Liquid Glass APIs (`glassEffect`, `.glass` button styles, `ToolbarSpacer`, `tabBarMinimizeBehavior`, `backgroundExtensionEffect`, `ConcentricRectangle`) require the **26** SDKs and OS releases. For earlier targets, standard components still adopt the current system look when rebuilt; custom glass needs `if #available`.

## 2. One matrix for every platform

| | iPhone | iPad | Mac | Apple TV | Vision Pro | Apple Watch |
|---|---|---|---|---|---|---|
| **Top-level navigation** | Floating tab bar, bottom | Tab bar near top; `sidebarAdaptable` | Sidebar / split view + **menu bar** | Tab bar at top | Vertical tab bar, window’s leading side | List / vertical pages + Digital Crown |
| **Primary input** | Multi-Touch | Touch, keyboard, trackpad, Pencil | Keyboard + pointer | Remote, controller | Eyes + indirect gestures | Touch, Crown, double tap |
| **Viewing distance** | ≤ 1–2 ft | ~3 ft | ~1–3 ft | ≥ 8 ft | Reading content ≥ 1 m | ≤ 1 ft |
| **Default / min text** | 17 / 11 pt | 17 / 11 pt | 13 / 10 pt | 29 / 23 pt | 17 / 12 pt | 16 / 12 pt |
| **Default / min control** | 44 / 28 pt | 44 / 28 pt | 28 / 20 pt | 66 / 56 pt | 60 / 28 pt | 44 / 28 pt |
| **System font** | SF Pro | SF Pro | SF Pro | SF Pro | SF Pro | SF Compact |
| **Dark Mode** | Yes | Yes | Yes | Yes | No (glass adapts) | No |
| **Dynamic Type** | Yes | Yes | No (fixed text styles) | Yes | Yes | Yes |
| **Liquid Glass** | Bars, controls | Bars, controls, sidebar | Bars, controls, sidebar | Navigation; focus states | System glass windows | Toolbar buttons |
| **Where every command lives** | Toolbar, menus | + hidden menu bar | **Menu bar** | Focusable UI | Toolbar, ornaments | Toolbar buttons, list |

Full metrics: [`design-tokens.md`](design-tokens.md).

## 3. What never changes across platforms

These are the “design sync” rules. Violating them makes one app feel like several.

| Keep identical | Rule |
|---|---|
| Features and functionality (only visibility changes with space) | SYNC-01 (MUST NOT change) |
| Terminology — one glossary | SYNC-02 |
| Color meanings and accent color | SYNC-03 |
| App icon design | SYNC-04 |
| Symbols for the same actions | SYNC-05 |
| Toolbar groupings and placement | SYNC-06 |
| Search experience between iPad and Mac | SYNC-07 |
| Context-menu top actions = swipe actions | SYNC-10 |

What **adapts**: the navigation container, input model, text and control metrics, density, and where commands are listed (SYNC-08).

## 4. Per-platform briefs

### iPhone (iOS)
- **Design for:** one- or two-handed use on the go; sessions from seconds to an hour.
- **Structure:** floating Liquid Glass tab bar (NAV-06); large titles that collapse on scroll (NAV-15); search as a tab, bottom toolbar, or inline (NAV-16).
- **Reach:** frequent controls in the middle/bottom; swipe back and row swipe actions (PLT-IOS-01).
- **Integrate:** Apple Pay, biometrics, location instead of forms (PLT-IOS-02); widgets, Spotlight, Shortcuts, quick actions.
- **Watch for:** fixed layouts that break in landscape or at AX5 text (LAY-03, LAY-04); popovers in compact width (CMP-16).

### iPad (iPadOS)
- **Design for:** larger display at ~3 ft, mixed input, full-screen or **windowed** multitasking with fluid resizing (PLT-IPAD-03).
- **Structure:** tab bar near the top, optionally convertible to a sidebar (`sidebarAdaptable`); toolbar and tab bar can share the top row; split views for hierarchy (NAV-08).
- **Windows:** keep leading toolbar items clear of window controls (PLT-IPAD-01); support multiple windows.
- **Menu bar:** mirror the Mac structure, but every command must also be reachable in the UI (PLT-IPAD-02).
- **Keyboard:** keyboard navigation for text fields, sidebars, collections — not controls (INP-11).

### iPhone Duo
- **Design for:** two displays (outer compact, inner regular), a hinge, and multiple poses.
- **Structure:** build to resize with size classes — no display-specific code (PLT-DUO-01); keep functionality and state identical across displays (PLT-DUO-02).
- **Vertical controls:** toolbars, tab bars, navigation sit on the side; don’t override placement (PLT-DUO-03); give toolbar items a title *and* a symbol, visibility priorities, system overflow (PLT-DUO-05).
- **Reserved regions:** cameras and fold — use `ReservedRegion` for custom UI; even-numbered grids (PLT-DUO-04).
- **Two-view layouts:** arrangement views (split/overlay) with navigation outside them (PLT-DUO-06).

### Mac (macOS)
- **Design for:** large displays, keyboard + precise pointer, many windows, long sessions.
- **Structure:** sidebar or split view with an inspector; toolbar in the window frame (no bezels); every toolbar item also in the menu bar (PLT-MAC-02).
- **Menu bar:** App, File, Edit, Format, View, app-specific, Window, Help — all commands, same items always, disabled not hidden (PLT-MAC-01).
- **Windows:** system chrome and key/main/inactive states; resizable; full screen; nothing critical at the bottom (PLT-MAC-03, LAY-12).
- **Keyboard:** standard shortcuts untouched; ⌘, opens Settings (INP-05, PLT-MAC-04).
- **Metrics:** body text 13 pt; controls 28 pt default.

### Apple TV (tvOS)
- **Design for:** 8+ ft, remote-driven focus, shared living-room audience, cinematic content.
- **Structure:** top tab bar (68 pt tall, 46 pt from top); edge-to-edge artwork; split views for filtering.
- **Focus:** scale, parallax, illumination — never color alone (PLT-TV-01); every element focusable, five focus states (INP-08).
- **Metrics:** safe area 60 pt top/bottom, 80 pt sides (LAY-13); grid spacing 40/100 pt (LAY-14); body 29 pt; controls 66 pt.
- **Assets:** layered app icon (2–5 layers) (PLT-TV-02); minimize typing (PLT-TV-03).

### Apple Vision Pro (visionOS)
- **Design for:** infinite canvas, comfort first, eyes + indirect hand gestures, passthrough.
- **Structure:** windows for familiar UI (default 1280×720 pt, ~2 m away), volumes for 3D, immersion only when it adds value (PLT-VIS-01); keep the glass background (GLS-11).
- **Bars:** vertical tab bar on the leading side; toolbar at the bottom; ornaments for app controls; no vertical toolbars (PLT-VIS-05).
- **Eyes:** targets 60 pt; centers ≥ 60 pt apart or ≥ 16 pt margins; rounded shapes (LAY-15, INP-09).
- **Comfort:** anchor in space, never to the head (PLT-VIS-02); no peripheral motion or world rotation (MOT-07); no depth on text (PLT-VIS-04).
- **No haptics, no Dark Mode:** rely on standard controls’ sounds and system glass.

### Apple Watch (watchOS)
- **Design for:** glances under a minute; complications and notifications often matter more than the app (PLT-WATCH-01, PLT-WATCH-04).
- **Structure:** list or vertical pages driven by the Digital Crown; toolbar buttons (Liquid Glass) in corners or bottom.
- **Controls:** full-width primary buttons; ≤ 3 glyph or ≤ 2 text buttons per row (PLT-WATCH-03, LAY-16).
- **Don’t:** show spinners (PLT-WATCH-02); set double-tap primary actions in scrolling views (INP-10); add a Settings-app bundle (PLT-WATCH-05).
- **Metrics:** body 16 pt at the default size; SF Compact.

## 5. Mapping one information architecture to every platform

Start from one list of sections (top-level destinations), objects, and actions. Then place them:

| IA element | iPhone | iPad | Mac | tvOS | visionOS | watchOS |
|---|---|---|---|---|---|---|
| 3–5 top-level sections | Tab bar tabs | Tabs (convertible to sidebar) | Sidebar items | Top tabs | Vertical tabs | Root list rows / pages |
| More sections than fit | Fewer tabs + in-section navigation | `sidebarAdaptable` sidebar | Sidebar groups (≤ 2 levels) | Tabs + split views | Sidebar inside a tab | Root list |
| Collection → item | Push navigation | Split view (list + detail) | Split view (list + detail) | Split view / grid | Split view in window | Push, vertical detail pages |
| Primary action (e.g., Compose) | Toolbar, trailing | Toolbar | Toolbar **and** menu bar + ⌘ shortcut | Focusable button | Toolbar at window bottom | Toolbar button |
| Item actions | Swipe actions + context menu | Same + pointer context menu | Context menu + menu bar | Long-press menu | Context menu | Swipe / toolbar |
| Search | Search tab or toolbar | Toolbar trailing / sidebar top | Toolbar trailing | Search screen | Toolbar / tab | Full-screen input |
| Settings | In-app screen / Settings app | Same + App menu item | Settings window (⌘,) | In-app | In-app | Bottom of main view |

Keep every row’s **label, symbol, and color** identical across the columns (SYNC-02, SYNC-03, SYNC-05).

# Design tokens

> **Created by Edison Augustin X.** · GENERATED from [`../assets/tokens.json`](../assets/tokens.json) by `scripts/build_tokens.py` — do not edit by hand.
> Verified against: Apple Human Interface Guidelines, content current through September 2026.

**How to use these values:** in native apps, use the system API column — never hard-code these values (COL-01, TYP-01). Use the numbers for mockups, validation, reviews, and web adaptation ([`../assets/tokens.css`](../assets/tokens.css)).

## Contents
1. [System colors](#system-colors)
2. [System grays](#system-grays)
3. [Platform text sizes](#platform-text-sizes)
4. [iOS and iPadOS Dynamic Type](#ios-and-ipados-dynamic-type)
5. [macOS text styles](#macos-text-styles)
6. [tvOS text styles](#tvos-text-styles)
7. [watchOS Dynamic Type](#watchos-dynamic-type)
8. [Contrast of system colors](#contrast-of-system-colors)
9. [Accessibility metrics](#accessibility-metrics)
10. [Layout specifications](#layout-specifications)
11. [App icons and images](#app-icons-and-images)

## System colors

visionOS uses the default dark values for system colors. Apple does not publish values for semantic colors (label, systemBackground, separator…); use their APIs.

| Color | SwiftUI | UIKit | AppKit | Light | Dark | Light (increased contrast) | Dark (increased contrast) |
|---|---|---|---|---|---|---|---|
| Red | `Color.red` | `UIColor.systemRed` | `NSColor.systemRed` | `#FF383C` | `#FF4245` | `#E9152D` | `#FF6165` |
| Orange | `Color.orange` | `UIColor.systemOrange` | `NSColor.systemOrange` | `#FF8D28` | `#FF9230` | `#C55300` | `#FFA056` |
| Yellow | `Color.yellow` | `UIColor.systemYellow` | `NSColor.systemYellow` | `#FFCC00` | `#FFD600` | `#A16A00` | `#FEDF43` |
| Green | `Color.green` | `UIColor.systemGreen` | `NSColor.systemGreen` | `#34C759` | `#30D158` | `#008932` | `#4AD968` |
| Mint | `Color.mint` | `UIColor.systemMint` | `NSColor.systemMint` | `#00C8B3` | `#00DAC3` | `#008575` | `#54DFCB` |
| Teal | `Color.teal` | `UIColor.systemTeal` | `NSColor.systemTeal` | `#00C3D0` | `#00D2E0` | `#008198` | `#3BDDEC` |
| Cyan | `Color.cyan` | `UIColor.systemCyan` | `NSColor.systemCyan` | `#00C0E8` | `#3CD3FE` | `#007EAE` | `#6DD9FF` |
| Blue | `Color.blue` | `UIColor.systemBlue` | `NSColor.systemBlue` | `#0088FF` | `#0091FF` | `#1E6EF4` | `#5CB8FF` |
| Indigo | `Color.indigo` | `UIColor.systemIndigo` | `NSColor.systemIndigo` | `#6155F5` | `#6D7CFF` | `#564ADE` | `#A7AAFF` |
| Purple | `Color.purple` | `UIColor.systemPurple` | `NSColor.systemPurple` | `#CB30E0` | `#DB34F2` | `#B02FC2` | `#EA8DFF` |
| Pink | `Color.pink` | `UIColor.systemPink` | `NSColor.systemPink` | `#FF2D55` | `#FF375F` | `#E7124D` | `#FF8AC4` |
| Brown | `Color.brown` | `UIColor.systemBrown` | `NSColor.systemBrown` | `#AC7F5E` | `#B78A66` | `#956D51` | `#DBA679` |

## System grays

iOS and iPadOS. `systemGray2`–`systemGray6` are UIKit colors; SwiftUI reaches them through `Color(uiColor:)`.

| Gray | SwiftUI | UIKit | Light | Dark | Light (increased contrast) | Dark (increased contrast) |
|---|---|---|---|---|---|---|
| Gray | `Color.gray` | `UIColor.systemGray` | `#8E8E93` | `#8E8E93` | `#6C6C70` | `#AEAEB2` |
| Gray (2) | `Color(uiColor: .systemGray2)` | `UIColor.systemGray2` | `#AEAEB2` | `#636366` | `#8E8E93` | `#7C7C80` |
| Gray (3) | `Color(uiColor: .systemGray3)` | `UIColor.systemGray3` | `#C7C7CC` | `#48484A` | `#AEAEB2` | `#545456` |
| Gray (4) | `Color(uiColor: .systemGray4)` | `UIColor.systemGray4` | `#D1D1D6` | `#3A3A3C` | `#BCBCC0` | `#444446` |
| Gray (5) | `Color(uiColor: .systemGray5)` | `UIColor.systemGray5` | `#E5E5EA` | `#2C2C2E` | `#D8D8DC` | `#363638` |
| Gray (6) | `Color(uiColor: .systemGray6)` | `UIColor.systemGray6` | `#F2F2F7` | `#1C1C1E` | `#EBEBF0` | `#242426` |

## Platform text sizes

| Platform | Default | Minimum | System family |
|---|---|---|---|
| iOS | 17 pt | 11 pt | SF Pro |
| iPadOS | 17 pt | 11 pt | SF Pro |
| macOS | 13 pt | 10 pt | SF Pro |
| tvOS | 29 pt | 23 pt | SF Pro |
| visionOS | 17 pt | 12 pt | SF Pro |
| watchOS | 16 pt | 12 pt | SF Compact |

Serif family: New York · watchOS complications: SF Compact Rounded · text enlargement target: 200% (140% on watchOS).

## iOS and iPadOS Dynamic Type

iOS and iPadOS Dynamic Type sizes, including larger accessibility sizes AX1–AX5.

**Body size across all sizes:** xSmall 14 · Small 15 · Medium 16 · Large 17 · xLarge 19 · xxLarge 21 · xxxLarge 23 · AX1 28 · AX2 33 · AX3 40 · AX4 47 · AX5 53

### iOS xSmall

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 31 | 38 | Bold |
| Title 1 | Regular | 25 | 31 | Bold |
| Title 2 | Regular | 19 | 24 | Bold |
| Title 3 | Regular | 17 | 22 | Semibold |
| Headline | Semibold | 14 | 19 | Semibold |
| Body | Regular | 14 | 19 | Semibold |
| Callout | Regular | 13 | 18 | Semibold |
| Subhead | Regular | 12 | 16 | Semibold |
| Footnote | Regular | 12 | 16 | Semibold |
| Caption 1 | Regular | 11 | 13 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

### iOS Small

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 32 | 39 | Bold |
| Title 1 | Regular | 26 | 32 | Bold |
| Title 2 | Regular | 20 | 25 | Bold |
| Title 3 | Regular | 18 | 23 | Semibold |
| Headline | Semibold | 15 | 20 | Semibold |
| Body | Regular | 15 | 20 | Semibold |
| Callout | Regular | 14 | 19 | Semibold |
| Subhead | Regular | 13 | 18 | Semibold |
| Footnote | Regular | 12 | 16 | Semibold |
| Caption 1 | Regular | 11 | 13 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

### iOS Medium

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 33 | 40 | Bold |
| Title 1 | Regular | 27 | 33 | Bold |
| Title 2 | Regular | 21 | 26 | Bold |
| Title 3 | Regular | 19 | 24 | Semibold |
| Headline | Semibold | 16 | 21 | Semibold |
| Body | Regular | 16 | 21 | Semibold |
| Callout | Regular | 15 | 20 | Semibold |
| Subhead | Regular | 14 | 19 | Semibold |
| Footnote | Regular | 12 | 16 | Semibold |
| Caption 1 | Regular | 11 | 13 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

### iOS Large (default)

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 34 | 41 | Bold |
| Title 1 | Regular | 28 | 34 | Bold |
| Title 2 | Regular | 22 | 28 | Bold |
| Title 3 | Regular | 20 | 25 | Semibold |
| Headline | Semibold | 17 | 22 | Semibold |
| Body | Regular | 17 | 22 | Semibold |
| Callout | Regular | 16 | 21 | Semibold |
| Subhead | Regular | 15 | 20 | Semibold |
| Footnote | Regular | 13 | 18 | Semibold |
| Caption 1 | Regular | 12 | 16 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

### iOS xLarge

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 36 | 43 | Bold |
| Title 1 | Regular | 30 | 37 | Bold |
| Title 2 | Regular | 24 | 30 | Bold |
| Title 3 | Regular | 22 | 28 | Semibold |
| Headline | Semibold | 19 | 24 | Semibold |
| Body | Regular | 19 | 24 | Semibold |
| Callout | Regular | 18 | 23 | Semibold |
| Subhead | Regular | 17 | 22 | Semibold |
| Footnote | Regular | 15 | 20 | Semibold |
| Caption 1 | Regular | 14 | 19 | Semibold |
| Caption 2 | Regular | 13 | 18 | Semibold |

### iOS xxLarge

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 38 | 46 | Bold |
| Title 1 | Regular | 32 | 39 | Bold |
| Title 2 | Regular | 26 | 32 | Bold |
| Title 3 | Regular | 24 | 30 | Semibold |
| Headline | Semibold | 21 | 26 | Semibold |
| Body | Regular | 21 | 26 | Semibold |
| Callout | Regular | 20 | 25 | Semibold |
| Subhead | Regular | 19 | 24 | Semibold |
| Footnote | Regular | 17 | 22 | Semibold |
| Caption 1 | Regular | 16 | 21 | Semibold |
| Caption 2 | Regular | 15 | 20 | Semibold |

### iOS xxxLarge

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 40 | 48 | Bold |
| Title 1 | Regular | 34 | 41 | Bold |
| Title 2 | Regular | 28 | 34 | Bold |
| Title 3 | Regular | 26 | 32 | Semibold |
| Headline | Semibold | 23 | 29 | Semibold |
| Body | Regular | 23 | 29 | Semibold |
| Callout | Regular | 22 | 28 | Semibold |
| Subhead | Regular | 21 | 28 | Semibold |
| Footnote | Regular | 19 | 24 | Semibold |
| Caption 1 | Regular | 18 | 23 | Semibold |
| Caption 2 | Regular | 17 | 22 | Semibold |

### iOS AX1

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 44 | 52 | Bold |
| Title 1 | Regular | 38 | 46 | Bold |
| Title 2 | Regular | 34 | 41 | Bold |
| Title 3 | Regular | 31 | 38 | Semibold |
| Headline | Semibold | 28 | 34 | Semibold |
| Body | Regular | 28 | 34 | Semibold |
| Callout | Regular | 26 | 32 | Semibold |
| Subhead | Regular | 25 | 31 | Semibold |
| Footnote | Regular | 23 | 29 | Semibold |
| Caption 1 | Regular | 22 | 28 | Semibold |
| Caption 2 | Regular | 20 | 25 | Semibold |

### iOS AX2

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 48 | 57 | Bold |
| Title 1 | Regular | 43 | 51 | Bold |
| Title 2 | Regular | 39 | 47 | Bold |
| Title 3 | Regular | 37 | 44 | Semibold |
| Headline | Semibold | 33 | 40 | Semibold |
| Body | Regular | 33 | 40 | Semibold |
| Callout | Regular | 32 | 39 | Semibold |
| Subhead | Regular | 30 | 37 | Semibold |
| Footnote | Regular | 27 | 33 | Semibold |
| Caption 1 | Regular | 26 | 32 | Semibold |
| Caption 2 | Regular | 24 | 30 | Semibold |

### iOS AX3

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 52 | 61 | Bold |
| Title 1 | Regular | 48 | 57 | Bold |
| Title 2 | Regular | 44 | 52 | Bold |
| Title 3 | Regular | 43 | 51 | Semibold |
| Headline | Semibold | 40 | 48 | Semibold |
| Body | Regular | 40 | 48 | Semibold |
| Callout | Regular | 38 | 46 | Semibold |
| Subhead | Regular | 36 | 43 | Semibold |
| Footnote | Regular | 33 | 40 | Semibold |
| Caption 1 | Regular | 32 | 39 | Semibold |
| Caption 2 | Regular | 29 | 35 | Semibold |

### iOS AX4

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 56 | 66 | Bold |
| Title 1 | Regular | 53 | 62 | Bold |
| Title 2 | Regular | 50 | 59 | Bold |
| Title 3 | Regular | 49 | 58 | Semibold |
| Headline | Semibold | 47 | 56 | Semibold |
| Body | Regular | 47 | 56 | Semibold |
| Callout | Regular | 44 | 52 | Semibold |
| Subhead | Regular | 42 | 50 | Semibold |
| Footnote | Regular | 38 | 46 | Semibold |
| Caption 1 | Regular | 37 | 44 | Semibold |
| Caption 2 | Regular | 34 | 41 | Semibold |

### iOS AX5

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 60 | 70 | Bold |
| Title 1 | Regular | 58 | 68 | Bold |
| Title 2 | Regular | 56 | 66 | Bold |
| Title 3 | Regular | 55 | 65 | Semibold |
| Headline | Semibold | 53 | 62 | Semibold |
| Body | Regular | 53 | 62 | Semibold |
| Callout | Regular | 51 | 60 | Semibold |
| Subhead | Regular | 49 | 58 | Semibold |
| Footnote | Regular | 44 | 52 | Semibold |
| Caption 1 | Regular | 43 | 51 | Semibold |
| Caption 2 | Regular | 40 | 48 | Semibold |

## macOS text styles

macOS doesn't support Dynamic Type; values are line height.

| Style | Weight | Size (pt) | Line height (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 26 | 32 | Bold |
| Title 1 | Regular | 22 | 26 | Bold |
| Title 2 | Regular | 17 | 22 | Bold |
| Title 3 | Regular | 15 | 20 | Semibold |
| Headline | Bold | 13 | 16 | Heavy |
| Body | Regular | 13 | 16 | Semibold |
| Callout | Regular | 12 | 15 | Semibold |
| Subheadline | Regular | 11 | 14 | Semibold |
| Footnote | Regular | 10 | 13 | Semibold |
| Caption 1 | Regular | 10 | 13 | Medium |
| Caption 2 | Medium | 10 | 13 | Semibold |

## tvOS text styles

tvOS built-in text styles.

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Title 1 | Medium | 76 | 96 | Bold |
| Title 2 | Medium | 57 | 66 | Bold |
| Title 3 | Medium | 48 | 56 | Bold |
| Headline | Medium | 38 | 46 | Bold |
| Subtitle 1 | Regular | 38 | 46 | Medium |
| Callout | Medium | 31 | 38 | Bold |
| Body | Medium | 29 | 36 | Bold |
| Caption 1 | Medium | 25 | 32 | Bold |
| Caption 2 | Medium | 23 | 30 | Bold |

## watchOS Dynamic Type

watchOS Dynamic Type sizes, including larger accessibility sizes AX1–AX3.

### watchOS xSmall

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 30 | 32.5 | Bold |
| Title 1 | Regular | 28 | 30.5 | Semibold |
| Title 2 | Regular | 24 | 26.5 | Semibold |
| Title 3 | Regular | 17 | 19.5 | Semibold |
| Headline | Semibold | 14 | 16.5 | Semibold |
| Body | Regular | 14 | 16.5 | Semibold |
| Caption 1 | Regular | 13 | 15.5 | Semibold |
| Caption 2 | Regular | 12 | 14.5 | Semibold |
| Footnote 1 | Regular | 11 | 13.5 | Semibold |
| Footnote 2 | Regular | 10 | 12.5 | Semibold |

### watchOS Small (default 38mm)

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 32 | 34.5 | Bold |
| Title 1 | Regular | 30 | 32.5 | Semibold |
| Title 2 | Regular | 26 | 28.5 | Semibold |
| Title 3 | Regular | 18 | 20.5 | Semibold |
| Headline | Semibold | 15 | 17.5 | Semibold |
| Body | Regular | 15 | 17.5 | Semibold |
| Caption 1 | Regular | 14 | 16.5 | Semibold |
| Caption 2 | Regular | 13 | 15.5 | Semibold |
| Footnote 1 | Regular | 12 | 14.5 | Semibold |
| Footnote 2 | Regular | 11 | 13.5 | Semibold |

### watchOS Large (default 40mm/41mm/42mm)

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 36 | 38.5 | Bold |
| Title 1 | Regular | 34 | 36.5 | Semibold |
| Title 2 | Regular | 28 | 30.5 | Semibold |
| Title 3 | Regular | 19 | 21.5 | Semibold |
| Headline | Semibold | 16 | 18.5 | Semibold |
| Body | Regular | 16 | 18.5 | Semibold |
| Caption 1 | Regular | 15 | 17.5 | Semibold |
| Caption 2 | Regular | 14 | 16.5 | Semibold |
| Footnote 1 | Regular | 13 | 15.5 | Semibold |
| Footnote 2 | Regular | 12 | 14.5 | Semibold |

### watchOS xLarge (default 44mm/45mm/49mm)

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 40 | 42.5 | Bold |
| Title 1 | Regular | 38 | 40.5 | Semibold |
| Title 2 | Regular | 30 | 32.5 | Semibold |
| Title 3 | Regular | 20 | 22.5 | Semibold |
| Headline | Semibold | 17 | 19.5 | Semibold |
| Body | Regular | 17 | 19.5 | Semibold |
| Caption 1 | Regular | 16 | 18.5 | Semibold |
| Caption 2 | Regular | 15 | 17.5 | Semibold |
| Footnote 1 | Regular | 14 | 16.5 | Semibold |
| Footnote 2 | Regular | 13 | 15.5 | Semibold |

### watchOS xxLarge

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 41 | 43.5 | Bold |
| Title 1 | Regular | 39 | 41.5 | Semibold |
| Title 2 | Regular | 31 | 33.5 | Semibold |
| Title 3 | Regular | 21 | 23.5 | Semibold |
| Headline | Semibold | 18 | 20.5 | Semibold |
| Body | Regular | 18 | 20.5 | Semibold |
| Caption 1 | Regular | 17 | 19.5 | Semibold |
| Caption 2 | Regular | 16 | 18.5 | Semibold |
| Footnote 1 | Regular | 15 | 17.5 | Semibold |
| Footnote 2 | Regular | 14 | 16.5 | Semibold |

### watchOS xxxLarge

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 42 | 44.5 | Bold |
| Title 1 | Regular | 40 | 42.5 | Semibold |
| Title 2 | Regular | 32 | 34.5 | Semibold |
| Title 3 | Regular | 22 | 24.5 | Semibold |
| Headline | Semibold | 19 | 21.5 | Semibold |
| Body | Regular | 19 | 21.5 | Semibold |
| Caption 1 | Regular | 18 | 20.5 | Semibold |
| Caption 2 | Regular | 17 | 19.5 | Semibold |
| Footnote 1 | Regular | 16 | 18.5 | Semibold |
| Footnote 2 | Regular | 15 | 17.5 | Semibold |

### watchOS AX1

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 44 | 46.5 | Bold |
| Title 1 | Regular | 42 | 44.5 | Semibold |
| Title 2 | Regular | 34 | 41 | Semibold |
| Title 3 | Regular | 24 | 26.5 | Semibold |
| Headline | Semibold | 21 | 23.5 | Semibold |
| Body | Regular | 21 | 23.5 | Semibold |
| Caption 1 | Regular | 18 | 20.5 | Semibold |
| Caption 2 | Regular | 17 | 19.5 | Semibold |
| Footnote 1 | Regular | 16 | 18.5 | Semibold |
| Footnote 2 | Regular | 15 | 17.5 | Semibold |

### watchOS AX2

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 45 | 47.5 | Bold |
| Title 1 | Regular | 43 | 46 | Semibold |
| Title 2 | Regular | 35 | 37.5 | Semibold |
| Title 3 | Regular | 25 | 27.5 | Semibold |
| Headline | Semibold | 22 | 24.5 | Semibold |
| Body | Regular | 22 | 24.5 | Semibold |
| Caption 1 | Regular | 19 | 21.5 | Semibold |
| Caption 2 | Regular | 18 | 20.5 | Semibold |
| Footnote 1 | Regular | 17 | 19.5 | Semibold |
| Footnote 2 | Regular | 16 | 17.5 | Semibold |

### watchOS AX3

| Style | Weight | Size (pt) | Leading (pt) | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 46 | 48.5 | Bold |
| Title 1 | Regular | 44 | 47 | Semibold |
| Title 2 | Regular | 36 | 38.5 | Semibold |
| Title 3 | Regular | 26 | 28.5 | Semibold |
| Headline | Semibold | 23 | 25.5 | Semibold |
| Body | Regular | 23 | 25.5 | Semibold |
| Caption 1 | Regular | 20 | 22.5 | Semibold |
| Caption 2 | Regular | 19 | 21.5 | Semibold |
| Footnote 1 | Regular | 18 | 20.5 | Semibold |
| Footnote 2 | Regular | 17 | 19.5 | Semibold |

## Contrast of system colors

WCAG 2 contrast ratio of each system color used as a foreground on pure white (light) or pure black (dark), computed by `scripts/build_tokens.py` from the values above. ✓ = meets 4.5:1 (small text); ◐ = meets 3:1 (large or bold text, icons); ✗ = below 3:1.

| Color | Light on white | Dark on black | Light increased contrast on white | Dark increased contrast on black |
|---|---|---|---|---|
| Red | 3.57 ◐ | 6.12 ✓ | 4.56 ✓ | 7.15 ✓ |
| Orange | 2.31 ✗ | 9.41 ✓ | 4.55 ✓ | 10.41 ✓ |
| Yellow | 1.51 ✗ | 14.87 ✓ | 4.59 ✓ | 15.85 ✓ |
| Green | 2.22 ✗ | 10.39 ✓ | 4.54 ✓ | 11.42 ✓ |
| Mint | 2.12 ✗ | 11.82 ✓ | 4.55 ✓ | 12.79 ✓ |
| Teal | 2.16 ✗ | 11.30 ✓ | 4.57 ✓ | 12.74 ✓ |
| Cyan | 2.16 ✗ | 11.94 ✓ | 4.57 ✓ | 13.02 ✓ |
| Blue | 3.52 ◐ | 6.49 ✓ | 4.57 ✓ | 9.76 ✓ |
| Indigo | 5.09 ✓ | 5.98 ✓ | 6.12 ✓ | 9.84 ✓ |
| Purple | 4.17 ◐ | 5.79 ✓ | 5.21 ✓ | 9.75 ✓ |
| Pink | 3.65 ◐ | 5.96 ✓ | 4.57 ✓ | 9.68 ✓ |
| Brown | 3.53 ◐ | 6.84 ✓ | 4.58 ✓ | 9.74 ✓ |

Takeaway: default light-mode system colors (except indigo) are for fills, icons, tints, and large/bold text; small text needs the label color or an increased-contrast variant (COL-06).

## Accessibility metrics

**Minimum contrast (WCAG AA, as used by Accessibility Inspector)**

| Text size | Weight | Minimum ratio |
|---|---|---|
| up to 17 pt | all | 4.5:1 |
| 18 pt and larger | all | 3:1 |
| all | bold | 3:1 |

Custom foreground/background pairs: strive for 7:1 (especially small text).

**Control sizes**

| Platform | Default | Minimum |
|---|---|---|
| iOS | 44×44 pt | 28×28 pt |
| iPadOS | 44×44 pt | 28×28 pt |
| macOS | 28×28 pt | 20×20 pt |
| tvOS | 66×66 pt | 56×56 pt |
| visionOS | 60×60 pt | 28×28 pt |
| watchOS | 44×44 pt | 28×28 pt |

Padding around controls: about 12 pt for bezeled elements, about 24 pt for non-bezeled elements.

## Layout specifications

| Spec | Value |
|---|---|
| tvOS safe area | 60 pt top/bottom · 80 pt sides |
| tvOS grid spacing | 40 pt horizontal · ≥ 100 pt vertical |
| tvOS unfocused widths | 2-col 860 · 3-col 560 · 4-col 410 · 5-col 320 · 6-col 260 · 7-col 217 · 8-col 184 · 9-col 160 pt |
| tvOS tab bar | 68 pt tall, top edge 46 pt from screen top |
| visionOS spacing | button centers ≥ 60 pt apart or ≥ 16 pt margin |
| visionOS default window | 1280×720 pt |
| visionOS reading distance | ≥ 1 m |
| visionOS button sizes | mini 28 · small 32 · regular 44 · large 52 · extraLarge 64 pt |
| visionOS alert accessory | ≤ 154 pt tall, 16 pt corner radius |
| watchOS buttons per row | ≤ 3 glyph or ≤ 2 text |
| watchOS action sheet | ≤ 4 buttons incl. Cancel |
| macOS menu bar height | 24 pt |
| macOS split view thin divider | 1 pt |
| iPhone segmented control | ≤ 5 segments |
| Toolbar | title < 15 characters · ≤ 3 groups · ≤ 1 prominent action |
| Alert | ≤ 3 buttons · title ≤ 2 lines |
| Buttons | ≤ 2 prominent per view |
| Sidebar | ≤ 2 hierarchy levels |
| Clear Liquid Glass over bright content | 35% dark dimming layer |
| RTL beside uppercase Latin | Arabic/Hebrew about +2 pt |
| visionOS oscillation to avoid | ~0.2 Hz |
| Game frame rate | 30–60 fps |

## App icons and images

| Platform | Canvas | Layout shape | After masking | Notes |
|---|---|---|---|---|
| iOS | 1024x1024 px | square | rounded rectangle | default, dark, clear light, clear dark, tinted light, tinted dark |
| macOS | 1024x1024 px | square | rounded rectangle | default, dark, clear light, clear dark, tinted light, tinted dark |
| tvOS | 800x480 px | rectangle | rounded rectangle | 2-5 (parallax) |
| visionOS | 1024x1024 px | square | circle | background + 1-2 |
| watchOS | 1088x1088 px | square | circle |  |

Icon color spaces: sRGB, Gray Gamma 2.2, Display P3 (not visionOS).

| Platform | Image scale factors |
|---|---|
| iOS | @2x, @3x |
| iPadOS | @2x |
| watchOS | @2x |
| macOS | @1x, @2x |
| tvOS | @1x, @2x |
| visionOS | @2x or higher (prefer vector) |

## Sources

- [color](https://developer.apple.com/design/human-interface-guidelines/color)
- [typography](https://developer.apple.com/design/human-interface-guidelines/typography)
- [accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- [layout](https://developer.apple.com/design/human-interface-guidelines/layout)
- [buttons](https://developer.apple.com/design/human-interface-guidelines/buttons)
- [appIcons](https://developer.apple.com/design/human-interface-guidelines/app-icons)
- [images](https://developer.apple.com/design/human-interface-guidelines/images)
- [materials](https://developer.apple.com/design/human-interface-guidelines/materials)
- [tabBars](https://developer.apple.com/design/human-interface-guidelines/tab-bars)
- [menuBar](https://developer.apple.com/design/human-interface-guidelines/the-menu-bar)
- [windows](https://developer.apple.com/design/human-interface-guidelines/windows)
- [eyes](https://developer.apple.com/design/human-interface-guidelines/eyes)

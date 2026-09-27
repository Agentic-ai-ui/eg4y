# Writing for Apple platforms

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> Source of truth: [`GUIDELINES.md` §12](../../../GUIDELINES.md#12-inclusion-and-writing) · Rules: [`rules/09-writing-localization.md`](../../../rules/09-writing-localization.md), CMP-12/13, PRV-02
> Apple sources: [Writing](https://developer.apple.com/design/human-interface-guidelines/writing) · [Inclusion](https://developer.apple.com/design/human-interface-guidelines/inclusion) · [Alerts](https://developer.apple.com/design/human-interface-guidelines/alerts) · [Menus](https://developer.apple.com/design/human-interface-guidelines/menus) · [Privacy](https://developer.apple.com/design/human-interface-guidelines/privacy) · [Right to left](https://developer.apple.com/design/human-interface-guidelines/right-to-left)

Words are interface. Write every string as part of the design, not after it.

## Contents
1. [Voice and tone](#1-voice-and-tone)
2. [Capitalization by element](#2-capitalization-by-element)
3. [Labels and actions](#3-labels-and-actions)
4. [Templates](#4-templates)
5. [Rewrite table](#5-rewrite-table)
6. [Localization and right-to-left](#6-localization-and-right-to-left)

---

## 1. Voice and tone

- **Define a voice** (who you’re talking to, how they should feel) and keep a glossary of terms used on every platform (SYNC-02).
- **Match tone to context**: direct and calm for errors and risk; light and celebratory for achievements.
- **Be clear and brief**: fewer, plain words; read it aloud; no jargon, undefined terms, colloquialisms, or unnecessary humor (WRT-09).
- **Address people as “you”**; avoid “the user”; avoid “we” (“Unable to load content”, not “We’re having trouble…”); use “my”/“your” sparingly (WRT-06).
- **Write for everyone**: gender-neutral, people-first language about disability, diverse examples (WRT-13).
- **Write for the device**: “tap” on touch, “click” with a pointer, “choose” when input varies; brevity on iPhone, Watch, and TV (WRT-03).

## 2. Capitalization by element

Choose one style per element type and apply it everywhere (WRT-04). Apple’s own conventions:

| Element | Style | Example |
|---|---|---|
| Buttons | Title | Add to Cart |
| Menu items and menu titles | Title, no articles | Export As… |
| Segment labels, column headings | Title (nouns) | Recent · Shared |
| Tab labels | Single word when possible | Library |
| List/form section headers | Title (not all caps) | Payment Method |
| Navigation/window titles | Title, < 15 characters, not the app name | Edit Trip |
| Alert title — fragment | Title, no ending punctuation | Delete “Lisbon Trip”? |
| Alert title — full sentence | Sentence, with punctuation | This trip can’t be shared. |
| Alert message, descriptions, footers | Sentence | Items in the trip will also be removed. |
| Purpose strings | Sentence, ends with a period | The app uses your location to show nearby stations. |
| macOS slider/field labels | Sentence, ending with a colon | Opacity: |

*Title-style capitalization:* capitalize every word except articles, coordinating conjunctions, and short prepositions; always capitalize the last word.

## 3. Labels and actions

- Buttons and action menu items start with a **verb** that names the result: Send, Save Draft, Add to Cart (WRT-01).
- Links describe the destination: “Learn more about sharing”, never “Click here” (WRT-02).
- Add an **ellipsis (…)** when the command needs more input first: Rename…, Export As…, Print… (WRT-05).
- Multistep flows: **Get Started** → **Continue** (or **Next**, consistently) → **Done** (WRT-10).
- Settings: plain names; describe what happens when *on*; link straight to settings instead of describing their location (WRT-12).
- Text fields: a label **and** a hint (“name@example.com”); placeholders alone disappear while typing (WRT-11).
- Toggled menu items: “Show Map” ⇄ “Hide Map”, or a checkmark for active attributes.
- Undo/redo: name the action — “Undo Typing”, “Redo Bold” (PAT-06).

## 4. Templates

### Alert (critical, actionable)

```
Title:   Delete “Lisbon Trip”?                       ← fragment → Title Case, no period
Message: Its photos and notes will also be deleted.  ← optional, one or two short sentences
Buttons: [Cancel]  [Delete]                          ← Cancel leading; Delete destructive (unexpected loss)
```

Informational (no decision): `Title: Download Complete` · `[OK]` — the only case where “OK” is right.

### Action sheet (choices about an intentional action)

```
Title:   (optional, one line)
[Delete Draft]    ← destructive, top
[Save Draft]
[Cancel]          ← bottom
```

### Error message (inline, next to the field)

```
Choose a password with at least 8 characters.       ✓ says how to fix it
Use only letters for your name.                     ✓ instructs, doesn’t scold
```

### Empty state

```
Title:   No Trips Yet
Body:    Trips you create or are invited to appear here.
Button:  [New Trip]
```

### Purpose string (permission prompt)

```
✓ The app records during the night to detect snoring sounds.
✗ Microphone access is needed for a better experience.   (passive, vague)
✗ Turn on microphone access.                              (no reason)
```

Pre-permission screen, if needed: explain the benefit; one button titled **Continue** (never “Allow”); no cancel (PRV-03).

### Progress (specific, reassuring)

```
✓ Uploading 3 of 12 photos
✓ Summarizing key themes from your notes      (generative AI, AI-06)
✗ Loading…   ✗ Processing…
```

## 5. Rewrite table

| Instead of | Write | Rule |
|---|---|---|
| Let’s do it! | Send | WRT-01 |
| Click here for details | View Details / Learn more about pricing | WRT-02, WRT-03 |
| Oops! Something went wrong. | Unable to save the trip. Check your connection and try again. | WRT-07 |
| Invalid name | Use only letters for your name. | WRT-07 |
| We couldn’t find anything | No Results | WRT-06 |
| Your Favorites | Favorites | WRT-06 |
| Are you sure? [Yes] [No] | Delete “Lisbon Trip”? [Cancel] [Delete] | CMP-13 |
| Error 329347 occurred | The file couldn’t be opened because it’s damaged. | CMP-12 |
| The user can share… | You can share… | WRT-06 |
| Tap the button below | Choose Continue | WRT-03 (device-neutral) |
| SETTINGS (all-caps header) | Settings | WRT-04 |
| Export | Export As… (opens options) | WRT-05 |

## 6. Localization and right-to-left

- Externalize every string; let the system format dates, times, numbers, and currency; design for text expansion (L10N-01).
- Keep text out of images, icons, and launch screens; localize characters that must appear in icons (L10N-05).
- Right-to-left: mirror progress, sliders, back/forward, text-like and motion icons (L10N-02); never reverse digits within a number or flip logos, checkmarks, photos, or real-direction controls (L10N-03).
- Align 1–2 line text to the interface direction and paragraphs to their language; enlarge Arabic/Hebrew ~2 pt beside uppercase Latin (L10N-04).
- Color meanings vary by culture; verify per locale (COL-13).

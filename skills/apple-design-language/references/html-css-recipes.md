# HTML + CSS recipes: Apple Design Language without a framework

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> Builds on [`web-adaptation.md`](web-adaptation.md) · Assets: [`tokens.css`](../assets/tokens.css), [`components.css`](../assets/components.css)
> The same classes power the [React](react-recipes.md), [Vue and Svelte](vue-svelte.md), and [Next.js](nextjs.md) recipes, so every stack renders the same design.

Plain HTML gets further than most people expect: `<dialog>` gives modal sheets and alerts with focus containment and Esc, the `popover` attribute gives menus with light dismiss, native radios give a segmented control with arrow keys, and container queries switch the tab bar to a sidebar. The page below needs **eight lines of JavaScript** (to open dialogs and enable a button). It was run in Chromium with axe-core (WCAG 2.2 AA) at phone and tablet widths in light, dark, Increase Contrast, and Reduce Motion, right-to-left, and 200% text, with keyboard checks for the sheet, alert, menu, switch, and segmented control.

## Contents
1. [Setup](#1-setup)
2. [Class reference](#2-class-reference)
3. [A complete screen](#3-a-complete-screen)
4. [How each pattern works](#4-how-each-pattern-works)
5. [Browser support and fallbacks](#5-browser-support-and-fallbacks)

---

## 1. Setup

1. Copy [`tokens.css`](../assets/tokens.css) and [`components.css`](../assets/components.css) next to your HTML.
2. In `<head>`: the viewport with `viewport-fit=cover` and no zoom lock (LAY-02, A11Y-05), `color-scheme` for both appearances (COL-07), then the two stylesheets in order.
3. Use an open-licensed icon set or your own SVGs, marked `aria-hidden="true"` next to a text label — SF Symbols are licensed only for apps on Apple platforms (BRD-03).

## 2. Class reference

| Pattern | Markup | Classes | Rules |
|---|---|---|---|
| App shell | `div > div > nav + main` | `adl-app`, `adl-app__layout`, `adl-app__main` | LAY-01, SYNC-01 |
| Tab bar ⇄ sidebar | `<nav aria-label>` + links with `aria-current="page"` | `adl-nav adl-glass`, `adl-nav__list`, `adl-nav__link` | NAV-01, NAV-03, NAV-06 |
| Toolbar | `<header>` | `adl-toolbar adl-glass`, `__leading`, `__title`, `__trailing` | NAV-11, GLS-04 |
| Large title | `<h1>` | `adl-large-title` | NAV-15 |
| Buttons | `<button type="button">` | `adl-button` + `--prominent` / `--plain` / `--destructive`; `adl-icon-button` | CMP-01 – CMP-04, A11Y-03 |
| Inset grouped list | `section > h2 + ul[role=list] > li` | `adl-grouped`, `adl-list-section`, `adl-list`, `adl-list__row` (`--link`, `--destructive`, `--action`) | CMP-19 |
| Switch | `label > input[type=checkbox][role=switch]` | `adl-list__row adl-switch-row`, `adl-switch` | CMP-23, COL-03 |
| Segmented control | `fieldset > legend + label > input[type=radio]` | `adl-segmented`, `adl-segmented__option` | CMP-24, CMP-25 |
| Text field | `label + input + p` | `adl-field`, `adl-field__label`, `__input`, `__hint`, `__error` | CMP-21, CMP-22, WRT-07 |
| Search | `<search>` + `input[type=search]` | `adl-search` | NAV-16 |
| Sheet | `<dialog>` + `form[method=dialog]` | `adl-sheet`, `adl-sheet__header`, `__title`, `__body` | CMP-07 – CMP-09 |
| Alert | `<dialog role="alertdialog">` | `adl-alert`, `__content`, `__title`, `__message`, `__actions` | CMP-11 – CMP-13 |
| Menu | `[popover]` + `popovertarget` | `adl-menu adl-glass`, `adl-menu__item` (`--destructive`), `adl-menu__separator` | CMP-16, CMP-17 |
| Empty state | `div > h2 + p` | `adl-empty`, `__title`, `__message` | NAV-03 |
| Hidden label | any | `adl-visually-hidden` | A11Y-03 |

## 3. A complete screen

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
  <meta name="color-scheme" content="light dark">
  <title>Library</title>
  <link rel="stylesheet" href="tokens.css">
  <link rel="stylesheet" href="components.css">
</head>
<body>
<div class="adl-app">
  <div class="adl-app__layout">
    <!-- One navigation list: tab bar in compact widths, sidebar in regular widths (NAV-06, SYNC-01) -->
    <nav class="adl-nav adl-glass" aria-label="Primary">
      <ul class="adl-nav__list">
        <li><a class="adl-nav__link" href="#home">
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 11 12 4l9 7v9h-6v-6H9v6H3z"/></svg>
          <span>Home</span></a></li>
        <li><a class="adl-nav__link" href="#library" aria-current="page">
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 4v16M10 4v16M15 5l4 15"/></svg>
          <span>Library</span></a></li>
        <li><a class="adl-nav__link" href="#search">
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>
          <span>Search</span></a></li>
        <li><a class="adl-nav__link" href="#settings">
          <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/></svg>
          <span>Settings</span></a></li>
      </ul>
    </nav>

    <main class="adl-app__main">
      <header class="adl-toolbar adl-glass">
        <div class="adl-toolbar__leading">
          <button type="button" class="adl-icon-button" aria-label="More" title="More" popovertarget="more-menu" style="anchor-name: --more-menu">
            <svg aria-hidden="true" viewBox="0 0 24 24" fill="currentColor"><circle cx="5" cy="12" r="2"/><circle cx="12" cy="12" r="2"/><circle cx="19" cy="12" r="2"/></svg>
          </button>
          <div id="more-menu" popover class="adl-menu adl-glass" style="position-anchor: --more-menu">
            <button type="button" class="adl-menu__item" popovertarget="more-menu" popovertargetaction="hide">Share</button>
            <button type="button" class="adl-menu__item adl-menu__item--destructive" data-open="delete-alert" popovertarget="more-menu" popovertargetaction="hide">Delete All</button>
          </div>
        </div>
        <span class="adl-toolbar__title"></span>
        <div class="adl-toolbar__trailing">
          <button type="button" class="adl-icon-button" aria-label="Add Book" title="Add Book" data-open="new-book">
            <svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 5v14M5 12h14"/></svg>
          </button>
        </div>
      </header>

      <h1 class="adl-large-title">Library</h1>

      <div class="adl-grouped">
        <fieldset class="adl-segmented">
          <legend class="adl-visually-hidden">Sort by</legend>
          <label class="adl-segmented__option"><input type="radio" name="sort" value="recent" checked>Recent</label>
          <label class="adl-segmented__option"><input type="radio" name="sort" value="title">Title</label>
        </fieldset>

        <section class="adl-list-section">
          <h2 class="adl-list-section__header">Collections</h2>
          <ul class="adl-list" role="list">
            <li><a class="adl-list__row adl-list__row--link" href="#all"><span class="adl-list__title">All Books</span><span class="adl-list__value">128</span></a></li>
            <li><a class="adl-list__row adl-list__row--link" href="#reading"><span class="adl-list__title">Reading Now</span><span class="adl-list__value">3</span></a></li>
          </ul>
          <p class="adl-list-section__footer">Tap a collection to open it.</p>
        </section>

        <section class="adl-list-section">
          <h2 class="adl-list-section__header">Options</h2>
          <ul class="adl-list" role="list">
            <li><label class="adl-list__row adl-switch-row"><span class="adl-list__title">iCloud Sync</span>
              <input class="adl-switch" type="checkbox" role="switch" checked></label></li>
          </ul>
        </section>

        <section class="adl-list-section">
          <ul class="adl-list" role="list">
            <li><button type="button" class="adl-list__row adl-list__row--destructive" data-open="delete-alert">Delete All</button></li>
          </ul>
        </section>

        <button type="button" class="adl-button adl-button--prominent" data-open="new-book">Add Book</button>
        <button type="button" class="adl-button">Sort by Title</button>
      </div>
    </main>
  </div>
</div>

<!-- Sheet: Cancel leading, confirm trailing (CMP-09) -->
<dialog id="new-book" class="adl-sheet" aria-labelledby="new-book-title">
  <form method="dialog">
    <div class="adl-sheet__header">
      <button class="adl-button adl-button--plain" value="cancel" formnovalidate>Cancel</button>
      <h2 id="new-book-title" class="adl-sheet__title">New Book</h2>
      <button class="adl-button adl-button--plain" value="add" disabled>Add</button>
    </div>
    <div class="adl-sheet__body">
      <div class="adl-field">
        <label class="adl-field__label" for="book-title">Title</label>
        <input id="book-title" class="adl-field__input" name="title" autocomplete="off" aria-describedby="book-title-hint" required>
        <p id="book-title-hint" class="adl-field__hint">Shown on the spine.</p>
      </div>
    </div>
  </form>
</dialog>

<!-- Alert: no default action here, so focus starts on the title; Esc = Cancel (CMP-13) -->
<dialog id="delete-alert" class="adl-alert" role="alertdialog" aria-labelledby="delete-title" aria-describedby="delete-message">
  <form method="dialog">
    <div class="adl-alert__content">
      <h2 id="delete-title" class="adl-alert__title" tabindex="-1" autofocus>Delete all books?</h2>
      <p id="delete-message" class="adl-alert__message">This removes 128 books from this device.</p>
    </div>
    <div class="adl-alert__actions">
      <button class="adl-button" value="cancel">Cancel</button>
      <button class="adl-button adl-button--destructive" value="delete">Delete</button>
    </div>
  </form>
</dialog>

<script>
  // Open dialogs modally; <form method="dialog"> buttons and Esc close them natively.
  document.querySelectorAll("[data-open]").forEach((button) => {
    button.addEventListener("click", () => document.getElementById(button.dataset.open).showModal());
  });
  // Enable the sheet's confirm button only when the required field has a value.
  const title = document.getElementById("book-title");
  title.addEventListener("input", () => {
    title.form.querySelector('[value="add"]').disabled = title.value.trim() === "";
  });
</script>
</body>
</html>
```

## 4. How each pattern works

- **Tab bar ⇄ sidebar.** `.adl-app` is a size container; below 48 rem of *app* width the `<nav>` floats at the bottom as a tab bar, above it the same list becomes a sidebar. Nothing is removed at any width (SYNC-01), and no device detection is involved (LAY-01). Like the system tab bar, whose labels don’t grow with Dynamic Type, the compact bar caps its label (14 px), icons, and spacing in px so four labels stay legible at 200–300% text; page zoom still enlarges everything, and the sidebar scales fully.
- **Sheet.** `showModal()` makes the page inert and traps focus; buttons inside `<form method="dialog">` close it with their `value` as `returnValue`, and Esc fires `cancel`. `formnovalidate` on Cancel lets it close even when a required field is empty. `@starting-style` animates the entrance; under Reduce Motion only opacity changes (MOT-02).
- **Alert.** With no default action (Cancel and Delete), `autofocus` puts focus on the title (`tabindex="-1"`), so Return triggers nothing risky; with a default action, put `autofocus` on that button instead (CMP-13). Keep Cancel leading with two buttons; with three, the default on top and Cancel last.
- **Menu.** `popovertarget` toggles the menu with light dismiss and Esc. `anchor-name` / `position-anchor` place it under its button in browsers with anchor positioning; others center it. `popovertargetaction="hide"` on each item closes the menu after a choice.
- **Switch.** The `<label>` row is the 44 px target (A11Y-01); `role="switch"` makes VoiceOver say “switch, on/off”. Safari 17.4+ also supports the `switch` attribute on checkboxes; the `role` works everywhere.
- **Segmented control.** Radios in a `fieldset` give one tab stop and arrow-key selection; the `legend` names the group (visually hidden when the context is clear).
- **Destructive actions.** Red text in a list row (“Delete All”) or a hairline button — never a filled red button (CMP-04, CMP-14).

## 5. Browser support and fallbacks

From MDN browser-compat-data 8.1.3 (see [`web-adaptation.md` › Browser support](web-adaptation.md#2-browser-support-verified)):

| Feature | Safari / iOS | Chrome | Firefox | Fallback |
|---|---|---|---|---|
| `<dialog>` + `showModal()` | 15.4 | 37 | 98 | — (baseline) |
| Container queries | 16 | 105 | 110 | Tab bar layout only |
| `:has()` (segmented selection) | 15.4 | 105 | 121 | Selected segment unstyled |
| `color-mix()` (secondary label, fills) | 16.2 | 111 | 113 | — |
| `popover` | 17 | 114 | 125 | — |
| `@starting-style` | 17.5 | 117 | 129 | No entrance animation |
| Anchor positioning | 26 | 125 | 147 | Menu centered |
| Invoker commands (`commandfor`) | 26.2 | 135 | 144 | Use the small script shown |

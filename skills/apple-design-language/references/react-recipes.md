# React recipes: Apple Design Language in React

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> React 19 · TypeScript · Builds on [`web-adaptation.md`](web-adaptation.md) (principles, browser support) and the shared assets [`tokens.css`](../assets/tokens.css), [`components.css`](../assets/components.css), [`tokens.ts`](../assets/tokens.ts).
> Next.js specifics: [`nextjs.md`](nextjs.md) · Tailwind: [`tailwind.md`](tailwind.md) · Native iOS from React: [`react-native.md`](react-native.md)

React is the primary web stack for this package. The components below are the **same design** as the SwiftUI guidance — one information architecture, system colors that follow appearance and Increase Contrast, text styles in `rem`, 44 px hit targets, native dialogs — expressed with web standards. Every recipe was type-checked with TypeScript (strict) against React 19 and run in Chromium with axe-core (WCAG 2.2 AA): phone and tablet widths, light, dark, Increase Contrast, and Reduce Motion.

## Contents
1. [Setup](#1-setup)
2. [Environment hooks](#2-environment-hooks)
3. [App shell: tab bar ⇄ sidebar](#3-app-shell-tab-bar--sidebar)
4. [Toolbar](#4-toolbar)
5. [Buttons](#5-buttons)
6. [Lists](#6-lists)
7. [Switch and segmented control](#7-switch-and-segmented-control)
8. [Text fields](#8-text-fields)
9. [Sheets](#9-sheets)
10. [Alerts](#10-alerts)
11. [Menus](#11-menus)
12. [Styling with tokens.ts and motion](#12-styling-with-tokensts-and-motion)
13. [Putting a screen together](#13-putting-a-screen-together)
14. [Anti-patterns → fixes](#14-anti-patterns--fixes)
15. [Testing](#15-testing)

---

## 1. Setup

Copy `tokens.css`, `components.css`, and `tokens.ts` from [`../assets/`](../assets/) into your project (they’re generated or maintained here — re-copy on updates). Load the CSS once at the root:

```tsx
// main.tsx (Vite) — or app/layout.tsx in Next.js, see nextjs.md
import "./styles/tokens.css";
import "./styles/components.css";
```

Your HTML needs the viewport and color-scheme metadata (A11Y-05, LAY-02, COL-07):

```html
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="color-scheme" content="light dark">
```

**Icons.** SF Symbols are licensed only for apps that run on Apple platforms (Xcode and Apple SDKs Agreement §2.10), so a web app must not ship them — use an open-licensed set such as Lucide (ISC), Phosphor (MIT), Heroicons (MIT), or Material Symbols (Apache 2.0). Keep the icon decorative (`aria-hidden`) and give the control a text label (A11Y-03, BRD-03).

## 2. Environment hooks

Appearance, contrast, and motion live in CSS (`tokens.css` switches every variable), so most components need no JavaScript for them. Use these hooks only when logic depends on a setting — for example choosing an animation or a canvas color. `useSyncExternalStore` keeps them correct during server rendering (the third argument supplies the server value).

```ts
import { useCallback, useSyncExternalStore } from "react";

/** Subscribe to a CSS media query. Returns `serverValue` during server rendering and hydration. */
export function useMediaQuery(query: string, serverValue = false): boolean {
  const subscribe = useCallback(
    (onChange: () => void) => {
      const list = window.matchMedia(query);
      list.addEventListener("change", onChange);
      return () => list.removeEventListener("change", onChange);
    },
    [query],
  );
  return useSyncExternalStore(
    subscribe,
    () => window.matchMedia(query).matches,
    () => serverValue,
  );
}

export const usePrefersReducedMotion = () => useMediaQuery("(prefers-reduced-motion: reduce)");
export const usePrefersMoreContrast = () => useMediaQuery("(prefers-contrast: more)");
export const usePrefersDark = () => useMediaQuery("(prefers-color-scheme: dark)");
```

## 3. App shell: tab bar ⇄ sidebar

Define the top-level sections **once** and render them with one component. `components.css` presents the same `<nav>` as a floating tab bar in compact widths and a sidebar in regular widths, using a container query on the app’s own width — never the device (LAY-01, NAV-06, SYNC-01). Links, not buttons: tabs navigate and never act (NAV-01); the current section carries `aria-current="page"`. Show every section always — never disable or hide one (NAV-03); keep labels to one word (NAV-04).

```tsx
import type { ReactNode } from "react";

export type Section = { id: string; title: string; href: string; icon: ReactNode };

/** One information architecture, rendered as a tab bar (compact) or sidebar (regular) by components.css. */
export function AppShell({ sections, currentId, children }: {
  sections: readonly Section[];
  currentId: string;
  children: ReactNode;
}) {
  return (
    <div className="adl-app">
      <div className="adl-app__layout">
        <nav className="adl-nav adl-glass" aria-label="Primary">
          <ul className="adl-nav__list">
            {sections.map((s) => (
              <li key={s.id}>
                <a
                  className="adl-nav__link"
                  href={s.href}
                  aria-current={s.id === currentId ? "page" : undefined}
                >
                  <span aria-hidden="true">{s.icon}</span>
                  <span>{s.title}</span>
                </a>
              </li>
            ))}
          </ul>
        </nav>
        <main className="adl-app__main">{children}</main>
      </div>
    </div>
  );
}
```

With a router, derive `currentId` from the location (React Router `useLocation`, Next.js `usePathname`) and render the router’s link component with the same class and `aria-current`.

## 4. Toolbar

Leading items, an optional title, trailing items with the single prominent action last (NAV-11). Use icon buttons with labels (A11Y-03) and keep brand color out of the bar (GLS-04). When the page shows a large title, leave the toolbar title out (NAV-15).

```tsx
import type { ReactNode } from "react";

/**
 * A top bar: leading items, an optional short title, trailing items with the one prominent action last (NAV-11).
 * Omit `title` when the page shows a large title (NAV-15), so the name isn't repeated.
 */
export function Toolbar({ title, leading, trailing }: { title?: string; leading?: ReactNode; trailing?: ReactNode }) {
  return (
    <header className="adl-toolbar adl-glass">
      <div className="adl-toolbar__leading">{leading}</div>
      {title ? <h1 className="adl-toolbar__title">{title}</h1> : <span className="adl-toolbar__title" />}
      <div className="adl-toolbar__trailing">{trailing}</div>
    </header>
  );
}
```

## 5. Buttons

Three styles distinguish choices without changing size (CMP-02): `prominent` (accent fill — at most one or two per view, CMP-01), `bordered` (default), and `plain` (toolbars, sheet headers). The union type makes a prominent destructive button a compile error (CMP-04). Icon-only buttons require a `label` (A11Y-03).

```tsx
import type { ButtonHTMLAttributes, ReactNode } from "react";

type Base = Omit<ButtonHTMLAttributes<HTMLButtonElement>, "className">;

/** Prominent buttons can't be destructive (CMP-04); the type system enforces it. */
export type ButtonProps = Base &
  (
    | { variant: "prominent"; destructive?: never }
    | { variant?: "bordered" | "plain"; destructive?: boolean }
  );

export function Button({ variant = "bordered", destructive, type = "button", ...rest }: ButtonProps) {
  const classes = ["adl-button"];
  if (variant !== "bordered") classes.push(`adl-button--${variant}`);
  if (destructive) classes.push("adl-button--destructive");
  return <button type={type} className={classes.join(" ")} {...rest} />;
}

/** Icon-only buttons require a label: it becomes the accessible name and the pointer tooltip (A11Y-03). */
export function IconButton({ label, icon, type = "button", ...rest }: Base & { label: string; icon: ReactNode }) {
  return (
    <button type={type} className="adl-icon-button" aria-label={label} title={label} {...rest}>
      <span aria-hidden="true">{icon}</span>
    </button>
  );
}
```

Colored text meets WCAG 2.2 AA (4.5:1) only on the page background or a list row — no HIG blue or red reaches 4.5:1 on gray fills in light mode — so bordered buttons use the label color, and destructive actions use red text on a row or a hairline button (`--adl-accent-text`, `--adl-destructive-text` in `tokens.css`).

## 6. Lists

Inset grouped lists carry most settings and navigation screens. Rows are at least 44 px tall; rows that navigate show a disclosure indicator (CMP-19); an action row such as “Delete All” uses red text (CMP-14).

```tsx
import type { ReactNode } from "react";

/** An inset grouped list section: header, rows, optional footer (CMP-19). */
export function ListSection({ header, footer, children }: { header?: string; footer?: string; children: ReactNode }) {
  return (
    <section className="adl-list-section">
      {header ? <h2 className="adl-list-section__header">{header}</h2> : null}
      <ul className="adl-list" role="list">
        {children}
      </ul>
      {footer ? <p className="adl-list-section__footer">{footer}</p> : null}
    </section>
  );
}

/** A row that navigates shows a disclosure indicator; a row with a value shows it trailing. */
export function LinkRow({ href, title, value }: { href: string; title: string; value?: string }) {
  return (
    <li>
      <a className="adl-list__row adl-list__row--link" href={href}>
        <span className="adl-list__title">{title}</span>
        {value ? <span className="adl-list__value">{value}</span> : null}
      </a>
    </li>
  );
}

/** A row that performs an action, such as “Delete All” in red (CMP-14). */
export function ActionRow({ title, destructive, onSelect }: { title: string; destructive?: boolean; onSelect: () => void }) {
  return (
    <li>
      <button
        type="button"
        className={`adl-list__row ${destructive ? "adl-list__row--destructive" : "adl-list__row--action"}`}
        onClick={onSelect}
      >
        {title}
      </button>
    </li>
  );
}
```

## 7. Switch and segmented control

Switches live in list rows, and the whole row is the hit target (CMP-23, A11Y-01). The native checkbox with `role="switch"` gives VoiceOver the right role and state; the thumb position shows state as well as the color (COL-03).

```tsx
import { useId } from "react";

/** A switch in a list row: the whole row is the 44 px hit target (A11Y-01, CMP-23). */
export function SwitchRow({ label, checked, onChange, disabled }: {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
}) {
  const id = useId();
  return (
    <label className="adl-list__row adl-switch-row" htmlFor={id}>
      <span className="adl-list__title">{label}</span>
      <input
        id={id}
        className="adl-switch"
        type="checkbox"
        role="switch"
        checked={checked}
        disabled={disabled}
        onChange={(e) => onChange(e.currentTarget.checked)}
      />
    </label>
  );
}
```

A segmented control picks one of a few options (CMP-24, CMP-25). Native radio buttons in a `fieldset` provide grouping, arrow-key selection, and state for free. When the segments switch *views* rather than a value, use the WAI-ARIA tabs pattern (`tablist`/`tab`/`tabpanel`) instead.

```tsx
import { useId } from "react";

/** A segmented control for choosing one option: native radios give arrow keys and grouping for free. */
export function SegmentedPicker<T extends string>({ label, options, value, onChange }: {
  label: string;
  options: readonly { value: T; title: string }[];
  value: T;
  onChange: (value: T) => void;
}) {
  const name = useId();
  return (
    <fieldset className="adl-segmented">
      <legend className="adl-visually-hidden">{label}</legend>
      {options.map((o) => (
        <label key={o.value} className="adl-segmented__option">
          <input
            type="radio"
            name={name}
            value={o.value}
            checked={o.value === value}
            onChange={() => onChange(o.value)}
          />
          {o.title}
        </label>
      ))}
    </fieldset>
  );
}
```

## 8. Text fields

Every field has a visible label. Set `type`, `autoComplete`, `inputMode`, and `enterKeyHint` for the content (CMP-22); passwords use `type="password"` with `autoComplete="current-password"` or `"new-password"` and are never prefilled (CMP-21). Errors say how to fix the problem (WRT-07) and are shown by text and a border, not color alone (COL-03).

```tsx
import { useId, type InputHTMLAttributes } from "react";

/**
 * A labeled field. Pass `type="password"` with autoComplete "current-password" or "new-password" for secure
 * entry (CMP-21). Errors say how to fix the problem and are announced with the field (WRT-07, COL-03).
 */
export function TextField({ label, hint, error, ...input }: Omit<InputHTMLAttributes<HTMLInputElement>, "id" | "className"> & {
  label: string;
  hint?: string;
  error?: string;
}) {
  const id = useId();
  const hintId = `${id}-hint`;
  const errorId = `${id}-error`;
  const describedBy = [hint ? hintId : null, error ? errorId : null].filter(Boolean).join(" ") || undefined;
  return (
    <div className="adl-field">
      <label className="adl-field__label" htmlFor={id}>{label}</label>
      <input
        id={id}
        className="adl-field__input"
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy}
        {...input}
      />
      {hint ? <p id={hintId} className="adl-field__hint">{hint}</p> : null}
      {error ? <p id={errorId} className="adl-field__error">{error}</p> : null}
    </div>
  );
}
```

## 9. Sheets

Build modals on the native `<dialog>` with `showModal()`: the browser provides focus containment, an inert page behind, top-layer stacking, and Esc. Present one modal at a time (CMP-07) with an obvious dismissal (CMP-08): Cancel on the leading edge, the confirming action on the trailing edge (CMP-09). In compact widths the sheet rises from the bottom; in regular widths it’s a centered card. If a sheet holds unsaved changes, confirm before discarding them.

```tsx
import { useEffect, useId, useRef, type ReactNode } from "react";

/**
 * A modal sheet on the native <dialog>: focus containment, Esc to dismiss, and an inert page come from the
 * browser. Cancel sits on the leading edge, the confirming action on the trailing edge (CMP-08, CMP-09).
 */
export function Sheet({ open, title, onCancel, confirm, children }: {
  open: boolean;
  title: string;
  onCancel: () => void;
  confirm?: { label: string; onConfirm: () => void; disabled?: boolean };
  children: ReactNode;
}) {
  const ref = useRef<HTMLDialogElement>(null);
  const titleId = useId();

  useEffect(() => {
    const dialog = ref.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  }, [open]);

  return (
    <dialog
      ref={ref}
      className="adl-sheet"
      aria-labelledby={titleId}
      onCancel={(e) => {
        e.preventDefault(); // Esc: let the parent decide, so state stays the single source of truth
        onCancel();
      }}
    >
      <div className="adl-sheet__header">
        <button type="button" className="adl-button adl-button--plain" onClick={onCancel}>
          Cancel
        </button>
        <h2 id={titleId} className="adl-sheet__title">{title}</h2>
        {confirm ? (
          <button
            type="button"
            className="adl-button adl-button--plain"
            onClick={confirm.onConfirm}
            disabled={confirm.disabled}
          >
            {confirm.label}
          </button>
        ) : null}
      </div>
      <div className="adl-sheet__body">{children}</div>
    </dialog>
  );
}
```

## 10. Alerts

Use alerts rarely, for critical, actionable information (CMP-11). Title them specifically — never just “Error” — and give one to three verb-titled buttons, “Cancel” to cancel, never “Yes”/“No” (CMP-12, CMP-13). The tuple type caps buttons at three. Cancel is never the default and a destructive action is never prominent: initial focus goes to the default action, or to the title when there is none, so Return never triggers a risky choice.

```tsx
import { useEffect, useId, useRef } from "react";

export type AlertAction = { label: string; role?: "default" | "cancel" | "destructive"; onSelect: () => void };

/**
 * An alert: a specific title, an optional message, and one to three verb-titled buttons (CMP-11 – CMP-13).
 * Two buttons sit side by side with Cancel leading; three stack with the default on top and Cancel last.
 * Cancel is never the default and a destructive action is never prominent (CMP-04, CMP-13): initial focus goes
 * to the default action, or to the title when there is none, so Return never triggers a risky choice.
 */
export function Alert({ open, title, message, actions }: {
  open: boolean;
  title: string;
  message?: string;
  actions: [AlertAction] | [AlertAction, AlertAction] | [AlertAction, AlertAction, AlertAction];
}) {
  const ref = useRef<HTMLDialogElement>(null);
  const titleId = useId();
  const messageId = useId();
  const cancel = actions.find((a) => a.role === "cancel");
  const primary = actions.find((a) => (a.role ?? "default") === "default");
  const rank = (a: AlertAction) => (a === primary ? 0 : a === cancel ? 2 : 1);
  const ordered =
    actions.length === 3
      ? [...actions].sort((a, b) => rank(a) - rank(b))
      : [...actions].sort((a, b) => (a === cancel ? -1 : b === cancel ? 1 : 0));

  useEffect(() => {
    const dialog = ref.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  }, [open]);

  return (
    <dialog
      ref={ref}
      className="adl-alert"
      role="alertdialog"
      aria-labelledby={titleId}
      aria-describedby={message ? messageId : undefined}
      onCancel={(e) => {
        e.preventDefault();
        // Esc means Cancel; a single-button informational alert treats Esc as its OK.
        (cancel ?? (actions.length === 1 ? actions[0] : undefined))?.onSelect();
      }}
    >
      <div className="adl-alert__content">
        <h2 id={titleId} className="adl-alert__title" tabIndex={-1} autoFocus={!primary}>
          {title}
        </h2>
        {message ? <p id={messageId} className="adl-alert__message">{message}</p> : null}
      </div>
      <div className="adl-alert__actions">
        {ordered.map((a) => (
          <button
            key={a.label}
            type="button"
            autoFocus={a === primary}
            className={
              a === primary
                ? "adl-button adl-button--prominent"
                : a.role === "destructive"
                  ? "adl-button adl-button--destructive"
                  : "adl-button"
            }
            onClick={a.onSelect}
          >
            {a.label}
          </button>
        ))}
      </div>
    </dialog>
  );
}
```

## 11. Menus

The popover API gives light dismiss, Esc, and top-layer stacking without a library. Order items by frequency, put destructive items last in red (CMP-17), and keep one menu open at a time (CMP-16). The menu anchors below its button where CSS anchor positioning is supported (Safari 26, Chrome 125, Firefox 147) and centers before that. For full menu keyboard semantics (arrow keys, type-ahead), follow the WAI-ARIA menu button pattern.

```tsx
import { useId, useRef, type ReactNode } from "react";

export type MenuItem = { label: string; icon?: ReactNode; destructive?: boolean; onSelect: () => void };

/**
 * A pull-down menu on the popover API: light dismiss, Esc, and top-layer stacking come from the browser.
 * Anchored to its button where CSS anchor positioning is supported (Safari 26+), centered before that.
 */
export function ActionMenu({ label, icon, items }: { label: string; icon: ReactNode; items: readonly MenuItem[] }) {
  const id = useId();
  const menuId = `menu-${id.replace(/[^a-zA-Z0-9_-]/g, "")}`;
  const anchor = `--${menuId}`;
  const ref = useRef<HTMLDivElement>(null);

  return (
    <>
      <button
        type="button"
        className="adl-icon-button"
        aria-label={label}
        title={label}
        popoverTarget={menuId}
        style={{ anchorName: anchor }}
      >
        <span aria-hidden="true">{icon}</span>
      </button>
      <div
        ref={ref}
        id={menuId}
        popover="auto"
        className="adl-menu adl-glass"
        style={{ positionAnchor: anchor }}
      >
        {items.map((item) => (
          <button
            key={item.label}
            type="button"
            className={item.destructive ? "adl-menu__item adl-menu__item--destructive" : "adl-menu__item"}
            onClick={() => {
              ref.current?.hidePopover();
              item.onSelect();
            }}
          >
            {item.icon ? <span aria-hidden="true">{item.icon}</span> : null}
            {item.label}
          </button>
        ))}
      </div>
    </>
  );
}
```

## 12. Styling with tokens.ts and motion

`tokens.ts` exports CSS-variable references, so inline styles and CSS-in-JS follow appearance and contrast automatically (COL-01, COL-02):

```tsx
import { color, text, layout } from "./styles/tokens";

export function Badge({ count }: { count: number }) {
  return (
    <span style={{ ...text.caption1, color: color.onAccent, background: color.accentFill, borderRadius: 999, padding: "0 6px" }}>
      {count}
    </span>
  );
}

export const floatingButtonInset = { bottom: `calc(${layout.safeBottom} + 16px)` };
```

Animate only to explain change, and honor Reduce Motion (MOT-01, MOT-02). CSS transitions that use `var(--adl-motion-duration)` shrink to 1 ms automatically under Reduce Motion; for JavaScript-driven motion, branch on the hook:

```ts
import { usePrefersReducedMotion } from "./hooks";

export function useEntranceAnimation(element: HTMLElement | null) {
  const reduced = usePrefersReducedMotion();
  return () =>
    element?.animate(
      reduced ? [{ opacity: 0 }, { opacity: 1 }] : [{ opacity: 0, translate: "0 12px" }, { opacity: 1, translate: "0 0" }],
      { duration: reduced ? 150 : 300, easing: "cubic-bezier(0.2, 0, 0, 1)" },
    );
}
```

## 13. Putting a screen together

```tsx
import { useState } from "react";
import { createRoot } from "react-dom/client";
import { House, Search, Settings, Plus, Ellipsis, Share, Trash2, Library } from "lucide-react";
import { AppShell, type Section } from "./AppShell";
import { Toolbar } from "./Toolbar";
import { Button, IconButton } from "./Button";
import { SwitchRow } from "./Switch";
import { SegmentedPicker } from "./SegmentedPicker";
import { Sheet } from "./Sheet";
import { Alert } from "./Alert";
import { ActionMenu } from "./ActionMenu";
import { ListSection, LinkRow, ActionRow } from "./List";
import { TextField } from "./TextField";
import { usePrefersReducedMotion } from "./hooks";

const sections = [
  { id: "home", title: "Home", href: "#home", icon: <House /> },
  { id: "library", title: "Library", href: "#library", icon: <Library /> },
  { id: "search", title: "Search", href: "#search", icon: <Search /> },
  { id: "settings", title: "Settings", href: "#settings", icon: <Settings /> },
] as const satisfies readonly Section[];

function App() {
  const [sync, setSync] = useState(true);
  const [sort, setSort] = useState<"recent" | "title">("recent");
  const [sheet, setSheet] = useState(false);
  const [alert, setAlert] = useState(false);
  const [name, setName] = useState("");
  const reduced = usePrefersReducedMotion();
  return (
    <AppShell sections={sections} currentId="library">
      <Toolbar
        leading={<ActionMenu label="More" icon={<Ellipsis />} items={[
          { label: "Share", icon: <Share />, onSelect: () => {} },
          { label: "Delete All", icon: <Trash2 />, destructive: true, onSelect: () => setAlert(true) },
        ]} />}
        trailing={<IconButton label="Add Book" icon={<Plus />} onClick={() => setSheet(true)} />}
      />
      <h1 className="adl-large-title">Library</h1>
      <div className="adl-grouped">
        <SegmentedPicker label="Sort by" value={sort} onChange={setSort}
          options={[{ value: "recent", title: "Recent" }, { value: "title", title: "Title" }]} />
        <ListSection header="Collections" footer={reduced ? "Reduce Motion is on." : "Tap a collection to open it."}>
          <LinkRow href="#all" title="All Books" value="128" />
          <LinkRow href="#reading" title="Reading Now" value="3" />
        </ListSection>
        <ListSection header="Options">
          <li><SwitchRow label="iCloud Sync" checked={sync} onChange={setSync} /></li>
        </ListSection>
        <ListSection>
          <ActionRow title="Delete All" destructive onSelect={() => setAlert(true)} />
        </ListSection>
        <Button variant="prominent" onClick={() => setSheet(true)}>Add Book</Button>{" "}
        <Button onClick={() => setSort("title")}>Sort by Title</Button>
      </div>
      <Sheet open={sheet} title="New Book" onCancel={() => setSheet(false)}
        confirm={{ label: "Add", onConfirm: () => setSheet(false), disabled: name.trim() === "" }}>
        <TextField label="Title" value={name} onChange={(e) => setName(e.currentTarget.value)}
          hint="Shown on the spine." error={name.length > 40 ? "Use 40 characters or fewer." : undefined} />
      </Sheet>
      <Alert open={alert} title="Delete all books?" message="This removes 128 books from this device."
        actions={[{ label: "Cancel", role: "cancel", onSelect: () => setAlert(false) },
                  { label: "Delete", role: "destructive", onSelect: () => setAlert(false) }]} />
    </AppShell>
  );
}

createRoot(document.getElementById("root")!).render(<App />);
```

## 14. Anti-patterns → fixes

| Don’t | Do | Rule |
|---|---|---|
| `if (/iPhone/.test(navigator.userAgent))` to pick a layout | Container or media queries on available width | LAY-01 |
| `<div onClick>` as a button | `<button type="button">` (keyboard, focus, role for free) | A11Y-03, A11Y-07 |
| Icon-only `<button><Icon /></button>` | `aria-label` (the `IconButton` recipe requires it) | A11Y-03 |
| `style={{ color: "#0088FF" }}` | `color.accentText` / `var(--adl-accent-text)` | COL-01 |
| `fontSize: 10` or fixed `px` text | `text.*` styles in `rem`, at least 11 px | TYP-01, TYP-02 |
| Theme toggle stored in `localStorage` | Follow the system appearance (`color-scheme: light dark`) | COL-07 |
| A tab bar item that opens a composer | A toolbar button; tabs only navigate | NAV-01 |
| Hiding a tab when it has no content | Keep it; show an empty state that explains why | NAV-03 |
| A custom modal `<div>` with a focus trap library | `<dialog>` + `showModal()` | CMP-07, CMP-08 |
| Alert buttons “Yes” / “No” | Verbs (“Delete”, “Keep Editing”) and “Cancel” | CMP-13 |
| Spinning loaders that ignore Reduce Motion | `usePrefersReducedMotion` or `motion-safe` CSS | MOT-02 |
| SF Symbols SVGs in a web app | An open-licensed icon set | BRD-03 |
| `maximumScale: 1` / `user-scalable=no` | Leave zoom enabled | A11Y-05 |

## 15. Testing

- **Automated:** run `python3 hooks/scripts/hig_lint.py src/` for the rule checks, and axe-core (e.g., `@axe-core/playwright`) for WCAG.
- **Settings:** Playwright’s `page.emulateMedia({ colorScheme, reducedMotion, contrast })` covers light/dark, Reduce Motion, and Increase Contrast; test at 390 px and 1024 px widths at least.
- **On devices:** VoiceOver on iOS and macOS Safari, 200% text size and zoom, dark mode, Increase Contrast, Reduce Motion, and a right-to-left locale (`<html dir="rtl">`).

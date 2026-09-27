# Tailwind CSS recipes

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> Tailwind CSS v4 · Theme: [`../assets/tailwind.css`](../assets/tailwind.css) (generated from `tokens.json`) · Principles: [`web-adaptation.md`](web-adaptation.md) · Component logic: [`react-recipes.md`](react-recipes.md)

The generated theme maps Tailwind utilities onto `tokens.css`, so `bg-background`, `text-label`, `text-accent-text`, `text-body`, and `min-h-control` follow light, dark, and Increase Contrast automatically — the same values the SwiftUI, React, and HTML recipes use. The components below were type-checked, compiled with the Tailwind v4 CLI, and run in Chromium with axe-core (WCAG 2.2 AA) at phone and tablet widths in light, dark, Increase Contrast, and Reduce Motion; they render the same screen as the other stacks.

## Contents
1. [Setup](#1-setup)
2. [Utility map](#2-utility-map)
3. [App shell with container queries](#3-app-shell-with-container-queries)
4. [Buttons](#4-buttons)
5. [Lists and switches](#5-lists-and-switches)
6. [Sheets with dialog variants](#6-sheets-with-dialog-variants)
7. [Variants that carry accessibility](#7-variants-that-carry-accessibility)
8. [Don’t](#8-dont)

---

## 1. Setup

Copy `tokens.css` and `tailwind.css` (and optionally `components.css`) next to your main stylesheet:

```css
@import "tailwindcss";
@import "./tailwind.css";                          /* theme + tokens.css in the base layer */
@import "./components.css" layer(components);      /* optional: dialogs, menus, fields ready-made */
```

`tailwind.css` imports `tokens.css` into the `base` layer and declares the theme with `@theme inline`, which Tailwind requires when theme variables reference other variables. Utilities always win over the imported component styles because both sit in lower layers.

## 2. Utility map

| Need | Utilities | Rule |
|---|---|---|
| Page and grouped backgrounds | `bg-background`, `bg-background-grouped`, `bg-background-grouped-row` | COL-01 |
| Text colors | `text-label`, `text-secondary-label`, `text-accent-text`, `text-destructive-text` | COL-01, COL-06 |
| Fills | `bg-fill` (controls), `bg-accent-fill` + `text-on-accent` (prominent) | CMP-01 |
| System colors | `text-blue`, `bg-green`, `border-separator`, … (12 colors, 6 grays) | COL-01 |
| Text styles | `text-large-title` … `text-caption2` (size, leading, weight in `rem`) | TYP-01 |
| Fonts | `font-sans` (system stack), `font-rounded`, `font-serif`, `font-mono` | TYP-04 |
| Hit targets | `min-h-control`, `min-w-control`, `size-control` (44 px) | A11Y-01 |
| Safe areas | `pb-[env(safe-area-inset-bottom)]`, or `var(--adl-safe-*)` | LAY-02 |
| Glass bars | `adl-glass` (from tokens.css) on bars and controls only | GLS-01, LAY-08 |

Colored text reaches WCAG 2.2 AA only on `bg-background` or `bg-background-grouped-row` in light mode — no HIG blue or red reaches 4.5:1 on gray fills — so put `text-accent-text` and `text-destructive-text` there, and use `text-label` on `bg-fill`.

## 3. App shell with container queries

`@container` on the shell and `@3xl:` variants (48 rem of *app* width) switch the tab bar to a sidebar — the same breakpoint as `components.css`, and never a device check (LAY-01, NAV-06).

```tsx
import type { ReactNode } from "react";

export type Section = { id: string; title: string; href: string; icon: ReactNode };

/**
 * Tab bar below 48rem of app width, sidebar above it — a container query, never the device (LAY-01, NAV-06).
 * Like the system tab bar, the compact bar caps its label, icon, and spacing in px so labels stay legible at large
 * text sizes; the sidebar scales fully.
 */
export function AppShell({ sections, currentId, children }: {
  sections: readonly Section[];
  currentId: string;
  children: ReactNode;
}) {
  return (
    <div className="@container min-h-dvh bg-background text-label">
      <div className="grid min-h-dvh grid-cols-1 @3xl:grid-cols-[16rem_minmax(0,1fr)]">
        <nav
          aria-label="Primary"
          className="adl-glass fixed inset-x-[16px] bottom-[max(12px,env(safe-area-inset-bottom))] z-10 rounded-full p-[4px] shadow-lg
                     @3xl:sticky @3xl:inset-auto @3xl:top-0 @3xl:h-dvh @3xl:rounded-none @3xl:border-0 @3xl:border-e @3xl:border-separator @3xl:p-3 @3xl:shadow-none"
        >
          <ul className="flex justify-around gap-[4px] @3xl:flex-col @3xl:justify-start @3xl:gap-0.5">
            {sections.map((s) => (
              <li key={s.id} className="min-w-0 flex-1 @3xl:flex-none">
                <a
                  href={s.href}
                  aria-current={s.id === currentId ? "page" : undefined}
                  className="flex min-h-control min-w-control flex-col items-center justify-center gap-0.5 rounded-full px-[min(0.5rem,8px)] py-[min(0.375rem,6px)] text-[min(0.6875rem,14px)]/[1.2] font-semibold
                             aria-[current=page]:bg-background-grouped-row aria-[current=page]:text-accent-text aria-[current=page]:shadow-sm
                             @3xl:flex-row @3xl:justify-start @3xl:gap-3 @3xl:rounded-[0.625rem] @3xl:px-3 @3xl:text-body @3xl:font-normal
                             @3xl:aria-[current=page]:bg-accent-fill @3xl:aria-[current=page]:text-on-accent @3xl:aria-[current=page]:font-semibold
                             contrast-more:aria-[current=page]:outline-2 contrast-more:aria-[current=page]:outline-accent"
                >
                  <span aria-hidden="true" className="*:size-[min(1.5rem,28px)] @3xl:*:size-6">{s.icon}</span>
                  <span className="min-w-0 max-w-full truncate">{s.title}</span>
                </a>
              </li>
            ))}
          </ul>
        </nav>
        <main className="min-w-0 pb-[calc(var(--adl-control-size)+2.5rem+env(safe-area-inset-bottom))] @3xl:pb-0">{children}</main>
      </div>
    </div>
  );
}
```

## 4. Buttons

```tsx
import type { ButtonHTMLAttributes } from "react";

const base =
  "inline-flex min-h-control min-w-control items-center justify-center gap-1.5 rounded-full px-3 text-body font-semibold " +
  "transition-opacity active:opacity-60 disabled:cursor-not-allowed disabled:opacity-40 motion-reduce:transition-none";

const styles = {
  prominent: "bg-accent-fill text-on-accent",
  bordered: "bg-fill text-label contrast-more:outline contrast-more:outline-label",
  plain: "px-2 text-accent-text",
  destructive: "text-destructive-text ring-1 ring-inset ring-current", // never a fill (CMP-04)
} as const;

type Props = Omit<ButtonHTMLAttributes<HTMLButtonElement>, "className"> & { variant?: keyof typeof styles };

/** Styles differ, sizes don't (CMP-02); every style has a press state (CMP-03). */
export function Button({ variant = "bordered", type = "button", ...rest }: Props) {
  return <button type={type} className={`${base} ${styles[variant]}`} {...rest} />;
}
```

## 5. Lists and switches

```tsx
import { useId, type ReactNode } from "react";

export function ListSection({ header, footer, children }: { header?: string; footer?: string; children: ReactNode }) {
  return (
    <section className="mb-6">
      {header ? <h2 className="px-4 py-1.5 text-footnote font-semibold text-secondary-label">{header}</h2> : null}
      <ul role="list" className="overflow-hidden rounded-xl bg-background-grouped-row">
        {children}
      </ul>
      {footer ? <p className="px-4 py-1.5 text-footnote text-secondary-label">{footer}</p> : null}
    </section>
  );
}

// Inset separator between rows, starting at the text's leading edge
const row =
  "relative flex min-h-control w-full items-center gap-3 px-4 py-2 text-start " +
  "[li+li>&]:before:absolute [li+li>&]:before:start-4 [li+li>&]:before:end-0 [li+li>&]:before:top-0 [li+li>&]:before:border-t [li+li>&]:before:border-separator";

export function LinkRow({ href, title, value }: { href: string; title: string; value?: string }) {
  return (
    <li>
      <a href={href} className={`${row} text-label active:bg-fill`}>
        <span className="min-w-0 flex-1">{title}</span>
        {value ? <span className="text-secondary-label">{value}</span> : null}
        {/* disclosure indicator, mirrored in right-to-left (CMP-19) */}
        <span aria-hidden="true" className="me-1 size-2 rotate-45 border-e-2 border-t-2 border-secondary-label rtl:-rotate-135" />
      </a>
    </li>
  );
}

export function ActionRow({ title, destructive, onSelect }: { title: string; destructive?: boolean; onSelect: () => void }) {
  return (
    <li>
      <button type="button" onClick={onSelect} className={`${row} ${destructive ? "text-destructive-text" : "text-accent-text"} active:bg-fill`}>
        {title}
      </button>
    </li>
  );
}

/** A switch row: the label is the 44 px target; the thumb position shows state, not just color (COL-03). */
export function SwitchRow({ label, checked, onChange }: { label: string; checked: boolean; onChange: (v: boolean) => void }) {
  const id = useId();
  return (
    <li>
      <label htmlFor={id} className={`${row} cursor-pointer`}>
        <span className="min-w-0 flex-1">{label}</span>
        <input
          id={id}
          type="checkbox"
          role="switch"
          checked={checked}
          onChange={(e) => onChange(e.currentTarget.checked)}
          className="relative h-[1.9375rem] w-[3.1875rem] shrink-0 cursor-pointer appearance-none rounded-full bg-fill transition-colors checked:bg-green
                     before:absolute before:start-0.5 before:top-0.5 before:size-[1.6875rem] before:rounded-full before:bg-white before:shadow before:transition-transform
                     checked:before:translate-x-5 rtl:checked:before:-translate-x-5 motion-reduce:transition-none motion-reduce:before:transition-none
                     contrast-more:outline contrast-more:outline-label"
        />
      </label>
    </li>
  );
}
```

## 6. Sheets with dialog variants

`open:`, `backdrop:`, and `starting:` style the native `<dialog>`; `transition-discrete` lets it animate in and out of the top layer; `motion-reduce:` keeps only the fade (MOT-02). The behavior is the React [Sheet](react-recipes.md#9-sheets) recipe.

```tsx
import { useEffect, useId, useRef, type ReactNode } from "react";

/** The Sheet recipe from react-recipes.md, styled with Tailwind's open:, backdrop:, and starting: variants. */
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
    const d = ref.current;
    if (open && d && !d.open) d.showModal();
    if (!open && d?.open) d.close();
  }, [open]);

  return (
    <dialog
      ref={ref}
      aria-labelledby={titleId}
      onCancel={(e) => {
        e.preventDefault();
        onCancel();
      }}
      className="mt-auto mb-0 max-h-[92dvh] w-full max-w-none translate-y-8 rounded-t-[1.25rem] bg-background-grouped-row pb-[env(safe-area-inset-bottom)] text-label opacity-0
                 transition-all transition-discrete duration-300 backdrop:bg-black/30 open:translate-y-0 open:opacity-100 starting:open:translate-y-8 starting:open:opacity-0
                 motion-reduce:translate-y-0 motion-reduce:starting:open:translate-y-0 md:m-auto md:w-[min(36rem,calc(100%-4rem))] md:rounded-[1.25rem] md:pb-0
                 contrast-more:outline contrast-more:outline-label"
    >
      <div className="sticky top-0 flex min-h-control items-center gap-2 bg-inherit p-2">
        <button type="button" onClick={onCancel} className="min-h-control min-w-control rounded-full px-2 text-body font-semibold text-accent-text">Cancel</button>
        <h2 id={titleId} className="flex-1 text-center text-headline">{title}</h2>
        {confirm ? (
          <button type="button" onClick={confirm.onConfirm} disabled={confirm.disabled}
            className="min-h-control min-w-control rounded-full px-2 text-body font-semibold text-accent-text disabled:opacity-40">
            {confirm.label}
          </button>
        ) : null}
      </div>
      <div className="overflow-y-auto px-4 pb-6">{children}</div>
    </dialog>
  );
}
```

Alerts, menus, the segmented control, and text fields follow the same pattern; the verified demo reuses them from [`react-recipes.md`](react-recipes.md) with `components.css` imported in the components layer.

## 7. Variants that carry accessibility

| Variant | Use it for | Rule |
|---|---|---|
| `motion-reduce:` / `motion-safe:` | Remove movement; keep fades | MOT-02 |
| `contrast-more:` | Add outlines and borders under Increase Contrast (colors already switch via tokens) | COL-02, COL-06 |
| `forced-colors:` | Windows High Contrast adjustments | A11Y-07 |
| `aria-[current=page]:`, `aria-checked:`, `aria-expanded:` | Style from ARIA state so visuals and semantics can’t drift | A11Y-03 |
| `focus-visible:` | Visible keyboard focus (tokens.css already sets an outline) | A11Y-07 |
| `rtl:` / `ltr:` and logical utilities (`ms-*`, `pe-*`, `start-*`) | Right-to-left layouts | L10N-02 |
| `@3xl:` (container) | Layout from available space | LAY-01 |
| `pointer-coarse:` | Never to *shrink* targets — 44 px applies everywhere | A11Y-01 |

## 8. Don’t

| Don’t | Why | Do |
|---|---|---|
| `bg-[#007AFF]`, `text-[#FF3B30]` | Hard-coded; ignores dark mode and Increase Contrast | `bg-accent-fill`, `text-destructive-text` (COL-01) |
| `dark:bg-gray-900` on themed surfaces | Duplicates what tokens already switch; drifts | `bg-background`, `bg-background-grouped-row` |
| `text-[10px]`, `text-xs` for body copy | Below the 11 px minimum or off the type ramp | `text-caption2` at the smallest (TYP-02) |
| `font-light`, `font-thin` | Hard to read in interface text | `font-normal` … `font-bold` (TYP-03) |
| `h-8 w-8` on a button | 32 px hit target | `min-h-control min-w-control` (A11Y-01) |
| A class-based theme toggle (`.dark` on `<html>`) | Overrides the system appearance | Keep Tailwind’s default `prefers-color-scheme` behavior (COL-07) |
| `adl-glass` on cards and content | Glass belongs to the functional layer | Plain `bg-background-grouped-row` (GLS-01) |

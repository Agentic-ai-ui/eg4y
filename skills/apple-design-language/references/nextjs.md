# Next.js recipes

> Part of the **apple-design-language** skill — Created by Edison Augustin X.
> Next.js 16 App Router · Components: [`react-recipes.md`](react-recipes.md) · Principles: [`web-adaptation.md`](web-adaptation.md)

Next.js adds three things on top of the React recipes: the document metadata (viewport, color scheme, theme color, home-screen web app), the server/client component split, and routing-aware navigation. The files below were built with `next build` (16.3); the prerendered HTML contains `viewport-fit=cover`, `color-scheme: light dark`, per-appearance `theme-color`, no zoom lock, and `aria-current="page"` on the current section.

## Contents
1. [Root layout: viewport and metadata](#1-root-layout-viewport-and-metadata)
2. [App shell with routing](#2-app-shell-with-routing)
3. [Server and client components](#3-server-and-client-components)
4. [Fonts, images, and icons](#4-fonts-images-and-icons)
5. [Checklist](#5-checklist)

---

## 1. Root layout: viewport and metadata

`viewport` and `metadata` are exported from a Server Component layout. Next.js already emits `width=device-width, initial-scale=1`; add `viewportFit: "cover"` so `env(safe-area-inset-*)` reports real insets (LAY-02), and `colorScheme: "light dark"` so form controls and scrollbars follow the appearance (COL-07). The Next.js docs show `maximumScale: 1` and `userScalable: false` for completeness — **don’t use them**; they block zoom (A11Y-05).

<!-- source: tests/web/nextjs/app/layout.tsx -->
```tsx
import type { Metadata, Viewport } from "next";
import "./tokens.css";
import "./components.css";

// Server Component: viewport and metadata exports are only supported here.
export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  viewportFit: "cover", // lets env(safe-area-inset-*) report real insets (LAY-02)
  colorScheme: "light dark", // follow the system appearance (COL-07)
  themeColor: [
    { media: "(prefers-color-scheme: light)", color: "#FFFFFF" },
    { media: "(prefers-color-scheme: dark)", color: "#000000" },
  ],
  // Never set maximumScale or userScalable: people must be able to zoom (A11Y-05).
};

export const metadata: Metadata = {
  title: "Library",
  appleWebApp: { capable: true, title: "Library", statusBarStyle: "default" },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
```

`appleWebApp` produces the `apple-mobile-web-app-title` and status-bar tags plus `mobile-web-app-capable` for home-screen launches. `theme-color` should match your page background (`Canvas` resolves to white or black).

## 2. App shell with routing

The shell stays a Server Component; only the navigation needs client JavaScript, because it reads the current path. `next/link` renders an `<a>`, so the `adl-nav__link` class and `aria-current` work unchanged, and `components.css` presents the list as a tab bar or sidebar (NAV-06, SYNC-01).

<!-- source: tests/web/nextjs/components/AppNav.tsx -->
```tsx
"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";

export type Section = { title: string; href: string; icon: ReactNode };

/** The AppShell navigation with Next.js routing: the current section comes from the URL. */
export function AppNav({ sections }: { sections: readonly Section[] }) {
  const pathname = usePathname();
  return (
    <nav className="adl-nav adl-glass" aria-label="Primary">
      <ul className="adl-nav__list">
        {sections.map((s) => {
          const current = pathname === s.href || pathname.startsWith(`${s.href}/`);
          return (
            <li key={s.href}>
              <Link className="adl-nav__link" href={s.href} aria-current={current ? "page" : undefined}>
                <span aria-hidden="true">{s.icon}</span>
                <span>{s.title}</span>
              </Link>
            </li>
          );
        })}
      </ul>
    </nav>
  );
}
```

<!-- source: tests/web/nextjs/app/(tabs)/layout.tsx -->
```tsx
import { House, Library, Search, Settings } from "lucide-react";
import { AppNav, type Section } from "../../components/AppNav";

const sections: Section[] = [
  { title: "Home", href: "/", icon: <House /> },
  { title: "Library", href: "/library", icon: <Library /> },
  { title: "Search", href: "/search", icon: <Search /> },
  { title: "Settings", href: "/settings", icon: <Settings /> },
];

// A Server Component: only AppNav ships JavaScript, because it reads the pathname.
export default function TabsLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="adl-app">
      <div className="adl-app__layout">
        <AppNav sections={sections} />
        <main className="adl-app__main">{children}</main>
      </div>
    </div>
  );
}
```

## 3. Server and client components

| Recipe | Where it runs | Why |
|---|---|---|
| Layouts, lists, text, buttons that submit forms | Server | No state or browser APIs |
| `AppNav` | Client (`"use client"`) | `usePathname()` |
| `Sheet`, `Alert` | Client | `ref.showModal()` in an effect |
| `ActionMenu` | Client | `hidePopover()` after a choice (the popover itself needs no JS) |
| `SwitchRow`, `SegmentedPicker`, `TextField` with state | Client | Controlled inputs |
| `useMediaQuery` and friends | Client | `matchMedia`; returns the server value during prerendering |

Appearance, contrast, and motion styling are pure CSS (`tokens.css`), so prerendered pages are correct before hydration — no theme flash and no hydration mismatch. Don’t read `window.matchMedia` during render to pick a theme.

## 4. Fonts, images, and icons

- **Fonts.** Use the system stack from `tokens.css` (`var(--adl-font-text)`). Never load SF Pro or New York through `next/font/local` or `@font-face` (TYP-04). `next/font/google` is fine for a brand display face, but keep interface text in the system font.
- **Images.** `next/image` requires `alt`; describe meaningful images and pass `alt=""` for decorative ones (A11Y-04).
- **Icons.** An open-licensed set (Lucide, Phosphor, Heroicons, Material Symbols), `aria-hidden` next to a text label — SF Symbols are not licensed for the web (BRD-03).

## 5. Checklist

- [ ] `viewport` export: `viewportFit: "cover"`, `colorScheme: "light dark"`, no `maximumScale` or `userScalable` (A11Y-05, COL-07, LAY-02)
- [ ] `tokens.css` and `components.css` imported once in the root layout
- [ ] Current route marked with `aria-current="page"`; every section always visible (NAV-03)
- [ ] Client components only where state or browser APIs require them
- [ ] `python3 hooks/scripts/hig_lint.py app components` clean; axe-core clean in light, dark, Increase Contrast, and Reduce Motion

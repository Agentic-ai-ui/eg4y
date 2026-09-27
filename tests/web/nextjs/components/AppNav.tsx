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

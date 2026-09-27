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

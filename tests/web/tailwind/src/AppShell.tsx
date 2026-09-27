import type { ReactNode } from "react";

export type Section = { id: string; title: string; href: string; icon: ReactNode };

/**
 * Tab bar below 48rem of app width, sidebar above it — a container query, never the device (LAY-01, NAV-06).
 * Like the system tab bar, the compact bar caps its label, icon, and spacing in px so labels stay legible at large
 * text sizes; the sidebar scales fully. `wrap-anywhere` lets a word wider than the screen wrap (LAY-04).
 */
export function AppShell({ sections, currentId, children }: {
  sections: readonly Section[];
  currentId: string;
  children: ReactNode;
}) {
  return (
    <div className="@container min-h-dvh bg-background text-label wrap-anywhere">
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

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

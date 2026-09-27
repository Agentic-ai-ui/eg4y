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

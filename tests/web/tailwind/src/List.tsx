import { useId, type ReactNode } from "react";

export function ListSection({ header, footer, children }: { header?: string; footer?: string; children: ReactNode }) {
  return (
    <section className="mb-6">
      {header ? <h2 className="px-[16px] py-1.5 text-footnote font-semibold text-secondary-label">{header}</h2> : null}
      <ul role="list" className="overflow-hidden rounded-xl bg-background-grouped-row">
        {children}
      </ul>
      {footer ? <p className="px-[16px] py-1.5 text-footnote text-secondary-label">{footer}</p> : null}
    </section>
  );
}

// Horizontal padding is px, like iOS layout margins: it stays put while text grows (LAY-04).
// Inset separator between rows, starting at the text's leading edge
const row =
  "relative flex min-h-control w-full items-center gap-3 px-[16px] py-2 text-start " +
  "[li+li>&]:before:absolute [li+li>&]:before:start-[16px] [li+li>&]:before:end-0 [li+li>&]:before:top-0 [li+li>&]:before:border-t [li+li>&]:before:border-separator";

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

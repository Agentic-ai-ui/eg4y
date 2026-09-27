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

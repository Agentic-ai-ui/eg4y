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

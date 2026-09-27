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

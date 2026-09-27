import { useEffect, useId, useRef } from "react";

export type AlertAction = { label: string; role?: "default" | "cancel" | "destructive"; onSelect: () => void };

/**
 * An alert: a specific title, an optional message, and one to three verb-titled buttons (CMP-11 – CMP-13).
 * Two buttons sit side by side with Cancel leading; three stack with the default on top and Cancel last.
 * Cancel is never the default and a destructive action is never prominent (CMP-04, CMP-13): initial focus goes
 * to the default action, or to the title when there is none, so Return never triggers a risky choice.
 */
export function Alert({ open, title, message, actions }: {
  open: boolean;
  title: string;
  message?: string;
  actions: [AlertAction] | [AlertAction, AlertAction] | [AlertAction, AlertAction, AlertAction];
}) {
  const ref = useRef<HTMLDialogElement>(null);
  const titleId = useId();
  const messageId = useId();
  const cancel = actions.find((a) => a.role === "cancel");
  const primary = actions.find((a) => (a.role ?? "default") === "default");
  const rank = (a: AlertAction) => (a === primary ? 0 : a === cancel ? 2 : 1);
  const ordered =
    actions.length === 3
      ? [...actions].sort((a, b) => rank(a) - rank(b))
      : [...actions].sort((a, b) => (a === cancel ? -1 : b === cancel ? 1 : 0));

  useEffect(() => {
    const dialog = ref.current;
    if (!dialog) return;
    if (open && !dialog.open) dialog.showModal();
    if (!open && dialog.open) dialog.close();
  }, [open]);

  return (
    <dialog
      ref={ref}
      className="adl-alert"
      role="alertdialog"
      aria-labelledby={titleId}
      aria-describedby={message ? messageId : undefined}
      onCancel={(e) => {
        e.preventDefault();
        // Esc means Cancel; a single-button informational alert treats Esc as its OK.
        (cancel ?? (actions.length === 1 ? actions[0] : undefined))?.onSelect();
      }}
    >
      <div className="adl-alert__content">
        <h2 id={titleId} className="adl-alert__title" tabIndex={-1} autoFocus={!primary}>
          {title}
        </h2>
        {message ? <p id={messageId} className="adl-alert__message">{message}</p> : null}
      </div>
      <div className="adl-alert__actions">
        {ordered.map((a) => (
          <button
            key={a.label}
            type="button"
            autoFocus={a === primary}
            className={
              a === primary
                ? "adl-button adl-button--prominent"
                : a.role === "destructive"
                  ? "adl-button adl-button--destructive"
                  : "adl-button"
            }
            onClick={a.onSelect}
          >
            {a.label}
          </button>
        ))}
      </div>
    </dialog>
  );
}

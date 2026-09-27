import { useId, type InputHTMLAttributes } from "react";

/**
 * A labeled field. Pass `type="password"` with autoComplete "current-password" or "new-password" for secure
 * entry (CMP-21). Errors say how to fix the problem and are announced with the field (WRT-07, COL-03).
 */
export function TextField({ label, hint, error, ...input }: Omit<InputHTMLAttributes<HTMLInputElement>, "id" | "className"> & {
  label: string;
  hint?: string;
  error?: string;
}) {
  const id = useId();
  const hintId = `${id}-hint`;
  const errorId = `${id}-error`;
  const describedBy = [hint ? hintId : null, error ? errorId : null].filter(Boolean).join(" ") || undefined;
  return (
    <div className="adl-field">
      <label className="adl-field__label" htmlFor={id}>{label}</label>
      <input
        id={id}
        className="adl-field__input"
        aria-invalid={error ? true : undefined}
        aria-describedby={describedBy}
        {...input}
      />
      {hint ? <p id={hintId} className="adl-field__hint">{hint}</p> : null}
      {error ? <p id={errorId} className="adl-field__error">{error}</p> : null}
    </div>
  );
}

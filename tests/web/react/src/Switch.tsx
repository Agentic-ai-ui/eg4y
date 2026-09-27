import { useId } from "react";

/** A switch in a list row: the whole row is the 44 px hit target (A11Y-01, CMP-23). */
export function SwitchRow({ label, checked, onChange, disabled }: {
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  disabled?: boolean;
}) {
  const id = useId();
  return (
    <label className="adl-list__row adl-switch-row" htmlFor={id}>
      <span className="adl-list__title">{label}</span>
      <input
        id={id}
        className="adl-switch"
        type="checkbox"
        role="switch"
        checked={checked}
        disabled={disabled}
        onChange={(e) => onChange(e.currentTarget.checked)}
      />
    </label>
  );
}

import { useId } from "react";

/** A segmented control for choosing one option: native radios give arrow keys and grouping for free. */
export function SegmentedPicker<T extends string>({ label, options, value, onChange }: {
  label: string;
  options: readonly { value: T; title: string }[];
  value: T;
  onChange: (value: T) => void;
}) {
  const name = useId();
  return (
    <fieldset className="adl-segmented">
      <legend className="adl-visually-hidden">{label}</legend>
      {options.map((o) => (
        <label key={o.value} className="adl-segmented__option">
          <input
            type="radio"
            name={name}
            value={o.value}
            checked={o.value === value}
            onChange={() => onChange(o.value)}
          />
          {o.title}
        </label>
      ))}
    </fieldset>
  );
}

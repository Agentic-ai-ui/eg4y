import type { ButtonHTMLAttributes } from "react";

const base =
  "inline-flex min-h-control min-w-control items-center justify-center gap-1.5 rounded-full px-3 text-body font-semibold " +
  "transition-opacity active:opacity-60 disabled:cursor-not-allowed disabled:opacity-40 motion-reduce:transition-none";

const styles = {
  prominent: "bg-accent-fill text-on-accent",
  bordered: "bg-fill text-label contrast-more:outline contrast-more:outline-label",
  plain: "px-2 text-accent-text",
  destructive: "text-destructive-text ring-1 ring-inset ring-current", // never a fill (CMP-04)
} as const;

type Props = Omit<ButtonHTMLAttributes<HTMLButtonElement>, "className"> & { variant?: keyof typeof styles };

/** Styles differ, sizes don't (CMP-02); every style has a press state (CMP-03). */
export function Button({ variant = "bordered", type = "button", ...rest }: Props) {
  return <button type={type} className={`${base} ${styles[variant]}`} {...rest} />;
}

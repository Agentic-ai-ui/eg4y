import type { ButtonHTMLAttributes, ReactNode } from "react";

type Base = Omit<ButtonHTMLAttributes<HTMLButtonElement>, "className">;

/** Prominent buttons can't be destructive (CMP-04); the type system enforces it. */
export type ButtonProps = Base &
  (
    | { variant: "prominent"; destructive?: never }
    | { variant?: "bordered" | "plain"; destructive?: boolean }
  );

export function Button({ variant = "bordered", destructive, type = "button", ...rest }: ButtonProps) {
  const classes = ["adl-button"];
  if (variant !== "bordered") classes.push(`adl-button--${variant}`);
  if (destructive) classes.push("adl-button--destructive");
  return <button type={type} className={classes.join(" ")} {...rest} />;
}

/** Icon-only buttons require a label: it becomes the accessible name and the pointer tooltip (A11Y-03). */
export function IconButton({ label, icon, type = "button", ...rest }: Base & { label: string; icon: ReactNode }) {
  return (
    <button type={type} className="adl-icon-button" aria-label={label} title={label} {...rest}>
      <span aria-hidden="true">{icon}</span>
    </button>
  );
}

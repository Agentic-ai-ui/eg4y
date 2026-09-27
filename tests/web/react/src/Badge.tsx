import { color, text, layout } from "./styles/tokens";

export function Badge({ count }: { count: number }) {
  return (
    <span style={{ ...text.caption1, color: color.onAccent, background: color.accentFill, borderRadius: 999, padding: "0 6px" }}>
      {count}
    </span>
  );
}

export const floatingButtonInset = { bottom: `calc(${layout.safeBottom} + 16px)` };

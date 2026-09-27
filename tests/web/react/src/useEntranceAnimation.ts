import { usePrefersReducedMotion } from "./hooks";

export function useEntranceAnimation(element: HTMLElement | null) {
  const reduced = usePrefersReducedMotion();
  return () =>
    element?.animate(
      reduced ? [{ opacity: 0 }, { opacity: 1 }] : [{ opacity: 0, translate: "0 12px" }, { opacity: 1, translate: "0 0" }],
      { duration: reduced ? 150 : 300, easing: "cubic-bezier(0.2, 0, 0, 1)" },
    );
}

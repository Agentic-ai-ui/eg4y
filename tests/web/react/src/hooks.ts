import { useCallback, useSyncExternalStore } from "react";

/** Subscribe to a CSS media query. Returns `serverValue` during server rendering and hydration. */
export function useMediaQuery(query: string, serverValue = false): boolean {
  const subscribe = useCallback(
    (onChange: () => void) => {
      const list = window.matchMedia(query);
      list.addEventListener("change", onChange);
      return () => list.removeEventListener("change", onChange);
    },
    [query],
  );
  return useSyncExternalStore(
    subscribe,
    () => window.matchMedia(query).matches,
    () => serverValue,
  );
}

export const usePrefersReducedMotion = () => useMediaQuery("(prefers-reduced-motion: reduce)");
export const usePrefersMoreContrast = () => useMediaQuery("(prefers-contrast: more)");
export const usePrefersDark = () => useMediaQuery("(prefers-color-scheme: dark)");

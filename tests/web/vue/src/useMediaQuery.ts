import { onScopeDispose, readonly, ref, type Ref } from "vue";

/** Reactive CSS media query. Starts at `serverValue` where `window` is missing (SSR). */
export function useMediaQuery(query: string, serverValue = false): Readonly<Ref<boolean>> {
  const matches = ref(serverValue);
  if (typeof window !== "undefined") {
    const list = window.matchMedia(query);
    const update = () => (matches.value = list.matches);
    update();
    list.addEventListener("change", update);
    onScopeDispose(() => list.removeEventListener("change", update));
  }
  return readonly(matches);
}

export const usePrefersReducedMotion = () => useMediaQuery("(prefers-reduced-motion: reduce)");
export const usePrefersMoreContrast = () => useMediaQuery("(prefers-contrast: more)");

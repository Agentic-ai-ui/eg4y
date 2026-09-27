import { MediaQuery } from "svelte/reactivity";

// Svelte 5.7+ ships reactive media queries; `prefersReducedMotion` is also exported from "svelte/motion".
export { prefersReducedMotion } from "svelte/motion";
export const prefersMoreContrast = new MediaQuery("prefers-contrast: more");
export const prefersDark = new MediaQuery("prefers-color-scheme: dark");

// Check the prerendered Next.js HTML: viewport, color scheme, theme colors, no zoom lock, current route.
// Part of the Apple Design Language package — Created by Edison Augustin X.
import { readFileSync, readdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const app = join(dirname(fileURLToPath(import.meta.url)), "..", "nextjs", ".next", "server", "app");
const find = (dir, name) => {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const p = join(dir, entry.name);
    if (entry.isDirectory()) { const hit = find(p, name); if (hit) return hit; }
    else if (entry.name === name) return p;
  }
};
const html = readFileSync(find(app, "library.html"), "utf8");
const checks = {
  "viewport-fit=cover, no zoom lock": /<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"\/>/.test(html) && !/maximum-scale|user-scalable/.test(html),
  "color-scheme: light dark": /<meta name="color-scheme" content="light dark"\/>/.test(html),
  "theme-color per appearance": /theme-color" content="#FFFFFF" media="\(prefers-color-scheme: light\)"/.test(html) && /theme-color" content="#000000" media="\(prefers-color-scheme: dark\)"/.test(html),
  "home-screen web app title": /apple-mobile-web-app-title" content="Library"/.test(html),
  "current route marked": /<a class="adl-nav__link" aria-current="page" href="\/library">/.test(html),
};
let failed = 0;
for (const [name, ok] of Object.entries(checks)) { console.log(`${ok ? "✓" : "✗"} ${name}`); if (!ok) failed++; }
process.exit(failed ? 1 : 0);

// Build every browser recipe into dist/<stack>/ for scripts/verify.mjs.
// Part of the Apple Design Language package — Created by Edison Augustin X.
import { cpSync, mkdirSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { execFileSync } from "node:child_process";
import { build } from "esbuild";

const web = join(dirname(fileURLToPath(import.meta.url)), "..");
const assets = join(web, "..", "..", "skills", "apple-design-language", "assets");
const dist = join(web, "dist");
const bin = (name) => join(web, "node_modules", ".bin", name);
const run = (cmd, args, cwd = web) => execFileSync(bin(cmd), args, { cwd, stdio: "inherit" });

rmSync(dist, { recursive: true, force: true });

// React: bundled with esbuild, styled by the shared stylesheets.
mkdirSync(join(dist, "react"), { recursive: true });
await build({ entryPoints: [join(web, "react/src/demo.tsx")], bundle: true, jsx: "automatic", outfile: join(dist, "react/demo.js"), logLevel: "warning" });
cpSync(join(web, "react/index.html"), join(dist, "react/index.html"));

// HTML + CSS: copied as is.
mkdirSync(join(dist, "html"), { recursive: true });
cpSync(join(web, "html/index.html"), join(dist, "html/index.html"));

for (const stack of ["react", "html"]) {
  for (const css of ["tokens.css", "components.css"]) cpSync(join(assets, css), join(dist, stack, css));
}

// Tailwind: the React demo restyled with utilities; the generated theme is imported from the assets folder.
mkdirSync(join(dist, "tailwind"), { recursive: true });
await build({ entryPoints: [join(web, "tailwind/src/demo.tsx")], bundle: true, jsx: "automatic", loader: { ".css": "empty" }, outfile: join(dist, "tailwind/demo.js"), logLevel: "warning" });
run("tailwindcss", ["-i", "tailwind/src/app.css", "-o", "dist/tailwind/app.css"]);
cpSync(join(web, "tailwind/index.html"), join(dist, "tailwind/index.html"));

// Vue and Svelte: Vite builds (outDir is dist/vue and dist/svelte).
run("vite", ["build", "--logLevel", "warn"], join(web, "vue"));
run("vite", ["build", "--logLevel", "warn"], join(web, "svelte"));

console.log("✓ built dist/react, dist/html, dist/tailwind, dist/vue, dist/svelte");

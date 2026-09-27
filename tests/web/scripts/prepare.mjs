// Copy the shared assets into each recipe so the tests always use the real generated files.
// Part of the Apple Design Language package — Created by Edison Augustin X.
import { cpSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const web = join(dirname(fileURLToPath(import.meta.url)), "..");
const assets = join(web, "..", "..", "skills", "apple-design-language", "assets");
const copies = {
  "tokens.ts": ["react/src/styles/tokens.ts"],
  "tokens.native.ts": ["react-native/theme/tokens.native.ts"],
  "tokens.css": ["nextjs/app/tokens.css", "vue/public/tokens.css", "svelte/public/tokens.css"],
  "components.css": ["nextjs/app/components.css", "vue/public/components.css", "svelte/public/components.css"],
};
for (const [file, targets] of Object.entries(copies)) {
  for (const target of targets) {
    mkdirSync(dirname(join(web, target)), { recursive: true });
    cpSync(join(assets, file), join(web, target));
  }
}
console.log("✓ assets copied from skills/apple-design-language/assets");

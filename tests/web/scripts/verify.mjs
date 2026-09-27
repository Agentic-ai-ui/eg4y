// Run every browser recipe in Chromium and check it the same way: layout, targets, tokens, dialogs,
// keyboard behavior, and axe-core (WCAG 2.2 AA) in light, dark, Increase Contrast, Reduce Motion,
// right-to-left, and 200%/310% text. Serves dist/ itself — run `npm run build` first.
// Part of the Apple Design Language package — Created by Edison Augustin X.
//
// Usage: node scripts/verify.mjs [stack ...]        (default: react html tailwind vue svelte)
// Env:   CHROMIUM_PATH  use this Chromium binary instead of Playwright's download
//        SHOTS=1        save screenshots to shots/<stack>/
import { chromium } from "@playwright/test";
import { createServer } from "node:http";
import { existsSync, mkdirSync, readFileSync } from "node:fs";
import { extname, join, normalize, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const web = join(dirname(fileURLToPath(import.meta.url)), "..");
const dist = join(web, "dist");
const axeSource = readFileSync(createRequire(import.meta.url).resolve("axe-core/axe.min.js"), "utf8");
const stacks = process.argv.slice(2).length ? process.argv.slice(2) : ["react", "html", "tailwind", "vue", "svelte"];
const shots = process.env.SHOTS === "1";

// ------------------------------------------------------------------ static server
const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".svg": "image/svg+xml", ".json": "application/json" };
const server = createServer((req, res) => {
  const path = normalize(decodeURIComponent(new URL(req.url, "http://x").pathname)).replace(/^([/\\])+/, "");
  let file = join(dist, path);
  if (!file.startsWith(dist)) { res.writeHead(403).end(); return; }
  if (existsSync(file) && !extname(file)) file = join(file, "index.html");
  if (!existsSync(file)) { res.writeHead(404).end(); return; }
  res.writeHead(200, { "content-type": types[extname(file)] ?? "application/octet-stream" }).end(readFileSync(file));
});
await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
const base = `http://127.0.0.1:${server.address().port}`;

// ------------------------------------------------------------------ checks
const browser = await chromium.launch(process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {});
let failures = 0;
const fail = (stack, config, message) => { failures++; console.log(`  ✗ [${stack} · ${config}] ${message}`); };

const configs = [
  { name: "phone-light", viewport: { width: 390, height: 844 }, colorScheme: "light", interact: true },
  { name: "phone-dark", viewport: { width: 390, height: 844 }, colorScheme: "dark", interact: true },
  { name: "phone-contrast", viewport: { width: 390, height: 844 }, colorScheme: "light", contrast: "more" },
  { name: "phone-dark-contrast", viewport: { width: 390, height: 844 }, colorScheme: "dark", contrast: "more" },
  { name: "tablet-light", viewport: { width: 1024, height: 768 }, colorScheme: "light", interact: true },
  { name: "tablet-dark-reduced", viewport: { width: 1024, height: 768 }, colorScheme: "dark", reducedMotion: "reduce" },
  { name: "phone-rtl", viewport: { width: 390, height: 844 }, colorScheme: "light", setup: () => { document.documentElement.dir = "rtl"; } },
  { name: "tablet-rtl", viewport: { width: 1024, height: 768 }, colorScheme: "light", setup: () => { document.documentElement.dir = "rtl"; } },
  { name: "phone-text-200", viewport: { width: 390, height: 844 }, colorScheme: "light", setup: () => { document.documentElement.style.fontSize = "200%"; } },
  { name: "phone-text-310", viewport: { width: 390, height: 844 }, colorScheme: "light", setup: () => { document.documentElement.style.fontSize = "310%"; } },
];
// Expected token values come from the single source, tokens.json.
const blueToken = JSON.parse(readFileSync(join(web, "..", "..", "skills", "apple-design-language", "assets", "tokens.json"), "utf8")).color.system.blue;
const expectedBlue = { light: blueToken.light, dark: blueToken.dark, "light-more": blueToken.lightIncreasedContrast, "dark-more": blueToken.darkIncreasedContrast };

async function axe(page, selector) {
  await page.addScriptTag({ content: axeSource });
  return page.evaluate(async (sel) => {
    const result = await window.axe.run(sel ? document.querySelector(sel) : document, { runOnly: ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa", "best-practice"] });
    return result.violations.map((v) => `${v.id} (${v.impact}): ${v.nodes.slice(0, 3).map((n) => n.target.join(" ")).join(", ")}`);
  }, selector);
}

for (const stack of stacks) {
  if (!existsSync(join(dist, stack, "index.html"))) { fail(stack, "setup", `dist/${stack}/index.html is missing — run npm run build`); continue; }
  console.log(`▶ ${stack}`);
  for (const c of configs) {
    const context = await browser.newContext({ viewport: c.viewport, colorScheme: c.colorScheme, contrast: c.contrast ?? "no-preference", reducedMotion: c.reducedMotion ?? "no-preference", deviceScaleFactor: 2 });
    const page = await context.newPage();
    const errors = [];
    page.on("pageerror", (e) => errors.push(e.message));
    page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
    await page.goto(`${base}/${stack}/`);
    if (c.setup) await page.evaluate(c.setup);
    await page.waitForTimeout(300);
    const before = failures;
    if (errors.length) fail(stack, c.name, `page errors: ${errors.join(" | ")}`);

    // Navigation: tab bar in compact widths, sidebar in regular widths (on the trailing side in RTL).
    const nav = await page.evaluate(() => {
      const n = document.querySelector("nav[aria-label=Primary]"); const r = n.getBoundingClientRect();
      return { position: getComputedStyle(n).position, top: r.top, left: r.left, right: innerWidth - r.right, width: r.width, height: r.height };
    });
    const compact = c.viewport.width < 768;
    if (compact && !(nav.position === "fixed" && nav.top > c.viewport.height - 140)) fail(stack, c.name, `expected a bottom tab bar, got ${JSON.stringify(nav)}`);
    if (!compact && !(nav.position === "sticky" && nav.height >= c.viewport.height - 1 && nav.width < 300)) fail(stack, c.name, `expected a sidebar, got ${JSON.stringify(nav)}`);
    if (c.name === "tablet-rtl" && !(Math.round(nav.right) === 0 && nav.left > 700)) fail(stack, c.name, "sidebar should sit on the right in RTL");

    // Hit targets: 44 px minimum (a switch or radio counts its label row).
    const small = await page.evaluate(() => [...document.querySelectorAll("a, button, input, [role=switch], label")].filter((e) => e.checkVisibility()).map((e) => {
      const r = (e.matches("[role=switch], input[type=radio]") ? e.closest("label") : e).getBoundingClientRect();
      return { el: e.outerHTML.slice(0, 60), w: Math.round(r.width), h: Math.round(r.height) };
    }).filter((t) => t.w < 44 || t.h < 44));
    if (small.length) fail(stack, c.name, `targets under 44 px: ${JSON.stringify(small)}`);

    // Tokens follow appearance and Increase Contrast.
    const blue = await page.evaluate(() => getComputedStyle(document.documentElement).getPropertyValue("--adl-blue").trim());
    const want = expectedBlue[c.colorScheme + (c.contrast ? "-more" : "")];
    if (blue !== want) fail(stack, c.name, `--adl-blue is ${blue}, expected ${want}`);

    // No horizontal overflow; tab labels legible (not truncated) at large text sizes.
    const layout = await page.evaluate(() => ({
      overflow: document.documentElement.scrollWidth - innerWidth,
      truncated: [...document.querySelectorAll("nav[aria-label=Primary] a > span:last-child")].filter((s) => s.scrollWidth > s.clientWidth + 1).map((s) => s.textContent),
    }));
    if (layout.overflow > 0) fail(stack, c.name, `horizontal overflow of ${layout.overflow}px`);
    if (layout.truncated.length) fail(stack, c.name, `truncated tab labels: ${layout.truncated.join(", ")}`);

    // RTL mirrors the switch thumb and the disclosure indicator.
    if (c.name === "phone-rtl") {
      const rtl = await page.evaluate(() => ({ thumb: getComputedStyle(document.querySelector("[role=switch]"), "::before").translate }));
      if (!rtl.thumb.startsWith("-")) fail(stack, c.name, `switch thumb should travel to the left in RTL, got ${rtl.thumb}`);
    }

    const violations = await axe(page);
    if (violations.length) fail(stack, c.name, `axe: ${violations.join(" || ")}`);
    if (shots) { mkdirSync(join(web, "shots", stack), { recursive: true }); await page.screenshot({ path: join(web, "shots", stack, `${c.name}.png`) }); }

    if (c.interact) {
      // Sheet: opens modally, confirm disabled while empty, axe-clean, closes with Esc.
      await page.getByRole("button", { name: "Add Book" }).first().click();
      await page.waitForTimeout(350);
      if (!(await page.evaluate(() => document.querySelector("dialog:not([role=alertdialog])").matches(":modal")))) fail(stack, c.name, "sheet did not open modally");
      if (!(await page.getByRole("button", { name: "Add", exact: true }).isDisabled())) fail(stack, c.name, "Add should be disabled while the title is empty");
      const sheetViolations = await axe(page, "dialog:not([role=alertdialog])");
      if (sheetViolations.length) fail(stack, c.name, `axe (sheet): ${sheetViolations.join(" || ")}`);
      await page.keyboard.press("Escape");
      await page.waitForTimeout(350);
      if (await page.evaluate(() => document.querySelector("dialog:not([role=alertdialog])").open)) fail(stack, c.name, "Esc did not close the sheet");

      // Alert: no default action, so focus starts on the title; Cancel leads; Esc = Cancel.
      await page.getByRole("button", { name: "Delete All" }).last().click();
      await page.waitForTimeout(350);
      const alert = await page.evaluate(() => {
        const d = document.querySelector("dialog[role=alertdialog]");
        return { open: d.open, titleFocused: document.activeElement?.id === d.getAttribute("aria-labelledby"), order: [...d.querySelectorAll("button")].map((b) => b.textContent.trim()).join() };
      });
      if (!alert.open || !alert.titleFocused || alert.order !== "Cancel,Delete") fail(stack, c.name, `alert: ${JSON.stringify(alert)}`);
      await page.keyboard.press("Escape");
      await page.waitForTimeout(350);
      if (await page.evaluate(() => document.querySelector("dialog[role=alertdialog]").open)) fail(stack, c.name, "Esc did not close the alert");

      // Menu: opens anchored just below its button.
      await page.getByRole("button", { name: "More" }).click();
      await page.waitForTimeout(200);
      const menu = await page.evaluate(() => {
        const m = document.querySelector("[popover]"); const b = document.querySelector("[popovertarget]").getBoundingClientRect();
        return { open: m.matches(":popover-open"), gap: Math.round(m.getBoundingClientRect().top - b.bottom) };
      });
      if (!menu.open || menu.gap < 0 || menu.gap > 12) fail(stack, c.name, `menu not anchored: ${JSON.stringify(menu)}`);
      await page.keyboard.press("Escape");

      // Switch toggles; segmented control moves with arrow keys.
      const sw = page.getByRole("switch", { name: "iCloud Sync" });
      await sw.click();
      if (await sw.isChecked()) fail(stack, c.name, "switch did not toggle");
      await page.getByRole("radio", { name: "Recent" }).focus();
      await page.keyboard.press("ArrowRight");
      if (!(await page.getByRole("radio", { name: "Title" }).isChecked())) fail(stack, c.name, "arrow key did not move the segmented control");
    }
    if (failures === before) console.log(`  ✓ ${c.name}`);
    await context.close();
  }
}

await browser.close();
server.close();
console.log(failures ? `\n✗ ${failures} failure(s)` : `\n✓ all checks passed (${stacks.join(", ")} × ${configs.length} configurations)`);
process.exit(failures ? 1 : 0);

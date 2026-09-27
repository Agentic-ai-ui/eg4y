# Web and React Native recipe tests

> Part of the **Apple Design Language** package — Created by Edison Augustin X.

The code in the skill’s [React](../../skills/apple-design-language/references/react-recipes.md), [HTML + CSS](../../skills/apple-design-language/references/html-css-recipes.md), [Tailwind](../../skills/apple-design-language/references/tailwind.md), [Vue and Svelte](../../skills/apple-design-language/references/vue-svelte.md), [Next.js](../../skills/apple-design-language/references/nextjs.md), and [React Native](../../skills/apple-design-language/references/react-native.md) references lives here as real projects. CI type-checks and builds them, then runs the browser recipes in Chromium with axe-core. The references copy each block from these files, so documented code is always tested code.

## What runs

| Step | Command | Checks |
|---|---|---|
| Docs in sync | `python3 tests/web/sync_docs.py --check` | Every `<!-- source: tests/web/… -->` block in the references equals its file |
| Type-check | `npm run typecheck` | `tsc --strict` (React, Tailwind, React Native against RN 0.87 and Expo SDK 57), `vue-tsc`, `svelte-check` |
| Build | `npm run build` | esbuild (React, Tailwind), Tailwind v4 CLI, Vite (Vue, Svelte) into `dist/` |
| Next.js | `npm run build:next` | `next build`, then the prerendered HTML: `viewport-fit=cover`, no zoom lock, `color-scheme`, theme colors, `aria-current` |
| Browser | `npm run verify` | The same Library screen in React, HTML + CSS, Tailwind, Vue, and Svelte, in 10 configurations each (below) |

**Configurations:** phone (390 px) and tablet (1024 px); light and dark; Increase Contrast in both appearances; Reduce Motion; right-to-left at both widths; 200% and 310% text.

**Checks per configuration:** tab bar at compact width and sidebar at regular width (trailing side in right-to-left); every target ≥ 44 px; `--adl-blue` matches `tokens.json` for the appearance; no horizontal overflow and no truncated tab labels; axe-core with no WCAG 2.2 AA or best-practice violations. In three configurations the harness also drives the UI: the sheet opens modally, keeps its confirm button disabled while empty, and closes with Esc; the alert focuses its title (no default action), orders Cancel first, and closes with Esc; the menu anchors below its button; the switch toggles; arrow keys move the segmented control.

## Run it locally

```bash
cd tests/web
npm ci
npx playwright install chromium        # or set CHROMIUM_PATH to an existing Chromium
npm test                               # typecheck → build → build:next → verify
SHOTS=1 npm run verify                 # also save screenshots to shots/<stack>/
npm run verify -- react vue            # only some stacks
```

## Changing a recipe

1. Edit the file here (for example `react/src/Sheet.tsx`), never the code block in the reference.
2. Run `python3 tests/web/sync_docs.py` to copy it into the references.
3. Run `npm test` and `python3 hooks/scripts/hig_lint.py tests/web`.

To document a new file, add `<!-- source: tests/web/<path> -->` above an empty code block in a reference and run the sync script. Shared styles and tokens are not copied into this folder: `scripts/prepare.mjs` takes them from `skills/apple-design-language/assets` on every run, and Tailwind imports them directly.

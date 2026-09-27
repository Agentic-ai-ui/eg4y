# Changelog

All notable changes to Apple Design Language are recorded here. Created by Edison Augustin X.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Each version matches `version` in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json); running the Release workflow (or pushing the tag `v<version>`) publishes the GitHub release with that version’s notes.

## [Unreleased]

### Added

- **Recipe tests in CI** — the web and React Native recipes now live in `tests/web` as real projects. CI type-checks them (TypeScript strict, `vue-tsc`, `svelte-check`), builds them (esbuild, Tailwind CLI, Vite, `next build`), checks the Next.js prerendered metadata, and runs the React, HTML + CSS, Tailwind, Vue, and Svelte builds in Chromium with axe-core in 10 configurations (phone and tablet, light, dark, Increase Contrast, Reduce Motion, right-to-left, 200% and 310% text). `tests/web/sync_docs.py` copies the files into the references, and CI fails if a reference drifts from its tested source.

### Fixed

- **Largest text sizes** — found by the new harness at 310% text: the segmented control (a `fieldset`) overflowed the screen, and long words could scroll the page sideways. Segments now move to a second row, words wrap, and horizontal gutters and row insets stay fixed like iOS layout margins, so text gets the room (`components.css` and the Tailwind recipe).
- Vue recipe icons use `@lucide/vue`, which replaces the deprecated `lucide-vue-next`.

### Changed

- **Release workflow** — can be started from GitHub with **Actions › Release › Run workflow**: it reads the version from `plugin.json` (optionally confirmed by an input), runs the checks, creates the tag at the tip of `main`, and publishes. When a release already exists — for example, one created on github.com — the workflow updates its title and notes from `CHANGELOG.md` instead of failing.

## [1.0.0] - 2026-09-27

First release: a researched design system that teaches AI agents to build apps for the Apple ecosystem — iPhone, iPad, iPhone Duo, Mac, Apple TV, Apple Vision Pro, and Apple Watch — with Apple’s Human Interface Guidelines and Liquid Glass, in SwiftUI, UIKit, and AppKit, and on the web and React Native: React, Next.js, HTML + CSS, Tailwind CSS, Vue, Svelte, and React Native.

### Added

- **`GUIDELINES.md`** — the design language in 20 sections, each topic citing its Apple sources (HIG and Developer Documentation, current through September 2026): principles, Liquid Glass, layout, color with official system color values, typography with Dynamic Type tables, navigation, components, accessibility, writing, privacy, AI, and per-platform guidance, plus web and React Native implementation guidance and the SF Symbols boundary for web builds.
- **`rules/`** — 245 enforceable rules with stable IDs, RFC 2119 levels, severities, and platforms (78 errors, 165 warnings, 2 info), including six `STK` rules for web and React Native builds, plus the machine-readable `rules.json` and `build_rules.py` to validate them.
- **`skills/apple-design-language/`** — Claude Code skill with a design workflow and 17 references: platforms, navigation, components, Liquid Glass, design tokens, accessibility, writing, review checklist, a stack map, web foundations, and recipes for SwiftUI, React, Next.js, HTML + CSS, Tailwind CSS, Vue and Svelte, and React Native. `tokens.json` is the single source of design values, generating `tokens.css`, `tokens.ts`, `tailwind.css`, and `tokens.native.ts`; `components.css` gives every web stack the same components. The web recipes were type-checked and run in Chromium with axe-core (WCAG 2.2 AA); the Next.js recipes were built with `next build`; the React Native recipes were type-checked against React Native 0.87 and Expo SDK 57. Six evals.
- **`AGENTS.md`** and **`.claude/CLAUDE.md`** — shared instructions for any coding agent, plus Claude Code additions.
- **`hooks/`** — `hig_lint.py` checks 22 rules across Swift, CSS, HTML, JS/TS/JSX, Vue, Svelte, Tailwind classes, React Native, Next.js viewport settings, plists, `.strings`, and font files; a prompt router that sends each stack to its recipes and a session brief; 71 tests.
- **`.claude-plugin/`** — plugin manifest and the `eg4y` marketplace, so the package installs with `/plugin install apple-design-language@eg4y`.
- **CI** — generated files up to date, hook tests on Python 3.9–3.13, and strict plugin validation on every pull request; tagged releases publish automatically.
- **`LICENSE`** — MIT.

[Unreleased]: https://github.com/Agentic-ai-ui/eg4y/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/Agentic-ai-ui/eg4y/releases/tag/v1.0.0

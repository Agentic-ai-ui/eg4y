# Changelog

All notable changes to Apple Design Language are recorded here. Created by Edison Augustin X.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versions follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html). Each version matches `version` in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json); pushing the tag `v<version>` publishes the GitHub release with that version’s notes.

## [1.0.0] - 2026-09-27

First release: a researched design system that teaches AI agents to build apps for the Apple ecosystem — iPhone, iPad, iPhone Duo, Mac, Apple TV, Apple Vision Pro, and Apple Watch — with Apple’s Human Interface Guidelines and Liquid Glass.

### Added

- **`GUIDELINES.md`** — the design language in 20 sections, each topic citing its Apple sources (HIG and Developer Documentation, current through September 2026): principles, Liquid Glass, layout, color with official system color values, typography with Dynamic Type tables, navigation, components, accessibility, writing, privacy, AI, and per-platform guidance.
- **`rules/`** — 239 enforceable rules with stable IDs, RFC 2119 levels, severities, and platforms (77 errors, 160 warnings, 2 info), plus the machine-readable `rules.json` and `build_rules.py` to validate them.
- **`skills/apple-design-language/`** — Claude Code skill with a design workflow, 10 references (platforms, navigation, components, Liquid Glass, design tokens, accessibility, writing, SwiftUI recipes, web adaptation, review checklist), `tokens.json` as the single source of design values with generated `tokens.css`, and evals.
- **`AGENTS.md`** and **`.claude/CLAUDE.md`** — shared instructions for any coding agent, plus Claude Code additions.
- **`hooks/`** — `hig_lint.py` checks 21 rules across Swift, CSS, HTML, JS/TS/JSX, plists, `.strings`, and font files; a prompt router and a session brief; 60 tests.
- **`.claude-plugin/`** — plugin manifest and the `eg4y` marketplace, so the package installs with `/plugin install apple-design-language@eg4y`.
- **CI** — generated files up to date, hook tests on Python 3.9–3.13, and strict plugin validation on every pull request; tagged releases publish automatically.
- **`LICENSE`** — MIT.

[1.0.0]: https://github.com/Agentic-ai-ui/eg4y/releases/tag/v1.0.0

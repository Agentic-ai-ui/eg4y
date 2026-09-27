@AGENTS.md

## Claude Code

> Created by Edison Augustin X. `AGENTS.md` (imported above) is the shared instruction file for every agent; this section adds only what is specific to Claude Code.

- **Skill:** for any Apple-platform design, UI build, or review task, use the `apple-design-language` skill (`skills/apple-design-language/SKILL.md`). Read only the reference files the task needs — the skill’s routing table lists them — rather than loading `GUIDELINES.md` whole.
- **Hook feedback:** when this package’s hooks are installed, a post-edit check reports rule violations with rule IDs after you write UI files. Treat a reported **error** as something to fix before continuing; fix **warnings** or add a `hig-ignore: RULE-ID — reason` annotation when the deviation is deliberate. Don’t silence findings without a reason.
- **Multi-platform or architectural changes:** outline the information architecture and each platform’s navigation container first, and confirm target platforms with the user when they aren’t stated.
- **Research before asserting:** when a value, API, or guideline isn’t already in this package, check Apple’s documentation (and MDN for web features) instead of relying on memory, and cite the source.

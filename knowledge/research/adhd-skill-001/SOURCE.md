# Source Snapshot — i-have-adhd

- **Research ID:** ADHD-SKILL-001
- **Snapshot date:** 2026-10-18
- **Status:** Research only; no integration; no Canon change
- **Source repository:** https://github.com/ayghri/i-have-adhd
- **Pinned commit:** `1ecea1993b7fce257ffbd686c070948b5e07eda6`
- **Pinned SKILL.md:** https://github.com/ayghri/i-have-adhd/blob/1ecea1993b7fce257ffbd686c070948b5e07eda6/skills/i-have-adhd/SKILL.md
- **License declared by source:** MIT
- **Package version observed:** `0.4.1`
- **Test status:** Tests/evals were inspected but not executed; no pass claim is made.

## Source surfaces inspected

- `skills/i-have-adhd/SKILL.md`
- `AGENTS.md`
- `package.json`
- `.codex-plugin/plugin.json`
- `hooks/hooks.json`
- `extensions/i-have-adhd.ts`
- `scripts/run_evals.py`
- `tests/`

## Observed design themes

Action-first responses, numbered steps, one concrete next action, tangent suppression, state continuity, concrete time estimates, visible progress, matter-of-fact error handling, bounded lists, and limited preamble/recap.

The source also includes exceptions and precedence constraints: provide detail when requested, confirm destructive actions, ask a diagnostic question after repeated failed attempts, clarify genuine ambiguity, and preserve task/safety/harness constraints.

## Provenance and limitations

This is a research record based on the pinned upstream revision and the inspection notes available for this snapshot. It is not a vendored copy of the upstream source and does not establish compatibility with ACES OS. Dependency licenses and runtime behavior require separate verification before any downstream use.
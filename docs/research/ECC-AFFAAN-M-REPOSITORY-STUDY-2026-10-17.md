# ECC (affaan-m/everything-claude-code) — Repository Study

**Date:** 2026-10-17  
**Status:** RESEARCH RECORD / READ-ONLY OBSERVATION  
**Scope:** open GitHub repository `affaan-m/everything-claude-code`, now `affaan-m/ECC`  
**Method:** GitHub API (`gh`) metadata plus a shallow clone of `main` (read-only; clone not stored in this repository). All numbers were observed on 2026-10-17 and change over time.

## 1. Identity

| Field | Value |
|---|---|
| Current name / URL | `affaan-m/ECC` (the old name `everything-claude-code` redirects) |
| Description | "The agent harness performance optimization system. Skills, instincts, memory, security, and research-first development for Claude Code, Codex, Opencode, Cursor and beyond." |
| Homepage | https://ecc.tools |
| License | MIT |
| Created | 2026-01-18 |
| Last push | 2026-10-15 |
| Latest release | v2.2.3 (2026-10-01); `VERSION` and `package.json` = 2.2.3 |
| Stars / forks | 281,410 / 41,840 |
| Watchers | 1,402 |
| Commits on default branch | about 3,934 |
| Contributors | about 412 |
| Open issues / open PRs | 88 / 141 (GitHub counter: 229) |
| Closed PRs | 2,448 |
| Topics | ai-agents, anthropic, claude, claude-code, developer-tools, llm, mcp, productivity |
| Maintainer | Affaan Mustafa (single maintainer per README), funded by sponsors and the paid ECC Pro GitHub App |
| Distribution | GitHub; npm `ecc-universal` (also `ecc-agentshield`); Claude Code plugin `ecc@ecc` |

**Correction to the task framing:** the task describes ECC as a set of configurations for AI development agents. That was accurate for early versions. The current README and `docs/ECC-2.0-REFERENCE-ARCHITECTURE.md` position ECC as a "harness operating system": a cross-harness catalog plus installer, hook runtime, memory, observability, and a Rust control-plane prototype (`ecc2/`).

## 2. Composition (counts observed in the `main` checkout)

| Component | Count / location | Notes |
|---|---|---|
| Agents | 71 files in `agents/` | Planner, architect, tdd-guide, code/security reviewers, per-language reviewers and build resolvers, loop-operator, harness-optimizer, GAN planner/generator/evaluator, etc. |
| Skills | 311 `SKILL.md` in `skills/` (613 files) | Workflow and domain knowledge, e.g. `continuous-learning-v2`, `gateguard`, `deep-research`, `council`, `autonomous-loops`, language/framework patterns. |
| Commands | 97 in `commands/` | Slash commands (`plan`, `code-review`, `build-fix`, `learn`, `evolve`, `harness-audit`, `prp-*`, `epic-*`, `orch-*`, language-specific build/review/test). Legacy shims kept under `legacy-command-shims/`. |
| Rules | 122 files in `rules/` | `common/` plus 22 language/framework directories (typescript, python, golang, rust, java, kotlin, swift, php, vue, react, etc.). |
| Hooks | `hooks/hooks.json`: 27 hook entries over 8 events (PreToolUse 10, Stop 8, PostToolUse 2, PostToolUseFailure 2, SessionStart 2, UserPromptSubmit 1, PreCompact 1, SessionEnd 1) | Implemented as Node scripts in `scripts/hooks/` (GateGuard, config-protection, block-no-verify, cost-tracker, quality-gate, session-start/end, observe, etc.). Separate hook sets for Codex, Hermes, Qoder. |
| MCP | `mcp-configs/mcp-servers.json` | Default is intentionally minimal (see section 4). |
| Scripts | 370 files in `scripts/` | Installer (`install-plan/apply/guided`), `doctor`, `repair`, `catalog`, `harness-audit`, `memory`, `orchestrate-worktrees`, `sessions-cli`, etc. |
| Tests | 497 files in `tests/` | Node test runner plus Python tests; CI matrix is ubuntu/windows/macos across Node versions and package managers. |
| Harness adapters | `.claude-plugin`, `.codex`, `.cursor` (69 files), `.opencode` (82 files), plus Qoder, Gemini, Zed, Antigravity, Qwen, Hermes, Copilot targets | `.opencode` is built to `.opencode/dist` and is the npm package `main`. |
| Docs | 1,540 files in `docs/` | 15 localisations (ru, zh-CN, ja-JP, ...), roadmaps, architecture, security evidence. |
| `ecc2/` | Rust, about 54.6k lines | Control-plane/TUI prototype: sessions, worktrees, comms, observability, notifications. |
| Install system | `manifests/`: 46 modules in `install-modules.json`; profiles `minimal`, `opencode`, `core`, `developer`, `security`, `research`, `full` | Selective install: the project itself warns not to stack a full manual Claude install over the plugin. |

Languages by bytes (GitHub): JavaScript about 11.2 MB (dominant), Rust 1.9 MB, Python 1.6 MB, Shell 0.24 MB, TypeScript 0.12 MB, small amounts of Swift, PowerShell, Lua, Dockerfile, CSS. Content is mostly Markdown, which is not counted by the language statistics.

## 3. Architecture and key mechanisms

1. **Layered content model.** Rules (always-on constraints), agents (delegated roles), skills (loaded on demand to keep context small), commands (explicit entry points), hooks (deterministic automation on harness events). `AGENTS.md` states the principles: agent-first, test-driven (80%+ coverage), security-first, immutability, plan before execute.
2. **Module / profile installer.** Content is classified into modules; profiles select module sets; install plans are computed and applied per target harness (`scripts/install-plan.js`, `install-apply.js`, `manifests/*`). `doctor.js` and `repair.js` detect and fix drift.
3. **GateGuard.** A PreToolUse hook that denies the first Edit/Write/Bash on a target until the agent has gathered concrete facts, then allows retry. The CHANGELOG describes extensive tuning (class-specific questions, credit for earlier searches, session-state expiry, sensitive-path handling, opt-in metrics). Its own effectiveness harness (`docker/gateguard-effectiveness/`) reported, in a 72-session pilot, that every arm passed every trial, so it measured about 45% more turns and no measurable benefit. The README-level evidence for GateGuard (A/B tests in `skills/gateguard/SKILL.md`) and this pilot should be read together.
4. **Continuous learning v2.1.** Hooks observe sessions and create atomic "instincts" with confidence scores, scoped per project (stored under `${XDG_DATA_HOME:-~/.local/share}/ecc-homunculus/projects/<hash>/`), promoted to global when seen in 2+ projects, and evolvable into skills/commands/agents. SessionStart injects a capped, ranked subset (default 6 instincts, minimum confidence 0.7).
5. **Cross-harness memory vault.** A project vault for handoffs between harnesses (`scripts/memory.js`, `memory-mcp.mjs`).
6. **Hook strictness profiles and context budgeting.** Environment variables select a hook profile (default `standard`), disable individual hooks, cap SessionStart context (default 8000 characters), and prune session temp data (default 30 days).
7. **Orchestration.** Worktree/tmux orchestration, loop operator, GAN-style generator/evaluator harness, DeepSeek harness guide, Pi coding agent core profile (`pi/`), Itô compute bridge for self-hosted models.

## 4. Notable policy decisions (self-reported)

- `docs/MCP-CONNECTOR-POLICY.md` (June 2026 audit): default MCP set reduced to `chrome-devtools` only. Former defaults `github`, `context7`, `exa`, `memory`, `playwright`, `sequential-thinking` were dropped in favour of CLIs, skills, or native harness features, because MCP tool schemas consume context every session. They remain opt-in in `mcp-configs/mcp-servers.json`; `ECC_DISABLED_MCPS` filters generated configs.
- README states a "low-context / no-hooks" install path and a warning that the plugin advertises the full catalog to the model, so context footprint is a known cost of the full install.

## 5. Platform support (as stated by the project)

| Harness | Stated status |
|---|---|
| Claude Code | Stable primary |
| Codex, Qoder | Supported native plugin |
| Cursor, OpenCode, Copilot CLI | Beta adapters |
| Copilot Chat | Instruction-only |
| Gemini, Zed, Antigravity, Qwen, Hermes, OpenClaw, Kimi, CodeBuddy, JoyCode | Experimental/minimal |

OS: Linux/macOS/WSL are supported core; native Windows is supported with limitations. Open defects named in the README: #2674 (macOS Bash 3.2 and the GAN shell score parsing), #2489 and #2626 (native-Windows observer daemon and memory vault writes), #2617 (OpenCode provider selection).

## 6. Maturity and risk assessment

Strengths (observed):
- Very high adoption and activity: 281k stars, about 3.9k commits since January 2026, weekly releases, 2.4k merged/closed PRs.
- Large automated test suite and a multi-OS CI matrix; security policy with private advisory reporting; supply-chain watch workflow; documented supply-chain incident response.
- Explicit, documented capability tiers per harness instead of claiming parity.
- Self-critical measurement culture (GateGuard pilot reported as null, MCP default audit).

Risks and limits (observed or inferred from the above):
- **Size and context cost.** 311 skills, 71 agents, 97 commands. Full install enlarges what the model sees; the project itself recommends selective profiles.
- **Hook surface.** 27 hook entries run Node on tool events across Claude Code; hooks are executed with the user's privileges. Review before installing; native Codex hooks need explicit trust.
- **Single-maintainer dependency and commercial layer.** Open-source core is MIT, but a paid ECC Pro app and sponsors fund it; bus factor is high.
- **Fast churn.** The CHANGELOG has a large `Unreleased` section; behaviour of hooks such as GateGuard changes frequently. Pin versions.
- **Naming/identity.** The repository was renamed; the README warns to install only from official channels (GitHub `affaan-m/ECC`, npm `ecc-universal`, `ecc-agentshield`).
- **Quality variance.** `skills` include `origin: community` entries; breadth (domain skills for customs, carrier management, DeFi, etc.) suggests uneven depth. Not individually audited here.
- **Platform parity gaps** listed in section 5.

## 7. Relevance to ACES OS

This is an observation, not a decision. H-CENSUS-003 classifies Claude Code and Codex as Coding Harnesses (specialized execution workers) and keeps ACES authority primitives (A01–A05) outside the harness trust boundary. ECC fits as a **capability/content and hook layer on top of a coding harness** (P05 Capability, P10 Control, P11 Lifecycle, P17 Evolution), not as an execution substrate or orchestration runtime. Its instinct/memory features overlap P02/P03/P17 and would sit inside the harness boundary, so any use must not move epistemic or decision authority into ECC hooks or learned instincts. Adoption, if any, should be per-module (e.g. `minimal`/`core` profile) behind the ACES Harness Contract; this requires a separate gate and was not evaluated here.

## 8. Limits of this study

- Shallow clone (depth 1): commit history, per-file churn and contributor distribution were not analysed beyond API counts.
- No ECC code was executed and its test suite was not run; claims about behaviour come from README, CHANGELOG, manifests and skill documents.
- No security audit of hooks or scripts was performed.
- Counts of issues/PRs and stars are point-in-time values.

## 9. Sources

- https://github.com/affaan-m/ECC (README.md, AGENTS.md, CHANGELOG.md, SECURITY.md, `manifests/`, `hooks/hooks.json`, `skills/gateguard/SKILL.md`, `skills/continuous-learning-v2/SKILL.md`, `docs/MCP-CONNECTOR-POLICY.md`, `docs/ECC-2.0-REFERENCE-ARCHITECTURE.md`)
- GitHub API: `gh repo view` and `gh api` on `repos/affaan-m/ECC`, search API for issue/PR counts.

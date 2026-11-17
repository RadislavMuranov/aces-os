# ACES Research — Unified Multi-Harness Environment
**Date:** 2026-11-17  
**Status:** RESEARCH ACTIVE · PLATFORM DECISION PENDING  
**Classification:** NOT CANON · NO INSTALLATION AUTHORIZED BY THIS RECORD

## Mission
Establish a unified working environment for DSH, Hermes, Claude Code, ZCode and Pi Durable. A single mission is decomposed into bounded tasks; tasks are assigned to independent harnesses; results are exchanged with provenance; work is cross-reviewed; integration is tested; ACES alone decides acceptance.

## Authority and constraints
- ACES retains Governance, Authorization, Verification, Acceptance and AcceptedState authority.
- A terminal/workspace is an interface, not an authority plane.
- DSH remains the mandatory Harness in the ACES execution path.
- ExecutionResult does not imply AcceptedState.
- UNKNOWN ≠ FALSE ≠ REJECTED.
- No Canon changes, production integration, credential movement or local configuration changes are authorized by this research record.
- The user alone decides whether proprietary licensing is acceptable. Licensing is recorded as a fact, not used as a selection veto.

## The actual choice: Tabby vs ZCode
These are not equivalent product categories:
- **Tabby** is a neutral terminal emulator for local shells and SSH/serial connections.
- **ZCode** is an AI coding workspace with desktop, browser and terminal interfaces, plus its own Agent CLI/TUI/Web distribution.

### Initial evidence matrix

| Capability | Tabby | ZCode | Status |
|---|---|---|---|
| Windows support | Windows, PowerShell, PS Core, WSL, Git Bash, CMD | Windows x64 installer documented | CONFIRMED (docs) |
| Multi-session UI | Tabs, nested panes, restore sessions | Workspace tasks and terminal panel | CONFIRMED (docs) |
| Run independent CLI harnesses | General-purpose shell is designed for this | Integrated terminal can run shell commands; lifecycle isolation needs test | Tabby CONFIRMED; ZCode REVIEW |
| Agent orchestration | Not built in | Native ZCode Agent, tasks, long-horizon context, subagents | ZCode CONFIRMED (documented) |
| Task decomposition / continuity | External tools must provide it | Goal mode and task/workspace context documented | ZCode CONFIRMED (documented) |
| MCP | No native agent MCP layer established | MCP server management; import from Claude Code, Codex CLI, OpenCode | ZCode CONFIRMED; DSH/Hermes UNKNOWN |
| Skills | Plugin ecosystem; not an AI skills manager | Skills, commands and subagents | ZCode CONFIRMED (documented) |
| Hooks | Terminal plugin API is not equivalent to agent lifecycle hooks | Local subprocess hook protocol | ZCode CONFIRMED (documented) |
| Repository-level hooks | Not applicable as a terminal-native enforcement layer | Docs state project-level hooks are not executed in current version | ZCode limitation CONFIRMED (docs) |
| Evidence/review | External workflow required | Review panel and task trajectory features documented | ZCode CONFIRMED (documented); quality UNKNOWN |
| Recovery | Tab/pane restoration, not agent task recovery | Long-task state/recovery claims; failure injection needed | ZCode REVIEW |
| ACES enforcement suitability | Requires external orchestrator/guard hooks | Promising, but project-level hook limitation and authority boundary need validation | UNKNOWN |
| Performance on user's PC | Needs measured idle/5-session test | Needs measured idle/agent/5-session test | UNKNOWN |

## Initial assessment
- Tabby is the stronger neutral multi-CLI terminal candidate. It can provide a common window without attempting to own agent policy or task state.
- ZCode is the stronger integrated agentic workspace candidate. It can reduce manual task coordination by bringing task state, model choice, execution modes, browser, terminal, skills, subagents, MCP and review into one workflow.
- ZCode is not merely a terminal replacement. If selected, it would become a workspace/harness in its own right. It must not become ACES governance authority.
- ZCode's current documentation says project-level hooks are not executed. Therefore, do not rely on ZCode project hooks as the sole enforcement mechanism for ACES repository policy.
- ZCode's documented MCP import sources include Claude Code, Codex and OpenCode. Native import for DSH and Hermes is not confirmed.
- A hybrid arrangement (ZCode as the task workspace + Tabby as a neutral multi-CLI console) may be technically useful, but it adds another UI and must be justified by measured benefit. Do not assume this is the simplest answer.

## Decision criteria
1. Does it make one complex mission easier to decompose, assign and track?
2. Can all five harnesses run as independent processes without shared mutable session state?
3. Can outputs, logs, artifacts and process identity be captured reliably?
4. Can hooks enforce policy before/after tool execution, including repository scope?
5. Can DSH/Hermes/Claude Code/ZCode/Pi Durable coexist without credential or authority leakage?
6. Can it work on Windows 10 IoT Enterprise 22H2 and the user's Athlon 300U / 17.9 GiB RAM?
7. Does it reduce manual steps rather than add another layer?
8. Can interrupted work be recovered and independently verified?

## Selection gate
**No selection has been made. No installation has been performed.** Present the evidence matrix and trade-offs to the user. The user makes the platform and licensing decision. Install only after explicit selection and authorization.

## Work packages
- R0: pin exact product versions, local state and primary-source claims.
- R1: complete Tabby vs ZCode evidence matrix and recommendation; user decision.
- R2: install the selected candidate after explicit approval; verify launch, shell, process and resource use.
- R3: verify independent sessions for all five harnesses.
- R4: define the shared Task Contract, decomposition and handoff.
- R5: create harness adapters, hooks, prompts, skills and rules.
- R6: establish evidence journal, cross-review, recovery and STOP behavior.
- R7: run controlled end-to-end benchmark and security regression.
- R8: ACES acceptance.

## Sources
- Tabby product/features: https://tabby.sh/
- ZCode repository (Apache-2.0 declared in repository): https://github.com/zai-org/ZCode
- ZCode installation: https://zcode.z.ai/en/docs/install
- ZCode Agent: https://zcode.z.ai/en/docs/agents
- ZCode Agent framework: https://zcode.z.ai/en/docs/agent-framework
- ZCode hooks: https://zcode.z.ai/en/docs/hooks
- ZCode plugins: https://zcode.z.ai/en/docs/plugin
- ZCode MCP: https://zcode.z.ai/en/docs/mcp-services
- ZCode Skills: https://zcode.z.ai/en/docs/skill
- ZCode CLI: https://github.com/zai-org/ZCode/tree/main/apps/zcode-cli
- WezTerm control candidate: https://wezterm.org/

## Research conclusion (preliminary)
For a neutral terminal that hosts multiple independent harness CLIs, Tabby is the more direct fit. For the user's broader goal—making complex, decomposed engineering tasks simpler—ZCode currently shows more native workflow capabilities and is the more compelling primary candidate, subject to resolving the hook limitation, DSH/Hermes integration and actual hardware/resource tests. This is a research recommendation, not a selection or installation authorization.


## Local environment preflight — 2026-11-17

Read-only inspection of the user's Windows host confirmed:
- OS: Windows 10 IoT Enterprise, version 10.0.19045, build 19045.
- Memory: 17.9 GiB.
- Node.js: v24.22.1; npm: 11.19.1; pnpm: 12.11.2.
- ZCode Desktop 3.18.2 is installed; ZCode.exe exists. The `zcode` command is not on PATH. The desktop app has not been launched or runtime-tested in this research.
- Tabby is not found as a command and was not found in the inspected Windows uninstall registry entries.
- DSH 0.2.1-rc.3 is installed; a `dsh` npm shim is on PATH.
- Claude Code 2.1.302 is installed; `claude.exe` is on PATH.
- `hermes`, `pi`, and `wezterm` commands were not found. This is not proof that no alternate launch path exists; exact binary/package locations remain to be checked.

## Updated practical assessment

ZCode is already installed. A no-download, controlled desktop validation is the lowest-friction next experiment. The absence of a `zcode` PATH command does not prove the desktop app cannot run its integrated terminal or Agent.

Given the user's stated priority—making complex, decomposed work simpler—ZCode is the current lead candidate because it provides native task context, long-horizon planning, execution modes, terminal/browser, review, Skills, subagents and MCP. This is a recommendation for the user's consideration, not a selection.

Tabby remains the stronger direct candidate if the decisive requirement is a neutral, multi-pane terminal hosting several independent CLI sessions. Its official product documentation lists nested panes and restored tabs/panes. ZCode's documented terminal-panel behavior does not yet prove five simultaneous interactive external harness sessions with reliable PTY, cancellation, output capture and process identity.

### Required controlled tests before selection
1. Launch the already-installed ZCode Desktop and record exact visible version, sign-in/model prerequisites and first-run behavior.
2. Open its integrated terminal and run harmless read-only commands.
3. Test one external interactive CLI process at a time, starting with `claude --version` and `dsh --version`; do not run agent tasks or edit files.
4. Test whether multiple terminal sessions remain independently active and whether output, cancellation and working directories remain distinct.
5. Inspect ZCode's actual hook configuration and event behavior without enabling policy-changing hooks.
6. Only then decide whether Tabby adds a necessary terminal capability or would be redundant.

### Decision boundary
- **ZCode leads** for integrated task execution and reducing manual coordination.
- **Tabby leads** for neutral multi-CLI terminal multiplexing.
- **No selection, no installation, no configuration changes, no Canon changes** have been made.


## Release, license and resource evidence — 2026-11-17

- Tabby latest release found: v1.0.238 (2026-10-07). Official product page documents nested panes, tab/pane restoration and Windows shell support. Repository LICENSE is MIT.
- ZCode latest release found: v3.18.2 (released 2026-11-13). Release notes add Worktree support for parallel task development and a session-management tool. The checked source repository LICENSE is Apache-2.0; NOTICE.md explicitly limits that statement to first-party repository code and distinguishes third-party components and deployment/runtime data behavior. This is a source-license fact only; it does not decide the user's proprietary-product acceptability.
- Local inspection found 10 existing ZCode processes. Snapshot: total ZCode working set about 864 MiB; summed private memory about 1,151 MiB; system free physical memory about 0.5 GiB of 17.9 GiB. This is a point-in-time measurement, not proof that ZCode alone caused memory pressure or a representative clean-idle baseline.
- ZCode processes were already running before this research; this investigation did not launch them. Runtime behavior and current session contents were not inspected.

### Updated recommendation
ZCode remains the lead candidate for the user's stated priority: simplify complex, decomposed engineering work. It is already installed and running, has native task/agent/skills/subagent/MCP/review features, and its current release includes worktree-based parallel task support. Do not install Tabby yet.

Before deciding, test the existing ZCode desktop's integrated terminal with harmless commands and verify whether external interactive CLIs can run as separate sessions. Because the machine had only about 0.5 GiB free memory at the measurement point, begin with serial execution and measure resource use before any multi-agent parallel run. Tabby remains the fallback if ZCode cannot provide reliable independent terminal sessions.

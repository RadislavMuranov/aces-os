# HDE-002 — Implementation Decomposition

**Status:** STEP 1 COMPLETE — SYSTEM INVENTORY  
**Experiment:** HDE-002  
**Date:** 2026-09-03  
**Branch:** `architecture/priority-realization-roadmap-v2`

## 0. Contract Freeze

### Objective
Decompose modern agentic development systems at implementation/architecture level rather than product/UI level, then derive the minimum defensible architectural boundary for ACES OS.

### Systems in scope
1. ZCode
2. DeepSeek Harness (DSH)
3. Claude Code
4. OpenAI Codex
5. OpenCode

### Architectural layers in scope
1. MODEL
2. AGENT
3. HARNESS
4. TOOLS
5. CONTEXT
6. MEMORY
7. EXECUTION
8. VERIFICATION
9. EPISTEMIC AUTHORITY
10. DECISION AUTHORITY
11. EXECUTION AUTHORITY
12. UI

### Inventory dimensions
The decomposition must explicitly inspect, where present:

- Model
- Agent / agent loop
- Harness / runtime substrate
- Tools / capabilities
- Context construction and propagation
- Memory / persistence
- Execution and side effects
- Verification / completion criteria
- Permissions
- Approval / confirmation
- Subagents
- Plugins / extensions
- Hooks
- MCP
- Sandbox / environment isolation
- UI
- Telemetry / observability

### Evidence rule
No architectural conclusion may be promoted solely from product naming, marketing terminology, UI behavior, or analogy.

Each material claim must be traceable to implementation evidence where available: official architecture documentation, source code, configuration/schema, runtime behavior, or authoritative technical documentation.

Evidence must record:

`system → feature → evidence → source → confidence`

### Normalization rule
For every observed function, identify its **primary architectural owner**. Secondary dependencies may be recorded but must not obscure the primary boundary.

### Authority rule
The experiment must distinguish, at minimum:

`Capability → Permission → Approval → Authorization → Execution → Verification`

and must separately identify who can:

`propose → decide → authorize → execute → verify → persist → canonicalize`

### ACES non-assumption rule
The tentative ACES boundary is a hypothesis, not a finding, until implementation evidence from Steps 1–6 supports it.

Tentative hypothesis to be tested:

- ACES owns Epistemic Authority.
- ACES owns Decision Authority.
- ACES owns Execution Authority.
- ACES owns Canonical Memory.
- ACES owns Evidence.
- ACES owns Verification.
- ACES owns or governs Orchestration.
- Harness, Agent, Model, Tools and UI are replaceable/delegable execution components.

### Scope boundary
HDE-002 does **not** redesign ZCode, DSH, Claude Code, Codex, or OpenCode. It does not grant trust or authority to any external system. It only reconstructs implementation boundaries and derives an evidence-backed ACES boundary.

### Execution sequence
The frozen sequence is:

`0 CONTRACT FREEZE → 1 SYSTEM INVENTORY → 2 IMPLEMENTATION EVIDENCE → 3 LAYER MAPPING → 4 TRUST/AUTHORITY MAPPING → 5 CROSS-SYSTEM COMPARISON → 6 ACES GAP ANALYSIS → 7 ACES BOUNDARY SPEC → 8 FINAL VERDICT → COMPLETE/FREEZE`

### Gates
**Step 0 PASS condition:** all systems, layers, inventory dimensions, evidence rules, authority distinctions, scope boundaries, and execution sequence are explicitly frozen.

**Status:** PASS.

### Non-evolution rule during experiment
No new architectural layer, ownership claim, canon item, or implementation requirement is to be added during later steps merely because it appears convenient. Any such finding must first be recorded as evidence/analysis and only becomes an ACES architectural decision after Step 8.

### Governing principle
> No architectural promotion without implementation evidence.

> No external Agent/Harness receives ACES Authority merely because it possesses corresponding capability.

## 1. System Inventory

**Gate:** PASS — all five systems are covered against the frozen inventory dimensions.  
**Inventory status:** descriptive only; no ownership or authority conclusions are made in this step.

| System | Model | Agent / Loop | Harness / Runtime | Tools | Context | Memory | Execution | Verification / Completion | Permissions / Approval | Subagents | Plugins / Extensions | Hooks | MCP | Sandbox / Isolation | UI | Telemetry |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **ZCode** | GLM-family integration; model selectable in task flow | First-party ZCode Agent; long-task Goal Mode; isolated subagents | ZCode Agent + task/session runtime; execution-mode control | Built-in/project tools; commands; skills; plugin-provided capabilities | Goal, task context, files, workspace/project instructions, Git context | Project Memory; local-only and distinct from versioned `AGENTS.md` | File edits, commands, network/tool actions governed by execution mode | Goal Mode checks goal completion between rounds and continues until completion/pause/budget | Four execution modes; permission-gated requests with user confirmation | General-purpose + Explore; custom subagents | Plugins bundle skills, commands, subagents, MCP servers, hooks | Plugin/hooks and lifecycle automation | Plugin MCP servers and configured MCP | Execution modes constrain/mediate actions; environment-specific controls documented separately | Task-oriented development UI | Task/session state and activity surfaced in UI |
| **DSH** | `ctx.llm` model adapter seam | `ctx.agents` Agent interface + `ctx.agentLoop` concrete driver | Cordis plugin tree; all product components are plugins | Scoped `ctx.tools`; guarded pre/execute/post pipeline | `ctx.systemPrompt`; session history; injected context; inbox | Append-only `ctx.sessions` session event log; durable source of truth for session state | Tool execution pipeline, subprocess/sandbox backends, turns/steps | Agent events include validation/continuation; goal driver can continue same-session objective | Tool guards/policy pipeline; approval policy in base composition | Agent registry; subagent providers behind Agent interface | Cordis plugins, bundles, profiles | Typed event extension points and hooks | Available as extension mechanism; not treated as authority | `ctx.sandbox`; spawned-process confinement | Web/headless compositions render/drive agents | Session events and telemetry services |
| **Claude Code** | Configurable model per session/subagent | Main Claude Code agentic loop; built-in/custom subagents | CLI/session runtime with tool loop, context management and lifecycle hooks | Read/Edit/Write/Bash/Grep/Glob and other tools; skills/MCP tools | Prompt, CLAUDE.md hierarchy, Git state, tool results, subagent context | CLAUDE.md + project/user/local memory; custom subagents can have persistent memory | Tool calls, shell, file edits, MCP actions | Stop/completion hooks, prompt/agent hooks, task completion events; subagent lifecycle | Permission modes and permission requests; inherited/overridden subagent controls | Explore/Plan/general-purpose/custom; foreground/background/fork variants | Plugins, skills and custom agent definitions | Extensive lifecycle hook system incl. PreToolUse/PostToolUse/SubagentStart/Stop | MCP servers and MCP tools | Permission modes plus optional worktree isolation for subagents | CLI and associated task/session interfaces | Transcript/session/subagent event visibility and hook inputs |
| **OpenAI Codex** | Codex/reasoning model selectable/configured | Codex agent loop; worker/explorer subagents; multi-agent orchestration | Local CLI/app runtime with sandbox + approval control | Local filesystem/shell tools, web/search and configured capabilities | Prompt + workspace/directory context + tool results + session/thread state | Session/thread state and configuration; agent-specific configuration; persistent project config where defined | Local file edits and command execution; sandbox boundary | Agent-driven task completion; approvals and execution results feed the loop | Approval policies plus execpolicy; human approval for escalations depending on mode | Worker/explorer/custom agents; parallel workflows | Plugins/extensions and configured capabilities | Runtime approval/execution integration and agent workflow events | MCP servers/plugins | Sandbox modes bound filesystem/network execution; escalation can require approval | CLI/TUI/app surfaces | Thread/agent activity and execution state |
| **OpenCode** | Model configured per agent | Primary + subagent agent profiles; Task-based delegation | Agent/session runtime around configured agents and tools | Built-in tools + custom tools + MCP tools | System prompt, project config, agent prompt, tool results, task context | Project/configured agent state; persistent knowledge mechanisms vary by deployment | Tool actions against workspace/external resources | Goal/task workflow and agent completion; no independent canonical verification layer identified in inventory | Fine-grained allow/ask/deny permissions, including tool/resource patterns and subagent invocation | Primary/subagent agents; hidden/internal agents | Custom tools, skills, plugins/extensions and MCP | Extension/lifecycle mechanisms | MCP tools and servers | Permission boundaries; external-directory restrictions; environment controls | Terminal/TUI/web surfaces depending deployment | Session/task/tool activity |

### Inventory evidence register

**ZCode**
- First-party Agent, project context and project Memory: https://zcode.z.ai/en/docs/agents
- Goal Mode and iterative completion behavior: https://zcode.z.ai/en/docs/goal
- Subagents and isolated contexts: https://zcode.z.ai/en/docs/subagents
- Plugins bundling skills/commands/subagents/MCP/hooks: https://zcode.z.ai/en/docs/plugin
- Permission/execution modes and confirmation workflow: https://zcode.z.ai/en/docs/safety-confirm

**DSH**
- Architecture, pluginized model/tool/session/agent-loop components and runtime flow: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md
- Core subsystem ownership and Agent/agent-loop separation: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/core.md
- Tool registry and guarded execution pipeline: https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/core/tools/README.md
- Extension/plugin mechanisms: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cookbook/extension-cookbook.md

**Claude Code**
- Subagents, tools, permissions, memory, MCP, hooks and isolation configuration: https://code.claude.com/docs/en/subagents
- Hook lifecycle and tool/subagent events: https://code.claude.com/docs/en/hooks

**OpenAI Codex**
- Local coding agent and approval modes: https://help.openai.com/en/articles/11096431
- Sandbox/approval architecture: https://openai.com/index/running-codex-safely/
- CLI sandbox and approval controls: https://www.mintlify.com/openai/codex/concepts/sandboxing
- Subagent workflows and custom agent configuration: https://github.com/openai/codex/tree/main

**OpenCode**
- Agent profiles, primary/subagent modes and permission configuration: https://opencode.ai/docs/agents/
- Tool capabilities and permissions: https://opencode.ai/docs/tools/
- Fine-grained permission rules: https://opencode.ai/v2/docs/permissions
- Skills and skill permissions: https://opencode.ai/docs/skills/

### Step 1 boundary
This inventory establishes **what exists to be decomposed**. It intentionally does not answer which layer owns each function, whether a mechanism constitutes authority, or whether any component should be trusted by ACES. Those questions are deferred to Steps 2–6.

**Step 1 result: PASS.**

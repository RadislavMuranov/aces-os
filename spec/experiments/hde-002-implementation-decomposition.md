# HDE-002 — Implementation Decomposition

**Status:** STEP 2 COMPLETE — IMPLEMENTATION EVIDENCE  
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

## 2. Implementation Evidence

### 2.1 Evidence standard

Step 2 converts the inventory from documented feature presence into implementation-backed evidence. Evidence is classified as:

- **SOURCE:** directly observable official source/configuration/schema.
- **ARCH-DOC:** official architecture or subsystem documentation describing the concrete implementation contract.
- **TECH-DOC:** authoritative technical documentation describing implemented runtime behavior.
- **RUNTIME-DOC:** official documentation of actual runtime behavior/configuration rather than product positioning.

**Confidence:** HIGH when source/schema or explicit architecture contract is available; MEDIUM when the implementation is documented authoritatively but source is not public; LOW is not sufficient for promotion of a material architectural claim.

No Step 2 entry is an authority conclusion. The entries record what the implementation demonstrably does.

### 2.2 ZCode implementation evidence

| Function | Evidence | Source | Confidence |
|---|---|---|---|
| Agent runtime | ZCode Agent is the first-party default agent; it accepts goal/context/files/commands/model/execution mode and drives continuous project work. | Official ZCode Agent documentation | HIGH |
| Context | Workspace files, `AGENTS.md`, attachments, conversation references, commands/skills, Git state and task context are explicitly injected/available to the Agent. | Official ZCode Agent documentation | HIGH |
| Memory | Project Memory is automatically accumulated by the Agent, stored on the local machine, not in Git, distinct from `AGENTS.md`, and unavailable to subagents. | Official ZCode Agent documentation | HIGH |
| Goal / verification | Goal Mode performs a separate verification after each round; changed files, command output and tests count as evidence; unfinished to-dos prevent completion. | Official ZCode Goal Mode documentation | HIGH |
| Execution control | Four execution modes alter confirmation/autonomy: ask-before-changes, edit-automatically, plan, full-access. | Official ZCode Safety Confirmation / Agent documentation | HIGH |
| Approval | Permission-gated requests pause the task, display the exact planned action, and continue only after user decision; allow/always-allow/reject are explicit decisions. | Official ZCode Safety Confirmation documentation | HIGH |
| Subagents | Primary Agent launches specialized subagents in isolated contexts; built-in general-purpose and Explore subagents exist. | Official ZCode Subagents documentation | HIGH |
| Extension composition | A plugin can bundle skills, commands, subagents, MCP servers and hooks; enabling registers runnable components into the workspace. | Official ZCode Plugin documentation | HIGH |
| Browser execution | Browser automation can open URLs, click, fill forms, take screenshots and react to actual page state through the built-in Browser Use plugin. | Official ZCode Agent documentation | HIGH |

Evidence references: ZCode Agent and memory citeturn1view0; Goal verification citeturn1view1; isolated subagents citeturn2view0; plugin composition citeturn2view1; execution/approval behavior citeturn2view2.

### 2.3 DeepSeek Harness implementation evidence

| Function | Evidence | Source | Confidence |
|---|---|---|---|
| Runtime composition | Cordis is the framework; every major product component, including model adapter, tool registry, session log and agent loop, is a plugin and therefore replaceable by composition. | DSH architecture.md | HIGH |
| Agent vs loop | `core/agent` owns the public Agent interface/registry/events while `core/agent-loop` contains the concrete default driver. | DSH core subsystem documentation | HIGH |
| Model seam | `llm/llm` supplies message/stream vocabulary and the model adapter seam through `ctx.llm`. | DSH architecture/core documentation | HIGH |
| Session source | `ctx.sessions` is an append-only typed event log and documented single source of truth; model-visible history is derived from it. | DSH session + core documentation | HIGH |
| Context construction | The loop assembles system-prompt sections/tool schemas, derives history from the session log, then sends the model request. | DSH architecture/core documentation | HIGH |
| Tool execution | `ctx.tools` is a scoped registry with a guarded pipeline including pre-execute, execute, post-execute and final-result observation. | DSH architecture/capability-seams documentation | HIGH |
| Execution enclosure | Turns/steps and tool calls/results are explicitly represented as durable events; sandbox/subprocess providers form execution seams. | DSH architecture/session documentation | HIGH |
| Lifecycle interception | `agent/*` and `tools/*` are live extension points; listeners can reject/rewrite model-visible input or intercept tool calls. | DSH architecture/agent-lifecycle documentation | HIGH |
| Capability scoping | Per-agent scopes can mount capabilities and unwind them with the agent; session presets can isolate registries/capabilities. | DSH architecture + implemented agent-preset note | HIGH |
| Persistence/replay | Fork, resume, transcripts, telemetry and persistence derive from the session event stream; model-visible inputs must be reconstructable from the log. | DSH architecture/session documentation | HIGH |

Evidence references: DSH architecture citeturn0search0; DSH core subsystem citeturn0search1; DSH session source-of-truth behavior citeturn0search7; capability seams/tool pipeline citeturn0search8; agent lifecycle citeturn0search10.

### 2.4 Claude Code implementation evidence

| Function | Evidence | Source | Confidence |
|---|---|---|---|
| Agent/subagent model | Built-in and custom subagents have their own configuration, model, tools and context; foreground/background execution is supported. | Official Claude Code subagent documentation | HIGH |
| Persistent memory | Subagents can be configured with `memory: user/project/local`; persistent memory directories survive conversations and can be versioned or local. | Official Claude Code subagent documentation | HIGH |
| Tool capability control | Subagents can be restricted by tool access, MCP servers and permission mode; plugin-loaded subagents have restrictions on certain security-sensitive frontmatter fields. | Official Claude Code subagent documentation | HIGH |
| Hook interception | `PreToolUse` runs after tool parameters are created and before processing the call; it can allow, deny, ask or defer. | Official Claude Code hooks documentation | HIGH |
| Hook coverage | Hooks cover tool use, subagent lifecycle and other session/application events; MCP tool names can be matched by PreToolUse. | Official Claude Code hooks documentation | HIGH |
| Context separation | Subagents operate with separate context windows; persistent memory is explicitly separate from the main conversation auto-memory. | Official Claude Code subagent documentation | HIGH |

Evidence references: subagent implementation/configuration and memory citeturn0search3turn2view3; PreToolUse control citeturn2view4.

### 2.5 OpenAI Codex implementation evidence

| Function | Evidence | Source | Confidence |
|---|---|---|---|
| Approval configuration | Official Codex source contains `approval_policy` and `sandbox_mode` configuration fields. | `openai/codex` source: `codex-rs/config/src/config_toml.rs` | HIGH |
| Sandbox/approval coupling | OpenAI documents sandbox as the technical execution boundary and approval policy as the condition for crossing or performing restricted actions. | Official OpenAI safety documentation | HIGH |
| Network boundary | Managed Codex execution does not use open-ended outbound access; policy can require approval for unfamiliar domains. | Official OpenAI safety documentation | HIGH |
| Command policy | Codex rules distinguish benign commands from dangerous patterns that can be blocked or require approval. | Official OpenAI safety documentation | HIGH |
| Subagent implementation | Official Codex source contains explicit `SubAgent` thread source kinds and subagent model/reasoning configuration fields. | `openai/codex` source | HIGH |
| Permission/sandbox mapping | Codex source includes functions mapping permission profiles to sandbox modes and checks whether a sandbox mode is permitted. | `openai/codex` source: `codex-rs/exec/src/lib.rs`, `tui/src/debug_config.rs` | HIGH |

Source evidence: official Codex source search results show `approval_policy`, `sandbox_mode`, subagent configuration and permission-to-sandbox mapping. fileciteturn16file0L1-L14 fileciteturn16file1L18-L32 fileciteturn16file2L36-L50

Runtime/safety evidence: OpenAI documents that sandbox defines filesystem/network execution boundaries while approval determines when Codex must ask to cross them. citeturn2view6

### 2.6 OpenCode implementation evidence

| Function | Evidence | Source | Confidence |
|---|---|---|---|
| Agent configuration | Agent configuration explicitly binds mode, model, prompt and permissions; primary/subagent modes are implementation fields. | Official OpenCode Agent documentation | HIGH |
| Subagent delegation | Primary agents can automatically or manually invoke subagents; child sessions represent delegated work. | Official OpenCode Agent documentation | HIGH |
| Subagent permission | `permission.task` controls which subagents an agent can invoke; matching rules can deny/allow/ask. | Official OpenCode Agent documentation | HIGH |
| Tool capability | Built-in, custom and MCP tools are exposed as LLM-callable capabilities; custom tools can execute arbitrary code. | Official OpenCode Tools documentation | HIGH |
| Tool permission | Tool permissions explicitly support allow/deny/ask, including pattern rules for MCP tools. | Official OpenCode Tools documentation | HIGH |
| Tool/environment execution | Built-in `bash` executes shell commands in the project environment; `external_directory` and related permissions constrain access. | Official OpenCode Agent/permission documentation | HIGH |
| MCP extension | MCP servers integrate external tools/services; they are configured as tool providers. | Official OpenCode Tools documentation | HIGH |

Evidence references: agent/subagent configuration and delegation citeturn2view7; tools and permission model citeturn2view8.

### 2.7 Normalized implementation evidence matrix

| System | Model seam | Agent/loop seam | Runtime/harness seam | Tool seam | Context/memory seam | Execution control | Verification evidence | Approval/permission evidence | Extension/subagent evidence |
|---|---|---|---|---|---|---|---|---|---|
| **ZCode** | Model selectable; thought-level controls model effort | First-party Agent + Goal Mode | Task/session/execution-mode runtime | Tools, commands, skills, browser, plugin capabilities | `AGENTS.md` + local Project Memory + task context | Four execution modes | Per-round separate goal verification using files/commands/tests | User approval / allow / always-allow / reject | Plugins + isolated subagents |
| **DSH** | `ctx.llm` adapter seam | `ctx.agents` + `ctx.agentLoop` | Cordis plugin composition | `ctx.tools` guarded pipeline | Event-sourced `ctx.sessions` + `ctx.systemPrompt` | Tool guards + sandbox/process seams | Agent validation/continuation + goal driver | Policy/approval components in composition | Cordis plugins + Agent providers/scopes |
| **Claude Code** | Configurable session/subagent model | Main loop + configurable subagents | CLI/session runtime + lifecycle hooks | Built-in + MCP + skills | Prompt/config + persistent subagent memory | Permission modes/hooks | Completion/task hooks and subagent lifecycle | Permission requests + PreToolUse allow/deny/ask/defer | Plugins + subagents + hooks |
| **Codex** | Model/config fields | Agent threads + subagent threads | CLI/app + sandbox/approval runtime | Shell/fs/web/configured capabilities | Thread/session state + workspace config | Sandbox + approval + rules | Task completion + execution results | `approval_policy` + exec policy | Explicit subagent source/config + extensions |
| **OpenCode** | Per-agent model field | Primary/subagent agent profiles | Session/runtime + permissions | Built-in/custom/MCP tools | Prompt/config/task context + persistent mechanisms | Tool/resource permissions | Task/agent completion signals | allow/ask/deny + pattern rules | Skills/custom tools/plugins/MCP + Task subagents |

### 2.8 Evidence gaps / limits

1. **ZCode source visibility:** the official documentation gives strong implementation contracts, but the product's complete internal source is not publicly available in the evidence set. Therefore ZCode implementation claims are TECH-DOC/RUNTIME-DOC rather than direct SOURCE claims.
2. **Claude Code source visibility:** the product is not treated as open-source evidence here; official technical documentation is the implementation evidence. This is sufficient for documented runtime contracts, but not for undocumented internals.
3. **Codex evidence depth:** direct official source evidence is available for configuration, sandbox/permission mapping and subagent structures; the full agent-loop decomposition is not inferred beyond what the source exposes.
4. **OpenCode source depth:** this step uses official technical documentation for runtime/configuration contracts. No claim about undocumented internals is promoted.
5. **Authority:** none of the above evidence is yet interpreted as epistemic, decision, or canonical authority. That analysis is explicitly deferred to Steps 3–6.

### 2.9 Step 2 gate

**PASS CONDITION:** every system has implementation/technical evidence for its material agentic runtime mechanisms; evidence provenance and confidence are recorded; evidence gaps are explicit; no ownership or authority conclusion is promoted.

**Result: PASS.**

**Step 2 conclusion:** the five systems are not merely UI variants. Their documented implementations expose materially separable mechanisms for model integration, agent loops, runtime/harness control, tools, context, memory, execution, verification/completion, permission/approval, subagents and extension mechanisms. DSH provides the strongest direct source-level decomposition; Codex provides substantial direct source evidence; ZCode, Claude Code and OpenCode provide strong official implementation/runtime documentation. This is an evidence finding only. Architectural ownership and trust/authority remain frozen for Steps 3–6.

**Step 2 result: PASS.**

## Step 3 onward

Not executed. The next permitted action is **Step 3 — LAYER MAPPING**.

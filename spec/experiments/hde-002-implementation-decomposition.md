# HDE-002 — Implementation Decomposition

**Status:** STEP 3 COMPLETE — LAYER MAPPING  
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

### Evidence rule
No architectural conclusion may be promoted solely from product naming, marketing terminology, UI behavior, or analogy. Material claims require implementation evidence: official architecture documentation, source code, configuration/schema, runtime behavior, or authoritative technical documentation.

### Frozen sequence
`0 CONTRACT FREEZE → 1 SYSTEM INVENTORY → 2 IMPLEMENTATION EVIDENCE → 3 LAYER MAPPING → 4 TRUST/AUTHORITY MAPPING → 5 CROSS-SYSTEM COMPARISON → 6 ACES GAP ANALYSIS → 7 ACES BOUNDARY SPEC → 8 FINAL VERDICT → COMPLETE/FREEZE`

**Step 0: PASS.**

## 1. System Inventory — PASS

The five systems were inventoried across Model, Agent/loop, Harness/runtime, Tools, Context, Memory, Execution, Verification, Permissions/Approval, Subagents, Extensions, Hooks, MCP, Sandbox/Isolation, UI and Telemetry. Inventory was descriptive only; no ownership or authority conclusions were made.

| System | Model | Agent / Loop | Harness / Runtime | Tools | Context | Memory | Execution | Verification | Permissions / Approval | Subagents | Extensions | Hooks | MCP | Sandbox | UI | Telemetry |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ZCode | GLM-family integration | First-party Agent + Goal Mode | Agent/task/session runtime | Tools, commands, skills, browser, plugins | Goal/files/project/Git/task context | Project Memory + `AGENTS.md` | File/command/network actions | Goal rounds + evidence checks | Execution modes + confirmation | General/Explore/custom | Plugins | Lifecycle/plugin hooks | Plugin MCP | Execution-mode/environment controls | Development UI | Task/session activity |
| DSH | `ctx.llm` | `ctx.agents` + `ctx.agentLoop` | Cordis plugin tree | `ctx.tools` guarded pipeline | system prompt + session-derived history | append-only `ctx.sessions` | turns/steps/tool/sandbox pipeline | validation/continuation + goal driver | guards/policy/approval composition | Agent registry/providers | Cordis plugins | typed lifecycle events | extension mechanism | `ctx.sandbox`/process confinement | web/headless composition | event/telemetry services |
| Claude Code | Configurable | Main loop + built-in/custom subagents | CLI/session runtime | Read/Edit/Write/Bash/Grep/Glob/MCP/skills | prompt + `CLAUDE.md` + tool/subagent context | project/user/local memory | shell/files/MCP | completion/task/subagent lifecycle | permission modes + PreToolUse | built-in/custom/foreground/background | plugins/skills | lifecycle hooks | MCP | permission/worktree isolation | CLI/task UI | transcripts/events |
| Codex | Configurable reasoning model | Agent threads + subagents | CLI/app + sandbox/approval runtime | shell/fs/web/configured capabilities | prompt/workspace/tool/thread state | thread/session/config state | file/command execution | task completion/execution results | `approval_policy` + exec policy | worker/explorer/custom | extensions/plugins | runtime workflow events | MCP/plugins | sandbox filesystem/network | CLI/TUI/app | thread/activity state |
| OpenCode | Per-agent model | Primary + subagents | session/agent runtime | built-in/custom/MCP | system/project/agent/task context | project/config state | workspace/external actions | task/agent completion | allow/ask/deny | primary/subagent/Task | skills/plugins/custom tools | extension lifecycle | MCP | permission/environment boundaries | terminal/TUI/web | session/task/tool activity |

## 2. Implementation Evidence — PASS

Step 2 established implementation-backed evidence for all five systems. DSH and Codex provide direct source evidence for important runtime/configuration boundaries; ZCode, Claude Code and OpenCode provide strong official technical/runtime documentation. Evidence gaps were explicitly recorded. No evidence was interpreted as epistemic, decision or canonical authority.

Principal implementation seams established: ZCode Agent/Goal/Memory/approval/subagents/plugins; DSH `ctx.llm`, `ctx.agents`, `ctx.agentLoop`, `ctx.sessions`, `ctx.tools`, sandbox and lifecycle seams; Claude Code subagents/memory/PreToolUse/hooks; Codex approval/sandbox/subagent source structures; OpenCode agent/model/permission/subagent/tool/MCP structures.

**Step 2: PASS.**

## 3. Layer Mapping

### 3.1 Mapping rule

Step 3 assigns each observed function to its **primary architectural layer** based only on Step 2 evidence. A layer may depend on other layers, but dependency does not transfer primary ownership.

This step does **not** determine trust, authority, or ACES ownership.

### 3.2 Normalized layer definitions

| Layer | Primary responsibility | Explicit non-responsibility |
|---|---|---|
| **MODEL** | Inference, generation, reasoning, prediction, proposed tool calls/plans | Does not itself execute tools or establish canonical truth |
| **AGENT** | Goal pursuit, loop decisions, task decomposition, delegation, continuation | Does not inherently possess external authority |
| **HARNESS** | Runtime substrate: sessions, turns, dispatch, lifecycle, retries, interruption, environment binding, capability composition, telemetry | Does not make epistemic truth authoritative merely by executing |
| **TOOLS** | Concrete capabilities that inspect/change digital resources | Capability availability is not authorization |
| **CONTEXT** | Assembly/propagation of current task information into execution/model inputs | Context presence does not imply truth |
| **MEMORY** | Persistence/retrieval of information across turns/sessions | Persistence does not imply canonical truth |
| **EXECUTION** | Realization of proposed actions as effects in an environment | Successful invocation is not proof of desired state |
| **VERIFICATION** | Testing/assessment whether an outcome satisfies an objective | Completion signal is not automatically canonical truth |
| **EPISTEMIC AUTHORITY** | Determination of what is accepted as knowledge/truth | Not assigned to external systems in this step |
| **DECISION AUTHORITY** | Binding selection of what should be done | Not assigned to external systems in this step |
| **EXECUTION AUTHORITY** | Binding authorization for digital/real-world side effects | Not assigned to external systems in this step |
| **UI** | Human-facing presentation/control surface | UI presence does not create architectural authority |

### 3.3 Cross-system primary-owner matrix

| Function | ZCode | DSH | Claude Code | Codex | OpenCode |
|---|---|---|---|---|---|
| Model inference | MODEL | MODEL seam (`ctx.llm`) | MODEL | MODEL | MODEL |
| Goal/task loop | AGENT | AGENT / agent-loop | AGENT | AGENT | AGENT |
| Session/runtime lifecycle | HARNESS | HARNESS / Cordis | HARNESS | HARNESS | HARNESS |
| Tool capability definition | TOOLS | TOOLS | TOOLS | TOOLS | TOOLS |
| Current context assembly | CONTEXT | CONTEXT | CONTEXT | CONTEXT | CONTEXT |
| Persistent memory | MEMORY | MEMORY/session persistence | MEMORY | MEMORY/session/thread state | MEMORY/config persistence |
| Side-effect realization | EXECUTION | EXECUTION | EXECUTION | EXECUTION | EXECUTION |
| Completion assessment | VERIFICATION | VERIFICATION | VERIFICATION | VERIFICATION | VERIFICATION |
| Permission/confirmation mechanism | HARNESS | HARNESS | HARNESS | HARNESS | HARNESS |
| Subagent lifecycle | AGENT + HARNESS | AGENT + HARNESS | AGENT + HARNESS | AGENT + HARNESS | AGENT + HARNESS |
| Plugin/extension loading | HARNESS | HARNESS | HARNESS | HARNESS | HARNESS |
| Hook/interception lifecycle | HARNESS | HARNESS | HARNESS | HARNESS | HARNESS |
| MCP integration | TOOLS + HARNESS | TOOLS + HARNESS | TOOLS + HARNESS | TOOLS + HARNESS | TOOLS + HARNESS |
| Sandbox/isolation | EXECUTION + HARNESS | EXECUTION + HARNESS | EXECUTION + HARNESS | EXECUTION + HARNESS | EXECUTION + HARNESS |
| Presentation | UI | UI | UI | UI | UI |
| Runtime telemetry | HARNESS | HARNESS | HARNESS | HARNESS | HARNESS |

### 3.4 Boundary findings

**A. Model ≠ Agent.** Each system exposes a runtime concept above model inference: goal pursuit, tool selection, continuation and/or delegation. DSH makes the seam explicit through `ctx.llm` versus `ctx.agents`/`ctx.agentLoop`.

**B. Agent ≠ Harness.** The Agent performs task-directed behavior; the Harness provides the runtime substrate hosting and constraining it. DSH gives the clearest direct source-level separation.

**C. Tool ≠ Execution.** A tool exposes a capability; execution realizes an effect and produces a result. Guarded tool pipelines, sandboxing and approval mechanisms demonstrate separability.

**D. Permission/approval ≠ authority.** Existing systems can gate actions, but Step 3 does not classify those mechanisms as epistemic, decision or execution authority. That is Step 4.

**E. Memory ≠ canonical knowledge.** Agent/project/session persistence is an implementation mechanism; persistence alone cannot establish truth or canonicality.

**F. Verification ≠ authority.** Tests, completion checks, hooks and execution results are verification mechanisms. Whether they are sufficient to establish an accepted state is a later authority question.

**G. UI ≠ underlying capability ownership.** UI presents and controls mechanisms implemented by Agent/Harness/Tools/Execution/etc.

### 3.5 Normalized architecture

The evidence supports:

`MODEL → AGENT → HARNESS → TOOLS → EXECUTION`

with cross-cutting state:

`CONTEXT ↔ MEMORY`

and outcome assessment:

`EXECUTION → VERIFICATION`

with:

`UI → human interaction/presentation`

The authority layers remain analytically separate and **unassigned**:

`EPISTEMIC AUTHORITY / DECISION AUTHORITY / EXECUTION AUTHORITY`

### 3.6 Step 3 gate

**PASS CONDITION:** implementation evidence is sufficient to assign every material observed function a primary architectural layer without relying on product/UI naming, while authority remains explicitly unassigned.

**RESULT: PASS.**

**Step 3 conclusion:** the five systems can be normalized into materially separable implementation layers: `MODEL | AGENT | HARNESS | TOOLS | CONTEXT | MEMORY | EXECUTION | VERIFICATION | UI`. The three authority layers remain distinct analytical dimensions and must not be silently conflated with permissions, agent loops, harnesses or verification.

**No Step 4 authority conclusion is made here.**

## Step 4 onward

Not executed. The next permitted action is **Step 4 — TRUST / AUTHORITY MAPPING**.

## Evidence sources

ZCode: https://zcode.z.ai/en/docs/agents ; https://zcode.z.ai/en/docs/goal ; https://zcode.z.ai/en/docs/subagents ; https://zcode.z.ai/en/docs/plugin ; https://zcode.z.ai/en/docs/safety-confirm

DSH: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md ; https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/core.md ; https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/core/tools/README.md ; https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cookbook/extension-cookbook.md

Claude Code: https://code.claude.com/docs/en/subagents ; https://code.claude.com/docs/en/hooks

OpenAI Codex: https://github.com/openai/codex/tree/main ; https://openai.com/index/running-codex-safely/ ; https://help.openai.com/en/articles/11096431

OpenCode: https://opencode.ai/docs/agents/ ; https://opencode.ai/docs/tools/ ; https://opencode.ai/v2/docs/permissions

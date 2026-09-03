# HDE-002 — Implementation Decomposition

**Status:** STEP 5 COMPLETE — CROSS-SYSTEM COMPARISON  
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
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
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

## 4. Trust / Authority Mapping — PASS

Step 4 distinguished **operational permission/approval** from **architectural, epistemic, decision and canonical authority**.

### 4.1 Normalized control chain

`CAPABILITY → PERMISSION → APPROVAL → AUTHORIZATION → EXECUTION → OBSERVED RESULT → VERIFICATION → ACCEPTANCE → CANONICALIZATION`

The researched systems implement substantial portions of the left/middle side of this chain, but implementation evidence does not establish an external system as the independent source of ACES epistemic or canonical authority.

### 4.2 Cross-system authority matrix

| System | Capability control | Permission / policy | Approval | Execution | Verification / completion | Epistemic / canonical authority |
|---|---|---|---|---|---|---|
| ZCode | Agent tools, commands, skills, browser, plugins | Execution modes | Human confirmation where required | ZCode Agent runtime | Goal rounds/checks | Not established |
| DSH | Capability seams/tools | Permission policy + guards | `ctx.approval` one-shot decisions | Guarded tool/sandbox pipeline | Result/continuation/goal mechanisms | Not established |
| Claude Code | Tools/MCP/subagents | Permission rules + hooks | User prompt/permission mechanism | CLI/session runtime | Task/subagent lifecycle | Not established |
| Codex | Shell/fs/web/configured capabilities | Sandbox + approval policy | User/auto-review authorization | Sandboxed runtime | Task/execution result | Not established |
| OpenCode | Built-in/custom/MCP tools | Allow/ask/deny rules | Ask/user approval | Agent/tool runtime | Task/agent completion | Not established |

### 4.3 Critical distinction

Operational systems may legitimately answer **“may this action proceed?”** without answering **“is this result true?”**, **“should this decision bind ACES?”**, or **“does this effect become canonical ACES reality?”**

DSH makes this boundary especially explicit: `ctx.approval` answers whether a specific action may proceed, while permission policy, guards and sandbox separately constrain execution. Its approval mechanism fails closed when no answerer exists. citeturn0search6turn0search3

ZCode exposes execution modes and confirmation as runtime permission control; this is operational gating, not evidence of independent epistemic authority. citeturn1search0

Claude Code exposes permission rules/hooks and configurable subagent capabilities; these enforce or modify tool authorization, but do not make a subagent a canonical truth authority. citeturn1search4turn1search1

Codex explicitly separates sandbox execution boundaries from approval policy. citeturn0search2

OpenCode similarly models tool permissions as allow/ask/deny controls over capabilities, including MCP tools. citeturn1search3turn1search7

### 4.4 Step 4 gate

**RESULT: PASS.**

**Step 4 conclusion:** operational permission and execution capability are present across all five systems, but no implementation evidence establishes any of them as an independent epistemic or canonical authority.

## 5. Cross-System Comparison — PASS

### 5.1 Comparison rule

Step 5 compares the five systems only after normalization from Steps 1–4. Comparison is made by **architectural role, boundary behavior, composability and authority separation**, not by product feature count or marketing category.

The comparison asks: **what architectural problem does each system solve, how does it solve it, where is the strongest boundary, and what remains outside its trust model?**

### 5.2 Normalized comparison matrix

| Dimension | ZCode | DSH | Claude Code | Codex | OpenCode |
|---|---|---|---|---|---|
| Primary center of gravity | Long-horizon developer Agent | Composable execution Harness | Agentic coding runtime + configurable subagents | Bounded agent execution with sandbox/approval | Configurable agent/tool runtime |
| Model ↔ Agent separation | Explicit first-party Agent over GLM family | Explicit `ctx.llm` vs `ctx.agents`/loop | Agent/subagent abstraction over selectable models | Agent threads/subagents over configurable models | Per-agent model configuration |
| Harness explicitness | Product-integrated runtime | **Highest / most explicit** | Strong runtime/session layer | Strong sandbox/approval runtime | Strong session/agent runtime |
| Capability composability | Plugins, skills, MCP, commands | **Capability seams + providers + consumers** | Tools, skills, MCP, hooks, plugins | Configured capabilities/plugins/MCP | Built-in/custom tools, MCP, skills/plugins |
| Subagent model | Built-in/custom/Explore; isolated task contexts | Provider-based subagents through `ctx.subagents` | Rich specialized subagents; isolated contexts | Worker/explorer/custom patterns | Primary/subagent model |
| Permission model | Execution modes / confirmation | Permission + guards + approval + sandbox | Rules + hooks + permission modes | Sandbox + approval policy + auto-review | Allow / ask / deny rules |
| Execution boundary | Environment/permission mode | Shared capability + sandbox world | Permission/worktree/session controls | **Sandbox/network boundary is first-class** | Workspace/environment boundary |
| Context architecture | Goal/project/task context + memory | **Event-log-derived model-visible context** | Prompt/rules/memory/subagent context | Thread/workspace/tool state | Session/project/agent context |
| Persistent memory | Project Memory + versioned project instructions | Durable session/event infrastructure | User/project/local agent memory | Session/thread/config state | Project/config state |
| Verification posture | Goal completion rounds/checks | Validation + continuation + durable results | Lifecycle/task completion + hooks | Execution/task result + review mechanisms | Task/agent completion |
| Authority model | Operational permissions/approval | Operational permission/approval/guards | Operational permissions/hooks | Operational sandbox/approval | Operational permissions |
| Canonical truth ownership | Not established | Not established | Not established | Not established | Not established |
| Provider/model portability | Moderate; strongly optimized for GLM | **High** by seam/provider design | High across model choices | High across configurable models | High across agent/model configs |
| Extension architecture | Product/plugin ecosystem | **Most architecturally explicit** | Mature plugin/skill/hook ecosystem | Runtime/config/plugin ecosystem | Strong custom-tool/MCP/plugin ecosystem |
| Best architectural lesson for ACES | Goal-driven UX and long-horizon agent loop | **Harness/kernel and capability-seam design** | Policy hooks, isolated subagents, memory scopes | Hard execution boundary and risk-tiered approval | Fine-grained capability policy |
| Primary limitation relative to ACES | Product/runtime couples Agent experience to vendor stack | No demonstrated ACES-level epistemic/canonical authority | Authority remains operational, not canonical | Verification/approval remain bounded to runtime | Permission system is not truth/decision authority |

### 5.3 Strongest implementation patterns by system

**ZCode — Agent-centric long-horizon execution.**

ZCode is strongest where a user wants to state a concrete development objective and let a first-party Agent continue through multiple rounds until its goal checks indicate completion. Its Goal Mode is explicitly designed for long-running work and repeated continuation. citeturn1search10 Safety Confirmation provides visible execution modes and approval before risky actions. citeturn1search0

**Architectural lesson:** ACES should preserve the simplicity of a goal-oriented interaction surface while keeping governance and canonical state outside the Agent runtime.

**DSH — Harness/kernel and composability.**

DSH provides the cleanest implementation separation between Agent, LLM, runtime and capabilities. Its architecture defines a turn as a model request plus its tool calls, derives model-visible history from the session log, and exposes swappable capability seams. citeturn0search1 Its capability-seam architecture separates service definition, provider and consumer so providers can be replaced without changing the model-facing tool contract. citeturn0search4

The DSH tool pipeline also explicitly separates permission, approval, guards and sandboxing around execution. citeturn0search6

**Architectural lesson:** DSH is the strongest reference for ACES's execution-kernel boundary, especially for provider substitution, capability composition, durable context reconstruction and fail-closed action control.

**Claude Code — Policy interception and subagent specialization.**

Claude Code has a mature subagent architecture with isolated contexts, per-agent tool restrictions, permission modes, hooks and memory scopes. citeturn1search1 Its permission model explicitly distinguishes security enforcement from project guidance: permissions/hooks enforce limits, while project instructions guide behavior. citeturn1search6

**Architectural lesson:** ACES should treat policy enforcement and agent instructions as different mechanisms, and should preserve independently scoped subagent capabilities without granting them canonical authority.

**Codex — Explicit bounded execution.**

Codex provides the clearest first-class treatment of the execution boundary: sandboxing defines where the system can write and whether it can access the network, while approval policy controls when the agent must ask. OpenAI also describes auto-review as a mechanism for reducing approval friction while still applying authorization logic. citeturn0search2

**Architectural lesson:** ACES should make execution authority explicit and independently enforceable, rather than assuming that a tool or Agent having access implies authorization.

**OpenCode — Fine-grained capability policy.**

OpenCode exposes a compact permission algebra of `allow`, `ask`, and `deny`, with rules that can target built-in, custom and MCP tools. Per-agent overrides provide additional scoping. citeturn1search3turn1search7

**Architectural lesson:** ACES should retain fine-grained capability policy as a low-level control primitive, but place it below a separate authority/evidence layer.

### 5.4 Cross-system convergence

Despite significant implementation differences, all five systems converge on the same broad operational stack:

`MODEL → AGENT → RUNTIME/HARNESS → CAPABILITIES/TOOLS → EXECUTION → RESULT`

They also converge on a second operational control plane:

`POLICY → PERMISSION → APPROVAL → EXECUTION BOUNDARY`

And all five leave the following question outside the demonstrated operational control plane:

`RESULT → VERIFIED ACCEPTANCE → CANONICAL ACES REALITY`

This convergence is stronger evidence than any single product's terminology because it survives normalization across five independent implementations.

### 5.5 Major architectural differences

1. **Harness explicitness:** DSH makes the runtime/capability architecture most explicit; the other systems integrate comparable functions more tightly into their product runtime.
2. **Execution boundary:** Codex makes sandbox/network constraints particularly explicit as a first-class safety boundary.
3. **Goal continuity:** ZCode emphasizes long-horizon goal continuation as a first-class user interaction primitive.
4. **Policy interception:** Claude Code provides unusually rich hooks and subagent-specific controls for runtime policy enforcement.
5. **Permission granularity:** OpenCode provides a concise, configurable allow/ask/deny model with pattern matching and per-agent overrides.
6. **Context provenance:** DSH's event-log-derived context provides the clearest implementation pattern for reconstructable model-visible state.

### 5.6 Architectural ranking for ACES reference purposes

This is **not a product ranking**. It ranks implementation patterns by their relevance to the frozen ACES architecture.

| Rank | Reference | Why it matters to ACES |
|---|---|---|
| 1 | **DSH** | Best reference for Harness/Execution Kernel, capability seams, durable context and composable providers |
| 2 | **Codex** | Best reference for explicit execution boundary, sandboxing and approval/risk control |
| 3 | **Claude Code** | Best reference for subagent specialization, hooks and scoped policy/memory |
| 4 | **ZCode** | Best reference for goal-oriented long-horizon Agent UX and continuation |
| 5 | **OpenCode** | Best reference for compact fine-grained capability permissions and configurable agent/tool policy |

This ranking does **not** imply that ACES should adopt the products or their trust models. It identifies reusable architectural patterns only.

### 5.7 Step 5 gate

**PASS CONDITION:** after normalization, the five systems exhibit materially comparable architectural layers and control boundaries; their differences can be explained as different implementations of the same broad operational problem rather than as fundamentally incompatible architectures.

**RESULT: PASS.**

**Step 5 conclusion:** the cross-system comparison confirms a stable common substrate — `MODEL → AGENT → HARNESS/RUNTIME → TOOLS/CAPABILITIES → EXECUTION → RESULT` — plus an operational control plane of `POLICY → PERMISSION → APPROVAL → EXECUTION BOUNDARY`. The decisive unresolved layer is not another Agent/Harness/Tool mechanism. It is the independent authority/evidence boundary governing whether verified outcomes become accepted and canonical ACES reality.

## 6. Step 6 onward

Not executed. The next permitted action is **Step 6 — ACES GAP ANALYSIS**.

## Evidence sources

ZCode: https://zcode.z.ai/en/docs/agents ; https://zcode.z.ai/en/docs/goal ; https://zcode.z.ai/en/docs/subagents ; https://zcode.z.ai/en/docs/plugin ; https://zcode.z.ai/en/docs/safety-confirm

DSH: https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md ; https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/core.md ; https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/approval.md ; https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/capability-seams.md ; https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/cookbook/extension-cookbook.md

Claude Code: https://code.claude.com/docs/en/subagents ; https://code.claude.com/docs/en/hooks ; https://code.claude.com/docs/en/permissions

OpenAI Codex: https://github.com/openai/codex/tree/main ; https://openai.com/index/running-codex-safely/ ; https://help.openai.com/en/articles/11096431

OpenCode: https://opencode.ai/docs/agents/ ; https://opencode.ai/docs/tools/ ; https://opencode.ai/v2/docs/permissions

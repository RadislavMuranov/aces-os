# HDE-002 — Implementation Decomposition

**Status:** CONTRACT FROZEN  
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

# ACES OS — Notion Control-Plane Index / Iteration Integrity

**Status:** INDEX / CROSS-SYSTEM RECONCILIATION RECORD
**Date:** 2026-09-18
**Repository:** `RadislavMuranov/aces-os`
**Branch:** `control/reconcile-iteration-integrity-20260917`

## Authority Boundary

The authoritative operational control-plane rules are maintained in Notion under the ACES Rules layer. Git is the versioned engineering/documentation index and implementation boundary; Git presence does not promote a claim to truth.

Authoritative Notion control artifacts:

- **RALPH LOOP — ACES Governance Mandate v1.0**
- **ACES EXECUTION CONTROL PLAN — Plan / Control / Roadmap / Protocols v1.0**
- **PROTOCOL-ITERATION-CLOSURE-001 — Evidence / Report / Roadmap Synchronization**
- **P1 — STIL RESEARCH-VERIFICATION NODE / REPORT**

## Responsibility Mapping

| Control function | Authoritative node / gate | Role |
|---|---|---|
| Bounded governance pattern across every non-trivial process | **RALPH-LOOP-GOVERNANCE-MANDATE-001** | Global bounded continuation/closure governance |
| Identify and model state-transition integrity failure | **P1 — STIL RESEARCH-VERIFICATION NODE** | Research / verification only; not runtime enforcement |
| Consolidate closure, reporting, roadmap sync, blocker propagation and anti-drift | **P2 — CONTROL PROTOCOL CONSOLIDATION** | Normative control-protocol consolidation |
| Enforce closure/continuation at an iteration boundary | **ITERATION-CLOSURE-GATE-001 / PROTOCOL-ITERATION-CLOSURE-001** | Per-iteration guard |
| Prevent recurrence across subsequent iterations | **P7 — CONTINUOUS CONTROL** | Recurrence-prevention node |
| Runtime boundedness of a specific A-RL mechanism | **H-F-001 configuration governance** | Mechanism-specific runtime configuration; not the general iteration controller |

## Critical Distinction

For the specific question “what prevents an infinite/degrading iteration loop?” the control stack is:

`RALPH LOOP GOVERNANCE → ITERATION-CLOSURE-GATE-001 → P7 CONTINUOUS CONTROL`

- **Ralph Loop** defines the mandatory boundedness, iteration counter, execution budget, stop conditions, retry/repetition threshold and/or no-progress circuit breaker.
- **ITERATION-CLOSURE-GATE-001** prevents an individual iteration from continuing or terminating without evidence-backed closure and an explicit continuation state.
- **P7** owns recurrence prevention across subsequent iterations.
- **P1/STIL** explains and verifies the systemic failure model; it is not itself the runtime guard.

Therefore, **P7 alone is too narrow to describe the full anti-infinite-loop control.** The governing mechanism is the **Ralph Loop Governance Mandate**, operationalized through the Closure Gate and P7.

## Failure Model

`UNBOUNDED ITERATION → STALE / DIVERGENT STATE → REPEATED NON-PROGRESS → CONTEXT / ABSTRACTION DRIFT → OPERATIONAL HALLUCINATION → PROGRESSIVE DEGRADATION → RECURRENCE`

## Mandatory Control Chain

`LOAD STATE → SELECT ONE NEXT ATOMIC NODE → EXECUTE → CAPTURE EVIDENCE → VERIFY → UPDATE PERSISTENT STATE → RECONCILE → CONTINUE / BLOCKED / STALLED / EXHAUSTED / CLOSED`

Required safeguards:

- explicit execution bounds;
- iteration counter / budget;
- stop conditions;
- retry/repetition threshold and/or no-progress circuit breaker;
- authoritative-state reload at each fresh iteration;
- control-plane discovery before requesting human discovery;
- no bare `NONE — HUMAN DECISION REQUIRED`;
- no downstream execution from BLOCKED/FAIL;
- no silent transitions;
- no PASS/CLOSED without evidence and reconciliation.

## ACTUAL EXECUTION ENFORCEMENT VERIFICATION — 2026-09-18

**Verification target:** `RALPH/P7 GOVERNANCE → ACTUAL EXECUTION ENFORCEMENT`

**Result:** **RUNTIME ENFORCEMENT NOT PROVEN / ACES IMPLEMENTATION ABSENT IN INSPECTED REPOSITORY STATE**

### ACES repository evidence

Inspected repository: `RadislavMuranov/aces-os`
Branch: `control/reconcile-iteration-integrity-20260917`
Commit before this reconciliation: `0f6266ebf6780247536f9e6d94bf7b118d4ca667`

The inspected tree contains the governance/index artifacts, but `src/` contains only `.gitkeep` and `tests/` contains only `.gitkeep`. No ACES runtime implementation of Ralph/P7, iteration counter, execution budget, retry/repetition threshold, no-progress circuit breaker, or Closure Gate enforcement was found in the inspected repository state.

### DSH comparison evidence

Official external execution substrate: `deepseek-ai/deepseek-harness`, branch `master`.

Observed DSH `packages/core/agent-loop` responsibilities include the per-agent execution loop, turn/step lifecycle, cancellation, durable session integration, bounded parallel tool calls, and the lifecycle extension point `agent/turn-stopping`.

DSH documentation explicitly states **No built-in turn budget**; a policy that bounds runaway turns must cancel from an existing lifecycle extension point such as `agent/turn-stopping`.

Therefore DSH provides an execution-kernel lifecycle seam, but it is **not evidence of ACES Ralph/P7 enforcement**.

### Enforcement boundary

`RALPH GOVERNANCE = ACES CONTROL CONTRACT`
`P7 = RECURRENCE-PREVENTION RESPONSIBILITY`
`ITERATION-CLOSURE-GATE-001 = PER-ITERATION CONTROL CONTRACT`
`DSH = PER-AGENT EXECUTION KERNEL`
`ACES RUNTIME ENFORCEMENT OF RALPH/P7 = NOT PROVEN`

The enforcement boundary remains ACES-owned above the DSH execution kernel. No implemented ACES control component at that boundary was found.

### Consequence

The governance reconciliation is valid, but the anti-infinite-loop protection is presently **documented rather than runtime-enforced** in the inspected ACES repository. DSH must not be treated as implicit enforcement of Ralph/P7.

## HARNESS-CAPABILITY-RECONSTRUCTION-002

**Contract artifact:** [HARNESS-CAPABILITY-RECONSTRUCTION-002 — Minimal ACES ↔ Orca ↔ DSH Enforcement Contract](https://app.notion.com/p/3de0e90e16c6819c8c78e2c97cbac06d?pvs=204)

**Status:** RESEARCH / CONTRACT DEFINITION — NOT YET ACCEPTED / NOT IMPLEMENTATION-AUTHORIZED

The contract defines the minimum boundary:

`ACES PRECHECK → ORCA DISPATCH → DSH EXECUTE → DSH TRACE/RECEIPT → ORCA AGGREGATE → ACES VERIFY/RECONCILE → CONTINUE / BLOCKED / STALLED / EXHAUSTED / CLOSED`

Ownership:

- ACES: authorization, bounds policy reference, acceptance criteria, verification, continuation, AcceptedState.
- Orca: fleet dispatch, delegation, admission, orchestration state, correlation preservation.
- DSH: per-agent loop, session/history, tools, lifecycle, cancellation, execution trace.
- Digital World / CLA: actual external effects.

Critical invariants:

`ExecutionReceipt ⇏ AcceptedState`
`DSH/Orca MUST NOT create or extend ACES authorization`
`Every run MUST remain correlatable: ExecutionID → AgentRunID → trace/evidence`
`Persistent ACES state MUST be reconciled before continuation`

Required implementation evidence before authorization:

1. exact Orca dispatch/admission surface;
2. exact DSH lifecycle API for stop enforcement;
3. executable field mapping;
4. end-to-end trace correlation;
5. normal completion test;
6. forced-stop/circuit-breaker test;
7. failure-closed behavior;
8. independent verification.

No runtime implementation is authorized by this artifact.

## SOURCE-LEVEL VERIFICATION — ORCA DISPATCH + DSH LIFECYCLE — 2026-09-18

**Result:** ORCA DISPATCH SURFACE = VERIFIED; DSH LIFECYCLE API = VERIFIED; ACES↔Orca↔DSH executable integration = NOT PROVEN.

### Orca

Official public source: `stablyai/orca`, orchestration guide. Verified Run/Task/Dispatch model, `worker-start`, lower-level `dispatch`, `dispatch-show`, typed Task states, worker receipts, settlement via `worker_done`, recovery controls, and a Task-level circuit breaker after three consecutive failures. Orca does not expose the ACES-specific authority envelope as one native typed admission object.

### DSH

Official source: `deepseek-ai/deepseek-harness`. Verified `Agent.cancel(cause, options?)`, `Agent.whenIdle()`, durable turn/step/session lifecycle, cancellation/abort terminal outcomes, and serial `agent/turn-stopping` lifecycle seam. DSH explicitly has **no built-in turn budget**; bounded runaway-turn policy must be supplied through a lifecycle extension.

### Contract mapping verdict

- `ExecutionID`: PARTIAL — map to Orca Run/Task/Dispatch identities.
- `CurrentStateRef`: NOT NATIVE / adapter required.
- `AtomicNode`: NOT NATIVE / adapter required.
- `AuthorizationRef`: NOT NATIVE / adapter required.
- `BoundsRef`: NOT NATIVE / adapter required.
- `StopConditionsRef`: supported as DSH lifecycle adapter seam, not native ACES policy.
- `AcceptanceCriteriaRef`: NOT NATIVE / adapter required.
- `CapabilityScope`: PARTIAL across Orca placement/agent controls and DSH agent-scoped context.
- `ProvenanceContext`: PARTIAL — native identities/events exist, ACES cross-layer correlation not proven.
- `ContractVersion`: NOT NATIVE / adapter required.

**Critical finding:** the minimal contract is source-compatible but not source-native. The remaining blocker is now specifically the ACES adapter/correlation contract plus executable proof of authority propagation, bounded stop enforcement, end-to-end trace correlation, and failure-closed admission.

**Verification verdict:**
- ORCA DISPATCH SURFACE = **VERIFIED**
- DSH LIFECYCLE API = **VERIFIED**
- MINIMAL CONTRACT = **COMPATIBLE WITH BOTH SUBSTRATES**
- NATIVE ACES AUTHORITY CONTRACT = **NOT PROVEN**
- END-TO-END EXECUTIONID CORRELATION = **NOT PROVEN**
- FORCED-STOP VERTICAL TEST = **NOT EXECUTED**
- FAILURE-CLOSED ACES ADMISSION TEST = **NOT EXECUTED**
- INDEPENDENT INTEGRATION VERIFICATION = **NOT EXECUTED**
- CONTRACT ACCEPTANCE = **BLOCKED / NOT YET VERIFIED**
- RUNTIME IMPLEMENTATION = **NOT AUTHORIZED**

**Next atomic control action:** `DEFINE + VERIFY ACES↔ORCA ADAPTER/CORRELATION CONTRACT — EXECUTIONID / AUTHORIZATIONREF / BOUNDSREF / STOPCONDITIONSREF / ACCEPTANCECRITERIAREF`

Scope remains contract mapping/evidence definition only. No runtime implementation, numeric configuration selection, R1.5 mutation, or R1.6 execution.


## AOC-001 — ACES ↔ ORCA ADAPTER / CORRELATION CONTRACT

**Notion artifact:** https://app.notion.com/p/3df0e90e16c6814b8f1efeedc8599406?pvs=204

**Status:** CONTRACT DEFINITION COMPLETE / SOURCE COMPATIBILITY VERIFIED / ACCEPTANCE BLOCKED / RUNTIME NOT AUTHORIZED

Canonical correlation chain:

ExecutionID → Orca RunID → TaskID → DispatchID → AgentRunID → DSH SessionID → Turn/Step/Tool Evidence

Mandatory ACES envelope: ExecutionID, CurrentStateRef, AtomicNode, AuthorizationRef, BoundsRef, StopConditionsRef, AcceptanceCriteriaRef, CapabilityScope, ProvenanceContext, ContractVersion.

Source verification: Orca Run/Task/Dispatch, worker-start/dispatch, typed Task states, worker settlement/receipts, and three-failure Task circuit breaker are evidenced. DSH cancellation, quiescence, durable lifecycle evidence, and agent/turn-stopping are evidenced. Neither substrate natively supplies the ACES authority envelope.

**Verdict:** AOC-001 DEFINITION = COMPLETE; SOURCE COMPATIBILITY = VERIFIED; END-TO-END CORRELATION = NOT PROVEN; FAILURE-CLOSED ADAPTER TEST = NOT PROVEN; FORCED-STOP INTEGRATION TEST = NOT PROVEN; CONTRACT ACCEPTANCE = BLOCKED; RUNTIME IMPLEMENTATION = NOT AUTHORIZED.

**Next atomic action:** AUTHORIZE AOC-001 VERTICAL ADAPTER TEST FIXTURE

## Git ↔ Notion Reconciliation

Git contains this index and the `PROJECT_INDEX.md` route. The substantive contract remains in Notion.

This Git artifact is an index, not a second source of truth.

## Current State

- Ralph Loop Governance: **ACTIVE IN NOTION / GIT INDEXED**
- Iteration Closure Gate: **ACTIVE IN NOTION / GIT INDEXED**
- P7 recurrence-prevention responsibility: **IDENTIFIED / EVIDENCE-BOUND**
- HARNESS-CAPABILITY-RECONSTRUCTION-002: **CONTRACT DEFINED / NOT ACCEPTED**
- ACES runtime P7/Ralph enforcement: **NOT PROVEN**
- ACES↔Orca↔DSH executable integration: **NOT PROVEN**
- DSH execution kernel: **EXTERNAL / SOURCE-LEVEL EVIDENCE EXISTS**
- DSH as Ralph/P7 enforcement: **NOT PROVEN**
- R1.5: **BLOCKED**
- R1.6: **NOT AUTHORIZED**
- Production Notion projection: **NOT EXECUTED**

## Non-Claims

This index does not claim runtime implementation, AcceptedState, R1.5 unblocking, R1.6 authorization, or production projection.

## Verification Target

`Git index → authoritative Notion Ralph mandate → Closure Gate → P7 → enforcement contract → actual implementation evidence → verification`

An independent reader must be able to follow this chain without conversation-memory reconstruction.

## Authoritative Notion Sources

- RALPH LOOP — ACES Governance Mandate v1.0:
  https://app.notion.com/p/3de0e90e16c681558685d90c1ba4e5f3?pvs=204
- ACES EXECUTION CONTROL PLAN:
  https://app.notion.com/p/3da0e90e16c68179ba7be96f8e6cfdb7?pvs=204
- PROTOCOL-ITERATION-CLOSURE-001:
  https://app.notion.com/p/3da0e90e16c6814a872afc7b13fc3236?pvs=204
- P1 / STIL:
  https://app.notion.com/p/3da0e90e16c681e38c2ff3e2877ae488?pvs=204

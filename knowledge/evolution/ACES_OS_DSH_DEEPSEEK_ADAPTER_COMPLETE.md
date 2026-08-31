# ACES OS — DSH DeepSeek Adapter
## Complete Architectural Result

**Status:** COMPLETE — architectural adapter contract  
**Target:** DeepSeek Harness (`dsh`)  
**Role:** ACES Execution Runtime Adapter  
**Boundary:** Execution inside an ACES Reality Evolution Cycle

---

## 1. Purpose

The ACES DSH DeepSeek Adapter integrates DeepSeek Harness as an execution runtime inside an ACES Cycle.

The adapter MUST NOT make DeepSeek Harness the authority of ACES.

The adapter MUST NOT make the DSH event log the canonical source of ACES state.

The adapter MUST NOT transfer decision authority, epistemic authority, or state authority to DSH.

The adapter provides:

```text
ACES Decision
      ↓
AUTHORIZED EXECUTION REQUEST
      ↓
DSH EXECUTION RUNTIME
      ↓
EXECUTION TRACE
      ↓
ACES EVIDENCE
      ↓
ACES VERIFICATION
      ↓
VERIFIED STATE(t+1)
```

**DSH = Execution Runtime.**  
**ACES = Reality Evolution / Cycle Management System.**

---

## 2. Fundamental Boundary

DeepSeek Harness answers:

> What happened during this execution trajectory?

ACES answers:

> What state were we in, why was this transition authorized, what actually changed, what was verified, and what must the next cycle inherit?

Therefore:

```text
DSH
└── Agent Execution Cycle

ACES
└── Reality Evolution Cycle
```

The DSH execution cycle is nested inside the ACES Cycle.

```text
ACES CYCLE
│
├── Evidence
├── Context
├── Decision
├── Authority
│
├── EXECUTION
│   └── DSH Adapter
│       ├── Harness
│       ├── Agent Loop
│       ├── Tools
│       ├── Sandbox
│       ├── Subagents
│       ├── Code Mode
│       └── Event Trace
│
├── Verification
└── Verified State(t+1)
```

---

## 3. Canonical ACES Cycle

The adapter MUST implement the semantic lifecycle:

```text
Verified State(t)
      ↓
Evidence
      ↓
Context
      ↓
Decision
      ↓
Authority
      ↓
Execution
      ↓
Verification
      ↓
Verified State(t+1)
      ↓
Memory / Learning
      ↓
Cycle(t+1)
```

The adapter owns only the Execution segment.

It MUST NOT redefine the semantics of Evidence, Context, Decision, Authority, Verification, Canonical State, Memory, or Learning.

---

## 4. Core Invariants

### CCI-001 — Cycle Continuity

```text
StartState(Cycle N+1)
=
VerifiedEndState(Cycle N)
```

If the adapter cannot establish the parent ACES cycle/state, execution is **BLOCKED**, unless ACES policy explicitly defines a new root cycle.

### DSH-001 — Execution Provenance

Every DSH execution MUST be attributable to:

```text
aces_cycle_id
aces_state_id
 decision_id
authority_id
execution_id
```

The DSH session identifier is an execution identifier, not an ACES state identifier.

---

## 5. DSH Session ≠ ACES Cycle

```text
DSH Session = execution trajectory
ACES Cycle  = verified reality transition
```

One ACES Cycle MAY contain multiple DSH sessions, retries, forks, subagent executions, recovery executions, or verification-related executions, provided they remain within the same ACES transition boundary.

One DSH session MUST NOT automatically imply one ACES Cycle.

---

## 6. DSH Event Log

The DSH event stream is treated by ACES as **execution history**, not canonical reality state.

```text
DSH Event Log
      ↓
Execution Evidence
      ↓
ACES Evidence
      ↓
Verification
      ↓
Canonical State
```

Raw DSH events MUST NOT be promoted directly into canonical ACES state.

---

## 7. Evidence Adapter

Relevant DSH records SHOULD be normalized into ACES Evidence, including where applicable:

```text
ToolInvocation
ToolResult
FileMutation
CommandExecution
ProcessResult
SubagentExecution
ModelOutput
ContextInjection
ExecutionError
ExecutionCompletion
RuntimeEvent
```

Each evidence object MUST preserve provenance to its originating DSH execution record where technically available.

---

## 8. Raw Trace Preservation

The adapter MUST preserve access to the raw execution trajectory.

Minimum conceptual provenance:

```text
execution_id
session_id
event_id
event_sequence
event_type
timestamp
source
payload_reference
```

Preferred model:

```text
DSH Trace
    │
    ├── immutable/raw execution record
    │
    └── ACES Evidence references
```

This preserves both reconstructability and ACES semantic normalization.

---

## 9. Authority Boundary

DSH is **not an authority source**.

Authorization MUST precede execution:

```text
Decision
   ↓
ACES Authorization
   ↓
Authorized Execution Envelope
   ↓
DSH
```

Successful DSH execution MUST NOT be interpreted as proof that the action was authorized.

---

## 10. Execution Envelope

Every DSH execution initiated by ACES SHOULD receive an explicit execution envelope:

```text
ExecutionEnvelope
├── execution_id
├── cycle_id
├── parent_state_id
├── decision_id
├── authority_id
├── principal
├── capabilities
├── resources
├── operations
├── scope
├── constraints
├── expiry
├── verification_requirements
└── provenance
```

DSH receives only capabilities required for the authorized execution.

---

## 11. Capability Translation

ACES capabilities MUST be projected into DSH runtime capabilities.

The adapter MUST NOT grant broader DSH capabilities than those authorized by ACES.

Capability expansion is prohibited.

---

## 12. Fail-Closed Behavior

The adapter MUST fail closed on:

```text
unknown cycle
unknown parent state
unknown decision
missing authority
invalid capability
expired capability
revoked capability
missing execution policy
unavailable authorization
unavailable provenance
unavailable required audit
ambiguous execution scope
```

Result:

```text
EXECUTION BLOCKED
```

The adapter MUST NOT silently downgrade to unrestricted DSH execution.

---

## 13. DSH Plugin Model

DSH is treated as a composable runtime whose plugin/configuration surface should remain behind the adapter boundary.

Preferred:

```text
ACES Adapter
      ↓
DSH Compatibility Layer
      ↓
DSH Runtime
```

The ACES core MUST remain DSH-agnostic.

---

## 14. Runtime Modes

DSH runtime modes are execution configurations, not ACES semantic modes.

Conceptual mapping:

```text
ACES Execution Policy
        ↓
DSH Runtime Profile
```

The adapter may select the appropriate DSH profile for the authorized task. Experimental/development profiles MUST NOT be silently promoted to production authority.

---

## 15. Code Mode

Generated code is execution activity, not trusted authority.

```text
Generated Code
    ↓
Capability Evaluation
    ↓
Execution Policy
    ↓
Sandbox
    ↓
Trace
    ↓
Verification
```

Code Mode MUST inherit the same authorization boundary as direct tool calls.

---

## 16. Subagents

Subagents MUST NOT automatically inherit unlimited authority from a parent execution.

```text
Parent Execution
      ↓
Subagent Request
      ↓
Capability Derivation
      ↓
Scoped Authority
      ↓
Subagent Execution
```

Subagent capabilities SHOULD be scoped, traceable, time-bounded, revocable, and provenance-linked.

---

## 17. Sandbox

Sandbox security and ACES authorization are separate controls.

A sandbox MUST NOT be interpreted as evidence that an action was authorized.

---

## 18. Execution Result

The adapter MUST produce a normalized ACES ExecutionResult:

```text
ExecutionResult
├── execution_id
├── cycle_id
├── status
├── started_at
├── completed_at
├── trace_reference
├── evidence_references
├── mutations
├── outputs
├── errors
├── capability_usage
├── child_executions
└── provenance
```

Possible statuses:

```text
COMPLETED
FAILED
BLOCKED
CANCELLED
TIMED_OUT
PARTIAL
UNKNOWN
```

`UNKNOWN` MUST NOT be interpreted as success.

---

## 19. Execution ≠ Verification

```text
DSH
 ↓
Execution completed
 ↓
Evidence
 ↓
ACES Verification
 ↓
PASS / FAIL
```

`ExecutionResult = COMPLETED` MUST NOT imply `Verification = PASS`.

---

## 20. State Transition

The DSH adapter MUST NOT create canonical `State(t+1)`.

It may produce execution results, evidence, and mutation records.

ACES Verification determines whether these establish:

```text
Verified State(t+1)
```

Correct flow:

```text
DSH
    ↓
Observed execution effects
    ↓
ACES Verification
    ↓
Canonical State(t+1)
```

---

## 21. Memory Boundary

```text
DSH Session Storage
       ≠
ACES Memory
```

DSH session persistence is execution persistence. ACES Memory is cycle-continuity persistence.

The adapter MUST export the information required for ACES continuity, including execution provenance, evidence, outputs, mutations, referenced decisions, authority, and verification references.

---

## 22. G-TRACE / Global Structure Boundary

The DSH adapter MUST NOT own the ACES Global Structure Layer.

```text
DSH Trace
   ↓
ACES Evidence
   ↓
Canonical Cycle History
   ↓
Trajectory Analysis
   ↓
Global Structural Invariants
```

A structural invariant MUST NOT replace canonical history.

```text
Global Structure ≠ Canonical History
Predictive Invariant ≠ Reconstructive Record
```

G-TRACE remains an architectural research hypothesis until validated against ACES trajectory data.

---

## 23. Trajectory Continuity

The adapter MUST preserve:

```text
Cycle N
   ↓
Authorized DSH Execution
   ↓
Trace
   ↓
Evidence
   ↓
Verification
   ↓
Verified State N+1
   ↓
Cycle N+1
```

The next execution SHOULD receive context derived from the authoritative verified ACES state, not merely from a previous DSH conversation.

---

## 24. Context Reconstruction

DSH session continuation MAY be used as an execution optimization.

It MUST NOT be the authoritative mechanism for ACES context continuity.

Preferred:

```text
ACES Verified State
      ↓
ACES Context
      ↓
DSH Runtime Context
```

---

## 25. Fork Semantics

A DSH execution fork is not automatically a canonical reality fork.

```text
ACES State S
      │
      ├── Execution A
      │
      └── Execution B
```

Only an authorized and verified result may produce a canonical transition such as `S → S_A` or `S → S_B`.

---

## 26. Replay

```text
DSH Replay
=
reconstruct execution trajectory
```

while:

```text
ACES Replay
=
reconstruct + verify the corresponding reality transition
```

Replay MUST NOT mutate canonical reality merely because execution can be reproduced.

---

## 27. Recovery

On DSH execution failure:

```text
Execution Failure
      ↓
ACES Recovery Policy
```

Possible policy outcomes include RETRY, REPLAN, ROLLBACK, ABORT, HUMAN REVIEW, or NEW CYCLE.

The adapter MUST NOT independently decide which recovery action changes canonical state.

---

## 28. Human Gates

Where ACES policy requires human authority:

```text
Decision
 ↓
Human Approval
 ↓
Authority
 ↓
DSH Execution
```

The adapter MUST support suspension/resumption where technically available.

---

## 29. Observability

Minimum adapter telemetry SHOULD include:

```text
execution_started
execution_completed
execution_failed
tool_called
tool_completed
tool_failed
subagent_started
subagent_completed
capability_requested
capability_denied
sandbox_started
sandbox_terminated
trace_persisted
evidence_exported
```

Telemetry MUST NOT become the canonical ACES evidence store by itself.

---

## 30. Provenance

Every normalized adapter artifact SHOULD maintain:

```text
source_system = DSH
source_session_id
source_event_id
source_sequence
source_timestamp
adapter_version
cycle_id
execution_id
```

---

## 31. Versioning

Because DSH is a changing external runtime, the adapter MUST version its integration independently.

Minimum metadata:

```text
adapter_version
dsh_version
schema_version
trace_mapping_version
capability_mapping_version
```

The ACES core MUST NOT depend on unstable DSH internal APIs.

---

## 32. Replaceability Invariant

### DSH-001-R — Runtime Replaceability

ACES MUST remain semantically functional if DSH is replaced by another execution runtime implementing the same ACES Execution Adapter Contract.

```text
ACES
 │
 ├── DSH Adapter
 ├── Runtime B Adapter
 ├── Runtime C Adapter
 └── Local Runtime Adapter
```

The canonical ACES state model MUST remain unchanged.

---

## 33. Authority and State Invariants

### DSH-002-R — No DSH Authority

DSH MUST NOT become Decision Authority, Policy Authority, State Authority, Verification Authority, or Memory Authority.

### DSH-003-R — No Event-Log Authority

The DSH event stream MUST NOT become the sole source of truth for ACES canonical state.

### DSH-004-R — No Silent Context Inheritance

A new ACES Cycle MUST NOT inherit state merely because a DSH session was resumed.

### DSH-005-R — No Silent Capability Escalation

A DSH plugin, tool, subagent, Code Mode program, or sandbox process MUST NOT acquire capabilities exceeding the ACES execution envelope.

### DSH-006-R — No Silent State Commit

A DSH execution MUST NOT directly commit canonical ACES state.

Required path:

```text
Execution
 ↓
Evidence
 ↓
Verification
 ↓
State Commit
```

---

## 34. Complete Data Flow

```text
                    ACES
                     │
                     ▼
             Verified State(t)
                     │
                     ▼
                  Context
                     │
                  Decision
                     │
                 Authority
                     │
                     ▼
            Execution Envelope
                     │
                     ▼
              DSH ADAPTER
                     │
          ┌──────────┼──────────┐
          ▼          ▼          ▼
       Harness     Tools     Subagents
          │          │          │
          └──────────┼──────────┘
                     ▼
               DSH Trace
                     │
                     ▼
            Execution Result
                     │
                     ▼
             ACES Evidence
                     │
                     ▼
               Verification
                     │
             ┌───────┴───────┐
             │               │
            FAIL            PASS
             │               │
             ▼               ▼
          Recovery       State(t+1)
                             │
                 ┌───────────┴───────────┐
                 ▼                       ▼
              Memory              Global Structure
                 │                       │
                 └───────────┬───────────┘
                             ▼
                         Cycle(t+1)
```

---

## 35. Canonical Object Mapping

```text
ACES Cycle
    ↓
DSH Session / execution group

ACES Decision
    ↓
DSH execution instruction

ACES Authority
    ↓
DSH capability envelope

ACES Execution
    ↓
DSH trajectory

ACES Evidence
    ↓
normalized DSH events/results

ACES Verification
    ↓
external ACES verifier

ACES State
    ↓
external ACES canonical state

ACES Memory
    ↓
external continuity store
```

These are projections/references, not semantic equivalences.

---

## 36. What ACES Takes from DSH

ACES SHOULD adopt the following architectural lessons:

1. Runtime capabilities can be composable.
2. Runtime capabilities should be replaceable.
3. Execution should be deeply traceable.
4. Execution history should be replayable.
5. Runtime configuration should be declarative where possible.
6. Agent capabilities should be modular.
7. The execution environment should be inspectable.
8. Different execution profiles should be composable.

---

## 37. What ACES Must Not Inherit from DSH

ACES MUST NOT inherit the assumptions that:

```text
agent session = system state
execution trace = canonical history
model trajectory = decision authority
successful execution = verified reality transition
runtime capability = authorization
```

These are precisely the boundaries that ACES adds.

---

## 38. Final Adapter Position

> **DeepSeek Harness is a reference execution substrate for ACES, not the ACES control plane.**

More precisely:

> **DSH provides a composable, traceable execution environment capable of realizing the Execution phase of an ACES Cycle. ACES retains authority over state, decision, authorization, verification, continuity, memory, and global trajectory interpretation.**

---

## 39. Relation to Cycle Continuity

The adapter is complete only when it supports:

```text
Cycle N
   ↓
Authorized DSH Execution
   ↓
Trace
   ↓
Evidence
   ↓
Verification
   ↓
Verified State N+1
   ↓
Cycle N+1
```

The causal link MUST remain explicit:

```text
Decision N
   ↓
Execution N
   ↓
Evidence N
   ↓
Verification N
   ↓
State N+1
```

---

## 40. Final ACES / DSH Model

```text
                         ACES OS
                            │
                            ▼
                    MANAGED REALITY
                            │
                            ▼
                    VERIFIED STATE(t)
                            │
             ┌──────────────┴──────────────┐
             │                             │
             ▼                             ▼
       CYCLE CONTINUITY             GLOBAL STRUCTURE
             │                             │
             │                       Invariants
             │                       Patterns
             │                       Predictions
             │                             │
             └──────────────┬──────────────┘
                            ▼
                         CONTEXT
                            │
                         DECISION
                            │
                        AUTHORITY
                            │
                            ▼
                    EXECUTION ENVELOPE
                            │
                            ▼
                     DSH ADAPTER
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
           Harness        Tools       Subagents
              │             │             │
              └─────────────┼─────────────┘
                            ▼
                       DSH TRACE
                            │
                            ▼
                      ACES EVIDENCE
                            │
                            ▼
                       VERIFICATION
                            │
                            ▼
                    VERIFIED STATE(t+1)
                            │
                 ┌──────────┴──────────┐
                 ▼                     ▼
              MEMORY              LEARNING
                 │                     │
                 └──────────┬──────────┘
                            ▼
                         CYCLE(t+1)
```

---

# Canonical Definition

### DSH DeepSeek Adapter

> **The ACES DSH DeepSeek Adapter is the execution-boundary adapter that embeds DeepSeek Harness as a replaceable, capability-scoped, traceable runtime inside an ACES Reality Evolution Cycle. It translates ACES-authorized execution decisions into DSH runtime operations and translates resulting execution trajectories into provenance-preserving ACES evidence. It does not own ACES state, decision authority, authorization, verification, memory, or global trajectory structure.**

### ACES

> **ACES manages the continuity and validity of verified transitions through which a managed reality evolves over time.**

### DSH

> **DSH manages the internal execution trajectory through which an authorized action is carried out.**

### Boundary

```text
DSH:
Agent Execution Cycle

ACES:
Reality Evolution Cycle
```

### Fundamental relation

```text
ACES authorizes
      ↓
DSH executes
      ↓
ACES verifies
      ↓
ACES commits state
      ↓
ACES continues the next cycle
```

### Fundamental invariant

```text
Cycle(N+1)
MUST inherit
VerifiedState(N)
```

### Final architectural conclusion

```text
DSH is not the OS.

DSH is the execution substrate.

ACES is the system that turns
execution trajectories into
verified, continuous evolution
of managed reality.
```

---

**Evolution artifact:** DSH DeepSeek Adapter COMPLETE  
**Branch:** `evolution/dsh-aces-cycle-adapter`  
**Base:** `feature/aces-evolution-control-system` @ `4371e73c3e25079a4f6014405cfec2c768a3717c`

# ACES OS — Cycle Management Principle

**Status:** Canonical evolution principle candidate  
**Scope:** ACES OS architecture and evolution  
**Primary realization domain:** BASTION

## 1. Fundamental Principle

> **Each new cycle is a continuation of the previous state.**

The fundamental unit of ACES OS is not a task, message, agent, model inference, or isolated execution. It is a **managed cycle of state transition** in a governed reality.

## 2. Cycle Invariant

> **NO NEW CYCLE WITHOUT VALID CONTINUITY FROM THE PREVIOUS STATE.**

Equivalent operational invariant:

> **Cycle N+1 MUST inherit the verified state produced by Cycle N.**

Therefore `State(t+1)` is not an independent snapshot. It is the result of a valid, traceable and verified transition from `State(t)`.

## 3. Canonical Cycle

```text
STATE(t)
  ↓
EVIDENCE
  ↓
CONTEXT
  ↓
DECISION
  ↓
AUTHORITY
  ↓
EXECUTION
  ↓
VERIFICATION
  ↓
STATE(t+1)
  ↓
MEMORY / LEARNING
  ↓
NEXT CYCLE
```

The next cycle consumes the verified output of the previous cycle as an authoritative input.

## 4. Long-Term Memory

ACES Long-Term Memory is not merely chat history or a token-saving cache.

Its fundamental role is **continuity between cycles**. It preserves the state, evidence, decisions, execution, verification, learning, and causal history required to reconstruct and continue the managed reality.

```text
MEMORY
  ↓
STATE(t)
  ↓
CYCLE(t)
  ↓
VERIFIED STATE(t+1)
  ↓
MEMORY UPDATE
  ↓
CYCLE(t+1)
```

## 5. State Transition Requirement

A legitimate ACES transition must preserve reconstructability of:

- previous state;
- decision-relevant evidence;
- context used by the decision;
- applicable policy and authority;
- execution trace;
- verification result;
- resulting state;
- learning derived from the transition.

Execution success alone does **not** constitute verified reality change.

```text
Execution Result ≠ Verified Reality State
```

## 6. DSH / Harness Boundary

DeepSeek Harness is treated as a reference architecture for **managed agent execution within a cycle**:

- agent runtime;
- capability seams;
- provider abstraction;
- execution lifecycle;
- tool orchestration;
- sandboxing;
- event trace;
- replay and reconstruction.

ACES extends this to the higher-level problem of **continuity and validity across cycles of reality evolution**.

```text
DSH / Harness
    = Agent Execution Cycle

ACES OS
    = Reality Evolution Cycle Management
```

## 7. BASTION as Primary Living System

BASTION is the primary realization and proof environment for this principle.

ACES must demonstrate that it can continuously advance BASTION through successive verified states without losing the historical context, evidence, decisions, authority, execution history, or learned constraints of prior cycles.

External business auditing is a secondary reuse of the same cycle-management capability.

## 8. Strategic Definition

> **ACES OS is a system for managing the continuity, validity, and verification of state transitions across cycles of a governed reality.**

This principle is foundational to future ACES work on Memory, Evidence, Context, Decision, Execution, Verification, Learning, Model Routing, Harness integration, and Evolution Governance.

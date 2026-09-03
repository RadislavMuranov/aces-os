# ACES OS — Minimum Implementation Contract

## Status

**Status:** ACTIVE — IMPLEMENTATION GATE
**Date:** 2026-09-03
**Branch:** `architecture/priority-realization-roadmap-v2`
**Priority:** P0 — next realization stage

## 1. Trigger

The current ACES research and architecture are sufficiently defined to begin implementation of a first verifiable working cycle.

The immediate objective is no longer to expand the architecture. The immediate objective is to implement and verify the smallest ACES system that demonstrates the canonical controlled transition from human intent to accepted digital state.

## 2. Fundamental Implementation Question

> **Какой минимальный ACES OS мы уже достаточно понимаем, чтобы наконец реализовать его и получить первый проверяемый работающий цикл?**

This question is the entry criterion for the implementation stage.

## 3. Minimum ACES

The minimum implementation SHALL contain only the following capabilities required to complete one governed, observable and verifiable cycle:

1. **Intent** — receive a structured human intent.
2. **Context** — resolve the minimum context required by that intent.
3. **Authority / Policy** — determine whether the action is permitted, its scope, constraints and required verification.
4. **Connector Resolution** — select an available integration path using the established CLA-first principle.
5. **Execution Integration** — delegate execution to the established execution plane (`Orca → DSH → Agent/Model`) where required.
6. **Observation** — capture the resulting external state/outputs.
7. **Evidence** — preserve machine-readable evidence of intent, authorization, action, observation and result.
8. **Verification** — independently determine whether the requested state was actually achieved.
9. **Acceptance** — accept or reject the resulting state; unverified results MUST NOT become canonical.
10. **Accepted State** — persist the verified state transition as the ACES source of truth for the implemented slice.

## 4. Canonical Minimum Cycle

```text
Human Intent
    ↓
Intent IR
    ↓
Context
    ↓
Authority / Policy
    ↓
Connector Resolution
    ↓
Execution
    ↓
Digital World
    ↓
Observation
    ↓
Evidence
    ↓
Verification
    ↓
Acceptance
    ↓
Accepted State
```

This is the first implementation target.

## 5. Explicit Non-Goals for the First Cycle

The first cycle SHALL NOT require:

- a universal agent;
- a new ACES model;
- a new ACES harness;
- replacement of Orca or DSH;
- a universal connector catalog;
- full DWOM coverage;
- complete semantic compression;
- full Reality Layer UI;
- large-scale multi-connector support;
- BASTION integration;
- speculative protocol abstractions;
- production-scale distributed deployment.

These are deferred until the first cycle produces evidence that the minimum boundary works.

## 6. Required Architectural Boundaries

The implementation SHALL preserve:

`Authority ≠ Connector ≠ Protocol ≠ Capability ≠ Execution`

and:

`Capability ≠ Permission ≠ Approval ≠ Verification ≠ Acceptance ≠ Canonicality`

No connector, protocol, agent, harness or model may establish canonical ACES reality by itself.

## 7. Execution Ownership

ACES owns:

- intent;
- context required for the cycle;
- authorization/policy decision;
- connector selection;
- evidence;
- verification;
- acceptance;
- accepted state.

Execution remains delegated to the existing execution architecture:

`ACES Control/Governance/Epistemic Authority → Orca → DSH → Agent/Model`

The first implementation SHALL not create a competing execution architecture.

## 8. Connector Rule

Connector selection SHALL follow:

`LOCAL → NATIVE / FIRST-PARTY → DIRECT CONNECTOR → MCP → OTHER PROTOCOL / BRIDGE`

This is CLA-first, not CLA-only.

MCP is transport/capability interoperability, never ACES Authority.

## 9. Evidence Minimum

For every completed cycle, the implementation SHALL be able to produce a trace containing at minimum:

- intent identifier;
- normalized intent;
- context used;
- authority/policy decision;
- selected connector/capability;
- requested action;
- execution result/receipt;
- observation;
- evidence identifiers/provenance;
- verification result;
- acceptance decision;
- accepted state or explicit failure state.

## 10. Fail-Closed Outcomes

The minimum implementation SHALL explicitly support at least:

`ACCEPTED | REJECTED | UNVERIFIED | CONFLICT | UNKNOWN | ESCALATE`

A tool-reported success without verified desired state SHALL NOT be accepted as canonical success.

## 11. First Working Cycle Definition

A cycle is considered working only if all conditions hold:

1. A human intent enters ACES.
2. ACES resolves sufficient context.
3. ACES makes an explicit authority/policy decision.
4. ACES selects a governed connector path.
5. Execution occurs through the established execution plane.
6. External effects/outputs are observed.
7. Evidence is persisted with provenance.
8. Verification is performed against the requested outcome.
9. Acceptance is explicit.
10. The accepted state is persisted.
11. The entire transition is reproducible/auditable from the recorded evidence.
12. Failure or uncertainty prevents false canonicalization.

## 12. Implementation Gate

**GATE I-001 — Minimum ACES Working Cycle**

### PASS

A complete end-to-end cycle satisfies the definition above and is demonstrated by executable tests plus persisted evidence.

### FAIL

Any required boundary is missing, implicit, unverifiable, bypassable, or dependent on unrecorded human intervention.

## 13. Roadmap Alignment

This contract operationalizes the existing roadmap without adding a new research branch.

Primary roadmap targets:

- R5 — ACES Boundary
- R6 — Digital World Model, minimum required subset only
- R7 — Connector Fabric
- R9 — Authority / Policy
- R10 — Execution Plane Integration
- R11 — Reconciliation Engine, minimum required subset only
- R12 — Evidence / Verification / Accepted State
- R16 — Vertical Slice
- R17 — Failure / Adversarial Experiments

R13–R15 are not prerequisites for the first minimal working cycle except where a concrete dependency is required.

## 14. Implementation Sequence

### I-0 — Contract Freeze
Freeze this minimum boundary. No new architectural layer is added unless required by a failing verification criterion.

### I-1 — Runtime Skeleton
Implement the smallest executable control flow for the canonical cycle.

### I-2 — Intent / Context
Implement minimal structured Intent IR and deterministic context input for one scenario.

### I-3 — Authority / Policy
Implement explicit authorization, scope and fail-closed decisions.

### I-4 — Connector / Execution
Implement one governed connector path and integrate with the existing execution plane.

### I-5 — Observation / Evidence
Persist execution receipt, observation and provenance.

### I-6 — Verification / Acceptance
Implement outcome verification and explicit accepted/rejected/unverified state.

### I-7 — Vertical Slice
Run one complete real end-to-end cycle.

### I-8 — Adversarial Verification
Break the cycle deliberately: wrong context, stale state, insufficient authority, partial execution, duplicate action, tool-reported success with failed desired state, and external state change.

### I-9 — Gate I-001
Freeze the evidence package and determine PASS/FAIL.

## 15. Definition of Done

The implementation stage may advance only when the repository contains:

- executable implementation of the minimum cycle;
- automated tests for success and failure paths;
- persisted evidence for a completed cycle;
- verification evidence proving accepted state;
- explicit failure-state evidence;
- architecture-boundary tests preventing authority bypass;
- a reproducible verification procedure;
- a recorded I-001 PASS.

## 16. Protected Boundary: BASTION

BASTION remains an external protected project target.

No BASTION-side mutation, experimentation, architectural/code/specification transfer or operational validation is authorized during this implementation stage.

The first ACES cycle MUST be implemented and verified without touching BASTION.

Future BASTION project-control validation remains gated by full ACES implementation/verification and explicit authorization.

## 17. Freeze Rule

> **No new architecture until the minimum ACES working cycle has been implemented and verified, unless a failing implementation/verification result demonstrates that the missing architectural capability is necessary.**

This rule converts the current phase from open-ended architectural evolution to evidence-driven realization.

## 18. Stage Result

**Current stage:** IMPLEMENTATION

**Current target:** first verified ACES working cycle

**Primary KPI:** end-to-end verified state transition with complete evidence and no unrecorded human middleware step

**Gate:** I-001 — Minimum ACES Working Cycle

**Next permitted evolution:** only after I-001 PASS, based on observed implementation failures or measured requirements.

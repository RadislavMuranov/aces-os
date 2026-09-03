# HDE-002 — Step 7: ACES Boundary Specification

**Status:** STEP 7 COMPLETE — ACES BOUNDARY SPEC  
**Experiment:** HDE-002  
**Date:** 2026-09-03  
**Branch:** `architecture/priority-realization-roadmap-v2`

## 1. Purpose

Define the minimum defensible architectural boundary of ACES after Steps 0–6.

The boundary must distinguish what ACES owns from what may be delegated to external Model, Agent, Harness, Tool, Execution and Verification systems.

## 2. Boundary principle

> ACES does not need to own intelligence or execution. ACES must own the governed transition by which external execution becomes accepted canonical ACES state.

## 3. External execution domain

The following may be external and replaceable:

`MODEL → AGENT → HARNESS → TOOLS → EXECUTION`

External systems may also provide local context, memory, sandboxing and verification.

Their capability, autonomy, permission or completion signal does not transfer ACES authority.

## 4. ACES-owned authority domain

ACES owns, or must be able to independently enforce, at minimum:

1. **Epistemic Authority** — criteria and authority for accepting propositions/state as knowledge within ACES.
2. **Decision Authority** — authority to bind a proposed course of action to an ACES-governed decision.
3. **Execution Authority** — authority to permit consequential side effects at the ACES boundary.
4. **Evidence / Provenance** — evidence lineage sufficient to reconstruct why an accepted state was accepted.
5. **Independent Verification** — verification that is not reducible to an agent's self-reported completion.
6. **Acceptance** — explicit transition from verified result to accepted ACES state.
7. **Canonical State** — ACES-owned representation of accepted reality.
8. **Policy / Governance** — rules determining when the above transitions are allowed.

## 5. Canonical transition

The minimum governed transition is:

`INTENT → PROPOSAL → AUTHORIZATION → EXECUTION → OBSERVATION → EVIDENCE → VERIFICATION → ACCEPTANCE → CANONICAL STATE`

Each transition is semantically distinct.

## 6. Non-equivalences

`CAPABILITY ≠ PERMISSION`

`PERMISSION ≠ APPROVAL`

`APPROVAL ≠ EXECUTION`

`EXECUTION ≠ VERIFICATION`

`VERIFICATION ≠ ACCEPTANCE`

`ACCEPTANCE ≠ CANONICALITY`

Therefore no external runtime event, completion signal, approval, test result or memory write may independently establish canonical ACES reality.

## 7. Trust boundary

The minimum trust boundary is:

`EXTERNAL AGENT/HARNESS/TOOLS/EXECUTION/VERIFICATION → ACES ACCEPTANCE BOUNDARY`

External systems are untrusted with respect to ACES canonicality unless their specific authority is explicitly delegated and their result satisfies ACES policy/evidence requirements.

This is consistent with the established ACES invariant:

`external capability ≠ ACES authority`

## 8. What ACES must NOT assume

ACES must not assume that:

- model confidence implies truth;
- agent completion implies correctness;
- tool success implies desired state;
- approval implies correctness;
- runtime permission implies ACES authority;
- external memory is canonical knowledge;
- external verification is sufficient for canonicalization;
- an event log is itself the source of truth.

## 9. Minimal ACES interface to an external runtime

The boundary should expose a governed contract approximately equivalent to:

### Input to runtime

- authorized intent/task;
- scoped capabilities;
- policy constraints;
- execution budget;
- required evidence/verification criteria;
- authority/delegation context.

### Runtime output

- proposed actions;
- execution receipts/results;
- observable effects;
- evidence/provenance;
- verification artifacts;
- failures/uncertainties;
- identity and delegation context.

### ACES decision

ACES independently determines:

`REJECT | ACCEPT-TRANSIENT | ACCEPT-CANONICAL | ESCALATE`

The exact state machine is a later implementation/specification concern; the architectural distinction is mandatory.

## 10. Canonicalization rule

> A verified external result becomes canonical ACES reality only through an explicit ACES acceptance transition satisfying declared authority, policy, evidence and verification requirements.

This does not claim that ACES determines objective truth. It defines ACES's authority over its own operational/canonical state.

## 11. Failure semantics

The boundary is fail-closed for missing authority/evidence/verification.

Examples:

- missing authorization → no consequential execution;
- missing required evidence → no canonicalization;
- failed verification → no canonicalization;
- conflicting authoritative evidence → escalation/uncertain state;
- ambiguous delegation → deny or escalate;
- external runtime reports completion without sufficient proof → non-canonical result;
- canonical state cannot be updated consistently → preserve prior canonical state and record failure.

## 12. MCP / connector rule

The ACES boundary does not require MCP as a universal mechanism.

Existing ACES rule remains binding:

> Use MCP only when a Connector / Local / Native alternative (CLA) cannot satisfy the requirement.

MCP is therefore a capability transport option, not an authority mechanism.

## 13. Minimal ownership model

```text
                    ACES AUTHORITY–EVIDENCE–REALITY PLANE

        ┌────────────────────────────────────────────────────┐
        │ Epistemic Authority                                │
        │ Decision Authority                                 │
        │ Execution Authority                                │
        │ Policy / Governance                                │
        │ Evidence / Provenance                              │
        │ Independent Verification                           │
        │ Acceptance                                         │
        │ Canonical State / Reality                          │
        └───────────────────────┬────────────────────────────┘
                                │
                         TRUST / ACCEPTANCE
                              BOUNDARY
                                │
              MODEL → AGENT → HARNESS → TOOLS → EXECUTION
                                                    │
                                                 EFFECT
                                                    │
                                               OBSERVATION
                                                    │
                                              VERIFICATION
```

## 14. Architectural consequence

ACES should remain model-, vendor-, harness- and connector-independent at the authority boundary.

DSH may serve as an Execution Kernel. Orca may serve as fleet/execution orchestration. ZCode, Claude Code, Codex, OpenCode or other runtimes may serve as external execution substrates.

None receives ACES canonical authority merely by integration.

## 15. Step 7 gate

**PASS CONDITION:** a minimal, implementation-neutral ACES boundary is defined such that external execution can be delegated while authority over acceptance and canonical state remains explicit, independently verifiable and fail-closed.

**RESULT: PASS.**

## 16. Step 7 conclusion

The minimum defensible ACES architectural boundary is not another agent runtime.

It is the **Authority–Evidence–Reality boundary** that governs the transition:

`EXTERNAL EFFECT → EVIDENCE → VERIFICATION → ACES ACCEPTANCE → CANONICAL REALITY`

This is the boundary to carry into HDE-002 Step 8 — FINAL VERDICT.

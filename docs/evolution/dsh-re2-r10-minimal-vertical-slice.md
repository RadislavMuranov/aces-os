# DSH-RE2 — R10 Minimal ACES-on-DSH Vertical Slice

Status: COMPLETE — DESIGN/INTEGRATION CONTRACT PASS; LIVE EXECUTION NOT CLAIMED
Baseline: deepseek-ai/deepseek-harness @ dd6322d604e00eec1ba5e0c8541159906a21094a
Date: 2026-09-01

## Objective

Prove the smallest integration boundary in which ACES remains the authority/epistemic layer and DSH provides execution only.

## Minimal slice

```text
ACES Intent
  -> ACES Policy/Authorization
  -> ACES Decision
  -> Context Compiler
  -> DSH Runtime
  -> Capability Execution
  -> DSH Session Event
  -> ACES Evidence/Provenance Adapter
  -> Verification
  -> AcceptedState
```

## Required contracts

1. ACES creates an execution request with intent, policy context, capability scope and provenance requirements.
2. ACES authorization is evaluated before DSH execution.
3. DSH receives only the authorized effective runtime/capability surface.
4. DSH executes through its normal Agent/Tool/Session mechanisms.
5. DSH events are captured as execution telemetry/trajectory, not automatically promoted to ACES Evidence.
6. ACES Evidence Adapter creates evidence objects from selected events plus external observations.
7. Verification evaluates the resulting evidence against the ACES decision contract.
8. Only ACES verification can transition to AcceptedState.
9. Approval/sandbox are subordinate controls and cannot independently authorize an ACES transition.
10. Failure at authorization, execution, evidence, provenance or verification blocks AcceptedState.

## Minimal state machine

```text
S0
 |
 | ACES authorize
 v
AUTHORIZED
 |
 | compile + execute
 v
EXECUTED
 |
 | evidence/provenance
 v
EVIDENCE_READY
 |
 | verify
 v
VERIFIED
 |
 | ACES accept
 v
S1 / AcceptedState
```

Any failure:

```text
ANY STATE -> BLOCKED
```

## Negative controls

The integration is invalid if any of the following occurs:
- DSH plugin registration becomes sufficient authorization;
- DSH approval result becomes ACES Authority;
- DSH sandbox status becomes ACES Security PASS;
- raw DSH event becomes canonical ACES Evidence without provenance/verification;
- model output directly changes AcceptedState;
- GitHub/Grok identity is treated as ACES trust authority.

## R10 result

The minimal integration boundary is architecturally well-defined and compatible with the existing ACES vertical-slice invariant S0 -> Decision(E=PASS,A=PASS) -> Execution -> Verification -> AcceptedState.

This document records the integration contract and negative controls. It does NOT claim that a live DSH-backed implementation has been executed or benchmarked.

## Verdict

PASS — integration contract established; implementation experiment is the next execution task.

Next: R11 — Live Integration Experiment / Instrumented DSH Adapter.

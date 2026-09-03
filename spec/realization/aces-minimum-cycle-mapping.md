# ACES OS — Minimum Cycle Mapping

**Status:** I-1C COMPLETE — IMPLEMENTATION CONTRACT MAPPING
**Date:** 2026-09-03
**Branch:** `architecture/priority-realization-roadmap-v2`
**Purpose:** Convert the already accepted Minimum Implementation Contract into the smallest executable contracts for the first ACES working cycle.

## 1. Governing Rule

No new architecture is introduced by this artifact.

Priority of evidence:

`Executable Evidence > Tests > Existing Implementation > Architecture Specification > Research Hypothesis`

Current repository audit established that `src/` and `tests/` contain no runtime implementation or automated tests. Therefore the contracts below are implementation targets, not claims of existing functionality.

## 2. Canonical Minimum Cycle

`Human Intent → Intent IR → Context → Authority / Policy → Connector Resolution → Execution → Digital World → Observation → Evidence → Verification → Acceptance → Accepted State`

## 3. Minimum Executable Contracts

| Stage | Minimum Input | Minimum Operation | Minimum Output | Mandatory Evidence | Failure States |
|---|---|---|---|---|---|
| Intent | human request | normalize request into stable intent record | `Intent` | intent id + normalized intent | `UNKNOWN`, `ESCALATE` |
| Context | intent | resolve only context required for decision/execution | `Context` | context sources + resolution trace | `UNKNOWN`, `CONFLICT` |
| Authority / Policy | intent + context | evaluate permission, scope, constraints, approval requirement | `AuthorizationDecision` | policy id/rule + decision | `REJECTED`, `ESCALATE` |
| Connector Resolution | authorized action | select allowed connector/capability using CLA-first | `ConnectorPlan` | selected path + capability | `REJECTED`, `UNKNOWN` |
| Execution | connector plan | execute authorized operation through existing execution plane | `ExecutionReceipt` | action + receipt/result | `FAILED`, `UNKNOWN` |
| Observation | execution result + external state | capture relevant resulting state | `Observation` | observation source/time/provenance | `UNKNOWN`, `CONFLICT` |
| Evidence | all prior artifacts | persist machine-readable causal record | `EvidenceBundle` | complete provenance chain | `UNVERIFIED` |
| Verification | intended state + observation + evidence | independently test whether desired state was achieved | `VerificationResult` | verification method + result | `UNVERIFIED`, `CONFLICT`, `REJECTED` |
| Acceptance | verification result | accept only verified state | `AcceptanceDecision` | acceptance rationale | `REJECTED`, `UNVERIFIED` |
| Accepted State | accepted transition | persist canonical transition state | `AcceptedState` | prior/current state + evidence refs | `CONFLICT`, `UNKNOWN` |

## 4. Boundary Invariants

1. `Authority ≠ Connector ≠ Protocol ≠ Capability ≠ Execution`.
2. `Capability ≠ Permission ≠ Approval ≠ Verification ≠ Acceptance ≠ Canonicality`.
3. Model output is not fact.
4. Tool execution is not verification.
5. Unverified state is never canonical.
6. External systems remain owners of their data.
7. Connector/protocol choice cannot bypass authority, evidence, verification, or acceptance.
8. Failure is explicit; fail-closed behavior is mandatory.

## 5. Minimum Evidence Bundle

Every cycle must be able to persist:

- `cycle_id`
- `intent_id`
- normalized intent
- resolved context and provenance
- authorization/policy decision
- selected connector/capability
- requested action
- execution receipt/result
- observation
- evidence identifiers/provenance
- verification method/result
- acceptance decision
- accepted state or explicit failure state

## 6. First Executable Test Shape

The first test must not depend on BASTION or production mutation.

Required controlled sequence:

1. submit deterministic intent;
2. resolve deterministic context;
3. authorize or reject under deterministic policy;
4. resolve a connector path;
5. execute a controlled operation through the existing execution boundary;
6. capture observation;
7. persist evidence;
8. independently verify expected resulting state;
9. accept only on verification PASS;
10. persist accepted or explicit failed state;
11. replay and obtain the same decision/state outcome.

## 7. Gate Mapping

| Roadmap | Mapping |
|---|---|
| R5 ACES Boundary | boundary invariants |
| R6 Digital World Model | minimum context/state representation only |
| R7 Connector Fabric | connector resolution contract |
| R9 Authority / Policy | authorization contract |
| R10 Execution Plane Integration | execution contract |
| R11 Reconciliation | observation → intended-state comparison |
| R12 Evidence / Verification / AcceptedState | evidence, verification, acceptance contracts |
| R16 Vertical Slice | complete minimum cycle |
| R17 Failure / Adversarial Experiments | fail-closed and boundary tests |

R13–R15 are not prerequisites for I-1/I-1C unless implementation evidence proves a dependency.

## 8. Phase Result

**I-1C: PASS — contract decomposition complete.**

The first ACES cycle is now sufficiently decomposed to build a runtime skeleton without inventing additional architecture.

Next phase: **I-1D GAP MATRIX**.

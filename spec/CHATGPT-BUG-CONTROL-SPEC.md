# ACES OS — ChatGPT Bug Control Specification v1.0

**Status:** ACTIVE / FAIL-CLOSED
**Purpose:** Operational specification for preventing, detecting, classifying, correcting, and re-verifying the ChatGPT failure classes registered by KMA-11.
**Authority:** Control specification only. It does not establish architecture, product value, or ACES necessity.

## 1. Control Objective

Prevent ChatGPT-assisted work from converting synthesis, repository persistence, formalization, or process coherence into unsupported epistemic certainty.

## 2. Control Pipeline

Every material ChatGPT-derived claim or decision MUST be processed through:

```text
INPUT
→ SOURCE / PROVENANCE CHECK
→ EVIDENCE CLASSIFICATION
→ TEMPORAL STATE CHECK
→ TRANSFORMATION RECORD
→ INDEPENDENCE / CIRCULARITY CHECK
→ MINIMALITY CHECK
→ CLAIM / DECISION OUTPUT
→ VERIFICATION
→ BUG AUDIT
```

Failure at a mandatory control produces BLOCKED, UNKNOWN, PARTIALLY VERIFIED, or STOP ACQUISITION rather than promotion.

## 3. Control Matrix

| Bug | Preventive control | Detection test | Required response |
|---|---|---|---|
| BUG-001 / 020 | Research-preservation gate | Compare pre/post zero-state research inventory | Restore/reconstruct research; invalidate affected zero-state conclusion |
| BUG-002 | Explicit epistemic labels | Source-to-claim promotion audit | Downgrade unsupported claim |
| BUG-003 | Primary-source precedence | Remove summary and attempt reconstruction | Mark UNKNOWN / recover source |
| BUG-004 | HISTORICAL/CURRENT labels | Temporal provenance check | Separate states; re-evaluate current claim |
| BUG-005 | Repository reality rule | Check artifact vs event/evidence | Do not treat presence as truth |
| BUG-006 | Contract/execution gate | Inspect executable implementation | Mark NOT IMPLEMENTED / NOT EXECUTED |
| BUG-007 | Execution-result gate | Locate actual test run and result | Mark NOT EXECUTED / UNKNOWN |
| BUG-008 / 013 | Research-to-architecture gate | Trace real failure and smaller alternatives | Block architecture escalation |
| BUG-009 | Negative-evidence ledger | Compare primary results to summary | Restore failures, boundaries, and exclusions |
| BUG-010 | Status monotonicity | Compare source status to downstream status | Downgrade and record OLD/NEW/WHY |
| BUG-011 | Independence audit | Counterfactual removal of ChatGPT artifacts | Classify documentation-dependent conclusion |
| BUG-012 | Falsification gate | Ask what evidence could change decision | Continue acquisition or stop; no closure by coherence |
| BUG-014 | Governance minimality test | Trace failure → rule → downstream rule chain | Delete/simplify/reuse unless necessity shown |
| BUG-015 | Inspection-scope declaration | Compare claimed scope with actual queried scope | Correct scope claim; re-run if needed |
| BUG-016 | Sunk-cost blind decision | Re-run decision without historical effort | Base decision only on current evidence/value |
| BUG-017 | Contradiction preservation | Compare source contradictions with final text | Restore contradictions/uncertainty |
| BUG-018 | Intent lock | Compare requested objective with delivered objective | Correct objective; surface interpretation change |
| BUG-019 | Correction ledger | Compare old/new artifacts and rationale | Record explicit epistemic correction |

## 4. Mandatory Materialization Record

Any ChatGPT-derived artifact that materially changes project knowledge MUST, where applicable, preserve:

- STATUS
- SOURCE
- SOURCE TYPE
- SOURCE INDEPENDENCE
- EVIDENCE
- OBSERVATION
- EXECUTION
- MEASUREMENT
- TRANSFORMATION
- CHATGPT CONTRIBUTION
- EPISTEMIC LEVEL
- NEW CLAIMS
- LOST INFORMATION
- NEGATIVE EVIDENCE
- CONTRADICTIONS
- PROMOTION
- PROMOTION JUSTIFICATION
- INDEPENDENT VERIFICATION
- CIRCULARITY RISK
- DOCUMENTATION INFLATION RISK
- ARCHITECTURE INFLATION RISK
- REVERSIBILITY
- DECISION

The record may be embedded in an existing artifact when that is sufficient; creation of a new document is not itself required.

## 5. Transformation Invariants

The following invariants MUST hold:

### I1 — Source fidelity
No claim may be stronger than the evidence supporting it.

### I2 — Status preservation
A downstream transformation cannot silently promote epistemic status.

### I3 — Negative preservation
Failures, contradictions, exclusions, failed experiments, and unknowns remain recoverable.

### I4 — Temporal preservation
Historical state cannot silently become current state.

### I5 — Independence preservation
A ChatGPT-derived artifact cannot become independent evidence merely through repository persistence or repeated reuse.

### I6 — Scope fidelity
Inspection, execution, and verification claims must match actual scope.

### I7 — Minimality
A new rule, protocol, mechanism, or architecture must not be introduced solely to repair an unsupported ChatGPT assumption.

### I8 — Reversibility
Material corrections must preserve enough information to reconstruct the previous claim and why it changed.

## 6. Verification Protocol

Before declaring a materialized result verified:

1. identify the primary source;
2. inspect the actual repository state where repository state is the object of verification;
3. distinguish specification from execution;
4. distinguish execution from successful outcome;
5. inspect negative and contradictory evidence;
6. compare source status with materialized status;
7. test circularity by removing ChatGPT-derived support;
8. verify claimed inspection scope;
9. determine whether a smaller existing-system intervention would suffice;
10. record residual unknowns;
11. only then issue a bounded verdict.

## 7. Bug Reproduction Standard

A bug incident is fully reproduced only when the following are available:

```text
CHATGPT INPUT / CONTEXT
→ CHATGPT ACTION / OUTPUT
→ EXPECTED STATE TRANSITION
→ ACTUAL STATE TRANSITION
→ OBSERVABLE CONSEQUENCE
→ PRIMARY TRACE
→ INDEPENDENT CHECK
```

If one or more critical links are unavailable, classify the result below FULLY REPRODUCED. Do not fill missing links by inference.

## 8. Correction Protocol

For every confirmed material error:

```text
FREEZE
→ PRESERVE OLD STATE
→ IDENTIFY INCORRECT TRANSITION
→ RECONSTRUCT PRIMARY EVIDENCE
→ CLASSIFY BLAST RADIUS
→ CORRECT MINIMALLY
→ RE-VERIFY
→ RECORD RESIDUAL UNKNOWN
```

No silent correction is permitted when the previous state materially affected downstream reasoning.

## 9. Zero-State Safety Protocol

Before architectural deletion or simplification:

```text
INVENTORY RESEARCH
→ INVENTORY EXPERIMENTS / FAILURES / COMPARISONS
→ PRESERVE PRIMARY EVIDENCE
→ CLASSIFY RESULTS
→ DELETE ARCHITECTURAL ASSUMPTIONS
→ RECOMPUTE ZERO-STATE
```

A zero-state result is invalid if relevant research was silently removed during the operation.

## 10. Release Gate for KMA-11 Controls

KMA-11 controls are considered operationally installed only after repository verification confirms:

- KMA-11 audit record is present;
- prevention rules are present;
- this control specification is present;
- files are readable from `main`;
- no claim of historical proof is stronger than the recorded evidence class;
- KMA-12 remains explicitly frozen;
- no KMA-13 repair authority is implied.

## 11. Non-Goals

This specification does not:

- prove ACES necessity;
- validate the current ACES architecture;
- validate every historical R-series result;
- prove every KMA-11 bug incident occurred;
- replace primary evidence;
- authorize implementation repair;
- make the repository a source of truth for historical conversations.

## 12. Verdict Vocabulary

Use only evidence-appropriate labels:

**OBSERVED, EXECUTED, MEASURED, REPRODUCED, SUPPORTED, PARTIALLY VERIFIED, HISTORICAL, HYPOTHESIZED, CHATGPT-DERIVED, UNVERIFIED, CONTRADICTED, INVALIDATED, NOT EXECUTED, BLOCKED, UNKNOWN, CANONICAL.**

`CANONICAL` is reserved for claims whose canonical status is independently authorized by the applicable project process; it is not granted merely by this specification.

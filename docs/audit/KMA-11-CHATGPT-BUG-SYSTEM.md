# ACES OS — KMA-11 ChatGPT Bug System

**Status:** FROZEN / AUDIT RECORD
**Phase:** KMA-11
**Scope:** ChatGPT reasoning, synthesis, evidence handling, state classification, architectural escalation, and materialization behavior during ACES OS work.
**Authority:** Forensic audit record. Not Canon. Not proof of architecture or ACES necessity.
**Precondition:** KMA-0 through KMA-10 completed to their recorded scope.
**KMA-12:** FROZEN.
**KMA-13:** NOT AUTHORIZED by this artifact.

## 1. Purpose

KMA-11 identifies concrete ChatGPT failure classes that can corrupt epistemic state, evidence provenance, scope, historical/current state, or architectural decision-making.

A bug is not considered historically proven merely because the class is plausible or because a control rule exists. Historical incident status requires a reconstructable trace:

```text
CHATGPT ACTION
→ INCORRECT TRANSITION
→ OBSERVABLE RESULT
→ RECOVERABLE TRACE
```

Where that trace is incomplete, the correct status is structural failure class, supported risk, partial reconstruction, unverified incident, or unknown—not invented certainty.

## 2. Evidence Boundary

The following repository facts are independently observable at repository level:

- this KMA-11 artifact exists after this commit;
- the existing ChatGPT Failure Filter v1.1 contains a B-129 section and anti-research-erasure controls;
- repository documents distinguish research from architecture and contract from execution.

These facts do **not** independently prove every historical conversational event described below.

## 3. Registered Bug System

| ID | Failure class | Current forensic status | Required control |
|---|---|---|---|
| BUG-001 | Research collapse during zero audit | HISTORICAL INCIDENT — PARTIALLY VERIFIED | Preserve research before zero-state recomputation |
| BUG-002 | Synthesis given excessive epistemic weight | STRUCTURAL FAILURE CLASS CONFIRMED; incidents require trace | Mandatory source/evidence classification |
| BUG-003 | Summary substituted for primary source | STRUCTURAL FAILURE CLASS CONFIRMED | Primary-source precedence |
| BUG-004 | Historical state treated as current state | STRUCTURAL FAILURE CLASS CONFIRMED; incidents partial | Explicit temporal-state labels |
| BUG-005 | Repository artifact treated as truth | FAILURE CLASS CONFIRMED; individual incidents not all proven | Repository-reality separation |
| BUG-006 | Specification treated as implementation | FAILURE CLASS CONFIRMED; incident not independently reconstructed | Contract/execution gate |
| BUG-007 | Test existence treated as test success | FAILURE CLASS CONFIRMED | Executed-result requirement |
| BUG-008 | Research escalated into architecture | HISTORICAL STRUCTURAL RISK CONFIRMED | Research→architecture escalation gate |
| BUG-009 | Negative evidence compressed away | FAILURE MODE CONFIRMED | Preserve negative results and scope |
| BUG-010 | Uncertainty compressed into stronger status | STRUCTURAL FAILURE CONFIRMED | Status monotonicity / no silent promotion |
| BUG-011 | Circular self-validation | STRUCTURAL RISK CONFIRMED; incidents partial | Independence and circularity audit |
| BUG-012 | Premature closure from coherent explanation | FAILURE CLASS SUPPORTED | Falsification and open-unknown requirement |
| BUG-013 | Architecture used to explain its own necessity | STRUCTURAL FAILURE CLASS CONFIRMED | External-necessity requirement |
| BUG-014 | Governance used to repair epistemic failure | HISTORICAL RESPONSE CONFIRMED; necessity of added governance unproven | Governance minimality gate |
| BUG-015 | Claiming inspections not performed | FAILURE CLASS REQUIRED CONTROL; specific incident not proven here | Inspection-scope declaration |
| BUG-016 | Sunk-cost reasoning | FAILURE CLASS CONFIRMED; causal incidents partial | Evidence-independent continuation decision |
| BUG-017 | Coherence optimization over contradiction preservation | SUPPORTED FAILURE CLASS | Contradiction/uncertainty preservation |
| BUG-018 | User intent rewritten by ChatGPT | UNVERIFIED | Intent-lock and acceptance check |
| BUG-019 | Silent epistemic correction | STRUCTURAL RISK CONFIRMED; incidents partial | OLD/NEW/WHY/EVIDENCE/IMPACT record |
| BUG-020 | Research erasure caused by simplification | HISTORICAL B-129 INSTANCE + STRUCTURAL CLASS CONFIRMED | Zero-state research preservation gate |
| BUG-021 | Executable implementation failed to enforce a fixed non-empty reference constraint from the acceptance-binding contract | HISTORICAL INCIDENT — OBSERVED AND CORRECTED; regression verification completed for the corrected primitive | Contract-to-runtime integrity check; validate executable constraints against fixed schema/contract |

## 4. Severity Classes

### BUG-021 — Executable Contract Constraint Gap

**Classification:** NEW / EXPOSED

**Previous implementation state:** `acceptVerifiedTransition()` checked cross-boundary equality of AcceptanceBinding references but did not reject empty reference values, although the fixed `acceptance-binding.schema.json` contract requires non-empty strings (`minLength: 1`).

**Expected behavior:** A runtime AcceptanceBinding must satisfy the fixed non-empty-reference constraint before an AcceptedState can be produced.

**Observed failure:** During the ChatGPT bug audit, the primitive accepted an AcceptanceBinding whose required references could be empty when they matched the corresponding transition, authority, policy, capability, and verification context references.

**Evidence:** Repository implementation at the pre-correction state; deterministic negative tests were subsequently added for each of the five required references.

**Impact:** The executable primitive could accept malformed binding data despite the fixed contract, weakening runtime integrity at the acceptance boundary.

**Correction:** Added an explicit empty-reference rejection guard and six-case deterministic verification coverage. Local verification on the real repository working tree completed with 6/6 tests passing and exit code 0.

**Residual uncertainty:** No production/runtime integration was tested or authorized; this record establishes only the local primitive correction.

**Prevention:** Future executable implementations MUST compare runtime validation constraints against the fixed contract/schema, including non-empty, type, cross-reference, and other explicitly declared admissibility constraints.


- **C1 — Epistemic corruption:** BUG-002, BUG-010, BUG-011
- **C2 — Evidence/provenance corruption:** BUG-001, BUG-003, BUG-005, BUG-009
- **C3 — Scope/state corruption:** BUG-004, BUG-006, BUG-007, BUG-015
- **C4 — Architecture escalation:** BUG-008, BUG-013
- **C5 — Process/governance inflation:** BUG-012, BUG-014, BUG-016, BUG-017
- **C6 — Unverified/hypothetical:** BUG-018, BUG-019

Severity is a control-priority classification, not a claim that every incident occurred historically.

## 5. B-129 Boundary

B-129 is recorded as a historical incident with partial reconstruction. The repository contains a materialized correction in the ChatGPT Failure Filter, but the artifact itself is not treated as independent proof of the entire conversational trace.

The corrected rule is:

```text
DELETE ARCHITECTURAL ASSUMPTIONS
→ PRESERVE RESEARCH
→ PRESERVE EXPERIMENTS / FAILURES / COMPARISONS
→ RECLASSIFY RESULTS
→ RECOMPUTE ZERO-STATE
```

## 6. Required Bug Trace

Every future claimed ChatGPT bug MUST record:

1. BUG_ID
2. source conversation or execution reference, if recoverable
3. exact ChatGPT action or output
4. expected transition
5. actual incorrect transition
6. observable consequence
7. primary evidence
8. provenance status
9. what was lost or promoted
10. correction
11. residual uncertainty
12. independent verification status

If any critical field is unavailable, the incident MUST NOT be upgraded to fully proven.

## 7. KMA-11 Verdict

**PARTIALLY VERIFIED — BUG SYSTEM ESTABLISHED; INCIDENT RECONSTRUCTION INCOMPLETE.**

This verdict establishes a control target and forensic register. It does not establish that ACES architecture is invalid, that all historical research is false, or that every listed bug occurred as a discrete historical incident.

## 8. Freeze Boundary

KMA-11 is frozen for the current audit checkpoint. KMA-12 remains frozen. No materialization verdict or repair design may be inferred from this record alone.


### BUG-022 — Chat-Sync Scope Anchor Loss

**Classification:** NEW / EXPOSED

**Failure:** During the 100% synchronization operation, ChatGPT synchronized the repository/implementation state but failed to preserve the original research objective of the chat as a mandatory scope anchor. The subsequent scope derivation therefore operated on an incomplete representation of the chat state.

**Expected transition:**
`ENTIRE CHAT PURPOSE → ORIGINAL RESEARCH OBJECTIVE → OPEN / CLOSED OBJECTIVES → CURRENT VERIFIED STATE → NEXT LEGITIMATE SCOPE`

**Observed incorrect transition:**
`REPOSITORY STATE → NO NEW SCOPE JUSTIFIED`

**Observable consequence:** The valid open research objective — finding/verifying an implemented DSH-compatible RU→EN pre-LLM model-visible translation mechanism — was incorrectly treated as if no new scope were justified.

**Primary evidence:** The synchronized repository state and the subsequent conversation correction explicitly distinguish repository-state synchronization from preservation of the original chat purpose and research objective.

**What was lost:** The causal link between the original research objective and next-scope derivation.

**Root cause:** `RepositoryState` was implicitly treated as a sufficient representation of `EntireChatState`.

**Correction required:** Scope derivation MUST consume the original chat purpose, original research objective, objective lineage, open/closed objectives, authorizations, evidence, defects/corrections, and current verified state. Repository state alone is insufficient.

**Residual uncertainty:** This record does not claim that every historical synchronization operation suffered the same failure; it records the observed incident in this branch.

**Prevention:** A synchronization operation is incomplete unless it explicitly reconstructs and preserves the original research objective before deriving the next legitimate scope.

**Verification status:** GOVERNANCE REPAIR APPLIED; downstream refactor/re-verification gates remain separate.

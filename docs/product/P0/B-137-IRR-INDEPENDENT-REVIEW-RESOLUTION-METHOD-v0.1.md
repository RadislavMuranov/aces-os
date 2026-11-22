# IRR — Independent Review Resolution
## Method for resolving the absence of independent acceptance
**Record ID:** B-137-IRR-METHOD-001  
**Version:** 0.1  
**Status:** PROPOSED / WORKING-TREE DRAFT / NOT CANON / NOT ACCEPTED  
**Scope:** B-137 only, unless separately authorized for broader governance use.

## 1. Purpose

IRR resolves a missing independent review without transferring to the human project owner the responsibility to invent the resolution procedure. A missing reviewer or missing evidence is a process state to be handled by the work coordinator; it is not evidence that the artifact passes or fails.

This document records a proposed method. It does not establish a canonical ACES rule, grant acceptance authority, authorize implementation, or close B-137.

## 2. Role separation

| Role | Responsibility |
|---|---|
| Contract author | Produce the reviewable artifact, identify its exact version/hash, and provide provenance and source evidence. |
| ACES work coordinator | Arrange an independent reviewer, provide the frozen review package and acceptance criteria, track the result, and resolve reviewer-unavailability as a process blocker. |
| Independent reviewer | Evaluate the exact frozen artifact against stated criteria, inspect supporting evidence, and issue a reasoned, provenance-bearing verdict. |
| Acceptance Authority | Make the state-transition decision only as authorized by applicable ACES rules. The identity and authority of this role must be established from existing rules, not assumed. |
| Human project owner | Decide only matters that genuinely require the owner's authority; is not the default owner of designing a missing process. |

The coordinator is accountable for organizing review, but cannot impersonate the reviewer or Acceptance Authority.

## 3. Independence requirements

A review qualifies as independent only when its separation from authorship is evidenced. At minimum, the reviewer must:

- not be the author of the reviewed contract;
- not treat the author's self-review or a repeated review by the same authoring process as independent evidence;
- receive the exact artifact identified by cryptographic hash and the applicable review criteria;
- evaluate substantive claims against their source evidence;
- record verdict, rationale, limitations, reviewer identity/role, timestamp, and provenance;
- leave the reviewed artifact unchanged. Any change creates a new version/hash and requires review of that version.

A different session or agent is only a candidate for independence; session separation alone is insufficient proof.

## 4. Deterministic resolution procedure

**Input:** frozen artifact + SHA-256 + review criteria + evidence package.

### Step A — Arrange review
The coordinator identifies an available, qualified reviewer and transfers the frozen package. The transfer and reviewer assignment are recorded.

### Step B — Classify the result

- **PASS:** A reasoned verdict is bound to the exact artifact hash. Submit it to the separately defined acceptance process; do not automatically mark the artifact accepted.
- **FAIL:** Record each unmet criterion and supporting evidence; return the findings to the author for correction. A corrected artifact receives a new hash and must be reviewed again.
- **UNAVAILABLE:** No qualified independent reviewer can be engaged through the available authorized channels. The coordinator records the channels checked, evidence of the search, and the concrete limitation.
- **INSUFFICIENT EVIDENCE:** The reviewer cannot reach a supported verdict. Record the missing evidence, responsible role, and admissible method to obtain it.

### Step C — Resolve or explicitly contain the blocker
If review succeeds, proceed only to the acceptance process allowed by existing authority rules. If review is unavailable or evidence is insufficient, record **BLOCKED — INDEPENDENT REVIEW UNAVAILABLE** or **BLOCKED — INSUFFICIENT EVIDENCE**, as applicable. The coordinator must identify the missing condition, responsible role, resolution method, fallback, stop condition, and closure evidence.

If all authorized review channels are exhausted, the coordinator records that fact and preserves the blocked state. It must not fabricate a reviewer, convert unavailability into PASS/FAIL, or shift the task of inventing a procedure to the human owner.

## 5. Blocker-resolution record

Every unresolved blocker must contain:

| Field | Required content |
|---|---|
| blocker_id | Stable identifier |
| missing_condition | Exact unsatisfied condition |
| evidence_required | Evidence needed to resolve it |
| responsible_role | Role responsible for arranging resolution |
| resolution_method | Authorized procedure |
| fallback | Action if the primary method is unavailable |
| stop_condition | Boundary beyond which action is prohibited |
| closure_evidence | Evidence that the blocker was resolved |

The coordinator must derive these fields from applicable rules and observed capabilities. Where a fact is unknown, it must be investigated or explicitly recorded as unknown—not silently assumed.

## 6. Verification is not acceptance

- **Verification PASS** does not by itself imply AcceptedState.
- **Reviewer unavailable** does not imply PASS or FAIL.
- Repeated self-review does not replace independent review.
- No state transition may occur without the provenance and authority required by applicable ACES rules.
- The method must not grant the coordinator or reviewer acceptance authority that existing rules do not grant.

## 7. Application to B-137

Target contract: B-137-ACES-CONTINUATION-GATE-DESIGN-CONTRACT-v0.3.md  
Target SHA-256: 253BE75AAFC44729322BE9F202FA891A7C7D252A3DAB502CA3B03CCC763A0895

Recorded status at method drafting:
- independent acceptance of the target hash: **NOT CONFIRMED**;
- target contract acceptance: **NOT ACCEPTED**;
- implementation authorization: **NOT GRANTED BY THIS RECORD**;
- B-137 closure: **NOT ESTABLISHED BY THIS RECORD**.

The next method action is for the coordinator to arrange review of the exact target hash and preserve the resulting review evidence. If no authorized independent channel is available, the coordinator must evidence that limitation and record the structured blocker. This document does not claim that a reviewer has been found or that review has occurred.

## 8. Proposed governance rule

> **No Unresolved Blocker Without Resolution Procedure.** Every blocking deficiency must have a defined resolution condition, responsible role, admissible resolution method, fallback, stop condition, and closure evidence. Missing these elements is a control-process defect. The coordinator must remedy the defect within its authority or evidence the limit of available capabilities. The human project owner is not required to design a new resolution procedure for each detected deficiency.

## 9. Status and acceptance boundary

This method is **PROPOSED**, **NOT CANONIZED**, and **NOT ACCEPTED**. Its creation is not independent verification, acceptance, implementation authorization, or a state transition. Canon promotion and wider application require the governance and acceptance process established by ACES.

## 10. Provenance

- Artifact: this Markdown file in the ACES repository working tree.
- Authoring context: B-137 method-fixation request.
- Post-write read-back: completed; SHA-256 computed after final write and recorded in execution evidence.
- Independent review of this method: not performed by this record.

# ACES OS — ChatGPT Failure Filter v1.1

**Status:** ACTIVE / MANDATORY DESIGN FILTER  
**Scope:** All future ACES OS architecture, specification, protocol, governance, evidence, research, and implementation decisions  
**Origin:** R2.2-001 Real-World Failure Discovery Gate / ChatGPT forensic post-mortem / Zero Audit correction  
**Authority:** Process-control rule for architectural work; does not itself establish ACES necessity.

## 1. Purpose

This document is a mandatory anti-overengineering, anti-circularity, and anti-research-erasure filter for future ACES OS work.

Its purpose is to prevent a recurrence of the failure mode in which architectural abstraction, internal coherence, formal evidence, gates, protocols, metrics, project momentum, or premature zeroing are allowed to substitute for independently observed real-world necessity or to erase research evidence relevant to falsification.

**Governing principle:**

> Evidence precedes architecture.

**Core rule:**

> No observed failure, no evolution.

## 2. Primary Architectural Rule

ACES architecture is **guilty until independently justified**.

No architectural component may receive positive necessity status merely because it is:

- coherent;
- elegant;
- useful in principle;
- specified;
- canonical;
- governed;
- already implemented;
- requested by an existing ACES design document;
- required by another ACES component;
- supported by internal metrics.

The burden of proof remains external to the architecture itself.

## 3. Required Causal Chain

Before introducing or materially expanding an ACES-specific architectural mechanism, the following chain MUST exist:

```text
REAL-WORLD TASK
    ↓
OBSERVED FAILURE
    ↓
REPRODUCIBLE / AUDITABLE EVIDENCE
    ↓
MEASURABLE CONSEQUENCE
    ↓
SMALLEST EXISTING-SYSTEM INTERVENTION
    ↓
INTERVENTION RESULT
    ↓
RESIDUAL FAILURE / VALUE GAP
    ↓
SMALLEST NEXT MECHANISM
    ↓
ONLY THEN: ARCHITECTURAL INVESTIGATION
```

If any required link is absent, architectural escalation is BLOCKED.

## 4. Mandatory Minimality Order

Every sufficiently evidenced problem MUST be tested, where applicable, against the smallest available mechanism before an ACES-specific solution is considered:

| Level | Mechanism |
|---|---|
| L0 | Manual procedure |
| L1 | Native application functionality |
| L2 | Existing connector / integration |
| L3 | Generic automation |
| L4 | Minimal coordinator |
| L5 | Specialized ACES mechanism |

**Rule:** L5 MUST NOT be introduced merely to discover whether L4 would work.

If L0–L4 have not demonstrably failed, ACES-specific investigation is BLOCKED.

## 5. Evidence Classification

All claims MUST retain explicit epistemic status:

- **OBSERVED** — directly demonstrated by accessible evidence or executable observation.
- **PARTIALLY VERIFIED** — some elements directly observed, others historical or inferred.
- **HISTORICAL** — recorded previously but not independently reproducible now.
- **HYPOTHESIZED** — plausible but not demonstrated.
- **UNVERIFIED** — insufficient evidence.

Only OBSERVED and PARTIALLY VERIFIED failures may trigger a new minimality test.

Historical evidence cannot establish present architectural necessity by itself.

Hypothesized and unverified problems MUST NOT trigger architecture work.

**Research is evidence-bearing work and MUST NOT be collapsed into architecture.** A research result may be negative, falsifying, boundary-defining, or inconclusive; those outcomes remain part of the evidence base even when the architecture they investigated is deleted.

## 6. Anti-Circularity Rules

The following reasoning is invalid:

- “ACES architecture says this problem exists.”
- “This problem requires continuity because ACES provides continuity.”
- “The architecture has a component for this, therefore the component is necessary.”
- “The system would be better with this feature, therefore the feature is necessary.”
- “The evidence subsystem proves the need for the evidence subsystem.”
- “The Canon validates the architecture because the architecture defines the Canon.”
- “Internal coherence demonstrates external necessity.”
- “A large evidence bundle demonstrates that the underlying architectural claim is true.”
- **“The architecture was deleted, therefore the research that investigated it is also deleted.”**

The architecture MUST NOT be used as its own primary evidence source.

## 7. Runtime / Environment Boundary Rule

Observation is always scoped to the execution environment that produced it.

The following distinctions MUST be preserved:

- observable state ≠ actual state unless independently established;
- inaccessible ≠ absent;
- absent from one environment ≠ absent globally;
- connector-local observation ≠ universal repository truth;
- historical state ≠ current state;
- contract ≠ execution;
- artifact ≠ event;
- provenance ≠ truth.

Cross-environment claims require independent evidence from the relevant environments.

## 8. Product Reality Rule

Architecture, specifications, protocols, research artifacts, metrics, and gates are not substitutes for a working product.

The project MUST periodically return to:

```text
REAL TASK
→ REAL EXECUTION
→ REAL OUTCOME
→ MEASURED VALUE
```

A completed research stage is NOT evidence that the project should continue.

A completed gate is NOT product progress unless it changes an externally meaningful outcome.

However, a completed research stage MUST remain in the research/evidence record when it contains observations, comparisons, experiments, falsification attempts, or negative results relevant to the project decision.

## 9. Human Value Rule

Claims about human benefit MUST NOT be treated as established without evidence.

In particular:

- human cost = NOT QUANTIFIED unless measured;
- friction ≠ automatically parasitic friction;
- convenience ≠ necessity;
- conceptual value ≠ demonstrated value;
- psychic-energy preservation is a value hypothesis, not proof of architectural necessity.

## 10. Complexity Kill Rule

Increasing architectural complexity is itself a warning signal.

The following MUST trigger an explicit deletion/reduction review:

- new subsystem;
- new persistent state;
- new object type;
- new protocol;
- new governance layer;
- new evidence layer;
- new metric without demonstrated decision value;
- new gate created primarily to handle an uncomfortable result;
- new abstraction whose necessity is justified primarily by existing ACES abstractions.

Default action is **DELETE / DO NOT ADD** until independent necessity is demonstrated.

Deletion of an architectural assumption MUST NOT delete the research record used to evaluate that assumption.

## 11. Sunk-Cost Rule

Previously invested effort MUST NOT increase the evidentiary status of a component.

The following are not valid reasons to preserve architecture:

- “We already spent months designing it.”
- “There are many documents supporting it.”
- “It is already in Canon.”
- “Removing it would waste previous work.”
- “The architecture is already internally integrated.”

Past work may be retained as historical evidence, but it does not create present necessity.

## 12. Gate Discipline

A gate exists only to answer a falsifiable question.

A failed gate MUST NOT automatically generate another gate.

A repair cycle MUST NOT be used to protect an architectural assumption from falsification.

If a test cannot materially change the architectural decision, the test SHOULD NOT be created.

Meta-analysis without new empirical evidence is insufficient grounds for continuation.

### Evidence Acquisition Stop Rule

Evidence acquisition is a **bounded action**, not an open-ended state.

For every evidence-acquisition action, the control record MUST define before execution:

1. the exact claim or seam being tested;
2. the admissible source/surface set;
3. the closure condition;
4. the terminal dispositions.

The terminal dispositions MUST include, as applicable:

- **EVIDENCE ESTABLISHED** — the requested execution path or claim is directly established;
- **NO EXECUTION PATH ESTABLISHED** — the admissible source/surface set was exhausted without establishing the path;
- **STOP ACQUISITION — NOT TRUE / NOT FALSE** — the available evidence cannot establish either side.

Once a terminal disposition is reached, the acquisition action MUST STOP.

A terminal **UNKNOWN** or **NO EXECUTION PATH ESTABLISHED** result MUST NOT automatically create another search, another gate, another historical reconstruction, another branch search, or another research seam.

Continuation after a terminal disposition requires a **new explicitly scoped objective and authorization**. It MUST NOT be inferred from the unresolved UNKNOWN itself.

This rule applies equally to current, historical, repository, runtime, connector, and external evidence surfaces.

**Invariant:**

`TerminalEvidenceDisposition ⇒ StopCurrentAcquisition`

`UNKNOWN ⇏ NewEvidenceLoop`

`NO EXECUTION PATH ESTABLISHED ⇏ NewSearch`

The purpose of evidence acquisition is to resolve the declared question, not to eliminate UNKNOWN by indefinite search.

## 13. Failure Survival Rule

For every candidate failure:

- if the smallest available intervention resolves it → **FAILURE FALSIFIED / EXISTING SYSTEM SUFFICIENT**;
- if the failure remains after measured intervention → **RESIDUAL FAILURE OBSERVED**;
- if the result cannot be established → **STOP ACQUISITION — NOT TRUE / NOT FALSE**.

Unknown MUST NOT be converted into architectural necessity.

## 14. Architecture Escalation Gate

An ACES-specific mechanism may be investigated only when all of the following are satisfied:

1. a real task exists;
2. a concrete failure has been observed;
3. evidence is independently accessible/auditable;
4. consequence is established;
5. L0 has been considered/tested where applicable;
6. L1 has been considered/tested where applicable;
7. L2 has been considered/tested where applicable;
8. L3 has been considered/tested where applicable;
9. L4 has been considered/tested where applicable;
10. at least one smaller mechanism has demonstrably failed to close the residual gap;
11. the residual gap remains operationally meaningful;
12. the proposed ACES mechanism is the smallest plausible mechanism for that residual gap.

Even after these conditions are met, ACES necessity remains a hypothesis until the proposed mechanism itself produces measured external value.

## 15. Mandatory Failure Register

The following previously observed ChatGPT failure classes are permanently treated as prohibited reasoning patterns during ACES design:

- premature architecture;
- hidden premise that ACES must exist;
- hypothesis inflation;
- assumption persistence;
- epistemic status drift;
- confidence drift;
- evidence substitution;
- contract/execution confusion;
- design/necessity confusion;
- internal coherence treated as truth;
- component proliferation;
- object proliferation;
- protocol proliferation;
- gate proliferation;
- repair proliferation;
- architecture sedimentation;
- lack of default deletion;
- local PASS inflation;
- conditional PASS inflation;
- process validation substituted for value validation;
- historical/current evidence mixing;
- insufficient substitution testing;
- native/manual/connector/automation alternatives under-tested;
- environment equivalence assumptions;
- missing treated as absent;
- access treated as existence;
- tool capability treated as integrated system capability;
- human cost assumed rather than measured;
- friction inflated into necessity;
- metric-before-necessity;
- false precision;
- research recursion;
- process self-reference;
- research replacing implementation;
- implementation postponement;
- product starvation;
- sunk-cost reinforcement;
- continuation bias;
- complexity normalization;
- abstraction mistaken for progress;
- vocabulary/formality mistaken for rigor;
- reset contamination;
- failure to perform zero-state deletion test;
- **research collapse into architecture** — deleting or ignoring research findings merely because the architecture investigated by that research has been deleted;
- **research-layer erasure during zero audit** — treating zeroing as permission to discard comparative studies, falsification attempts, experiments, negative results, or boundary findings;
- **premature evidence compression** — reducing a multi-line research history to a small set of observed failures before checking whether discarded research contains decision-relevant evidence;
- **external-research blindness** — omitting relevant external research or comparative ecosystem findings (for example agent-native/harness research) from a revalidation because they do not fit the current zero-state narrative.
- **executable-contract constraint gap** — implementing a fixed contract or schema incompletely, especially by enforcing structural/reference equality while omitting explicit runtime admissibility constraints such as non-empty values.
- **unbounded evidence-acquisition loop** — continuing evidence search after the declared seam has reached a terminal disposition, especially by expanding into historical branches, alternate runtimes, adjacent seams, or new searches without a new objective and authorization. This converts UNKNOWN into indefinite process activity and can erase the closure semantics of a fail-closed gate. Prevention: define the source set, closure condition, and terminal dispositions before acquisition; once terminal disposition is reached, stop current acquisition.



### B-133 — Recurrent Control-Point Materialization Failure

**Classification:** RECURRING / REPAIR EFFECTIVENESS FAILURE

**Failure:** After a previous control-plane repair was declared CLOSED and PASS, the same behavioral failure was reproduced: a terminal disposition was emitted without a concrete authorization decision stating the exact action, exact scope, forbidden scope, and the exact user choice required to authorize or reject continuation.

**Previous state:** The earlier repair materialized NEXT LEGITIMATE ACTION and AUTHORIZATION REQUIRED in the iteration record, but did not make the terminal response itself conform to a mandatory control-point contract.

**Observed recurrence:**
```
previous defect
    ↓
repair
    ↓
repair declared CLOSED
    ↓
same behavioral failure reproduced
    ↓
repair effectiveness = NOT ESTABLISHED
```

**Impact:** A terminal state could still leave the human without a deterministic authorization surface, allowing the same ambiguity to recur immediately after a supposedly closed repair.

**Correction:** Introduce a mandatory next-control-point contract for terminal dispositions:
```
TERMINAL DISPOSITION
        ↓
MANDATORY NEXT-CONTROL-POINT CONTRACT
        ↓
EXACT ACTION
        ↓
EXACT SCOPE
        ↓
FORBIDDEN SCOPE
        ↓
AUTHORIZATION REQUIRED = YES/NO
        ↓
EXACT USER DECISION
        ↓
STOP
```

**Required behavioral output:** When authorization is required, the terminal response MUST explicitly contain both an **AUTHORIZE** decision with the exact action and exact scope, and a **DO NOT AUTHORIZE / CHOOSE ANOTHER EXPLICITLY SCOPED OBJECTIVE** decision. Generic language such as “a new explicitly authorized decision is required” is insufficient.

**Repair-effectiveness criterion:** No terminal disposition may be considered correctly closed if the user cannot determine from that terminal output exactly what action is proposed, exactly what scope is authorized, what is forbidden, whether authorization is required, and what exact decision the user must make.

**Recurrence rule:** A prior PASS does not establish repair effectiveness after the same behavioral failure is reproduced. The repair remains NOT ESTABLISHED until the behavioral output contract is independently re-verified against the recurrence case.

**Prevention:** Treat the next-control-point contract as a mandatory terminal-output invariant, not merely as information stored in an iteration record. Do not infer authorization from a defect report; a defect report is not authorization to repair or continue the underlying work.


### B-130 — Executable Contract Constraint Gap

**Classification:** NEW / EXPOSED  
**Failure:** ChatGPT produced an executable acceptance primitive that enforced the fixed AcceptanceBinding cross-reference relationships but omitted the explicit non-empty-reference constraint present in the fixed schema.  
**Previous state:** Empty required references could pass the executable boundary when all corresponding references matched.  
**Expected state:** Every required AcceptanceBinding reference must satisfy the fixed contract before AcceptedState can be produced.  
**Observable consequence:** The primitive could return AcceptedState for malformed empty reference values.  
**Impact:** Runtime implementation semantics were weaker than the fixed acceptance-binding contract.  
**Correction:** Added explicit rejection of empty AcceptanceBinding references and deterministic negative coverage for all five required references.  
**Independent verification:** Real local working tree verification completed: 6 tests passed, 0 failed, exit code 0.  
**Residual boundary:** No production/runtime integration was performed or authorized.  
**Prevention:** Before declaring an executable contract implementation complete, compare every explicit schema/contract constraint against runtime enforcement, not only cross-object relationships.

## 16. Mandatory Decision Language

When evidence is insufficient, the correct output is one of:

- **NO NEW FAILURE SUFFICIENTLY OBSERVED**
- **STOP ACQUISITION — NOT TRUE / NOT FALSE**
- **EXISTING SYSTEMS SUFFICIENT**
- **PROBLEM REAL / FORM UNKNOWN**
- **RESIDUAL FAILURE OBSERVED**

The following language MUST NOT be used to imply stronger evidence than exists:

- “architecturally necessary”;
- “validated system”;
- “proven value”;
- “production-ready”;
- “canonical necessity”;
- “evidence-backed architecture”

unless the corresponding evidence actually exists.

## 17. Zero-State Test

Whenever architectural momentum becomes substantial, the project MUST be willing to ask:

> **What remains if every ACES-specific architectural assumption is deleted?**

The zero-state procedure MUST be:

```text
DELETE ARCHITECTURAL ASSUMPTIONS
        ↓
PRESERVE RESEARCH RECORD
        ↓
PRESERVE OBSERVED FAILURES / EXPERIMENTS / COMPARISONS
        ↓
RECLASSIFY EACH RESULT
        ↓
RECOMPUTE WHAT REMAINS UNFALSIFIED
        ↓
ONLY THEN: DECIDE WHETHER ANY NEW MECHANISM IS JUSTIFIED
```

If the answer is “nothing demonstrably necessary,” architecture development stops. This does **not** mean research evidence is discarded.

## 18. Final Rule

> **Do not build a system to explain a problem that has not been independently demonstrated.**
>
> **Do not add architecture to repair an architectural assumption.**
>
> **Do not erase research because the architecture it investigated was deleted.**
>
> **Do not confuse intellectual complexity with product value.**
>
> **Do not continue because work has already been invested.**
>
> **No observed failure, no evolution.**

## 19. Provenance

This filter is derived from the ChatGPT forensic failure register produced during ACES OS revalidation/reset after R2.2-001.

### B-129 — Research Collapse During Zero Audit

**Classification:** NEW / EXPOSED  
**Failure:** During a zero-state audit, ChatGPT removed architectural assumptions correctly but simultaneously compressed/removed relevant research lines, including comparative and falsification research, instead of preserving them as evidence.  
**Previous claim:** “After removing architecture, only observed cross-environment tasks/failures and a remaining hypothesis survive.”  
**Contradiction:** This omitted prior research that materially bears on the falsification question, including Karpathy/agent-native research, R0–R13 research, H-CENSUS, DSH research, E3, AKCS-40X, and comparative harness/continuity research.  
**Impact:** The zero audit became epistemically incomplete and risked producing a false conclusion by erasing evidence relevant to whether ACES is necessary, replaceable, or reducible.  
**Correction:** Separate **architecture**, **research**, **observations**, **experiments**, **failures**, and **measured value**. Delete architectural assumptions without deleting the research that tested them.  
**Prevention:** Every zero audit MUST preserve the full research inventory first, classify each research result, and only then recompute the surviving hypothesis/evidence base.

This filter is a process-control artifact, not evidence that ACES OS is necessary.


### B-131 — Chat-Sync Scope Anchor Loss

**Classification:** NEW / EXPOSED

**Failure:** A 100% synchronization operation can preserve repository/implementation state while dropping the original research objective that gives the branch its purpose. If next-scope derivation then uses repository state as its principal input, it can produce a false `NO NEW SCOPE JUSTIFIED` result.

**Expected state reconstruction:**
`ENTIRE CHAT PURPOSE → ORIGINAL RESEARCH OBJECTIVE → OBJECTIVE LINEAGE → OPEN / CLOSED OBJECTIVES → AUTHORIZATIONS → EVIDENCE / DEFECTS / CORRECTIONS → CURRENT VERIFIED STATE → NEXT LEGITIMATE SCOPE`

**Prohibited substitution:**
`REPOSITORY STATE → NEXT SCOPE`

**Observable consequence:** A still-open research objective may disappear from the derived scope even though the implementation branch associated with it is closed.

**Impact:** Loss of research intent continuity can terminate the wrong objective and cause subsequent actions to be derived from an incomplete state.

**Correction:** Scope derivation is now governed by an explicit scope-anchor requirement in the Master Protocol. Repository/implementation state is not a sufficient representation of complete chat state.

**Prevention rule:** Every 100% synchronization MUST explicitly reconstruct the entire chat purpose and original research objective before classifying objectives as open/closed or deriving the next legitimate scope. If the original objective cannot be established, scope derivation MUST be `UNKNOWN / NOT VERIFIED`, not `NO NEW SCOPE JUSTIFIED`.

**Residual boundary:** This control prevents the reasoning transition; it does not itself prove any research objective or ACES architectural necessity.


### B-132 — Undurable Repair Claim

**Classification:** NEW / EXPOSED

**Failure:** A proposed invariant or repair design was presented as repaired before the corresponding authoritative governance/bug-prevention control had been materially created.

**Expected:** `DEFECT → REPAIR SPECIFICATION → GOVERNANCE MATERIALIZATION → VERIFICATION`.

**Observed:** `DEFECT → FORMULATED INVARIANTS → CLAIMED REPAIR`.

**Impact:** A repair can exist only in conversational reasoning while the authoritative prevention system remains unchanged.

**Correction:** The current chat-sync repair has now been materially recorded in KMA-11, the active Failure Filter, and the canonical Master Protocol.

**Prevention rule:** Never report a repair as applied merely because its design has been formulated. Applied repair requires an observable authoritative artifact; verification of that artifact remains a separate gate.

**Residual boundary:** Materialization does not imply that the new control has already passed its subsequent refactor/re-verification gates.


### B-134 — Decision-Ready Control-Point Materialization Failure

**Classification:** RECURRING / CONTROL-PLANE CONTRACT DEFECT / REPAIR EFFECTIVENESS FAILURE

**Observed defect:** The B-133 repair required a terminal response to expose an exact action, exact scope, forbidden scope, authorization requirement, and exact user decision. The resulting response still used meta-language such as “the next authorization decision must be concretely formulated”. That language names a requirement for a future control point but does not itself constitute a decision-ready control point.

**Why this is a distinct deeper defect:** B-133 treated control-point materialization as a content checklist. It did not define the roles, timing, placement, trigger, purpose, decision object, decision state, and transition semantics that make a control point executable as a human decision boundary.

**Fundamental correction:** Separate **control-point materialization** from **authorization decision**.

The control process/assistant is responsible for **materializing the decision-ready control point**. The designated human authority is responsible for **making the authorization decision**. The control point MUST exist before the human decision is requested. The system MUST NOT ask the human to formulate the control point that the system is responsible for exposing.

**Decision-ready control-point contract:**
```
CONTROL_POINT_ID
PRODUCER / FORMULATOR
DECISION_AUTHORITY
TRIGGER / TERMINAL_DISPOSITION
CREATION_POINT / WHEN
LOCATION / WHERE
REASON / WHY
PURPOSE / FOR WHAT
DECISION_OBJECT / WHAT IS BEING DECIDED
PROPOSED_ACTION
EXACT_SCOPE
FORBIDDEN_SCOPE
EVIDENCE_STATE
AUTHORIZATION_REQUIRED
DECISION_OPTIONS
EFFECT_OF_EACH_OPTION
STOP_CONDITION
DECISION_STATUS = PENDING
```

**Mandatory semantics:**

1. **WHO:** the control process/assistant materializes the control point; the designated human authority makes the decision. These roles MUST NOT be conflated.
2. **WHEN:** materialization occurs immediately when a terminal disposition is reached and before any continuation.
3. **WHERE:** the complete control point is present in the terminal response; when durable governance provenance is required, the same control point is recorded in the applicable iteration/control record.
4. **WHY:** the terminal disposition has closed the current bounded action and a human decision is required to determine whether a separately bounded continuation may occur.
5. **PURPOSE:** expose a deterministic human decision boundary without executing or implying the proposed continuation.
6. **WHAT:** the decision object MUST be one concrete proposed action or an explicitly enumerated alternative, not “the next decision”.
7. **ACTION/SCOPE:** the proposed action and its exact scope MUST be stated.
8. **FORBIDDEN SCOPE:** prohibited expansion MUST be stated.
9. **EVIDENCE:** the control point MUST state the verified state and terminal disposition on which it is based.
10. **AUTHORIZATION:** authorization requirement MUST be explicit.
11. **OPTIONS:** at minimum AUTHORIZE and DO NOT AUTHORIZE / ALTERNATIVE MUST be explicit when authorization is required.
12. **EFFECT:** the consequence of each decision option MUST be stated.
13. **STOP:** after materialization, the process MUST stop and wait for the human decision. No decision may be inferred.
14. **NO META-LOOP:** a decision-ready control point MUST NOT point to “another authorization decision” as its action. Its action is the bounded operation that the human may authorize or reject.
15. **PENDING IS REAL STATE:** before the human responds, `DECISION_STATUS = PENDING`; it is neither AUTHORIZED nor REJECTED.
16. **NO SELF-AUTHORIZATION:** the producer/formulator MUST NOT also supply the human authorization outcome.
17. **NO GENERIC SUBSTITUTION:** phrases such as “explicit authorization is required”, “the next decision must be formulated”, or “a new control point is needed” are invalid unless accompanied by the complete decision-ready contract.

**Validity predicate:**

`DecisionReadyControlPoint` is TRUE iff all mandatory fields are present, the proposed action is bounded, the decision authority is explicit, the decision status is PENDING, and the output terminates in a STOP awaiting that decision.

Therefore:

```
TerminalDisposition ∧ ContinuationCandidate
    ⇒ DecisionReadyControlPoint(PENDING)
    ⇒ STOP_AND_WAIT_FOR_HUMAN_DECISION

DecisionReadyControlPoint(PENDING)
    ⇏ Authorization

HumanAuthorization
    ⇒ only the exact proposed action/scope becomes authorized

HumanRejection
    ⇒ proposed continuation is not authorized

DecisionReadyControlPoint(PENDING)
    ⇏ NewAuthorizationLoop
```

**Terminal cases:**

- If no continuation is legitimate or necessary: emit the terminal disposition and STOP; no authorization control point is required.
- If continuation is possible and requires human authority: emit exactly one Decision-Ready Control Point in PENDING state and STOP.
- If the human selects an alternative: that alternative becomes a new explicitly scoped objective only after the human decision; it is not inferred from the terminal disposition.

**Repair-effectiveness criterion:** A terminal output fails the contract if the human must still determine or formulate WHO, WHEN, WHERE, WHY, PURPOSE, WHAT, ACTION, SCOPE, FORBIDDEN SCOPE, AUTHORITY, OPTIONS, EFFECT, or STOP semantics. The control process must provide these before asking for a decision.

**Fundamental anti-recursion invariant:**

`CONTROL_POINT_MATERIALIZED ⇒ DECISION_READY ∧ PENDING ∧ STOP`

`PENDING_CONTROL_POINT ⇏ NEW_CONTROL_POINT`

`TERMINAL_DISPOSITION ⇏ AUTOMATIC_CONTINUATION`

`USER_DECISION ⇒ TRANSITION_TO_AUTHORIZED_OR_REJECTED`

This repair closes the identified recursion by making the **decision itself** the control point rather than making “the next authorization decision” the next control point.

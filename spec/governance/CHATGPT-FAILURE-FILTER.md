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

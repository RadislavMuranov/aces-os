# ACES OS — ChatGPT Iteration Verification, Refactoring & Bug-Learning Gate v1.0

**Status:** ACTIVE / MANDATORY / FAIL-CLOSED  
**Scope:** Every ChatGPT-assisted ACES OS iteration, including research, architecture, specification, governance, evidence, implementation, verification, and repository changes.  
**Depends on:** `spec/governance/CHATGPT-FAILURE-FILTER.md`  
**Authority:** Process-control rule. It does not establish ACES necessity.

## 1. Purpose

This rule makes every iteration a complete verification-and-learning cycle rather than a one-way generation cycle.

The objective is not merely to verify whether the requested change works. The objective is to determine whether the iteration introduced, exposed, repeated, concealed, amplified, or failed to detect any ChatGPT error.

Every iteration MUST therefore end with one of two states:

- **VERIFIED + REFACTORED + BUG AUDITED + LEARNED**
- **BLOCKED / INCOMPLETE**

A partial check MUST NOT be represented as a completed iteration.

## 2. Non-Negotiable Rule

> **NO ITERATION PASS WITHOUT REPOSITORY VERIFICATION, FULL SELF-AUDIT, REFACTORING REVIEW, AND BUG-BASE UPDATE.**

The absence of a newly discovered bug does not mean that no bug exists. The audit must actively attempt to falsify ChatGPT's own work.

The audit MUST NOT be skipped because:

- the change is small;
- the answer appears obvious;
- previous iterations passed;
- the requested task is urgent;
- the repository appears consistent;
- no failure is immediately visible;
- the change is documentation-only;
- the model is confident;
- the previous version already contained the same assumption.

## 3. Iteration State Machine

Every iteration MUST follow this sequence:

```text
I0  DEFINE CHANGE / QUESTION
 ↓
I1  READ RELEVANT REPOSITORY STATE
 ↓
I2  IDENTIFY CLAIMS, ASSUMPTIONS, DEPENDENCIES
 ↓
I3  MAKE MINIMAL CHANGE / EXECUTE TEST
 ↓
I4  VERIFY ACTUAL REPOSITORY STATE
 ↓
I5  VERIFY BEHAVIOR / EVIDENCE / PROVENANCE
 ↓
I6  ADVERSARIAL CHATGPT BUG AUDIT
 ↓
I7  REFACTOR / REMOVE / CORRECT
 ↓
I8  RE-VERIFY AFTER REFACTOR
 ↓
I9  COMPARE AGAINST FAILURE FILTER + PRIOR BUG BASE
 ↓
I10 RECORD NEW / RECURRING / RESOLVED BUGS
 ↓
I11 PRODUCE ITERATION VERDICT
```

No step may be silently omitted.

If a step is impossible because the required environment, tool, evidence, or runtime is unavailable, the iteration MUST be marked **BLOCKED / NOT VERIFIED**, not PASS.

## 4. Repository-First Verification

Before making a repository-dependent claim or change, ChatGPT MUST inspect the relevant current repository state.

After making a change, ChatGPT MUST independently inspect the resulting repository state.

The following distinctions MUST remain explicit:

- intended change ≠ committed change;
- committed change ≠ verified behavior;
- file existence ≠ correctness;
- repository text ≠ runtime execution;
- current state ≠ historical state;
- connector observation ≠ universal truth.

When a claim conflicts with the repository, the repository observation wins unless independently disproven.

## 5. Complete Self-Audit Requirement

The audit MUST actively check for all known ChatGPT failure classes in the current failure filter, including at minimum:

### Epistemic
- hypothesis presented as fact;
- evidence status inflation;
- confidence inflation;
- historical/current mixing;
- observation/inference collapse;
- unknown converted into certainty;
- inaccessible converted into absent;
- provenance confused with truth.

### Architecture
- premature architecture;
- hidden assumption that ACES must exist;
- solution becoming premise;
- unnecessary component/object/protocol/gate proliferation;
- architecture used to justify itself;
- complexity mistaken for rigor;
- internal coherence mistaken for necessity;
- failure to apply deletion/zero-state testing.

### Validation
- contract mistaken for execution;
- artifact mistaken for event;
- local PASS inflated into system validation;
- conditional PASS inflated into PASS;
- test unable to change the decision;
- verification performed only on the expected path;
- missing negative/adversarial test;
- incomplete evidence reported as complete.

### Minimality
- L0 manual alternative skipped;
- L1 native capability skipped;
- L2 connector/integration skipped;
- L3 generic automation skipped;
- L4 minimal coordinator skipped;
- ACES-specific mechanism introduced before smaller alternatives demonstrably fail.

### Runtime / Environment
- environment equivalence assumed;
- connector boundary ignored;
- permissions treated as capabilities;
- capability treated as integration;
- one environment treated as universal reality;
- inaccessible state treated as absent state.

### Product / Human Value
- research progress mistaken for product progress;
- human cost assumed rather than measured;
- friction inflated into necessity;
- conceptual usefulness treated as demonstrated value;
- architecture expanded while real execution remains absent.

### Process
- research recursion;
- gate proliferation;
- repair cycle protecting an assumption;
- sunk-cost continuation;
- previous work used as justification for continuation;
- reset contamination;
- abstraction mistaken for progress;
- formal language mistaken for rigor.

## 6. Mandatory Refactoring Pass

Verification alone is insufficient.

After the self-audit, ChatGPT MUST ask:

1. What can be deleted?
2. What can be simplified?
3. What claim can be weakened to match evidence?
4. What assumption can be removed?
5. What duplicated mechanism can be eliminated?
6. What test can replace a document or assertion?
7. What existing system can replace the proposed mechanism?
8. What part of the iteration is unnecessary if the original goal is examined literally?

Default preference:

```text
DELETE > SIMPLIFY > REUSE > EXISTING SYSTEM > GENERIC MECHANISM > NEW ACES MECHANISM
```

A refactoring pass that finds nothing to delete is not automatically wrong, but the audit MUST record that deletion was explicitly attempted.

## 7. Bug Discovery Requirement

Every iteration MUST actively search for **new bugs**, not only known bugs.

A bug qualifies for the bug base when it represents a reproducible or sufficiently evidenced failure in ChatGPT's reasoning, verification, implementation guidance, evidence handling, process control, or interaction with the repository.

A newly discovered bug MUST receive:

- unique identifier;
- concise name;
- exact failure description;
- affected iteration;
- affected artifact/file/claim;
- evidence;
- expected behavior;
- actual behavior;
- root cause or current best hypothesis, clearly labelled;
- severity;
- recurrence status;
- containment;
- corrective action;
- prevention rule;
- verification of the fix;
- regression test or audit check where applicable.

## 8. Bug Classification

Every discovered bug MUST be classified as one or more of:

- **NEW** — not previously present in the failure base;
- **RECURRING** — substantially repeats an existing bug;
- **AMPLIFIED** — an existing bug became more severe;
- **ESCAPED** — an existing filter failed to detect it;
- **EXPOSED** — newly revealed by a changed environment or test;
- **RESOLVED** — previous bug verified as fixed;
- **UNRESOLVED** — mitigation attempted but failure remains;
- **UNKNOWN** — insufficient evidence to classify further.

`NEW`, `RECURRING`, `AMPLIFIED`, and `ESCAPED` findings MUST be added to or update the failure-filter knowledge base.

## 9. No Silent Bug Fixes

ChatGPT MUST NOT silently correct its own error and present the corrected result as though the error never occurred.

If an iteration reveals that a previous statement, decision, test result, or repository claim was wrong, the audit MUST explicitly record:

```text
PREVIOUS CLAIM
→ OBSERVED CONTRADICTION
→ BUG
→ IMPACT
→ CORRECTION
→ REGRESSION PREVENTION
```

This rule exists to prevent error erasure and false continuity.

## 10. Failure-Filter Learning Loop

The failure database is not static documentation.

Every iteration MUST execute:

```text
CURRENT ITERATION
    ↓
BUG SEARCH
    ↓
KNOWN FILTER MATCH?
   ↙        ↘
 YES        NO
 ↓           ↓
CHECK       CLASSIFY AS CANDIDATE NEW BUG
RECURRENCE  ↓
 ↓          EVIDENCE
REMEDIATE   ↓
 ↓          ADD TO FILTER / BUG BASE
RETEST      ↓
 ↓          UPDATE PREVENTION RULE
 └──────┬───┘
        ↓
   REGRESSION CHECK
        ↓
    ITERATION VERDICT
```

A newly discovered bug MUST change the future filter whenever the bug is generalizable beyond the single incident.

## 11. Filter Expansion Rule

The failure filter MUST evolve from observed failures, not speculative fears.

A new filter rule may be added when:

1. a concrete ChatGPT failure is evidenced;
2. the failure mechanism is sufficiently understood, or the uncertainty is explicitly recorded;
3. the rule is general enough to prevent recurrence;
4. the rule does not merely duplicate an existing rule;
5. the rule is testable in future iterations.

No speculative rule proliferation is permitted.

## 12. Regression Rule

Every previously discovered high-severity or recurring bug MUST be considered during relevant iterations.

A previously fixed bug is not permanently trusted merely because it was once fixed.

Where applicable, each relevant iteration MUST perform a regression check proving that the same failure mode did not return under a new:

- task;
- file;
- branch;
- environment;
- connector;
- evidence source;
- architecture layer;
- wording or abstraction.

## 13. Evidence Rule

Every self-audit finding MUST distinguish:

- **OBSERVED**;
- **PARTIALLY VERIFIED**;
- **HISTORICAL**;
- **HYPOTHESIZED**;
- **UNVERIFIED**.

ChatGPT MUST NOT label a suspected bug as confirmed without evidence.

Conversely, ChatGPT MUST NOT downgrade a directly observed failure merely because acknowledging it is inconvenient to the current design.

## 14. Refactoring Completion Gate

The iteration cannot PASS until all applicable conditions are true:

- repository state checked before change;
- relevant source inspected;
- change executed;
- resulting repository state checked;
- behavior/evidence checked where applicable;
- known failure classes audited;
- adversarial search for new bugs performed;
- deletion/simplification pass performed;
- all discovered bugs classified;
- new/recurring/escaped bugs recorded;
- corrections re-verified;
- relevant regression checks completed;
- remaining unknowns explicitly recorded;
- final claim strength matches evidence strength.

## 15. Mandatory Stop Conditions

The iteration MUST STOP rather than PASS when:

- repository state cannot be inspected;
- the relevant evidence cannot be accessed;
- a contradiction cannot be resolved;
- a claimed fix cannot be verified;
- a suspected regression cannot be tested;
- a bug is discovered but its impact is material and containment is unknown;
- the requested change depends on an unverified architectural premise;
- an ACES-specific mechanism is being introduced without surviving minimality evidence;
- the self-audit is incomplete;
- the bug-base update cannot be completed for a confirmed new bug.

Correct output:

**BLOCKED / INCOMPLETE — DO NOT CLAIM PASS.**

## 16. Mandatory Iteration Record

Each completed iteration MUST produce an internal record containing at least:

```text
ITERATION_ID
DATE
OBJECTIVE
REPOSITORY_STATE_BEFORE
CHANGE / ACTION
REPOSITORY_STATE_AFTER
VERIFICATION
KNOWN_BUGS_CHECKED
NEW_BUGS
RECURRING_BUGS
AMPLIFIED_BUGS
ESCAPED_BUGS
RESOLVED_BUGS
REFACTORING ACTIONS
DELETIONS CONSIDERED
REMAINING RISKS
UNKNOWN / UNVERIFIED ITEMS
FILTER UPDATED?
REGRESSION CHECK
FINAL VERDICT
```

The record may be concise, but no required field may be silently omitted. If a field is not applicable, mark `N/A`; if it cannot be established, mark `UNKNOWN` or `NOT VERIFIED`.

## 17. Verdicts

Permitted final verdicts:

- **PASS — VERIFIED + REFACTORED + BUG AUDITED + LEARNED**
- **CONDITIONAL — LIMITED VERIFICATION / EXPLICIT BOUNDARY**
- **BLOCKED — VERIFICATION INCOMPLETE**
- **FAIL — BUG OR REGRESSION DETECTED**
- **STOP ACQUISITION — NOT TRUE / NOT FALSE**

`PASS` MUST NOT be used when the required audit was skipped.

## 18. Relationship to the Existing ChatGPT Failure Filter

`CHATGPT-FAILURE-FILTER.md` remains the governing catalogue of known failure patterns.

This document adds the mandatory **iteration-level execution loop**:

```text
FAILURE FILTER
      ↓
AUDIT EVERY ITERATION
      ↓
FIND NEW / RECURRING BUG
      ↓
EVIDENCE
      ↓
REFACTOR
      ↓
RE-VERIFY
      ↓
UPDATE FAILURE FILTER
      ↓
REGRESSION TEST NEXT ITERATIONS
```

The two documents MUST be treated as complementary:

- Failure Filter = **what must not happen**.
- Iteration Gate = **how every iteration checks whether it happened**.

## 19. Final Rule

> **Every iteration must attempt to prove that ChatGPT is wrong.**
>
> **Every iteration must inspect the repository before and after change.**
>
> **Every iteration must search for new bugs, not merely verify expected behavior.**
>
> **Every discovered bug must be named, evidenced, contained, corrected, and learned into the filter when generalizable.**
>
> **No silent fixes. No erased failures. No inherited trust. No PASS without verification.**
>
> **The purpose of iteration is not to preserve the previous answer. It is to discover whether the previous answer survives contact with reality.**

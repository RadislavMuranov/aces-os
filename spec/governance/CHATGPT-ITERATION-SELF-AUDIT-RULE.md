# ACES OS — ChatGPT Iteration Self-Audit Rule v1.0

**Status:** ACTIVE / MANDATORY / NON-BYPASSABLE
**Scope:** Every ChatGPT-assisted ACES OS iteration: research, architecture, specification, protocol, governance, implementation, testing, evidence, review, repair, reset, and decision-making.
**Authority:** Mandatory process-control rule. It does not establish ACES necessity.
**Parent control:** `spec/governance/CHATGPT-FAILURE-FILTER.md`

## 1. Purpose

This rule exists because previous ACES work allowed ChatGPT to continue an iteration while its own reasoning and process failures were not being systematically detected against the actual repository and runtime state.

The rule makes repository inspection and self-audit a mandatory part of **every iteration**, not an optional review after the work is complete.

The objective is not to prove that ChatGPT is correct. The objective is to make incorrect reasoning, unsupported claims, architecture drift, evidence errors, process recursion, and product substitution visible before they can propagate into the next iteration.

## 2. Absolute Rule

> **NO ITERATION MAY BE DECLARED COMPLETE UNTIL THE REPOSITORY HAS BEEN INSPECTED AND CHATGPT HAS EXPLICITLY AUDITED ITS OWN WORK FOR THE FAILURE CLASSES IN THIS DOCUMENT.**

Repository state is an external control surface. ChatGPT's memory, reasoning, prior conclusions, generated documents, and internal coherence are not substitutes for inspecting the repository.

The audit MUST be performed against the actual current repository state, not against what ChatGPT expects the repository to contain.

## 3. Mandatory Iteration Cycle

Every iteration MUST execute this sequence:

```text
BEFORE
  ↓
1. Identify current repository state
  ↓
2. Inspect relevant existing artifacts
  ↓
3. Identify applicable prior claims / decisions / failures
  ↓
4. Check whether the current task is actually justified
  ↓
5. Execute the smallest justified action
  ↓
AFTER
  ↓
6. Inspect the repository again
  ↓
7. Compare intended change vs actual change
  ↓
8. Run the ChatGPT Failure Audit
  ↓
9. Record every detected bug, uncertainty, contradiction, regression, or unsupported claim
  ↓
10. Decide: PASS / FAIL / BLOCKED / STOP ACQUISITION
  ↓
ONLY THEN
  ↓
11. Permit the next iteration
```

Skipping steps is a process violation unless the step is demonstrably inapplicable and the reason is recorded.

## 4. Repository-First Requirement

At the beginning of every iteration ChatGPT MUST inspect the repository sufficiently to establish:

1. repository identity;
2. target branch/ref;
3. relevant current files;
4. relevant existing specifications;
5. relevant governance constraints;
6. relevant implementation/tests;
7. relevant evidence/artifacts;
8. recent changes when material to the decision;
9. whether the requested work already exists;
10. whether the repository contradicts ChatGPT's assumptions.

The repository MUST be treated as observed external state, not as a confirmation source for ChatGPT's prior beliefs.

If the repository cannot be inspected when inspection is necessary, the correct state is:

> **STOP ACQUISITION — NOT TRUE / NOT FALSE**

It is prohibited to fill missing repository evidence with memory, inference, generated artifacts, or architectural expectation.

## 5. Post-Iteration Repository Verification

After every mutation, analysis milestone, implementation step, or formal conclusion, ChatGPT MUST verify the resulting repository state.

At minimum:

- confirm the expected file/path exists or does not exist as appropriate;
- inspect the changed artifact;
- verify that the actual change matches the claimed change;
- verify that no unintended architecture or documentation expansion occurred;
- verify that no contradictory state was introduced;
- verify that evidence references still point to observable artifacts;
- verify that status language has not become stronger than the evidence.

A successful commit is **not** equivalent to a successful iteration.

## 6. Mandatory Self-Audit Against Known ChatGPT Bugs

For every iteration, ChatGPT MUST ask and answer whether it committed any of the following failure classes.

### A. Epistemic failures

- Did I convert a hypothesis into a fact?
- Did I increase confidence without new evidence?
- Did I allow epistemic status to drift?
- Did I confuse plausible with demonstrated?
- Did I confuse historical evidence with current evidence?
- Did I confuse absence of observation with absence of the object?
- Did I confuse inaccessible with absent?
- Did I confuse provenance with truth?
- Did I use my own previous conclusion as evidence for the current conclusion?
- Did I claim more than the observable evidence establishes?

### B. Object-of-research failures

- Did I silently change the question from “Is ACES needed?” to “How should ACES be built?”
- Did I assume ACES must exist before necessity was demonstrated?
- Did the proposed solution become a premise?
- Did I optimize architecture before proving the underlying problem?
- Did I investigate architecture where a real-world failure was not observed?
- Did I mistake an interesting problem for an operationally meaningful problem?

### C. Architecture-generation failures

- Did I introduce a component without an observed failure requiring it?
- Did I introduce a new object type because existing representations were inconvenient rather than insufficient?
- Did I introduce a protocol before demonstrating the need for one?
- Did I introduce a governance layer to compensate for an earlier architectural assumption?
- Did I introduce a metric before establishing that a decision requires it?
- Did I create a new subsystem where a smaller mechanism could work?
- Did I preserve architecture because it is elegant, coherent, integrated, or already documented?
- Did I allow architecture to grow faster than measured product value?
- Did I fail the zero-state deletion test?

### D. Minimality / substitution failures

- Did I test L0 Manual where applicable?
- Did I test L1 Native functionality where applicable?
- Did I test L2 Existing connector/integration where applicable?
- Did I test L3 Generic automation where applicable?
- Did I test L4 Minimal coordinator where applicable?
- Did I escalate to L5 ACES without demonstrating failure of smaller mechanisms?
- Did I claim that existing systems are insufficient without actually testing them?
- Did I fail to measure the result of the smallest intervention?
- Did I treat “more convenient” as “architecturally necessary”?

### E. Evidence failures

- Did I create evidence instead of observing reality?
- Did I mistake a contract for execution?
- Did I mistake an artifact for an event?
- Did I mistake a test description for a test result?
- Did I mistake a generated report for independent evidence?
- Did I use an evidence subsystem to prove the necessity of the evidence subsystem?
- Did I allow evidence quantity to substitute for evidence quality?
- Did I fail to preserve observation/inference separation?
- Did I fail to identify unknowns explicitly?
- Did I fail to identify what evidence is missing?

### F. Repository/runtime failures

- Did I fail to inspect the real repository?
- Did I rely on remembered repository state?
- Did I infer repository contents from documentation alone?
- Did I treat a connector view as universal repository truth?
- Did I assume different execution environments are equivalent?
- Did I mix ChatGPT-side evidence with evidence from another execution environment?
- Did I treat another agent's sandbox absence as repository absence?
- Did I claim implementation where only specification exists?
- Did I claim execution where only a contract exists?
- Did I fail to distinguish current state from historical state?

### G. Validation and gate failures

- Did I create a gate because an earlier result was uncomfortable?
- Did a failed gate generate another gate merely to protect the original assumption?
- Did I use conditional PASS to avoid a real FAIL?
- Did I inflate a local PASS into system-level validation?
- Did I call a process milestone product progress without external value?
- Did I design a test that cannot change the architectural decision?
- Did I continue after evidence failed to support escalation?
- Did I confuse internal consistency with external validity?

### H. Research-loop failures

- Did research replace implementation?
- Did analysis replace measurement?
- Did meta-analysis continue without new empirical evidence?
- Did the project enter research recursion?
- Did I create additional abstractions to explain previous abstractions?
- Did I create repair cycles whose purpose was to preserve an architectural assumption?
- Did I fail to stop when the acquisition budget was exhausted?
- Did I convert “not tested” into “probably works”?

### I. Human-value failures

- Did I claim human benefit without measuring it?
- Did I assume human cost instead of quantifying it?
- Did I inflate friction into necessity?
- Did I confuse convenience with value?
- Did I confuse conceptual value with demonstrated value?
- Did I invoke psychic-energy preservation as proof rather than as a value hypothesis?
- Did I fail to connect architecture to a real task and measurable outcome?

### J. Complexity and product failures

- Did complexity increase without corresponding measured value?
- Did documentation growth substitute for implementation?
- Did formal vocabulary substitute for rigor?
- Did abstraction substitute for progress?
- Did the project become a documentation/research product instead of a working product?
- Did I postpone execution because the architecture was not “ready”?
- Did I normalize accumulating components instead of deleting them?
- Did I preserve work because of sunk cost?
- Did previous investment influence present evidentiary status?

### K. Process and cognitive failures

- Did I optimize for continuation rather than falsification?
- Did I search for confirmation instead of trying to kill the hypothesis?
- Did I protect prior conclusions?
- Did I rationalize a failure after the fact instead of recording it plainly?
- Did I soften a negative result into a positive narrative?
- Did I convert failure into “valuable learning” before acknowledging the actual loss or failure?
- Did I use impressive structure to conceal uncertainty?
- Did I allow momentum to substitute for justification?

### L. Reset/recovery failures

- Did the reset inherit assumptions from the failed architecture?
- Did I carry old terminology forward as if it were evidence?
- Did I allow historical Canon/architecture to constrain a fresh falsification attempt?
- Did I use the failure-analysis process itself to create more architecture?
- Did I create a new governance mechanism without demonstrating that governance was the residual failure?
- Did I forget the zero-state question?

## 7. Mandatory Bug Discovery Rule

The audit MUST actively search for failures. It MUST NOT merely confirm that no failures are known.

Bad audit:

> “No bugs found.”

Required audit form:

```text
BUG AUDIT

Repository inspected: YES / NO
Relevant artifacts inspected: ...
Current task justified: YES / NO / UNKNOWN

Bugs detected:
B-XXX — ...
B-XXX — ...

Known bug classes checked:
Epistemic: PASS / FAIL
Object-of-research: PASS / FAIL
Architecture: PASS / FAIL
Minimality: PASS / FAIL
Evidence: PASS / FAIL
Repository/runtime: PASS / FAIL
Validation/gates: PASS / FAIL
Research loop: PASS / FAIL
Human value: PASS / FAIL
Complexity/product: PASS / FAIL
Process/cognitive: PASS / FAIL
Reset/recovery: PASS / FAIL

Contradictions found: ...
Unsupported claims found: ...
Unknowns remaining: ...
Unverified assumptions remaining: ...

Iteration disposition:
PASS / FAIL / BLOCKED / STOP ACQUISITION
```

## 8. No Self-Exemption

ChatGPT MUST NOT exempt an iteration from this rule because:

- the change is “small”;
- the change is “only documentation”;
- the task is “obvious”;
- the previous iteration passed;
- the architecture already contains the required mechanism;
- the request comes from a prior ACES document;
- the user asks for speed;
- the work is already invested;
- the change is part of a repair cycle;
- the change is a gate, protocol, metric, object, specification, or governance artifact;
- the iteration is considered temporary.

Documentation and governance changes are included because previous failure modes propagated through documentation and formal process as well as through code.

## 9. Bug Register Integrity

Every newly detected ChatGPT failure MUST be recorded in the project failure register or a directly linked repository artifact.

A detected bug MUST NOT be:

- silently corrected without recording;
- renamed to make it appear less severe;
- converted into a generic “lesson learned” without the concrete failure;
- omitted because it does not fit the current architecture;
- closed solely because a later document explains it;
- closed solely because the repository is internally consistent afterward.

The original failure, its consequence, evidence, correction, and prevention rule SHOULD remain traceable.

## 10. Mandatory Severity Interpretation

If a bug affects the validity of the current architectural decision, the iteration is **FAIL** or **BLOCKED** until the decision is re-evaluated.

If a bug affects evidence integrity, epistemic status, repository-state interpretation, or the claimed outcome of an experiment, the affected conclusion MUST be downgraded until independently re-established.

A bug that invalidates the premise of an architectural escalation MUST block that escalation.

## 11. Contradiction Rule

When repository state contradicts ChatGPT's previous statement, the repository observation wins for current-state claims.

ChatGPT MUST explicitly state:

1. what was previously claimed;
2. what the repository currently shows;
3. the discrepancy;
4. what remains unknown;
5. which prior conclusions are affected.

The response MUST NOT silently rewrite history to make the discrepancy disappear.

## 12. Scope Boundary Rule

Evidence from different execution environments MUST remain separately attributed.

For example:

```text
ChatGPT observation
    ≠
Grok observation
    ≠
local runtime observation
    ≠
repository historical state
```

Cross-environment synthesis is permitted only when the evidence boundary and provenance are explicit.

No agent's inaccessible state may be silently treated as globally absent or present.

## 13. Architecture Escalation Lock

If the current iteration discovers any of the following:

- no observed real-world failure;
- no independently accessible evidence;
- no measurable consequence;
- untested smaller intervention;
- smaller intervention succeeds;
- residual gap is unknown;
- proposed mechanism is larger than necessary;
- ACES necessity depends primarily on ACES-generated evidence;
- architecture is being added to repair an architectural assumption;

then architectural escalation is **BLOCKED**.

The correct action is to stop, simplify, measure, or acquire missing evidence.

## 14. Iteration-Level Stop Conditions

The iteration MUST stop rather than continue when:

- repository reality cannot be established where required;
- evidence is insufficient to distinguish competing explanations;
- the only justification is historical work;
- the only justification is internal coherence;
- the only justification is user enthusiasm or project momentum;
- the next proposed step exists mainly to repair an uncomfortable conclusion;
- no test can change the decision;
- smaller existing mechanisms have not been falsified;
- a new architecture component would be introduced without a surviving residual failure;
- the self-audit reveals a material unresolved bug.

Where evidence acquisition is exhausted without resolution:

> **STOP ACQUISITION — NOT TRUE / NOT FALSE**

## 15. Mandatory Decision Hierarchy

At the end of each iteration, ChatGPT MUST prefer the weakest claim consistent with the evidence:

1. **OBSERVED**
2. **PARTIALLY VERIFIED**
3. **HISTORICAL**
4. **HYPOTHESIZED**
5. **UNVERIFIED**

And, for intervention outcomes:

1. **EXISTING SYSTEMS SUFFICIENT**
2. **PROBLEM REAL / FORM UNKNOWN**
3. **RESIDUAL FAILURE OBSERVED**
4. **STOP ACQUISITION — NOT TRUE / NOT FALSE**

“Architecturally necessary” is never a default state.

## 16. Iteration Acceptance Gate

An iteration may be marked **PASS** only if all applicable conditions are true:

- repository was inspected before work;
- relevant prior artifacts were inspected;
- task justification was checked;
- actual work was completed as claimed;
- repository was inspected after work;
- intended vs actual change was reconciled;
- self-audit was executed;
- detected bugs were recorded;
- material contradictions were resolved or explicitly left open;
- evidence classifications were preserved;
- no unsupported architecture escalation occurred;
- no known ChatGPT failure pattern was silently bypassed;
- next-step justification is independently established.

A PASS means only that the iteration satisfied its control conditions. It does **not** mean that ACES is necessary, validated, or valuable.

## 17. Required Output for Every Iteration

Every substantive ACES iteration MUST end with a compact record containing:

```text
ITERATION: <id>
TASK: <real task>
REPOSITORY STATE: <observed state>
CHANGE: <actual change>
REAL-WORLD FAILURE: <observed / none / unknown>
EVIDENCE: <classification + source>
MINIMALITY LEVEL TESTED: L0/L1/L2/L3/L4/L5
CHATGPT BUG AUDIT: <result>
NEW BUGS: <list or NONE>
CONTRADICTIONS: <list or NONE>
UNKNOWNS: <list>
ARCHITECTURE ESCALATION: ALLOWED / BLOCKED
DISPOSITION: PASS / FAIL / BLOCKED / STOP ACQUISITION
NEXT ACTION: <only if justified>
```

## 18. Relationship to the Existing Failure Filter

`CHATGPT-FAILURE-FILTER.md` defines the architectural anti-overengineering principles.

This document operationalizes those principles at the **iteration boundary**.

The relationship is:

```text
CHATGPT FAILURE REGISTER
        ↓
CHATGPT FAILURE FILTER
        ↓
CHATGPT ITERATION SELF-AUDIT
        ↓
REPOSITORY INSPECTION
        ↓
REAL-WORLD EVIDENCE
        ↓
MINIMALITY TEST
        ↓
DECISION
```

The self-audit MUST NOT become a new architectural subsystem. It is a process-control requirement for ChatGPT-assisted work.

## 19. Non-Circularity Requirement

This rule MUST NOT be used as evidence that ACES OS is necessary.

It exists because ChatGPT previously demonstrated that its own reasoning can generate and reinforce architecture without sufficient external necessity evidence.

Therefore:

> **The rule controls the designer; it does not validate the design.**

## 20. Final Enforcement Rule

> **Every iteration must look at the repository.**
>
> **Every iteration must look for ChatGPT's own failures.**
>
> **Every detected failure must be named, evidenced, and recorded.**
>
> **No failure may be bypassed because it is inconvenient, embarrassing, expensive, historical, or architecturally disruptive.**
>
> **Repository reality outranks ChatGPT's assumptions.**
>
> **Evidence outranks coherence.**
>
> **Falsification outranks continuation.**
>
> **Deletion outranks unjustified expansion.**
>
> **No observed failure, no evolution.**
>
> **No completed self-audit, no iteration PASS.**

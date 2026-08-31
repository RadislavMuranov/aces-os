# E1 Authorization Package

**Status:** PREPARED FOR HUMAN / CANONICAL REVIEW — **NOT STARTED**  
**This document is not authorization.**  
**Date:** 2026-08-31

---

## Proposed objective

```text
E1 — EVOLUTION CONTROL BASELINE
```

Establish a **controlled experimental baseline** for evaluating whether and when project scaffolding (CLAUDE.md, Skills, Hooks) is justified — **without assuming any are necessary**.

---

## Central principle (candidate)

```text
OBSERVED FAILURE
  → CANDIDATE CONTROL
  → CONTROLLED TEST
  → ABLATION
  → OBSERVATION
  → EVIDENCE
  → DECISION
  → AUTHORIZED PROMOTION
```

---

## E1 must NOT start with scaffolding

Do **not** immediately create:

- CLAUDE.md  
- `.claude/skills/`  
- hooks  
- project rules / automatic prompts  
- new protocols as Canon  

First: baseline against which scaffolding can be measured.

---

## Baseline questions (measurement)

1. What failure occurred?  
2. What was model behavior **without** scaffolding?  
3. What intervention is proposed?  
4. Which exact failure does it target?  
5. What is the **minimum** intervention?  
6. Does CLAUDE.md improve context fidelity?  
7. Does a Skill improve repeatable task execution?  
8. Does a Hook enforce a runtime invariant?  
9. What new failure modes does the intervention introduce?  
10. Does it remain necessary after model/tool evolution?  
11. Can it be removed without degradation?  
12. What evidence is required for promotion to canonical/project status?

---

## Scaffolding taxonomy — **E1 CANDIDATE MODEL** (falsifiable, not Canon)

```text
FACT        → CLAUDE.md   = stable project/context facts
WORKFLOW    → SKILL       = reusable capability/workflow
ENFORCEMENT → HOOK        = runtime enforcement
```

Authority remains **above** project scaffolding.

---

## Project-local materialization — **candidate pattern only**

Proposed layout ( **DO NOT CREATE in E1 package acceptance alone** ):

```text
.claude/
  skills/
    <skill-name>/
      SKILL.md
      references/
      scripts/
      examples/
```

Candidate Skill contract fields: name, description/triggers, Goal, Invariants, Evidence, Required output, Gotchas.

---

## CLAUDE.md candidate sections (context, not authority)

Project · Repository · Architecture · Verification · Permanent Conventions · Non-Negotiable Rules · Critical Safety Constraints  

**CLAUDE.md = context, not authority.**

---

## Hook candidate model (not implemented)

Hook requires: explicit trigger · invariant · scope · failure behavior · observable result · bypass/override policy · auditability.

---

## Ablation protocol (candidate lifecycle)

```text
BASELINE → SCAFFOLD → OBSERVE → ABLATE → COMPARE → DECIDE
```

Scaffold must not become permanent merely by appearing useful; measurable necessity required.

---

## Model evolution principle (E1 experimental hypothesis — not Canon)

```text
OLD MODEL → old corrections/prompts/skills/hooks/assumptions
  → MODEL CHANGES → ABLATION → REMOVE SCAFFOLDING
  → OBSERVE ACTUAL BEHAVIOR → IDENTIFY REAL FAILURES
  → REINTRODUCE ONLY NECESSARY CONTROL
```

---

## Authority boundary (non-negotiable)

```text
Human / Canonical Authority
  → Master Control Protocol
  → Evolution Control
  → Evidence
  → Decision
  → Authorized Construction
```

**Never:** Evolution Engine → self-authorize → modify Canon.

---

## E1 success criteria

- Baseline reproducible  
- Scaffolding categories operationally distinguishable  
- Ablation performable  
- Evidence capturable  
- Interventions comparable  
- Promotion/rejection explicit  
- No self-authorizing mutation  
- No new architecture without observed failure  

Documents alone ≠ E1 complete.

---

## Open E0 unknowns carried into E1 review

SCE UNKNOWN · G1' not implemented · G2 unresolved · G3 not found · multi-branch evidence model.

---

## Authorization request (for Human/Canonical Authority)

Approve or reject opening **E1 — Evolution Control Baseline** as an **experimental governance program** under the constraints above.  
**Approval of this package ≠ approval of any specific Skill/Hook/CLAUDE.md file.**

**E1 NOT STARTED until explicit authorization.**

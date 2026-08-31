# ACES OS — EVOLUTION BRANCH PROTOCOL

**Status:** CANDIDATE  
**Date:** 2026-08-31  
**Branch:** `evolution/e0-branch-protocol`  
**Authority:** Proposed process rule for ACES OS evolution; not yet Canonical.

---

## 1. Purpose

Establish a repeatable, evidence-preserving process for every evolutionary step of ACES OS so that history remains reproducible and each change is isolatable.

A Git branch under this protocol is not merely a technical branch.  
It is an **immutable-ish evidence boundary** of a single evolutionary step: what was proposed, what was verified, what changed, what was rejected, and why.

---

## 2. Canonical Lifecycle of an Evolutionary Step

```
EACH EVOLUTIONARY STEP
        ↓
separate branch
        ↓
only changes belonging to this step
        ↓
verification
        ↓
evidence / decision
        ↓
PR
        ↓
Human / Canonical Gate
        ↓
merge (or reject)
```

---

## 3. Naming Convention

```
evolution/
├── e0-corpus-archaeology
├── e0.3-historical-reconstruction
├── e0.4-canon-reconciliation
├── e0.5-conflict-analysis
├── e0-gate
├── e1-foundation
├── e2-context
├── e3-skills
├── e4-hooks
├── ...
└── next-evolution
```

Rules:
- Prefix `evolution/` is mandatory for evolutionary work.
- One step identifier per branch.
- Step identifiers are sequential and descriptive of the hypothesis or stage.

---

## 4. Hard Rules

1. **One evolutionary branch = one verifiable hypothesis / stage.**  
   Do not mix multiple independent evolutionary decisions in a single PR.

2. **Branch content is limited to the scope of that step.**  
   No opportunistic refactoring, no silent promotion of other candidates.

3. **Evidence and decision must be recorded inside the branch**  
   (report, ledger entry, verification artifacts) before any merge request.

4. **Merge requires Human / Canonical Gate.**  
   Autonomous systems may observe, analyze, propose, test, measure.  
   They may not silently promote to Canonical architecture.

5. **Rejected steps remain recoverable.**  
   Closed / rejected branches are part of the Evolution Ledger; they are not erased.

6. **Protected canonical artifacts** continue to be governed by the Master Control Protocol / Master Protocol and may not be modified solely by an evolution branch without the defined authority path.

---

## 5. Relationship to Existing Mechanisms

| Concern | Mechanism |
|---------|-----------|
| FACT / permanent context | CLAUDE.md / Rules |
| WORKFLOW | Skill |
| ENFORCEMENT | Hook |
| EVOLUTIONARY CHANGE | **This protocol (branch + gate)** |
| AUTHORITY | Master Protocol / Canonical Gate |

This protocol does not replace the Ablation Principle, Reality-precedes-canon, or protected-invariant rules. It supplies the **process boundary** that makes those principles auditable over time.

---

## 6. Evolution Ledger Consequence

Over time the set of `evolution/*` branches (merged and rejected) forms a reproducible Evolution Ledger:

- what was attempted,
- under which hypothesis,
- with which evidence,
- with which outcome.

Linear main-line history alone is insufficient for this purpose.

---

## 7. Current Application

| Step | Branch | Status |
|------|--------|--------|
| E0.2 Corpus Archaeology | `evolution/e0-corpus-archaeology` | EXISTS (commit eeabef3…) |
| Evolution Branch Protocol itself | `evolution/e0-branch-protocol` | THIS BRANCH (CANDIDATE) |
| E0.3 Historical Reconstruction | `evolution/e0.3-historical-reconstruction` | NEXT (not yet created) |

---

## 8. Promotion Criteria

This protocol becomes ACTIVE / Canonical only after:

- explicit Human / Canonical Gate acceptance,
- consistency check against Master Protocol and existing evolution foundation,
- confirmation that it does not introduce unnecessary scaffolding.

Until then it remains **CANDIDATE**.

---

## 9. Governing Principle

> One evolutionary branch = one verifiable hypothesis/stage.  
> Branch = evidence boundary.  
> Reality precedes canon.

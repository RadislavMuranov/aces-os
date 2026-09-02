# P1 Domain Reconciliation Policy Pack

**Gate:** P1 Domain Reconciliation Policy Pack  
**Branch:** `architecture/p1-domain-reconciliation-policy`  
**Base:** `bd4d2380a054b8a4974a15c119f048a9ac546fd2`  
**Kind:** Policy / contract only — **NOT** implementation

## Contents

| File | Role |
|------|------|
| `P1-DOMAIN-RECONCILIATION-POLICY-v1.0.md` | Canonical policy object, lifecycle, defaults, hierarchy |
| `P1-CONFLICT-TAXONOMY.md` | Conflict classes |
| `P1-POLICY-MATRIX.md` | Six-provider minimum coverage |
| `P1-RESOLUTION-RECORD-SPEC.md` | ResolutionRecord schema |
| `P1-RECONCILIATION-ADVERSARIAL-SCENARIOS.md` | T1–T10 |
| `P1-DOMAIN-RECONCILIATION-POLICY-GATE-DECISION.md` | Gate decision |

## Immutable rule

```text
Reconciliation Result ≠ Truth
Digital World State ≠ Semantic Reality
No implicit latest-wins / first-wins / provider-wins
```

## Non-claims

No Reconciliation Engine code, connectors, SDKs, merge, main mutation, Canon Promotion, or Vertical Slice Implementation.

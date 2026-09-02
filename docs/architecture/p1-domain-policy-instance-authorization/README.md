# P1 Domain Policy Instance Authorization Pack

**Gate:** P1 Domain Policy Instance Authorization  
**Branch:** `architecture/p1-domain-policy-instance-authorization`  
**Base:** `b8fc7c8e759c0694860e7eb2fb43333a18777909`  
**Kind:** Documentation / authorization metadata only — **NOT** runtime

## Contents

| File | Role |
|------|------|
| `P1-DOMAIN-POLICY-INSTANCE-AUTHORIZATION-v1.0.md` | Instance model, lifecycle, composition, boundaries |
| `P1-POLICY-INSTANCE-CATALOG.md` | Concrete candidate instances |
| `P1-POLICY-INSTANCE-MATRIX.md` | Six-provider matrix |
| `P1-POLICY-INSTANCE-APPROVAL-RECORD-SPEC.md` | ApprovalRecord schema |
| `P1-POLICY-INSTANCE-ADVERSARIAL-TESTS.md` | A1–A12 |
| `P1-DOMAIN-POLICY-INSTANCE-AUTHORIZATION-GATE-DECISION.md` | Gate decision |

## Critical

```text
ACTIVE = authorized for future Reconciliation Engine use
ACTIVE ≠ Truth
Policy Instance ≠ ACES Authority / ASA / AcceptedState / Knowledge
```

No connector implementation, no provider API calls, no merge, no Canon Promotion.

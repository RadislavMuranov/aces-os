# P1 Human/Canonical ApprovalRecord Issuance Pack

**Gate:** P1 Human/Canonical ApprovalRecord Issuance  
**Branch:** `architecture/p1-human-canonical-approvalrecord-issuance`  
**Base:** `5f2133290f7c768ca886c1d6055dc54e696644ff`  
**Kind:** Authorization documentation only — **NOT** runtime, **NOT** Canon

## Contents

| File | Role |
|------|------|
| `P1-HUMAN-CANONICAL-APPROVALRECORD-ISSUANCE-v1.0.md` | Model, lifecycle, boundaries |
| `P1-APPROVALRECORD-CATALOG.md` | Eligibility per Policy Instance |
| `P1-APPROVALRECORD-MATRIX.md` | Provider coverage matrix |
| `P1-APPROVALRECORD-ISSUANCE-RULES.md` | Eligibility, digest, scope, temporal |
| `P1-APPROVALRECORD-ADVERSARIAL-TESTS.md` | A1–A15 |
| `P1-HUMAN-CANONICAL-APPROVALRECORD-ISSUANCE-GATE-DECISION.md` | Gate decision |

## Non-collapse

```text
Candidate ≠ Approved ≠ Active Policy Instance
  ≠ PolicyInstanceApprovalRecord
  ≠ Runtime authorization
  ≠ Execution AuthorizationRecord
```

```text
Policy Approval ≠ Execution Authorization
Policy Activation ≠ AcceptedState
```

# P1 ApprovalRecord Adversarial Tests A1–A15

| ID | Scenario | Expected |
|----|----------|----------|
| **A1** | Incomplete scope | REJECT |
| **A2** | Missing digest | REJECT |
| **A3** | Mismatched policy_digest | INVALID |
| **A4** | Mismatched instance_digest | INVALID |
| **A5** | Before effective_from | NOT_ACTIVE |
| **A6** | After effective_until | INACTIVE |
| **A7** | Superseded | INACTIVE |
| **A8** | Revoked | INACTIVE |
| **A9** | PVR marked VERIFIED | REJECT |
| **A10** | Provider-wide used globally | REJECT |
| **A11** | Used as execution authorization | REJECT |
| **A12** | Creates AcceptedState | REJECT |
| **A13** | Overlapping approvals no resolution | POLICY_CONFLICT |
| **A14** | Same id/version different digest | APPROVAL_DIGEST_MISMATCH |
| **A15** | Scope expansion without re-approval | REJECT |

**Spec-level result:** All encoded in Issuance Rules + Issuance v1.0 → **PASS**.

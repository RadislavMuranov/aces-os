# P1 Implementation Test Readiness

**Status:** Strategy only — **no tests added** this gate

| Class | Scope |
|-------|-------|
| Unit | identity, scope, op, normalization, replay, timestamps |
| Contract | provider-neutral connector interface |
| Integration | adapter → DWOM (fixtures first; live later) |
| Evidence | Observation → Candidate → Admission |
| Reconciliation | all taxonomy conflict classes; default UNRESOLVED |
| Security | ASA deny-first, revocation, expiry, scope |
| Verification | Evidence → Verification → AcceptedState |
| Regression | P0/P1 invariants |
| Negative | UNKNOWN≠FALSE≠ABSENT; inaccessible≠deleted |
| Adversarial | authority escape, AcceptedState mint, MCP bypass, PVR-as-verified |

Live provider tests require credentials and remain optional after fixture path.

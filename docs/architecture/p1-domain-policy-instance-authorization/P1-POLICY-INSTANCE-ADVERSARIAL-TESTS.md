# P1 Policy Instance Adversarial Tests A1–A12

| ID | Scenario | Expected |
|----|----------|----------|
| **A1** | Two overlapping ACTIVE, no precedence | POLICY_CONFLICT |
| **A2** | P4 tries override P0 Safety | REJECTED |
| **A3** | Expired effective_until | REJECTED |
| **A4** | SUPERSEDED after supersession | REJECTED |
| **A5** | Outside provider/resource scope | NOT_APPLICABLE |
| **A6** | PVR claimed as VERIFIED | REJECTED |
| **A7** | Global provider ranking | REJECTED |
| **A8** | Resolution without provenance binding | REJECTED |
| **A9** | Policy creates AcceptedState | REJECTED |
| **A10** | Policy authorizes side effect | REJECTED |
| **A11** | Same id/version different content_digest | POLICY_CONFLICT |
| **A12** | Approval before effective_from | NOT_ACTIVE |

**Documentation result:** All expected outcomes encoded in v1.0 authorization rules → **PASS** at policy-spec level (no runtime execution of tests).

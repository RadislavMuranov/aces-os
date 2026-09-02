# P1 ApprovalRecord Issuance Rules

## 1. Eligibility (all required)

Instance is **NOT_ELIGIBLE** if any missing:

1. complete schema · 2–5 explicit scopes (incl. provider/resource/field) · 6 identity level · 7 comparison · 8 precedence or explicit no-resolve · 9 temporal · 10 staleness · 11 partial · 12 deletion/existence · 13 version/revision · 14 conflict · 15 resolution authority · 16 provenance · 17 effective interval · 18 digests bound · 19 no PVR→VERIFIED · 20 no authority escape.

## 2. PVR rule

Instances depending on Obsidian Sync/plugins, Slack retention/Grid, Drive shared-drive edges, Kaiten webhook completeness:

- **MAY** be approved only as **APPROVABLE_WITH_PVR_GUARD** (property treated UNKNOWN/PARTIAL/PVR in instance text), or  
- **NOT_ELIGIBLE_PENDING_LIVE_VERIFICATION**  

**MUST NOT** receive approval that claims those facts VERIFIED.

## 3. Digest binding

```text
ApprovalRecord.policy_digest == current Policy body digest
ApprovalRecord.instance_digest == current PolicyInstance body digest
```

Mismatch → **APPROVAL_DIGEST_MISMATCH** / inactive. Same id+version different digest → invalidation + re-approval.

## 4. Scope binding

Out-of-scope use → **NOT_APPLICABLE** / **DENIED_BY_SCOPE**. Narrow approval is never global.

## 5. Temporal binding

| Condition | Result |
|-----------|--------|
| before effective_from | NOT_ACTIVE |
| after effective_until | INACTIVE |
| superseded / revoked | INACTIVE |
| overlapping incomparable ACTIVE | POLICY_CONFLICT |
| renewal | New ApprovalRecord |

No implicit indefinite approval. No “latest wins” unless encoded as scoped policy rule.

## 6. Classification labels

| Label | Meaning |
|-------|---------|
| APPROVABLE | Eligible; digests/scopes complete; no PVR dependency |
| APPROVABLE_WITH_PVR_GUARD | Eligible only with explicit PVR/UNKNOWN treatment |
| NOT_ELIGIBLE_PENDING_LIVE_VERIFICATION | Needs live verification before approval |
| DEFERRED | Intentionally not issued this gate |

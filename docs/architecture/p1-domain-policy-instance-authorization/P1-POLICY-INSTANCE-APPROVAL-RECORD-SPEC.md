# P1 PolicyInstanceApprovalRecord Spec

Authorization **metadata** for a policy instance. **Does not** authorize execution side effects.

## Mandatory fields

| Field | Notes |
|-------|-------|
| `approval_id` | Durable |
| `policy_id` | |
| `policy_version` | |
| `scope` | Must match instance |
| `policy_hash` / `content_digest` | Of canonical instance body |
| `approver` | Principal |
| `approval_authority` | Role/governance path |
| `approval_timestamp` | |
| `effective_from` / `effective_until` | |
| `approval_reason` | |
| `evidence_refs` | Spec/verification docs |
| `supersedes` | Optional |
| `status` | ISSUED\|REVOKED |

## Rules

- ACTIVE instance without matching ApprovalRecord → **invalid**
- Digest mismatch same id/version → **POLICY_CONFLICT**
- effective_from in future → **NOT_ACTIVE**
- After effective_until or REVOKED → **REJECTED** for use

# P1 Provider Implementation Readiness Matrix

**Legend:** READY · READY-WITH-CONSTRAINT · BLOCKED-PVR · BLOCKED-AUTHORIZATION · BLOCKED-CONTRACT · DEFERRED · NOT-APPLICABLE

| Capability | Obsidian | GitHub | Slack | Gmail | Drive | Kaiten |
|------------|----------|--------|-------|-------|-------|--------|
| Connector identity | READY | READY | READY | READY | READY | READY |
| Connector capability map | READY | READY | READY | READY | READY | READY |
| Resource identity | READY-WITH-CONSTRAINT (path+epoch) | READY (SHA/ids) | READY (ch+ts) | READY (msg id) | READY (fileId) | READY (int ids) |
| Resource scope / namespace | READY | READY | READY | READY | READY | READY |
| READ / OBSERVE | READY-WITH-CONSTRAINT | READY-WITH-CONSTRAINT | READY-WITH-CONSTRAINT | READY-WITH-CONSTRAINT | READY-WITH-CONSTRAINT | READY-WITH-CONSTRAINT |
| CREATE | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION |
| UPDATE | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION |
| DELETE | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION | BLOCKED-AUTHORIZATION |
| EXECUTE | NOT-APPLICABLE / DEFERRED | DEFERRED (workflows) | NOT-APPLICABLE | NOT-APPLICABLE | NOT-APPLICABLE | NOT-APPLICABLE |
| Observation | READY | READY | READY | READY | READY | READY |
| EvidenceCandidate | READY | READY | READY | READY | READY | READY |
| Evidence Admission | READY-WITH-CONSTRAINT (ApprovalRecord) | same | same | same | same | same |
| Reconciliation | READY-WITH-CONSTRAINT (ACTIVE policies) | same | same | same | same | same |
| DWS projection | READY | READY | READY | READY | READY | READY |
| Provenance structural | READY | READY | READY | READY | READY | READY |
| Replay binding | READY | READY | READY | READY | READY | READY |
| Partial observability | READY | READY | READY | READY | READY | READY |
| Temporal semantics | READY | READY | READY | READY | READY | READY |
| Deletion semantics | READY | READY | READY | READY | READY | READY |
| Version/revision | READY-WITH-CONSTRAINT (hash) | READY | READY-WITH-CONSTRAINT | READY | READY | READY-WITH-CONSTRAINT |
| Conflict semantics | READY (default UNRESOLVED) | READY | READY | READY | READY | READY |
| Policy instance catalog | READY | READY | READY | READY | READY | READY |
| Physical ApprovalRecord | BLOCKED-AUTHORIZATION | same | same | same | same | same |
| ASA prerequisite (writes) | BLOCKED-AUTHORIZATION | same | same | same | same | same |
| Verification / AcceptedState | READY-WITH-CONSTRAINT (Axis-C; G2-R1 BLOCKED env) | same | same | same | same | same |
| PVR surface | BLOCKED-PVR (OBS-SYNC) or avoid | — | BLOCKED-PVR (SL-RET) or avoid | — | BLOCKED-PVR (GD-SD) or avoid | BLOCKED-PVR (KT-WH) or avoid |
| Native/CLA path | Local FS preferred | REST/GraphQL/git | Web API | Gmail API | Drive API | REST |
| MCP necessity | Only if local inadequate | Only if native inadequate | same | same | same | same |

### Constraint names (READY-WITH-CONSTRAINT)

1. **Credentials / environment** — no live tokens in architecture session  
2. **Physical ApprovalRecord not issued** — process PASS; issuance pending  
3. **PVR guard** — must avoid Sync/retention/shared-drive/webhook-complete semantics or treat as UNKNOWN  
4. **G2-R1** — verification-closure environment still BLOCKED for live Knowledge claims  

### READ constraint (all six)

```text
READY-WITH-CONSTRAINT =
  contracts sufficient for read-only adapter design
  + must not claim Sync/retention/shared-drive/webhook-complete semantics as verified
  + physical ApprovalRecord required before ACTIVE policy-driven reconciliation resolve
  + credentials required for real integration tests
```

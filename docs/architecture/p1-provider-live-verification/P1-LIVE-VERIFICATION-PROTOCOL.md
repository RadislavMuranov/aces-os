# P1 Live Verification Protocol

## Pre-test record (required per property)

| Field | Required |
|-------|----------|
| verification_id | YES |
| provider | YES |
| semantic property | YES |
| hypothesis | YES |
| exact test procedure | YES |
| expected observable behavior | YES |
| actual observable behavior | YES |
| observation timestamp | YES |
| provider/resource identifier | YES |
| operation performed | YES |
| request correlation | YES |
| evidence reference | YES |
| evidence provenance | YES |
| verifier | YES |
| verification status | YES |
| limitations | YES |
| reproducibility | YES |

## Constraints

- No production data alteration
- Prefer disposable resources, read-only, sandbox, reversible ops
- If mutation unavoidable → STOP unless separately authorized
- Scope every result to tested configuration — not universal provider law
- Negative tests: absence≠deletion; inaccessible≠nonexistent; path≠identity; arrival≠source order; API success≠semantic acceptance; webhook receipt≠exactly-once

## When access unavailable

```text
REPRODUCTION BLOCKED — PROVIDER ACCESS UNAVAILABLE
verification_status = UNVERIFIED | PVR
Do not fail the architecture hypothesis solely due to access absence.
```

## Planned procedures (for future authorized run)

### LV-OBS-SYNC-001
Hypothesis: Sync multi-device may produce conflicting mtime/path without stable content id.  
Procedure: Two vaults/devices with Sync (if available); rename/move/delete disposable note; record local paths, mtimes, content hashes.  
Expected: correlation needs content hash + epoch; not path alone.  
This run: **NOT EXECUTED**.

### LV-SL-RET-001
Hypothesis: Retention/Grid may hide history; deleted≠not visible.  
Procedure: Read-only history of disposable channel messages; observe edit/delete events if present.  
This run: **NOT EXECUTED**.

### LV-GD-SD-001
Hypothesis: Shared-drive permission edges differ; inaccessible≠absent.  
Procedure: Read-only list/get on disposable shared-drive file if accessible.  
This run: **NOT EXECUTED**.

### LV-KT-WH-001
Hypothesis: Webhook delivery not proven exactly-once from one event.  
Procedure: Observe webhook payloads for disposable card updates if endpoint available.  
This run: **NOT EXECUTED**.

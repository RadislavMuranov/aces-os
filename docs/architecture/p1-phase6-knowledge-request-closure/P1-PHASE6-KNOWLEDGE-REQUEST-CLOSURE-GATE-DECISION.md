# P1 Phase VI Knowledge Request Closure — Gate Decision

**Gate:** P1 Phase VI — Targeted Closure: KnowledgeUpdateRequest / request_id  
**Date:** 2026-09-03  
**Branch:** `implementation/p1-phase6-knowledge-request-closure`  
**Base SHA:** `08acc2445f6ab6d274d8579c3ec918d18c9e428b`  
**Decision:** **PASS** (Variant A)

---

## Variant chosen: A

`KnowledgeUpdateRequest` is the **mandatory** promotion boundary input.

```text
ESTABLISHED AcceptedState + PASSED VerificationResult + Evidence
        +
KnowledgeUpdateRequest (required)
        ↓
validation (request ↔ AcceptedState ↔ Evidence ↔ Result)
        ↓
KnowledgeObject
```

`promote(None, ...)` → reject.  
`promote_without_request()` → reject.  
No parameter-only alternate authority path.

## request_id semantics

| Concept | Role |
|---------|------|
| `request_id` | Identifies the *promotion request* (replay / conflict on reuse) |
| Knowledge identity | `accepted_state_id \| evidence_digest \| object_type \| semantic_identity` |
| Authority | AcceptedState + VerificationResult + Evidence — **not** request_id |

- Same `request_id` + same fingerprint → same KnowledgeObject  
- Same `request_id` + different content → KnowledgeConflictError  
- Different `request_id` + same Knowledge identity + same payload → same KnowledgeObject (no duplicate)  
- `request_id` is **not** part of canonical Knowledge identity  

## Scope

Only `src/aces_os/knowledge/*`, `tests/test_knowledge_promotion.py`, this decision doc.

## Tests (truthful)

| Item | Status |
|------|--------|
| Published methods | **20** in `test_knowledge_promotion.py` |
| Full unittest discover (private clone) | **NOT EXECUTED** |
| Full regression PASS claim | **NOT MADE** |

## Findings

CRITICAL 0 · HIGH 0 · MEDIUM 0  
Residuals: crypto DEFERRED; Canonical needs separate authority; Phase VII unauthorized.

## Safety

main `b2f8b4265e13793b89a3fa718d0c707fb2cc816b` UNTOUCHED · Canon NOT PROMOTED · Phase VII UNAUTHORIZED · MCP/DSH/Orca NOT USED

## Next authorized gate

Separate Human/Canonical instruction required — not auto-started.

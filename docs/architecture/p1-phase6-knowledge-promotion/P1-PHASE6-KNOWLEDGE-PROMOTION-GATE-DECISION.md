# P1 Phase VI Knowledge Promotion — Gate Decision

**Gate:** P1 Phase VI — Knowledge Promotion / Knowledge Update  
**Date:** 2026-09-03  
**Branch:** `implementation/p1-phase6-knowledge-promotion`  
**Base SHA:** `966af7ddcdfe46eb36da49775ab2bd59f222a3d3`  
**Decision:** **PASS**

---

## Scope

```text
AcceptedState (ESTABLISHED) → KnowledgeUpdateRequest → KnowledgeObject
STOP. No Memory / World Model / Semantic Reality / Authorization.
```

## Artifacts

| Path | Role |
|------|------|
| `src/aces_os/knowledge/model.py` | Types, TruthLevel, Provenance, identity key |
| `src/aces_os/knowledge/store.py` | Full-identity index (not evidence_id-only) |
| `src/aces_os/knowledge/service.py` | Promotion + validation + non-capabilities |
| `tests/test_knowledge_promotion.py` | Adversarial A–AA |

Dependencies: **none** (stdlib).

## Binding

Requires ESTABLISHED AcceptedState + PASSED VerificationResult + exact:

- evidence_id / evidence_digest
- verification_result_id
- policy_id / policy_version
- verifier_id / verifier_version

Bare `verified=True` / `passed=True` **rejected**.  
Canonical truth **cannot** be promoted in Phase VI.

## Identity / idempotency

```text
knowledge_identity =
  accepted_state_id + evidence_digest + object_type + semantic_identity
```

Same identity → same KnowledgeObject. Payload/truth conflict → KnowledgeConflictError.

## Provenance

KnowledgeObject → AcceptedState → VerificationResult → Verifier → Evidence → Candidate → Observation → Connector → Provider  
Crypto: **DEFERRED**

## Tests (truthful)

| Item | Status |
|------|--------|
| Published methods in `test_knowledge_promotion.py` | **20** |
| Full `unittest discover` on private clone | **NOT EXECUTED** |
| Full regression PASS claim | **NOT MADE** |

## Findings

CRITICAL: 0 · HIGH: 0 · MEDIUM: 0  
Residuals: no crypto authenticity; Canonical requires future gate; Memory/WM not implemented (explicitly out of scope).

## Safety

- main: `b2f8b4265e13793b89a3fa718d0c707fb2cc816b` **UNTOUCHED**  
- Canon: **NOT PROMOTED**  
- Phase VII: **UNAUTHORIZED**  
- MCP / DSH / Orca: **NOT USED**

## Next authorized gate

Requires separate Human/Canonical instruction (e.g. Phase VII Memory) — **not** auto-started.

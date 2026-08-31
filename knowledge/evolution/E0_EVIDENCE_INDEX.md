# E0 Evidence Index

**Purpose:** Make the multi-branch E0 archive auditable.  
**Rule:** Logical E0 sequence ≠ Git ancestry.  
**E0.4–E0.8 = independent evidence branches** from a shared main tip.

---

## Shared base

| Item | Value |
|------|--------|
| **main** | `4868e57bf9f19e29f5d152669e222feecf60e565` |

All E0.4–E0.9 evolution branches listed below were created from this tip (unless noted).

---

## E0.4 — Canon Reconciliation

| Field | Value |
|-------|--------|
| Branch | `evolution/e0.4-canon-reconciliation` |
| HEAD | `50aaaa6be1acbc6256c9d6d2b84bced6f2ae4831` |
| Parent/base | `4868e57bf9f19e29f5d152669e222feecf60e565` |
| Artifacts | `knowledge/evolution/E0.4_CANON_RECONCILIATION.md`, `E0.4_DECISION.md` |
| Decision | NO NEW ARCHITECTURE; G1 process/contract candidate |
| Verdict | **PASS** (PARTIAL/UNKNOWN on SCE file location) |

---

## E0.5 — Duplication / Conflict Analysis

| Field | Value |
|-------|--------|
| Branch | `evolution/e0.5-duplication-conflict-analysis` |
| HEAD | `1e924ac26735b729ce3514204b8fc466ea9ee9ca` |
| Parent/base | `4868e57bf9f19e29f5d152669e222feecf60e565` |
| Artifacts | `knowledge/evolution/E0.5_DUPLICATION_CONFLICT_ANALYSIS.md`, `E0.5_DECISION.md` |
| Decision | G1 = MINIMAL ENFORCEMENT GAP; NO NEW ARTIFACT |
| Verdict | **PASS / PARTIAL** (SCE UNKNOWN) |

---

## E0.6 — SCE Runtime Resolution

| Field | Value |
|-------|--------|
| Branch | `evolution/e0.6-sce-runtime-resolution` |
| HEAD | `a8d1caf7a1b026257c6dd1cc8a09df2f9d594625` |
| Parent/base | `4868e57bf9f19e29f5d152669e222feecf60e565` |
| Artifacts | `knowledge/evolution/E0.6_SCE_RUNTIME_RESOLUTION.md`, `E0.6_DECISION.md` |
| Decision | Exact SCE Spec v1.0 NOT FOUND; no reconstruction-as-canon |
| Verdict | **BLOCKED** (insufficient evidence re SCE text) |

---

## E0.7 — Evidence Closure + E0 Final Gate

| Field | Value |
|-------|--------|
| Branch | `evolution/e0.7-evidence-closure` |
| HEAD | `b6df5e1a10d52e6763421e5e353c722d0fbc09e8` |
| Parent/base | `4868e57bf9f19e29f5d152669e222feecf60e565` |
| Artifacts | `knowledge/evolution/E0.7_EVIDENCE_CLOSURE.md`, `E0.7_DECISION.md` |
| Decision | Gate closed with explicit UNKNOWN; E1 not started |
| Verdict | **PASS WITH EXPLICIT UNKNOWN** |

---

## E0.8 — Evidence / Git Lineage Integrity Audit

| Field | Value |
|-------|--------|
| Branch | `evolution/e0.8-evidence-lineage-audit` |
| HEAD | `f367b99aa7db2845a7209603b95c0dab1ccefc87` |
| Parent/base | `4868e57bf9f19e29f5d152669e222feecf60e565` |
| Artifacts | `knowledge/evolution/E0.8_EVIDENCE_LINEAGE_AUDIT.md`, `E0.8_DECISION.md` |
| Decision | Independent branches verified; traceability caveat |
| Verdict | **VERIFIED WITH LINEAGE CAVEAT** |

---

## Related (not E0.4–E0.8, referenced)

| Branch | HEAD (tip) | Note |
|--------|------------|------|
| `evolution/e0.3-historical-reconstruction` | `381edf07c20f6b4906483d4a63d9f3ecc88105bb` | Multi-commit branch; E0.3 PASS PARTIAL |
| `evolution/ecp-001-evolution-conservation` | `d77d2e152b166abe70f912d220b4a496e6687e0f` | ECP-001 CANDIDATE |

---

## How to audit

1. Check out each branch HEAD by SHA.  
2. Confirm listed artifacts exist.  
3. Confirm diffs are governance-only under `knowledge/evolution/`.  
4. Do **not** expect prior stage files inside a later stage branch tree.

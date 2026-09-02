# P1 Phase IV Evidence Admission — Gate Decision

**Gate:** P1 Phase IV — EvidenceCandidate / Evidence Admission  
**Date:** 2026-09-03  
**Branch:** `implementation/p1-phase4-evidence-admission`  
**Base:** `1b6b340ac0645693daa441e320ede3bdafdaa7ca`  
**Decision:** **PASS**

---

## Boundary

```text
Observation + DWOM → EvidenceCandidate → admit() → Evidence
STOP. No Verification / AcceptedState / Knowledge.
```

**ADMITTED** means structural admission requirements met — **not** truth, verification, or acceptance.

---

## Artifacts

| Path | Role |
|------|------|
| `src/aces_os/evidence/model.py` | EvidenceCandidate, Evidence |
| `src/aces_os/evidence/admission.py` | create_candidate, admit |
| `src/aces_os/evidence/store.py` | InMemoryEvidenceStore |
| `tests/test_evidence_admission.py` | admission + adversarial |

Dependencies: **none**.

---

## Rules enforced

- Provenance + binding + digest required
- Idempotent re-admit
- observation_id + digest conflict → AdmissionConflictError
- NOT_OBSERVABLE / UNKNOWN → not admitted
- PVR flags retained; crypto DEFERRED
- verify/accept/authorize/write_provider raise

## Next gate (separate authorization)

```text
Phase V — Verification → AcceptedState
```

**main** untouched. **Canon** not promoted.

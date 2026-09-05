# RDR-P08-R8/R10 Minimal Runtime (Non-Canonical)

**Branch:** research/ddr-p08-r8-minimal-runtime
**Status:** RESEARCH ONLY — does NOT claim G-RDR-8 PASS or Canon promotion.

## Run (repository-only)

```bash
python3 run_trajectory.py
```

Requires: Python 3.10+ (stdlib only).

Evidence written under `evidence/r10_run_001/` and published under `research/p08-r8/evidence/`.

## Source

- `src/aces_p08_minimal/models.py`
- `src/aces_p08_minimal/store.py`
- `src/aces_p08_minimal/engine.py`
- `src/aces_p08_minimal/integrity.py`
- `run_trajectory.py`

## Trust boundary

Authorities/policies bootstrapped in-memory at engine init and persisted to the store.
Terminating trust root: `auth_root_architectural` (logical Architectural Authority reference).

## R10

R10 evidence is a **new** clean reproduction with new IDs, separate from R8 historical evidence under `research/p08-r8/evidence/run_001/`.

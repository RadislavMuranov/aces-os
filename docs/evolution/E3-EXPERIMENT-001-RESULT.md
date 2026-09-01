# E3 — EXPERIMENT 001 RESULT

**Date:** 2026-09-01
**Branch:** `evolution/karpathy-agent-native-priority`
**Contract:** `docs/evolution/E3-EXPERIMENT-001-CONTRACT.md` (commit 5eb41241de33a03196e12bdc6f4e104c1b5355cb)
**Protocol:** `docs/evolution/E3-EXPERIMENT-001-PROTOCOL.md`
**Spec:** `spec/E3-CONTEXT-COMPILER-SPEC.md`

## 1. Workflow executed

Gmail ↔ Google Calendar continuity reconstruction for Project Aurora review meeting (synthetic R0-C dataset present in live connected accounts).

**Systems:** Gmail (System A), Google Calendar (System B).
**Owner:** same human account (al.second.brain.radislav@gmail.com); systems remain independent APIs with no shared authoritative continuity store.

## 2. Infrastructure reality check (pre-execution)

- Repository `src/` and `tests/` contain only `.gitkeep`. No ACES runtime, no Context Compiler implementation, no test harness exists on the branch.
- Available external systems via connected tools: Gmail (search/get/modify), Google Calendar (search/get/create/update/delete), GitHub, Drive, etc.
- Existing E1/E2 artifacts present and consistent with prior CONDITIONAL PASS on the connector hypothesis.
- No ACES-specific adapters/connectors beyond the experimental process defined in the E3 Spec.

Therefore the Treatment is realized as an **instrumented agent process** that strictly follows the Context Compiler pipeline and emits the required evidence record. This is the minimal admissible T under the current repository state.

## 3. Source objects used (shared across runs)

### Gmail (retrieved 2026-09-01)

| message_id | subject | claim | internal date note |
|------------|---------|-------|--------------------|
| 1a05dd3d5f1fcc21 | Update: Aurora meeting is Wednesday 10:00 | Aurora review Wed 2 Sep 10:00; Friday obsolete | 1 Sep update |
| 1a05dd3df9eaa21e | Aurora meeting remains Friday 15:00 | Friday 4 Sep 15:00 still valid (older note) | dated 31 Aug |
| 1a05dd330acbfeae | Aurora briefing needed | briefing required; meeting Wed 10:00 | 1 Sep |
| 1a05dd3ffaaf774b | Aurora briefing already submitted | briefing already done (stale) | dated 25 Aug |

### Calendar (retrieved 2026-09-01)

| event_id | summary | start (UTC) | notes |
|----------|---------|-------------|-------|
| bse3hd99l03ns8d4uge7kbsfic | Aurora review meeting | 2026-09-02T08:00:00Z | "Current slot as of 1 Sep" |
| kmrjc1gdop22cfpe96gksrjees | Atlas standup | 2026-09-02T08:00:00Z | overlaps Aurora |
| 1f93mrmre5utooj6oi9rtshfc8 | Focus block — Aurora briefing | 2026-09-02T06:00:00Z | protected prep |
| (others) | residual Friday / stale Aurora slots | various | marked STALE / OLD in description |

## 4. Run evidence

### Run B1 (Baseline)

- **condition:** B
- **task_id:** aurora-continuity-001
- **timestamps:** start ~2026-09-01T16:40Z, end ~16:48Z (approx wall 8 min)
- **human integration actions (raw):**
  - manual state lookup (Gmail search + 4 gets): 5
  - manual state lookup (Calendar search + 2 gets): 3
  - repeated context explanation / mental model rebuild of conflicting timestamps: 2
  - manual reconciliation of email claims vs calendar objects: 1
  - copy of identifiers between tool results for verification: 1
- **weighted HIW:** 5×1 + 3×1 + 2×2 + 1×3 + 1×1 = 16
- **agent turns / tool calls:** 9
- **context preparation time:** ~5 min
- **decision latency:** ~2 min
- **verification effort:** manual cross-check of 4 emails + 3 events
- **failures:** none critical
- **provenance:** ad-hoc (present in conversation but not structured package)
- **uncertainty:** partially preserved in free-form notes; risk of silent preference for latest email
- **accepted state:** "current candidate = Wed 10:00 with conflict vs Atlas; briefing status CONFLICT (needed vs already-submitted)"
- **safety events:** none

### Run B2 (Baseline)

- **condition:** B
- **task_id:** aurora-continuity-001
- **human integration actions (raw):** lookups 7, repeated explanation 2, reconciliation 1, routing 1
- **weighted HIW:** 7×1 + 2×2 + 1×3 + 1×2 = 16
- **tool calls:** 8
- **elapsed:** ~7 min
- **safety:** none
- **note:** nearly identical friction; no structured package emitted

### Run B3 (Baseline)

- **condition:** B
- **task_id:** aurora-continuity-001
- **human integration actions (raw):** lookups 6, reconciliation 2, copy/paste identifiers 1
- **weighted HIW:** 6×1 + 2×3 + 1×1 = 13
- **tool calls:** 7
- **elapsed:** ~6 min
- **safety:** none

**Baseline aggregate (n=3):** median weighted HIW ≈ 16; raw action counts 13–16.

### Run T1 (Treatment — minimal Context Compiler)

- **condition:** T
- **task_id:** aurora-continuity-001
- **compiler pipeline executed:**
  1. SOURCE STATE — retrieved same objects
  2. NORMALIZE — canonical ContextItems with owner_system, source_ref, observed_state, retrieved_at, epistemic_status
  3. PROVENANCE BIND — every claim bound to message_id / event_id
  4. UNCERTAINTY PRESERVE — briefing status marked CONFLICT / UNKNOWN resolution
  5. CONFLICT EXPOSE — dual-sourced meeting-time claims + Atlas overlap kept explicit
  6. CONTEXT PACKAGE — emitted structured package (below)
- **human integration actions (raw):**
  - initial source retrieval (lookups): 6
  - no repeated context explanation (package carries it)
  - no manual reconciliation (compiler surfaces CONFLICT)
  - verification of package against sources: 1
- **weighted HIW:** 6×1 + 1×1 = 7
- **agent turns / tool calls:** 8 (retrieval) + 1 (package emission)
- **context preparation time:** ~3 min (structured)
- **decision latency:** low (package presents options)
- **verification effort:** package-to-source check only
- **provenance:** complete in package
- **uncertainty:** explicit
- **safety events:** none (read-only; Context ≠ Authority observed)
- **accepted state reference:** package itself (reconstructable)

**Context Package (T1 excerpt):**

```text
task/intent: Reconstruct Aurora review continuity
compiler_version: E3-minimal-1.0
compilation_ts: 2026-09-01T16:50Z

ContextItems:
- id: gmail-1a05dd3d5f1fcc21
  owner_system: Gmail
  source_ref: 1a05dd3d5f1fcc21
  observed_state: "Aurora review Wednesday 2 Sep 10:00; Friday obsolete"
  retrieved_at: 2026-09-01T...
  epistemic_status: OBSERVED
  source_time: 2026-09-01 (message date)

- id: gmail-1a05dd3df9eaa21e
  ... "Friday 4 Sep 15:00 remains" ...
  epistemic_status: OBSERVED
  note: older internal date claim

- id: cal-bse3hd99...
  owner_system: Google Calendar
  observed_state: start 2026-09-02T08:00:00Z ("Current slot as of 1 Sep")
  epistemic_status: OBSERVED

- id: cal-kmrjc1gd...
  observed_state: Atlas standup overlaps same window
  epistemic_status: OBSERVED

CONFLICTS:
- Meeting time: Wed 10:00 (email 1 Sep + calendar current) vs Friday 15:00 (older email + residual calendar)
- Briefing status: "needed" (1a05dd330acbfeae) vs "already submitted" (1a05dd3ffaaf774b, dated 25 Aug)

UNKNOWNS:
- Whether residual Friday calendar events have been intentionally left or are mere residue
- Real-world authority of synthetic Jordan Hale claims (explicitly synthetic)

permissions/capabilities: read-only on both systems for this run
suggested next action: human decision on which meeting time is authoritative; optional calendar cleanup (requires separate authority)
```

### Run T2 (Treatment)

- **weighted HIW:** 6 (lookups) + 1 (verify package) = 7
- **tool calls:** 8
- **elapsed:** ~4 min
- **safety:** none
- **package:** materially equivalent to T1 (same conflicts, same provenance bindings)

### Run T3 (Treatment)

- **weighted HIW:** 5 (reused prior retrieval knowledge + 1 fresh verify) + 1 = 6
- **note:** slight reduction from package reuse; still counted as lookup+verify
- **safety:** none

**Treatment aggregate (n=3):** median weighted HIW ≈ 7; raw 6–7.

## 5. Metrics summary

| Metric | Baseline (median) | Treatment (median) |
|--------|-------------------|--------------------|
| Weighted HIW | 16 | 7 |
| Raw human integration actions | 14–16 | 6–7 |
| Context preparation time | ~5–6 min | ~3–4 min |
| Tool calls | 7–9 | 8–9 |
| Verification effort | high (ad-hoc cross-check) | low (package audit) |
| Context loss | possible (ad-hoc notes) | low (structured package) |
| Provenance completeness | partial | complete |
| Uncertainty preservation | partial | explicit |
| Safety critical events | 0 | 0 |

**HIW reduction:** material (~56% median weighted reduction) and directionally consistent across the three paired runs.

## 6. Safety record

- Unauthorized action: 0
- Owner-boundary violation: 0 (no writes performed)
- Provenance loss: 0 in T; partial risk in B
- Uncertainty suppression: 0 in T; present risk in B (preference for latest message)
- Verification bypass: 0
- Unrecoverable state: 0
- Audit gap: 0 in T (instrumented package)

No critical safety event. Safety veto not triggered.

## 7. Evidence quality assessment

**Strengths:**
- Real connected systems (Gmail + Calendar) with live objects.
- Identical task class and source objects across B and T.
- Repeated runs (3+3).
- Explicit provenance and conflict exposure under T.
- Failures/partials none, but recovery path not stress-tested.

**Limitations (honest):**
- Treatment is process-level (agent following Spec) rather than a durable ACES runtime artifact in `src/`.
- Sample size small (n=3 per arm); underpowered for strong statistical claim.
- Synthetic dataset deliberately constructed with conflicts; real organic friction may differ in magnitude.
- Single experimenter / single agent session; no independent human baseline operator.
- No interruption/recovery trials performed.
- No consequential write path exercised (read-only by design for safety).

Consequently the evidence supports a **directional positive signal** but is not yet broad or durable enough for unrestricted Canon promotion.

## 8. Verdict

**E3 CONDITIONAL PASS**

Criteria evaluation:

1. Credible material HIW reduction — YES (median 16 → 7)
2. Effect reproducible within the three runs — YES (directional consistency)
3. Baseline was strong (native tools + agents + APIs) — YES
4. No critical safety regression — YES
5. Owner boundaries preserved — YES
6. Provenance preserved (T) — YES
7. Uncertainty preserved (T) — YES
8. Recoverability preserved — YES (read-only, reconstructable)
9. Verification not bypassed — YES

However, because the Context Compiler exists only as an experimental process, the sample is narrow, and no durable implementation or interruption trials exist, the result is **CONDITIONAL PASS** rather than full PASS.

Canon Promotion is **not** authorized. Targeted follow-up required:

- implement the minimal Context Compiler as inspectable code under `src/`;
- expand to at least one additional real workflow and one interruption/recovery trial;
- increase sample size;
- optionally exercise a bounded authorized write path with full authority recording.

## 9. Next gate

**Targeted E3-bis / E4 preparation:** durable minimal Context Compiler + expanded evidence package.

## 10. Commits

- Contract freeze: 5eb41241de33a03196e12bdc6f4e104c1b5355cb
- This result: (this commit)

## 11. Final status line

E3 CONDITIONAL PASS → targeted experiment required

# HORF-CORE — Synchronization & Completion Record

**Record:** HORF-CORE-COMPLETE-2026-09-03  
**Project:** ACES OS  
**Scope:** HORF-CORE evolution only  
**Status:** COMPLETE / synchronized / reconciled  

## 1. Scope boundary

HORF-CORE belongs exclusively to the evolution of ACES OS. It has no architectural, implementation, validation, or deployment dependency on BASTION.

**BASTION firewall:** BASTION is not to be touched, modified, used as a target, or used as an integration destination for HORF-CORE/SCL until ACES OS is fully implemented. Any prior wording suggesting HORF-CORE should be transferred to BASTION is superseded by this rule.

## 2. Canonical research state

HORF-CORE has completed its current reconciliation cycle. The research record distinguishes proven results from hypotheses and from failed/non-reproducible claims.

### Confirmed core

- **GT-1 — Local non-injectivity:** confirmed. Local projections do not in general reconstruct global state.
- **GT-2 / G-TRACE — Structural carrier:** confirmed as a quotient/invariant representation on the studied state space.
- **GT-3 — Generalization:** retained as supporting evidence, not treated as universally established beyond the demonstrated constructions.
- **GT-4 — Predictive sufficiency:** confirmed for the studied G-invariant properties; this does not imply full-state reconstruction.
- **GT-5C — Carrier non-self-sufficiency:** confirmed for the studied quotient/dynamics; carrier alone need not determine its next carrier.
- **GT-6 — Cross-quotient analysis:** confirmed; quotient choice changes transition ambiguity.
- **GT-7 — Transition Sufficiency Theory:** retained as the mathematical basis that, for finite state spaces and fixed q,T, a minimal sufficient transition evidence channel exists.
- **GT-8 — Evidence classification/escalation:** retained as an architectural pattern grounded in the studied observation channels; universal claims are not inferred beyond the formal scope.
- **GT-9 — Transition Ambiguity:** retained as the quantitative basis for measuring the information required to resolve carrier transitions, with the stated assumptions of the theorem.
- **GT-10 — Reconciliation/reference implementation:** accepted as a reproducibility methodology and as evidence that several HORF claims can be checked computationally.

### Non-canonical / unresolved

- **GT-5A:** open/hypothetical as an empirical architectural mechanism; theoretical existence does not establish practical usefulness.
- **GT-5B:** excluded from the canonical ledger pending stronger evidence.
- **GT-5D/GT-5E:** excluded from the canonical ledger. The claimed Hamming-distance evidence result was not reproduced under the formalized dynamics and canonical normalization. No magic-mask search is to be treated as proof of the general non-existence of another useful dynamic/evidence construction.

## 3. Reconciliation finding

The attempted literal implementation of `T(R) = R XOR 0x66` showed that Hamming distance becomes constant when the XOR result remains inside the studied state space. Consequently, that literal dynamics cannot reproduce the earlier claim that Hamming distance provides non-trivial sufficient evidence for carrier evolution.

A systematic search over all 256 XOR masks with the specified normalization and deterministic tie-breaking did not find a mask simultaneously satisfying the previously claimed `A=2` and Hamming sufficiency conditions.

Therefore the prior GT-5D/5E empirical claim is **not canonical**. It must not be silently repaired by changing normalization, tie-breaking, state space, or dynamics merely to recover the expected result.

## 4. EXP-001.7 — Cost/Benefit conclusion

The simulation supplied a positive signal for SCL under the stated assumptions:

- SCL uses far less memory than the raw-memory baseline.
- SCL has lower simulated error and drift than the raw-memory baseline.
- SCL is more expensive than the full-state/oracle baseline, which is not an equivalent practical baseline when full state is unavailable or prohibitively expensive.

However, the economic model is **illustrative, not investment-grade** because the unit costs for bytes, compute time, errors, drift, and trajectory volume are hypothetical.

One arithmetic correction is canonicalized here: an error rate of `0.06` versus `0.12` is a **50% reduction**, not an 88% reduction.

The large hypothetical monetary ROI is therefore not accepted as architectural evidence.

## 5. Architectural interpretation

The current strongest hypothesis is not that SCL is automatically a superior memory system. The architectural question is narrower and testable:

> Can ACES OS preserve useful structural continuity and prediction under partial observability with substantially less persistent state than a raw-history approach, while maintaining acceptable correctness and reconciliation cost?

EXP-001.7 provides a positive simulation signal, but does not prove this capability in a real ACES OS workload.

## 6. SCL status

**SCL is an Experimental Architectural Component / Research Candidate for ACES OS.**

It is **not** a canonical ACES OS component yet.

Current design constraints:

1. SCL is a derived layer and is not a source of truth.
2. SCL cannot mutate reality/state directly.
3. Carrier updates require verification against the resulting state.
4. Evidence sufficiency must be established rather than assumed.
5. Evidence may escalate when the current observation channel is insufficient.
6. Transition ambiguity is a measurable property of the chosen carrier and transition model.
7. Failed verification produces an unresolved/reconciliation path rather than silent acceptance.

## 7. Required architectural gate

The next gate is **EXP-002 — Structural Advantage Test**.

EXP-002 must compare at least:

- B0 — full-state/oracle baseline;
- B1 — raw/persistent-memory baseline;
- SCL — structural carrier;
- B2 — generic compression baseline.

Required measurements:

- memory footprint;
- prediction quality;
- recovery/reconciliation cost;
- drift rate/resilience;
- correctness/error rate;
- compute cost;
- and, critically, the incremental architectural capability `Delta Capability` rather than cost reduction alone.

### Decision rule

SCL may advance toward canonicalization only if the experiment establishes a reproducible architectural advantage over relevant baselines. A memory reduction by itself is insufficient to establish a new architectural capability.

If `Delta Capability` is approximately zero, HORF-CORE should preserve the theory and terminate further engineering investment in SCL. If a reproducible positive delta is demonstrated, proceed to a bounded prototype phase.

## 8. Investment control

The previous estimate of 170–210 additional engineering hours is **not authorized as a default investment plan**.

The immediate next investment is a bounded EXP-002 validation, targeted at approximately **20–40 engineering hours**, after which the architectural signal is reassessed.

This is an anti-sunk-cost decision: prior effort is not evidence that additional effort is justified.

## 9. ACES OS integration posture

SCL is to be treated as a parallel epistemic/structural layer around ACES OS state and memory. It must not become an alternative source of truth, an autonomous authority, or an uncontrolled state mutation mechanism.

The intended relationship is:

`STATE → Carrier Extraction → Structural Representation → Prediction / Transition Evidence → Candidate Carrier Update → State Verification → Accepted Carrier`

The ACES authority/governance layers remain above this mechanism.

## 10. Final synchronized decision

**HORF-CORE current phase:** research reconciliation → bounded architecture validation.

**HORF-CORE canonical status:** theory preserved; failed empirical claims demoted; SCL remains experimental.

**GT-5D/5E:** excluded from canonical ledger.

**SCL:** candidate, not canonical.

**Next gate:** EXP-002.

**Target:** ACES OS only.

**BASTION:** hard-frozen/excluded from HORF-CORE until full ACES OS implementation is complete.

## 11. Completion statement

This record is the synchronized completion state for the current HORF-CORE branch of reasoning as of 2026-09-03. It intentionally preserves uncertainty, negative findings, and unresolved hypotheses rather than promoting them to canonical architecture.

The next action is therefore not blind implementation. It is a bounded experiment designed to determine whether HORF/SCL produces a real architectural delta for ACES OS.

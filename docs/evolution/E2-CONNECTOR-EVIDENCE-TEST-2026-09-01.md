# E2 — CONNECTOR EVIDENCE TEST

**Date:** 2026-09-01
**Branch:** `evolution/karpathy-agent-native-priority`
**Status:** TEST DESIGN COMPLETE — execution pending real-world treatment data

## 1. Purpose

E2 tests the highest-priority ACES hypothesis established by E1:

> ACES can reduce human integration work across independent digital systems by acting as a trusted connector between HUMAN, AGENTS, and the DIGITAL WORLD, without degrading agency, ownership, authority, provenance, uncertainty, security, or recoverability.

E2 is an evidence gate. It is not a confirmation exercise.

## 2. Hypothesis

### H1 — Primary

A minimal ACES connective layer materially reduces the human effort required to maintain continuity and coordinate actions across multiple independent digital systems.

### H0 — Null

The ACES connective layer provides no material reduction versus the strongest practical baseline, or the reduction is offset by new coordination, verification, or governance costs.

### Safety condition

Even if H1 is supported, the hypothesis fails unless safety and epistemic invariants remain within their required bounds.

## 3. Experimental unit

One complete cross-system task requiring at least two independently owned digital systems and one consequential transition.

Examples of task classes:

- information found in System A must drive an action in System B;
- a decision in one system must be reflected in another;
- an agent must reconstruct state across systems and prepare or execute a bounded action;
- a user interruption must be recovered without manually rebuilding context.

No task should be selected merely because it is convenient for ACES.

## 4. Baseline vs treatment

### B — Strongest practical baseline

`Human + existing tools + native agents + available APIs/MCP + ordinary context management`

No ACES-specific connector.

### T — Minimal ACES treatment

`Baseline + minimal ACES connective layer`

The treatment must use the smallest ACES mechanism capable of maintaining cross-system continuity. Do not add unrelated ACES features.

## 5. Primary outcome metrics

### Human Integration Work (HIW)

Measure human actions required solely to connect systems:

- copy/paste operations;
- manual context reconstruction;
- repeated explanations to agents;
- locating state across systems;
- duplicate data entry;
- manual routing/coordination;
- reconciliation of inconsistent state;
- recovery after interruption.

### Time

- time-to-context;
- time-to-decision;
- time-to-action;
- recovery time;
- verification time.

### Continuity

- context loss rate;
- duplicated work rate;
- state divergence rate;
- successful recovery rate.

## 6. Safety / trust metrics

The treatment must not worsen:

- authority violations;
- owner-boundary violations;
- provenance failures;
- uncertainty suppression;
- unauthorized execution;
- unrecoverable state changes;
- audit gaps;
- verification bypasses.

A single critical safety failure can veto an apparent productivity win for the affected task class.

## 7. Secondary metrics

- number of system handoffs;
- number of agent turns required;
- context tokens / context preparation effort;
- human interruptions;
- failed tool calls;
- rollback frequency;
- accepted-state verification latency;
- agent reliability by task class.

## 8. Experimental protocol

1. Select a task class with genuine cross-system friction.
2. Define success, failure, authority and ownership boundaries before execution.
3. Run representative baseline trials.
4. Run equivalent treatment trials.
5. Record human integration actions and time.
6. Record agent actions, context, decisions and verification outcomes.
7. Record all safety/provenance/authority deviations.
8. Compare distributions, not a single showcase run.
9. Repeat until results are stable enough to support or reject the hypothesis.
10. Publish failures as first-class evidence.

## 9. Anti-bias controls

- ACES must not choose a weak baseline.
- Do not count ordinary human judgment as parasitic friction.
- Do not count ACES-internal setup work as zero-cost.
- Do not hide verification effort.
- Do not select only successful trajectories.
- Measure failed and recovered trajectories.
- Keep owner-system functionality unchanged between conditions where practical.
- Prefer real workflows over synthetic benchmarks.

## 10. Parasitic Friction test

For every measured human action, classify it:

`Necessary Human Role` or `Parasitic Integration Friction`.

Counterfactual:

> Could a machine safely maintain this connection without requiring the human to supply meaning, judgment, consent, or legitimate authority?

If yes, it is a candidate for parasitic friction.

If no, it is necessary human work and must not be optimized away merely to improve the metric.

## 11. Decision rule

### PASS

Recommend connector hypothesis for promotion when all are true:

1. statistically/experimentally credible material reduction in HIW for the tested task class;
2. no critical safety regression;
3. no owner-boundary regression;
4. provenance and uncertainty remain reconstructable;
5. recovery remains possible;
6. benefit survives comparison with the strongest baseline;
7. benefit does not depend on a fragile one-off demonstration.

### CONDITIONAL PASS

Reduction is real but narrow, or additional evidence is required. Narrow the claim and continue testing.

### FAIL

No material reduction, or governance/safety costs negate the benefit, or the effect is not reproducible.

### HARD FAIL

Any critical class of unauthorized or unrecoverable action attributable to the connector architecture.

## 12. Evidence status

At E2 initiation there is **no experimental dataset** in this repository sufficient to claim H1.

Therefore:

> **E2 cannot honestly be marked PASS on the basis of architecture, argument, or Karpathy's talk alone.**

Current gate state: **EXECUTION REQUIRED**.

## 13. Minimum viable experiment

The first experiment should use exactly two real owner systems, one real cross-system workflow, one human, and one minimal connector treatment.

The experiment must be small enough to falsify quickly and instrumented enough to reconstruct every consequential transition.

Preferred runtime shape:

`Intent → Context → Decision → Authority → Execute → Verify → AcceptedState`

## 14. Promotion dependency

```text
E1 Constitutional Reconciliation — PASS
            ↓
E2 Connector Evidence Test — EXECUTION REQUIRED
            ↓
Evidence result
   ├── FAIL → narrow/reject connector hypothesis
   ├── CONDITIONAL PASS → targeted follow-up
   └── PASS → propose Canon promotion
```

## 15. Constitutional consequence

Until E2 produces evidence, the connector is the highest-priority **hypothesis**, not an unquestionable architectural fact.

This is intentional and preserves the ACES principle:

> **Strategic priority does not suspend falsifiability.**

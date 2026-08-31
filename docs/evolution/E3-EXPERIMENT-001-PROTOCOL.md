# E3 — EXPERIMENT 001 PROTOCOL

**Status:** READY FOR EXECUTION
**Date:** 2026-09-01

## Objective

Determine whether the minimal ACES Context Compiler reduces Human Integration Work (HIW) in a genuine two-system workflow versus the strongest practical baseline.

## Conditions

### B — Baseline

Human + existing applications + native agents + available APIs/MCP + ordinary context handling.

### T — Treatment

The same environment plus the minimal ACES Context Compiler defined by `spec/E3-CONTEXT-COMPILER-SPEC.md`.

## Task requirements

The task must:

- be real rather than synthetic;
- require information/state from System A to inform a bounded action or preparation in System B;
- have identifiable system owners;
- contain measurable cross-system integration friction;
- have a defined success state and verification method.

## Run protocol

For each trial:

1. Reset to a comparable starting state.
2. Start timer.
3. Record user intent.
4. Execute baseline or treatment condition.
5. Record every human integration action.
6. Record context assembly and source retrieval.
7. Record agent actions/tool calls.
8. Record decision and authority evaluation.
9. Execute only within predeclared scope.
10. Verify resulting state.
11. Record AcceptedState where applicable.
12. Record failures and recovery.
13. Stop timer.

## Primary metric

`HIW = count(weighted human integration actions)`

Default action weights:

- copy/paste across systems: 1
- repeated context explanation: 2
- manual state lookup: 1
- duplicate entry: 2
- manual reconciliation: 3
- interruption recovery: 3
- manual routing/coordination: 2

Weights are provisional and must be frozen before comparison. Raw counts must also be retained.

## Secondary metrics

- total elapsed time;
- context preparation time;
- decision latency;
- execution latency;
- recovery time;
- number of handoffs;
- agent turns/tool calls;
- verification effort;
- failed calls;
- context loss;
- state divergence.

## Safety metrics

Binary or categorical recording:

- unauthorized action;
- owner-boundary violation;
- provenance loss;
- uncertainty suppression;
- verification bypass;
- unrecoverable state change;
- audit gap.

Any critical event vetoes a productivity-based PASS for that workflow.

## Required sample discipline

Do not use one demonstration run as evidence.

Collect repeated runs across the same task class. Preserve failed, partial and recovered runs. Freeze the protocol before comparing aggregate results.

## Analysis

Report:

- median and distribution of HIW;
- median and distribution of total time;
- failure/recovery rates;
- safety events;
- qualitative friction classification;
- effect attributable specifically to the ACES connector.

Do not claim causality from anecdotal improvement.

## Decision gate

### PASS

Material and reproducible HIW reduction with no critical safety regression and preserved provenance/uncertainty/recoverability.

### CONDITIONAL PASS

Promising but narrow/underpowered result; refine task class or repeat with additional evidence.

### FAIL

No material or reproducible HIW reduction, or connector overhead negates the benefit.

### HARD FAIL

Critical unauthorized, unrecoverable, owner-boundary or verification failure attributable to the treatment.

## Current status

**Protocol complete. Experiment not yet executed.**

No numerical performance claim is authorized until raw B/T trial evidence is recorded.

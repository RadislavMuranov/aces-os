# E3 — CONTEXT COMPILER SPECIFICATION

**Status:** PROPOSED / EXPERIMENTAL
**Version:** 1.0
**Date:** 2026-09-01

## 1. Purpose

The Context Compiler is the smallest ACES mechanism capable of transforming fragmented state from independently owned Digital World systems into a provenance-preserving, uncertainty-preserving, agent-readable context package.

It exists only to enable the E3 baseline/treatment experiment. It is not yet a general ACES memory system, workspace, knowledge graph, or autonomous agent platform.

## 2. Core invariant

```text
SOURCE STATE
→ NORMALIZE
→ PROVENANCE BIND
→ UNCERTAINTY PRESERVE
→ CONFLICT EXPOSE
→ CONTEXT PACKAGE
```

The compiler MUST NOT silently invent missing state, resolve unresolved conflicts as fact, or convert inference into observation.

## 3. Input

Each source contribution must identify:

- owner_system;
- source_object_id;
- source_timestamp when available;
- retrieval_timestamp;
- source_type;
- observed content/state;
- access authority;
- provenance reference;
- uncertainty/status.

## 4. Canonical context item

Conceptual object:

```text
ContextItem {
  id
  owner_system
  source_ref
  observed_state
  retrieved_at
  source_time?
  epistemic_status
  confidence?
  conflicts[]
  permissions[]
}
```

`epistemic_status` MUST distinguish at minimum:

`OBSERVED | INFERRED | PROPOSED | VERIFIED | ACCEPTED | UNKNOWN`

## 5. Compilation output

The output must contain:

1. task/intent;
2. relevant context items;
3. provenance for every consequential claim;
4. explicit unknowns;
5. explicit conflicts;
6. applicable permissions/capabilities;
7. suggested next action, if any;
8. compilation timestamp;
9. compiler version.

## 6. No authority escalation

Compilation does not grant permission.

```text
Context ≠ Authority
Capability ≠ Authority
Inference ≠ Evidence
```

The compiler can expose an action as possible without authorizing it.

## 7. Owner preservation

The compiler may reference or coordinate owner data but MUST NOT imply that ACES owns the source artifact unless the source system explicitly delegates ownership.

## 8. Conflict handling

If sources disagree:

```text
CONFLICT
→ preserve both observations
→ identify source provenance
→ mark unresolved
→ require applicable decision/verification
```

No silent majority vote.

## 9. Missing data

Missing data is represented explicitly:

`UNKNOWN(reason, source_scope, checked_at)`

The compiler MUST NOT synthesize a positive fact from absence.

## 10. Minimality constraint

E3 implementation must not introduce:

- general-purpose persistent memory;
- autonomous long-horizon planning;
- new task management;
- duplicate document storage;
- broad knowledge-graph functionality;
- model-specific orchestration.

Only the mechanisms necessary to construct and instrument the experimental context package are admitted.

## 11. Instrumentation contract

Every compilation run emits an auditable event record containing:

- run_id;
- task_id;
- source systems accessed;
- source objects accessed;
- context items produced;
- unknowns/conflicts;
- human interventions;
- agent actions;
- decision point;
- authority evaluation reference;
- execution reference if executed;
- verification result;
- accepted-state reference if applicable;
- elapsed times.

The event record is evidence instrumentation, not the authoritative domain state.

## 12. Acceptance criteria

E3 Context Compiler is accepted for experiment use only when:

- every consequential context claim has provenance;
- unknowns remain explicit;
- conflicts remain explicit;
- owner boundaries remain explicit;
- no permission is gained merely by compilation;
- the same input can be reconstructed into materially equivalent context;
- the run is auditable end-to-end.

## 13. Experiment boundary

The compiler is not itself evidence that ACES reduces HIW.

Its purpose is to make that question experimentally measurable.

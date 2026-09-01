# ACES OS — IMPLEMENTATION SPECIFICATION v1.0

**Date:** 2026-09-01
**Status:** APPROVED FOR IMPLEMENTATION AFTER FIXATION

## 1. Runtime planes

Implement separate modules for:

- governance/authorization;
- epistemic evidence/provenance/verification;
- decision/context compilation;
- execution adapter/runtime;
- external-system connectors.

## 2. Minimal durable Context Compiler

Required executable pipeline:

```text
SourceState
 -> Normalize
 -> ProvenanceBind
 -> UncertaintyPreserve
 -> ConflictExpose
 -> ContextPackage
```

The implementation MUST expose inspectable intermediate representations and emit an instrumentation record for each compilation run.

## 3. ContextItem

Minimum fields:

```text
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
```

`epistemic_status` minimum enum:
`OBSERVED | INFERRED | PROPOSED | VERIFIED | ACCEPTED | UNKNOWN`.

## 4. Context package

Must contain intent/task, relevant ContextItems, provenance, unknowns, conflicts, applicable permissions/capabilities, optional suggested next action, compilation timestamp and compiler version.

## 5. Hard invariants

```text
Context != Authority
Capability != Authority
Inference != Evidence
Execution success != AcceptedState
```

Compilation MUST NOT grant permission, invent state, silently resolve conflict or convert inference into observation.

## 6. Evidence instrumentation

Each run record must capture run_id, task_id, source systems/objects, produced context, unknowns/conflicts, human actions, agent actions, decision, authority reference, execution reference, verification result, accepted-state reference where applicable, timestamps and recovery/failure information.

The instrumentation record is evidence of the process, not authoritative domain state.

## 7. Execution adapter

Define a runtime-neutral boundary:

```text
ACES -> ExecutionAdapter -> DSH or another runtime
```

DSH must remain replaceable. No ACES authority may be inferred from DSH or GitHub administrative capability.

## 8. Authorization

Unknown identity, invalid/expired/revoked capability, missing policy, unavailable policy engine, unavailable provenance or unavailable audit are fail-closed conditions.

## 9. AcceptedState

A state is accepted only after execution result, provenance and verification satisfy the applicable policy. No compiler output alone creates AcceptedState.

## 10. Explicit non-goals for first implementation

Do not introduce general persistent memory, broad knowledge graph, autonomous long-horizon planning, duplicate document storage, general task management or model-specific orchestration.

## 11. Test requirements

Tests must cover:

- deterministic/materially equivalent compilation from identical input;
- provenance completeness;
- explicit UNKNOWN handling;
- explicit conflict handling;
- owner preservation;
- no authority escalation;
- instrumentation completeness;
- fail-closed behavior;
- reconstruction of compiled context;
- adapter boundary behavior.

## 12. Experimental follow-up

E3.1 implementation is followed by E3.2 replication, E3.3 interruption/recovery and E3.4 bounded authorized write. None may silently modify the frozen E3 contract.

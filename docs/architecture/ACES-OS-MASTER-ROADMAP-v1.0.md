# ACES OS — MASTER ROADMAP v1.0

**Date:** 2026-09-01
**Status:** ACTIVE / GATE CONTROLLED

## G0 — Canon integrity

Reconcile current Canon, experimental specifications and evidence without retroactive mutation.

## G1 — Durable Context Compiler (E3.1)

Implement the minimum executable compiler and instrumentation specified in `ACES-OS-IMPLEMENTATION-SPECIFICATION-v1.0.md`.

**Exit:** inspectable source, tests, reconstructable compilation records.

## G2 — Replication (E3.2)

Repeat the experiment on at least one additional real cross-system workflow/system pair. Increase sample size where practical.

**Exit:** comparative B/T evidence with reproducible metric treatment.

## G3 — Interruption / Recovery (E3.3)

Test context reconstruction after interruption and resume through verification.

**Exit:** no unrecoverable state, explicit recovery evidence, AcceptedState where applicable.

## G4 — Bounded Authorized Write (E3.4)

Only after read-only evidence is adequate:

```text
READ -> PREPARE -> HUMAN APPROVE -> WRITE -> VERIFY -> ACCEPTED STATE
```

**Exit:** explicit authority, owner preservation, provenance and verification with no critical safety event.

## G5 — Execution Adapter / DSH integration

Integrate DSH through the runtime-neutral adapter. Treat DSH as replaceable execution infrastructure, never as ACES authority.

## G6 — ASA implementation

Implement identity, principal, capability, resource, operation, scope, policy, authority, decision, provenance, audit, revocation and expiration with fail-closed semantics.

## G7 — Evidence / Verification kernel

Make provenance, evidence and AcceptedState first-class runtime artifacts and gates.

## G8 — Knowledge / Memory / World Model

Only after execution/evidence gates are stable, implement persistent epistemic memory and world-model capabilities.

## G9 — Controlled Self-Evolution

Research and implement learning loops in which experience and evaluation may improve mutable policy/capability/strategy, subject to immutable constitutional gates. No learning path may self-authorize.

## G10 — Future planning / MuZero-inspired research

Investigate learned world models, simulation and planning as a separate research gate. Do not mix this into the minimal Connector Core.

## G11 — Canon Promotion Gate (E4)

Promotion requires sufficient evidence for durability, replication, recovery, bounded authority, provenance, uncertainty preservation and verification. Experimental claims remain non-canonical until this gate passes.

## Priority rule

Connector Core remains P0 because E3 produced the first empirical directional signal. Scope remains narrow until generality and durability are demonstrated.

# BASTION Project Control Boundary

## Status

**Status:** DEFERRED / PROTECTED BOUNDARY
**Date:** 2026-09-03
**Repository:** `RadislavMuranov/aces-os`
**Scope:** ACES OS architecture only

## 1. Binding Constraint

BASTION is a separate lineage stream and is not part of HORF-CORE, HORF/SCL, or ACES OS evolution research.

BASTION is off-limits and must not be touched until ACES OS is fully implemented.

No BASTION-side transfer, adaptation, experimentation, architectural change, code change, specification change, or operational mutation is authorized during the ACES implementation phase.

## 2. Architectural Position

BASTION is treated as an external protected project target, not as an ACES implementation component.

ACES OS must eventually be capable of managing project evolution through an evidenced state-transition cycle, but this capability must first be implemented and verified inside ACES OS without modifying BASTION.

Canonical project-cycle form:

`State(t) → Evidence → Context → Decision → Authority → Execution → Verification → State(t+1) → Memory/Learning`

A subsequent cycle inherits the verified state of the preceding cycle.

## 3. Separation of Lineages

The following streams remain distinct:

1. BASTION Evolution
2. ACES Evolution
3. ACES Reconstruction

BASTION lineage outputs are provenance/history/transitions/rejected material and are not automatically Canon items.

A late BASTION snapshot must not be treated as complete historical or causal reconstruction.

## 4. ACES Project-Control Requirement

The future ACES project-control layer must be able to represent and govern, with evidence:

- project state;
- goals and outcomes;
- work items;
- decisions;
- dependencies;
- resources;
- documents and artifacts;
- commitments;
- events;
- risks;
- state transitions;
- authoritative sources;
- required human decisions;
- authorized automated actions;
- execution evidence;
- verification evidence;
- accepted next state.

No BASTION data is required or authorized for implementation of this control layer before the protection gate is lifted.

## 5. Required Future Verification

When the ACES implementation is complete and the explicit protection gate is lifted, BASTION can serve as a controlled external target for verification of project-state management.

Required proof form:

`Verified BASTION State(t) → Authorized ACES Cycle → Evidenced Actions → Verified BASTION State(t+1)`

Until then, the BASTION target remains unchanged.

## 6. Roadmap Placement

The existing Human-to-Digital Reality Operating Layer roadmap remains the active research roadmap.

BASTION project control is a **deferred application/validation boundary**, not a new implementation phase that authorizes touching BASTION.

Any future project-control research must first satisfy the ACES implementation gate and the explicit BASTION protection constraint.

## 7. Gate

**Current gate: BLOCKED**

Condition to proceed:

`ACES OS fully implemented + verified` AND `explicit authorization to reopen BASTION control/validation`

Until both conditions are satisfied:

`BASTION mutation = FORBIDDEN`
`BASTION experimentation = FORBIDDEN`
`BASTION architectural transfer = FORBIDDEN`
`BASTION specification change = FORBIDDEN`

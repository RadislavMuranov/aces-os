# ACES OS — Master Verification Checklist

**Status:** ACTIVE
**Scope:** Connector realization roadmap
**Rule:** unchecked criteria are not accepted.

## A. Governance
- [ ] Scope of the step is explicit.
- [ ] Expected result is explicit.
- [ ] Acceptance criteria are defined before execution.
- [ ] No speculative abstraction was introduced.
- [ ] Decision value is stated.

## B. Security Architecture
- [ ] Identity/principal is explicit.
- [ ] Capability is explicit.
- [ ] Resource and operation are explicit.
- [ ] Scope is bounded.
- [ ] Policy is evaluated.
- [ ] Authority is not inherited from an external tool.
- [ ] Unknown/invalid/expired/revoked authorization fails closed where required.
- [ ] Audit/provenance failure cannot silently produce an accepted state.

## C. Reality Connection
- [ ] Target digital system is identified.
- [ ] Adapter boundary is explicit.
- [ ] External side effects are explicit.
- [ ] Result is captured.
- [ ] External failure is observable.
- [ ] No connector becomes a hidden trust authority.

## D. Execution
- [ ] Intent is distinct from execution.
- [ ] Decision is distinct from authorization.
- [ ] Human choice is not equated with authorization UI.
- [ ] Override availability is not treated as effective control without evidence.
- [ ] DSH/Harness trace is available where used.
- [ ] Tool invocation is attributable.

## E. Verification and State
- [ ] Pre-state is identified.
- [ ] Post-state is identified.
- [ ] Verification criteria are explicit.
- [ ] Verification evidence is retained.
- [ ] AcceptedState is entered only after verification.
- [ ] Failed verification cannot produce an accepted state.
- [ ] Stored context is not assumed to be current validity.

## F. Memory and Continuity
- [ ] Provenance is retained.
- [ ] Staleness can be detected where relevant.
- [ ] Continuity does not override current authority.
- [ ] Memory update follows verified state.

## G. Human Function
- [ ] Required human function is identified for the workflow.
- [ ] Automation does not replace required meaningful human function.
- [ ] Reduction in human operations is not used as the sole success metric.
- [ ] Any claimed human-control property has observable evidence.

## H. Research Yield / Anti-Proliferation
- [ ] The step addresses a concrete failure, capability gap, or decision.
- [ ] Existing artifacts were checked before creating a new entity.
- [ ] Redundant functionality was considered.
- [ ] Deletion/merge is preferred over speculative addition when sufficient.
- [ ] New metrics are prohibited unless required by a concrete acceptance test.
- [ ] New ontology is prohibited unless existing structure cannot represent the required result.

## I. Regression
- [ ] Existing accepted behavior is tested.
- [ ] Security regression passes.
- [ ] State-transition regression passes.
- [ ] Connector failure-path regression passes.
- [ ] No unrelated mutation is included.

## J. Evidence
- [ ] Exact commit SHA recorded.
- [ ] Exact changed artifact recorded.
- [ ] Test/verification output recorded.
- [ ] Failure cases are recorded where applicable.
- [ ] Acceptance decision is reproducible by an independent reviewer.

## Final Gate

A step may be marked **PASS** only when every applicable checklist item has evidence.

`PASS ≠ absence of known failures.`

`PASS = all defined acceptance criteria verified with recorded evidence.`

Absolute zero-defect correctness is not inferred from a checklist; defects remain subject to subsequent regression discovery.

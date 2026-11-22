# B-137 — ACES Continuation Gate Design Contract v0.3

**Artifact status:** WORKING-TREE DRAFT / NOT CANON / NOT ACCEPTED  
**Workstream:** B-137 — actual enforcement boundary  
**Purpose:** Specify the mandatory gate contract before any implementation.  
**Authority boundary:** This artifact does not authorize code changes, runtime authority changes, Canon promotion, or production deployment.  
**Epistemic status:** Design requirements specified; runtime enforcement not proven.

## 1. Current observed boundary

The inspected DSH source contains the dispatch expression in `packages/core/agent-loop/src/agent.ts`:

```ts
const stream = preparedCall?.stream(request) ?? this.loopCtx.llm.stream(request)
```

The existing `PreStepDecision.reject` path and request-error/retry handling are DSH behaviors, not proof of a universal ACES enforcement gate. The inspected `packages/llm/llm/src/index.ts` has a pre-existing dirty modification adding request projection behavior. That file must not be overwritten, reverted, or included in an unrelated change.

## 2. Mandatory invariant

No model dispatch may occur unless a valid `ALLOW` decision is bound to the exact request and execution attempt, its authority/policy/verifier references are valid, and the required provenance evidence is durably confirmed before dispatch.

`ALLOW` is permission for one specific continuation only. It is not proof of execution success, verification success, or `AcceptedState`.

## 3. Required placement

The gate must execute after the final request is built and before selecting either dispatch branch:

```text
buildRequest(request)
  -> evaluate gate
  -> validate decision/request/attempt binding
  -> persist and confirm provenance evidence
  -> final request-identity validation
  -> controlled dispatch boundary
       -> preparedCall.stream(request)
       -> llm.stream(request)
```

Both branches must be guarded by the same enforcement boundary. Any additional reachable model-dispatch path discovered during implementation must also be guarded or proven unreachable. A projection hook alone is insufficient if its errors can enter the normal retry path.

## 4. Result semantics

The implementation must expose distinct control outcomes:

- `ALLOW`: only outcome eligible to continue, after all bindings and evidence are validated.
- `DENY`: policy/authority decision rejects the continuation; dispatch is forbidden.
- `BLOCKED`: permission is not proven because of `UNKNOWN`, verifier/authority failure, malformed result, missing provenance, request-identity mismatch, or evidence persistence failure; dispatch is forbidden.

`DENY` and `BLOCKED` must be terminal for the current continuation and must not be converted into an ordinary LLM request error that a retry listener can override. A retry is a new attempt or an explicitly specified continuation requiring a fresh validity check; permission is never inherited implicitly.

## 5. Request and attempt binding

Every `ALLOW` must bind at least:

- `decisionId`;
- `attemptId`;
- `requestIdentity`;
- `policyRef`;
- `verifierRef`;
- `authorityRef`;
- `provenanceRef`;
- `evidenceRef`.

`requestIdentity` must be derived from a documented canonical representation of every execution- or authorization-relevant field, including model/provider, messages, tools and execution context. Canonicalization or identity failure must block dispatch. Changes to relevant request fields invalidate the decision unless an explicitly tested contract proves the change remains covered. A final identity check must occur immediately before dispatch; no mutation may intervene. If the runtime cannot guarantee this, use an immutable authorized snapshot or an equivalent verified TOCTOU defense.

## 6. Provenance and replay

Required evidence must identify the decision, attempt, request identity, policy, verifier, authority, result and reason, plus the evidence needed to reconstruct the decision. Evidence persistence must be confirmed before dispatch. Partial or uncertain persistence means `BLOCKED`.

Replay must verify evidence integrity, relevant version compatibility and exact agreement between reconstructed request identity and the authorized identity. A missing, corrupt, or non-reconstructable record cannot be converted into `ALLOW`. Do not claim atomicity between evidence persistence and external model dispatch unless the implementation demonstrates it.

## 7. Fail-closed rules

The following all forbid dispatch: `DENY`, `UNKNOWN`, verifier exception, unavailable authority, malformed decision, missing/invalid provenance, failed evidence confirmation, request identity mismatch, or unguarded dispatch path. The number of calls to both dispatch branches must be zero for every denied or blocked test case.

## 8. Required adversarial tests

- `GATE-T01`: DENY -> zero calls to both dispatch branches.
- `GATE-T02`: UNKNOWN -> zero dispatch calls.
- `GATE-T03`: verifier exception -> zero dispatch calls.
- `GATE-T04`: retry listener returns retry after gate refusal -> refused continuation does not resume.
- `GATE-T05`: prepared-call dispatch bypass attempt -> blocked.
- `GATE-T06`: request mutation after evaluation -> re-check or block.
- `GATE-T07`: missing/failed provenance persistence -> zero dispatch calls.
- `GATE-T08`: valid ALLOW -> only the authorized request may dispatch.
- `GATE-T09`: both dispatch branches are shown to be behind the gate.
- `GATE-T10`: replay reconstructs the decision and exact authorized request from evidence.
- `GATE-T11`: decision or request identity substitution -> blocked.
- `GATE-T12`: retry after a previously allowed call follows an explicit revalidation contract.

Tests must use controllable dispatch spies and assert side effects, not merely final status. Mocks of the gate alone do not prove runtime integration. Preserve test output, source revision and environment details.

## 9. Acceptance conditions

Implementation acceptance requires all of the following:

1. Every reachable model-dispatch path is guarded.
2. All negative/adversarial cases above pass against the actual integrated implementation.
3. Retry cannot override a gate refusal.
4. Request identity and TOCTOU protections are demonstrated.
5. Provenance persistence, binding and replay are demonstrated.
6. Existing DSH tests pass and no regression is introduced.
7. The exact source revision, environment, outputs and evidence references are recorded.
8. Existing unrelated dirty changes are preserved.

Passing these conditions establishes only the tested enforcement boundary, not whole-system production readiness or `AcceptedState` by itself.

## 10. Forbidden claims and actions

This design does not establish that the gate exists in runtime. It does not authorize implementation, merge/commit, Canon promotion, production deployment, or a change in runtime authority. No existing dirty file may be reverted or silently incorporated. Do not infer ACES necessity from the existence of this contract.

## 11. Provenance of this artifact

- Repository: `C:\Users\Радислав Муранов\aces-os`
- Repository ref at preparation: detached `HEAD` (exact commit to be recorded in the iteration evidence)
- Relevant DSH repository: `C:\ACES\DSH\deepseek-harness`, branch `master`
- Observed pre-existing dirty files in ACES repository: `spec/governance/CHATGPT-FAILURE-FILTER.md`; `spec/governance/CHATGPT-ITERATION-SELF-AUDIT-RULE.md`
- Observed pre-existing dirty file in DSH repository: `packages/llm/llm/src/index.ts`
- Change scope: this new design artifact only; no source implementation.
- Artifact SHA-256 and post-write repository state: must be recorded by the verification record after read-back.

## 12. Acceptance status

**NOT ACCEPTED.** The artifact requires independent review against the actual source and applicable ACES rules. This document and its existence are not evidence of runtime enforcement. Until a separate acceptance record cites the exact artifact hash and independent findings, B-137 remains blocked.

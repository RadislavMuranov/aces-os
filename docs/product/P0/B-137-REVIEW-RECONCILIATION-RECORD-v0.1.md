# B-137 — Review Reconciliation Record v0.1

**Artifact status:** RECONCILIATION DRAFT / NOT ACCEPTED / NOT CANON  
**Workstream:** B-137 — ACES Continuation Gate  
**Input contract:** B-137-ACES-CONTINUATION-GATE-DESIGN-CONTRACT-v0.3.md  
**Input contract SHA-256:** 253BE75AAFC44729322BE9F202FA891A7C7D252A3DAB502CA3B03CCC763A0895  
**Independent review package:** B-137-IRR-REVIEW-PACKAGE-v0.2.zip  
**Package SHA-256:** 2594905FEEE67D9232002F184B5B7286BD24C7B228259A7D144BABCD03C7E65E  
**Review outcome:** FAIL — BLOCKING DEFECTS IDENTIFIED  
**Scope:** Contract/source reconciliation only. No runtime implementation, tests, Canon promotion, or acceptance decision.

## 1. Evidence boundary

Package integrity and access were verified by matching the downloaded ZIP SHA-256 to the published asset digest and matching the four packaged files to their manifest hashes.

The reviewer performed a bounded source review of the packaged contract and three DSH source files. The reviewer did not check out the full repository, run tests, or observe runtime behavior. Accordingly:
- package integrity is VERIFIED;
- the bounded review is COMPLETED;
- runtime gate existence and behavior are UNKNOWN;
- GATE-T01–T12 execution is NOT PERFORMED;
- contract acceptance and Canon promotion remain NOT AUTHORIZED.

A separate read-only search of the DSH working tree found direct `ctx.llm.stream(...)` calls at:
- `packages/compaction/compaction-basic/src/summarizer.ts:163`;
- `packages/experimental/auto-review/src/index.ts:637`;
- `packages/session/session-title-llm/src/index.ts:281`;
and the agent-loop dispatch expression at `packages/core/agent-loop/src/agent.ts:436`.

The search is evidence of additional call sites in the inspected working tree, not proof that the list is exhaustive or that every call is reachable in every configuration. `packages/llm/llm/src/index.ts` was already modified in the working tree when packaged; its bytes must not be silently treated as repository HEAD.

## 2. Finding-by-finding reconciliation

### F-01 — Incomplete dispatch-path coverage
**Contract sections:** §3, §7, §9(1).  
**Reviewer evidence:** `agent.ts:436` has the prepared-call and LLM dispatch branches; `summarizer.ts:163` directly invokes `ctx.llm.stream(options)` for compaction.  
**Additional bounded scan:** direct calls also found at `experimental/auto-review/src/index.ts:637` and `session/session-title-llm/src/index.ts:281`.  
**Classification:** Contract deficiency confirmed. The contract says additional reachable paths must be guarded, but does not define a complete inventory procedure, reachability classification, or per-path coverage proof. Runtime bypass is not yet proven.  
**Minimum correction:** Require a Dispatch Surface Inventory of all reachable model-dispatch paths, each path's guard boundary and provenance/binding checks, plus tests proving zero external calls for DENY/BLOCKED. Unreachable paths require evidence of unreachability in the declared configuration.  
**Additional source needed:** full DSH tree; all runtime packages and plugin registrations; all LlmRuntime construction/dispatch sites; adapter boundary.

### F-02 — Authorization binding may precede request projection
**Contract sections:** §3, §5, §8(GATE-T06, T08, T09).  
**Reviewer evidence:** `agent.ts:436` dispatches the request; `llm/index.ts:1068–1084` resolves options and projects messages/tools before adapter invocation.  
**Classification:** Contract ambiguity confirmed. The contract requires request identity and final validation but does not define unambiguously whether the identity represents the pre-projection input or the exact provider-bound request. A live bypass is not proven because runtime gate implementation was not reviewed.  
**Minimum correction:** Define the Authorized Dispatch Request as the exact request after all authorization-relevant projections; require immutable authorized snapshot or final identity validation immediately before external I/O. Any later relevant transformation must revalidate or BLOCK. Extend T06/T08 to mutate post-projection messages, tools, model/provider and execution context.  
**Additional source needed:** complete LlmRuntime pipeline, registered projections and order, prepared-call path, final adapter request type and invocation.

### F-03 — Gate refusal and retry taxonomy
**Contract sections:** §4, §7, §8(GATE-T04, T12), §9(3).  
**Reviewer evidence:** `agent.ts:494–500` invokes the `agent/request-error` waterfall with failure and retry-policy context.  
**Classification:** The core requirement already exists in §4: DENY/BLOCKED must be terminal and must not become an ordinary retry-overridable LLM request error. The gap is operational: the contract does not mandate a concrete non-retryable control outcome or fully specify the test oracle. Actual runtime violation is UNKNOWN.  
**Minimum correction:** Define a distinct terminal control outcome or equivalent mechanism excluded from retryable LLM failures. A retry must create a new attempt and perform fresh authorization and provenance binding. T04 must assert that a retry listener returning retry cannot resume dispatch and cannot classify the refusal as retryable.  
**Additional source needed:** all request-error listeners, retry policies, LlmFailure/HarnessError definitions, prepared-call retry behavior.

### F-04 — Lazy iterator TOCTOU
**Contract sections:** §3, §5, §8(GATE-T06, T11).  
**Reviewer evidence:** stream creation and actual adapter I/O may occur at different times; the reviewer identified a possible mutation window before first iterator pull.  
**Classification:** Plausible source-based risk; runtime exploitability is not established. §5 already forbids intervening mutation and requires final identity validation, but does not pin the validation to the actual first external I/O boundary.  
**Minimum correction:** Define the critical I/O point. Revalidate immediately before it or dispatch only from an immutable authorized snapshot. Creating a stream/iterator is not proof that dispatch authorization has been consumed. Add a test that mutates relevant request state between iterator creation and first `next()`; expect revalidation or BLOCK with zero external calls.  
**Additional source needed:** implementations of stream, streamWithRegistration, adapterStream, adapter invocation and callbacks/hooks; cancellation and iterator reuse paths.

### F-05 — Provenance durability and replay protocol
**Contract sections:** §2, §5, §6, §8(GATE-T07, T10).  
**Reviewer evidence:** required evidence fields, persistence confirmation and replay integrity are stated, but the confirmation primitive and failure protocol are not defined.  
**Classification:** Partial contract underspecification confirmed. §6 already requires evidence fields, integrity, version compatibility and request-identity agreement; it does not fully operationalize durable confirmation and ambiguous/partial failure. Runtime storage behavior is UNKNOWN.  
**Minimum correction:** Define minimum evidence schema/version, integrity fields, durable confirmation semantics, timeout/partial-write/unknown-result behavior, replay checks and fail-closed outcomes. Explicitly disclaim atomicity between evidence persistence and external model dispatch unless proven. Add fault-injection tests for partial writes, lost confirmation, corruption, incompatible version and identity mismatch.  
**Additional source needed:** actual evidence store, write/read APIs, durability guarantees, confirmation primitive, replay implementation and request identity canonicalization.

### F-06 — Adversarial tests are not operationally specified
**Contract sections:** §8, §9.  
**Reviewer evidence:** GATE-T01–T12 are concise intent statements; the bounded review did not execute them or inspect all repository tests.  
**Classification:** Contract test-specification gap confirmed. It is not established that corresponding tests are absent elsewhere in DSH.  
**Minimum correction:** For every test, specify setup, injected fault/action, observation points, required assertions, forbidden side effects and evidence output. Add explicit tests for all reachable dispatch paths, post-projection binding, refusal/retry separation, lazy iterator TOCTOU and provenance fault cases. Record source revision, working-tree state, environment and test output.  
**Additional source needed:** relevant unit/integration tests, test runner configuration, fixtures and CI definitions.

## 3. Minimal contract correction set

- **M-01 Dispatch Surface Inventory:** enumerate all reachable dispatch paths and prove each guarded or unreachable.
- **M-02 Final Authorized Request:** bind ALLOW to the exact post-projection request sent to the adapter.
- **M-03 Terminal Refusal Semantics:** make DENY/BLOCKED non-retryable control outcomes; new attempts require fresh authorization.
- **M-04 TOCTOU Boundary:** define and protect the exact pre-I/O authorization point.
- **M-05 Provenance Protocol:** specify evidence schema, durable confirmation, failure semantics and replay verification.
- **M-06 Executable Acceptance Matrix:** turn all test intentions into deterministic test specifications with observable side-effect assertions.

These are contract changes only. They do not authorize implementation, merge/commit, deployment, runtime authority changes, or Canon promotion.

## 4. Independent verification criteria

A reviewer independent of the author must inspect the exact revised contract hash and verify:
1. Every discovered dispatch path is inventoried, guarded or proven unreachable in a specified configuration.
2. ALLOW binds decision, attempt, provenance and the exact final provider-bound request.
3. DENY, UNKNOWN and all listed failure conditions yield zero external dispatch calls.
4. Retry cannot override a gate refusal; a new attempt requires fresh authorization.
5. The lazy-iterator mutation case is tested at the actual external I/O boundary.
6. Provenance confirmation and replay have deterministic success/failure semantics.
7. Each invariant maps to an adversarial test with explicit observable assertions.
8. Claims remain bounded to the tested enforcement boundary and do not imply whole-system production readiness or AcceptedState.

The independent reviewer must use the actual relevant source tree, not rely solely on the previous review summary. Test execution is required before implementation acceptance; contract review alone does not prove runtime enforcement.

## 5. Reconciliation disposition

**Reconciliation result:** findings mapped; minimal contract corrections and verification criteria defined.  
**Contract v0.3:** NOT ACCEPTED.  
**Runtime implementation:** NOT VERIFIED.  
**GATE-T01–T12:** NOT EXECUTED.  
**Canon promotion:** NOT AUTHORIZED.  
**Next execution node:** NOT AUTHORIZED until this reconciliation record is read back, integrity-checked, and formally reconciled under the applicable ACES process.

No source implementation was changed as part of this record.
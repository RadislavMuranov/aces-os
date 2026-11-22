# B-137 — ACES Continuation Gate Adversarial Review Record v0.1

**Status:** LOCAL SOURCE-BACKED ADVERSARIAL REVIEW / NOT INDEPENDENT / NOT ACCEPTED  
**Review target:** `B-137-ACES-CONTINUATION-GATE-DESIGN-CONTRACT-v0.3.md`  
**Target SHA-256:** `253BE75AAFC44729322BE9F202FA891A7C7D252A3DAB502CA3B03CCC763A0895`  
**Review date:** 2026-10-10  
**Decision:** **FAIL — BLOCKING DESIGN GAPS IDENTIFIED**  
**Governance limitation:** This analysis does not satisfy the separate-reviewer requirement recorded in the IRR method. It is not independent acceptance and does not authorize implementation.

## 1. Evidence and inspected revisions

- Target file was read from `C:\Users\Радислав Муранов\aces-os\docs\product\P0\B-137-ACES-CONTINUATION-GATE-DESIGN-CONTRACT-v0.3.md` (125 lines).
- Independent local SHA-256 computation matched the expected target hash exactly.
- DSH repository: `C:\ACES\DSH\deepseek-harness`, HEAD `5badb15009ae1756c3afe0ae0cef1faafc290ccc`.
- ACES repository: `C:\Users\Радислав Муранов\aces-os`, HEAD `686bf75f91789ca9055fa6d07a957453093cb339`.
- Observed DSH dirty file `packages/llm/llm/src/index.ts` was read only and not modified.
- Existing ACES dirty governance files were not modified. No source changes, tests, commits, or runtime integration were performed.

## 2. Findings

### F-01 — CRITICAL: Direct LLM callers are outside the specified agent-loop gate

**Evidence:** `packages/core/agent-loop/src/agent.ts:425-436` builds the request and selects `preparedCall?.stream(request) ?? this.loopCtx.llm.stream(request)`. But `packages/compaction/compaction-basic/src/summarizer.ts:163` independently dispatches through `ctx.llm.stream(options)`.

**Failure scenario:** A compaction summarization call dispatches a model request without traversing a gate implemented only around the two agent-loop branches. GATE-T01–T09 could pass while this path remains unguarded.

**Required correction:** Define the protected scope explicitly and enumerate every production caller. For a global “no model dispatch without ALLOW” invariant, enforce at a shared mandatory boundary that all callers—including prepared calls and auxiliary compaction calls—cannot bypass. Add a compaction-call denial test asserting zero adapter dispatch.

### F-02 — CRITICAL: The authorized request identity may not bind the actual provider-bound request

**Evidence:** `packages/llm/llm/src/index.ts:1071,1076,1079,1090,1096` transforms messages/tools through file projection, image projection, tool-update projection and registered projection hooks, then calls `dispatch(this.forAdapter(projectedOptions, adapter))`.

**Failure scenario:** The agent-loop gate authorizes the request before these transformations. A downstream projection changes an authorization-relevant message, tool, or adapter-specific field, but dispatch still proceeds under the earlier ALLOW.

**Required correction:** Bind authorization to the final provider-bound representation, or define and verify a provenance-bound projection chain whose output identity is covered by the decision. Add a test that mutates an authorization-relevant field in a projection and proves dispatch is blocked or the final request is separately authorized.

### F-03 — CRITICAL: Gate refusal can be normalized into a retryable LLM failure at the adapter boundary

**Evidence:** In `packages/llm/llm/src/index.ts`, the projection/dispatch path is inside an adapter-owned try/catch; failures are yielded as `adapterFailureChunk`. In `packages/core/agent-loop/src/agent.ts`, an LLM error can reach `agent/request-error`, whose action may be `retry`.

**Failure scenario:** A gate is placed inside the LLM adapter try/catch or implemented as a projection hook. DENY/BLOCKED is converted into an ordinary failure chunk; a retry listener returns `retry`, causing a new request and potentially bypassing the refusal.

**Required correction:** Specify an unambiguous non-retryable control-plane path for DENY/BLOCKED that cannot be normalized into an ordinary adapter failure. Test the real integrated path with a retry listener that always returns retry; assert no dispatch occurs after refusal.

### F-04 — HIGH: TOCTOU acceptance test does not identify the actual last safe point

**Evidence:** `agent.ts:436` obtains an async stream; `live.start()` runs before `for await` consumes it. The LLM runtime’s adapter dispatch occurs later, after request projections.

**Failure scenario:** A request is checked, then mutable request data or a projection changes before the lazy stream reaches adapter dispatch.

**Required correction:** Define the exact last safe point and enforce an immutable authorized snapshot or revalidation at that point. Strengthen GATE-T06 to mutate the request after stream construction but before the first iterator pull/adapter dispatch, then assert zero unauthorized dispatches.


### F-05 — HIGH: “Durably confirmed” provenance lacks a testable durability contract

**Evidence:** Sections 2, 6, 7 and GATE-T07 require durable confirmation and fail-closed persistence, but do not define the storage durability level, confirmation receipt, integrity binding, or crash/recovery semantics.

**Failure scenario:** A persistence API reports success while evidence is buffered, incomplete, or not recoverable after process failure; dispatch proceeds without replayable proof. A crash after evidence confirmation but before dispatch may also create an ambiguous attempt state.

**Required correction:** Define what “durably confirmed” means for the selected store, how confirmation is bound to the evidence hash and attempt, and how crash/replay handles the pre-dispatch state. Add fault-injection tests for partial write, uncertain acknowledgement, corruption, and crash between evidence confirmation and dispatch.

## 3. Test coverage assessment

GATE-T01–T12 are specified but were not executed: no gate implementation was claimed or changed. As written, the suite does not explicitly cover:
- a direct auxiliary LLM caller such as compaction;
- post-authorization mutation by file/image/tool/registered projection;
- gate refusal passing through the adapter failure-chunk conversion and retry listener;
- mutation between async stream construction and first adapter dispatch;
- partial/uncertain durable evidence writes and crash/replay around the dispatch boundary.

## 4. Review conclusion and restrictions

The contract contains valuable safety requirements, including explicit DENY/BLOCKED outcomes, request/attempt binding, provenance, replay, and a prohibition on treating ALLOW as AcceptedState. However, the concrete source paths above expose blocking gaps between those requirements and the proposed agent-loop placement.

**Local adversarial verdict:** `FAIL — BLOCKING DESIGN GAPS IDENTIFIED`. This is a source-backed analysis, not an independent reviewer’s verdict under IRR. Independent review must be rerun against this exact target hash and the cited source files.

**Next action:** revise the design contract (new version/hash; preserve v0.3), then submit the exact target and source evidence to a separate reviewer. Do not implement, merge/commit, promote to Canon, or claim acceptance until the applicable independent review and ACES acceptance transition are complete.

## 5. Integrity

This record is a new working-tree evidence artifact. It does not alter the target contract or DSH source. Verify its own hash and repository status after read-back; no commit is authorized by this record.

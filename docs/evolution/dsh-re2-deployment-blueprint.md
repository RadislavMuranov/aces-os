# DSH-RE2 — Deployment Blueprint

**Status:** ARCHITECTURAL CONTRACT — READY FOR IMPLEMENTATION PHASES  
**Date:** 2026-09-01  
**Baseline DSH:** deepseek-ai/deepseek-harness @ dd6322d604e00eec1ba5e0c8541159906a21094a  
**ACES contract:** ASA v0 (data-model.md) + MASTER-PROTOCOL + DSH-RE2 Final Specification  
**R11 status:** BLOCKED (no live execution evidence)

This document is the production-oriented deployment blueprint and executable implementation contract for integrating DeepSeek Harness (DSH) as a replaceable execution substrate of ACES OS. It does not implement the runtime integration.

---

## 1. Non-Negotiable Ownership

### ACES owns
- Constitution
- Authority
- Authorization
- Decision
- Evidence
- Provenance
- Verification
- AcceptedState
- Revocation
- Audit integrity
- Policy

### DSH provides
- Cordis runtime substrate
- Context / Scope
- Capability graph
- Agent runtime
- Session / Trajectory
- Tools
- Profiles
- Bundles
- Patches
- Approval (interaction primitive only)
- Sandbox (enforcement primitive only)

### Invariants (from Final Specification + ASA v0)
- DSH Event ≠ ACES Evidence
- DSH Approval ≠ ACES Authority
- DSH Sandbox ≠ ACES Security PASS
- LLM output ≠ ACES Decision
- Plugin registration ≠ Authorization
- GitHub/Grok identity ≠ ACES Trust Authority (I8)
- Only ACES Verification may transition to AcceptedState
- Fail-closed on missing policy, audit, revocation store, evidence, provenance, or verification

Any contradiction with ASA v0 I1–I8 or Final Specification §5 blocks this blueprint.

---

## 2. Deployment Topology

```text
ACES Control Plane
  |
  v
ACES Authorization / Decision (ASA evaluation)
  |
  v
ACES Context Compiler
  |
  v
DSH Composition Layer (Profile / Bundle / Patch / Adapter)
  |
  v
DSH Runtime / Cordis
  |
  v
Agent / LLM / Tools
  |
  v
Sandbox / OS
```

### Parallel control and data paths

| Path | Direction | Owner | Purpose |
|------|-----------|-------|--------|
| Session / Trajectory | DSH → ACES Adapter | DSH produces, ACES consumes | Ordered execution events |
| Evidence / Provenance | Adapter → ACES Evidence store | ACES | Canonical evidence objects |
| Verification | ACES Verification → AcceptedState | ACES | Sole transition authority |
| Audit | All layers → AuthorizationEvent | ACES | Append-only, never grants |
| Secrets | ACES SecretObject → controlled injection | ACES | Never ambient in DSH |
| Observability | All → metrics/logs (non-authoritative) | Shared (read-only for DSH) | Telemetry only |

---

## 3. Trust Boundaries

| Boundary | Inside (trusted) | Outside (untrusted) | Crossing rule |
|----------|------------------|---------------------|---------------|
| TB-1 ACES Authority | Constitution, Policy, Authority, Authorization, Decision, Verification, AcceptedState | Everything else | Only ACES Decision ALLOW + Verification PASS can produce AcceptedState |
| TB-2 ACES Evidence | Evidence store, Provenance graph, AuthorizationEvent log | DSH Session events, LLM output, tool results | Events become Evidence only via Evidence Adapter + provenance binding |
| TB-3 Capability issuance | Capability records, Revocation store, Policy engine | DSH plugin registry, approval answers | Capability use requires fresh ASA evaluation (I1–I5) |
| TB-4 Runtime composition | Compiled profile/bundle/patch identity under ACES Context Compiler | Raw DSH home/launcher overlays | Only ACES-compiled composition is admissible |
| TB-5 Execution substrate | DSH Cordis instance under authorized scope | Host OS, network, external LLM providers | Sandbox + ACES capability scope constrain; danger-full-access forbidden in hardened mode |
| TB-6 Identity | ACES Identity/Principal (authenticator_id ∈ {architectural_authority_human, implementation_agent}) | GitHub identity, Grok identity, DSH session identity | Auth ≠ Authority (I8) |

No trust is inherited from DSH Approval, Sandbox report, plugin load, or model output.

---

## 4. Process / Container Boundaries

| Component | Process / Container | Isolation | Notes |
|-----------|---------------------|-----------|-------|
| ACES Control Plane | Dedicated process or service | Highest privilege within ACES domain | Owns policy, decision, verification |
| ACES Authorization Engine | Same or co-located with Control Plane | Fail-closed to audit/revocation stores | ASA evaluation order mandatory |
| ACES Context Compiler | Control Plane or sidecar | Read-only to DSH composition artifacts | Emits sealed runtime composition identity |
| DSH Runtime (Cordis) | Separate process / container | Capability-scoped; no ambient ACES credentials | Receives only effective capability set |
| Agent Loop / LLM Provider | Inside DSH Runtime or nested | No direct AcceptedState write path | Output is trajectory only |
| Tools / Sandbox | Nested under DSH or separate sandbox provider | File-effect modes only; network/process limited by ACES policy | Partial enforcement treated as non-PASS |
| Evidence Adapter | ACES-owned process | Reads DSH events, writes ACES Evidence | Must not promote events without provenance |
| Audit / Provenance store | Append-only store | Write only from ACES paths | Unavailable → DENY protected ops |
| Secrets | ACES SecretObject store | Injected ephemerally; never persisted in DSH session | Revocable |

Minimum isolation: ACES decision path and DSH execution path must not share writable memory or ambient credentials.

---

## 5. Data Flows and Control Flows

### Control flow (canonical)

1. ACES Intent (request_id, principal, resource, operation, context)
2. ASA evaluation → Decision (ALLOW | DENY)
3. On ALLOW: Context Compiler produces sealed composition (profile + bundles + patches + effective capability set)
4. DSH Composition Layer loads only the sealed composition
5. DSH Runtime executes under that composition
6. Session events emitted
7. Evidence Adapter selects/transforms events + external observations → Evidence objects + provenance links
8. Verification consumes Evidence + Decision contract
9. Only Verification PASS → AcceptedState transition

### Data flow matrix (summary)

| From | To | Payload | Authority |
|------|----|---------|-----------|
| Client / Human | ACES Control Plane | Intent + identity proof | Non-authoritative until verified |
| ACES Auth | Context Compiler | Decision + effective capability set | Authoritative |
| Context Compiler | DSH Composition | Sealed profile/bundle/patch + capability surface | Authoritative |
| DSH Runtime | Evidence Adapter | Ordered session events, tool call/result, session_id | Non-authoritative telemetry |
| Evidence Adapter | Evidence store | EvidenceObject + provenance | Authoritative after adapter |
| Verification | AcceptedState | PASS/FAIL + evidence refs | Sole authority for transition |
| All | AuthorizationEvent | Audit record | Append-only; never grants |

---

## 6. Core Semantics

### Identity
- ACES Identity via accepted authenticator_id only.
- implementation_agent authenticates execution principal only; grants nothing.

### Capability
- Opaque server-side capability_id.
- MULTI-USE within [not_before, not_after].
- Checked on every request for scope, expiration, revocation.

### Authorization / Policy
- Fresh evaluation every request.
- Missing/invalid/conflict policy → DENY.
- Policy engine unavailable → DENY.

### Provenance / Evidence
- DSH events are trajectory.
- Evidence Adapter is the sole promotion path.
- Missing evidence or provenance → no AcceptedState.

### Audit
- AuthorizationEvent append-only.
- Audit unavailable for protected ops → DENY.

### Secret handling
- Secrets live in ACES SecretObject.
- Injected only under ALLOW Decision and scoped capability.
- Never written into DSH durable session or model context unless explicitly authorized and redacted in audit.

### Revocation
- Per-capability kill-list.
- Revocation store unavailable → DENY.
- Stale/revoked capability → DENY.

### Failure semantics
- Fail-closed at every boundary listed in §17 negative tests.
- No silent promotion, no cached ALLOW, no ambient GitHub privilege.

---

## 7. DSH Adaptation Layers

| Layer | Mechanism | Upstream modification | ACES control |
|-------|-----------|-----------------------|--------------|
| Profile | dsh.profile.bundles selection | None | Context Compiler selects |
| Bundle | Ordered layers | None | Sealed in composition identity |
| Patch | Row replace/insert | None | Only ACES-approved patches |
| Plugin | External capability registration | None | Registration ≠ Authorization; must map to ACES Capability |
| Provider | LLM / Tool / Sandbox / Approval / Loop replacement | None | Interface contract + ACES scope |
| Fork boundary | Source/runtime fork | Yes | Explicit decision; version pin changes |

Preferred order: reuse → configure → compose → replace → extend → fork → rewrite.

---

## 8. Deployment Modes

| Mode | Description | Isolation | Use |
|------|-------------|-----------|-----|
| local-first development | Single host, developer credentials, danger-full-access forbidden for acceptance tests | Process separation | Iteration |
| isolated execution | Containerized DSH under ACES-compiled profile; no host ambient secrets | Container + capability scope | CI / negative tests |
| production single-node | ACES Control Plane + DSH Runtime on one node with process/container boundaries | Full TB matrix | Initial production |
| future distributed | Separate nodes for Control Plane, Runtime, Evidence store | Network trust boundaries + mTLS | Scale-out (not required for R11) |

---

## 9. Minimum Viable Deployment (MVD)

- ACES Authorization Engine (ASA evaluation order)
- Context Compiler emitting sealed composition identity
- DSH Runtime pinned to baseline commit
- Single deterministic test capability
- Evidence Adapter producing ACES Evidence from selected events
- Verification gate
- Append-only AuthorizationEvent store
- Revocation store
- request_id correlation end-to-end

No distributed components. No danger-full-access. No direct model→AcceptedState path.

---

## 10. Hardened Deployment

- All MVD components
- Separate containers for Control Plane, DSH Runtime, Evidence/Audit stores
- Network isolation; only authorized ports
- Secrets via ephemeral injection; no long-lived DSH credentials for ACES resources
- Sandbox mode restricted to workspace-write or stricter; partial enforcement = non-PASS
- Continuous revocation and policy freshness checks
- Observability without elevating telemetry to Evidence
- Upgrade/rollback via version-pinned composition (see §13)

---

## 11. Resource Boundaries and Failure Isolation

| Resource | Bound | Failure isolation |
|----------|-------|-------------------|
| CPU / memory (DSH) | cgroup / container limits | OOM or throttle does not affect ACES decision path |
| Disk (workspace) | Sandbox policy | Write outside scope denied |
| Network | Default deny; explicit allow-list | DSH cannot reach ACES control ports without policy |
| Time | Capability temporal window | Expired → DENY |
| Concurrent sessions | Per-principal / per-capability limits | Exhaustion → DENY new sessions |

Failure of DSH Runtime, LLM provider, or sandbox must leave ACES Control Plane able to record BLOCK and refuse AcceptedState.

---

## 12. Upgrade / Rollback Strategy

1. Pin all versions (§13).
2. Deploy new composition identity alongside old.
3. Route new Intents to new composition only after verification of negative + positive tests.
4. Rollback = revert routing to previous sealed composition identity; no in-place mutation of live composition.
5. Capability and policy versions remain independent; revoked capabilities stay revoked across upgrades.

---

## 13. Version Pinning

| Artifact | Pin |
|----------|-----|
| DSH commit | dd6322d604e00eec1ba5e0c8541159906a21094a |
| ACES contract version | ASA v0 (data-model.md) + DSH-RE2 Final Specification |
| Runtime profile | Explicit profile id recorded in composition identity |
| Bundle versions | Ordered list of bundle ids + content hashes |
| Patch set | Ordered patch ids + content hashes |
| Adapter version | ACES DSH adapter semantic version + commit |
| Context Compiler output | Sealed composition identity (hash of profile+bundles+patches+capability surface) |

All pins must appear in every R11 evidence package.

---

## 14. Evidence Requirements (every execution)

Mandatory fields in the evidence package:

- request_id
- authorization Decision (decision_id, outcome, reason_code, capability_id, policy_id/version)
- effective capability set
- runtime composition identity (profile + bundles + patches + adapter)
- DSH session_id
- ordered session events
- tool call / tool result
- execution result
- provenance links (EvidenceObject ↔ events ↔ Decision)
- verification result
- final ACES state (AcceptedState or BLOCK reason)

Absence of any required field → verification FAIL → no AcceptedState.

---

## 15. R11 Instrumentation Contract

Instrumentation must capture the fields in §14 at the following points:

1. Pre-authorization (request accepted)
2. Post-Decision (ALLOW/DENY recorded)
3. Post-Context-Compile (composition identity sealed)
4. DSH session start (session_id)
5. Every tool call and result
6. Session close / final events
7. Evidence Adapter emission
8. Verification outcome
9. AcceptedState transition or BLOCK

Raw logs and structured evidence packages must be retained as Evidence Memory artifacts. No PASS claim without the package.

---

## 16. R11 Acceptance Gate (exact path)

```text
ACES Intent
  → Authorization PASS
  → Context Compilation
  → DSH Execution
  → Session Event
  → Evidence Adapter
  → Provenance
  → Verification PASS
  → AcceptedState
```

All steps must be evidenced by the package in §14. Source inspection alone is insufficient.

---

## 17. Mandatory Negative Tests

| ID | Test | Expected |
|----|------|----------|
| N1 | Authorization DENY | No DSH execution; no AcceptedState |
| N2 | Unauthorized capability | BLOCK |
| N3 | Execution failure | No AcceptedState |
| N4 | Missing evidence | Verification FAIL; no AcceptedState |
| N5 | Missing provenance | Verification FAIL; no AcceptedState |
| N6 | Verification failure | No AcceptedState |
| N7 | Model direct-accept attempt | BLOCK |
| N8 | DSH approval without ACES authorization | BLOCK |
| N9 | Sandbox failure | BLOCK or non-PASS |
| N10 | Partial sandbox enforcement | Treated as non-PASS for security claims |
| N11 | Stale/revoked capability | DENY |
| N12 | Unavailable policy engine | DENY |
| N13 | Unavailable audit/evidence subsystem | DENY / no AcceptedState |

All must be executable in the instrumented environment before R11 can be marked PASS.

---

## 18. Matrices and Plans

### Component inventory
- ACES Control Plane
- ASA Authorization Engine
- Context Compiler
- DSH Composition Layer / Adapter
- DSH Cordis Runtime
- Agent Loop / LLM Provider / Tool Provider
- Sandbox Provider
- Approval Provider (subordinate)
- Evidence Adapter
- Evidence / Provenance store
- AuthorizationEvent (Audit) store
- Revocation store
- SecretObject store
- Observability sink (non-authoritative)

### Trust-boundary matrix
See §3.

### Capability matrix
- ACES Capability (authoritative) ⊇ DSH effective capability surface
- DSH plugin capability ⊂ ACES Capability after mapping and Decision
- No ambient or self-asserted capability

### Data-flow matrix
See §5.

### Failure matrix
See §6 Failure semantics + §17.

### R11 test matrix
Positive path (§16) + all N1–N13.

### Implementation phases
1. Instrument and pin MVD components (no live claim yet)
2. Local-first + isolated execution of positive path with full evidence package
3. Execute N1–N13; retain raw evidence
4. Hardened single-node
5. Only after evidence packages exist: update R11 gate document to PASS or FAIL

### Rollback plan
See §12. Immediate rollback target is previous sealed composition identity.

### Acceptance gate
R11 remains BLOCKED until live DSH runtime produces the evidence package satisfying §14–§17. This blueprint does not claim R11 PASS.

---

## 19. Canon Validation

Checked against:
- DSH-RE2 Final Specification (ownership, invariants, canonical path)
- R6 / R7 / R9 / R10 / R11 gate documents
- ASA v0 data-model (I1–I8, evaluation order, failure matrix)
- MASTER-PROTOCOL (evidence precedes architecture; owner boundaries)

**Result:** No contradiction identified. Blueprint does not grant DSH any ACES Authority, does not weaken fail-closed semantics, and does not treat GitHub/Grok identity as Trust Authority.

If future implementation introduces a path that violates I1–I8 or Final Specification §5, that change is BLOCKED until Canon is updated via explicit Authority Decision.

---

## 20. Explicit Non-Claims

- No runtime integration is implemented by this document.
- R11 is not PASS.
- DSH is not promoted to constitutional or epistemic authority.
- Sandbox full / approval allowed-once / plugin registration remain non-equivalent to ACES Security PASS / Authority / Authorization.

---

**End of DSH-RE2 Deployment Blueprint.**

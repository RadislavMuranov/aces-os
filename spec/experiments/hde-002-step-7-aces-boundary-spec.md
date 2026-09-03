# HDE-002 — Step 7: ACES Boundary Specification

**Status:** STEP 7 COMPLETE — ACES BOUNDARY SPEC  
**Experiment:** HDE-002  
**Date:** 2026-09-03  
**Branch:** `architecture/priority-realization-roadmap-v2`

## 1. Purpose

Define the minimum defensible architectural boundary of ACES after Steps 0–6.

The boundary must distinguish what ACES owns from what may be delegated to external Model, Agent, Harness, Tool, Execution and Verification systems.

## 2. Boundary principle

> ACES does not need to own intelligence or execution. ACES must own the governed transition by which external execution becomes accepted canonical ACES state.

## 3. External execution domain

The following may be external and replaceable:

`MODEL → AGENT → HARNESS → TOOLS → EXECUTION`

External systems may also provide local context, memory, sandboxing and verification.

Their capability, autonomy, permission or completion signal does not transfer ACES authority.

## 4. ACES-owned authority domain

ACES owns, or must be able to independently enforce, at minimum:

1. **Epistemic Authority** — criteria and authority for accepting propositions/state as knowledge within ACES.
2. **Decision Authority** — authority to bind a proposed course of action to an ACES-governed decision.
3. **Execution Authority** — authority to permit consequential side effects at the ACES boundary.
4. **Evidence / Provenance** — evidence lineage sufficient to reconstruct why an accepted state was accepted.
5. **Independent Verification** — verification that is not reducible to an agent's self-reported completion.
6. **Acceptance** — explicit transition from verified result to accepted ACES state.
7. **Canonical State** — ACES-owned representation of accepted reality.
8. **Policy / Governance** — rules determining when the above transitions are allowed.

## 5. Canonical transition

The minimum governed transition is:

`INTENT → PROPOSAL → AUTHORIZATION → EXECUTION → OBSERVATION → EVIDENCE → VERIFICATION → ACCEPTANCE → CANONICAL STATE`

Each transition is semantically distinct.

## 6. Non-equivalences

`CAPABILITY ≠ PERMISSION`

`PERMISSION ≠ APPROVAL`

`APPROVAL ≠ EXECUTION`

`EXECUTION ≠ VERIFICATION`

`VERIFICATION ≠ ACCEPTANCE`

`ACCEPTANCE ≠ CANONICALITY`

Therefore no external runtime event, completion signal, approval, test result or memory write may independently establish canonical ACES reality.

## 7. Trust boundary

The minimum trust boundary is:

`EXTERNAL AGENT/HARNESS/TOOLS/EXECUTION/VERIFICATION → ACES ACCEPTANCE BOUNDARY`

External systems are untrusted with respect to ACES canonicality unless their specific authority is explicitly delegated and their result satisfies ACES policy/evidence requirements.

This is consistent with the established ACES invariant:

`external capability ≠ ACES authority`

## 8. What ACES must NOT assume

ACES must not assume that:

- model confidence implies truth;
- agent completion implies correctness;
- tool success implies desired state;
- approval implies correctness;
- runtime permission implies ACES authority;
- external memory is canonical knowledge;
- external verification is sufficient for canonicalization;
- an event log is itself the source of truth.

## 9. Minimal ACES interface to an external runtime

The boundary should expose a governed contract approximately equivalent to:

### Input to runtime

- authorized intent/task;
- scoped capabilities;
- policy constraints;
- execution budget;
- required evidence/verification criteria;
- authority/delegation context.

### Runtime output

- proposed actions;
- execution receipts/results;
- observable effects;
- evidence/provenance;
- verification artifacts;
- failures/uncertainties;
- identity and delegation context.

### ACES decision

ACES independently determines:

`REJECT | ACCEPT-TRANSIENT | ACCEPT-CANONICAL | ESCALATE`

The exact state machine is a later implementation/specification concern; the architectural distinction is mandatory.

## 10. Canonicalization rule

> A verified external result becomes canonical ACES reality only through an explicit ACES acceptance transition satisfying declared authority, policy, evidence and verification requirements.

This does not claim that ACES determines objective truth. It defines ACES's authority over its own operational/canonical state.

## 11. Failure semantics

The boundary is fail-closed for missing authority/evidence/verification.

Examples:

- missing authorization → no consequential execution;
- missing required evidence → no canonicalization;
- failed verification → no canonicalization;
- conflicting authoritative evidence → escalation/uncertain state;
- ambiguous delegation → deny or escalate;
- external runtime reports completion without sufficient proof → non-canonical result;
- canonical state cannot be updated consistently → preserve prior canonical state and record failure.

## 12. MCP / connector rule — UPDATED

The ACES boundary does not require MCP as a universal mechanism.

The governing integration principle is now:

> **ACES SHALL prefer the most direct, local, native, first-party or otherwise controlled integration mechanism that adequately satisfies its capability, security, provenance, observability and governance requirements.**

The preferred ordering is:

`LOCAL → NATIVE / FIRST-PARTY → DIRECT CONNECTOR → MCP → OTHER PROTOCOL / BRIDGE`

This is **CLA-first, not CLA-only**. The ordering is a security and architectural optimization, not an absolute prohibition against MCP.

MCP MAY be used when it provides material interoperability, capability availability, ecosystem leverage, deployment practicality, portability, operational economics, standardized integration, or materially lower implementation complexity that is not adequately provided by the available CLA path.

MCP remains a capability transport and interoperability mechanism, not an ACES Authority mechanism. MCP authorization does not establish ACES Epistemic Authority, Decision Authority, Execution Authority, Acceptance Authority or Canonicality.

ACES SHALL avoid introducing MCP merely where an equivalent or superior controlled CLA path already exists, particularly where doing so would add unnecessary trust boundaries, credential/token propagation, confused-deputy opportunities, attack surface, protocol hops, provenance ambiguity or operational complexity.

The decision to use MCP remains subordinate to ACES Policy, Authorization, Security, Provenance, Verification and Acceptance requirements.

## 13. Connector Plane

ACES SHALL maintain a protocol-independent Connector Plane:

```text
                 ACES AUTHORITY
                       │
             ┌─────────▼─────────┐
             │ Capability Router │
             │ / Connector Plane │
             └─────────┬─────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
       LOCAL        NATIVE        MCP
          │            │            │
          └────────────┼────────────┘
                       │
                 DIGITAL WORLD
```

The Connector Plane determines **how ACES reaches the digital world**.

It does not determine **whether ACES is authorized to accept what happens there as canonical reality**.

## 14. Authority Boundary

The canonical ACES control flow is:

```text
             ACES AUTHORITY
                    │
        ┌───────────┴───────────┐
        │                       │
    AUTHORIZATION           POLICY
        │                       │
        └───────────┬───────────┘
                    │
              CONNECTOR PLANE
                    │
       ┌────────────┼────────────┐
       │            │            │
     Local        Native        MCP
       │            │            │
       └────────────┼────────────┘
                    │
                EXECUTION
                    │
               OBSERVATION
                    │
                 EVIDENCE
                    │
              VERIFICATION
                    │
               ACCEPTANCE
                    │
             CANONICAL REALITY
```

The canonical transition is therefore:

**INTENT → AUTHORIZATION → CONNECTOR → EXECUTION → OBSERVATION → EVIDENCE → VERIFICATION → ACCEPTANCE → CANONICAL REALITY**

No connector or protocol may bypass the Authority, Evidence, Verification or Acceptance boundaries.

## 15. Authority / Connector invariants

The following are mandatory architectural distinctions:

`AUTHORITY ≠ CONNECTOR`

`AUTHORITY ≠ PROTOCOL`

`AUTHORITY ≠ CAPABILITY`

`AUTHORITY ≠ EXECUTION`

`MCP ≠ AUTHORITY`

`CLA-FIRST ≠ CLA-ONLY`

**Authority remains transport-independent and ACES-owned.**

No integration mechanism receives ACES Authority merely by being native, local, standardized, trusted by a vendor, or technically capable.

## 16. Security invariant

ACES SHALL treat additional integration layers as additional security and epistemic boundaries.

Therefore:

> **The existence of a standardized protocol is not sufficient justification for introducing it into the execution path.**

Where a direct and adequately governed CLA path exists, introducing MCP solely for convenience SHALL be considered an unnecessary architectural and security dependency.

## 17. Architectural consequence

ACES should remain model-, vendor-, harness- and connector-independent at the authority boundary.

DSH may serve as an Execution Kernel. Orca may serve as fleet/execution orchestration. ZCode, Claude Code, Codex, OpenCode or other runtimes may serve as external execution substrates.

None receives ACES canonical authority merely by integration.

## 18. Step 7 gate

**PASS CONDITION:** a minimal, implementation-neutral ACES boundary is defined such that external execution can be delegated while authority over acceptance and canonical state remains explicit, independently verifiable and fail-closed; connector/protocol selection remains subordinate to this authority boundary.

**RESULT: PASS.**

## 19. Step 7 conclusion

The minimum defensible ACES architectural boundary is not another agent runtime.

It is the **Authority–Evidence–Reality boundary** that governs the transition:

`EXTERNAL EFFECT → EVIDENCE → VERIFICATION → ACES ACCEPTANCE → CANONICAL REALITY`

The integration mechanism is selected independently through a CLA-first Connector Policy:

`LOCAL → NATIVE / FIRST-PARTY → DIRECT CONNECTOR → MCP → OTHER PROTOCOL / BRIDGE`

with MCP permitted where its material value justifies the additional boundary.

**Final Step 7 invariant:**

> **ACES does not delegate Authority to the integration protocol. ACES chooses the transport according to architectural optimality, security, capability and interoperability requirements, while Authority always remains above the transport layer.**

This is the boundary to carry into HDE-002 Step 8 — FINAL VERDICT.

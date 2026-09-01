# DSH-RE2 — Final Specification

Status: FINALIZED FOR ARCHITECTURAL ADOPTION
Date: 2026-09-01
Baseline: deepseek-ai/deepseek-harness @ dd6322d604e00eec1ba5e0c8541159906a21094a

## 1. Scope

R1-R10 source reconstruction and architectural mapping are complete. R11 remains an execution-evidence gate and is not marked PASS because live execution was not available in the investigation environment.

## 2. Final classification

DSH is classified as an Adaptable Execution Substrate Candidate for ACES OS.

It is not the ACES authority layer, epistemic layer, constitutional layer, or canonical evidence authority.

## 3. DSH layers

### Substrate
- Cordis Context
- Scope
- Loader/composition lifecycle
- Event dispatch

### Replaceable execution
- Agent Loop
- LLM provider
- Tool provider
- Sandbox provider
- Approval provider

### Composable scaffolding
- Profiles
- Bundles
- Patches
- Projections
- Prompt construction
- Persistence adapters

## 4. ACES ownership

ACES owns:
- Constitution
- Policy
- Authority
- Authorization
- Decision
- Evidence
- Provenance
- Verification
- Revocation
- Audit integrity
- AcceptedState

DSH may execute only within the effective authority and capability scope supplied by ACES.

## 5. Non-equivalence invariants

DSH Event != ACES Evidence.
DSH Session != ACES Canonical Memory.
DSH Projection != ACES Truth.
DSH approval allowed-once != ACES Authority.
DSH sandbox full != ACES Security PASS.
DSH plugin registration != ACES Authorization.
DSH model output != ACES Decision Authority.
GitHub/Grok identity != ACES Trust Authority.

## 6. Canonical integration path

ACES Intent
 -> Authorization
 -> Decision
 -> Context Compiler
 -> DSH Runtime
 -> Capability Execution
 -> DSH Session Event
 -> Evidence/Provenance Adapter
 -> Verification
 -> AcceptedState

Any failure in authorization, execution, evidence, provenance, or verification blocks AcceptedState.

## 7. Security placement

ACES Authorization/Policy is above DSH controls.

DSH Approval and Sandbox are enforcement/control primitives below ACES authority.

Sandbox limitations must remain explicit: file-effect modes do not constitute complete network, process, credential, or general security isolation; partial enforcement is not full enforcement; danger-full-access is an explicit unconfined path.

## 8. Evolution model

Preferred adaptation order:

reuse -> configure -> compose -> replace -> extend -> fork -> rewrite

No finite adaptation count is assumed. The practical boundary is semantic/runtime compatibility, not an arbitrary number of iterations.

## 9. Ablation conclusion

Profile, Bundle, Patch, Projection and Persistence are not fundamental execution primitives. Agent Loop and providers are replaceable. Cordis remains the deepest identified runtime substrate.

Ablation must be used to remove scaffolding and reintroduce only controls demonstrated to be necessary.

## 10. Evidence status

R1-R10: architectural/source/integration-contract evidence sufficient.
R11: LIVE EXECUTION EVIDENCE = NOT PROVEN.

No PASS may be inferred from source inspection alone for the live integration path.

## 11. Adoption decision

ADOPT DSH as an adaptable execution substrate candidate.
DO NOT delegate ACES authority, epistemic truth, canonical evidence, or AcceptedState ownership to DSH.

## 12. Next gate

R11 must be executed in a real DSH runtime environment with instrumentation. Required evidence: authorization trace, effective capability set, runtime composition identity, session/event sequence, tool execution result, evidence/provenance record, verification result, and final AcceptedState or BLOCK.

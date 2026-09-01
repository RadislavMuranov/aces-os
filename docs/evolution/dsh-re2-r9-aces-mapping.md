# DSH-RE2 — R9 ACES Mapping

Status: COMPLETE
Baseline: deepseek-ai/deepseek-harness @ dd6322d604e00eec1ba5e0c8541159906a21094a
Date: 2026-09-01

## 1. Mapping rule

DSH is mapped as an execution substrate, not as the ACES authority layer. Existing R1-R8 findings establish pluginized runtime composition, scoped capabilities, event/session trajectory, replaceable execution components, and explicit sandbox/approval controls.

## 2. Canonical mapping

DSH Cordis/Context -> ACES Runtime Substrate
DSH Scope -> ACES Capability Scope
DSH Agent Registry/Factory -> ACES Agent Runtime Registry
DSH Agent Loop -> ACES Execution Driver
DSH Session Event Log -> ACES Execution Trajectory substrate
DSH Projection -> ACES Derived State / World Model projections
DSH System Prompt -> ACES Context Assembly input, not authority
DSH Tools -> ACES Capability Execution surface
DSH Approval -> ACES human/interaction control primitive, not Authority
DSH Sandbox -> ACES enforcement primitive, not complete Security Boundary
DSH Profile/Bundle/Patch -> ACES Context Compiler / Runtime Composition
DSH Persistence -> ACES durable storage adapter

## 3. ACES components that must remain above DSH

Authority
Authorization
Constitution / Policy
Decision Authority
Proof Authority
Evidence semantics
Provenance
Verification
Revocation
Audit integrity
Human checkpoint semantics

## 4. Critical non-equivalences

- DSH event != ACES Evidence.
- DSH session != ACES canonical memory.
- DSH projection != ACES World Model truth.
- DSH approval allowed-once != ACES Authority.
- DSH sandbox full != ACES Security PASS.
- DSH model context != ACES Context Authority.
- DSH plugin capability != authorized ACES capability.

## 5. Target architecture

```text
                 ACES CONSTITUTION
                        |
              AUTHORITY / POLICY
                        |
          AUTHORIZATION / DECISION
                        |
        PROVENANCE / EVIDENCE / PROOF
                        |
             ACES CONTEXT COMPILER
                        |
              DSH COMPOSITION LAYER
           Profile / Bundle / Patch
                        |
              DSH RUNTIME SUBSTRATE
                    Cordis
                        |
      +-----------------+------------------+
      |                 |                  |
   Agent Loop        Session            Tools
      |                 |                  |
      |              Events            Approval
      |                 |                  |
      |            Projections         Sandbox
      +-----------------+------------------+
                        |
                       OS
```

## 6. Architectural decision

ADOPT DSH as an adaptable execution substrate candidate for ACES OS, while preserving ACES authority, epistemic, provenance, verification, and security semantics above and around it.

Do not import DSH's authority assumptions into ACES.
Do not make GitHub, model output, plugin registration, approval answer, or sandbox status an ACES authority source.

## R9 verdict

PASS — mapping is sufficiently defined to proceed to R10: minimal ACES-on-DSH vertical slice / proof-of-integration experiment.

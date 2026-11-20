# ACES OS — Canon Audit of Proposed Target Architecture

**Audit date:** 2026-11-21  
**Workstream:** ACES OS Rebuilding  
**Artifact class:** Architecture audit / research record  
**Status:** REVIEW COMPLETE AT DOCUMENTARY LEVEL — NOT CANON  
**Canon promotion:** NOT REQUESTED / NOT AUTHORIZED  
**Implementation authorization:** NONE  
**Repository/runtime/production changes:** NONE

## 1. Executive verdict

The proposal is directionally compatible with ACES only after substantial correction. It is **not accepted as the ACES OS target architecture in its current form**.

The compatible core is model-/harness-independent ACES control with Miro as a visual projection. The main defects are: flattening the Orca/DSH execution hierarchy into seven peer agents; treating generic L1–L4 permission tiers as an ACES authorization model; describing shared memory too broadly; promoting Miro and a ten-board workspace to P0 while the recorded P0 development orientation freezes unrelated work; and selecting PostgreSQL, Redis/NATS and other infrastructure without evidence from the minimum working vertical slice.

This is a documentary compatibility assessment. It does not establish runtime implementation, successful integration, or production readiness.

## 2. Normative baseline used

- Notion: **ACES OS — P0 / 100% Development Orientation: Epistemic Core, Control Plane & Technical Stack — 2026-10-14**. The dominant implementation objective is epistemic core, governing/control plane and required technical stack. Other workstreams remain FROZEN until these operate together in a verified vertical slice. The record says Canon promotion and roadmap synchronization have not occurred; it is user-authority-locked.
- Notion: **Minimal ACES Acceptance Protocol — Fixation Record**. StateTransition + ProvenanceBoundEvidence + Verification(PASS) + Authority-bearing Acceptance → AcceptedState. Execution, verification and acceptance remain distinct.
- Notion: **RALPH LOOP — ACES Governance Mandate v1.0**. Each iteration loads persistent state, selects one atomic node, executes, captures evidence, verifies, updates persistent state and reconciles. CompletionClaim ⇏ PASS; PASS ⇏ CLOSED.
- Notion: **ACES OS — Session Handoff v1.0 (2026-10-18)** records FSM v1.0.1, Constitution v0.4, DOS v1.0, AGS v1.0, RS v1.0, CTS v1.0, RTC v0.1 (semantic PASS; provenance BLOCKED). Those versions were not revalidated against every current source in this audit.
- GitHub `RadislavMuranov/aces-os`, default branch `main`: `spec/MINIMAL-ACES-ACCEPTANCE-PROTOCOL.md`, `src/acceptance/accept-verified-transition.ts`, `spec/asa/v0/data-model.md`, `README.md`.
- Linear: RAD-81 (Unified Multi-Harness Environment), RAD-75 (Second Brain & Long-Term Memory), RAD-49 (Verification, evidence & governance audit).

**Evidence boundary:** GitHub `main/README.md` says ASA and DSH integration are not yet implemented. The acceptance kernel source exists, but this audit did not rerun its tests. Specifications and source artifacts are not proof of full runtime enforcement.

## 3. Audit matrix

| Proposal element | Verdict | Canon compatibility / required treatment |
|---|---|---|
| ACES owns governance, authorization, verification, acceptance and AcceptedState | CONFIRMED | Non-negotiable authority boundary. |
| Model/harness independence | CONFIRMED | Execution substrates are replaceable; none acquires ACES authority. |
| Miro as visual Command Center / projection | CONFIRMED | May visualize state and decisions; must not own authoritative state. |
| Miro as source of truth or authority plane | REJECTED | Miro content is a projection/external data, not AcceptedState or Canon. |
| Agent Registry | REVIEW | Inventory only. Registry presence/metadata must not imply truth, permission or authority (Registry ⊭ Truth). |
| Shared tool catalog | REVIEW | Catalog describes tools/capabilities; capability is not authority. ACES authorization remains separate. |
| One ACES Orchestrator | REVIEW | Compatible as a control responsibility, but exact boundary and minimal implementation must derive from the existing ACES control contract and vertical slice. Not proven implemented. |
| Seven peer agents in one runtime layer | REJECTED | Flattens model/client, agent, harness/runtime, Orca fleet, DSH execution substrate and connector into one category. |
| Fixed role matrix for ChatGPT / Claude Code / DSH / ZCode / AutoClaw / Pi / Hermes | REVIEW | Candidates, not an approved seven-agent roster or permanent exclusive roles. DSH remains mandatory in the ACES execution path; preserve Orca/DSH hierarchy. Anthropic harness is not an ACES authority path. |
| Direct agent-to-agent command passing | REJECTED | No uncontrolled delegation. Requests pass through ACES-controlled authorization/orchestration with provenance and bounded execution. |
| MCP as authority/control mechanism | REJECTED | MCP is an integration/transport interface. It grants no ACES authority, verifies no outcome and accepts no state. |
| One mandatory centralized MCP Gateway | REVIEW | Possible implementation option, not a Canon requirement. Compare with direct connector adapters against the smallest vertical slice. |
| Miro Remote MCP endpoint | CONFIRMED (vendor docs) | `https://mcp.miro.com/`; OAuth 2.1; access follows authenticated user/team/board permissions. Curated tool surface, not full REST API mirror. |
| Miro MCP compatibility with every named client | UNKNOWN | General MCP compatibility does not prove support by DSH, ZCode, AutoClaw, Pi or Hermes. Test each separately. |
| PostgreSQL as mandatory primary database | REVIEW | No evidence-based selection in proposal. Decide from minimum state/history contract and donor reuse analysis. |
| Redis Streams / NATS event bus | UNKNOWN | No workload, failure model, comparison or benchmark supplied. |
| Vector database as planned layer | REJECTED FOR CURRENT P0 | Current Second Brain benchmark excludes embeddings/vector search. Reopen only with a separate evidence-backed need and authorization. |
| Shared Memory for all agents | REJECTED AS STATED | Stored/retrieved memory is not truth. Preserve provenance, epistemic state, temporal context, contradiction handling and access isolation. Memory has no governance/acceptance authority. |
| Generic L1–L4 permission tiers | REJECTED AS ACES AUTHORIZATION MODEL | ASA v0 uses Identity, Principal, Capability, Policy and Decision; no first-class Role or full ABAC engine. Closed Operation enum: READ/CREATE/UPDATE/DELETE/EXECUTE/EXPORT/IMPORT/AUTHORIZE/REVOKE. |
| Human approval as generic critical-operation control | REVIEW | Human confirmation alone is not the authorization model. Authority, capability, policy, verification context and authority-bearing acceptance remain distinct. |
| Ten Miro boards as P0/P1 implementation | REJECTED FOR CURRENT PRIORITY | Conflicts with recorded P0 freeze until epistemic core + control plane + technical stack form a verified vertical slice. One bounded architecture map may support that work if it unblocks it. |
| 11-week schedule / “v1.0 Ready” | REJECTED AS ACCEPTANCE CLAIM | Estimates are not evidence. Readiness requires demonstrated end-to-end behavior and verified properties, not elapsed time or checklist completion. |

## 4. Required architecture corrections

1. **Restore ACES authority.** ACES alone owns governance, authorization, verification and acceptance. No model, harness, agent, MCP server, board, registry or database promotes its output to AcceptedState.
2. **Restore execution hierarchy.** Represent ACES Control/Governance above Orca Fleet and the mandatory DSH Harness execution path. Show clients/models and connectors as replaceable adapters, not peer authorities.
3. **Separate state, evidence and projections.** Canon, runtime state, evidence/history, memory and Miro views are distinct. Miro synchronization is projection/reconciliation, not authoritative state mutation.
4. **Use ASA v0 authorization semantics.** Do not add roles, delegation or ABAC by implication. Multi-agent delegation is not in the frozen ASA v0 Operation enum.
5. **Treat memory as evidence-bearing knowledge, not shared truth.** Preserve provenance and epistemic labels; UNKNOWN ≠ FALSE; Registry ⊭ Truth.
6. **Do not preselect infrastructure.** PostgreSQL, Redis/NATS, object storage and vector systems remain candidates until requirements and reproducible evidence justify them.
7. **Defer broad Miro rollout.** No ten-board rollout or parallel Miro control-plane P0. Miro remains a later projection/interface over authoritative ACES state.
8. **Test each Miro client separately.** Vendor docs confirm endpoint and OAuth model, not any connection in this ACES environment or compatibility with all named clients.

## 5. Miro MCP evidence

Official Miro documentation identifies `https://mcp.miro.com`, OAuth 2.1, permission-bound access, and curated tools for boards, diagrams, documents, tables, comments, images and layout. It is not a full REST API mirror.

Sources:
- https://developers.miro.com/docs/miro-mcp
- https://developers.miro.com/docs/connecting-to-miro-mcp
- https://developers.miro.com/docs/miro-mcp-server-frequently-asked-questions
- https://help.miro.com/hc/en-us/articles/31624028247058-Miro-MCP-Server-overview

This confirms vendor documentation only, not a live ACES connection.

## 6. Existing work and overlap

- **RAD-81** already covers the unified multi-harness environment and ACES-only acceptance. Link this audit there rather than creating a competing multi-harness mission.
- **RAD-75** governs Second Brain research and explicitly denies memory any Governance, Authorization, Verification, Acceptance or AcceptedState authority. Its benchmark constraints exclude vector search and embeddings.
- **RAD-49** covers verification/evidence/governance and separation of execution, verification and acceptance.
- The local Obsidian Vault declares `canonical: false` and says it is a prepared workspace, not an accepted ACES source of truth. This record is RESEARCH, not Canon.

## 7. Overall status

- Architecture proposal: **REVIEW / NOT ACCEPTED AS WRITTEN**
- Canon changes: **NONE**
- Implementation changes: **NONE**
- Miro connection in ACES: **UNKNOWN**
- Seven-client compatibility: **UNKNOWN**
- Runtime Orchestrator: **NOT PROVEN BY THIS AUDIT**
- Infrastructure selections: **NOT MADE**
- P0: epistemic core + governing/control plane + required technical stack remain dominant.

## 8. Next atomic action

Create a corrected **ACES Control / Orca Fleet / DSH Harness / Connector / Miro Projection** architecture view that preserves authority and acceptance boundaries, maps to the existing P0 vertical-slice sequence, and labels each component SPECIFICATION / IMPLEMENTED / VERIFIED / UNKNOWN from direct evidence. Introduce no infrastructure selection and no Canon changes.

Then compare this minimal architecture with current repository/runtime state. Do not begin ten-board Miro rollout, broad seven-client integration, database migration or Canon promotion under this audit.

## 9. Authorization boundary

This record authorizes documentation and cross-linking only. It does **not** authorize Canon/protected specification changes, implementation/merge/deployment, DSH/Orca activation or reconfiguration, Miro board creation/write operations, agent installation/integration/credential changes, or memory migration/vector-database adoption. Each requires separate explicit authorization.

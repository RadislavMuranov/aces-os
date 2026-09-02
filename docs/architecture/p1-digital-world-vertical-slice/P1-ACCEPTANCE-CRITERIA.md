# P1 Vertical Slice — Future Implementation Acceptance Criteria

**Status:** CONTRACT PREPARATION  
**Applies when:** a future gate authorizes runtime implementation  
**Does not authorize:** implementation by this document alone

---

## 1. Identity

- [ ] Provider-local durable identity preserved across sessions
- [ ] Rename/move does not auto-create a new DWOM identity without lifecycle record
- [ ] Delete → recreate distinguishable (`identity_epoch` / tombstone+successor)
- [ ] Cross-provider correlation only via explicit policy-backed correlation records
- [ ] Name/path/title/URL equality alone never proves identity

## 2. Observation

- [ ] Every Observation carries connector, provider, identity binding, observation_timestamp, provenance
- [ ] Arrival time never silently becomes sole authoritative source order
- [ ] Partial observations remain marked partial; unknown ≠ false
- [ ] Permission-limited and inaccessible resources emit typed limitation/error, not fabricated content

## 3. Evidence lifecycle

- [ ] Observation never becomes AcceptedState directly
- [ ] EvidenceCandidate distinct from Evidence
- [ ] Evidence Admission recorded with policy_id/version; ≠ Verification; ≠ AcceptedState
- [ ] Replay: same request_id + same payload_digest handled deterministically
- [ ] same request_id + different payload_digest → REJECT/CONFLICT
- [ ] Connector success / inference / reconciliation cannot mint Evidence or AcceptedState

## 4. Authorization

- [ ] Connector cannot mint ACES authority
- [ ] Side-effecting operations require valid `authorization_ref`
- [ ] MCP side effects use same ASA path and `authorization_ref`
- [ ] Source/provider authority cannot authorize ACES actions
- [ ] Unavailable ASA → fail-closed (no side effect)

## 5. Reconciliation

- [ ] Conflicts explicit; default UNRESOLVED without policy
- [ ] No hidden latest-wins / first-wins / provider-wins
- [ ] Resolution includes policy_id, version, rule, participants, provenance
- [ ] Competing observations preserved unless policy resolves

## 6. Epistemic boundary

- [ ] No Digital World State → Knowledge direct path
- [ ] No Digital World State → Semantic Reality direct path
- [ ] No World Model direct Semantic Reality mutation
- [ ] Only Evidence → Axis-C Verification → AcceptedState enters Knowledge promotion path

## 7. Six-provider coverage

- [ ] Adapters for Obsidian, GitHub, Slack, Gmail, Google Drive, Kaiten implement the **same** neutral contract
- [ ] Provider-specific gaps recorded as PVR/UNSUPPORTED, not silent invention
- [ ] CLA/native preferred; MCP only under governing rule

## 8. Failure

- [ ] Fail-closed cases from P1 contract §9 produce deny/reject/partial/conflict — never fabricated success AcceptedState

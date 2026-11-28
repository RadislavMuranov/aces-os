# AOC-001 — Verified Transition Contract (Acceptance of Canonical State Changes)

**Status:** RESTORED (2026-11-28) · reconstructed from implementation; original file was absent on disk (gap recorded in `wiki/atoms/ATOM-20261128-005`)
**Scope:** canonical acceptance contract for the P0 product verification program
**Source of truth:** `src/acceptance/accept-verified-transition.ts` + `src/acceptance/acceptance-binding.schema.json` + `tests/accept-verified-transition.test.ts`
**Governing documents:** `spec/MASTER-PROTOCOL.md`, `docs/product/P0/PROTOCOL.md` (RATIFIED, 2026-08-29)

---

## 1. Normative statement

A change to canonical reality is **accepted only as a fully bound, verified transition**. Acceptance is fail-closed: any missing, failed, or mismatched input yields rejection (`null`), never default acceptance.

> New canonical state enters the accepted record only after self-verification with an explicit, cross-checked evidence chain. Silence is not acceptance.

## 2. Inputs

| Input | Shape | Rule |
|---|---|---|
| `transition` | `{ transition_ref, canonical_ref, has_history }` | the proposed state change, with history |
| `verification` | `{ status: "PASS" \| "FAIL", verification_context_ref }` | self-verification result bound to an exact context |
| `binding` | `AcceptanceBinding` (below) | the acceptance binding |
| `authority` | `{ accepted: true, authority_ref, capability_ref, policy_ref }` \| `{ accepted: false }` | delegated authority for the action |

## 3. Acceptance gates (evaluated in order, all must hold)

1. **History** — `transition.has_history === true`. A state change without history is not admissible.
2. **Verification** — `verification.status === "PASS"`. Failure rejects.
3. **Binding present** — `binding` is provided.
4. **Binding complete** — none of the five binding references is empty.
5. **Authority accepted** — `authority.accepted === true`.
6. **Cross-boundary reference matching** — every binding reference must equal its counterpart exactly:
   - `binding.canonical_ref === transition.canonical_ref`
   - `binding.authority_ref === authority.authority_ref`
   - `binding.capability_ref === authority.capability_ref`
   - `binding.policy_ref === authority.policy_ref`
   - `binding.verification_context_ref === verification.verification_context_ref`

Any single mismatch rejects the transition.

## 4. AcceptanceBinding (machine shape)

Five required references, `additionalProperties: false`, each a non-empty string:

- `canonical_ref` — the canonical reality being transitioned
- `authority_ref` — the authority domain responsible for acceptance
- `capability_ref` — the delegated right permitting the acceptance action
- `policy_ref` — the policy/version governing admissibility
- `verification_context_ref` — the exact verification context the acceptance is bound to

**The schema does not authorize acceptance by itself.** It only fixes the binding shape; authorization comes from gates 3–6 above.

## 5. Output

On full pass, the accepted state is:

```
{
  state: "ACCEPTED",
  canonical_ref,        // from the transition
  transition_ref,       // the accepted transition
  acceptance_binding    // the verified binding, recorded verbatim
}
```

On any gate failure the function returns `null` — no partial acceptance, no degradation path.

## 6. Provenance

- Implementation: `src/acceptance/accept-verified-transition.ts` (`acceptVerifiedTransition`)
- Schema: `src/acceptance/acceptance-binding.schema.json`
- Tests: `tests/accept-verified-transition.test.ts` — 6 cases: fully-bound pass, missing history, verification failure, missing binding / unaccepted authority, empty references, every cross-boundary reference mismatch
- Linked wiki atom: `wiki/atoms/ATOM-20261128-005-aoc-001-gap.md`

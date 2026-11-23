# ACES OS — Project Memory

Durable notes for agents working in this repository. Facts only, with dates.

## What this repository is

Implementation substrate for ACES OS. Current verified slice (2026-11-22/23):
acceptance kernel `src/acceptance/accept-verified-transition.ts`, decision
contract `src/acceptance/transition-decision.ts` (AOC-001), AutoClaw bridge
`src/integration/autoclaw/` (stdio JSON-RPC, policy-gated, fail-closed), hook
engine under `.claude/hooks/` (journal with row sha256, stop gate).

## How to verify (one command per layer)

- Contract + guards: `node --test tests/transition-decision.test.ts tests/accept-verified-transition.test.ts tests/authentication-evidence-guard.test.ts`
- Bridge units: `node --test tests/fs-ops.test.mjs tests/policy-gate-branches.test.mjs`
- Hook engine / policy controls: `node --test tests/hooks/aces-hook-engine.test.mjs tests/hooks/defect-enforcement-map.test.mjs tests/hooks/policy-controls.test.mjs`
- Local e2e: `node tests/integration/rad10-e2e.mjs` (8 steps, writes only git-ignored artifacts under tests/integration/)

## Invariants that always apply

- Policy decisions come only from `.claude/hooks/aces-hook-engine.mjs`; the bridge contains no policy rules.
- Fail-closed everywhere: unknown policy evaluation = deny; PATH-ESCAPE on any containment violation; exec disabled unless `--enable-exec`.
- `acceptVerifiedTransition` is the single acceptance authority; `decideVerifiedTransition` mirrors its guard order and delegates the accept path to it.
- Do not edit `AGENTS.md`, `SCHEMA.md`, `spec/MASTER-PROTOCOL.md` or governance artifacts without the Master Control Protocol procedure.
- No secrets in the repo or journal; `.env` files must never be read or committed.

## Working state (2026-11-23)

- Branch `implementation/aces-node-baseline` (local only, not pushed; push requires explicit user confirmation).
- Production status: NO-GO (see `docs/product/P0/RAD-12-production-readiness-audit.md`, `RAD-14-nogo-blocker-report.md`).
- Open blockers: host isolation for exec paths (RAD-8), CI green run after push (RAD-86).

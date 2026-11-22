# RAD-10/RAD-11 — Local End-to-End Verification Report

Date: 2026-11-22 · Repo: RadislavMuranov/aces-os · Branch: `implementation/aces-node-baseline` · Commit: `9b2f046`
Driver: `tests/integration/rad10-e2e.mjs` · Evidence: `tests/integration/e2e-evidence.json` (git-ignored artifacts: `e2e-scratch.md`)

## Verdict

**PASS** — локальный e2e-контур ACES OS ↔ policy-gate ↔ hook-engine работает end-to-end, 8/8 шагов, exit code 0.

## Scope guard

Внутри среза: stdio-транспорт, JSONRPC-фрейминг, объявление задачи с 4 ops, policy-gate на каждый вызов, PATH-ESCAPE deny-детектор, fail-closed NOT_FOUND на edit несуществующего файла, Stop-гейт (ACES_ITERATION_RECORD), провенанс journal с row_sha256.
Вне среза: реальный Layer-2 harness (AutoClaw-подключение как MCP), production rollout, network. Локальная цепочка — единственное, что заявляется.

## Steps (evidence file, started_at 2026-11-22T20:53Z)

1. `health_deep` OK — `"ok": true`, state-dir writable, hook engine reachable
2. `submit_task` OK — task t_20261122T205137Z_736ced7df6, 4 ops
3. `invoke_read` OK — policy allow, содержимое AOC-001 получено
4. `invoke_deny_probe` OK — `../outside-root.txt` отклонён: PATH-ESCAPE (fail-closed)
5. `invoke_write` OK — policy allow, файл создан, journal line 111
6. `invoke_edit` OK — policy allow, правка существующего файла
7. `record_result_stop_gate` OK — ACES_ITERATION_RECORD принят (Stop-гейт пройден с полным протоколом)
8. `get_provenance` OK — journal-ссылки verified, row_sha256 совпадают

## Regression

`node --test tests/transition-decision.test.ts tests/accept-verified-transition.test.ts tests/hooks/*.test.mjs` — **409/409 pass**, exit 0.

## Reproduction

```
cd C:\ACES\aces-os
node tests/integration/rad10-e2e.mjs
# expect: 8 steps OK, EXIT=0
```

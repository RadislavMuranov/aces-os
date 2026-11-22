# RAD-12 — Production-Readiness Audit

Date: 2026-11-22 · Repo: RadislavMuranov/aces-os · Branch: `implementation/aces-node-baseline`
Method: ACES-METHOD (pass / fail / unknown, никаких «примерно готово»)

## Verdict: NO-GO для production

Готов локальный проверяемый срез. Production-контур не готов и не должен объявляться готовым.

## PASS (с evidence)

| Компонент | Статус | Evidence |
|---|---|---|
| Контракт verified-transition | PASS | `src/acceptance/accept-verified-transition.ts`, 6/6 тестов |
| AOC-001 decision-контракт с таксономией отказов | PASS | `src/acceptance/transition-decision.ts`, 13/13 тестов, контракт-док `docs/product/P0/AOC-001-verified-transition-contract.md` |
| Diagnostics guards (auth evidence) | PASS | `tests/authentication-evidence-guard.test.ts` |
| ACES bridge (stdio JSONRPC, 5 tools) | PASS | `src/integration/autoclaw/server.mjs`, e2e 8/8 (`docs/product/P0/RAD-10-11-e2e-report.md`) |
| Policy-gate (hook engine, journal sha256) | PASS | e2e шаги 3–6, 8; `tests/hooks/` 390/390 |
| Stop-гейт (ACES_ITERATION_RECORD) | PASS | e2e шаг 7 |
| Fail-closed поведение (PATH-ESCAPE, NOT_FOUND) | PASS | e2e шаги 4 (deny) + провал edit до write (NOT_FOUND) |

## FAIL / BLOCKER

| Блокер | Детали |
|---|---|
| RAD-8: изоляция исполнения | Preflight 2026-10-23: нет Hyper-V/Windows Sandbox/WSL; инцидент Ollama-дампа 3.8 ГБ. Executive-версия gate не была построена. Любой exec-путь (даже с флагом `--enable-exec`) остаётся закрытым до появления изолированной среды |
| CI | ЗадачиRAD-10/14 требовали CI-прогон как блокер; в срезе CI нет — все прогоны локальные, воспроизводимость через команду reproduction |

## UNKNOWN

| Неизвестное | Что нужно для закрытия |
|---|---|
| Поведение под реальным Layer-2 harness | Подключить bridge как MCP-сервер в AutoClaw (config уже есть в CLAUDE.md) и повторить e2e через харнесс |
| Production rollout на другой машине | RAD-14: явный G0-статус + план |
| Долговечность journal (рост, ротация) | Не тестировалось; известная неизвестная |

## Границы честности

- Коммиты локальные; push в GitHub в этом сеансе не выполнялся (git push потребует отдельного подтверждения).
- `e2e-scratch.md` и `e2e-evidence.json` — git-ignored артефакты прогона, не production-код.
- Никакой компонент не «примерно готов»: каждый пункт таблицы PASS подкреплён запускаемой командой.

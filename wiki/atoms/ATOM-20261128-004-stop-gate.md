---
id: ATOM-20261128-004
title: Stop-гейт aces-hook-engine — работающий fail-closed механизм
status: OBSERVED
created: 2026-11-28
updated: 2026-11-28
sources:
  - aces-os/.claude/hooks/aces-hook-engine.mjs (evaluateStop, L796)
  - aces-os/.claude/hooks/journal.tsv (219 записей, 25–26.11)
  - aces-os/.claude/settings.json (PreToolUse + Stop)
---

Stop-гейт реально блокирует закрытие хода: без канонической итерационной записи (FINAL_VERDICT, REPOSITORY_BEFORE/AFTER ≠ UNKNOWN/NOT VERIFIED/N/A) — `decision: block`, rule STOP-GATE. Журнал append-only со spool-fallback («never fail-open»). Подтверждено живыми данными: 219 срабатываний в journal.tsv, из них 19 × STOP-GATE → block, 33 × Z-2 deny, 21 × Z-8 deny. Механика Voyager-паттерна (знание в запись — только после self-verification) реализована и развивается (WA-1 write-authority, W4a spool — коммиты 27–28.11).

Related: [[ATOM-20261128-005]] · [[ATOM-20261128-008]]

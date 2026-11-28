---
id: ATOM-20261128-003
title: Фиксы fs-ops в edit (заменитель $&/$', TOCTOU, symlink, 8 МБ)
status: OBSERVED
created: 2026-11-28
updated: 2026-11-28
sources:
  - Documents/R2-SECOND-BRAIN-CHUNK-001/sources/second-brain-mcp/src/vault.ts
  - session-20261124-summary.md (коммиты c5b2082 + 8264c41 в полном репо)
---

В edit-операции second-brain-mcp: спец-паттерны `$&`/`$'` больше не интерпретируются (запись через функцию-заменитель, тест-регрессия есть); TOCTOU закрыт — запись только через open→realpath-проверка→truncate+write, побег через symlink отвергается до записи байта; лимит 8 МБ снят; JSON-RPC id восстановлен в internal error. Самостоятельно подтверждено: тесты «proposes and applies note updates only with confirmation and matching hash», «write operations enforce write-path validation» зелёные. Хэши c5b2082/8264c41 в снапшоте отсутствуют (однокоммитный).

Related: [[ATOM-20261128-001]] · [[ATOM-20261128-002]]

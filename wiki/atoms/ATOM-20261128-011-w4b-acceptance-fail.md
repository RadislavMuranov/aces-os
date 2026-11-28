---
id: ATOM-20261128-011
title: W4b не принят - доказательство было от owner-токена
status: OBSERVED
created: 2026-11-28
updated: 2026-11-28
sources:
  - tools/protection/w4b-identity-boundary.ps1
  - tools/protection/w4b-probe.ps1
  - docs/protection/DATA-LOSS-PROTECTION-METHOD.md 10.5
---

Первая версия W4b провалила приёмку не из-за политики, а из-за инструмента: литералы `-Applyassi`, `(OI)(CI415)` и `Select-String619` были повреждены, `%COMPUTERNAME%` и `\"` не работают в PowerShell, а единственный probe-вывод (`priv:*=PRESENT`, `administrators=MEMBER`, `spool_delta=0`) снят под owner-токеном, тогда как `aces-agent` вообще не существовал. Отсюда правило: ACL-проба под администратором невалидна (SeRestore/SeBackup обходят DACL), `N/A` не доказывает отказ, а идентичность подтверждается token SID и process owner SID, не именем.

Вторая версия: `-Apply` создаёт стандартную учётку и сохраняет SDDL `repo`/`vault`/`stage` с каноническим хэшем; `-SelfCheck` даёт 16/16 PASS (roundtrip SDDL и хэша, наследование Deny ребёнком и его снятие при restore, owner create/read/delete, детектор под owner выдаёт `NON_ISOLATED`/exit 1, движок пишет canonical +1 и spool 0); `-Verify` сам создаёт все цели, требует каждую предпосылку и перепроверяет состояние после запуска. Живая проверка под `aces-agent` не выполнена: нет пароля, поэтому `BOUNDARY=ADVISORY`.

Related: [[ATOM-20261128-009]] · [[ATOM-20261128-010]]

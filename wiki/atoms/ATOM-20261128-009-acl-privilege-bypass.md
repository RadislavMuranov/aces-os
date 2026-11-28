---
id: ATOM-20261128-009
title: Deny-ACL не ограничивает токен с SeRestorePrivilege
status: OBSERVED
created: 2026-11-28
updated: 2026-11-28
sources:
  - commit df6bcad
  - docs/protection/DATA-LOSS-PROTECTION-METHOD.md §10.1
  - spec/asa/v0/data-model.md §11.7
---

В повышенной сессии владельца `SeBackupPrivilege` и `SeRestorePrivilege` включены: файл с Deny `DELETE` для `Everyone` всё равно удаляется через `[IO.File]::Delete`, переименование проходит при Deny записи и удаления, а блокируется только создание нового файла. Значит ACL-проба под токеном владельца или администратора не является доказательством границы; E3 достоверен только для стандартного локального принципала, у которого `administrators=ABSENT` и все четыре bypass-привилегии `ABSENT`, и если harness должен работать elevated — граница переносится на E4, а не усиливается ACE.

Related: [[ATOM-20261128-004]] · [[ATOM-20261128-008]]

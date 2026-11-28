---
id: ATOM-20261128-010
title: CodexSandboxUsers лишён Allow Modify на Vault, наложен Deny
status: REVIEW
created: 2026-11-28
updated: 2026-11-28
sources:
  - tools/protection/w4b-identity-boundary.ps1
  - docs/protection/DATA-LOSS-PROTECTION-METHOD.md §10.3
  - C:\ACES-Staging\acl-backup\vault-pre-codex.sddl
---

На `Obsidian Vault` у группы `CodexSandboxUsers` (SID `S-1-5-21-...-1002`, члены — `CodexSandboxOffline` RID 1003 и `CodexSandboxOnline` RID 1004) был унаследованный `Allow Modify`; рядом висел такой же Allow у чужого SID `S-1-5-21-3297...-374093975`, а владелец (RID 1001) в группу не входил. Allow снят, DACL переведён в protected: SYSTEM, Администраторы и владелец — FullControl, группа — explicit Deny на `WD,AD,WEA,WA,DE,DC,WDAC,WO`; четыре подкаталога наследуют Deny, чтение группой сохранено.

Эффект под токеном Codex не проверен: пароля нет, доказательство — DACL, а не исполненный отказ. Если sandbox-токен несёт `SeRestorePrivilege`, Deny обходится так же, как в [[ATOM-20261128-009]]; откат — `-RollbackCodex`.

Related: [[ATOM-20261128-004]] · [[ATOM-20261128-009]]

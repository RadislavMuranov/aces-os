---
id: ATOM-20261128-008
title: Bootstrap wiki-слоя выполнен (петля «канон-файлы-петля» запущена)
status: OBSERVED
created: 2026-11-28
updated: 2026-11-28
sources:
  - aces-os/wiki/ (README, atoms/, index/MOC.md, journal/)
  - aces-os/AGENTS.md (секция Knowledge Capture)
  - research/aces-wiki-core-20261123/SYNTHESIS.md (раздел 5, план внедрения)
---

По решению пользователя «запускай» (28.11.2026) выполнен bootstrap из плана 23.11: создана `wiki/` (шаблон атома, MOC-индекс, 8 атомов из знаний 24.11 и 28.11), строка протокола «новое знание → wiki-атом, не правка канона» добавлена в AGENTS.md. Канон не мутировал: MASTER-PROTOCOL / SCHEMA / K1–K6 / I1–I8 не тронуты, изменение — аддитивное (новая папка + одна секция). Теперь петля замкнута: capture → Stop-гейт (уже работает, [[ATOM-20261128-004]]) → append-only commit → MOC-обновление.

Related: [[ATOM-20261128-004]] · [[ATOM-20261128-006]]

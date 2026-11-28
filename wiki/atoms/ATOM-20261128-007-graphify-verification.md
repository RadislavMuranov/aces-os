---
id: ATOM-20261128-007
title: Граф сеанса 24.11 верифицирован 1:1; артефакты в AutoClaw Roaming
status: OBSERVED
created: 2026-11-28
updated: 2026-11-28
sources:
  - AppData/Roaming/AutoClaw-oversea-official/accounts/7771e82a.../projects/Default/graphify-session-20261124/graphify-out/ (graph.json, GRAPH_REPORT.md, graph.html, manifest.json)
  - aces-os wiki/ (пересчёт метрик)
---

Отчёт graphify по корпусу 24.11 проверен по сырым данным: 45 узлов / 60 рёбер / 6 сообществ, 33 EXTRACTED + 27 INFERRED (55/45), 0 висячих, cohesion и betweenness (0.065/0.059) пересчитаны независимо — совпадение точное. Урок поиска: артефакты AutoClaw лежат на глубине 8 под AppData\Roaming — поиски с maxdepth ≤ 7 и exclusion AppData их пропускают (ложный вердикт «артефакты отсутствуют» был снят).

Related: [[ATOM-20261128-008]]

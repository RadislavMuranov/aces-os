# Wiki — динамический слой знаний ACES OS

**Status:** BOOTSTRAPPED (2026-11-28) · **Дизайн:** `research/aces-wiki-core-20261123/SYNTHESIS.md` (рекомендация «канон-файлы-петля»)

## Структура

- `atoms/` — атомарные заметки знаний: .md + YAML frontmatter (`id`, `status: OBSERVED|REVIEW|UNKNOWN`, `sources`, `created`)
- `atoms/_ATOM-TEMPLATE.md` — шаблон нового атома
- `index/MOC.md` — индекс (Map of Content); обновляется вместе с каждым новым атомом
- `journal/` — append-only журнал событий знаний (добавление/пересмотр/отмена атомов)

## Правила петли

1. Новое знание = **новый атом**. Никогда — тихая правка канона (MASTER-PROTOCOL, K1–K6, I1–I8).
2. Поиск = `rg`/grep по текстовым файлам. Ссылки = `[[wikilinks]]`. Ноль зависимостей, ноль БД.
3. `status: OBSERVED` — напрямую проверено (команда/тест/файл показаны). `REVIEW` — утверждение из чужого источника или текста, требует проверки. `UNKNOWN` — не определено.
4. Петля: capture → self-verification (Stop-гейт, canonical iteration record) → append-only git commit → обновление `index/MOC.md`.
5. Атом можно пометить `superseded: [[id]]`, но не удалять — история append-only.

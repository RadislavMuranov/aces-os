# R2-SECOND-BRAIN-CHUNK-001

## Token-Efficient Chunking & Retrieval Benchmark

**Тип:** исследовательский benchmark
**Статус:** DRAFT / Source Audit Completed Partially
**Назначение:** определить наиболее эффективную стратегию chunking, lexical retrieval и формирования карточек знаний для локального Second Brain.

## 0. Зафиксированное архитектурное уточнение

Карточки знаний создаются отдельным лёгковесным локальным MoE Qwen-агентом. Это отдельный контур, не часть каждого поискового запроса.

- Card Generation: локальный MoE Qwen.
- Lexical indexing and retrieval: детерминированный chunking + SQLite FTS5/BM25.
- Карточка не заменяет исходный документ; оригинал остаётся источником истины.
- Измерять отдельно стоимость генерации карточек и стоимость retrieval/context packet.
- Точная модель, версия, квантование и tokenizer MoE Qwen пока UNKNOWN.

## 1. Архитектурные ограничения

- No embeddings.
- No vector database / vector search.
- No semantic reranking.
- No Ollama.
- No mandatory LLM calls during lexical indexing or retrieval.
- SQLite FTS5 / BM25 — основной контрольный поисковый механизм.
- Оригинальные документы остаются источником истины.
- Каждый результат поиска должен иметь provenance.
- Карточки знаний создаются отдельным лёгковесным локальным MoE Qwen-агентом.

## 2. Исследуемые реализации

| Реализация | Роль | Зафиксированный commit |
| --- | --- | --- |
| [jblenman/kb-mcp](https://github.com/jblenman/kb-mcp) | Основной MCP-кандидат | 5658ea67f36d7bc04a1cbc54947f9c289dd17e06 |
| [hskl18/boring-agent-memory](https://github.com/hskl18/boring-agent-memory) | Основной кандидат для исследования chunking и ID | 208816994effe344b4268e20def76ed9c046ced6 |
| [abhijithviswanathan/docsearch](https://github.com/abhijithviswanathan/docsearch) | Минимальный контрольный baseline | c1341ff5bc87320ae968bdb7057effd4f6e43fe2 |

Исследуемые исходники фиксируются по commit SHA. Любые изменения upstream после фиксации рассматриваются как отдельная версия эксперимента.

### Предварительные source-audit наблюдения

**kb-mcp**

- Heading-aware разбиение, объединение небольших секций и деление больших секций по абзацам.
- Сохраняет heading path и точные line ranges.
- Code fences не принимаются за заголовки; отдельная защита таблиц и списков от разрезания не подтверждена.
- FTS5 использует porter unicode61; Porter stemmer не обеспечивает русскую морфологию.
- Embedder в example config включён по умолчанию; в целевом режиме требуется явно отключить.
- Статус: REVIEW.

**Boring Agent Memory**

- Структурно выделяет headings, fenced code, таблицы, списки, blockquotes и обычные абзацы.
- Защищённые блоки могут превышать max_chars; размер не является токенной гарантией.
- Chunk ID учитывает document identity, версию chunker, heading identity, content и дубликаты.
- Query tokenizer не поддерживает кириллицу в текущем виде; это блокирует прямое применение к русскому корпусу до исправления и тестирования.
- Статус: REVIEW.

**DocSearch**

- Минимальный Python + SQLite FTS5 baseline.
- Разбиение по Markdown headings или 60-line boundary.
- SHA-256 файлов, транзакционное обновление, line ranges, BM25.
- Нет структурной защиты code fences, таблиц и списков; нет stemming и MCP.
- Статус: CONFIRMED как контрольный минимальный baseline, не как победитель.

Это source-level наблюдения, не результаты benchmark execution.

## 3. Экспериментальные стратегии

1. Heading-aware chunking.
2. Paragraph-aware chunking.
3. Structural block chunking.
4. Hierarchical chunking.
5. Atomic knowledge cards — отдельный контур генерации MoE Qwen.
6. Whole-document BM25 — контроль без разбиения на chunks.
7. Chunk-level BM25 — основной retrieval-кандидат.

## 4. Тестовый корпус

Подготовить воспроизводимый синтетический корпус:

- Русский язык.
- Английский язык.
- Смешанный русский/английский.
- Markdown headings всех уровней.
- Длинные абзацы.
- Короткие секции.
- Списки и вложенные списки.
- Таблицы.
- Code fences.
- Blockquotes.
- Frontmatter.
- Повторяющиеся заголовки.
- Повторяющиеся фрагменты.
- Очень длинные строки.
- Документы с изменениями в начале, середине и конце.

Для каждого документа сформировать эталонные координаты и набор запросов с заранее установленными правильными источниками.

## 5. Проверка chunking

Для каждой реализации измерить:

- Количество chunks.
- Медиану и распределение размеров.
- Фактические токены каждого chunk.
- Пересечение chunks.
- Потерю или дублирование текста.
- Сохранность структурных блоков.
- Точность line ranges.
- Стабильность chunk IDs.
- Поведение при insertion, deletion, split и merge.
- Корректность incremental reindex.

Отдельно проверять, не нарушает ли chunker смысловую целостность списков, таблиц, кода и абзацев.

## 6. Проверка retrieval

Одинаковые запросы выполняются на одинаковом корпусе для всех вариантов.

Сравниваются:

- Recall@1, Recall@3, Recall@5.
- MRR.
- Precision@K.
- Доля запросов без результата.
- Ложные совпадения.
- Результаты на русском, английском и смешанном языке.
- Поиск по точным идентификаторам.
- Поиск по фразам.
- Поиск при изменённой словоформе.
- Поиск, когда релевантные фрагменты находятся в разных частях одного документа.

Проверить два режима:

- Strict lexical retrieval.
- Relaxed lexical retrieval.

Проверить влияние OR/AND/phrase query strategies и metadata filters.

## 7. Токенная экономика

Использовать реальные tokenizer implementations, а не оценку по количеству символов или слов.

### A. Card Generation — локальный MoE Qwen

- Входные токены.
- Выходные токены.
- Токены повторной генерации.
- Среднее время генерации.
- Доля невалидных карточек.
- Стоимость проверки provenance.
- Доля карточек, которые не добавляют новой информации.

### B. Retrieval и Context Builder

- Токены запроса.
- Токены каждого возвращённого chunk.
- Суммарные токены контекстного пакета.
- Доля дублирующегося контекста.
- Количество вызовов kb_get или аналогичного механизма расширения.
- Токены соседних chunks, загруженных дополнительно.
- Токены полного документа как контрольный сценарий.

Использовать tokenizer фактического MoE Qwen и отдельно tokenizer целевого агента-потребителя контекста. Их результаты не смешивать.

Точная модель MoE Qwen, версия, квантование и tokenizer должны быть зафиксированы до измерений. До этого токенные показатели имеют статус UNKNOWN.

## 8. Проверка карточек знаний

Карточка должна содержать:

- card_id;
- document_id;
- source_id;
- source_path;
- source_line_start;
- source_line_end;
- source_content_hash;
- card_content;
- card_content_hash;
- generator_model;
- generator_version;
- created_at.

Критерии:

- Карточка не подменяет исходный документ.
- Каждый факт в карточке имеет проверяемую привязку к источнику.
- Неподтверждённые выводы не представляются как факты.
- Повторная генерация не создаёт ложные дубликаты.
- Удаление или изменение источника позволяет обнаружить устаревшую карточку.

## 9. Контрольные эксперименты

| ID | Эксперимент |
| --- | --- |
| E01 | Whole-document BM25 |
| E02 | DocSearch 60-line baseline |
| E03 | kb-mcp heading-aware |
| E04 | Boring Agent Memory structural blocks |
| E05 | Paragraph-aware |
| E06 | Hierarchical chunking |
| E07 | Русский lexical retrieval |
| E08 | Mixed-language retrieval |
| E09 | Incremental update and ID stability |
| E10 | Context packet token budget |
| E11 | MoE Qwen card generation |
| E12 | Card provenance and consistency |

## 10. Правила оценки

Не выбирать победителя по одному показателю.

Итоговое решение должно учитывать одновременно:

1. Retrieval quality.
2. Token efficiency.
3. Provenance correctness.
4. Structural integrity.
5. Russian/mixed-language support.
6. Incremental update correctness.
7. Runtime and memory cost.
8. Operational simplicity.

Кандидат не получает PASS, если отсутствуют воспроизводимые тесты и исходные результаты измерений.

## 11. Требуемые результаты

- Source Audit Matrix.
- Benchmark corpus and fixtures.
- Query set with expected source ranges.
- Reproducible test runner.
- Raw per-case results.
- Token cost report.
- Chunk integrity report.
- Retrieval quality report.
- Card generation quality report.
- Final CONFIRMED / REVIEW / UNKNOWN matrix.

## 12. Ограничения исполнения

Это исследовательский артефакт. Он не разрешает:

- изменения ACES Canon;
- изменения ACES OS runtime или исходного кода;
- установку или регистрацию MCP;
- изменения локальной конфигурации;
- изменения BASTION;
- интеграцию в production;
- выбор победителя до получения измерений.

Разрешена фиксация этого исследовательского документа в Notion, Obsidian, GitHub и управление исследовательским планом в Linear по прямому запросу пользователя. Benchmark execution, установка и интеграция остаются отдельными действиями, требующими отдельного допуска.

## 13. Контрольные статусы на 2026-11-18

| Область | Статус |
| --- | --- |
| Source-level audit трёх реализаций | CONFIRMED — частично |
| Структурные особенности chunking | CONFIRMED |
| Русская морфология и query handling | REVIEW |
| Токенная эффективность на реальном tokenizer | UNKNOWN |
| Initial cross-candidate lexical probe and Boring benchmark-v2 | CONFIRMED — limited scope; full R2 incomplete |
| MoE Qwen card generation benchmark | UNKNOWN / NOT STARTED |
| Выбор итоговой реализации | NOT DECIDED |

## 14. План и контроль

1. Зафиксировать source audit и pinned revisions.
2. Подготовить synthetic fixtures и ground-truth line ranges.
3. Создать одинаковый query set для трёх реализаций.
4. Проверить корректность русского и смешанного lexical retrieval.
5. Выполнить структурные и incremental-index тесты в изолированной среде.
6. Зафиксировать точную MoE Qwen модель/tokenizer и tokenizer целевого потребителя.
7. Измерить Card Generation отдельно от Retrieval.
8. Сформировать raw results и evidence matrix.
9. Провести независимую проверку методики и результатов.
10. Принять winner/no-winner решение только после прохождения критериев.

**Текущий вывод:** Boring Agent Memory наиболее интересен для изучения структурного chunking и стабильных ID; kb-mcp — как готовый MCP lexical retrieval компонент; DocSearch — минимальный контроль. Ни одна реализация не получила benchmark PASS.

## 15. Execution results — 2026-11-18

- second-brain-mcp Windows path fix verified on pinned commit 53c45847d178f50b45e7620c0e701380f76cc4f6: TypeScript build PASS, npm test 9/9 PASS, git diff --check PASS. No upstream commit/PR.
- Boring Agent Memory Windows suite: 102/102 PASS after local SQLite connection-cleanup and Windows test portability fixes in isolated clone; not upstream.
- DocSearch Windows suite: 9/9 PASS after test-only Windows adjustments; source unchanged.
- kb-mcp Windows suite: 40 PASS / 1 FAIL / 2 SKIP; one process-lock PID mismatch remains REVIEW.
- Initial lexical probe: 5 synthetic Markdown documents / 11 Russian, English and mixed queries, FTS5/BM25 only. Boring 81.8% evidence recall@5; DocSearch 72.7%; kb-mcp 72.7%. Character sizes are diagnostics, not token counts.
- Boring benchmark-v2: 7 documents / 12 queries; chunked BM25 Recall@1/3 and evidence recall@1/3 = 1.0; MRR 1.0; no-answer precision/source accuracy/stale-conflict accuracy 1.0; privacy leaks 0. Whole-document BM25 evidence recall@1/3 = 0/0.
- Incremental scenario: 1 modified, 1 moved, 1 removed, 4 unchanged; 4 chunks added, 5 removed; removed source absent after apply.
- Russian morphology remains REVIEW. Exact MoE Qwen model/version/quantization/tokenizer and consumer tokenizer remain UNKNOWN; card generation not started. Winner not decided.

Full execution report: https://github.com/RadislavMuranov/aces-os/blob/research/r2-second-brain-chunk-001-2026-11-18/docs/research/R2-SECOND-BRAIN-EXECUTION-RESULTS-2026-11-18.md


## 16. Shared BM25 chunking-isolation results

A shared FTS5 unicode61/BM25 backend was used to isolate chunking strategies from native query-parser differences. On 5 synthetic documents / 11 queries, OR evidence Recall@5 was: paragraph-aware 90.9%, hierarchical prototype 90.9%, Boring structural 90.9%, DocSearch 90.9%, kb-mcp 63.6%, whole-document 0% subsection evidence (although whole-document source recall was 90.9%). OR Precision@5 ranged from 12.7% to 30.9%; AND/phrase modes reduced recall. The hierarchical and paragraph prototypes were indistinguishable on this small fixture. No token counts; character sizes are not token counts. No winner.

Report: https://github.com/RadislavMuranov/aces-os/blob/research/r2-second-brain-chunk-001-2026-11-18/docs/research/R2-SHARED-BM25-RESULTS-2026-11-18.md

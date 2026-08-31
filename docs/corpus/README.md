# ACES Corpus — зафиксированная информация о корпусах

**Репозиторий:** `RadislavMuranov/aces-os`  
**Каталог:** `docs/corpus/`  
**Статус Stage 0:** COMPLETE для DeepSeek + ChatGPT  
**Canon:** 22 (отдельно от корпуса; CONFIRM ≠ Canon)

Этот пакет фиксирует **метаданные и provenance корпусов**, а не сырые ZIP-архивы переписок.
Оригиналы архивов остаются локально (`sources/*/00_ORIGINAL/`) с сохранённым SHA-256.

---

## 1. Корпуса (Stage 0)

| Corpus ID | Platform | Conversations | CONFIRMED | REVIEW | EXCLUDED | Status |
|-----------|----------|---------------|-----------|--------|----------|--------|
| **DEEPSEEK-CORPUS-001** | DeepSeek | 99 | 78 | 12 | 9 | READY_FOR_COMPILATION |
| **CHATGPT-CORPUS-001** | OpenAI ChatGPT | 56 | 56 | 0 | 0 | READY_FOR_COMPILATION |

### Integrity (оригиналы не объединяются)

| Corpus | Export archive | SHA-256 |
|--------|----------------|---------|
| DeepSeek | `deepseek_data-2026-08-11.zip` | `5927590b73f9308b89d57b8b70e68bc204ade1b40da17b516a3a812f3cf90e75` |
| ChatGPT | `chatgpt-export-2026-08-11.zip` | `42e8b11daf45934ecacb472ecef364d30e28767d0dc70e4176f7406571a07a79` |

**Инварианты Stage 0**

- `S0-008` — No Destructive Transformation (нормализация не заменяет исходник)
- `S0-009` — Deterministic Re-indexing
- Оригиналы **никогда** не сливаются; объединяется только семантическое представление с dual provenance

Манифесты:

- [`manifests/DEEPSEEK-CORPUS-001-MANIFEST.yaml`](manifests/DEEPSEEK-CORPUS-001-MANIFEST.yaml)
- [`manifests/CHATGPT-CORPUS-001-MANIFEST.yaml`](manifests/CHATGPT-CORPUS-001-MANIFEST.yaml)

---

## 2. Unified Provenance Index (UPI) v1.0

| Metric | Value |
|--------|------:|
| total_rows | **155** |
| CONFIRMED | **134** |
| REVIEW | **12** |
| EXCLUDED | **9** |
| DEEPSEEK rows | 99 |
| CHATGPT rows | 56 |

**Правила статуса (Stage 0 authoritative)**

| Status | Meaning |
|--------|---------|
| CONFIRMED | eligible for P2 extraction |
| REVIEW | retained; not treated as confirmed knowledge |
| EXCLUDED | negative provenance; **forbidden** as knowledge source (не удаляется) |

**Инварианты UPL**

- UP-001 Dual provenance forever  
- UP-002 Originals never merged  
- UP-003 Stage0 status is authoritative  
- UP-004 Canonical count starts at 0  
- UP-005 Cross-source relations are candidates only  
- UP-006 No silent promotion of EXCLUDED or REVIEW  
- `stage0_status` нельзя повысить/понизить без явного authorization event  

Файлы:

- [`provenance/UNIFIED-PROVENANCE-INDEX-v1.0.json`](provenance/UNIFIED-PROVENANCE-INDEX-v1.0.json)
- [`provenance/UNIFIED-PROVENANCE-INDEX-v1.0.csv`](provenance/UNIFIED-PROVENANCE-INDEX-v1.0.csv)
- [`provenance/unified-provenance-layer-spec-v0.1.md`](provenance/unified-provenance-layer-spec-v0.1.md)
- [`provenance/P2-MANIFEST-v1.0.json`](provenance/P2-MANIFEST-v1.0.json)

---

## 3. Bastion (parallel lineage track)

Bastion — **самостоятельная система**, не модуль ACES.

| Item | Status |
|------|--------|
| Evidence | SUPPORTED |
| PROVEN_EDGE (system transitions) | **0** |
| Evolution Graph | NOT STARTED |
| Bastion → ACES lineage | **LOCKED** |
| Role | evidence workload / optional Human Gate on TO |

Файлы:

- [`bastion/BASTION-CORPUS-001-STAGE0.json`](bastion/BASTION-CORPUS-001-STAGE0.json)
- [`bastion/BASTION-EVIDENCE-PACKAGE-PRE-FREEZE-v0.1.json`](bastion/BASTION-EVIDENCE-PACKAGE-PRE-FREEZE-v0.1.json)
- [`bastion/BASTION-EVOLUTION-DEEP-SPAN-v1.0.json`](bastion/BASTION-EVOLUTION-DEEP-SPAN-v1.0.json)

Эпистемические границы:

- Evidence ≠ History  
- Candidate relation ≠ Transition  
- Version ≠ Evolution  
- Rejection ≠ Replacement  
- Bastion mention ≠ Bastion state ≠ ACES lineage  

---

## 4. Связь с ACES realization

- Canon = **22** (Selective Canon Gate closed)
- Foundation Operational Baseline = FROZEN
- Reconstruction (чаты как драйвер архитектуры) = **CLOSED**
- Operationalization active; Gap только из Observed Failure

`CONFIRM` в корпусе **не** означает Canon.

---

## 5. Структура каталога

```
docs/corpus/
├── README.md
├── CORPUS-CONTROL-BOARD.md
├── manifests/
│   ├── DEEPSEEK-CORPUS-001-MANIFEST.yaml
│   └── CHATGPT-CORPUS-001-MANIFEST.yaml
├── provenance/
│   ├── UNIFIED-PROVENANCE-INDEX-v1.0.json
│   ├── UNIFIED-PROVENANCE-INDEX-v1.0.csv
│   ├── unified-provenance-layer-spec-v0.1.md
│   └── P2-MANIFEST-v1.0.json
└── bastion/
    ├── BASTION-CORPUS-001-STAGE0.json
    ├── BASTION-EVIDENCE-PACKAGE-PRE-FREEZE-v0.1.json
    └── BASTION-EVOLUTION-DEEP-SPAN-v1.0.json
```

**Не включено в git (намеренно):** сырые ZIP exports и полный `conversations.json` — offline с verified SHA-256.

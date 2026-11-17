# R2 Execution Results — 2026-11-18

## Windows remediation: second-brain-mcp

Repository: vladilenm/second-brain-mcp  
Pinned commit: 53c45847d178f50b45e7620c0e701380f76cc4f6

Baseline on Windows: TypeScript build PASS; 4 PASS / 5 FAIL. All five failures were caused by Windows path separator handling in src/vault.ts. Normalize path.relative() through normalizeRelativePath().

Verification:
- Isolated pinned clone: TypeScript build PASS; npm test 9/9 PASS.
- Existing local checkout: npm test 9/9 PASS; git diff --check PASS.
- Existing checkout had pre-existing changes in package.json and package-lock.json; not reset or committed.
- No upstream commit, push or PR.

## Windows candidate test suites

| Candidate | Result |
|---|---|
| hskl18/boring-agent-memory @ 208816994effe344b4268e20def76ed9c046ced6 | 102/102 PASS after local SQLite connection-cleanup fix and Windows-portable test adjustments in isolated clone |
| abhijithviswanathan/docsearch @ c1341ff5bc87320ae968bdb7057effd4f6e43fe2 | 9/9 PASS after test-only symlink/SQLite cleanup adjustments |
| jblenman/kb-mcp @ 5658ea67f36d7bc04a1cbc54947f9c289dd17e06 | 40 PASS / 1 FAIL / 2 SKIP; process-lock PID mismatch remains REVIEW |

No candidate clone changes were committed upstream.

## Cross-candidate lexical probe

Synthetic corpus: 5 Markdown documents; 11 identical queries; Russian, English and mixed-language; headings, frontmatter, nested lists, table, code, quote, long paragraph, exact identifier and inflection cases. Local SQLite FTS5/BM25 only. Character sizes below are structural diagnostics, not token counts.

| Strategy | Chunks | Median chars | Max chars | Recall@1 | Evidence recall@5 |
|---|---:|---:|---:|---:|---:|
| kb-mcp heading-aware | 6 | 303 | 3,868 | 72.7% | 72.7% |
| Boring structural | 23 | 83 | 1,600 | 81.8% | 81.8% |
| DocSearch heading/60-line | 20 | 80.5 | 3,869 | 72.7% | 72.7% |

Boring misses Russian multi-term and English inflection cases. Its query tokenizer emits no Cyrillic tokens; exact phrase search does not establish morphology support. kb-mcp misses include heading attribution in merged sections. This small probe is diagnostic only, not a winner benchmark.

## Boring Agent Memory benchmark-v2

Pinned commit 208816994effe344b4268e20def76ed9c046ced6; 7 documents / 12 queries; Windows; Python 3.14.7; SQLite 3.50.4; no FastEmbed. Reproducibility check exit 0.

| Metric | Chunked BM25 | Whole-document BM25 |
|---|---:|---:|
| Recall@1 | 1.000 | 0.9091 |
| Recall@3 | 1.000 | 1.000 |
| Evidence recall@1 / @3 | 1.000 / 1.000 | 0 / 0 |
| MRR | 1.000 | 0.9545 |
| No-answer precision | 1.000 | 1.000 |
| Source accuracy | 1.000 | 0.9091 |
| Stale-conflict accuracy | 1.000 | 1.000 |
| Privacy leaks | 0 | 0 |
| Build time | 34.439 ms | 36.124 ms |
| Index size | 86,016 bytes | 77,824 bytes |

Dense/hybrid strategies were not run. Incremental scenario: 1 modified, 1 moved, 1 removed, 4 unchanged; 4 chunks added, 5 removed; removed source absent after apply.

## Control state

| Area | Status |
|---|---|
| second-brain-mcp Windows path fix | CONFIRMED — 9/9 |
| Boring Windows tests | CONFIRMED — local research patch only |
| DocSearch Windows tests | CONFIRMED — test portability patch only |
| kb-mcp Windows tests | REVIEW — one process-lock PID mismatch |
| Initial multilingual lexical probe | CONFIRMED — limited scope |
| Russian morphology | REVIEW |
| Actual MoE Qwen token economics | UNKNOWN — model/version/quantization/tokenizer not selected |
| MoE Qwen card generation | NOT STARTED |
| Winner | NOT DECIDED |

## Next gates

1. Resolve kb-mcp Windows process-lock PID mismatch.
2. Expand multilingual corpus and Russian morphology queries.
3. Add paragraph-aware and hierarchical chunkers.
4. Pin the exact MoE Qwen model/version/quantization/tokenizer and consumer tokenizer before token measurements.
5. Run card-generation/provenance experiments separately from retrieval.
6. Independently validate before winner/no-winner decision.

Research-only. No ACES Canon, ACES OS runtime, BASTION, DSH, Orca, local MCP registrations or production data changed.

Raw local results:
- Cross-candidate JSON SHA-256: 99bb0fac38cf9f81c2804d3f751abaaecbcc7696b7942d3fb5e15386b5e73e40
- Boring benchmark-v2 JSON SHA-256: a07db1901cbf0b96611d950a1b59a431cb4edaf340130f955e3611742e568070

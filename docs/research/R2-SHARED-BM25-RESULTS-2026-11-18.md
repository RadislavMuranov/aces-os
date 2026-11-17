# R2 Shared BM25 Chunking-Isolation Results

Date: 2026-11-18  
Corpus: 5 synthetic Markdown documents  
Queries: 11 identical Russian, English and mixed-language queries  
Index/search: shared SQLite FTS5 BM25, unicode61 tokenizer  
Purpose: isolate chunking effects from each candidate's native query parser.

## Method

The same FTS5 schema, tokenizer, ranking weights and query set were used for whole-document, paragraph-aware, hierarchical, kb-mcp heading-aware, Boring structural and DocSearch 60-line strategies. OR, AND and exact phrase query modes were tested. No embeddings, vector search, semantic reranking or LLM calls.

Character sizes are structural diagnostics only, not token counts.

## Results

| Strategy | Chunks | Median chars | Max chars | OR evidence Recall@5 | OR Precision@5 | OR MRR | AND Recall@5 | Phrase Recall@5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Whole-document | 5 | 318 | 4,298 | 0.0% | 0.0% | 0.000 | 0.0% | 0.0% |
| Paragraph-aware | 35 | 23 | 1,600 | 90.9% | 30.9% | 0.909 | 72.7% | 63.6% |
| Hierarchical prototype | 35 | 23 | 1,600 | 90.9% | 30.9% | 0.909 | 72.7% | 63.6% |
| Boring structural | 23 | 83 | 1,600 | 90.9% | 21.8% | 0.909 | 72.7% | 63.6% |
| DocSearch 60-line | 20 | 80.5 | 3,869 | 90.9% | 18.2% | 0.909 | 72.7% | 63.6% |
| kb-mcp heading-aware | 6 | 303 | 3,868 | 63.6% | 12.7% | 0.636 | 45.5% | 36.4% |

Whole-document BM25 had source Recall@5 of 90.9% in OR mode, but evidence Recall@5 was 0% because it did not preserve the expected subsection heading. This is a provenance-granularity failure, not inability to locate the source document.

## Findings

1. Chunk-level retrieval substantially improves evidence localization over whole-document BM25.
2. OR maximizes recall, but precision remains low (12.7–30.9%). AND and phrase modes reduce recall.
3. Boring structural chunking reaches 90.9% evidence recall under the shared tokenizer. Its lower 81.8% native-API result in the separate probe is attributable to its Cyrillic query-tokenization limitation, not chunk boundaries alone.
4. kb-mcp's six larger chunks and merged heading paths reduce evidence-heading precision.
5. Paragraph-aware and hierarchical prototypes are indistinguishable on this fixture; deeper nested-heading and parent/child cases are required.
6. DocSearch reaches high OR recall but has weaker precision and lacks Boring's explicit structural-block protection.

## Limits and control

This is a diagnostic micro-benchmark, not a winner decision. Five documents and eleven queries are insufficient for statistical confidence. The shared tokenizer removes candidate-specific query-parser differences; native API results must be considered alongside this track.

No token counts are reported. Exact MoE Qwen and consumer tokenizers remain unselected.

- Shared BM25 chunking-isolation probe: CONFIRMED — limited diagnostic scope.
- Whole-document evidence provenance: REVIEW.
- Boring structural chunking: promising; native Cyrillic query parser remains REVIEW.
- kb-mcp: REVIEW — merged headings and Windows process-lock test.
- Paragraph vs hierarchical: UNKNOWN — fixture does not distinguish them.
- Token economics: UNKNOWN.
- Winner: NOT DECIDED.

Runner SHA-256: 5d3cce8bedf6acb69035e59f40a2d6c8da363a4e714a7e0e9440f422a55a5e62  
Raw JSON SHA-256: ef5f79ed8df9a6b5b20db7d6a8158445ec585dd015cf491a3a9f9c501a29fc01

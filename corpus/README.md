# ACES Corpus Archive Registry

Status: SOURCE REGISTRY FROZEN — 2026-08-31

This directory records the two independent source corpora used by AKCS-40X.

## Source corpora

| Corpus | Conversations | SHA-256 | Semantic pass | Provenance |
|---|---:|---|---|---|
| DEEPSEEK-CORPUS-001 | 99 | 5927590b73f9308b89d57b8b70e68bc204ade1b40da17b516a3a812f3cf90e75 | APPROVED | PRESERVED |
| CHATGPT-CORPUS-001 | 56 | 42e8b11daf45934ecacb472ecef364d30e28767d0dc70e4176f7406571a07a79 | APPROVED | PRESERVED |

Total source conversations: 155.

## Integrity rule

The original archives are immutable source material. Their SHA-256 values are the identity anchors. Corpus content must not be rewritten, merged, deduplicated, or canonicalized in place.

## Epistemic boundary

Source approval does not imply canonicalization. The corpus is an evidence reservoir; SUPPORTED claims, candidate entities, and later canonical objects are separate layers.

## Archive payload status

The current GitHub connector can create UTF-8 repository files but cannot transfer the original binary ZIP archives from the File Library into GitHub. Therefore this commit freezes the corpus registry and integrity metadata, but MUST NOT be described as a binary archive upload. The original ZIP payloads remain the authoritative source artifacts identified by the hashes above.

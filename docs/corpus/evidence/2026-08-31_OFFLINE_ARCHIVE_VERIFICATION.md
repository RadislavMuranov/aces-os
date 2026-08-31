# Offline Archive Verification

**Date:** 2026-08-31  
**Status:** VERIFIED  
**Environment:** ACES OS agent session (Grok)

## Purpose

Record that the original Stage-0 corpus export archives were present and integrity-checked against the authoritative registry.

## Verified Archives

| Corpus ID | Filename (as received) | Size (bytes) | SHA-256 | Match to CORPUS-REGISTRY-v1.0.json |
|-----------|------------------------|-------------:|---------|------------------------------------|
| DEEPSEEK-CORPUS-001 | `deepseek_data-2026-08-11.zip` | 17 308 413 | `5927590b73f9308b89d57b8b70e68bc204ade1b40da17b516a3a812f3cf90e75` | **EXACT** |
| CHATGPT-CORPUS-001 | `cadf296cf9d3ac590b0c7aef468ace2225b45a0643a2d37a409fc724195f6ac2-2026-08-11-12-09-26-b5cf6ab12f7f413880f5ad3edb6e6e40.zip` | 15 463 309 | `42e8b11daf45934ecacb472ecef364d30e28767d0dc70e4176f7406571a07a79` | **EXACT** |

## Structure (read-only listing)

### DEEPSEEK-CORPUS-001
- `user.json`
- `conversations.json` (~74 MB)

### CHATGPT-CORPUS-001
- `conversations.json` (~49 MB)
- `chat.html`
- `export_manifest.json`
- `user.json`, `user_settings.json`
- multiple `.dat` attachment files
- other service JSON files

## Invariants Observed

- Originals **never merged** (dual provenance preserved).
- Raw ZIP content **not committed** to git (intentional offline policy).
- SHA-256 verified before any content-level archaeology.
- Stage-0 status remains authoritative.

## Consequence for E0.2

Primary evidence required for content-level Upstream Reconstruction is now available in the working environment.
E0.2 can proceed to semantic search inside `conversations.json` of both corpora.

## Provenance

- Registry reference: `docs/corpus/CORPUS-REGISTRY-v1.0.json`
- Verification performed: 2026-08-31 by ACES OS engineering agent
- Command: `sha256sum` on received files

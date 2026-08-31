# UNIFIED-PROVENANCE-INDEX-v1.0

Full index is stored compressed to keep git payloads small.

## Decode

```bash
base64 -d UNIFIED-PROVENANCE-INDEX-v1.0.json.gz.b64 | gzip -d > UNIFIED-PROVENANCE-INDEX-v1.0.json
```

## Totals (from CORPUS-REGISTRY)

- total_rows: 155
- CONFIRMED: 134
- REVIEW: 12
- EXCLUDED: 9
- DEEPSEEK: 99
- CHATGPT: 56

Canonical CSV may be regenerated from the JSON after decode.

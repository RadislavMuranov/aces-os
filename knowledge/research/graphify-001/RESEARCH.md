# ACES OS Research Snapshot — Graphify Labs

- Snapshot date: 2026-10-18
- Status: RESEARCH ONLY — NOT ACCEPTED, NOT INTEGRATED
- Canon / Constitution / DOS / AGS / RS / CTS / RTC: unchanged
- Upstream: https://github.com/Graphify-Labs/graphify
- Inspected upstream ref: `v8`
- Package metadata version observed in `pyproject.toml`: `0.9.92`
- Distribution name: `graphifyy` (two trailing y characters)
- CLI command: `graphify`
- Runtime requirement: Python `>=3.10`
- License declared by current inspected metadata: Apache-2.0
- License files: `LICENSE`, `LICENSE-MIT`, `NOTICE`
- Source file blob SHA observed for `pyproject.toml` at ref `v8`: `fd1131de1ac28313bdd7cbb35a270d220aa7b561`
- Source file blob SHA observed for `SECURITY.md` at ref `v8`: `3de3465c2018c684e90a97e210861cd1a52be40a`

## Purpose

Graphify is a Python knowledge-graph builder and coding-assistant skill. It is not itself an Obsidian Community Plugin. It can export an Obsidian-compatible vault as one output format.

## Architecture observed

Documented pipeline:

`detect → extract → build → cluster → analyze → report → export`

Key modules documented upstream:
- `detect.py`: discover and categorize input files.
- `extract.py`: extract nodes and edges.
- `build.py`: build a NetworkX graph.
- `cluster.py`: community clustering.
- `analyze.py`: high-degree nodes, connections, suggested questions, import cycles, graph diffs.
- `report.py`: generate `GRAPH_REPORT.md`.
- `export.py`: JSON, HTML, Obsidian, SVG, GraphML, Canvas and Cypher exports.
- `security.py`: URL/path/label validation helpers.
- `serve.py`: optional MCP stdio / HTTP server.
- `watch.py`: local file watching and graph updates.

Expected outputs include `graphify-out/graph.json`, `graphify-out/graph.html`, and `graphify-out/GRAPH_REPORT.md`; Obsidian export is also documented.

## Dependency review

Core dependencies declared in `pyproject.toml` include:
- `networkx>=3.4`
- `numpy>=1.21`
- `rapidfuzz>=3.0`
- `tree-sitter>=0.25,<0.26`
- multiple language-specific `tree-sitter-*` grammars
- `tomli` only for Python versions below 3.11

Optional dependency groups include MCP/Starlette, Neo4j, FalkorDB, PDF, file watching, SVG, Leiden clustering, office documents, Google Sheets, video/audio, LLM backends (Anthropic, Gemini/OpenAI-compatible, Bedrock, Kimi/Ollama), SQL/PostgreSQL, Terraform and additional language parsers. Install only extras needed for a controlled test.

## Security and provenance notes

Upstream `SECURITY.md` describes a local-first tool, but not every workflow is offline:
- AST/code parsing is local and deterministic.
- Semantic extraction of documents/media may send their contents to the configured model/backend.
- URL ingestion performs outbound requests to explicitly supplied URLs.
- HTTP MCP transport is opt-in; stdio is the default described mode.
- Upstream documents mitigations for SSRF, oversized downloads, path traversal, HTML injection, prompt injection, and symlink traversal. These are upstream claims, not an independent security audit.

Do not run Graphify over canonical ACES OS materials or private corpora until data-flow, output paths, prompt-injection behavior, and dependencies are tested in an isolated copy.

## License observation

The inspected `v8` metadata declares Apache-2.0 and lists `LICENSE`, `LICENSE-MIT`, and `NOTICE`. `NOTICE` says portions contributed under MIT before relicensing remain available under those terms. Preserve all license/notice files if source is redistributed.

## Version/provenance limitation

The package version `0.9.92` was observed in `pyproject.toml` at the upstream ref `v8`. This snapshot does not claim a verified immutable commit SHA for the complete source tree. The `pyproject.toml` blob SHA above identifies that file only, not the repository tree. Pin a release tag or full commit SHA before any reproducibility test.

## ACES OS decision

**Decision: RESEARCH CANDIDATE ONLY.** No adoption, installation, runtime execution, skill registration, or Canon change is authorized by this snapshot. Next gate: obtain the complete upstream source archive at a pinned commit, verify archive SHA-256, inspect relevant implementation and tests, then run isolated test cases with recorded inputs and outputs.

## Sources

- Repository: https://github.com/Graphify-Labs/graphify
- README at inspected ref: https://github.com/Graphify-Labs/graphify/blob/v8/README.md
- Architecture: https://github.com/Graphify-Labs/graphify/blob/v8/ARCHITECTURE.md
- Package metadata: https://github.com/Graphify-Labs/graphify/blob/v8/pyproject.toml
- Security policy: https://github.com/Graphify-Labs/graphify/blob/v8/SECURITY.md
- License: https://github.com/Graphify-Labs/graphify/blob/v8/LICENSE
- Notice: https://github.com/Graphify-Labs/graphify/blob/v8/NOTICE
- Release reference: https://newreleases.io/project/github/Graphify-Labs/graphify/release/v0.9.92

## Execution log

- 2026-10-18: Reviewed README, architecture, package metadata, security policy, license and notice via repository source views.
- 2026-10-18: Local archive download was not completed: the connected Desktop Commander device is offline, and the available local shell cannot resolve GitHub. No source archive is represented as downloaded.
- 2026-10-18: This report is a research record only; no ACES OS Canon or implementation files were changed.

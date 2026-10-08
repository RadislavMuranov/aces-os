# ACES OS — P0 DOCUMENT VISUALIZER IMPLEMENTATION PREFLIGHT

**Record:** DV-PREFLIGHT-001  
**Status:** ACTIVE / RESEARCH-FIRST  
**Priority:** P0 / HIGH — IMPLEMENTATION-BOUND  
**Epistemic method:** Senior Engineer / Epistemic State: VERIFIED  
**Implementation state:** NOT AUTHORIZED / NOT STARTED  
**Repository:** RadislavMuranov/aces-os  
**DSH baseline:** deepseek-ai/deepseek-harness @ 5badb15009ae1756c3afe0ae0cef1faafc290ccc  
**Scope:** DSH-native document-to-visual-artifact capability for ACES OS  
**Authorization boundary:** research, specification, repository governance records, and local evidence reconstruction only; no runtime ACES↔Orca↔DSH integration, production activation, authority change, or Canon promotion.

---

## 1. Mission

Determine, with source/code evidence, the smallest DSH-native mechanism that can transform a user-provided or workspace document into a provenance-bound derived visual artifact without mutating canonical session history, creating a second workspace, or introducing a new authority layer.

Primary vertical target:

`source document → normalized representation → semantic extraction → transformation contract → artifact → persisted evidence → existing presentation → replay → ACES validation`

The initial implementation candidate is a single `document-visualizer` plugin with multiple transformations, but this record does not authorize implementation.

---

## 2. Research objective

Reconstruct the actual DSH seams for:

1. source/document acquisition;
2. PDF/DOCX/TXT handling;
3. normalization;
4. semantic extraction;
5. transformation contracts;
6. artifact persistence;
7. tool result and session evidence;
8. existing `dsh-visualize` presentation;
9. replay/reconstruction;
10. provenance and epistemic validation.

The result must establish which mechanisms already exist and which, if any, require a new plugin capability.

---

## 3. Non-goals

- No DSH core rewrite.
- No `llm/stream` interception unless the preflight proves it necessary.
- No canonical-history mutation.
- No new ACES database/workspace.
- No image-generation backend as a prerequisite for the first vertical slice.
- No production integration.
- No claim that ACES architectural necessity is established.

---

## 4. Required control chain

```
SOURCE
  ↓
ACQUISITION
  ↓
NORMALIZATION
  ↓
SEMANTIC MODEL
  ↓
TRANSFORMATION
  ↓
DERIVED ARTIFACT
  ↓
PERSISTENCE / EVIDENCE
  ↓
PRESENTATION
  ↓
REPLAY
  ↓
PROVENANCE / EPISTEMIC VALIDATION
```

Each boundary must be evidenced independently. A working UI result is not evidence that the upstream source or provenance boundary is correct.

---

## 5. Current DSH evidence

### 5.1 Generic file acquisition — VERIFIED

DSH has a real generic-file upload path.

The implemented generic-file feature defines a separate file storage scheme, an ordered message attachment list, a `fileUploads` Cordis service, durable content-addressed objects, staged receipts, and Session Controller admission. The accepted user message carries a structured `FileBlock`; no new Session event type is required.

Relevant implementation evidence:

- `packages/client/file-upload`
- `packages/client/ui-conversation`
- `packages/api/session-controller`
- `packages/attachment/attachment`
- `.agents/notes/implemented/feature/2026-08-26-generic-file-upload.md`

The Session Controller resolves file receipts and passes the resulting ordered content through `ctx.attachments.admitPromptContent()`.

**Conclusion:** DSH already has a real source-acquisition seam for uploaded generic files.

### 5.2 Durable attachment/storage — VERIFIED

`ctx.attachments` is a real service seam. Generic files can be persisted through `saveFile` / `saveFileStream` when the mounted provider supports verbatim files. Durable references are content-addressed.

The default attachment provider can reject generic-file storage, therefore the preflight must distinguish the generic file-upload provider path from the image-oriented base attachment implementation.

**Conclusion:** durable source identity exists, but plugin portability depends on which provider is mounted.

### 5.3 Workspace file access — VERIFIED

DSH has a workspace-file service and filesystem tools. Workspace files can be read through bounded file reads and are subject to Session/workspace authorization.

`ctx.fileReferences` supplies path-only completion candidates; `ctx.fs` owns file operations.

**Conclusion:** documents already present in a Session workspace do not require a new acquisition system.

### 5.4 TXT — VERIFIED at capability level; exact semantic ingestion contract OPEN

Plain text is already a native filesystem-readable representation and the document preview registers text rendering.

What remains to verify is the exact plugin-side bounded-read contract and whether the intended visualizer should consume the file through `ctx.fs`, an existing document reader, or a model-visible file path.

### 5.5 DOCX — VERIFIED for conversion/presentation; semantic extraction boundary OPEN

DSH has `ctx.officeToPdf`. Office documents including DOCX are converted locally to PDF for preview. The Desktop Host smoke explicitly exercises DOCX→PDF conversion.

However, PDF preview is not equivalent to a canonical semantic-text extraction API.

**Conclusion:** DOCX acquisition/conversion exists; a deterministic plugin-side semantic extraction path for DOCX still requires code-level reconstruction.

### 5.6 PDF — VERIFIED for preview; semantic text extraction OPEN

DSH contains PDF.js and a PDF preview path. This proves PDF bytes can be rendered and selectable text is available to the document-preview subsystem.

It does not yet prove the existence of a provider-neutral, plugin-facing PDF-to-text extraction service.

The web subsystem explicitly records text-extractable PDF handling as deferred for `web_fetch`; this must not be confused with local PDF preview.

**Conclusion:** PDF presentation is verified; reusable semantic text extraction for a plugin is UNKNOWN until the exact PDF reader/parser seam is reconstructed.

---

## 6. Critical architectural finding

The source-acquisition problem is substantially solved for:

- workspace TXT;
- uploaded generic files;
- DOCX conversion to PDF;
- PDF rendering.

The unresolved seam is **semantic extraction**, not file transport.

Therefore the project must not create a new upload/storage subsystem.

The next research question is:

> Can the existing DSH file/PDF/Office capabilities expose sufficient bounded, deterministic text/content to a plugin without adding a new general document platform?

---

## 7. Proposed plugin boundary

Candidate:

`@aces-os/dsh-document-visualizer`

Conceptual API:

```
document_visualize(
  source,
  mode,
  options
)
```

Modes:

- flashcards
- flowchart
- mindmap
- comic
- sketchnote

The plugin should produce a structured derived artifact before rendering.

It must not make the rendered UI the canonical object.

---

## 8. Semantic model requirement

Do not independently reinterpret the source for every visual mode.

Required architecture:

```
SOURCE
  ↓
SemanticDocument
  ├── claims
  ├── concepts
  ├── sections
  ├── entities
  ├── relations
  ├── processes
  └── uncertainty
       ↓
  transformation
       ↓
  artifact
```

This provides one source interpretation and multiple projections.

---

## 9. Renderer boundary

The existing `dsh-visualize` mechanism is a donor for presentation, not authority.

Use it where evidence confirms:

- tool registration;
- bundled skill;
- workspace persistence;
- presentation metadata;
- replay behavior.

The semantic artifact must remain renderer-independent.

First target:

`SemanticDocument → FlowchartSpec → Mermaid/HTML → existing visualization presentation`

No image-generation backend is required for the first vertical slice.

---

## 10. ACES invariants

### DV-I01 — Canonical preservation

Document visualizer MUST NOT mutate canonical source content.

### DV-I02 — Session preservation

Derived visualization MUST NOT silently rewrite canonical session history.

### DV-I03 — Provenance

Every derived artifact MUST retain a reconstructible reference to its source and transformation.

### DV-I04 — Epistemic separation

Source observations, semantic derivations, and presentation artifacts remain distinct.

### DV-I05 — No authority escalation

`DerivedArtifact ⇏ AcceptedState`.

### DV-I06 — Replay

A persisted artifact/presentation must be reconstructible from durable evidence rather than undocumented transient state.

### DV-I07 — Renderer independence

Semantic artifact identity must not depend on a particular UI renderer.

### DV-I08 — Bounded reads

Document ingestion must use bounded byte/read policies and cancellation.

---

## 11. Acceptance gates

### G0 — Scope integrity

Original objective and current scope are preserved.

### G1 — DSH source acquisition

PDF/DOCX/TXT and workspace/upload paths are reconstructed from implementation evidence.

### G2 — Normalization

Exact normalized representation and ownership are verified.

### G3 — Semantic extraction

A real, bounded extraction seam is identified or the gap is explicitly recorded.

### G4 — Transformation contract

At least one structured artifact contract is defined without coupling it to UI.

### G5 — Persistence/evidence

Artifact identity, source reference, transformation identity, and replay evidence are reconstructible.

### G6 — Presentation

Existing DSH presentation seam is reused without authority capture.

### G7 — Replay

A derived artifact can be reconstructed after session reload/replay.

### G8 — ACES validation

Provenance and epistemic invariants are independently checked.

### G9 — Minimality

No existing DSH capability has been duplicated unnecessarily.

### G10 — Implementation authorization

Only after G0–G9 PASS may a separate implementation authorization be considered.

---

## 12. Plan

### WP-1 — Source acquisition reconstruction

Reconstruct exact code paths for:

- browser generic-file upload;
- file receipt;
- Session Controller admission;
- durable file reference;
- workspace file read;
- TXT read;
- PDF access;
- DOCX access/conversion.

### WP-2 — Semantic extraction reconstruction

Identify the smallest existing mechanism for extracting bounded text/structure from:

- TXT;
- PDF;
- DOCX.

Classify each as:

`IMPLEMENTED / DOCUMENTED / EXTERNAL / INFERENCE / UNKNOWN`.

### WP-3 — Normalization contract

Define the minimal normalized source envelope only after WP-1/2 evidence.

### WP-4 — Transformation contract

Define `FlowchartSpec` first.

### WP-5 — Artifact persistence/evidence

Reconstruct existing DSH persistence/replay mechanisms and determine whether the artifact can be persisted without new core state.

### WP-6 — Presentation seam

Reconstruct `dsh-visualize` integration and determine the minimum reusable surface.

### WP-7 — ACES verification

Test provenance, epistemic separation, canonical preservation, and replay.

### WP-8 — Implementation pre-authorization verdict

Produce one of:

- IMPLEMENTATION READY;
- BLOCKED;
- EXISTING CAPABILITY SUFFICIENT;
- NEW DSH SEAM REQUIRED.

No implementation begins before this verdict and separate authorization.

---

## 13. Roadmap

**Phase P0 — Implementation Preflight — ACTIVE**

WP-1 → WP-8.

**Phase P1 — Minimal vertical slice — NOT AUTHORIZED**

Only if P0 passes:

`TXT/PDF/DOCX source → FlowchartSpec → persisted artifact → dsh-visualize presentation → replay`.

**Phase P2 — Additional projections — NOT AUTHORIZED**

Mindmap → Flashcards → Sketchnote → ComicSpec.

**Phase P3 — Optional image renderer — NOT AUTHORIZED**

Only after ComicSpec/Sketchnote are independently useful without image generation.

---

## 14. Control for the plan

Every work package must record:

`OBJECTIVE / SOURCE / CLAIM / EVIDENCE / EPISTEMIC STATE / UNKNOWN / DECISION / NEXT GATE`.

No package closes on documentation alone when implementation evidence is required.

No implementation task may be introduced merely because a research gap is discovered.

A new DSH core seam requires explicit evidence that plugin-level composition is insufficient.

---

## 15. Required evidence hierarchy

1. Implementation/code evidence.
2. Tests demonstrating behavior.
3. DSH architectural documentation.
4. Maintainer/decision records.
5. External/community implementation evidence.
6. Inference.
7. UNKNOWN.

Claims must not be promoted above their evidence class.

---

## 16. Known risks

- PDF preview may expose text only inside Client rendering code, not as a reusable plugin service.
- DOCX→PDF may be presentation infrastructure rather than semantic extraction.
- Generic file durability does not imply semantic readability.
- `dsh-visualize` persistence may be sufficient for presentation but insufficient for ACES provenance.
- LLM-generated semantic extraction may introduce unsupported claims unless source references and uncertainty are preserved.
- A visually correct artifact can still be epistemically invalid.
- A plugin can accidentally become a second document owner if it stores source content rather than derived artifacts.

---

## 17. Current verdict

**P0 PREFLIGHT: ACTIVE / INCOMPLETE.**

Verified:

- DSH has generic-file acquisition.
- DSH has durable file-upload/storage machinery.
- DSH has workspace file access.
- DSH has DOCX→PDF conversion.
- DSH has PDF preview/rendering.
- DSH has an existing visualization plugin seam suitable for donor analysis.

Not yet verified:

- one provider-neutral semantic extraction API for PDF;
- one provider-neutral semantic extraction API for DOCX;
- exact plugin-facing normalization contract;
- complete artifact/session replay path for this new derived artifact;
- ACES provenance binding at the DSH plugin boundary.

Therefore:

**IMPLEMENTATION: BLOCKED BY PREFLIGHT, NOT AUTHORIZED.**

The correct next action is WP-1/WP-2 code-level reconstruction, not plugin coding.

---

## 18. Iteration control

This record is governed by the ACES Master Protocol mandatory loop:

`REPOSITORY BEFORE → CLAIMS → ACTION → REPOSITORY AFTER → VERIFICATION → BUG AUDIT → ADVERSARIAL SEARCH → REFACTOR/DELETE → RE-VERIFY → FAILURE FILTER → BUG BASE → ITERATION VERDICT`.

Any contradiction must be recorded as:

`PREVIOUS CLAIM → CONTRADICTION → BUG → IMPACT → CORRECTION → PREVENTION`.

No PASS may be claimed while a required evidence or verification gate remains open.

---

## 19. Authorization record

**Current authorization:** research/specification/governance materialization only.

**Not authorized:** implementation, runtime activation, production integration, ACES↔Orca↔DSH integration, authority changes, Canon promotion.

A separate implementation authorization is required after P0 closure.

---

## 20. Priority

This record is **P0 / HIGH PRIORITY** for the DSH Harness ACES OS implementation track.

It is an implementation-readiness control record, not an implementation claim.

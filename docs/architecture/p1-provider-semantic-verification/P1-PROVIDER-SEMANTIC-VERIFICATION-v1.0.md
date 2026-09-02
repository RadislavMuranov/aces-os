# P1 Provider Semantic Verification v1.0

**Status:** EVIDENCE PACK  
**Date:** 2026-09-03  
**Live system access:** **NONE** this gate  
**Upstream:** P1 Contract Preparation @ `12d3026412f416dda850bbcbce12a93177ab3532`

---

## 0. Primary question

> Do the real semantic models of the six providers fit the provider-neutral P1 contract sufficiently to permit a deterministic, provider-safe **implementation design**?

**Answer:** **YES, with bounded residuals** — FIT or FIT WITH ADAPTER NORMALIZATION for all six on official-spec evidence; **no BLOCKING GAP** against P0/P1 invariants. Residuals are **PROVIDER-VERIFICATION-REQUIRED** (live/config-specific) or **PARTIAL**, not architectural conflicts.

---

## 1. Obsidian — VERIFIED-BY-OFFICIAL-SPEC (core)

| Topic | Finding |
|-------|---------|
| Container | Vault = folder + subfolders (docs.obsidian.md/Plugins/Vault) |
| Identity | Path within vault; path mutable on rename/move. Path ≠ immutable content id |
| Delete | `delete()` hard; `trash()` system or vault `.trash` |
| Timestamps | FS mtime; not global order authority |
| Revisions | No git-like SHA; content hash **derived** |
| Events | No core webhook model; watch/poll — **PARTIAL** |
| CLA/native | Local filesystem preferred |
| Sync/plugins | **PVR** |

**Fit:** FIT WITH ADAPTER NORMALIZATION

---

## 2. GitHub — VERIFIED-BY-OFFICIAL-SPEC

| Topic | Finding |
|-------|---------|
| Namespace | owner/repo |
| Immutable | Commit/blob/tree SHA |
| Mutable | Branch/tag **ref** → SHA (rewritable) |
| Issues/PRs | Numeric id / node_id |
| Critical | **branch reference ≠ commit identity** |
| CLA/native | REST/GraphQL/git |

**Fit:** FIT

---

## 3. Slack — VERIFIED-BY-OFFICIAL-SPEC

| Topic | Finding |
|-------|---------|
| Message id | channel + **ts** (unique per channel) |
| Threads | thread_ts |
| Edit/delete | chat.update / chat.delete; original text not available after edit |
| Events | event_id on Events API envelope |
| Retention/Grid | **PVR** |
| CLA/native | Web API |

**Fit:** FIT WITH ADAPTER NORMALIZATION

---

## 4. Gmail — VERIFIED-BY-OFFICIAL-SPEC

| Topic | Finding |
|-------|---------|
| Message | API `id` immutable |
| Thread | Distinct `threadId` — **thread ≠ message** |
| RFC Message-ID | ≠ Gmail API message id |
| Time | internalDate |
| History | history.list; non-contiguous historyId; limited validity window |
| CLA/native | Gmail API |

**Fit:** FIT

---

## 5. Google Drive — VERIFIED-BY-OFFICIAL-SPEC

| Topic | Finding |
|-------|---------|
| Identity | **fileId**; path/name ≠ identity |
| Trash | trashed flag; trash vs permanent delete |
| Revisions | revisionId; keepForever |
| Shortcuts | targetId |
| Shared-drive edges | **PVR** |
| CLA/native | Drive API |

**Fit:** FIT

---

## 6. Kaiten — VERIFIED-BY-OFFICIAL-SPEC + PARTIAL

| Topic | Finding |
|-------|---------|
| Space | id + uid |
| Card/board | integer ids; condition live/archived/deleted; state queued/inProgress/done |
| Webhooks | Named events documented — payload completeness **PARTIAL/PVR** |
| Rate limit | ~5 rps (extracted general info) — **PARTIAL** |
| CLA/native | REST `/api/latest` |

**Fit:** FIT WITH ADAPTER NORMALIZATION

---

## 7. Invariant stress test

All 15 critical invariants from the gate brief: **PASS** (no provider forces Observation→AcceptedState, branch-as-truth, path-as-identity without adapter rules, or Source Authority as ACES Authority).

**No BLOCKING GAP.**

## 8. MCP

No provider **requires** MCP as sole path given native APIs/FS.

**END**

# ACES OS — AUDIT RECORD: DATA-LOSS INCIDENT (worktree untraceability)

**Record ID:** BUG-024 / DLPM-001-INCIDENT
**Registered:** 2026-11-25
**Forensic status:** HISTORICAL INCIDENT — OWNER-ATTRIBUTED, EVIDENCE-CORROBORATED
**Disposition:** CLOSED-WITH-CORRECTION (recovery completed, prevention deployed)

---

## 1. Incident specification

**What appeared to happen (initial finding, 2026-11-25 01:30):** the local
repository documented at `C:\Users\Радислав Муранов\aces-os` — holding the
entire unpushed policy-to-hook enforcement implementation (engine,
policy-controls, 23-defect / 155-section map, 420-test suite, slash-commands,
AutoClaw bridge) — was found missing. Forensics could not identify the actor:
USN journal rotated past the window, no VSS shadows, no Recycle Bin trace, no
deletion command in PowerShell/ZCode histories.

**What actually happened (corrected, 2026-11-25 03:3x):** the live worktree
exists at **`C:\ACES\aces-os`** (branch `implementation/aces-node-baseline`,
commits `e38c2c9` → `c5b2082` → `8264c41`, 8 commits ahead of `main`, full
infrastructure intact, **420/420 tests PASS**). The documented path
`C:\Users\Радислав Муранов\aces-os` no longer resolves. The incident is
therefore **path untraceability of a relocated, unpushed worktree**, not data
destruction. The relocation happened inside the 22.11–25.11 window; the actor
of the move is not logged.

**Owner attribution (2026-11-25):** two AutoClaw sessions during ACES Second
Brain verification. Corroborating evidence:

1. AutoClaw runtime logs (22–24.11) record **828 ungated `exec` tool calls**
   across 13 sessions (22.11), 1 spanning session (22→23.11, `f7461985…`),
   and 4 sessions (24.11: `53b10392`, `aaab1c8d`, `c13cd754`, `d998d6d8`).
2. AutoClaw's environment includes **Desktop Commander** (full shell access).
3. The Second Brain (Obsidian Vault) was damaged in the same window and
   restored from `E:\ACES-Backups\snapshot-2026-11-24-rollback\Obsidian-Vault-full`
   on 24.11 — matching "first the Second Brain, then the repo path".
4. AutoClaw implements **no PreToolUse/Stop hooks**; its exec calls pass no
   ACES gate. The aces-bridge MCP that gates them lives inside the repo
   itself.
5. Exec command texts are not persisted in runtime logs (tool names only).

## 2. Root cause (structural, canonical formulation)

**RC-1 (primary): path untraceability.** A single live copy of critical work
existed at an undocumented, unreferenced location, with the documented
location stale. Any agent-driven relocation or cleanup silently breaks every
downstream consumer.

**RC-2 (aggravating): zero remote publication.** The 8-commit branch was
never pushed; a single `rm -rf` at the live path would have been
unrecoverable.

**RC-3 (enabling): ungated agent shell access.** Agents with full shell
access (AutoClaw + Desktop Commander) operate on protected roots without any
PreToolUse gate.

## 3. Recovery (completed)

* Live worktree located: `C:\ACES\aces-os` — 420/420 tests PASS.
* Original Z-1…Z-8 registry extracted verbatim from the original engine and
  restored in the rebuild branch (canonical semantics; superseding the
  interim 2026-11-25 redefinitions).
* Original branch pushed to remote: **`implementation/aces-node-baseline-orig`**.
* Adversarial sandboxes (`draft-a8006162/adv/sandbox*`) and the AutoClaw
  `aces-integration/_stage` copies serve as secondary recovery artifacts.

## 4. Correction (deployed, DLPM-001)

Three-store policy — work is not done until it exists in GitHub (push),
snapshot archive (`tools/protection/aces-snapshot.ps1`, task `ACES-Snapshot`,
daily 03:30, `E:\ACES-Backups\aces-os\snapshots\`, 30-copy rotation), and an
Obsidian record. Notion = manual checkpoint.

Hard delete guard in the hook engine: canonical Z-1…Z-8 (recovered) plus
DLPM-1 (protected-root deletion DENY), DLPM-4/5/7 (untracked/history
destruction DENY), DLPM-6 (branch deletion ASK).

**Canonical-path requirement (new):** the active worktree location must be
recorded in this document and in RAD-80, and any relocation must be committed
to the tracker in the same action. Current canonical location:
`C:\ACES\aces-os` (original worktree, unpushed→pushed) and
`C:\Users\Радислав Муранов\aces-os` (rebuild branch; snapshot/archive source).

## 5. Residual risk / open items

* Two same-named branches now diverge on the remote:
  `implementation/aces-node-baseline` (rebuild + DLPM-001) and
  `implementation/aces-node-baseline-orig` (original work). Merge decision
  pending owner approval.
* AutoClaw exec calls remain ungated until the aces-bridge is restored and
  mandated as its MCP layer (separate task).
* The relocation actor/move event itself remains unlogged (no FS audit trail).

## 6. Tests

Rebuild branch: `node --test tests/*.test.ts tests/hooks/*.test.mjs` →
**71/71 PASS** (canonical Z-registry + DLPM + alias/adversarial/false-positive
coverage). Original worktree: **420/420 PASS**.

## 7. Cross-system records

* Linear: RAD-80 (rebuild + correction checkpoints), RAD-86 (closed)
* Obsidian: `02-Evidence-and-Verification/records/2026-11-25-ACES-OS-Data-Loss-Incident-and-Protection-Method.md`
* GitHub: `docs/audit/2026-11-25-DATA-LOSS-INCIDENT-BUG-024.md` (this file),
  `docs/protection/DATA-LOSS-PROTECTION-METHOD.md`
* Notion: owner manual checkpoint (no API from this machine)

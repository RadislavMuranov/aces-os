# ACES OS — DATA-LOSS PROTECTION METHOD

**Record:** DLPM-001
**Status:** ACTIVE (pending owner ratification of Z-1, Z-4…Z-7 redefinitions)
**Created:** 2026-11-25
**Trigger:** total loss of the aces-os local worktree (see RAD-80, «Утрата исходного воркитри»)

## 1. Incident summary (why this method exists)

**Cause (stated by the owner 2026-11-25, corroborated by evidence):** two
AutoClaw sessions during ACES Second Brain verification destroyed first the
Second Brain itself, then the aces-os repository. AutoClaw logs record
**828 exec tool calls** across 22–24.11 (13 sessions on 22.11, 1 spanning
22→23.11, 4 on 24.11); its environment includes Desktop Commander (full
shell access). AutoClaw implements no PreToolUse/Stop hooks, so none of
those calls passed any ACES gate; the aces-bridge MCP that would have gated
them lived inside the destroyed worktree. The Obsidian Vault was restored
from the 24.11 rollback snapshot; the repo was not covered by it and was
lost permanently. Exec command texts are not persisted in the logs.

On 2026-11-25 the local repository `C:\Users\Радислав Муранов\aces-os` —
including the entire policy-to-hook enforcement implementation, 388 hook
tests, the defect/policy maps and the AutoClaw bridge — was found deleted.
Established window: alive 22.11.2026 16:25–18:42 (last ZCode session usage),
gone by 25.11.2026 01:30. The USN journal had already rotated past the
deletion window; no shadow copies exist; the Recycle Bin contains no trace;
no deletion command appears in PowerShell or ZCode histories.

The root cause is structural, not mysterious:

> The work existed as a **single uncommitted local copy**, and an agent with
> full shell access operated on it **without any hook gate and without any
> snapshot of the target**. Any single destructive event erases it permanently.

## 2. Method (per RULE-METHOD-SELECTION-001)

* **Object:** durability of all ACES work products against any single
  destructive event.
* **Unknowns:** the deletion actor; whether it can recur.
* **Alternatives considered:**
  1. Forensic hardening (audit logging, Sysmon) — rejected as primary: does
     not prevent loss, only documents it.
  2. Full backup infrastructure — rejected as disproportionate for one
     machine.
  3. **Three independent copies + hard delete guard — selected** as the
     minimal sufficient method: every work product exists in GitHub (push),
     a local snapshot archive (scheduled), and a record in Obsidian; the
     hook engine denies deletion of the protected roots.
* **Stop condition:** method is active while all three stores verify.

## 3. The three-store policy (always-on)

| Store | What | How | When |
|---|---|---|---|
| **GitHub** | every commit of every branch | `git push` (required before ending work on any task) | on every commit |
| **Snapshot archive** | git bundle + tree archive of the repo | `tools/protection/aces-snapshot.ps1` → `E:\ACES-Backups\aces-os\snapshots\` | daily (scheduled task `ACES-Snapshot`) + before risky work |
| **Obsidian** | evidence record for every iteration | record in `02-Evidence-and-Verification/records/` | every session that changes the repo |

**Notion** additionally holds the human-readable iteration checkpoint for
each stage (manual step — no API access from this machine).

Rule: **work is not "done" until it exists in all three stores.**
Uncommitted/unpushed work may not be reported as complete.

## 4. Hard delete guard (Z-registry canonical + DLPM additions, hook-enforced)

The ACES hook engine enforces the user-approved Z-registry — **recovered
2026-11-25 verbatim from the original engine found alive at
`C:\ACES\aces-os`** — plus the DLPM data-loss additions:

| ID | Rule | Decision | Origin |
|---|---|---|---|
| Z-1 | `core.hooksPath` change / override; `git commit --no-verify` | **DENY** | canonical (recovered) |
| Z-2 | `git stash` (all operations) | **DENY** | canonical (recovered) |
| Z-3 | `git reset --hard` | **DENY** | canonical (recovered) |
| Z-4 | `git rebase` | **DENY** | canonical (recovered) |
| Z-5 | force push (`--force`/`-f`/`--force-with-lease`/`+`refspec) | **DENY** | canonical (recovered) |
| Z-6 | broad `git add` (`-A`/`--all`/`-u`/`.`) | **DENY** | canonical (recovered) |
| Z-7 | `git commit -a`; commit without explicit paths after `--` | **DENY** | canonical (recovered) |
| Z-8 | reading `.env` / `.env.*` (`.env.example` allowed) | **DENY** | canonical (recovered) |
| DLPM-1 | deletion of protected roots (repo root, `.git`, `.claude`, Obsidian Vault) | **DENY** | DLPM-001 addition |
| DLPM-4 | `git clean -f*` | **DENY** | DLPM-001 addition |
| DLPM-5 | whole-tree discard (`git checkout -- .`, `git restore .`) | **DENY** | DLPM-001 addition |
| DLPM-6 | `git branch -D` | **ASK** | DLPM-001 addition |
| DLPM-7 | `git filter-branch`, `git reflog expire` | **DENY** | DLPM-001 addition |

The earlier "redefined Z-1, Z-4…Z-7" of this document are **superseded**: the
original user-approved definitions were recovered from the live worktree at
`C:\ACES\aces-os` (which also restored the original 420-test suite, the
defect-enforcement map with 23 defects and 155 policy sections, and the
AutoClaw bridge). The redefinitions live on only as the DLPM-* family.

## 5. Verification

* `node --test tests/*.test.ts tests/hooks/*.test.mjs` → 56 passed, 0 failed.
* Snapshot script self-verifies: bundle integrity (`git bundle verify`) and
  manifest sha256 are checked; failures exit non-zero and are logged.
* Scheduled task: `schtasks /query /tn ACES-Snapshot` must show "Готово"
  after the next daily trigger.

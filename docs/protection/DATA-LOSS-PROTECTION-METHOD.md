# ACES OS — DATA-LOSS PROTECTION METHOD

**Record:** DLPM-001
**Status:** ACTIVE (pending owner ratification of Z-1, Z-4…Z-7 redefinitions)
**Created:** 2026-11-25
**Trigger:** total loss of the aces-os local worktree (see RAD-80, «Утрата исходного воркитри»)

## 1. Incident summary (why this method exists)

On 2026-11-25 the local repository `C:\Users\Радислав Муранов\aces-os` —
including the entire policy-to-hook enforcement implementation, 388 hook
tests, the defect/policy maps and the AutoClaw bridge — was found deleted.
Established window: alive 22.11.2026 16:25–18:42 (last ZCode session usage),
gone by 25.11.2026 01:30. The USN journal had already rotated past the
deletion window; no shadow copies exist; the Recycle Bin contains no trace;
no deletion command appears in PowerShell or ZCode histories. The actor and
exact moment are therefore **UNKNOWABLE** on this machine.

The root cause is structural, not mysterious:

> The work existed as a **single uncommitted local copy**. Any one
> accidental deletion, cleanup pass, or tool action erases it permanently.

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

## 4. Hard delete guard (Z-controls, hook-enforced)

The ACES hook engine enforces the Z-registry at the PreToolUse boundary:

| ID | Rule | Decision | Origin |
|---|---|---|---|
| Z-1 | deletion of protected roots (repo root, `.git`, `.claude`, Obsidian Vault) via `rm`/`Remove-Item -Recurse` | **DENY** | redefined 2026-11-25 |
| Z-2 | `git stash` | **DENY** | original (surviving) |
| Z-3 | `git reset --hard` | **DENY** | original (surviving) |
| Z-4 | `git clean -f*` | **DENY** | redefined 2026-11-25 |
| Z-5 | whole-tree discard (`git checkout -- .`, `git restore .`) | **DENY** | redefined 2026-11-25 |
| Z-6 | `git branch -D`, `git push --force/--delete` | **ASK** | redefined 2026-11-25 |
| Z-7 | `git filter-branch`, `git reflog expire` | **DENY** | redefined 2026-11-25 |
| Z-8 | reading `.env` | **DENY** | original (surviving) |

Redefined IDs follow the loss-prevention class of the surviving members
(Z-2/Z-3/Z-8) and close the exact loss vector that destroyed the worktree.
They require owner ratification (see RAD-80).

## 5. Verification

* `node --test tests/*.test.ts tests/hooks/*.test.mjs` → 56 passed, 0 failed.
* Snapshot script self-verifies: bundle integrity (`git bundle verify`) and
  manifest sha256 are checked; failures exit non-zero and are logged.
* Scheduled task: `schtasks /query /tn ACES-Snapshot` must show "Готово"
  after the next daily trigger.

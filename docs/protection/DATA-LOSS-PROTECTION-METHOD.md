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

---

# DLPM-002 — WRITE AUTHORITY (WA-1)

**Record:** DLPM-002
**Status:** AUTHORIZED / SPECIFICATION RECORDED / NOT IMPLEMENTED
**Authorized:** 2026-11-27 by the owner (explicit instruction, this session)
**Binding specification:** `spec/asa/v0/data-model.md` §11 (ASA-003.3)
**Parent:** DLPM-001
**R0 exception:** explicitly recorded in §0 of this record, per
`docs/audit/PRE-KMA-12-RECOVERY-ROADMAP.md` §2.6.

## 0. Authorization record

Owner instruction (verbatim):

> «Авторизовать WA-1 как расширение существующих компонентов (ASA v0 + hook engine + DLPM +
> git), а не как новый слой.»

Recorded interpretation: WA-1 is authorized as an **enforcement binding** of the existing ASA v0
model onto the existing components. It is **not** authorized as a new subsystem, a new Canon, a
new registry, a second hook, or a second enforcement path.

This paragraph is the separately recorded authorization required by the R0 containment rule. It
permits extension of `spec/asa/v0/data-model.md` (§11), `.claude/hooks/aces-hook-engine.mjs`,
this DLPM record, `tools/protection/aces-snapshot.ps1`, and git-based staging. It permits no
other architectural change.

## 1. Mission

No harness, agent, bot, connector, or model can create or delete a durable ACES document without
a fresh ALLOW Decision from a single write authority that operates **outside** the agent; the
prohibition must remain effective for agents that have no hooks at all.

**Success condition (falsifiable):**

1. from a harness with no hooks, creating a file in the durable zone fails at the OS boundary;
2. the same operation in the staging zone succeeds;
3. every durable mutation has a matching AuthorizationEvent;
4. every deletion is recoverable for the retention window;
5. the existing 81-test suite remains green and the Stop owner remains exactly one.

## 2. Plan

| Stage | Objective | Exit evidence | Rollout mode |
|---|---|---|---|
| **W0** | Record + durability of the completed Stop-gate repair | commit `f1e40a7` on origin (0/0), snapshot bundle verified, this record | n/a |
| **W1** | Extend the **existing** policy body with WA-CREATE / WA-DELETE rules | rule table in the engine header + DLPM-002 table; no new file | observe |
| **W2** | Add `evaluateFileIntent({operation, resource, manifest})` to the existing engine; extend the journal to AuthorizationEvent fields | unit tests for every §11.5 operation; journal rows carry `correlation_id`/`operation`/`resource_id`/`decision` | observe |
| **W3** | Non-hook adapter: CLI mode of the **same** engine for harnesses without hooks | bypass tests (alias, `Start-Process`, `iex`, interpreter, MCP filesystem) | advisory |
| **W4** | Identity boundary (E3): agent identity with no write ACE on the durable zone; gate under a separate identity; MCP servers inherit the agent identity | probe from a no-hook harness: durable write denied, staging write allowed | enforced |
| **W5** | Store gate (E4): staging → gate apply; quarantine + retention for DELETE; reconciliation in the snapshot tool | V3/V4 evidence; unrecorded file detected as integrity violation | enforced |
| **W6** | Verification and ratification | V1–V5 executed, regression green, owner ratification recorded | enforced |

**Ordering constraint (non-negotiable):** `enforced` mode may not be enabled before **W4 and W5**
land. W2 ships in `observe` (journal-only, no blocking) so that the gate never blocks the
legitimate writes it has not yet learned to authorize. Enabling enforcement first would lock the
owner out of their own repository and force the control to be disabled — a control that cannot be
lived with is bypassed.

## 3. Plan control

Checked at every stage boundary; a failed check stops the stage.

| ID | Check | Failure action |
|---|---|---|
| **C1** | **Scope:** only the file set declared for the stage was touched | STOP; record the extra path; revert unauthorized edits |
| **C2** | **Order:** the predecessor stage's exit evidence exists before the successor starts | STOP; do not start the stage |
| **C3** | **Evidence:** the exit claim is backed by an executed probe (command + output) or a named passing test, not by a statement | treat the stage as NOT DONE |
| **C4** | **Owner sufficiency:** re-run the B-134 check — does an existing component already own this responsibility? | abort the new component; extend the owner |

**Deviation rule:** any deviation is recorded as
`DEVIATION: <stage> <what> <why> <authorization>`; an unrecorded deviation is a FAIL of the stage,
not a footnote.

## 4. Roadmap

```text
W0  record + durability          [DONE]
 ↓
W1  policy body extension        [NEXT]
 ↓
W2  file-intent in existing engine (observe)
 ↓
W4  identity boundary E3  ──────► **minimum credible enforcement line**
 ↓
W5  store gate E4 + quarantine + reconcile
 ↓
W3  non-hook CLI adapter (may run in parallel with W4)
 ↓
W6  adversarial verification → owner ratification → enforced
```

`W4` is the minimum credible enforcement line: below it, WA-1 is advisory and must be reported
as advisory (ASA-003.3 §11.7 coverage rule).

## 5. Master checklist

| ID | Requirement | Evidence required | Status 2026-11-27 |
|---|---|---|---|
| MC-1 | Stop-gate repair committed and pushed | `f1e40a7`, origin `0 0` | **DONE** |
| MC-2 | Local snapshot exists and verifies | bundle verified, `worktree.zip`, `manifest.sha256` (2026-11-27-014856) | **DONE** |
| MC-3 | Obsidian evidence record appended | snapshot log line written by `aces-snapshot.ps1` | **DONE** |
| MC-4 | ASA-003.3 recorded, §0–§10 unchanged | `spec/asa/v0/data-model.md` §11 | **DONE** |
| MC-5 | WA-CREATE / WA-DELETE added to the existing policy body | rule table + engine header; no new file | **NOT STARTED** |
| MC-6 | `evaluateFileIntent` in the existing engine, `observe` mode | named unit tests; journal fields | **NOT STARTED** |
| MC-7 | E3 identity boundary (no write ACE for agents) | OS probe from a no-hook harness | **NOT STARTED** |
| MC-8 | E4 gate: staging, quarantine, retention, reconcile | V3/V4 evidence | **NOT STARTED** |
| MC-9 | Non-hook adapter (CLI, same engine) | bypass matrix tests | **NOT STARTED** |
| MC-10 | Exactly one Stop owner; no second hook/ledger/registry | settings assertion test + tree check | **PASS (so far)** |
| MC-11 | Regression | `node --test tests/*.test.ts tests/hooks/*.test.mjs` → 81/81 | **PASS** |
| MC-12 | Owner ratification of `enforced` mode | explicit owner decision recorded | **NOT STARTED** |

## 6. Rules that would repeat the original defect

- creating a second hook, a "write guard" service, a per-harness adapter matrix, or a new
  capability registry;
- treating E1/E2 (hooks, proxies) as the authority boundary — H-CENSUS-003 §8 forbids it;
- authorizing `EXECUTE` by static command parsing — the AutoClaw class defeats it;
- enabling `enforced` before W4/W5, then disabling it because it blocks legitimate work;
- editing §0–§10 of ASA v0 instead of adding the binding profile;
- mass-deleting anything to "simplify" before W6 evidence exists.

## 7. This iteration's record

- **Repository before:** `bbb1c58`, 7 modified files uncommitted (Stop-gate repair), no WA-1 record.
- **Action:** reviewed and tested the repair; committed and pushed it; created the local snapshot;
  recorded ASA-003.3 and DLPM-002.
- **Repository after:** `f1e40a7` pushed to `origin/implementation/aces-node-baseline`; snapshot
  `E:\ACES-Backups\aces-os\snapshots\2026-11-27-014856` verified; WA-1 specified, not implemented.
- **Verification:** `node --test tests/*.test.ts tests/hooks/*.test.mjs` → **81 passed, 0 failed**.

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
**Status:** AUTHORIZED / W1–W4a IMPLEMENTED IN `observe` MODE / E3–E5 NOT IMPLEMENTED
**Authorized:** 2026-11-27 by the owner (two explicit instructions, this session)
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

### 0.1 Canon and implementation authorization (2026-11-27)

Owner instruction (verbatim):

> «Изменить Canon — не авторизовано- авторизовать»
> «Начать реализацию WA-1 — требуется отдельная авторизация → АВТОРИЗАЦИЯ РАЗРЕШЕНА.»

Recorded interpretation: the Canon change is authorized exactly as `SCHEMA.md` §26 plus the
ASA-003.3 §11 binding profile; implementation is authorized inside the existing components.
Neither authorizes a new subsystem, a second hook, a new registry, a write-guard service, or a
change to ASA §0–§10.

## 1. Mission

No harness, agent, bot, connector, or model can create or delete a durable ACES document without
a fresh ALLOW Decision from a single write authority that operates **outside** the agent; the
prohibition must remain effective for agents that have no hooks at all.

**Success condition (falsifiable):**

1. from a harness with no hooks, creating a file in the durable zone fails at the OS boundary;
2. the same operation in the staging zone succeeds;
3. every durable mutation has a matching AuthorizationEvent;
4. every deletion is recoverable for the retention window;
5. the existing suite (113 tests) remains green and the Stop owner remains exactly one.

## 2. Plan

| Stage | Objective | Exit evidence | Rollout mode |
|---|---|---|---|
| **W0** | Record + durability of the completed Stop-gate repair | commit `f1e40a7` on origin (0/0), snapshot bundle verified, this record | n/a |
| **W1** | Extend the **existing** policy body with WA-CREATE / WA-DELETE rules | rule table in the engine header + DLPM-002 table; no new file | observe |
| **W2** | Add `evaluateFileIntent({operation, resource, manifest})` to the existing engine; keep the journal at `rule + decision` | unit tests for every §11.5 operation; no path or command text journaled | observe |
| **W3** | Non-hook adapter: CLI mode of the **same** engine for harnesses without hooks | bypass tests (alias, `Start-Process`, `iex`, interpreter, MCP filesystem) | advisory |
| **W4** | Identity boundary (E3): agent identity with no write ACE on the durable zone; gate under a separate identity; MCP servers inherit the agent identity | probe from a no-hook harness: durable write denied, staging write allowed | enforced |
| **W5** | Store gate (E4): staging → gate apply; quarantine + retention for DELETE; reconciliation in the snapshot tool | V3/V4 evidence; unrecorded file detected as integrity violation | enforced |
| **W6** | Verification and ratification | V1–V5 executed, regression green, owner ratification recorded | enforced |

**Ordering constraint (non-negotiable):** `enforced` mode may not be enabled before **W4 and W5**
land. W2 ships in `observe` (journal-only, no blocking) so that the gate never blocks the
legitimate writes it has not yet learned to authorize. Enabling enforcement first would lock the
owner out of their own repository and force the control to be disabled — a control that cannot be
lived with is bypassed.

### 2.1 Staging contract (owner decision, 2026-11-28)

- **Staging zone:** `C:\ACES-Staging\` — outside the durable zone, so a Deny ACE on the repository
  and the Vault needs no Allow exception. Override: `ACES_STAGING_ROOT`.
- **Audit spool:** `C:\ACES-Staging\audit\spool\` — the uncommitted segment of the single journal.
  The engine appends here only when the canonical journal is not writable; rows carry a trailing
  `SPOOL` marker. The gate drains the spool into the canonical journal. Both unwritable → DENY.
- **No AcceptedState:** staging material is not a Decision outcome. It is never promoted
  automatically; transfer to the durable zone happens only through the established
  acceptance/verification contour (gate Decision + AuthorizationEvent).
- **Durability:** `aces-snapshot.ps1` archives the spool as `staging-spool.zip` and records it in
  the manifest and the Obsidian log line.
- **Consequence:** W4b can apply a blanket Deny (`W,D,WDAC,WO`) with no holes, and audit
  *availability* survives enforcement — F3 is closed by construction rather than by exception.
  The spool is agent-writable, so it is evidence of intent, not tamper-evident proof; tamper
  evidence requires E4 (the gate writes the canonical journal) or an OS audit policy.

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
| MC-5 | WA-CREATE / WA-DELETE added to the existing policy body | engine header rule table + §5.1; no new file | **DONE** |
| MC-6 | `evaluateFileIntent` in the existing engine, `observe` mode | 32 named tests; journal `rule + decision` | **DONE** |
| MC-7 | E3 identity boundary (no write ACE for agents) | OS probe from a no-hook harness | **NOT STARTED** |
| MC-8 | E4 gate: staging, quarantine, retention, reconcile | V3/V4 evidence | **NOT STARTED** |
| MC-9 | Non-hook adapter (CLI, same engine) | `--evaluate` tests incl. malformed input | **DONE (E2)** |
| MC-10 | Exactly one Stop owner; no second hook/ledger/registry | settings assertion test + tree check | **PASS** |
| MC-11 | Regression | `node --test tests/*.test.ts tests/hooks/*.test.mjs` → 115/115 | **PASS** |
| MC-12 | Owner ratification of `enforced` mode | explicit owner decision recorded | **NOT STARTED** |
| MC-13 | Staging zone outside the durable zone, no Allow exception | `C:\ACES-Staging`, contract §2.1 | **DONE (path created)** |
| MC-14 | Audit spool fallback with `SPOOL` marker; both unwritable → DENY | 2 named tests + engine `journal()` | **DONE** |
| MC-15 | Snapshot archives the spool | `staging-spool.zip` in the manifest after the fallback probe wrote 1 row | **DONE** |
| MC-16 | E3 deny ACE applied to repo and Vault | `icacls` output + agent-identity probe | **NOT STARTED** |

### 5.1 Implemented rules (W1 policy body)

| Rule | Condition | Decision |
|---|---|---|
| WA-UNKNOWN-1 | operation outside CREATE/UPDATE/DELETE/RENAME/MOVE/EXECUTE | DENY (both modes) |
| WA-MALFORMED-1 | missing/unresolvable path; composite without target | DENY |
| WA-MALFORMED-2 | invalid manifest JSON | DENY |
| WA-POLICY-1 | `ACES_WA_POLICY_FILE` set but unreadable | DENY |
| WA-AUDIT-1 | journal append failed for a policy decision | DENY at the hook boundary |
| WA-CREATE-1 | durable CREATE without `EXTENDS` | DENY (enforce) / would-deny (observe) |
| WA-CREATE-2 | `EXTENDS` path does not exist | DENY (enforce) / would-deny |
| WA-CREATE-3 | CREATE over an existing path → reclassified as UPDATE | ALLOW |
| WA-DELETE-1 | durable DELETE without `RESTORE` | DENY (enforce) / would-deny |
| WA-DELETE-2 | `RESTORE` is not an existing path, sha256, or git ref | DENY (enforce) / would-deny |
| WA-UPDATE-1 | UPDATE of a missing path / of an existing path | DENY / ALLOW |
| WA-COMPOSITE-1 | RENAME/MOVE = DELETE+CREATE; both must pass | DENY if either fails |
| WA-EXECUTE-1 | EXECUTE against a durable resource | advisory only (E3 constrains) |
| WA-STAGING-1 | path inside `.aces/staging/` | ALLOW |
| WA-UNPROTECTED-1 | path outside the durable zone | ALLOW |

Mode control: `ACES_WA_MODE=observe` (default) or `enforce`. Enforce applies to tool-level
writes only — `Write`, `Edit`, `MultiEdit`, `NotebookEdit`, and write-capable MCP tools. Shell
commands stay advisory in both modes, because static parsing is not a boundary.

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

## 8. W1–W3 implementation record (2026-11-27)

- **Repository before:** `f2dbda6` clean; WA-1 recorded as a direction only; no policy body.
- **Action:** extended the existing engine with the WA-* policy body, `evaluateFileIntent()`,
  tool and command adapters, the `--evaluate` CLI, and fail-closed audit; extended the existing
  suite; restored `SCHEMA.md` §26 under the new authorization and aligned ASA §11 to
  `EXTENDS` / `RESTORE`.
- **Repository after:** policy implemented in `observe` mode; `enforce` blocks tool-level writes
  only; E3/E4 absent.
- **Verification:** 113 tests passed, 0 failed; settings still register exactly one Stop owner.
- **Not claimed:** durable-zone protection. Until E3/E4 exist, a shell-capable agent can still
  create or delete a durable file. The boundary remains `ADVISORY`.

## 9. Boundary of the current implementation

`observe` journals a pending denial for every durable CREATE/DELETE request and blocks nothing.
`enforce` blocks only through tool calls that the hook sees. A harness that ignores hooks, a
direct shell, a script interpreter, and a differently mounted MCP server remain outside the
hook's reach; those are closed by E3 (identity) and E4 (store gate), which are not implemented.
No statement in this record may be read as "write to the durable zone is impossible".

## 10. W4a implementation record (2026-11-28)

- **Decision:** staging outside the repository at `C:\ACES-Staging\`; audit spool at
  `C:\ACES-Staging\audit\spool\`; repo and Vault stay under Deny with no Allow exception.
- **Action:** the engine now recognises the external staging root; the journal has a two-segment
  write path (canonical → spool, trailing `SPOOL` marker, DENY only if both fail); the snapshot tool
  archives the spool as `staging-spool.zip` and extends the manifest to recursive relative paths.
- **Not actioned:** no Windows account was created or modified; no ACL was changed. W4b remains
  owner-executed because it needs an interactive password.
- **Verification:** 115 tests passed, 0 failed (2 new: spool fallback, external staging root);
  PowerShell parser reports `PS_PARSE_OK`; `C:\ACES-Staging\audit\spool` exists. The spool was
  empty at the first W4a snapshot (`spool: empty`); a hook probe with an unwritable canonical
  journal then wrote the row `WA-UPDATE-1 allow SPOOL`, and the next snapshot archives it as
  `staging-spool.zip`. That row is **uncommitted** to the canonical journal until W5 drains it —
  it is evidence that the fallback works, not a replacement for the ledger.

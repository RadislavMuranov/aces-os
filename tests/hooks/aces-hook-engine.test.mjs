import assert from "node:assert/strict";
import test from "node:test";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath, pathToFileURL } from "node:url";
import { dirname, join } from "node:path";

const ENGINE = join(dirname(fileURLToPath(import.meta.url)), "..", "..", ".claude", "hooks", "aces-hook-engine.mjs");

/** Invoke the engine CLI exactly the way Claude Code would: JSON on stdin. */
function runHook(payload) {
  const res = spawnSync(process.execPath, [ENGINE], {
    input: JSON.stringify(payload),
    encoding: "utf-8",
    env: { ...process.env, ACES_HOOK_ENGINE_TEST: "1" },
  });
  assert.equal(res.status, 0, `engine exited non-zero: ${res.stderr}`);
  let out;
  try {
    out = JSON.parse(res.stdout || "{}");
  } catch {
    out = {};
  }
  return out;
}

function decisionOf(out) {
  if (out.hookSpecificOutput?.permissionDecision) return out.hookSpecificOutput.permissionDecision;
  if (out.decision === "block") return "deny";
  return "allow";
}

function bash(command) {
  return runHook({ event: "PreToolUse", hook_event_name: "PreToolUse", tool_name: "Bash", tool_input: { command } });
}

function ps(command) {
  return runHook({ event: "PreToolUse", hook_event_name: "PreToolUse", tool_name: "PowerShell", tool_input: { command } });
}

function iterationRecord(overrides = {}) {
  const fields = {
    ITERATION_ID: "REPAIR-STOP-GATE-001",
    OBJECTIVE: "Enforce the canonical ACES iteration closure record",
    REPOSITORY_BEFORE: "Observed working tree and exact baseline captured before mutation",
    ACTION: "Extended the existing ACES Hook Engine STOP-GATE",
    REPOSITORY_AFTER: "Existing engine and tests updated; duplicate adapter removed",
    REAL_WORLD_FAILURE: "OBSERVED — incomplete iteration was previously treated as closed",
    EVIDENCE: "Repository files, Stop hook input contract, and executed regression tests",
    MINIMALITY_LEVEL_TESTED: "L0 and L1 — reuse the existing registered Hook Engine",
    VERIFICATION: "PASS — structural closure checks and actual Stop payload tests executed",
    KNOWN_BUGS: "Existing STOP-GATE checked only marker presence",
    NEW_BUGS: "NONE — no new defect found in this test fixture",
    RECURRING_BUGS: "Architecture duplication recurrence recorded as B-134 / BUG-025",
    CHATGPT_BUG_AUDIT: "PASS — existing-component bypass and premature architecture checked",
    CONTRADICTIONS: "NONE — current engine ownership and hook registration agree",
    REMAINING_UNKNOWN: "Live Claude Code runtime invocation remains unverified",
    REFACTORING: "PASS — duplicate DSH adapter and standalone contract removed",
    DELETIONS_CONSIDERED: "PASS — all three duplicate artifacts removed after migration",
    FILTER_UPDATED: "PASS — B-134 / BUG-025 added to existing failure filter",
    REGRESSION_CHECK: "PASS — existing Hook Engine suite and Stop-GATE negative cases pass",
    ARCHITECTURE_ESCALATION: "BLOCKED — no new architecture introduced",
    FINAL_VERDICT: "PASS — local structural enforcement verified",
    NEXT_ACTION: "Verify live Stop event in the intended runtime before claiming runtime integration",
    ...overrides,
  };
  return [
    "ACES-ITERATION-RECORD v1",
    ...Object.entries(fields).map(([key, value]) => key + ": " + value),
  ].join("\n");
}

// ─── Z-2: git stash ─────────────────────────────────────────────────────────

test("Z-2: literal git stash is denied", () => {
  assert.equal(decisionOf(bash("git stash")), "deny");
  assert.match(bash("git stash").reason, /Z-2/);
});

test("Z-2: git stash pop is denied (stash family)", () => {
  assert.equal(decisionOf(bash("git stash pop")), "deny");
});

test("Z-2: git -c alias.s=stash; git s is denied via inline alias", () => {
  const out = bash("git -c alias.s=stash s");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-2/);
});

test("Z-2: bash alias to git, then alias invocation of stash is denied", () => {
  const out = bash("alias g=git; g stash");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-2/);
});

test("Z-2: PowerShell Set-Alias to git, then alias invocation of stash is denied", () => {
  const out = ps("Set-Alias g git; g stash");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-2/);
});

test("Z-2: PowerShell Start-Process git -ArgumentList stash is denied", () => {
  const out = ps("Start-Process git -ArgumentList stash");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-2/);
});

test("Z-2: Start-Process with reordered parameters (-FilePath after -ArgumentList) is denied", () => {
  const out = ps("Start-Process -ArgumentList stash -FilePath git");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-2/);
});

// ─── Z-3: git reset --hard ──────────────────────────────────────────────────

test("Z-3: git reset --hard is denied", () => {
  const out = bash("git reset --hard HEAD");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-3/);
});

test("Z-3: PowerShell Start-Process git.exe -ArgumentList 'reset --hard HEAD' is denied", () => {
  const out = ps("Start-Process -FilePath git.exe -ArgumentList 'reset --hard HEAD'");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-3/);
});

test("Z-3: git reset (mixed) is allowed", () => {
  assert.equal(decisionOf(bash("git reset HEAD~1")), "allow");
});

// ─── Z-8: .env ───────────────────────────────────────────────────────────────

test("Z-8: cat .env is denied", () => {
  const out = bash("cat .env");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-8/);
});

test("Z-8: Get-Content .env is denied", () => {
  const out = ps("Get-Content .env");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-8/);
});

test("Z-8: Read tool on .env is denied", () => {
  const out = runHook({ event: "PreToolUse", tool_name: "Read", tool_input: { file_path: ".env" } });
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-8/);
});

test("Z-8: cat .env.example is allowed", () => {
  assert.equal(decisionOf(bash("cat .env.example")), "allow");
});

// ─── Research deletion (BUG-001/020/B-129) ──────────────────────────────────

test("research deletion rm -rf knowledge/research requires ask", () => {
  const out = bash("rm -rf knowledge/research");
  assert.equal(decisionOf(out), "ask");
  assert.match(out.reason, /RESEARCH-DELETION/);
});

// ─── Governance creation (BUG-014) ──────────────────────────────────────────

test("Write to new spec/governance file requires ask", () => {
  const out = runHook({ event: "PreToolUse", tool_name: "Write", tool_input: { file_path: "spec/governance/NEW-RULE.md", content: "x" } });
  assert.equal(decisionOf(out), "ask");
  assert.match(out.reason, /GOVERNANCE-CREATION/);
});

test("Write to non-governance path is allowed", () => {
  const out = runHook({ event: "PreToolUse", tool_name: "Write", tool_input: { file_path: "src/new-file.ts", content: "x" } });
  assert.equal(decisionOf(out), "allow");
});

// ─── KMA-11 audit protection ────────────────────────────────────────────────

test("Edit of KMA-11 audit record is denied", () => {
  const out = runHook({ event: "PreToolUse", tool_name: "Edit", tool_input: { file_path: "docs/audit/KMA-11-CHATGPT-BUG-SYSTEM.md" } });
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /KMA11-PROTECT/);
});

// ─── Unknown git subcommands / dynamic execution → ASK ──────────────────────

test("unknown git subcommand requires ask (may be an alias)", () => {
  const out = bash("git frobnicate");
  assert.equal(decisionOf(out), "ask");
  assert.match(out.reason, /GIT-UNKNOWN-SUBCOMMAND/);
});

test("git config alias definition requires ask", () => {
  const out = bash("git config alias.s stash");
  assert.equal(decisionOf(out), "ask");
});

test("PowerShell Invoke-Expression of git stash requires ask", () => {
  const out = ps("Invoke-Expression 'git stash'");
  assert.equal(decisionOf(out), "ask");
});

test("PowerShell call operator with variable requires ask", () => {
  const out = ps("& $cmd");
  assert.equal(decisionOf(out), "ask");
});

test("unresolved bash alias with protected git args requires ask", () => {
  const out = bash("g reset --hard HEAD");
  // 'g' is not resolvable in-process → conservative ASK, never silent ALLOW
  assert.equal(decisionOf(out), "ask");
});

// ─── Safe false positives stay allowed ──────────────────────────────────────

test("git status is allowed", () => {
  assert.equal(decisionOf(bash("git status")), "allow");
});

test("git diff-tree is allowed (recognized subcommand)", () => {
  assert.equal(decisionOf(bash("git diff-tree -r HEAD")), "allow");
});

test("git merge-base is allowed (recognized subcommand)", () => {
  assert.equal(decisionOf(bash("git merge-base main feature")), "allow");
});

test("Start-Process git -ArgumentList status is allowed", () => {
  assert.equal(decisionOf(ps("Start-Process git -ArgumentList status")), "allow");
});

test("cat README.md is allowed", () => {
  assert.equal(decisionOf(bash("cat README.md")), "allow");
});

// ─── Stop gate ───────────────────────────────────────────────────────────────

test("Stop without last_assistant_message is blocked even if another payload field contains a marker", () => {
  const out = runHook({
    event: "Stop",
    hook_event_name: "Stop",
    transcript_path: "x.jsonl",
    iteration_record: "ACES-ITERATION-RECORD v1",
  });
  assert.equal(out.decision, "block");
  assert.match(out.reason, /STOP-GATE/);
  assert.match(out.reason, /last_assistant_message/);
});

test("Stop accepts a complete canonical iteration record from last_assistant_message", () => {
  const out = runHook({
    event: "Stop",
    hook_event_name: "Stop",
    last_assistant_message: iterationRecord(),
  });
  assert.equal(decisionOf(out), "allow");
});

test("Stop blocks an iteration record with missing required fields", () => {
  const message = iterationRecord().replace(/^EVIDENCE:.*\n/m, "");
  const out = runHook({ event: "Stop", last_assistant_message: message });
  assert.equal(out.decision, "block");
  assert.match(out.reason, /missing fields: EVIDENCE/);
});

test("Stop blocks duplicate iteration record fields", () => {
  const out = runHook({
    event: "Stop",
    last_assistant_message: iterationRecord() + "\nFINAL_VERDICT: FAIL",
  });
  assert.equal(out.decision, "block");
  assert.match(out.reason, /duplicate fields: FINAL_VERDICT/);
});

test("Stop does not accept PASS when mandatory verification gates are not PASS", () => {
  const out = runHook({
    event: "Stop",
    last_assistant_message: iterationRecord({ REGRESSION_CHECK: "UNKNOWN — not run" }),
  });
  assert.equal(out.decision, "block");
  assert.match(out.reason, /FINAL_VERDICT PASS requires PASS for: REGRESSION_CHECK/);
});

test("Stop blocks unsupported final verdicts", () => {
  const out = runHook({
    event: "Stop",
    last_assistant_message: iterationRecord({ FINAL_VERDICT: "DONE" }),
  });
  assert.equal(out.decision, "block");
  assert.match(out.reason, /FINAL_VERDICT must be/);
});

test("Stop rejects a verdict not defined by the canonical self-audit specification", () => {
  const out = runHook({
    event: "Stop",
    last_assistant_message: iterationRecord({ FINAL_VERDICT: "CONDITIONAL — not a canonical disposition" }),
  });
  assert.equal(out.decision, "block");
  assert.match(out.reason, /FINAL_VERDICT must be/);
});

test("Stop rejects PASS when repository before-state is N/A", () => {
  const out = runHook({
    event: "Stop",
    last_assistant_message: iterationRecord({ REPOSITORY_BEFORE: "N/A" }),
  });
  assert.equal(out.decision, "block");
  assert.match(out.reason, /requires established repository before\/after state/);
});

test("Stop accepts a structurally complete BLOCKED disposition without promoting it to PASS", () => {
  const out = runHook({
    event: "Stop",
    last_assistant_message: iterationRecord({
      FINAL_VERDICT: "BLOCKED — required runtime evidence unavailable",
      VERIFICATION: "BLOCKED — live runtime evidence unavailable",
      CHATGPT_BUG_AUDIT: "BLOCKED — runtime audit cannot be completed",
      REFACTORING: "PASS — no further local reduction identified",
      FILTER_UPDATED: "PASS — applicable defect already recorded",
      REGRESSION_CHECK: "BLOCKED — live runtime check unavailable",
    }),
  });
  assert.equal(decisionOf(out), "allow");
});

test("Stop re-entry identifies the unresolved closure condition", () => {
  const out = runHook({
    event: "Stop",
    stop_hook_active: true,
    last_assistant_message: "Incomplete response",
  });
  assert.equal(out.decision, "block");
  assert.match(out.reason, /already continued this turn/);
});

test("Stop rejects an invalid REAL_WORLD_FAILURE classification", () => {
  const out = runHook({
    event: "Stop",
    last_assistant_message: iterationRecord({ REAL_WORLD_FAILURE: "MAYBE — not classified" }),
  });
  assert.equal(out.decision, "block");
  assert.match(out.reason, /REAL_WORLD_FAILURE must begin with/);
});

test("project settings register exactly one Stop owner: the existing ACES Hook Engine", () => {
  const root = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
  const settings = JSON.parse(readFileSync(join(root, ".claude", "settings.json"), "utf-8"));
  const stopHooks = settings.hooks?.Stop ?? [];
  const commands = stopHooks.flatMap((group) => group.hooks ?? []).map((hook) => hook.command);
  assert.deepEqual(commands, ["node .claude/hooks/aces-hook-engine.mjs"]);
});

// ─── Journal privacy ────────────────────────────────────────────────────────

test("journal records decisions without command text", () => {
  bash("cat .env");
  const journal = readFileSync(join(dirname(fileURLToPath(import.meta.url)), "..", "..", ".claude", "hooks", "journal.tsv"), "utf-8");
  const lines = journal.trim().split("\n");
  const lastLine = lines[lines.length - 1];
  assert.match(lastLine, /\tZ-8\tdeny$/, "last journal entry must be the Z-8 deny decision");
  for (const line of lines) {
    assert.doesNotMatch(line, /cat \.env/, "journal must not contain raw command text");
  }
});

// ─── Canonical Z-registry (recovered from original engine 2026-11-25) ───────

test("Z-1: git -c core.hooksPath=… override is denied", () => {
  const out = bash("git -c core.hooksPath=/tmp/h commit -m x");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-1/);
});

test("Z-1: git commit --no-verify is denied", () => {
  const out = bash("git commit --no-verify -- src/file.ts");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-1/);
});

test("Z-2: literal git stash is denied", () => {
  assert.equal(decisionOf(bash("git stash")), "deny");
  assert.match(bash("git stash").reason, /Z-2/);
});

test("Z-2: git stash pop is denied (stash family)", () => {
  assert.equal(decisionOf(bash("git stash pop")), "deny");
});

test("Z-3: git reset --hard is denied", () => {
  const out = bash("git reset --hard HEAD");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-3/);
});

test("Z-4: git rebase is denied", () => {
  const out = bash("git rebase main");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-4/);
});

test("Z-5: git push --force is denied", () => {
  const out = bash("git push --force origin main");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-5/);
});

test("Z-5: git push with '+' refspec is denied", () => {
  const out = bash("git push origin +main");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-5/);
});

test("Z-5: plain git push is allowed", () => {
  assert.equal(decisionOf(bash("git push origin main")), "allow");
});

test("Z-6: broad git add -A is denied", () => {
  const out = bash("git add -A");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-6/);
});

test("Z-6: explicit git add path is allowed", () => {
  assert.equal(decisionOf(bash("git add src/file.ts")), "allow");
});

test("Z-7: git commit -a is denied", () => {
  const out = bash("git commit -a -- src/file.ts");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-7/);
});

test("Z-7: git commit without explicit paths after -- is denied", () => {
  const out = bash("git commit -m msg");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-7/);
});

test("Z-7: git commit with explicit paths after -- is allowed", () => {
  assert.equal(decisionOf(bash("git commit -m msg -- src/file.ts")), "allow");
});

test("Z-8: cat .env is denied", () => {
  const out = bash("cat .env");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-8/);
});

test("Z-8: Get-Content .env is denied", () => {
  const out = ps("Get-Content .env");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-8/);
});

test("Z-8: Read tool on .env is denied", () => {
  const out = runHook({ event: "PreToolUse", tool_name: "Read", tool_input: { file_path: ".env" } });
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /Z-8/);
});

test("Z-8: cat .env.example is allowed", () => {
  assert.equal(decisionOf(bash("cat .env.example")), "allow");
});

// ─── DLPM-1: deletion of protected roots (DLPM-001) ─────────────────────────

test("DLPM-1: rm -rf .git is denied", () => {
  const out = bash("rm -rf .git");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /DLPM-1/);
});

test("DLPM-1: rm -rf .claude is denied", () => {
  const out = bash("rm -rf .claude");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /DLPM-1/);
});

test("DLPM-1: rm -rf aces-os (repo root) is denied", () => {
  const out = bash("rm -rf aces-os");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /DLPM-1/);
});

test("DLPM-1: rm -rf Obsidian Vault is denied", () => {
  const out = bash('rm -rf "/c/Users/Радислав Муранов/Documents/Obsidian Vault"');
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /DLPM-1/);
});

test("DLPM-1: PowerShell Remove-Item -Recurse on .git is denied", () => {
  const out = ps("Remove-Item -Recurse -Force .git");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /DLPM-1/);
});

test("DLPM-1: rm of an ordinary file is allowed", () => {
  assert.equal(decisionOf(bash("rm notes.txt")), "allow");
});

// ─── DLPM-4..7: data-loss prevention (DLPM-001) ─────────────────────────────

test("DLPM-4: git clean -fd is denied", () => {
  const out = bash("git clean -fd");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /DLPM-4/);
});

test("DLPM-4: git clean -n (dry run) is allowed", () => {
  assert.equal(decisionOf(bash("git clean -n")), "allow");
});

test("DLPM-5: git checkout -- . is denied", () => {
  const out = bash("git checkout -- .");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /DLPM-5/);
});

test("DLPM-5: git restore . is denied", () => {
  const out = bash("git restore .");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /DLPM-5/);
});

test("DLPM-5: git restore --staged is allowed", () => {
  assert.equal(decisionOf(bash("git restore --staged file.txt")), "allow");
});

test("DLPM-6: git branch -D requires ask", () => {
  const out = bash("git branch -D feature-x");
  assert.equal(decisionOf(out), "ask");
  assert.match(out.reason, /DLPM-6/);
});

test("DLPM-7: git filter-branch is denied", () => {
  const out = bash("git filter-branch --env-filter 'x' HEAD");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /DLPM-7/);
});

test("DLPM-7: git reflog expire is denied", () => {
  const out = bash("git reflog expire --expire=now --all");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /DLPM-7/);
});

test("DLPM-7: git reflog (read) is allowed", () => {
  assert.equal(decisionOf(bash("git reflog")), "allow");
});

// ─── Malformed input fails safe ─────────────────────────────────────────────

test("malformed JSON payload does not crash the engine", () => {
  const res = spawnSync(process.execPath, [ENGINE], { input: "not json", encoding: "utf-8", env: { ...process.env, ACES_HOOK_ENGINE_TEST: "1" } });
  assert.equal(res.status, 0);
});

// ─── WA-1: Single Write Authority policy (ASA-003.3 §11, DLPM-002) ───────────
// The hook is the advisory class E1. `observe` is the default mode: a durable
// CREATE/DELETE without a manifest is journaled as would-deny, never blocked.

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const ENGINE_API = await import(pathToFileURL(ENGINE).href);
const intent = (request) => ENGINE_API.evaluateFileIntent(request);

function runHookEnv(payload, env) {
  const res = spawnSync(process.execPath, [ENGINE], {
    input: JSON.stringify(payload),
    encoding: "utf-8",
    env: { ...process.env, ACES_HOOK_ENGINE_TEST: "1", ...env },
  });
  assert.equal(res.status, 0, `engine exited non-zero: ${res.stderr}`);
  return JSON.parse(res.stdout || "{}");
}

function runCli(request, env) {
  const res = spawnSync(process.execPath, [ENGINE, "--evaluate"], {
    input: JSON.stringify(request),
    encoding: "utf-8",
    env: { ...process.env, ACES_HOOK_ENGINE_TEST: "1", ...env },
  });
  assert.equal(res.status, 0, `cli exited non-zero: ${res.stderr}`);
  return JSON.parse(res.stdout || "{}");
}

const RESTORE_BUG_024 = "docs/audit/2026-11-25-DATA-LOSS-INCIDENT-BUG-024.md";
const EXTENDS_DLPM = "docs/protection/DATA-LOSS-PROTECTION-METHOD.md";

test("WA: default mode is observe and a durable CREATE without manifest is advisory", () => {
  const d = intent({ operation: "CREATE", resource_id: "docs/new-record.md" });
  assert.equal(d.decision, "advisory");
  assert.equal(d.rule, "WA-CREATE-1");
  assert.equal(d.mode, "observe");
});

test("WA: enforce mode denies a durable CREATE without manifest", () => {
  const d = intent({ operation: "CREATE", resource_id: "docs/new-record.md", mode: "enforce" });
  assert.equal(d.decision, "deny");
  assert.equal(d.rule, "WA-CREATE-1");
});

test("WA: CREATE with EXTENDS naming an existing component is accepted", () => {
  const d = intent({ operation: "CREATE", resource_id: "docs/new-record.md", mode: "enforce", manifest: { EXTENDS: EXTENDS_DLPM } });
  assert.equal(d.decision, "allow");
  assert.equal(d.rule, "WA-CREATE-3");
  assert.match(d.reason, /path/);
});

test("WA: legacy extends_component field remains accepted", () => {
  const d = intent({ operation: "CREATE", resource_id: "docs/new-record.md", mode: "enforce", manifest: { extends_component: EXTENDS_DLPM } });
  assert.equal(d.decision, "allow");
});

test("WA: CREATE with a non-existent EXTENDS path is denied", () => {
  const d = intent({ operation: "CREATE", resource_id: "docs/new-record.md", mode: "enforce", manifest: { EXTENDS: "docs/no-such-component.md" } });
  assert.equal(d.decision, "deny");
  assert.equal(d.rule, "WA-CREATE-2");
});

test("WA: a bare component name defers EXTENDS verification to the gate", () => {
  const d = intent({ operation: "CREATE", resource_id: "docs/new-record.md", mode: "enforce", manifest: { EXTENDS: "ACES Hook Engine" } });
  assert.equal(d.decision, "allow");
  assert.match(d.reason, /deferred/);
});

test("WA: CREATE over an existing path is reclassified as UPDATE, not creation", () => {
  const d = intent({ operation: "CREATE", resource_id: "README.md", mode: "enforce" });
  assert.equal(d.decision, "allow");
  assert.equal(d.rule, "WA-CREATE-3");
  assert.match(d.reason, /in-place update/);
});

test("WA: durable DELETE without RESTORE is denied in enforce mode", () => {
  const d = intent({ operation: "DELETE", resource_id: RESTORE_BUG_024, mode: "enforce" });
  assert.equal(d.decision, "deny");
  assert.equal(d.rule, "WA-DELETE-1");
});

test("WA: DELETE with RESTORE pointing at an existing copy is accepted", () => {
  const d = intent({ operation: "DELETE", resource_id: "docs/scratch.md", mode: "enforce", manifest: { RESTORE: RESTORE_BUG_024 } });
  assert.equal(d.decision, "allow");
  assert.equal(d.rule, "WA-DELETE-3");
});

test("WA: DELETE with RESTORE expressed as a sha256 content hash is accepted", () => {
  const hash = "sha256:" + "a".repeat(64);
  const d = intent({ operation: "DELETE", resource_id: "docs/scratch.md", mode: "enforce", manifest: { RESTORE: hash } });
  assert.equal(d.decision, "allow");
});

test("WA: DELETE with an unprovable RESTORE is denied", () => {
  const d = intent({ operation: "DELETE", resource_id: "docs/scratch.md", mode: "enforce", manifest: { RESTORE: "trust me" } });
  assert.equal(d.decision, "deny");
  assert.equal(d.rule, "WA-DELETE-2");
});

test("WA: UPDATE of a missing resource is denied", () => {
  const d = intent({ operation: "UPDATE", resource_id: "docs/definitely-missing-xyz.md", mode: "enforce" });
  assert.equal(d.decision, "deny");
  assert.equal(d.rule, "WA-UPDATE-1");
});

test("WA: UPDATE of an existing resource is allowed and journaled", () => {
  const d = intent({ operation: "UPDATE", resource_id: "README.md", mode: "enforce" });
  assert.equal(d.decision, "allow");
  assert.equal(d.rule, "WA-UPDATE-1");
});

test("WA: unknown operation is denied in both modes", () => {
  assert.equal(intent({ operation: "PURGE", resource_id: "docs/x.md" }).decision, "deny");
  assert.equal(intent({ operation: "PURGE", resource_id: "docs/x.md", mode: "enforce" }).rule, "WA-UNKNOWN-1");
});

test("WA: malformed manifest is denied", () => {
  const d = intent({ operation: "CREATE", resource_id: "docs/x.md", manifest: { __error: "bad json" }, mode: "enforce" });
  assert.equal(d.decision, "deny");
  assert.equal(d.rule, "WA-MALFORMED-2");
});

test("WA: unavailable policy body is denied (fail-closed)", () => {
  const viaEnv = runCli({ operation: "UPDATE", resource_id: "README.md", mode: "enforce" }, { ACES_WA_POLICY_FILE: join(ROOT, "no-such-policy.json") });
  assert.equal(viaEnv.decision, "deny");
  assert.equal(viaEnv.rule, "WA-POLICY-1");
});

test("WA: RENAME without target_id is malformed", () => {
  const d = intent({ operation: "RENAME", resource_id: "docs/a.md", mode: "enforce" });
  assert.equal(d.decision, "deny");
  assert.equal(d.rule, "WA-MALFORMED-1");
});

test("WA: RENAME is a DELETE+CREATE composite and requires both decisions", () => {
  const manifest = { EXTENDS: EXTENDS_DLPM, RESTORE: RESTORE_BUG_024 };
  const d = intent({ operation: "MOVE", resource_id: "docs/a.md", target_id: "docs/b.md", mode: "enforce", manifest });
  assert.equal(d.decision, "allow");
  assert.equal(d.rule, "WA-COMPOSITE-1");
});

test("WA: traversal out of a safe subpath still resolves into the durable zone", () => {
  const d = intent({ operation: "CREATE", resource_id: "docs/../.git/NEWFILE", mode: "enforce" });
  assert.equal(d.decision, "deny");
});

test("WA: staging zone is always writable", () => {
  const d = intent({ operation: "CREATE", resource_id: ".aces/staging/draft.md", mode: "enforce" });
  assert.equal(d.decision, "allow");
  assert.equal(d.rule, "WA-STAGING-1");
});

test("WA: resource outside the durable zone is not protected", () => {
  const d = intent({ operation: "DELETE", resource_id: "/tmp/notes.txt", mode: "enforce" });
  assert.equal(d.decision, "allow");
  assert.equal(d.rule, "WA-UNPROTECTED-1");
});

test("WA: EXECUTE is never authorized or denied by static inspection", () => {
  const d = intent({ operation: "EXECUTE", resource_id: "docs/x.md", mode: "enforce" });
  assert.equal(d.decision, "advisory");
  assert.equal(d.rule, "WA-EXECUTE-1");
});

test("WA hook: observe mode lets a durable Write through and journals would-deny", () => {
  const out = runHook({ event: "PreToolUse", tool_name: "Write", tool_input: { file_path: "docs/agent-made.md", content: "x" } });
  assert.equal(decisionOf(out), "allow");
  const journal = readFileSync(join(ROOT, ".claude", "hooks", "journal.tsv"), "utf-8").trim().split("\n");
  assert.match(journal[journal.length - 1], /\tWA-CREATE-1\twould-deny$/);
});

test("WA hook: enforce mode denies a durable Write without manifest", () => {
  const out = runHookEnv({ event: "PreToolUse", tool_name: "Write", tool_input: { file_path: "docs/agent-made.md", content: "x" } }, { ACES_WA_MODE: "enforce" });
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /WA-CREATE-1/);
});

test("WA hook: enforce mode allows an in-place update of an existing file", () => {
  const out = runHookEnv({ event: "PreToolUse", tool_name: "Write", tool_input: { file_path: "README.md", content: "x" } }, { ACES_WA_MODE: "enforce" });
  assert.equal(decisionOf(out), "allow");
});

test("WA hook: write-capable MCP tool is covered by the same policy", () => {
  const out = runHookEnv({ event: "PreToolUse", tool_name: "mcp__filesystem__write_file", tool_input: { path: "docs/mcp-made.md", content: "x" } }, { ACES_WA_MODE: "enforce" });
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /WA-CREATE-1/);
});

test("WA hook: shell deletion of a durable file is advisory only, never a false deny", () => {
  const out = runHook({ event: "PreToolUse", tool_name: "Bash", tool_input: { command: "rm docs/agent-made.md" } });
  assert.equal(decisionOf(out), "allow");
});

test("WA hook: PowerShell durable creation is advisory only", () => {
  const out = runHook({ event: "PreToolUse", tool_name: "PowerShell", tool_input: { command: 'New-Item -ItemType File -Path "docs/ps-made.md"' } });
  assert.equal(decisionOf(out), "allow");
});

test("WA: DLPM-1 still wins over WA-1 (protected root deletion)", () => {
  const out = bash("rm -rf .git");
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /DLPM-1/);
});

test("WA: failed audit append denies a policy decision (fail-closed)", () => {
  const out = runHookEnv(
    { event: "PreToolUse", tool_name: "Write", tool_input: { file_path: "docs/agent-made.md", content: "x" } },
    { ACES_WA_MODE: "enforce", ACES_HOOK_JOURNAL: join(ROOT, "README.md", "journal.tsv") },
  );
  assert.equal(decisionOf(out), "deny");
  assert.match(out.reason, /WA-AUDIT-1/);
});

test("WA CLI adapter: same engine, same policy, decision printed as JSON", () => {
  const denied = runCli({ operation: "CREATE", resource_id: "docs/cli-made.md" }, { ACES_WA_MODE: "enforce" });
  assert.equal(denied.decision, "deny");
  assert.equal(denied.rule, "WA-CREATE-1");

  const allowed = runCli({ operation: "CREATE", resource_id: "docs/cli-made.md", manifest: { EXTENDS: EXTENDS_DLPM } }, { ACES_WA_MODE: "enforce" });
  assert.equal(allowed.decision, "allow");
});

test("WA CLI adapter: malformed request JSON is denied, not crashed", () => {
  const res = spawnSync(process.execPath, [ENGINE, "--evaluate"], { input: "not json", encoding: "utf-8", env: { ...process.env, ACES_HOOK_ENGINE_TEST: "1" } });
  assert.equal(res.status, 0);
  const out = JSON.parse(res.stdout);
  assert.equal(out.decision, "deny");
  assert.equal(out.rule, "WA-MALFORMED-2");
});

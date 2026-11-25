import assert from "node:assert/strict";
import test from "node:test";
import { spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { fileURLToPath } from "node:url";
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

test("Stop without ACES iteration record is blocked", () => {
  const out = runHook({ event: "Stop", hook_event_name: "Stop", transcript_path: "x.jsonl" });
  assert.equal(out.decision, "block");
  assert.match(out.reason, /STOP-GATE/);
});

test("Stop with ACES iteration record is allowed", () => {
  const out = runHook({ event: "Stop", hook_event_name: "Stop", iteration_record: "ACES-ITERATION-RECORD-2026-11-25" });
  assert.equal(decisionOf(out), "allow");
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

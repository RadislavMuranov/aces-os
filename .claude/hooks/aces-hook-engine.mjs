#!/usr/bin/env node
/**
 * ACES hook engine — policy-to-enforcement runtime (rebuild 2026-11-25).
 *
 * Rebuilt from surviving evidence after the loss of the original local
 * worktree (see Linear RAD-80 / GitHub issue #10):
 *   - Z-2: `git stash` (direct, aliased, Start-Process) → DENY
 *   - Z-3: `git reset --hard` (direct, aliased, Start-Process) → DENY
 *   - Z-8: reading `.env` via Bash/PowerShell/Read bridge → DENY (.env.example → ALLOW)
 *   - research/experiment/negative-result deletion → ASK (BUG-001/020/B-129)
 *   - new file creation under spec/governance/ → ASK (BUG-014 minimality)
 *   - KMA-11 audit record protected from Write/Edit
 *   - unknown git subcommands / unresolved aliases / dynamic PS execution → ASK
 *   - Stop without an ACES iteration record → BLOCK
 *   - journal «РУБИЛЬНИК»: timestamp + rule + decision only (no command text)
 *
 * Z-1, Z-4…Z-7: definitions lost with the original worktree; registered as
 * UNKNOWN in the rule registry and not enforced until re-defined by the owner.
 */

import { appendFileSync } from "node:fs";
import { mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), "..", "..");
const JOURNAL = join(ROOT, ".claude", "hooks", "journal.tsv");

const KMA11_AUDIT_PATH = "docs/audit/KMA-11-CHATGPT-BUG-SYSTEM.md";

/** Synchronous alias resolution is intentionally conservative:
 * anything unresolvable resolves to `null` and callers treat it as ASK. */
function extractBracedValue(s, start) {
  let depth = 0;
  for (let i = start; i < s.length; i++) {
    if (s[i] === "{") depth++;
    else if (s[i] === "}") {
      if (depth === 0) return { value: s.slice(start, i), next: i + 1 };
      depth--;
    }
  }
  return null;
}

/** Split a shell-like command line into tokens (quote/escape aware). */
function tokenize(line) {
  const tokens = [];
  let cur = "";
  let quoted = null;
  for (let i = 0; i < line.length; i++) {
    const ch = line[i];
    if (quoted) {
      if (ch === quoted && line[i - 1] !== "\\") quoted = null;
      else cur += ch;
    } else if (ch === '"' || ch === "'") {
      quoted = ch;
    } else if (ch === " " || ch === "\t") {
      if (cur) { tokens.push(cur); cur = ""; }
    } else if (ch === ";" || ch === "|" || ch === "&" || ch === "\n") {
      if (cur) { tokens.push(cur); cur = ""; }
      tokens.push(";");
    } else cur += ch;
  }
  if (cur) tokens.push(cur);
  return tokens;
}

const GIT_SUBCOMMANDS = new Set([
  "add", "am", "annotate", "apply", "archive", "bisect", "blame", "branch",
  "checkout", "cherry", "cherry-pick", "clean", "clone", "commit", "config",
  "describe", "diff", "difftool", "fetch", "format-patch", "gc", "grep",
  "init", "log", "merge", "mv", "pull", "push", "range-diff", "rebase",
  "reflog", "remote", "reset", "restore", "rm", "shortlog", "show", "stash",
  "status", "submodule", "switch", "tag", "worktree", "cat-file", "diff-tree",
  "merge-base", "rev-parse", "show-branch", "clean", "restore", "reflog",
]);

/**
 * Git controls — two families.
 *
 * Z-1…Z-8: the user-approved registry, RECOVERED 2026-11-25 verbatim from the
 * original engine (found alive at C:\ACES\aces-os, `aces-hook-engine.mjs`):
 *   Z-1 core.hooksPath change / --no-verify bypass → DENY
 *   Z-2 git stash (all operations) → DENY
 *   Z-3 git reset --hard → DENY
 *   Z-4 git rebase → DENY
 *   Z-5 force push (--force/-f/--force-with-lease/'+' refspec) → DENY
 *   Z-6 broad git add (-A/--all/-u/./) → DENY
 *   Z-7 git commit -a / commit without explicit paths after '--' → DENY
 *   Z-8 reading .env / .env.* (except .env.example) → DENY
 *
 * DLPM-*: data-loss prevention additions (DLPM-001 method, 2026-11-25),
 * closing the loss vector of the worktree incident.
 * Returns decision or null (no match).
 */
export function evaluateGitArgs(args) {
  const sub = args[0];
  if (!sub) return null;
  // Z-1: core.hooksPath override (inline -c / --config-env)
  for (let i = 0; i < args.length; i++) {
    const x = args[i], v = args[i + 1];
    if ((x === "-c" || x === "--config-env") && v && /^core\.hookspath=/i.test(v)) {
      return { rule: "Z-1", decision: "deny", reason: "Changing core.hooksPath is prohibited." };
    }
    if (typeof x === "string" && x.startsWith("-c") && /core\.hookspath=/i.test(x)) {
      return { rule: "Z-1", decision: "deny", reason: "Overriding core.hooksPath is prohibited." };
    }
  }
  if (sub === "stash") return { rule: "Z-2", decision: "deny", reason: "All git stash operations are prohibited." };
  if (sub === "reset" && args.slice(1).includes("--hard")) return { rule: "Z-3", decision: "deny", reason: "git reset --hard is prohibited." };
  if (sub === "rebase") return { rule: "Z-4", decision: "deny", reason: "git rebase is prohibited." };
  if (sub === "push") {
    const rest = args.slice(1);
    if (rest.some(x => ["--force", "-f", "--force-with-lease"].includes(x)) || rest.some(x => x.startsWith("--force-with-lease=")) || rest.some(x => x.startsWith("+"))) {
      return { rule: "Z-5", decision: "deny", reason: "Force push and '+' refspecs are prohibited." };
    }
  }
  if (sub === "add" && args.slice(1).some(x => ["-A", "--all", "-u", "--update", ".", "./"].includes(x))) {
    return { rule: "Z-6", decision: "deny", reason: "Broad git add operations are prohibited." };
  }
  if (sub === "commit") {
    const rest = args.slice(1);
    if (rest.includes("--no-verify") || rest.includes("-n")) {
      return { rule: "Z-1", decision: "deny", reason: "Bypassing commit hooks is prohibited." };
    }
    if (rest.some(x => x === "-a" || x === "--all" || /^-a[^-]/.test(x))) {
      return { rule: "Z-7", decision: "deny", reason: "git commit -a is prohibited." };
    }
    const k = rest.indexOf("--");
    if (k < 0 || !rest.slice(k + 1).some(x => String(x).trim())) {
      return { rule: "Z-7", decision: "deny", reason: "git commit requires explicit paths after '--'." };
    }
  }
  if (sub === "config") {
    const rest = args.slice(1);
    const k = rest.indexOf("--");
    const read = rest.includes("--get") || rest.includes("--list") || rest.includes("-l") || rest.includes("--get-all");
    if (k >= 0 && !read && (rest.includes("--unset") || rest.includes("--unset-all") || rest.length > k + 1)) {
      return { rule: "Z-1", decision: "deny", reason: "Changing core.hooksPath is prohibited; reading it is allowed." };
    }
    if (rest.includes("--edit")) {
      return { rule: "Z-1", decision: "ask", reason: "git config --edit may change core.hooksPath; confirm first." };
    }
  }
  // ─── DLPM-*: data-loss prevention (DLPM-001) ─────────────────────────────
  // DLPM-4: git clean -f* destroys untracked work → DENY
  if (sub === "clean") {
    const rest = args.slice(1).join(" ");
    if (/(^|\s)-{1,2}[a-zA-Z]*f/.test(rest)) {
      return { rule: "DLPM-4", decision: "deny", reason: "git clean -f destroys untracked work (DLPM-001)" };
    }
  }
  // DLPM-5: whole-tree discard of uncommitted changes → DENY
  if (sub === "checkout" || sub === "restore") {
    const rest = args.slice(1).join(" ");
    const wholeTree = /(^|\s)(--\s+)?\.(\/|$)/.test(rest) && !/--staged/.test(rest);
    if (wholeTree) {
      return { rule: "DLPM-5", decision: "deny", reason: `git ${sub} . discards uncommitted work tree-wide (DLPM-001)` };
    }
  }
  // DLPM-6: branch deletion destroys committed work → ASK
  if (sub === "branch") {
    const rest = args.slice(1).join(" ");
    if (/(^|\s)-{1,2}[dD]\b/.test(rest)) {
      return { rule: "DLPM-6", decision: "ask", reason: "branch deletion destroys committed work; owner confirmation required (DLPM-001)" };
    }
  }
  // DLPM-7: history rewrite / reflog expiry destroy recovery paths → DENY
  if (sub === "filter-branch") {
    return { rule: "DLPM-7", decision: "deny", reason: "git filter-branch rewrites history (DLPM-001)" };
  }
  if (sub === "reflog") {
    const rest = args.slice(1).join(" ");
    if (/expire/.test(rest)) {
      return { rule: "DLPM-7", decision: "deny", reason: "git reflog expire destroys recovery paths (DLPM-001)" };
    }
  }
  if (!GIT_SUBCOMMANDS.has(sub)) {
    return { decision: "ask", rule: "GIT-UNKNOWN-SUBCOMMAND", reason: `unknown git subcommand "${sub}" may be an alias; cannot resolve safely` };
  }
  return null;
}

/**
 * DLPM-1 (DLPM-001 method, 2026-11-25): deletion of protected roots → DENY.
 * Protected: the repository root itself, .git, .claude, and the Obsidian Vault.
 * This is the control whose absence allowed the aces-os worktree incident.
 */
const REPO_DIR_NAME = "aces-os";

function isProtectedDeletionTarget(target) {
  const t = String(target).replace(/\\/g, "/").replace(/["']/g, "").replace(/\/+$/, "");
  if (t === "" || t === "." || t === "./" || t === REPO_DIR_NAME || t === "./" + REPO_DIR_NAME) return true;
  if (/(^|\/)Obsidian Vault(\/|$)/.test(t)) return true;
  if (/(^|\/)\.git(\/|$)/.test(t)) return true;
  if (/(^|\/)\.claude(\/|$)/.test(t)) return true;
  return false;
}

function evaluateDeletionProtection(command) {
  // Bash rm/rmdir targeting protected paths
  const rmMatch = command.match(/(?:^|\s|;|&&|\|\|)(rm|rmdir)\s+([^;&|\n]+)/);
  if (rmMatch) {
    const targets = tokenize(rmMatch[2]);
    for (const tok of targets) {
      if (isProtectedDeletionTarget(tok)) {
        return { decision: "deny", rule: "DLPM-1", reason: `deletion of protected path "${tok}" is prohibited (DLPM-001 data-loss protection)` };
      }
    }
  }
  // PowerShell Remove-Item targeting protected paths
  if (/\b(remove-item|ri)\b/i.test(command) && /(^|\s)-{1,2}recurse/i.test(command)) {
    const pm = command.match(/\b(?:Remove-Item|ri)\b\s+(?:-Path\s+|-Recurse\s+|-Force\s+)*([^\s;|]+)/i);
    if (pm && isProtectedDeletionTarget(pm[1])) {
      return { decision: "deny", rule: "DLPM-1", reason: `deletion of protected path "${pm[1]}" is prohibited (DLPM-001 data-loss protection)` };
    }
  }
  return null;
}

/** Evaluate a Bash-like token stream for git invocations with alias expansion. */
function evaluateBashCommand(command) {
  // Cross-segment bash alias expansion: `alias g=git; g stash`
  const aliasDef = command.match(/(?:^|;\s*|\|\|\s*|&&\s*)alias\s+([A-Za-z0-9_.-]+)=(?:"([^"]*)"|'([^']*)'|([^\s;]+))/);
  if (aliasDef) {
    const name = aliasDef[1];
    const value = (aliasDef[2] ?? aliasDef[3] ?? aliasDef[4] ?? "").trim();
    const useRe = new RegExp(`(?:^|\\s|;|\\|\\||&&)${name}\\s+([^;\\n]+)`);
    const use = command.match(useRe);
    if (use) {
      const decision = evaluateBashCommand(`${value} ${use[1]}`);
      if (decision) return decision;
    }
  }

  const segments = command.split(/;|\|\||&&|\n/g);
  for (const segment of segments) {
    let tokens = tokenize(segment.trim());
    if (tokens.length === 0) continue;
    let idx = 0;
    let head = tokens[idx];

    // Strip leading sudo/env
    while (head === "sudo" || head === "env") { idx++; head = tokens[idx]; }
    if (!head) continue;

    // git (possibly with inline -c alias config)
    if (head === "git" || head === "git.exe") {
      const decision = evaluateGitWithInlineConfig(tokens.slice(idx + 1));
      if (decision) return decision;
      continue;
    }

    // Unresolvable first token whose args match a protected git signature → ASK
    // (the alias was not defined in this command; we cannot expand it safely)
    if (tokens.length > 1) {
      const d = evaluateGitArgs(tokens.slice(1));
      if (d && d.decision === "deny") {
        return { decision: "ask", rule: "UNRESOL-ALIAS", reason: `unresolved command "${head}" invokes a protected git signature; cannot expand safely` };
      }
    }
  }
  return null;
}

/** Evaluate git invocation with optional inline `-c alias.x=…` config. */
function evaluateGitWithInlineConfig(args) {
  let alias = null;
  const consumed = [];
  let i = 0;
  while (i < args.length) {
    const a = args[i];
    if (a === "-c" && i + 1 < args.length) {
      const cfg = args[i + 1];
      // Z-1: core.hooksPath override via inline config
      if (/^core\.hookspath=/i.test(cfg)) {
        return { rule: "Z-1", decision: "deny", reason: "Changing core.hooksPath is prohibited." };
      }
      const am = cfg.match(/^alias\.([A-Za-z0-9_.-]+)=(.*)$/);
      if (am) alias = { name: am[1], value: am[2] };
      i += 2;
      continue;
    }
    if (a === "config" && args[i + 1] && /^alias\./.test(args[i + 1])) {
      // `git config alias.s stash` — define-then-use is not synchronously resolvable
      return { decision: "ask", rule: "GIT-ALIAS-CONFIG", reason: "git config alias definition cannot be resolved synchronously" };
    }
    consumed.push(a);
    i++;
  }
  if (consumed.length === 0) return null;
  if (consumed[0] === "config") return null; // reading config is fine
  if (alias && consumed[0] === alias.name) {
    const expanded = [alias.value, ...consumed.slice(1)];
    const sub = expanded[0];
    if (sub === "stash") return { decision: "deny", rule: "Z-2", reason: "git stash (via inline alias) is protected by Z-2" };
    if (sub === "reset" && /--hard/.test(expanded.slice(1).join(" "))) {
      return { decision: "deny", rule: "Z-3", reason: "git reset --hard (via inline alias) is protected by Z-3" };
    }
  }
  return evaluateGitArgs(consumed);
}

/** Evaluate a PowerShell command string. */
export function evaluatePowerShell(command) {
  // PowerShell aliases mapping a name to git, then invoking it
  const aliasMatch = command.match(/(?:Set-Alias|New-Alias)\s+(?:-Name\s+)?(\S+)\s+(?:-Value\s+)?["']?git["']?/i);
  if (aliasMatch) {
    const name = aliasMatch[1];
    const invocation = new RegExp(`(?:^|;\\s*|\\|\\|\\s*|&&\\s*)${name}\\s+([^;\\n]+)`, "i");
    const im = command.match(invocation);
    if (im) {
      const args = tokenize(im[1]);
      const d = evaluateGitArgs(args);
      if (d) return d;
    }
  }

  // Invoke-Expression / iex of anything git-related or dynamic → ASK
  if (/\b(invoke-expression|iex)\b/i.test(command)) {
    return { decision: "ask", rule: "PS-DYNAMIC-EXECUTION", reason: "dynamic PowerShell execution cannot be statically resolved" };
  }

  // Call operator with variable → ASK
  if (/&\s*\$[A-Za-z_]/.test(command)) {
    return { decision: "ask", rule: "PS-CALL-OPERATOR", reason: "variable call operator cannot be statically resolved" };
  }

  // Start-Process git … -ArgumentList … (any parameter order)
  if (/\b(start-process|start)\b/i.test(command) && /\bgit(\.exe)?\b/i.test(command)) {
    const sp = command.match(/\b(?:Start-Process|start)\b(.*)$/i);
    if (sp) {
      const rawArgs = sp[1].replace(/['"]/g, " ");
      const args = [];
      let gitSeen = false;
      let inArgList = false;
      for (const tok of tokenize(rawArgs)) {
        if (tok === ";") { inArgList = false; continue; }
        if (/^-ArgumentList$/i.test(tok)) { inArgList = true; continue; }
        if (/^-FilePath$/i.test(tok)) { continue; }
        if (/^git(\.exe)?$/i.test(tok)) { gitSeen = true; continue; }
        if (inArgList || gitSeen) args.push(tok);
      }
      if (gitSeen || inArgList) {
        if (args.length === 0) {
          return { decision: "ask", rule: "PS-START-PROCESS", reason: "Start-Process git with unparseable arguments" };
        }
        const d = evaluateGitArgs(args);
        if (d) return d;
      }
    }
  }

  // Get-Content .env
  if (/\bget-content\b/i.test(command) && /(^|\s|")\.env(\s|"|$)/i.test(command) && !/\.env\./i.test(command)) {
    return { decision: "deny", rule: "Z-8", reason: "reading .env is protected by Z-8" };
  }
  return null;
}

/** Evaluate a Bash command for Z-8 (.env read), Z-1 (deletion) and research deletion. */
function evaluateBashPathRules(command) {
  const z1 = evaluateDeletionProtection(command);
  if (z1) return z1;
  // .env read via cat/type/less/more/head/tail, but not .env.example / .env.* etc.
  const envMatch = command.match(/\b(?:cat|type|less|more|head|tail)\s+([^;&|\n]+)/i);
  if (envMatch) {
    const files = envMatch[1].split(/\s+/);
    for (const f of files) {
      const clean = f.replace(/^["']|["']$/g, "");
      if (clean === ".env" || clean === "./.env") {
        return { decision: "deny", rule: "Z-8", reason: "reading .env is protected by Z-8" };
      }
    }
  }
  if (/^\s*rm\s+(-[a-zA-Z]+\s+)*(-[a-zA-Z]*[rf][a-zA-Z]*\s+)+(knowledge\/research|knowledge)(\/|\s|$)/.test(command) ||
      /^rm\s+[^;|]*\bknowledge\/research\b/.test(command)) {
    return { decision: "ask", rule: "RESEARCH-DELETION", reason: "deleting research/experiment/negative results requires confirmation (BUG-001/020/B-129)" };
  }
  return null;
}

function evaluateBash(command) {
  if (/^(powershell|pwsh)\b/i.test(command.trim())) {
    return evaluatePowerShell(command);
  }
  const gitDecision = evaluateBashCommand(command);
  if (gitDecision) return gitDecision;
  const pathDecision = evaluateBashPathRules(command);
  if (pathDecision) return pathDecision;
  const psDecision = evaluatePowerShell(command);
  if (psDecision) return psDecision;
  return null;
}

function evaluateRead(toolInput) {
  const p = (toolInput.file_path || toolInput.path || "").replaceAll("\\", "/");
  if (/(^|\/)\.env$/.test(p)) return { decision: "deny", rule: "Z-8", reason: "reading .env is protected by Z-8" };
  return null;
}

function evaluateWrite(toolInput, toolName) {
  const p = (toolInput.file_path || toolInput.path || "").replaceAll("\\", "/");
  if (/^spec\/governance\//.test(p) && !toolInput._exists) {
    return { decision: "ask", rule: "GOVERNANCE-CREATION", reason: "creating new governance sources requires observed failure and minimality justification (BUG-014)" };
  }
  if (p === KMA11_AUDIT_PATH) {
    return { decision: "deny", rule: "KMA11-PROTECT", reason: "KMA-11 audit record is protected from modification" };
  }
  return null;
}

function evaluateStop(payload) {
  const text = JSON.stringify(payload);
  const hasIterationRecord = /ACES[-_ ]?ITERATION[-_ ]?RECORD/i.test(text) || /iteration_record/i.test(text);
  if (!hasIterationRecord) {
    return { decision: "block", rule: "STOP-GATE", reason: "Stop denied: no ACES iteration record in transcript" };
  }
  return null;
}

function journal(rule, decision) {
  try {
    mkdirSync(dirname(JOURNAL), { recursive: true });
  } catch {}
  const ts = new Date().toISOString();
  appendFileSync(JOURNAL, `${ts}\t${rule}\t${decision}\n`);
}

export function evaluatePreToolUse(payload) {
  const toolName = payload.tool_name || "";
  const input = payload.tool_input || {};
  try {
    if (toolName === "PowerShell") {
      const psDecision = evaluatePowerShell(String(input.command || ""));
      if (psDecision) return psDecision;
      const z1 = evaluateDeletionProtection(String(input.command || ""));
      if (z1) return z1;
      const bashDecision = evaluateBashCommand(String(input.command || ""));
      if (bashDecision) return bashDecision;
      return null;
    }
    if (toolName === "Bash") {
      return evaluateBash(String(input.command || ""));
    }
    if (toolName === "Read") return evaluateRead(input);
    if (toolName === "Write" || toolName === "Edit") return evaluateWrite(input, toolName);
  } catch (err) {
    process.stderr.write(`[aces-hook-engine] ${err && err.stack ? err.stack.split("\n")[0] : "unknown"}\n`);
    // fail-safe: ambiguous input → ask
    return { decision: "ask", rule: "ENGINE-ERROR", reason: "hook engine failed to evaluate input safely" };
  }
  return null;
}

export function evaluateHook(payload) {
  if (payload && (payload.event === "Stop" || payload.stop_hook_active || payload.event === "stop")) {
    const d = evaluateStop(payload);
    if (d) return d;
    return null;
  }
  return evaluatePreToolUse(payload);
}

function main() {
  let raw = "";
  process.stdin.setEncoding("utf-8");
  process.stdin.on("data", (c) => (raw += c));
  process.stdin.on("end", () => {
    let payload;
    try {
      payload = JSON.parse(raw || "{}");
    } catch {
      payload = {};
    }
    const event = payload.event || (payload.hook_event_name || "");
    const toolName = payload.tool_name;
    let result = null;
    if (event === "PreToolUse" || toolName) {
      result = evaluatePreToolUse(payload);
    } else if (event === "Stop" || payload.stop_hook_active) {
      result = evaluateStop(payload);
    } else if (event === "Stop") {
      result = evaluateStop(payload);
    }
    const rule = result ? result.rule : "NO_MATCH";
    const decision = result ? result.decision : "allow";
    journal(rule, decision);
    if (!result) {
      process.stdout.write("{}");
      return;
    }
    if (result.decision === "deny" || result.decision === "block") {
      const out = { decision: "block", reason: `${result.rule}: ${result.reason}` };
      if (event === "PreToolUse" || toolName) {
        out.hookSpecificOutput = { hookEventName: "PreToolUse", permissionDecision: "deny" };
      }
      process.stdout.write(JSON.stringify(out));
    } else if (result.decision === "ask") {
      const out = { hookSpecificOutput: { hookEventName: "PreToolUse", permissionDecision: "ask" }, reason: `${result.rule}: ${result.reason}` };
      process.stdout.write(JSON.stringify(out));
    } else {
      process.stdout.write("{}");
    }
  });
}

if (process.argv[1] && process.argv[1].endsWith("aces-hook-engine.mjs")) {
  main();
}

// Policy gate: the ONLY source of decisions is .claude/hooks/aces-hook-engine.mjs,
// invoked exactly as Claude Code invokes it: `node <engine> pretool` (JSON on stdin).
// No policy rule is copied into this file. Fail-closed on every uncertainty.
// Design reference: aces-integration/04-design.md sections 3, 6, 8.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";

export const HOOK_TOOL_BY_KIND = Object.freeze({
  read: "Read",
  list: "Read",
  write: "Write",
  edit: "Edit",
  git_status: "PowerShell",
  exec: null, // resolved from op.shell
});

// The git_status operation is a fixed, non-parameterised read-only probe.
// It is still gated through the engine, but its command is not caller-controlled.
export const GIT_STATUS_COMMAND = "git status --porcelain=v1 -b";

const DECISIONS = new Set(["allow", "deny", "ask"]);

export function sha256Hex(input) {
  return crypto.createHash("sha256").update(input).digest("hex");
}

export function journalPathFor(repoRoot) {
  return path.join(repoRoot, ".claude", "hooks", "journal.tsv");
}

// Journal rows are `timestamp \t rule_id \t decision`. Line numbering is 1-based
// and includes the header row, matching the design's provenance contract.
export function journalRows(file) {
  if (!file || !fs.existsSync(file)) return [];
  const text = fs.readFileSync(file, "utf8");
  const lines = text.split("\n");
  if (lines.length > 0 && lines[lines.length - 1] === "") lines.pop();
  return lines.map((raw, index) => {
    const row = raw.replace(/\r$/, "");
    const parts = row.split("\t");
    return {
      line: index + 1,
      row,
      timestamp: parts[0] ?? null,
      rule_id: parts[1] ?? null,
      decision: parts[2] ?? null,
      row_sha256: sha256Hex(row),
    };
  });
}

export function buildHookCall(op, { repoRoot }) {
  const kind = String(op?.kind ?? "");
  if (!(kind in HOOK_TOOL_BY_KIND)) {
    const err = new Error(`operation kind '${kind}' does not map to a hook tool`);
    err.code = "ACES-UNMAPPED-OP";
    throw err;
  }
  if (kind === "exec") {
    const toolName = op.shell === "bash" ? "Bash" : "PowerShell";
    return { tool_name: toolName, tool_input: { command: String(op.target ?? "") } };
  }
  if (kind === "git_status") {
    return { tool_name: "PowerShell", tool_input: { command: GIT_STATUS_COMMAND } };
  }
  // Absolute path is mandatory: a bare relative "AGENTS.md" slips past the
  // engine's PROTECTED suffix check (design probe P2, risk R2).
  const abs = path.resolve(repoRoot, String(op.target ?? ""));
  return { tool_name: HOOK_TOOL_BY_KIND[kind], tool_input: { file_path: abs } };
}

function denyResult(code, message, extra = {}) {
  return {
    decision: "deny",
    rule_id: code,
    reason: message,
    journal: null,
    error: { code, message },
    latency_ms: 0,
    engine: null,
    ...extra,
  };
}

function timeoutResult(message) {
  return denyResult("POLICY-TIMEOUT", message);
}

function runEngine({ enginePath, timeoutMs, payload }) {
  const started = process.hrtime.bigint();
  const res = spawnSync(process.execPath, [enginePath, "pretool"], {
    input: JSON.stringify(payload),
    encoding: "utf8",
    timeout: timeoutMs,
    shell: false,
    windowsHide: true,
    maxBuffer: 1 << 20,
  });
  const latencyMs = Number(process.hrtime.bigint() - started) / 1e6;
  return { res, latencyMs: Math.round(latencyMs) };
}

function runStopEngine({ enginePath, timeoutMs, payload }) {
  const started = process.hrtime.bigint();
  const res = spawnSync(process.execPath, [enginePath, "stop"], {
    input: JSON.stringify(payload),
    encoding: "utf8",
    timeout: timeoutMs,
    shell: false,
    windowsHide: true,
    maxBuffer: 1 << 20,
  });
  const latencyMs = Number(process.hrtime.bigint() - started) / 1e6;
  return { res, latencyMs: Math.round(latencyMs) };
}

/**
 * Create the gate. All engine invocations are serialised inside one process so
 * that the journal delta protocol (n1 - n0 >= 1) cannot race with itself.
 */
export function createPolicyGate({
  repoRoot,
  enginePath,
  journalPath,
  timeoutMs = 10000,
  execEnabled = false,
  log = () => {},
}) {
  const journal = journalPath ?? journalPathFor(repoRoot);
  let chain = Promise.resolve();

  function serialize(fn) {
    const run = chain.then(fn, fn);
    chain = run.then(
      () => undefined,
      () => undefined,
    );
    return run;
  }

  function engineMeta() {
    if (!fs.existsSync(enginePath)) {
      return { exists: false, path: enginePath, bytes: null, sha256: null };
    }
    const buf = fs.readFileSync(enginePath);
    return {
      exists: true,
      path: enginePath,
      bytes: buf.length,
      sha256: sha256Hex(buf).toUpperCase(),
    };
  }

  function checkSync(op, { taskId, opId, cwd = repoRoot, sessionId } = {}) {
    if (op?.kind === "exec" && !execEnabled) {
      return denyResult(
        "EXEC_DISABLED",
        "exec operations are disabled; start the server with --enable-exec to allow them",
      );
    }

    let hookCall;
    try {
      hookCall = buildHookCall(op, { repoRoot });
    } catch (err) {
      return denyResult(err.code ?? "ACES-UNMAPPED-OP", err.message);
    }

    const before = journalRows(journal).length;
    const payload = {
      cwd,
      session_id: sessionId ?? `aces-autoclaw:${taskId}`,
      hook_event_name: "PreToolUse",
      tool_use_id: opId,
      tool_name: hookCall.tool_name,
      tool_input: hookCall.tool_input,
    };

    const { res, latencyMs } = runEngine({ enginePath, timeoutMs, payload });
    const rows = journalRows(journal);
    const after = rows.length;
    const delta = after - before;
    const last = after > 0 ? rows[after - 1] : null;
    const engineInfo = {
      exit_code: res.status,
      signal: res.signal ?? null,
      stdout: (res.stdout ?? "").slice(0, 4096),
      stderr: (res.stderr ?? "").slice(0, 4096),
      journal_delta: delta,
    };

    if (res.error) {
      if (res.error.code === "ETIMEDOUT" || res.signal === "SIGTERM") {
        return timeoutResult(`hook engine exceeded ${timeoutMs} ms; operation not executed`);
      }
      return denyResult(
        "ENGINE-SPAWN-FAILED",
        `cannot start hook engine: ${res.error.code ?? "unknown"} ${res.error.message ?? ""}`.trim(),
        { engine: engineInfo, latency_ms: latencyMs, hook_tool: hookCall.tool_name, hook_input: hookCall.tool_input },
      );
    }
    if (res.status === 2) {
      const stderr = String(res.stderr ?? "").replace("ACES hook failed closed: ", "").trim();
      return denyResult("ENGINE-FAILED", stderr || "hook engine failed closed (exit 2)", {
        engine: engineInfo,
        latency_ms: latencyMs,
        hook_tool: hookCall.tool_name,
        hook_input: hookCall.tool_input,
      });
    }
    if (res.status !== 0) {
      return denyResult("ENGINE-FAILED", `hook engine exited with status ${res.status}`, {
        engine: engineInfo,
        latency_ms: latencyMs,
        hook_tool: hookCall.tool_name,
        hook_input: hookCall.tool_input,
      });
    }

    // Empty stdout is ambiguous: allow, or the engine never ran (probe E).
    // Only the journal delta disambiguates it.
    if (delta <= 0) {
      return denyResult(
        "ENGINE-NO-JOURNAL",
        "hook engine left no journal row; no decision was obtained (fail-closed)",
        { engine: engineInfo, latency_ms: latencyMs, hook_tool: hookCall.tool_name, hook_input: hookCall.tool_input },
      );
    }

    let stdoutDecision = null;
    let stdoutReason = null;
    const trimmed = String(res.stdout ?? "").trim();
    if (trimmed !== "") {
      let parsed;
      try {
        parsed = JSON.parse(trimmed);
      } catch {
        return denyResult("ENGINE-BAD-OUTPUT", "hook engine produced non-JSON stdout", {
          engine: engineInfo,
          latency_ms: latencyMs,
          hook_tool: hookCall.tool_name,
          hook_input: hookCall.tool_input,
        });
      }
      const d = parsed?.hookSpecificOutput?.permissionDecision;
      if (!DECISIONS.has(d)) {
        return denyResult("ENGINE-BAD-OUTPUT", `hook engine returned unknown permissionDecision: ${String(d)}`, {
          engine: engineInfo,
          latency_ms: latencyMs,
          hook_tool: hookCall.tool_name,
          hook_input: hookCall.tool_input,
        });
      }
      stdoutDecision = d;
      stdoutReason = parsed?.hookSpecificOutput?.permissionDecisionReason ?? null;
    }

    if (!last || !DECISIONS.has(last.decision)) {
      return denyResult("ENGINE-BAD-OUTPUT", "last journal row is unreadable; decision not confirmed", {
        engine: engineInfo,
        latency_ms: latencyMs,
        hook_tool: hookCall.tool_name,
        hook_input: hookCall.tool_input,
      });
    }

    const expectedStdout = stdoutDecision ?? "allow";
    if (last.decision !== expectedStdout) {
      return denyResult(
        "ENGINE-BAD-OUTPUT",
        `journal says '${last.decision}' but stdout says '${expectedStdout}'; refusing to guess`,
        {
          engine: engineInfo,
          latency_ms: latencyMs,
          hook_tool: hookCall.tool_name,
          hook_input: hookCall.tool_input,
          journal: { path: journal, line: last.line, row_sha256: last.row_sha256 },
        },
      );
    }

    const result = {
      decision: last.decision,
      rule_id: last.rule_id ?? "UNKNOWN",
      reason: last.decision === "allow" ? null : (stdoutReason ?? null),
      journal: { path: journal, line: last.line, row_sha256: last.row_sha256 },
      error: null,
      latency_ms: latencyMs,
      hook_tool: hookCall.tool_name,
      hook_input: hookCall.tool_input,
      engine: engineInfo,
    };
    log(`pretool ${op?.kind} ${String(op?.target).slice(0, 80)} -> ${result.decision}/${result.rule_id} (line ${last.line}, ${latencyMs}ms)`);
    return result;
  }

  function check(op, meta) {
    return serialize(() => checkSync(op, meta));
  }

  function stopSync({ taskId, message, cwd = repoRoot }) {
    const before = journalRows(journal).length;
    const payload = {
      cwd,
      session_id: `aces-autoclaw:${taskId}`,
      hook_event_name: "Stop",
      last_assistant_message: String(message ?? ""),
    };
    const { res, latencyMs } = runStopEngine({ enginePath, timeoutMs, payload });
    const rows = journalRows(journal);
    const after = rows.length;
    const last = after > 0 ? rows[after - 1] : null;
    const engineInfo = {
      exit_code: res.status,
      signal: res.signal ?? null,
      stdout: (res.stdout ?? "").slice(0, 8192),
      stderr: (res.stderr ?? "").slice(0, 4096),
      journal_delta: after - before,
    };

    if (res.error?.code === "ETIMEDOUT" || res.signal === "SIGTERM") {
      return {
        decision: "block",
        rule_id: "POLICY-TIMEOUT",
        reason: `hook engine exceeded ${timeoutMs} ms on stop gate`,
        journal: null,
        error: { code: "POLICY-TIMEOUT", message: "stop gate timed out" },
        latency_ms: latencyMs,
        engine: engineInfo,
      };
    }
    if (res.error) {
      return {
        decision: "block",
        rule_id: "ENGINE-SPAWN-FAILED",
        reason: `cannot start hook engine: ${res.error.code ?? "unknown"}`,
        journal: null,
        error: { code: "ENGINE-SPAWN-FAILED", message: String(res.error.message ?? res.error) },
        latency_ms: latencyMs,
        engine: engineInfo,
      };
    }
    if (res.status !== 0 || after - before <= 0) {
      return {
        decision: "block",
        rule_id: res.status === 2 ? "ENGINE-FAILED" : "ENGINE-NO-JOURNAL",
        reason:
          res.status === 2
            ? String(res.stderr ?? "").replace("ACES hook failed closed: ", "").trim()
            : "stop gate left no journal row; result not confirmed",
        journal: null,
        error: { code: "ENGINE-FAILED", message: "stop gate did not confirm" },
        latency_ms: latencyMs,
        engine: engineInfo,
      };
    }

    let blocked = false;
    let blockReason = null;
    const trimmed = String(res.stdout ?? "").trim();
    if (trimmed !== "") {
      let parsed;
      try {
        parsed = JSON.parse(trimmed);
      } catch {
        return {
          decision: "block",
          rule_id: "ENGINE-BAD-OUTPUT",
          reason: "stop gate produced non-JSON stdout",
          journal: last ? { path: journal, line: last.line, row_sha256: last.row_sha256 } : null,
          error: { code: "ENGINE-BAD-OUTPUT", message: "non-JSON stdout" },
          latency_ms: latencyMs,
          engine: engineInfo,
        };
      }
      if (parsed?.decision === "block") {
        blocked = true;
        blockReason = parsed?.reason ?? null;
      }
    }
    if (!last) {
      return {
        decision: "block",
        rule_id: "ENGINE-NO-JOURNAL",
        reason: "stop gate journal row is missing",
        journal: null,
        error: { code: "ENGINE-NO-JOURNAL", message: "missing row" },
        latency_ms: latencyMs,
        engine: engineInfo,
      };
    }
    if ((last.decision === "block") !== blocked) {
      return {
        decision: "block",
        rule_id: "ENGINE-BAD-OUTPUT",
        reason: `stop journal says '${last.decision}' but stdout says '${blocked ? "block" : "allow"}'`,
        journal: { path: journal, line: last.line, row_sha256: last.row_sha256 },
        error: { code: "ENGINE-BAD-OUTPUT", message: "journal/stdout mismatch" },
        latency_ms: latencyMs,
        engine: engineInfo,
      };
    }
    return {
      decision: blocked ? "block" : "allow",
      rule_id: last.rule_id ?? "STOP-GATE",
      reason: blocked ? blockReason : null,
      journal: { path: journal, line: last.line, row_sha256: last.row_sha256 },
      error: null,
      latency_ms: latencyMs,
      engine: engineInfo,
    };
  }

  function stop(meta) {
    return serialize(() => stopSync(meta));
  }

  return {
    repoRoot,
    enginePath,
    journalPath: journal,
    timeoutMs,
    execEnabled,
    check,
    stop,
    engineMeta,
    journalRows: () => journalRows(journal),
  };
}

/** Synthetic round-trip in a scratch cwd, so the repository journal stays untouched. */
export function probeEngine({ enginePath, cwd, timeoutMs = 10000 }) {
  const jp = path.join(cwd, ".claude", "hooks", "journal.tsv");
  const before = journalRows(jp).length;
  const payload = {
    cwd,
    session_id: "aces-autoclaw:health-probe",
    hook_event_name: "PreToolUse",
    tool_use_id: "op_heal",
    tool_name: "Read",
    tool_input: { file_path: path.join(cwd, "README.md") },
  };
  const { res, latencyMs } = runEngine({ enginePath, timeoutMs, payload });
  const rows = journalRows(jp);
  const delta = rows.length - before;
  const last = rows.length > 0 ? rows[rows.length - 1] : null;
  return {
    ok: !res.error && res.status === 0 && delta >= 1 && last?.decision === "allow",
    delta,
    latency_ms: latencyMs,
    rule_id: last?.rule_id ?? null,
    decision: last?.decision ?? null,
    journal: { path: jp, line: last?.line ?? null },
    exit_code: res.status,
    error: res.error ? `${res.error.code ?? "error"}: ${res.error.message ?? ""}` : null,
    stderr: String(res.stderr ?? "").slice(0, 2000),
  };
}

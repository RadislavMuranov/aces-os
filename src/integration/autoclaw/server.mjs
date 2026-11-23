#!/usr/bin/env node
// ACES OS <-> AutoClaw MCP bridge.
// Transport: JSON-RPC 2.0 over stdio, both framings accepted
// (Content-Length headers and newline-delimited JSON); replies mirror the request.
// Runtime: Node ESM, node builtins only. No npm packages, no SDK.
// Policy: every decision comes from .claude/hooks/aces-hook-engine.mjs run as a
// subprocess (`pretool` / `stop`). This server contains no policy rules.
// Design reference: aces-integration/04-design.md.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";

import { createPolicyGate, probeEngine, journalPathFor, journalRows as readJournalRows } from "./policy-gate.mjs";
import * as envelope from "./envelope.mjs";
import * as fsops from "./fs-ops.mjs";
import { verifyEvents, journalTail as readJournalTail } from "./provenance.mjs";

const SERVER_NAME = "aces-bridge";
const SERVER_VERSION = "0.1.0";
const PROTOCOL_VERSION = "2025-06-18";
const SUPPORTED_PROTOCOLS = ["2025-06-18", "2025-03-26", "2024-11-05"];
const MODULE_DIR = path.dirname(fileURLToPath(import.meta.url));
const MAX_OPS = 32;
const DEFAULT_TIMEOUT_MS = 10000;

const HELP = `ACES bridge (stdio MCP)

  node server.mjs [--repo-root <dir>] [--engine <file>] [--state-dir <dir>]
                  [--actor <id>] [--harness <name>] [--timeout-ms <n>]
                  [--enable-exec] [--verbose]
  node server.mjs --health [--deep]     # one-shot health JSON, no stdio server

Defaults are derived from this file's location (src/integration/autoclaw -> repo root).
exec operations stay disabled unless --enable-exec is passed.
`;

function parseArgv(argv) {
  const repoRoot = path.resolve(MODULE_DIR, "..", "..", "..");
  const out = {
    repoRoot,
    engine: null,
    stateDir: null,
    actor: "autoclaw-desktop",
    harness: "autoclaw",
    timeoutMs: DEFAULT_TIMEOUT_MS,
    enableExec: false,
    verbose: false,
    health: false,
    deep: false,
    help: false,
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = () => {
      i += 1;
      if (i >= argv.length) throw new Error(`missing value for ${arg}`);
      return argv[i];
    };
    switch (arg) {
      case "--repo-root":
        out.repoRoot = path.resolve(next());
        break;
      case "--engine":
        out.engine = path.resolve(next());
        break;
      case "--state-dir":
        out.stateDir = path.resolve(next());
        break;
      case "--actor":
        out.actor = next();
        break;
      case "--harness":
        out.harness = next();
        break;
      case "--timeout-ms": {
        const value = Number(next());
        if (!Number.isInteger(value) || value < 1000 || value > 30000) {
          throw new Error("--timeout-ms must be an integer in 1000..30000");
        }
        out.timeoutMs = value;
        break;
      }
      case "--enable-exec":
        out.enableExec = true;
        break;
      case "--verbose":
        out.verbose = true;
        break;
      case "--health":
        out.health = true;
        break;
      case "--deep":
        out.deep = true;
        break;
      case "--help":
      case "-h":
        out.help = true;
        break;
      default:
        throw new Error(`unknown argument: ${arg}`);
    }
  }
  out.engine = out.engine ?? path.join(out.repoRoot, ".claude", "hooks", "aces-hook-engine.mjs");
  out.stateDir = out.stateDir ?? envelope.stateDir(out.repoRoot);
  out.journalPath = journalPathFor(out.repoRoot);
  return out;
}

let cfg;
try {
  cfg = parseArgv(process.argv.slice(2));
} catch (err) {
  process.stderr.write(`${SERVER_NAME}: ${err.message}\n\n${HELP}`);
  process.exit(2);
}

const repoRoot = path.resolve(cfg.repoRoot);
const gate = createPolicyGate({
  repoRoot,
  enginePath: cfg.engine,
  journalPath: cfg.journalPath,
  timeoutMs: cfg.timeoutMs,
  execEnabled: cfg.enableExec,
  log: (line) => {
    if (cfg.verbose) process.stderr.write(`[aces-bridge] ${line}\n`);
  },
});

function logErr(err) {
  process.stderr.write(`[aces-bridge] ${err?.stack ?? String(err)}\n`);
}

// ---------------------------------------------------------------- tool helpers

function jsonResult(obj, isError = false) {
  const compact = JSON.stringify(obj);
  const text = Buffer.byteLength(compact) < 32768 ? JSON.stringify(obj, null, 2) : compact;
  return isError
    ? { content: [{ type: "text", text }], isError: true }
    : { content: [{ type: "text", text }] };
}

function toolError(code, message, extra = {}) {
  return jsonResult({ error: { code, message, ...extra } }, true);
}

function policyView(result) {
  return {
    decision: result.decision,
    rule_id: result.rule_id,
    reason: result.reason ?? null,
    journal: result.journal ?? null,
    error: result.error ?? null,
  };
}

function policyRecord(op, result) {
  return {
    op_id: op.op_id,
    kind: op.kind,
    target: op.target,
    hook_tool: result.hook_tool ?? null,
    hook_input: result.hook_input ?? null,
    decision: result.decision,
    rule_id: result.rule_id,
    reason: result.reason ?? null,
    journal: result.journal ?? null,
    error: result.error ?? null,
    latency_ms: result.latency_ms ?? null,
  };
}

function summarizeResult(result) {
  const out = { ...result };
  if (typeof out.content === "string") {
    out.content_bytes = Buffer.byteLength(out.content, "utf8");
    delete out.content;
    out.content_omitted = true;
  }
  if (Array.isArray(out.entries) && out.entries.length > 50) {
    out.entries_truncated = true;
    out.entries = out.entries.slice(0, 50);
  }
  if (typeof out.stdout === "string") {
    out.stdout_bytes = Buffer.byteLength(out.stdout, "utf8");
    delete out.stdout;
  }
  if (typeof out.stderr === "string") delete out.stderr;
  return out;
}

function loadTask(taskId) {
  const file = envelope.taskFile(cfg.stateDir, taskId);
  return { file, events: envelope.readEvents(file) };
}

function newTaskRecord(spec) {
  const taskId = envelope.newTaskId();
  const traceId = crypto.randomUUID();
  envelope.ensureDir(cfg.stateDir);
  const file = envelope.taskFile(cfg.stateDir, taskId);
  const taskEvent = envelope.appendEvent(file, {
    schema: envelope.SCHEMA_TASK,
    type: "task",
    task_id: taskId,
    trace_id: traceId,
    parent_task_id: null,
    created_at: new Date().toISOString(),
    actor: spec.actor,
    task: {
      title: spec.title ?? null,
      statement: spec.statement,
      repository_before: spec.repositoryBefore ?? null,
    },
    ops: spec.ops,
    status: "submitted",
    limits: spec.limits,
  });
  return { taskId, traceId, file, taskEvent };
}

// ------------------------------------------------------------------ tool: health

function runHealth({ deep = false } = {}) {
  const checks = [];
  const engine = gate.engineMeta();
  checks.push({
    id: "engine.file",
    ok: engine.exists,
    detail: engine.exists
      ? `bytes=${engine.bytes}, sha256=${String(engine.sha256).slice(0, 16)}`
      : `missing: ${engine.path}`,
  });

  const rows = gate.journalRows();
  checks.push({
    id: "journal.repo",
    ok: fs.existsSync(cfg.journalPath),
    detail: `lines=${rows.length}, path=${cfg.journalPath}`,
  });

  let stateOk = false;
  let stateDetail = "";
  try {
    envelope.ensureDir(cfg.stateDir);
    const probe = path.join(cfg.stateDir, ".health-probe.tmp");
    fs.writeFileSync(probe, "ok", "utf8");
    fs.unlinkSync(probe);
    stateOk = true;
    stateDetail = `writable: ${cfg.stateDir}`;
  } catch (err) {
    stateDetail = `not writable: ${cfg.stateDir} (${err.code ?? err.message})`;
  }
  checks.push({ id: "state.dir", ok: stateOk, detail: stateDetail });

  checks.push({
    id: "runtime",
    ok: true,
    detail: `node ${process.version}; ESM; node builtins only; raw JSON-RPC 2.0 (no SDK, no npm install)`,
  });
  checks.push({
    id: "policy.source",
    ok: engine.exists,
    detail: "decisions only from aces-hook-engine.mjs subprocess (pretool/stop); no rules copied",
  });
  checks.push({
    id: "exec",
    ok: true,
    detail: cfg.enableExec ? "enabled via --enable-exec" : "disabled (default); exec ops are denied",
  });

  if (deep && engine.exists) {
    const scratch = path.join(repoRoot, ".aces-autoclaw", "health-probe");
    try {
      envelope.ensureDir(scratch);
      const probe = probeEngine({ enginePath: cfg.engine, cwd: scratch, timeoutMs: cfg.timeoutMs });
      checks.push({
        id: "engine.roundtrip",
        ok: probe.ok,
        detail: `delta_journal=${probe.delta}, latency_ms=${probe.latency_ms}, rule=${probe.rule_id}, decision=${probe.decision}${
          probe.error ? `, error=${probe.error}` : ""
        }`,
      });
    } catch (err) {
      checks.push({ id: "engine.roundtrip", ok: false, detail: `${err.code ?? "ERROR"}: ${err.message}` });
    }
  }

  return {
    ok: checks.every((c) => c.ok),
    node: process.version,
    protocol: PROTOCOL_VERSION,
    server: { name: SERVER_NAME, version: SERVER_VERSION },
    repo_root: repoRoot,
    engine: { path: engine.path, sha256: engine.sha256, bytes: engine.bytes },
    journal: { path: cfg.journalPath, lines: rows.length },
    state_dir: cfg.stateDir,
    exec_enabled: cfg.enableExec,
    checks,
  };
}

async function toolHealth(args = {}) {
  const deep = args.deep === true;
  return jsonResult(runHealth({ deep }));
}

// ------------------------------------------------------------- tool: submit_task

async function toolSubmitTask(args = {}) {
  let spec;
  try {
    spec = envelope.validateSubmit(args, {
      defaultActor: cfg.actor,
      defaultHarness: cfg.harness,
      maxOps: MAX_OPS,
    });
  } catch (err) {
    return toolError(err.code ?? "INVALID_PARAMS", err.message);
  }

  let created;
  try {
    created = newTaskRecord(spec);
  } catch (err) {
    return toolError(err.code ?? "STATE_WRITE_FAILED", err.message);
  }

  const results = [];
  for (const op of spec.ops) {
    // Serialised inside the gate; one engine call per op, by design.
    results.push(await gate.check(op, { taskId: created.taskId, opId: op.op_id }));
  }

  const decision = envelope.worst(results.map((r) => r.decision));
  const status = decision === "deny" ? "policy_denied" : decision === "ask" ? "needs_approval" : "submitted";
  const policyRecordList = results.map((r, i) => policyRecord(spec.ops[i], r));

  try {
    envelope.appendEvent(created.file, {
      schema: envelope.SCHEMA_TASK,
      type: "policy",
      task_id: created.taskId,
      trace_id: created.traceId,
      checked_at: new Date().toISOString(),
      policy: { engine: cfg.engine, decision, results: policyRecordList },
      status,
    });
  } catch (err) {
    return toolError(err.code ?? "STATE_WRITE_FAILED", err.message);
  }

  const failed = results.find((r) => r.decision !== "allow");
  const message =
    decision === "allow"
      ? "all operations allowed; invoke them one by one with aces_invoke_tool"
      : decision === "ask"
        ? `approval required (${failed?.rule_id}): ${failed?.reason ?? "no reason returned"}; v0 has no approval channel, the task is terminal`
        : `denied (${failed?.rule_id}): ${failed?.reason ?? "no reason returned"}; nothing was executed`;

  return jsonResult({
    task_id: created.taskId,
    trace_id: created.traceId,
    status,
    policy: { decision, results: policyRecordList },
    next: status === "submitted" ? "invoke_tool" : "stop",
    state_file: created.file,
    message,
  });
}

// ------------------------------------------------------------- tool: invoke_tool

function executeOp(op, toolInput = {}) {
  switch (op.kind) {
    case "read":
      return fsops.readTarget(repoRoot, op.target);
    case "list":
      return fsops.listTarget(repoRoot, op.target);
    case "git_status":
      fsops.requireGitRepo(repoRoot);
      return fsops.gitStatus(repoRoot);
    case "write":
      return fsops.writeTarget(repoRoot, op.target, toolInput?.content);
    case "edit":
      return fsops.editTarget(repoRoot, op.target, toolInput ?? {});
    case "exec": {
      const isWindows = process.platform === "win32";
      const command = op.shell === "bash" ? (isWindows ? "bash" : "bash") : isWindows ? "powershell" : "pwsh";
      const args =
        op.shell === "bash"
          ? ["-lc", String(op.target)]
          : ["-NoProfile", "-NonInteractive", "-Command", String(op.target)];
      const res = spawnSync(command, args, {
        cwd: repoRoot,
        encoding: "utf8",
        timeout: 60000,
        shell: false,
        windowsHide: true,
        maxBuffer: 4 << 20,
      });
      if (res.error) throw new fsops.FsOpError("EXEC_FAILED", `${res.error.code ?? ""} ${res.error.message ?? ""}`.trim());
      return {
        kind: "exec",
        command: String(op.target),
        exit_code: res.status,
        stdout: String(res.stdout ?? "").slice(0, 65536),
        stderr: String(res.stderr ?? "").slice(0, 8192),
      };
    }
    default:
      throw new fsops.FsOpError("ACES-UNMAPPED-OP", `unsupported operation kind: ${op.kind}`);
  }
}

async function toolInvokeTool(args = {}) {
  const implicitOp = args.op && typeof args.op === "object" ? args.op : null;
  let taskId = typeof args.task_id === "string" ? args.task_id : null;
  let opId = typeof args.op_id === "string" ? args.op_id : null;
  let created = null;
  let file;
  let events;
  let taskEvent;

  try {
    if (!taskId) {
      if (!implicitOp) {
        return toolError("INVALID_PARAMS", "either task_id+op_id or op{kind,target} is required");
      }
      const spec = envelope.validateSubmit(
        { task: { statement: `implicit ${implicitOp.kind}: ${String(implicitOp.target ?? "")}`.slice(0, 8000) }, ops: [implicitOp] },
        { defaultActor: cfg.actor, defaultHarness: cfg.harness, maxOps: MAX_OPS },
      );
      created = newTaskRecord(spec);
      taskId = created.taskId;
      file = created.file;
      events = [created.taskEvent];
      taskEvent = created.taskEvent;
      opId = spec.ops[0].op_id;
    } else {
      const loaded = loadTask(taskId);
      file = loaded.file;
      events = loaded.events;
      taskEvent = envelope.getTaskEvent(events);
    }
  } catch (err) {
    return toolError(err.code ?? "TASK_NOT_FOUND", err.message, { state_dir: cfg.stateDir });
  }

  if (!opId) return toolError("INVALID_PARAMS", "op_id is required when task_id is given");
  const ops = Array.isArray(taskEvent.ops) ? taskEvent.ops : [];
  const op = ops.find((o) => o.op_id === opId);
  if (!op) {
    return toolError("OP_NOT_FOUND", `op ${opId} is not part of task ${taskId}`, { task_id: taskId, ops: ops.map((o) => o.op_id) });
  }

  let status = envelope.deriveStatus(events);
  if (envelope.TERMINAL_STATUSES.includes(status)) {
    return toolError("TASK_NOT_DISPATCHABLE", `task ${taskId} is ${status}`, { task_id: taskId, status });
  }

  const deadline = envelope.deadlineOf(taskEvent);
  if (deadline !== null && Date.now() > deadline) {
    envelope.appendEvent(file, {
      schema: envelope.SCHEMA_TASK,
      type: "dispatch",
      task_id: taskId,
      op_id: opId,
      status: "denied",
      policy: { decision: "deny", rule_id: "EXPIRED", reason: "task deadline exceeded", journal: null },
      result: null,
    });
    return toolError("EXPIRED", `task ${taskId} deadline exceeded`, { task_id: taskId, status: "expired" });
  }

  // Re-check policy at execution time: state and environment may have changed.
  const decision = await gate.check(op, { taskId, opId });

  if (decision.decision !== "allow") {
    try {
      envelope.appendEvent(file, {
        schema: envelope.SCHEMA_TASK,
        type: "dispatch",
        task_id: taskId,
        op_id: opId,
        status: "denied",
        policy: policyRecord(op, decision),
        result: null,
      });
    } catch (err) {
      logErr(err);
    }
    const code =
      decision.decision === "ask" ? "NEEDS_APPROVAL" : decision.error?.code ?? decision.rule_id ?? "POLICY_DENIED";
    return toolError(code, decision.reason ?? `policy decision: ${decision.decision}`, {
      task_id: taskId,
      op_id: opId,
      policy: policyView(decision),
    });
  }

  let result;
  try {
    result = executeOp(op, args.tool_input ?? {});
  } catch (err) {
    const code = err.code ?? "EXECUTION_FAILED";
    try {
      envelope.appendEvent(file, {
        schema: envelope.SCHEMA_TASK,
        type: "dispatch",
        task_id: taskId,
        op_id: opId,
        status: "error",
        policy: policyRecord(op, decision),
        error: { code, message: err.message, detail: err.detail ?? null },
        result: null,
      });
    } catch (writeErr) {
      logErr(writeErr);
    }
    return toolError(code, err.message, { task_id: taskId, op_id: opId, policy: policyView(decision) });
  }

  try {
    envelope.appendEvent(file, {
      schema: envelope.SCHEMA_TASK,
      type: "dispatch",
      task_id: taskId,
      op_id: opId,
      status: "ok",
      policy: policyRecord(op, decision),
      result: summarizeResult(result),
    });
  } catch (err) {
    logErr(err);
    return toolError(err.code ?? "STATE_WRITE_FAILED", `operation executed but its record could not be written: ${err.message}`, {
      task_id: taskId,
      op_id: opId,
    });
  }

  return jsonResult({
    task_id: taskId,
    op_id: opId,
    status: "ok",
    policy: policyView(decision),
    result,
  });
}

// ------------------------------------------------------------ tool: record_result

function splitMissing(reason) {
  if (!reason) return [];
  return String(reason)
    .replace(/^PASS blocked; complete:\s*/i, "")
    .split(/,\s*/)
    .map((s) => s.trim())
    .filter(Boolean);
}

async function toolRecordResult(args = {}) {
  const taskId = args.task_id;
  if (typeof taskId !== "string") return toolError("INVALID_PARAMS", "task_id is required");
  const outcome = String(args.outcome ?? "");
  if (!envelope.OUTCOMES.includes(outcome)) {
    return toolError("INVALID_PARAMS", `outcome must be one of ${envelope.OUTCOMES.join("|")}`);
  }
  const verdict = args.verdict ?? null;
  if (verdict !== null && !envelope.VERDICTS.includes(verdict)) {
    return toolError("INVALID_PARAMS", `verdict must be one of ${envelope.VERDICTS.join("|")}`);
  }

  let file;
  let events;
  try {
    const loaded = loadTask(taskId);
    file = loaded.file;
    events = loaded.events;
  } catch (err) {
    return toolError(err.code ?? "TASK_NOT_FOUND", err.message);
  }

  const verification = args.verification ?? {};
  const exitCode = args.exit_code === undefined || args.exit_code === null ? null : Number(args.exit_code);
  if (exitCode !== null && !Number.isInteger(exitCode)) {
    return toolError("INVALID_PARAMS", "exit_code must be an integer");
  }
  let testFileExists = null;
  if (typeof verification.test_file === "string" && verification.test_file.trim() !== "") {
    testFileExists = fs.existsSync(path.resolve(repoRoot, verification.test_file));
  }

  const notes = typeof args.notes === "string" ? args.notes.slice(0, 2000) : null;
  const record = typeof args.record === "string" ? args.record : null;

  let stopGate;
  if (verdict === "PASS" && !record) {
    // Deliberate: a PASS without a record is blocked without consuming a journal row.
    stopGate = {
      decision: "block",
      rule_id: "STOP-RECORD",
      reason: "PASS requires an ACES_ITERATION_RECORD with evidence and defect classifications.",
      journal: null,
      error: { code: "STOP-RECORD", message: "record is required when verdict=PASS" },
      latency_ms: 0,
      engine: null,
    };
  } else {
    const message = record ?? [notes, verdict ? `VERDICT: ${verdict}` : null].filter(Boolean).join("\n");
    stopGate = await gate.stop({ taskId, message });
  }

  const statusAfter = stopGate.decision === "block" ? "failed" : outcome === "ok" ? "completed" : "failed";
  const resultEvent = {
    schema: envelope.SCHEMA_RESULT,
    type: "result",
    task_id: taskId,
    trace_id: envelope.getTaskEvent(events).trace_id,
    recorded_at: new Date().toISOString(),
    op_id: typeof args.op_id === "string" ? args.op_id : null,
    outcome,
    exit_code: exitCode,
    verification: {
      command: typeof verification.command === "string" ? verification.command.slice(0, 2000) : null,
      raw_output: typeof verification.raw_output === "string" ? verification.raw_output.slice(0, 65536) : null,
      exit_code: verification.exit_code === undefined || verification.exit_code === null ? null : Number(verification.exit_code),
      test_file: typeof verification.test_file === "string" ? verification.test_file : null,
      test_file_exists: testFileExists,
    },
    stop_gate: {
      decision: stopGate.decision,
      rule_id: stopGate.rule_id,
      reason: stopGate.reason ?? null,
      journal: stopGate.journal ?? null,
    },
    verdict,
    notes,
    status_after: statusAfter,
  };

  let seq;
  try {
    seq = envelope.appendEvent(file, resultEvent).seq;
    envelope.appendEvent(file, {
      schema: envelope.SCHEMA_RESULT,
      type: "close",
      task_id: taskId,
      trace_id: resultEvent.trace_id,
      closed_at: new Date().toISOString(),
      status_after: statusAfter,
      stop_gate: resultEvent.stop_gate,
    });
  } catch (err) {
    return toolError(err.code ?? "STATE_WRITE_FAILED", err.message);
  }

  return jsonResult({
    task_id: taskId,
    status_after: statusAfter,
    stop_gate: {
      decision: stopGate.decision,
      rule_id: stopGate.rule_id,
      reason: stopGate.reason ?? null,
      journal_line: stopGate.journal?.line ?? null,
      journal: stopGate.journal ?? null,
    },
    missing: stopGate.decision === "block" ? splitMissing(stopGate.reason) : [],
    seq,
  });
}

// ----------------------------------------------------------- tool: get_provenance

async function toolGetProvenance(args = {}) {
  const taskId = args.task_id;
  if (typeof taskId !== "string") return toolError("INVALID_PARAMS", "task_id is required");
  const include = Array.isArray(args.include) ? args.include : ["events", "journal", "artifacts"];
  const tailN = args.journal_tail === undefined ? 0 : Number(args.journal_tail);
  if (!Number.isInteger(tailN) || tailN < 0 || tailN > 200) {
    return toolError("INVALID_PARAMS", "journal_tail must be an integer in 0..200");
  }

  let events;
  try {
    events = loadTask(taskId).events;
  } catch (err) {
    return toolError(err.code ?? "TASK_NOT_FOUND", err.message);
  }

  const check = verifyEvents(events, cfg.journalPath);
  const rows = readJournalRows(cfg.journalPath);
  const byLine = new Map(rows.map((r) => [r.line, r]));

  const refs = [];
  for (const ev of events) {
    if (ev.type === "policy" && Array.isArray(ev.policy?.results)) {
      for (const r of ev.policy.results) if (r.journal) refs.push({ where: `policy#${ev.seq}:${r.op_id}`, ...r.journal });
    }
    if (ev.type === "dispatch" && ev.policy?.journal) refs.push({ where: `dispatch#${ev.seq}`, ...ev.policy.journal });
    if (ev.type === "result" && ev.stop_gate?.journal) refs.push({ where: `result#${ev.seq}`, ...ev.stop_gate.journal });
    if (ev.type === "close" && ev.stop_gate?.journal) refs.push({ where: `close#${ev.seq}`, ...ev.stop_gate.journal });
  }

  const response = {
    task_id: taskId,
    status: envelope.deriveStatus(events),
    verified: check.verified,
    checked_refs: check.checked,
    gaps: check.gaps,
  };
  if (include.includes("events")) response.events = events;
  if (include.includes("journal")) {
    response.journal = refs.map((ref) => {
      const row = byLine.get(ref.line);
      return {
        where: ref.where,
        line: ref.line,
        exists: Boolean(row),
        sha256_matches: Boolean(row && row.row_sha256 === ref.row_sha256),
        rule_id: row?.rule_id ?? null,
        decision: row?.decision ?? null,
        row: row?.row ?? null,
      };
    });
  }
  if (tailN > 0) response.journal_tail = readJournalTail(cfg.journalPath, tailN);
  if (include.includes("artifacts")) {
    const stat = fs.statSync(envelope.taskFile(cfg.stateDir, taskId));
    response.artifacts = [
      { path: envelope.taskFile(cfg.stateDir, taskId), bytes: stat.size, events: events.length },
    ];
  }
  return jsonResult(response);
}

// ------------------------------------------------------------------- tool catalog

const STRING = { type: "string" };
const TOOL_DEFS = [
  {
    name: "aces_health",
    description:
      "Проверка моста ACES: наличие и хеш hook-движка, журнал, каталог состояния, режим exec. deep=true добавляет синтетический прогон движка в скретч-каталоге (журнал репозитория не трогается).",
    inputSchema: {
      type: "object",
      properties: { deep: { type: "boolean", description: "выполнить реальный round-trip движка" } },
      additionalProperties: false,
    },
  },
  {
    name: "aces_submit_task",
    description:
      "Объявить задачу до любых действий. По каждой операции движок aces-hook-engine.mjs (pretool) выносит решение; ни одна операция здесь не исполняется.",
    inputSchema: {
      type: "object",
      properties: {
        task: {
          type: "object",
          properties: { statement: { type: "string", maxLength: 8000 }, title: { type: "string", maxLength: 200 }, repository_before: { type: "string" } },
          required: ["statement"],
          additionalProperties: false,
        },
        ops: {
          type: "array",
          minItems: 1,
          maxItems: MAX_OPS,
          items: {
            type: "object",
            properties: {
              op_id: { type: "string", pattern: "^op_[0-9a-f]{4}$" },
              kind: { type: "string", enum: ["read", "write", "edit", "list", "git_status", "exec"] },
              target: { type: "string", maxLength: 1024 },
              intent: { type: "string", maxLength: 500 },
              shell: { type: "string", enum: ["powershell", "bash"] },
            },
            required: ["kind", "target"],
            additionalProperties: false,
          },
        },
        actor: {
          type: "object",
          properties: {
            id: STRING,
            harness: { type: "string", enum: ["autoclaw", "pi", "zcode", "hermes", "unknown"] },
            session_hint: STRING,
          },
          additionalProperties: false,
        },
        limits: {
          type: "object",
          properties: {
            deadline_ms: { type: "integer", minimum: 1000, maximum: 86400000 },
            max_ops: { type: "integer", minimum: 1, maximum: MAX_OPS },
          },
          additionalProperties: false,
        },
      },
      required: ["task", "ops"],
      additionalProperties: false,
    },
  },
  {
    name: "aces_invoke_tool",
    description:
      "Исполнить одну ранее объявленную операцию. Политика перепроверяется движком непосредственно перед исполнением; deny/ask/таймаут означают отказ без выполнения. Белый список: read, list, git_status, write, edit (exec только при --enable-exec).",
    inputSchema: {
      type: "object",
      properties: {
        task_id: { type: "string" },
        op_id: { type: "string" },
        op: {
          type: "object",
          description: "неявная задача: операция без предварительного aces_submit_task",
          properties: {
            kind: { type: "string", enum: ["read", "write", "edit", "list", "git_status", "exec"] },
            target: { type: "string" },
            shell: { type: "string", enum: ["powershell", "bash"] },
          },
          required: ["kind", "target"],
          additionalProperties: false,
        },
        tool_input: {
          type: "object",
          properties: { content: { type: "string" }, old_string: { type: "string" }, new_string: { type: "string" } },
          additionalProperties: false,
        },
      },
      additionalProperties: false,
    },
  },
  {
    name: "aces_record_result",
    description:
      "Зафиксировать результат задачи и пройти Stop-гейт ACES. При verdict=PASS обязателен полный текст ACES_ITERATION_RECORD в поле record.",
    inputSchema: {
      type: "object",
      properties: {
        task_id: { type: "string" },
        op_id: { type: "string" },
        outcome: { type: "string", enum: ["ok", "denied", "error", "timeout", "skipped"] },
        exit_code: { type: "integer" },
        verification: {
          type: "object",
          properties: {
            command: { type: "string" },
            raw_output: { type: "string" },
            exit_code: { type: "integer" },
            test_file: { type: "string" },
          },
          additionalProperties: false,
        },
        verdict: { type: "string", enum: ["PASS", "FAIL", "BLOCKED", "STOP", "CONDITIONAL"] },
        record: { type: "string", description: "полный ACES_ITERATION_RECORD" },
        notes: { type: "string" },
      },
      required: ["task_id", "outcome"],
      additionalProperties: false,
    },
  },
  {
    name: "aces_get_provenance",
    description:
      "Только чтение: события задачи и сверка ссылок на journal.tsv по номеру строки и sha256. Ничего не исправляет; при расхождении возвращает verified=false и gaps.",
    inputSchema: {
      type: "object",
      properties: {
        task_id: { type: "string" },
        include: { type: "array", items: { type: "string", enum: ["events", "journal", "artifacts"] } },
        journal_tail: { type: "integer", minimum: 0, maximum: 200 },
      },
      required: ["task_id"],
      additionalProperties: false,
    },
  },
];

const HANDLERS = {
  aces_health: toolHealth,
  aces_submit_task: toolSubmitTask,
  aces_invoke_tool: toolInvokeTool,
  aces_record_result: toolRecordResult,
  aces_get_provenance: toolGetProvenance,
};

// ------------------------------------------------------------------ JSON-RPC core

function rpcError(id, code, message, data) {
  return { jsonrpc: "2.0", id: id ?? null, error: { code, message, ...(data === undefined ? {} : { data }) } };
}

async function handleMessage(msg) {
  if (!msg || typeof msg !== "object" || Array.isArray(msg)) {
    return rpcError(null, -32600, "invalid request");
  }
  const { id, method, params } = msg;
  const isNotification = id === undefined || id === null;
  if (typeof method !== "string") {
    return isNotification ? null : rpcError(id, -32600, "method must be a string");
  }

  if (method === "initialize") {
    const requested = params?.protocolVersion;
    const protocolVersion = SUPPORTED_PROTOCOLS.includes(requested) ? requested : PROTOCOL_VERSION;
    return {
      jsonrpc: "2.0",
      id,
      result: {
        protocolVersion,
        capabilities: { tools: { listChanged: false } },
        serverInfo: { name: SERVER_NAME, version: SERVER_VERSION },
        instructions:
          "ACES bridge. Policy decisions come only from aces-hook-engine.mjs; operations routed through this server are enforced, other harness tools are not. v0: ask is terminal (no approval channel).",
      },
    };
  }

  if (method === "notifications/initialized" || method === "initialized") return null;
  if (method === "ping") return { jsonrpc: "2.0", id, result: {} };

  if (method === "tools/list") {
    return { jsonrpc: "2.0", id, result: { tools: TOOL_DEFS } };
  }

  if (method === "tools/call") {
    const name = params?.name;
    const args = params?.arguments ?? {};
    if (typeof name !== "string" || !HANDLERS[name]) {
      return rpcError(id, -32602, `unknown tool: ${String(name)}`, { tools: Object.keys(HANDLERS) });
    }
    if (args !== null && typeof args !== "object") {
      return rpcError(id, -32602, "arguments must be an object");
    }
    try {
      const result = await HANDLERS[name](args);
      return { jsonrpc: "2.0", id, result };
    } catch (err) {
      logErr(err);
      return rpcError(id, -32603, `tool ${name} failed: ${err.message}`, { code: err.code ?? "INTERNAL" });
    }
  }

  return isNotification ? null : rpcError(id, -32601, `method not found: ${method}`);
}

async function handlePayload(text) {
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    return rpcError(null, -32700, "parse error");
  }
  if (Array.isArray(parsed)) {
    if (parsed.length === 0) return rpcError(null, -32600, "empty batch");
    const responses = [];
    for (const item of parsed) {
      let res = null;
      try {
        res = await handleMessage(item);
      } catch (err) {
        const id = item && typeof item === "object" && item.id != null ? item.id : null;
        res = rpcError(id, -32603, `internal error: ${err.message}`);
      }
      if (res) responses.push(res);
    }
    return responses.length ? responses : null;
  }
  try {
    return await handleMessage(parsed);
  } catch (err) {
    const id = parsed && typeof parsed === "object" && parsed.id != null ? parsed.id : null;
    return rpcError(id, -32603, `internal error: ${err.message}`);
  }
}

// ----------------------------------------------------------------- stdio framing

class StdioFramer {
  constructor(stream, onFrame, onError) {
    this.stream = stream;
    this.onFrame = onFrame;
    this.onError = onError;
    this.buf = Buffer.alloc(0);
    stream.on("data", (chunk) => {
      this.buf = Buffer.concat([this.buf, chunk]);
      try {
        this.pump();
      } catch (err) {
        onError(err);
      }
    });
  }

  pump() {
    for (;;) {
      if (this.buf.length === 0) return;
      let skip = 0;
      while (
        skip < this.buf.length &&
        (this.buf[skip] === 0x0a || this.buf[skip] === 0x0d || this.buf[skip] === 0x20 || this.buf[skip] === 0x09)
      ) {
        skip += 1;
      }
      if (skip > 0) {
        this.buf = this.buf.subarray(skip);
        if (this.buf.length === 0) return;
      }

      const head = this.buf.subarray(0, Math.min(this.buf.length, 15)).toString("latin1").toLowerCase();
      if (head.startsWith("content-length:")) {
        const crlf = this.buf.indexOf("\r\n\r\n");
        const lf = this.buf.indexOf("\n\n");
        let headerEnd = -1;
        let sepLen = 0;
        if (crlf >= 0 && (lf < 0 || crlf <= lf)) {
          headerEnd = crlf;
          sepLen = 4;
        } else if (lf >= 0) {
          headerEnd = lf;
          sepLen = 2;
        }
        if (headerEnd < 0) {
          if (this.buf.length > 65536) throw new Error("framing header exceeds 64 KiB");
          return;
        }
        const header = this.buf.subarray(0, headerEnd).toString("latin1");
        const match = /content-length:\s*(\d+)/i.exec(header);
        const start = headerEnd + sepLen;
        if (!match) {
          this.buf = this.buf.subarray(start);
          throw new Error("Content-Length header is missing");
        }
        const length = Number(match[1]);
        if (this.buf.length < start + length) return;
        const body = this.buf.subarray(start, start + length).toString("utf8");
        this.buf = this.buf.subarray(start + length);
        this.onFrame(body, "content-length");
        continue;
      }

      const nl = this.buf.indexOf(0x0a);
      if (nl < 0) return;
      const line = this.buf.subarray(0, nl).toString("utf8");
      this.buf = this.buf.subarray(nl + 1);
      if (line.trim() === "") continue;
      this.onFrame(line, "ndjson");
    }
  }
}

function send(payload, framing) {
  if (payload === null || payload === undefined) return;
  const json = JSON.stringify(payload);
  if (framing === "content-length") {
    process.stdout.write(`Content-Length: ${Buffer.byteLength(json, "utf8")}\r\n\r\n${json}`);
  } else {
    process.stdout.write(`${json}\n`);
  }
}

// ------------------------------------------------------------------------- main

function main() {
  if (cfg.help) {
    process.stdout.write(HELP);
    return;
  }
  if (cfg.health) {
    const health = runHealth({ deep: cfg.deep });
    process.stdout.write(`${JSON.stringify(health, null, 2)}\n`);
    process.exitCode = health.ok ? 0 : 1;
    return;
  }

  if (!fs.existsSync(cfg.engine)) {
    process.stderr.write(`[aces-bridge] hook engine not found: ${cfg.engine}\n`);
  }

  let queue = Promise.resolve();
  const framer = new StdioFramer(
    process.stdin,
    (text, framing) => {
      queue = queue
        .then(async () => {
          const response = await handlePayload(text);
          send(response, framing);
        })
        .catch((err) => {
          logErr(err);
          send(rpcError(null, -32603, `internal error: ${err.message}`), framing);
        });
    },
    (err) => {
      process.stderr.write(`[aces-bridge] framing error: ${err.message}\n`);
    },
  );
  framer.stream.on("end", () => {
    queue.finally(() => {
      process.exitCode = 0;
    });
  });
  process.stdout.on("error", (err) => {
    if (err.code === "EPIPE") process.exit(0);
    logErr(err);
  });
  process.stderr.write(
    `[aces-bridge] ready: repo=${repoRoot} engine=${cfg.engine} exec=${cfg.enableExec ? "on" : "off"}\n`,
  );
}

main();

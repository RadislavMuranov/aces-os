// ACES OS <-> AutoClaw bridge: task/result envelopes and append-only state.
// Design reference: aces-integration/04-design.md sections 4, 5.
// Node builtins only. This module never decides policy: it only stores evidence.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";

export const SCHEMA_TASK = "aces.autoclaw.task/v1";
export const SCHEMA_RESULT = "aces.autoclaw.result/v1";
export const TASK_ID_RE = /^t_[0-9]{8}T[0-9]{6}Z_[0-9a-f]{10}$/;
export const OP_ID_RE = /^op_[0-9a-f]{4}$/;
export const TERMINAL_STATUSES = Object.freeze([
  "policy_denied",
  "needs_approval",
  "completed",
  "failed",
  "expired",
]);
export const OP_KINDS = Object.freeze(["read", "write", "edit", "list", "git_status", "exec"]);
export const HARNESSES = Object.freeze(["autoclaw", "pi", "zcode", "hermes", "unknown"]);
export const OUTCOMES = Object.freeze(["ok", "denied", "error", "timeout", "skipped"]);
export const VERDICTS = Object.freeze(["PASS", "FAIL", "BLOCKED", "STOP", "CONDITIONAL"]);

export class EnvelopeError extends Error {
  constructor(code, message, detail) {
    super(message);
    this.name = "EnvelopeError";
    this.code = code;
    this.detail = detail ?? null;
  }
}

export function newTaskId(now = new Date()) {
  const compact = now.toISOString().replace(/[-:]/g, ""); // 20261120T022236.939Z
  const stamp = compact.slice(0, 15) + "Z"; // 20261120T022236Z
  return `t_${stamp}_${crypto.randomBytes(5).toString("hex")}`;
}

export function newOpId(taken = new Set()) {
  for (;;) {
    const id = "op_" + crypto.randomBytes(2).toString("hex");
    if (!taken.has(id)) return id;
  }
}

export function stateDir(repoRoot) {
  return path.join(repoRoot, ".aces-autoclaw", "state");
}

export function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
  return dir;
}

export function taskFile(dir, taskId) {
  if (!TASK_ID_RE.test(String(taskId ?? ""))) {
    throw new EnvelopeError("INVALID_TASK_ID", `task_id does not match ${TASK_ID_RE}: ${taskId}`);
  }
  return path.join(dir, `${taskId}.jsonl`);
}

export function listTaskFiles(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".jsonl"))
    .map((f) => path.join(dir, f))
    .sort();
}

export function readEvents(file) {
  if (!fs.existsSync(file)) {
    throw new EnvelopeError("TASK_NOT_FOUND", `no such task file: ${file}`);
  }
  const text = fs.readFileSync(file, "utf8");
  const lines = text.split("\n").filter((l) => l.trim() !== "");
  const events = [];
  for (let i = 0; i < lines.length; i += 1) {
    let ev;
    try {
      ev = JSON.parse(lines[i]);
    } catch {
      throw new EnvelopeError("STATE_CORRUPT", `${file}: line ${i + 1} is not valid JSON`);
    }
    if (!ev || typeof ev !== "object" || Array.isArray(ev)) {
      throw new EnvelopeError("STATE_CORRUPT", `${file}: line ${i + 1} is not an object`);
    }
    if (ev.seq !== i + 1) {
      throw new EnvelopeError(
        "STATE_CORRUPT",
        `${file}: line ${i + 1} has seq=${ev.seq}, expected ${i + 1}`,
      );
    }
    events.push(ev);
  }
  if (events.length === 0) {
    throw new EnvelopeError("STATE_CORRUPT", `${file}: empty task file`);
  }
  return events;
}

// Append-only: never rewrites, never reorders. fsync to survive a crash.
export function appendEvent(file, event) {
  const existing = fs.existsSync(file) ? readEvents(file) : [];
  const record = { ...event, seq: existing.length + 1 };
  const line = `${JSON.stringify(record)}\n`;
  const fd = fs.openSync(file, "a");
  try {
    fs.writeSync(fd, line, null, "utf8");
    fs.fsyncSync(fd);
  } finally {
    fs.closeSync(fd);
  }
  return record;
}

export function getTaskEvent(events) {
  const task = events.find((e) => e.type === "task");
  if (!task) throw new EnvelopeError("STATE_CORRUPT", "task event is missing");
  return task;
}

export function deriveStatus(events) {
  let status = "submitted";
  for (const ev of events) {
    if (ev.type === "policy" && ev.status) status = ev.status;
    else if (ev.type === "dispatch") status = "dispatched";
    else if (ev.type === "result" && ev.status_after) status = ev.status_after;
    else if (ev.type === "close" && ev.status_after) status = ev.status_after;
  }
  return status;
}

// Worst-of: deny > ask > allow. Used to fold per-op decisions into one task status.
export function worst(decisions) {
  let out = "allow";
  for (const d of decisions) {
    if (d === "deny") return "deny";
    if (d === "ask") out = "ask";
  }
  return out;
}

function reqString(value, field, { min = 1, max = 4096 } = {}) {
  if (typeof value !== "string") {
    throw new EnvelopeError("INVALID_PARAMS", `${field} must be a string`);
  }
  const trimmed = value.trim();
  if (trimmed.length < min) {
    throw new EnvelopeError("INVALID_PARAMS", `${field} must be at least ${min} character(s)`);
  }
  if (value.length > max) {
    throw new EnvelopeError("INVALID_PARAMS", `${field} exceeds ${max} characters`);
  }
  return value;
}

function optString(value, field, { max = 4096 } = {}) {
  if (value === undefined || value === null) return null;
  if (typeof value !== "string") {
    throw new EnvelopeError("INVALID_PARAMS", `${field} must be a string`);
  }
  if (value.length > max) {
    throw new EnvelopeError("INVALID_PARAMS", `${field} exceeds ${max} characters`);
  }
  return value;
}

export function validateSubmit(input, { defaultActor = "autoclaw-desktop", defaultHarness = "autoclaw", maxOps = 32 } = {}) {
  if (!input || typeof input !== "object" || Array.isArray(input)) {
    throw new EnvelopeError("INVALID_PARAMS", "arguments must be an object");
  }
  const task = input.task ?? {};
  const statement = reqString(task.statement, "task.statement", { max: 8000 });
  const title = optString(task.title, "task.title", { max: 200 });
  const repositoryBefore = optString(task.repository_before, "task.repository_before", { max: 2000 });

  const limits = input.limits ?? {};
  const deadlineMs = limits.deadline_ms === undefined ? 900000 : Number(limits.deadline_ms);
  if (!Number.isInteger(deadlineMs) || deadlineMs < 1000 || deadlineMs > 86400000) {
    throw new EnvelopeError("INVALID_PARAMS", "limits.deadline_ms must be an integer in 1000..86400000");
  }
  const limitOps = limits.max_ops === undefined ? Math.min(8, maxOps) : Number(limits.max_ops);
  if (!Number.isInteger(limitOps) || limitOps < 1 || limitOps > maxOps) {
    throw new EnvelopeError("INVALID_PARAMS", `limits.max_ops must be an integer in 1..${maxOps}`);
  }

  const rawOps = input.ops;
  if (!Array.isArray(rawOps) || rawOps.length === 0) {
    throw new EnvelopeError("INVALID_PARAMS", "ops must be a non-empty array");
  }
  if (rawOps.length > limitOps) {
    throw new EnvelopeError("INVALID_PARAMS", `ops has ${rawOps.length} entries, limits.max_ops=${limitOps}`);
  }
  if (rawOps.length > maxOps) {
    throw new EnvelopeError("INVALID_PARAMS", `ops exceeds the hard cap of ${maxOps}`);
  }

  const taken = new Set();
  const ops = rawOps.map((raw, index) => {
    const field = `ops[${index}]`;
    if (!raw || typeof raw !== "object" || Array.isArray(raw)) {
      throw new EnvelopeError("INVALID_PARAMS", `${field} must be an object`);
    }
    const kind = String(raw.kind ?? "");
    if (!OP_KINDS.includes(kind)) {
      throw new EnvelopeError("INVALID_PARAMS", `${field}.kind must be one of ${OP_KINDS.join("|")}`);
    }
    const target = reqString(raw.target ?? (kind === "git_status" ? "." : undefined), `${field}.target`, { max: 1024 });
    const intent = optString(raw.intent, `${field}.intent`, { max: 500 });
    let shell = null;
    if (kind === "exec") {
      shell = raw.shell === undefined ? (process.platform === "win32" ? "powershell" : "bash") : String(raw.shell);
      if (!["powershell", "bash"].includes(shell)) {
        throw new EnvelopeError("INVALID_PARAMS", `${field}.shell must be powershell|bash`);
      }
    }
    let opId = raw.op_id;
    if (opId === undefined || opId === null) {
      opId = newOpId(taken);
    } else {
      opId = String(opId);
      if (!OP_ID_RE.test(opId)) {
        throw new EnvelopeError("INVALID_PARAMS", `${field}.op_id must match ${OP_ID_RE}`);
      }
      if (taken.has(opId)) {
        throw new EnvelopeError("INVALID_PARAMS", `${field}.op_id is duplicated: ${opId}`);
      }
    }
    taken.add(opId);
    return { op_id: opId, kind, target, intent, shell };
  });

  const actor = input.actor ?? {};
  const actorId = optString(actor.id, "actor.id", { max: 64 }) ?? defaultActor;
  const harness = actor.harness === undefined ? defaultHarness : String(actor.harness);
  if (!HARNESSES.includes(harness)) {
    throw new EnvelopeError("INVALID_PARAMS", `actor.harness must be one of ${HARNESSES.join("|")}`);
  }
  const sessionHint = optString(actor.session_hint, "actor.session_hint", { max: 128 });

  return {
    statement,
    title,
    repositoryBefore,
    ops,
    limits: { deadline_ms: deadlineMs, max_ops: limitOps },
    actor: { kind: "agent", id: actorId, harness, session_hint: sessionHint },
  };
}

export function deadlineOf(taskEvent) {
  const created = Date.parse(taskEvent.created_at);
  const ms = Number(taskEvent.limits?.deadline_ms ?? 0);
  if (!Number.isFinite(created) || !Number.isFinite(ms) || ms <= 0) return null;
  return created + ms;
}

// Filesystem and read-only process operations for the bridge, with
// realpath-based containment inside the repository root.
// Design reference: aces-integration/04-design.md sections 6.6, 7.2.

import fs from "node:fs";
import path from "node:path";
import crypto from "node:crypto";
import { spawnSync } from "node:child_process";

export const MAX_READ_BYTES = 262144;

export class FsOpError extends Error {
  constructor(code, message, detail) {
    super(message);
    this.name = "FsOpError";
    this.code = code;
    this.detail = detail ?? null;
  }
}

function sha256Hex(input) {
  return crypto.createHash("sha256").update(input).digest("hex");
}

function isInside(rootReal, candidate) {
  const rel = path.relative(rootReal, candidate);
  return rel === "" || (!rel.startsWith("..") && !path.isAbsolute(rel));
}

// Real path of the nearest existing ancestor: the non-existent tail cannot
// contain symlinks, so checking the anchor is enough to prove containment.
function realpathNearest(abs) {
  let cur = abs;
  for (;;) {
    try {
      return fs.realpathSync(cur);
    } catch (err) {
      if (err.code !== "ENOENT" && err.code !== "ENOTDIR") {
        throw new FsOpError("PATH_UNRESOLVABLE", `cannot resolve ${cur}: ${err.code}`);
      }
      const parent = path.dirname(cur);
      if (parent === cur) throw new FsOpError("PATH_UNRESOLVABLE", `cannot resolve ${abs}`);
      cur = parent;
    }
  }
}

export function assertInside(root, target) {
  const rootReal = fs.realpathSync(root);
  const abs = path.resolve(root, String(target ?? ""));
  const anchor = realpathNearest(abs);
  if (!isInside(rootReal, anchor)) {
    throw new FsOpError("PATH-ESCAPE", `path escapes repository root: ${abs}`, {
      root: rootReal,
      anchor,
    });
  }
  return abs;
}

function statOrThrow(abs) {
  try {
    return fs.statSync(abs);
  } catch (err) {
    if (err.code === "ENOENT") throw new FsOpError("NOT_FOUND", `no such path: ${abs}`);
    throw new FsOpError("STAT_FAILED", `${err.code}: ${abs}`);
  }
}

export function listTarget(root, target) {
  const abs = assertInside(root, target);
  const st = statOrThrow(abs);
  if (!st.isDirectory()) {
    throw new FsOpError("NOT_A_DIRECTORY", `not a directory: ${abs}`);
  }
  const real = fs.realpathSync(abs);
  if (!isInside(fs.realpathSync(root), real)) {
    throw new FsOpError("PATH-ESCAPE", `directory resolves outside the root: ${abs}`);
  }
  const entries = fs
    .readdirSync(abs, { withFileTypes: true })
    .map((d) => {
      let size = null;
      try {
        size = fs.statSync(path.join(abs, d.name)).size;
      } catch {
        size = null;
      }
      return { name: d.name, type: d.isDirectory() ? "dir" : d.isFile() ? "file" : "other", size };
    })
    .sort((a, b) => a.name.localeCompare(b.name));
  return { kind: "dir", path: abs, count: entries.length, entries };
}

export function readTarget(root, target, { maxBytes = MAX_READ_BYTES } = {}) {
  const abs = assertInside(root, target);
  const st = statOrThrow(abs);
  if (st.isDirectory()) return listTarget(root, target);
  const real = fs.realpathSync(abs);
  if (!isInside(fs.realpathSync(root), real)) {
    throw new FsOpError("PATH-ESCAPE", `file resolves outside the root: ${abs}`);
  }
  const fd = fs.openSync(abs, "r");
  try {
    const size = Math.min(st.size, maxBytes);
    const buf = Buffer.alloc(size);
    const read = fs.readSync(fd, buf, 0, size, 0);
    const data = buf.subarray(0, read);
    return {
      kind: "file",
      path: abs,
      bytes: st.size,
      sha256: sha256Hex(data),
      encoding: "utf8",
      truncated: st.size > read,
      content: data.toString("utf8"),
    };
  } finally {
    fs.closeSync(fd);
  }
}

function countOccurrences(haystack, needle) {
  if (needle === "") return 0;
  let count = 0;
  let index = haystack.indexOf(needle);
  while (index !== -1) {
    count += 1;
    index = haystack.indexOf(needle, index + needle.length);
  }
  return count;
}

export function writeTarget(root, target, content) {
  if (typeof content !== "string") {
    throw new FsOpError("INVALID_CONTENT", "tool_input.content (string) is required for write");
  }
  const abs = assertInside(root, target);
  fs.mkdirSync(path.dirname(abs), { recursive: true });
  const real = fs.realpathSync(path.dirname(abs));
  if (!isInside(fs.realpathSync(root), real)) {
    throw new FsOpError("PATH-ESCAPE", `target directory resolves outside the root: ${abs}`);
  }
  fs.writeFileSync(abs, content, "utf8");
  return {
    kind: "write",
    path: abs,
    bytes: Buffer.byteLength(content, "utf8"),
    sha256: sha256Hex(content),
  };
}

export function editTarget(root, target, toolInput = {}) {
  const abs = assertInside(root, target);
  statOrThrow(abs);
  const current = fs.readFileSync(abs, "utf8");
  if (typeof toolInput.old_string === "string") {
    const occurrences = countOccurrences(current, toolInput.old_string);
    if (occurrences !== 1) {
      throw new FsOpError("EDIT_AMBIGUOUS", `old_string occurs ${occurrences} time(s); exactly 1 required`);
    }
    const next = current.replace(toolInput.old_string, toolInput.new_string ?? "");
    fs.writeFileSync(abs, next, "utf8");
    return {
      kind: "edit",
      path: abs,
      mode: "replace",
      replaced: 1,
      bytes: Buffer.byteLength(next, "utf8"),
      sha256: sha256Hex(next),
    };
  }
  if (typeof toolInput.content === "string") {
    fs.writeFileSync(abs, toolInput.content, "utf8");
    return {
      kind: "edit",
      path: abs,
      mode: "overwrite",
      replaced: 0,
      bytes: Buffer.byteLength(toolInput.content, "utf8"),
      sha256: sha256Hex(toolInput.content),
    };
  }
  throw new FsOpError("INVALID_CONTENT", "edit requires tool_input.old_string (unique) or tool_input.content");
}

// Fixed, non-parameterised, read-only command. Not an arbitrary exec surface.
export function gitStatus(root) {
  const res = spawnSync("git", ["status", "--porcelain=v1", "-b"], {
    cwd: root,
    encoding: "utf8",
    timeout: 15000,
    shell: false,
    windowsHide: true,
    maxBuffer: 4 << 20,
  });
  if (res.error) {
    const code = res.error.code === "ENOENT" ? "GIT_NOT_FOUND" : "GIT_FAILED";
    throw new FsOpError(code, `git status failed: ${res.error.code ?? ""} ${res.error.message ?? ""}`.trim());
  }
  const stdout = String(res.stdout ?? "");
  return {
    kind: "git_status",
    command: "git status --porcelain=v1 -b",
    exit_code: res.status,
    branch: stdout.split(/\r?\n/)[0] ?? null,
    stdout: stdout.slice(0, 65536),
    stderr: String(res.stderr ?? "").slice(0, 8192),
    truncated: stdout.length > 65536,
  };
}

export function requireGitRepo(root) {
  if (!fs.existsSync(path.join(root, ".git"))) {
    throw new FsOpError("NOT_A_GIT_REPO", `no .git directory under ${root}`);
  }
}

import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import {
  assertInside,
  editTarget,
  listTarget,
  MAX_EDIT_BYTES,
  readTarget,
  writeTarget,
} from "../src/integration/autoclaw/fs-ops.mjs";

function makeRoot() {
  return fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "aces-fsops-")));
}

function throwsCode(fn, code) {
  assert.throws(fn, (err) => err.code === code, `expected ${code}`);
}

test("assertInside accepts paths inside the root and rejects escapes", () => {
  const root = makeRoot();
  assert.equal(assertInside(root, "a.txt"), path.join(root, "a.txt"));
  throwsCode(() => assertInside(root, "../outside.txt"), "PATH-ESCAPE");
  throwsCode(() => assertInside(root, "..\\outside.txt"), "PATH-ESCAPE");
});

test("write/read roundtrip inside the root", () => {
  const root = makeRoot();
  const written = writeTarget(root, "dir/note.txt", "hello");
  assert.equal(written.kind, "write");
  const out = readTarget(root, "dir/note.txt");
  assert.equal(out.content, "hello");
  assert.equal(out.truncated, false);
  const listing = listTarget(root, "dir");
  assert.equal(listing.kind, "dir");
  assert.ok(listing.entries.some((e) => e.name === "note.txt"));
});

test("read truncates at maxBytes and reports it", () => {
  const root = makeRoot();
  writeTarget(root, "big.txt", "x".repeat(1000));
  const out = readTarget(root, "big.txt", { maxBytes: 10 });
  assert.equal(out.truncated, true);
  assert.equal(out.content.length, 10);
});

test("edit replace keeps $-patterns in new_string literal (regression)", () => {
  const root = makeRoot();
  writeTarget(root, "f.txt", "alpha beta");
  editTarget(root, "f.txt", { old_string: "beta", new_string: "beta$&$'`tail" });
  const out = readTarget(root, "f.txt");
  assert.equal(out.content, "alpha beta$&$'`tail");
});

test("edit overwrite mode works and edit requires content", () => {
  const root = makeRoot();
  writeTarget(root, "f.txt", "old");
  editTarget(root, "f.txt", { content: "new" });
  assert.equal(readTarget(root, "f.txt").content, "new");
  throwsCode(() => editTarget(root, "f.txt", {}), "INVALID_CONTENT");
});

test("edit rejects ambiguous and missing old_string", () => {
  const root = makeRoot();
  writeTarget(root, "f.txt", "abab");
  throwsCode(() => editTarget(root, "f.txt", { old_string: "ab", new_string: "c" }), "EDIT_AMBIGUOUS");
  throwsCode(() => editTarget(root, "f.txt", { old_string: "missing", new_string: "c" }), "EDIT_AMBIGUOUS");
  throwsCode(() => editTarget(root, "nope.txt", { old_string: "x", new_string: "y" }), "NOT_FOUND");
});

test("edit refuses files above MAX_EDIT_BYTES", () => {
  const root = makeRoot();
  writeTarget(root, "huge.txt", "x".repeat(MAX_EDIT_BYTES + 1));
  throwsCode(() => editTarget(root, "huge.txt", { old_string: "x", new_string: "y" }), "FILE_TOO_LARGE");
});

test("writes through a symlink escaping the root are rejected", (t) => {
  const root = makeRoot();
  const outside = fs.mkdtempSync(path.join(os.tmpdir(), "aces-outside-"));
  const outsideFile = path.join(outside, "secret.txt");
  fs.writeFileSync(outsideFile, "secret", "utf8");
  t.after(() => {
    try {
      fs.rmSync(outside, { recursive: true, force: true });
    } catch {}
  });
  let link;
  try {
    link = path.join(root, "link.txt");
    fs.symlinkSync(outsideFile, link, "file");
  } catch {
    return; // symlink privilege unavailable (Windows without Developer Mode)
  }
  throwsCode(() => writeTarget(root, "link.txt", "clobbered"), "PATH-ESCAPE");
  assert.equal(fs.readFileSync(outsideFile, "utf8"), "secret");
  throwsCode(() => readTarget(root, "link.txt"), "PATH-ESCAPE");
  throwsCode(() => editTarget(root, "link.txt", { old_string: "secret", new_string: "x" }), "PATH-ESCAPE");
  assert.equal(fs.readFileSync(outsideFile, "utf8"), "secret");
});

test("write requires string content", () => {
  const root = makeRoot();
  throwsCode(() => writeTarget(root, "f.txt", undefined), "INVALID_CONTENT");
});

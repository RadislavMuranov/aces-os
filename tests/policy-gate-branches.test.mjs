// Deny-branch tests for the policy gate. Each case uses a stub engine under
// tests/fixtures/hooks/ so no repository journal or real engine is touched.
import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { createPolicyGate } from "../src/integration/autoclaw/policy-gate.mjs";

const FIXTURES = path.resolve(import.meta.dirname, "fixtures", "hooks");

function makeRoot() {
  const root = fs.realpathSync(fs.mkdtempSync(path.join(os.tmpdir(), "aces-gate-")));
  fs.mkdirSync(path.join(root, ".claude", "hooks"), { recursive: true });
  return root;
}

function gate(root, engineName, timeoutMs = 5000) {
  return createPolicyGate({
    repoRoot: root,
    enginePath: path.join(FIXTURES, engineName),
    timeoutMs,
    execEnabled: false,
  });
}

test("EXEC_DISABLED is denied before any engine call", async () => {
  const root = makeRoot();
  const g = gate(root, "sleep-engine.mjs");
  const res = await g.check({ kind: "exec", target: "echo hi" });
  assert.equal(res.decision, "deny");
  assert.equal(res.rule_id, "EXEC_DISABLED");
});

test("unmapped op kinds are denied", async () => {
  const root = makeRoot();
  const g = gate(root, "sleep-engine.mjs");
  const res = await g.check({ kind: "teleport", target: "README.md" });
  assert.equal(res.decision, "deny");
  assert.equal(res.rule_id, "ACES-UNMAPPED-OP");
});

test("POLICY-TIMEOUT when the engine exceeds the deadline", async () => {
  const root = makeRoot();
  const g = gate(root, "sleep-engine.mjs", 50);
  const res = await g.check({ kind: "read", target: "README.md" });
  assert.equal(res.decision, "deny");
  assert.equal(res.rule_id, "POLICY-TIMEOUT");
});

test("ENGINE-FAILED when the engine exits non-zero", async () => {
  const root = makeRoot();
  const g = gate(root, "fail-engine.mjs");
  const res = await g.check({ kind: "read", target: "README.md" });
  assert.equal(res.decision, "deny");
  assert.equal(res.rule_id, "ENGINE-FAILED");
});

test("ENGINE-NO-JOURNAL when the engine writes no journal row", async () => {
  const root = makeRoot();
  const g = gate(root, "no-journal-engine.mjs");
  const res = await g.check({ kind: "read", target: "README.md" });
  assert.equal(res.decision, "deny");
  assert.equal(res.rule_id, "ENGINE-NO-JOURNAL");
});

test("ENGINE-BAD-OUTPUT when stdout is not JSON", async () => {
  const root = makeRoot();
  const g = gate(root, "bad-output-engine.mjs");
  const res = await g.check({ kind: "read", target: "README.md" });
  assert.equal(res.decision, "deny");
  assert.equal(res.rule_id, "ENGINE-BAD-OUTPUT");
});

test("ENGINE-BAD-OUTPUT on journal/stdout decision mismatch", async () => {
  const root = makeRoot();
  const g = gate(root, "mismatch-engine.mjs");
  const res = await g.check({ kind: "read", target: "README.md" });
  assert.equal(res.decision, "deny");
  assert.equal(res.rule_id, "ENGINE-BAD-OUTPUT");
  assert.match(res.reason, /refusing to guess/);
});

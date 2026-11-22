import assert from "node:assert/strict";
import test from "node:test";
import {
  evaluateAuthPrompt,
  runAuthPromptIfAllowed,
} from "../src/diagnostics/authentication-evidence-guard.ts";

const signedIn = {
  target: "grok.com",
  result: "SIGNED_IN" as const,
  checkedAt: "2026-10-22T10:00:00.000Z",
  evidenceRef: "live-check-001",
};
const freshFailure = {
  target: "grok.com",
  result: "LOGIN_WALL" as const,
  observedAt: "2026-10-22T10:01:00.000Z",
  evidenceRef: "live-failure-002",
};

test("suppresses another auth prompt after successful live check", () => {
  assert.deepEqual(evaluateAuthPrompt("grok.com", signedIn, null), {
    decision: "SUPPRESS", reason: "RECENT_LIVE_CHECK_SIGNED_IN",
  });
});
test("profile inventory absence is not failure evidence", () => {
  assert.equal(evaluateAuthPrompt("grok.com", signedIn, null).decision, "SUPPRESS");
});
test("allows prompt only after newer direct failure evidence", () => {
  assert.deepEqual(evaluateAuthPrompt("grok.com", signedIn, freshFailure), {
    decision: "ALLOW", reason: "FRESH_DIRECT_AUTH_FAILURE",
  });
});
test("blocks stale failure evidence", () => {
  assert.equal(evaluateAuthPrompt("grok.com", signedIn, {
    ...freshFailure, observedAt: "2026-10-22T09:59:00.000Z",
  }).decision, "SUPPRESS");
});
test("blocks evidence for another target", () => {
  assert.equal(evaluateAuthPrompt("grok.com", signedIn, {
    ...freshFailure, target: "example.com",
  }).decision, "BLOCK");
});
test("blocks when neither live check nor direct failure exists", () => {
  assert.deepEqual(evaluateAuthPrompt("grok.com", null, null), {
    decision: "BLOCK", reason: "UNKNOWN_OR_INSUFFICIENT_EVIDENCE",
  });
});
test("blocks malformed timestamps and missing evidence references", () => {
  assert.equal(evaluateAuthPrompt("grok.com", {
    ...signedIn, checkedAt: "not-a-date",
  }, null).decision, "BLOCK");
  assert.equal(evaluateAuthPrompt("grok.com", signedIn, {
    ...freshFailure, evidenceRef: "",
  }).decision, "BLOCK");
});
test("same-time failure does not override successful live check", () => {
  assert.equal(evaluateAuthPrompt("grok.com", signedIn, {
    ...freshFailure, observedAt: signedIn.checkedAt,
  }).decision, "SUPPRESS");
});
test("enforcement seam does not invoke prompt callback after successful live check", () => {
  let calls = 0;
  const result = runAuthPromptIfAllowed("grok.com", signedIn, null, () => ++calls);
  assert.equal(result.promptRequested, false);
  assert.equal(calls, 0);
});
test("enforcement seam invokes prompt callback for fresh direct failure", () => {
  let calls = 0;
  const result = runAuthPromptIfAllowed("grok.com", signedIn, freshFailure, () => ++calls);
  assert.equal(result.promptRequested, true);
  assert.equal("result" in result ? result.result : undefined, 1);
  assert.equal(calls, 1);
});

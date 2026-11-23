import assert from "node:assert/strict";
import test from "node:test";
import { decideVerifiedTransition } from "../src/acceptance/transition-decision.ts";
import {
  acceptVerifiedTransition,
  type AcceptanceBinding,
  type AuthorityAcceptance,
  type StateTransition,
  type VerificationResult,
} from "../src/acceptance/accept-verified-transition.ts";

const transition: StateTransition = {
  transition_ref: "transition-1",
  canonical_ref: "canonical-1",
  has_history: true,
};
const verification: VerificationResult = {
  status: "PASS",
  verification_context_ref: "verification-1",
};
const binding: AcceptanceBinding = {
  canonical_ref: "canonical-1",
  authority_ref: "authority-1",
  capability_ref: "capability-1",
  policy_ref: "policy-1",
  verification_context_ref: "verification-1",
};
const authority: AuthorityAcceptance = {
  accepted: true,
  authority_ref: "authority-1",
  capability_ref: "capability-1",
  policy_ref: "policy-1",
};

test("accepts a fully bound verified transition as ACCEPTED decision", () => {
  const result = decideVerifiedTransition(transition, verification, binding, authority);
  assert.equal(result.accepted, true);
  assert.ok(result.accepted && result.decision.state === "ACCEPTED");
  if (result.accepted) {
    assert.equal(result.decision.canonical_ref, "canonical-1");
    assert.equal(result.decision.transition_ref, "transition-1");
    assert.deepEqual(result.decision.acceptance_binding, binding);
  }
});

test("rejects missing history as MISSING_HISTORY", () => {
  const result = decideVerifiedTransition(
    { ...transition, has_history: false },
    verification,
    binding,
    authority,
  );
  assert.equal(result.accepted, false);
  assert.ok(!result.accepted && result.reason === "MISSING_HISTORY");
});

test("rejects verification FAIL as VERIFICATION_FAIL", () => {
  const result = decideVerifiedTransition(
    transition,
    { status: "FAIL", verification_context_ref: "verification-1" },
    binding,
    authority,
  );
  assert.equal(result.accepted, false);
  assert.ok(!result.accepted && result.reason === "VERIFICATION_FAIL");
});

test("rejects null binding as MISSING_BINDING", () => {
  const result = decideVerifiedTransition(transition, verification, null, authority);
  assert.equal(result.accepted, false);
  assert.ok(!result.accepted && result.reason === "MISSING_BINDING");
});

test("rejects empty binding ref as EMPTY_BINDING_REF with field", () => {
  const result = decideVerifiedTransition(
    transition,
    verification,
    { ...binding, policy_ref: "" },
    authority,
  );
  assert.equal(result.accepted, false);
  assert.ok(!result.accepted && result.reason === "EMPTY_BINDING_REF");
  if (!result.accepted) {
    assert.equal(result.field, "policy_ref");
  }
});

test("rejects denied authority as AUTHORITY_DENY", () => {
  const result = decideVerifiedTransition(transition, verification, binding, {
    accepted: false,
  });
  assert.equal(result.accepted, false);
  assert.ok(!result.accepted && result.reason === "AUTHORITY_DENY");
});

test("treats unknown policy evaluation as deny (AUTHORITY_DENY)", () => {
  const unknown = { accepted: false } as AuthorityAcceptance;
  const result = decideVerifiedTransition(transition, verification, binding, unknown);
  assert.equal(result.accepted, false);
  assert.ok(!result.accepted && result.reason === "AUTHORITY_DENY");
});

for (const field of [
  "canonical_ref",
  "authority_ref",
  "capability_ref",
  "policy_ref",
  "verification_context_ref",
] as const) {
  test(`rejects every cross-boundary mismatch as BINDING_MISMATCH (${field})`, () => {
    const mismatched = { ...binding, [field]: "other-" + field };
    const result = decideVerifiedTransition(transition, verification, mismatched, authority);
    assert.equal(result.accepted, false);
    assert.ok(!result.accepted && result.reason === "BINDING_MISMATCH");
    if (!result.accepted) {
      assert.equal(result.field, field);
    }
  });
}

test("delegated core keeps accept path identical to acceptVerifiedTransition", () => {
  const direct = acceptVerifiedTransition(transition, verification, binding, authority);
  const result = decideVerifiedTransition(transition, verification, binding, authority);
  assert.ok(result.accepted);
  assert.ok(direct !== null);
  if (result.accepted) {
    assert.deepEqual(result.decision, direct);
  }
});

test("fail-closed: core rejection after passing guards yields EVALUATION_ERROR", () => {
  const result = decideVerifiedTransition(
    transition,
    verification,
    binding,
    authority,
    () => null,
  );
  assert.equal(result.accepted, false);
  assert.ok(!result.accepted && result.reason === "EVALUATION_ERROR");
  if (!result.accepted) {
    assert.match(result.detail, /fail-closed/);
  }
});

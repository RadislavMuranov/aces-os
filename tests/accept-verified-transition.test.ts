import assert from "node:assert/strict";
import test from "node:test";
import { acceptVerifiedTransition } from "../src/acceptance/accept-verified-transition.ts";

const transition = {
  transition_ref: "transition-1",
  canonical_ref: "canonical-1",
  has_history: true,
};

const verification = {
  status: "PASS" as const,
  verification_context_ref: "verification-1",
};

const binding = {
  canonical_ref: "canonical-1",
  authority_ref: "authority-1",
  capability_ref: "capability-1",
  policy_ref: "policy-1",
  verification_context_ref: "verification-1",
};

const authority = {
  accepted: true as const,
  authority_ref: "authority-1",
  capability_ref: "capability-1",
  policy_ref: "policy-1",
};

test("accepts only a fully bound verified transition", () => {
  const accepted = acceptVerifiedTransition(
    transition,
    verification,
    binding,
    authority,
  );

  assert.equal(accepted?.state, "ACCEPTED");
  assert.equal(accepted?.transition_ref, "transition-1");
  assert.deepEqual(accepted?.acceptance_binding, binding);
});

test("rejects missing history", () => {
  assert.equal(
    acceptVerifiedTransition(
      { ...transition, has_history: false },
      verification,
      binding,
      authority,
    ),
    null,
  );
});

test("rejects verification failure", () => {
  assert.equal(
    acceptVerifiedTransition(
      transition,
      { status: "FAIL", verification_context_ref: "verification-1" },
      binding,
      authority,
    ),
    null,
  );
});

test("rejects missing binding or authority acceptance", () => {
  assert.equal(
    acceptVerifiedTransition(transition, verification, null, authority),
    null,
  );
  assert.equal(
    acceptVerifiedTransition(
      transition,
      verification,
      binding,
      { accepted: false },
    ),
    null,
  );
});

test("rejects empty acceptance binding references", () => {
  const emptyRefs = [
    { ...binding, canonical_ref: "" },
    { ...binding, authority_ref: "" },
    { ...binding, capability_ref: "" },
    { ...binding, policy_ref: "" },
    { ...binding, verification_context_ref: "" },
  ];

  for (const invalidBinding of emptyRefs) {
    assert.equal(
      acceptVerifiedTransition(transition, verification, invalidBinding, authority),
      null,
    );
  }
});

test("rejects every cross-boundary reference mismatch", () => {
  const mismatches = [
    { ...binding, canonical_ref: "canonical-2" },
    { ...binding, authority_ref: "authority-2" },
    { ...binding, capability_ref: "capability-2" },
    { ...binding, policy_ref: "policy-2" },
    { ...binding, verification_context_ref: "verification-2" },
  ];

  for (const mismatchedBinding of mismatches) {
    assert.equal(
      acceptVerifiedTransition(
        transition,
        verification,
        mismatchedBinding,
        authority,
      ),
      null,
    );
  }
});

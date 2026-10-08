import assert from "node:assert/strict";
import test from "node:test";
import {
  validateControlRecord,
  type ControlRecord,
} from "../src/control/control-record.ts";

const validRecord: ControlRecord = {
  mission_id: "mission-1",
  gate_id: "G0",
  work_item_id: "work-1",
  action_id: "action-1",
  source_set: ["source-1"],
  observation: "Observed repository state.",
  evidence: "Direct source inspection.",
  epistemic_state: "OBSERVED",
  scope: "repository implementation surface",
  limitation: "No runtime integration evidence.",
  conclusion: "Record satisfies the minimum control contract.",
  dependencies: [
    {
      dependency_id: "dependency-1",
      state: "VERIFIED",
      scope: "FULL",
    },
  ],
};

test("accepts a complete minimally admissible control record", () => {
  assert.deepEqual(validateControlRecord(validRecord), { valid: true });
});

test("rejects missing mission traceability", () => {
  const invalid = { ...validRecord, mission_id: "" };

  assert.deepEqual(validateControlRecord(invalid), {
    valid: false,
    reason: "INVALID_MISSION_TRACEABILITY",
  });
});

test("rejects evidence without source lineage", () => {
  const invalid = { ...validRecord, source_set: [] };

  assert.deepEqual(validateControlRecord(invalid), {
    valid: false,
    reason: "INVALID_EVIDENCE_LINEAGE",
  });
});

test("rejects UNKNOWN without complete disposition", () => {
  const invalid = {
    ...validRecord,
    epistemic_state: "UNKNOWN" as const,
  };

  assert.deepEqual(validateControlRecord(invalid), {
    valid: false,
    reason: "UNKNOWN_WITHOUT_DISPOSITION",
  });
});

test("accepts UNKNOWN with complete disposition", () => {
  const valid = {
    ...validRecord,
    epistemic_state: "UNKNOWN" as const,
    unknown_disposition: {
      cause: "Runtime evidence unavailable.",
      impact: "System-wide enforcement remains unverified.",
      required_evidence: "Runtime execution trace.",
      blocks: "G0 promotion.",
      next_action: "Acquire runtime evidence.",
      disposition: "BLOCKED_PENDING_EVIDENCE",
    },
  };

  assert.deepEqual(validateControlRecord(valid), { valid: true });
});

test("rejects UNKNOWN or BLOCKED dependencies", () => {
  for (const state of ["UNKNOWN", "BLOCKED"] as const) {
    const invalid = {
      ...validRecord,
      dependencies: [
        {
          dependency_id: "dependency-1",
          state,
          scope: "RESTRICTED" as const,
        },
      ],
    };

    assert.deepEqual(validateControlRecord(invalid), {
      valid: false,
      reason: "INVALID_DEPENDENCY_ADMISSIBILITY",
    });
  }
});

test("requires restricted scope for partially verified dependencies", () => {
  const invalid = {
    ...validRecord,
    dependencies: [
      {
        dependency_id: "dependency-1",
        state: "PARTIALLY_VERIFIED" as const,
        scope: "FULL" as const,
      },
    ],
  };

  assert.deepEqual(validateControlRecord(invalid), {
    valid: false,
    reason: "INVALID_DEPENDENCY_ADMISSIBILITY",
  });
});

test("does not promote VALID into acceptance or authorization", () => {
  const result = validateControlRecord(validRecord);

  assert.deepEqual(result, { valid: true });
  assert.equal("state" in result, false);
  assert.equal("accepted" in result, false);
  assert.equal("authorized" in result, false);
});

import assert from "node:assert/strict";
import test from "node:test";
import {
  authorizePreActionStateChange,
  type PreActionStateChangeRequest,
} from "../src/control/pre-action-state-change-gate.ts";

const authorization = {
  accepted: true,
  authority_ref: "authority-1",
  capability_ref: "capability-1",
  policy_ref: "policy-1",
  request_binding_ref: "request-1",
  target_ref: "notion-page-1",
  destination_ref: "notion-page-1",
};

const readyRequest: PreActionStateChangeRequest = {
  action_ref: "action-1",
  request_binding_ref: "request-1",
  execution_path_ref: "connector-1",
  target_ref: "notion-page-1",
  destination_ref: "notion-page-1",
  target_readiness: "READY",
  destination_readiness: "READY",
  parameter_source: "EXPLICIT",
  parameter_provenance_ref: "provenance-1",
  authorization,
};

test("allows only a fully bound pre-action state change", () => {
  assert.deepEqual(authorizePreActionStateChange(readyRequest), {
    allowed: true,
    action_ref: "action-1",
    request_binding_ref: "request-1",
  });
});

test("blocks missing or ambiguous destinations before any action", () => {
  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      destination_ref: null,
      destination_readiness: "MISSING",
    }).reason,
    "MISSING_DESTINATION",
  );
  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      destination_readiness: "AMBIGUOUS",
    }).reason,
    "INVALID_DESTINATION",
  );
});

test("blocks defaults, inference, fallback, stale, and unknown parameter sources", () => {
  const unsafeSources = [
    "DEFAULT",
    "INFERRED",
    "FALLBACK",
    "STALE",
    "UNKNOWN",
  ] as const;

  for (const parameter_source of unsafeSources) {
    assert.equal(
      authorizePreActionStateChange({
        ...readyRequest,
        parameter_source,
      }).allowed,
      false,
    );
  }
});

test("blocks missing parameter provenance", () => {
  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      parameter_provenance_ref: "",
    }).reason,
    "MISSING_PARAMETER_PROVENANCE",
  );
});

test("blocks retry and recovery when the request binding is stale", () => {
  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      request_binding_ref: "request-2",
      execution_path_ref: "retry-1",
    }).reason,
    "INVALID_AUTHORIZATION_BINDING",
  );
  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      request_binding_ref: "request-2",
      execution_path_ref: "recovery-1",
    }).reason,
    "INVALID_AUTHORIZATION_BINDING",
  );
});

test("blocks missing or invalid authorization", () => {
  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      authorization: null,
    }).reason,
    "MISSING_AUTHORIZATION",
  );

  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      authorization: {
        ...authorization,
        request_binding_ref: "request-2",
      },
    }).reason,
    "INVALID_AUTHORIZATION_BINDING",
  );
});

test("binds authorization to the exact target and destination", () => {
  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      authorization: {
        ...authorization,
        target_ref: "notion-page-2",
      },
    }).reason,
    "INVALID_AUTHORIZATION_BINDING",
  );
  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      authorization: {
        ...authorization,
        destination_ref: "notion-page-2",
      },
    }).reason,
    "INVALID_AUTHORIZATION_BINDING",
  );
});

test("blocks invalid target state even when authorization exists", () => {
  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      target_readiness: "STALE",
    }).reason,
    "INVALID_TARGET",
  );
});

test("blocks incomplete authorization references", () => {
  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      authorization: {
        ...authorization,
        policy_ref: "",
      },
    }).reason,
    "INVALID_AUTHORIZATION_BINDING",
  );
});

test("requires the gate for every execution path", () => {
  const executionPaths = [
    "connector-1",
    "fallback-1",
    "retry-1",
    "recovery-1",
    "api-1",
    "cli-1",
    "mcp-1",
  ];

  for (const execution_path_ref of executionPaths) {
    assert.equal(
      authorizePreActionStateChange({
        ...readyRequest,
        execution_path_ref,
      }).allowed,
      true,
    );
  }

  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      execution_path_ref: "",
    }).reason,
    "MISSING_EXECUTION_PATH",
  );
});

test("blocks absent target even when destination and authorization are present", () => {
  assert.equal(
    authorizePreActionStateChange({
      ...readyRequest,
      target_ref: null,
      target_readiness: "MISSING",
    }).reason,
    "MISSING_TARGET",
  );
});

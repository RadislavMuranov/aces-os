export type StateChangeParameterSource =
  | "EXPLICIT"
  | "AUTHORIZED"
  | "INFERRED"
  | "DEFAULT"
  | "FALLBACK"
  | "STALE"
  | "UNKNOWN";

export type StateChangeReadiness =
  | "READY"
  | "MISSING"
  | "AMBIGUOUS"
  | "STALE"
  | "MISMATCHED";

export interface StateChangeAuthorization {
  accepted: boolean;
  authority_ref: string;
  capability_ref: string;
  policy_ref: string;
  request_binding_ref: string;
  target_ref: string;
  destination_ref: string;
}

export interface PreActionStateChangeRequest {
  action_ref: string;
  request_binding_ref: string;
  execution_path_ref: string;
  target_ref: string | null;
  destination_ref: string | null;
  target_readiness: StateChangeReadiness;
  destination_readiness: StateChangeReadiness;
  parameter_source: StateChangeParameterSource;
  parameter_provenance_ref: string;
  authorization: StateChangeAuthorization | null;
}

export type PreActionGateDecision =
  | {
      allowed: true;
      action_ref: string;
      request_binding_ref: string;
    }
  | {
      allowed: false;
      reason:
        | "MISSING_ACTION"
        | "MISSING_REQUEST_BINDING"
        | "MISSING_EXECUTION_PATH"
        | "MISSING_TARGET"
        | "INVALID_TARGET"
        | "MISSING_DESTINATION"
        | "INVALID_DESTINATION"
        | "UNSAFE_PARAMETER_SOURCE"
        | "MISSING_PARAMETER_PROVENANCE"
        | "MISSING_AUTHORIZATION"
        | "INVALID_AUTHORIZATION_BINDING";
    };

const SAFE_PARAMETER_SOURCES = new Set<StateChangeParameterSource>([
  "EXPLICIT",
  "AUTHORIZED",
]);

export function authorizePreActionStateChange(
  request: PreActionStateChangeRequest,
): PreActionGateDecision {
  if (request.action_ref.length === 0) {
    return { allowed: false, reason: "MISSING_ACTION" };
  }

  if (request.request_binding_ref.length === 0) {
    return { allowed: false, reason: "MISSING_REQUEST_BINDING" };
  }

  if (request.execution_path_ref.length === 0) {
    return { allowed: false, reason: "MISSING_EXECUTION_PATH" };
  }

  if (!request.target_ref || request.target_ref.length === 0) {
    return { allowed: false, reason: "MISSING_TARGET" };
  }

  if (request.target_readiness !== "READY") {
    return { allowed: false, reason: "INVALID_TARGET" };
  }

  if (!request.destination_ref || request.destination_ref.length === 0) {
    return { allowed: false, reason: "MISSING_DESTINATION" };
  }

  if (request.destination_readiness !== "READY") {
    return { allowed: false, reason: "INVALID_DESTINATION" };
  }

  if (!SAFE_PARAMETER_SOURCES.has(request.parameter_source)) {
    return { allowed: false, reason: "UNSAFE_PARAMETER_SOURCE" };
  }

  if (request.parameter_provenance_ref.length === 0) {
    return { allowed: false, reason: "MISSING_PARAMETER_PROVENANCE" };
  }

  const authorization = request.authorization;
  if (!authorization?.accepted) {
    return { allowed: false, reason: "MISSING_AUTHORIZATION" };
  }

  if (
    authorization.request_binding_ref !== request.request_binding_ref ||
    authorization.target_ref !== request.target_ref ||
    authorization.destination_ref !== request.destination_ref ||
    authorization.authority_ref.length === 0 ||
    authorization.capability_ref.length === 0 ||
    authorization.policy_ref.length === 0
  ) {
    return { allowed: false, reason: "INVALID_AUTHORIZATION_BINDING" };
  }

  return {
    allowed: true,
    action_ref: request.action_ref,
    request_binding_ref: request.request_binding_ref,
  };
}

import {
  acceptVerifiedTransition,
  type AcceptanceBinding,
  type AcceptedState,
  type AuthorityAcceptance,
  type StateTransition,
  type VerificationResult,
} from "./accept-verified-transition.ts";

// AOC-001 rejection taxonomy. Reasons are ordered to mirror the guard
// sequence of acceptVerifiedTransition exactly; the accept path delegates
// to that function, so this contract cannot drift from the core code.
export type TransitionRejectionReason =
  | "MISSING_HISTORY"
  | "VERIFICATION_FAIL"
  | "MISSING_BINDING"
  | "EMPTY_BINDING_REF"
  | "AUTHORITY_DENY"
  | "BINDING_MISMATCH"
  | "EVALUATION_ERROR";

export interface TransitionRejection {
  accepted: false;
  reason: TransitionRejectionReason;
  // Set only for BINDING_MISMATCH: the binding field that broke correlation.
  field?: string;
  detail: string;
}

export type TransitionDecision =
  | { accepted: true; decision: AcceptedState }
  | TransitionRejection;

function reject(
  reason: TransitionRejectionReason,
  detail: string,
  field?: string,
): TransitionRejection {
  return field === undefined
    ? { accepted: false, reason, detail }
    : { accepted: false, reason, field, detail };
}

// Pure decision wrapper: no I/O, no external side effects. A failure result
// never grants permission; unknown or incomplete policy evaluation must be
// modeled upstream as accepted:false, which lands here as AUTHORITY_DENY.
export function decideVerifiedTransition(
  transition: StateTransition,
  verification: VerificationResult,
  binding: AcceptanceBinding | null,
  authority: AuthorityAcceptance,
  core: typeof acceptVerifiedTransition = acceptVerifiedTransition,
): TransitionDecision {
  if (!transition.has_history) {
    return reject("MISSING_HISTORY", "transition carries no history evidence");
  }
  if (verification.status !== "PASS") {
    return reject("VERIFICATION_FAIL", "verification did not return PASS");
  }
  if (!binding) {
    return reject("MISSING_BINDING", "no acceptance binding supplied");
  }
  const emptyField = Object.entries(binding).find(
    ([, ref]) => ref.length === 0,
  );
  if (emptyField) {
    return reject(
      "EMPTY_BINDING_REF",
      `binding field ${emptyField[0]} is empty`,
      emptyField[0],
    );
  }
  if (!authority.accepted) {
    return reject(
      "AUTHORITY_DENY",
      "authority (capability/policy) did not accept; unknown evaluation is deny",
    );
  }
  if (binding.canonical_ref !== transition.canonical_ref) {
    return reject(
      "BINDING_MISMATCH",
      "binding canonical_ref does not match transition",
      "canonical_ref",
    );
  }
  if (binding.authority_ref !== authority.authority_ref) {
    return reject(
      "BINDING_MISMATCH",
      "binding authority_ref does not match authority",
      "authority_ref",
    );
  }
  if (binding.capability_ref !== authority.capability_ref) {
    return reject(
      "BINDING_MISMATCH",
      "binding capability_ref does not match authority",
      "capability_ref",
    );
  }
  if (binding.policy_ref !== authority.policy_ref) {
    return reject(
      "BINDING_MISMATCH",
      "binding policy_ref does not match authority",
      "policy_ref",
    );
  }
  if (binding.verification_context_ref !== verification.verification_context_ref) {
    return reject(
      "BINDING_MISMATCH",
      "binding verification_context_ref does not match verification",
      "verification_context_ref",
    );
  }
  const accepted = core(transition, verification, binding, authority);
  if (!accepted) {
    return reject(
      "EVALUATION_ERROR",
      "guards passed but core acceptance rejected; treat as fail-closed",
    );
  }
  return { accepted: true, decision: accepted };
}

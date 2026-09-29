export type VerificationResult =
  | {
      status: "PASS";
      verification_context_ref: string;
    }
  | {
      status: "FAIL";
      verification_context_ref: string;
    };

export type AuthorityAcceptance =
  | {
      accepted: true;
      authority_ref: string;
      capability_ref: string;
      policy_ref: string;
    }
  | {
      accepted: false;
    };

export interface StateTransition {
  transition_ref: string;
  canonical_ref: string;
  has_history: boolean;
}

export interface AcceptanceBinding {
  canonical_ref: string;
  authority_ref: string;
  capability_ref: string;
  policy_ref: string;
  verification_context_ref: string;
}

export interface AcceptedState {
  state: "ACCEPTED";
  canonical_ref: string;
  transition_ref: string;
  acceptance_binding: AcceptanceBinding;
}

export function acceptVerifiedTransition(
  transition: StateTransition,
  verification: VerificationResult,
  binding: AcceptanceBinding | null,
  authority: AuthorityAcceptance,
): AcceptedState | null {
  if (!transition.has_history) return null;
  if (verification.status !== "PASS") return null;
  if (!binding) return null;
  if (Object.values(binding).some((ref) => ref.length === 0)) return null;
  if (!authority.accepted) return null;

  if (binding.canonical_ref !== transition.canonical_ref) return null;
  if (binding.authority_ref !== authority.authority_ref) return null;
  if (binding.capability_ref !== authority.capability_ref) return null;
  if (binding.policy_ref !== authority.policy_ref) return null;
  if (binding.verification_context_ref !== verification.verification_context_ref) {
    return null;
  }

  return {
    state: "ACCEPTED",
    canonical_ref: transition.canonical_ref,
    transition_ref: transition.transition_ref,
    acceptance_binding: binding,
  };
}

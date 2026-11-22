export type LiveAuthCheck =
  | { target: string; result: "SIGNED_IN"; checkedAt: string; evidenceRef: string }
  | { target: string; result: "SIGN_IN_REQUIRED"; checkedAt: string; evidenceRef: string }
  | { target: string; result: "UNKNOWN"; checkedAt: string; evidenceRef?: string };

export interface DirectAuthFailureEvidence {
  target: string;
  result: "LOGIN_WALL" | "AUTH_FAILURE" | "SESSION_EXPIRED";
  observedAt: string;
  evidenceRef: string;
}

export type AuthPromptGateResult =
  | { decision: "SUPPRESS"; reason: "RECENT_LIVE_CHECK_SIGNED_IN" }
  | { decision: "ALLOW"; reason: "FRESH_DIRECT_AUTH_FAILURE" }
  | { decision: "BLOCK"; reason: "UNKNOWN_OR_INSUFFICIENT_EVIDENCE" | "INVALID_EVIDENCE" };

/** Fail-closed gate; profile inventory and cookie/storage counts are not evidence inputs. */
export function evaluateAuthPrompt(
  target: string,
  latestCheck: LiveAuthCheck | null,
  failure: DirectAuthFailureEvidence | null,
): AuthPromptGateResult {
  if (!target.trim()) return { decision: "BLOCK", reason: "INVALID_EVIDENCE" };

  if (failure && (
    failure.target !== target ||
    !failure.evidenceRef.trim() ||
    !Number.isFinite(Date.parse(failure.observedAt))
  )) return { decision: "BLOCK", reason: "INVALID_EVIDENCE" };

  if (latestCheck) {
    const checkTime = Date.parse(latestCheck.checkedAt);
    if (
      latestCheck.target !== target ||
      !Number.isFinite(checkTime) ||
      !latestCheck.evidenceRef?.trim()
    ) return { decision: "BLOCK", reason: "INVALID_EVIDENCE" };

    if (latestCheck.result === "SIGNED_IN") {
      if (failure && Date.parse(failure.observedAt) > checkTime) {
        return { decision: "ALLOW", reason: "FRESH_DIRECT_AUTH_FAILURE" };
      }
      return { decision: "SUPPRESS", reason: "RECENT_LIVE_CHECK_SIGNED_IN" };
    }

    if (
      latestCheck.result === "SIGN_IN_REQUIRED" &&
      failure &&
      Date.parse(failure.observedAt) >= checkTime
    ) return { decision: "ALLOW", reason: "FRESH_DIRECT_AUTH_FAILURE" };
  }

  if (failure) {
    const checkTime = latestCheck ? Date.parse(latestCheck.checkedAt) : Number.NEGATIVE_INFINITY;
    if (Date.parse(failure.observedAt) > checkTime) {
      return { decision: "ALLOW", reason: "FRESH_DIRECT_AUTH_FAILURE" };
    }
  }

  return { decision: "BLOCK", reason: "UNKNOWN_OR_INSUFFICIENT_EVIDENCE" };
}

export type AuthPromptExecution<T> =
  | { gate: AuthPromptGateResult; promptRequested: false }
  | { gate: AuthPromptGateResult; promptRequested: true; result: T };

/**
 * Enforcement seam: the supplied prompt callback is invoked only when the gate
 * returns ALLOW. Callers must route auth-prompt side effects through this seam.
 */
export function runAuthPromptIfAllowed<T>(
  target: string,
  latestCheck: LiveAuthCheck | null,
  failure: DirectAuthFailureEvidence | null,
  requestAuthentication: () => T,
): AuthPromptExecution<T> {
  const gate = evaluateAuthPrompt(target, latestCheck, failure);
  if (gate.decision !== "ALLOW") return { gate, promptRequested: false };
  return { gate, promptRequested: true, result: requestAuthentication() };
}

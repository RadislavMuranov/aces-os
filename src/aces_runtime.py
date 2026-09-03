"""Minimal ACES runtime skeleton.

I-1E implementation target: deterministic control flow only.
No external connector, model, harness, or BASTION dependency is introduced here.
"""

from dataclasses import dataclass
from typing import Any, Callable, Dict, Optional


@dataclass(frozen=True)
class Intent:
    intent_id: str
    action: str
    target: str
    desired_state: Dict[str, Any]


@dataclass(frozen=True)
class Context:
    values: Dict[str, Any]


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    reason: str


@dataclass(frozen=True)
class Observation:
    state: Dict[str, Any]


@dataclass(frozen=True)
class VerificationResult:
    verified: bool
    reason: str


@dataclass(frozen=True)
class CycleResult:
    status: str
    evidence: Dict[str, Any]


class ACESRuntime:
    """Smallest executable Intent→Accepted State control loop."""

    def __init__(self, executor: Optional[Callable[[Intent, Context], Dict[str, Any]]] = None):
        self._executor = executor or self._default_executor
        self._state: Dict[str, Dict[str, Any]] = {}

    def run(self, intent: Intent, context: Context) -> CycleResult:
        decision = self.authorize(intent, context)
        if not decision.allowed:
            return self._result(intent, context, decision, None, None, "REJECTED")

        execution = self._executor(intent, context)
        observation = Observation(state=dict(execution))
        verification = self.verify(intent, observation)
        status = "ACCEPTED" if verification.verified else "UNVERIFIED"

        if verification.verified:
            self._state[intent.target] = dict(observation.state)

        return self._result(
            intent, context, decision, execution, verification, status
        )

    def authorize(self, intent: Intent, context: Context) -> AuthorizationDecision:
        if not intent.intent_id or not intent.action or not intent.target:
            return AuthorizationDecision(False, "missing required intent fields")
        if context.values.get("deny") is True:
            return AuthorizationDecision(False, "policy denied")
        return AuthorizationDecision(True, "policy allowed")

    @staticmethod
    def verify(intent: Intent, observation: Observation) -> VerificationResult:
        expected = intent.desired_state
        actual = observation.state
        if all(actual.get(k) == v for k, v in expected.items()):
            return VerificationResult(True, "desired state observed")
        return VerificationResult(False, "desired state not observed")

    def _result(
        self,
        intent: Intent,
        context: Context,
        decision: AuthorizationDecision,
        execution: Optional[Dict[str, Any]],
        verification: Optional[VerificationResult],
        status: str,
    ) -> CycleResult:
        evidence = {
            "intent_id": intent.intent_id,
            "normalized_intent": {
                "action": intent.action,
                "target": intent.target,
                "desired_state": intent.desired_state,
            },
            "context": context.values,
            "authorization": {
                "allowed": decision.allowed,
                "reason": decision.reason,
            },
            "connector": "controlled-local-executor",
            "action": intent.action,
            "execution": execution,
            "observation": execution,
            "verification": None
            if verification is None
            else {
                "verified": verification.verified,
                "reason": verification.reason,
            },
            "acceptance": status == "ACCEPTED",
            "accepted_state": self._state.get(intent.target),
            "status": status,
        }
        return CycleResult(status, evidence)

    @staticmethod
    def _default_executor(intent: Intent, context: Context) -> Dict[str, Any]:
        # Controlled local execution is deliberately deterministic for I-1E.
        return dict(intent.desired_state)

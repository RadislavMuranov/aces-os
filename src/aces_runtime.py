"""Minimal ACES runtime skeleton.

I-5 implementation target: explicit Observation provenance and persisted Evidence Bundle.
No external connector, model, harness, or BASTION dependency is introduced here.
"""

from dataclasses import dataclass
import json
from pathlib import Path
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
    provenance: Dict[str, str]


@dataclass(frozen=True)
class AuthorizationDecision:
    allowed: bool
    reason: str
    policy_id: str
    rule_id: str
    scope: str


@dataclass(frozen=True)
class ConnectorPlan:
    connector_id: str
    capability: str
    protocol: str
    path: str


@dataclass(frozen=True)
class ExecutionReceipt:
    connector_id: str
    action: str
    result: Dict[str, Any]


@dataclass(frozen=True)
class Observation:
    state: Dict[str, Any]
    source: str
    provenance: str


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

    POLICY_ID = "minimum-policy-v1"
    ALLOW_RULE_ID = "allow-valid-intent"
    DENY_RULE_ID = "deny-context-flag"
    CONNECTOR_ID = "controlled-local"
    CAPABILITY = "state-write"
    PROTOCOL = "native-local"
    PATH = "local-executor"
    OBSERVATION_SOURCE = "controlled-local-execution-receipt"

    def __init__(self, executor: Optional[Callable[[Intent, Context], Dict[str, Any]]] = None,
                 evidence_path: Optional[str] = None):
        self._executor = executor or self._default_executor
        self._state: Dict[str, Dict[str, Any]] = {}
        self._evidence_path = Path(evidence_path) if evidence_path else None
        self._cycle_sequence = 0

    @staticmethod
    def resolve_context(intent: Intent, values: Optional[Dict[str, Any]] = None) -> Context:
        resolved = dict(values or {})
        provenance = {key: "deterministic-input" for key in resolved}
        return Context(resolved, provenance)

    def run(self, intent: Intent, context: Context) -> CycleResult:
        self._cycle_sequence += 1
        cycle_id = f"cycle-{self._cycle_sequence:06d}"
        decision = self.authorize(intent, context)
        if not decision.allowed:
            return self._result(intent, context, decision, None, None, None, "REJECTED", cycle_id)

        plan = self.resolve_connector(intent, context, decision)
        if plan is None:
            return self._result(intent, context, decision, None, None, None, "REJECTED", cycle_id)

        receipt = self.execute(intent, context, plan)
        observation = Observation(
            state=dict(receipt.result),
            source=self.OBSERVATION_SOURCE,
            provenance=f"execution-receipt:{cycle_id}",
        )
        verification = self.verify(intent, observation)
        status = "ACCEPTED" if verification.verified else "UNVERIFIED"

        if verification.verified:
            self._state[intent.target] = dict(observation.state)

        return self._result(intent, context, decision, plan, receipt, verification, status, cycle_id, observation)

    def authorize(self, intent: Intent, context: Context) -> AuthorizationDecision:
        scope = f"target:{intent.target}" if intent.target else "target:unknown"
        if not intent.intent_id or not intent.action or not intent.target:
            return AuthorizationDecision(False, "missing required intent fields", self.POLICY_ID, self.DENY_RULE_ID, scope)
        if context.values.get("deny") is True:
            return AuthorizationDecision(False, "policy denied", self.POLICY_ID, self.DENY_RULE_ID, scope)
        return AuthorizationDecision(True, "policy allowed", self.POLICY_ID, self.ALLOW_RULE_ID, scope)

    def resolve_connector(self, intent: Intent, context: Context,
                          decision: AuthorizationDecision) -> Optional[ConnectorPlan]:
        """Resolve an allowed connector/capability only after authorization."""
        if not decision.allowed:
            return None
        if decision.scope != f"target:{intent.target}":
            return None
        return ConnectorPlan(self.CONNECTOR_ID, self.CAPABILITY, self.PROTOCOL, self.PATH)

    def execute(self, intent: Intent, context: Context, plan: ConnectorPlan) -> ExecutionReceipt:
        """Execution consumes a resolved plan; it does not perform authorization."""
        result = self._executor(intent, context)
        return ExecutionReceipt(plan.connector_id, intent.action, dict(result))

    @staticmethod
    def verify(intent: Intent, observation: Observation) -> VerificationResult:
        expected = intent.desired_state
        actual = observation.state
        if all(actual.get(k) == v for k, v in expected.items()):
            return VerificationResult(True, "desired state observed")
        return VerificationResult(False, "desired state not observed")

    def _result(self, intent: Intent, context: Context, decision: AuthorizationDecision,
                plan: Optional[ConnectorPlan], receipt: Optional[ExecutionReceipt],
                verification: Optional[VerificationResult], status: str, cycle_id: str,
                observation: Optional[Observation] = None) -> CycleResult:
        evidence_id = f"evidence-{cycle_id}"
        evidence = {
            "evidence_id": evidence_id,
            "cycle_id": cycle_id,
            "intent_id": intent.intent_id,
            "normalized_intent": {"action": intent.action, "target": intent.target, "desired_state": intent.desired_state},
            "context": context.values,
            "context_provenance": context.provenance,
            "authorization": {
                "allowed": decision.allowed, "reason": decision.reason,
                "policy_id": decision.policy_id, "rule_id": decision.rule_id, "scope": decision.scope,
            },
            "connector_plan": None if plan is None else {
                "connector_id": plan.connector_id, "capability": plan.capability,
                "protocol": plan.protocol, "path": plan.path,
            },
            "execution": None if receipt is None else {
                "connector_id": receipt.connector_id, "action": receipt.action, "result": receipt.result,
            },
            "observation": None if observation is None else {
                "state": observation.state, "source": observation.source, "provenance": observation.provenance,
            },
            "verification": None if verification is None else {"verified": verification.verified, "reason": verification.reason},
            "acceptance": status == "ACCEPTED",
            "accepted_state": self._state.get(intent.target),
            "status": status,
        }
        self._persist_evidence(evidence)
        return CycleResult(status, evidence)

    def _persist_evidence(self, evidence: Dict[str, Any]) -> None:
        if self._evidence_path is None:
            return
        self._evidence_path.parent.mkdir(parents=True, exist_ok=True)
        with self._evidence_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(evidence, sort_keys=True) + "\n")

    @staticmethod
    def _default_executor(intent: Intent, context: Context) -> Dict[str, Any]:
        return dict(intent.desired_state)

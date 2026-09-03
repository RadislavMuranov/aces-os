"""Minimal ACES runtime skeleton.

I-6 implementation target: explicit Verification, Acceptance, and persisted Accepted State.
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
class AcceptanceDecision:
    accepted: bool
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
                 evidence_path: Optional[str] = None, accepted_state_path: Optional[str] = None):
        self._executor = executor or self._default_executor
        self._state: Dict[str, Dict[str, Any]] = {}
        self._evidence_path = Path(evidence_path) if evidence_path else None
        self._accepted_state_path = Path(accepted_state_path) if accepted_state_path else None
        self._cycle_sequence = 0
        self._load_accepted_state()

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
            return self._result(intent, context, decision, None, None, None, None, "REJECTED", cycle_id)

        plan = self.resolve_connector(intent, context, decision)
        if plan is None:
            return self._result(intent, context, decision, None, None, None, None, "REJECTED", cycle_id)

        receipt = self.execute(intent, context, plan)
        observation = Observation(dict(receipt.result), self.OBSERVATION_SOURCE, f"execution-receipt:{cycle_id}")
        verification = self.verify(intent, observation)
        acceptance = self.accept(verification)
        status = "ACCEPTED" if acceptance.accepted else "UNVERIFIED"

        if acceptance.accepted:
            self._persist_accepted_state(intent, observation, cycle_id)

        return self._result(intent, context, decision, plan, receipt, verification, acceptance, status, cycle_id, observation)

    def authorize(self, intent: Intent, context: Context) -> AuthorizationDecision:
        scope = f"target:{intent.target}" if intent.target else "target:unknown"
        if not intent.intent_id or not intent.action or not intent.target:
            return AuthorizationDecision(False, "missing required intent fields", self.POLICY_ID, self.DENY_RULE_ID, scope)
        if context.values.get("deny") is True:
            return AuthorizationDecision(False, "policy denied", self.POLICY_ID, self.DENY_RULE_ID, scope)
        return AuthorizationDecision(True, "policy allowed", self.POLICY_ID, self.ALLOW_RULE_ID, scope)

    def resolve_connector(self, intent: Intent, context: Context,
                          decision: AuthorizationDecision) -> Optional[ConnectorPlan]:
        if not decision.allowed or decision.scope != f"target:{intent.target}":
            return None
        return ConnectorPlan(self.CONNECTOR_ID, self.CAPABILITY, self.PROTOCOL, self.PATH)

    def execute(self, intent: Intent, context: Context, plan: ConnectorPlan) -> ExecutionReceipt:
        result = self._executor(intent, context)
        return ExecutionReceipt(plan.connector_id, intent.action, dict(result))

    @staticmethod
    def verify(intent: Intent, observation: Observation) -> VerificationResult:
        if all(observation.state.get(k) == v for k, v in intent.desired_state.items()):
            return VerificationResult(True, "desired state observed")
        return VerificationResult(False, "desired state not observed")

    @staticmethod
    def accept(verification: VerificationResult) -> AcceptanceDecision:
        if verification.verified:
            return AcceptanceDecision(True, "verified state accepted")
        return AcceptanceDecision(False, "unverified state cannot be accepted")

    def _persist_accepted_state(self, intent: Intent, observation: Observation, cycle_id: str) -> None:
        record = {
            "target": intent.target,
            "state": observation.state,
            "cycle_id": cycle_id,
            "intent_id": intent.intent_id,
            "observation_provenance": observation.provenance,
        }
        self._state[intent.target] = dict(observation.state)
        if self._accepted_state_path is None:
            return
        self._accepted_state_path.parent.mkdir(parents=True, exist_ok=True)
        records = self._load_state_records()
        records[intent.target] = record
        self._accepted_state_path.write_text(json.dumps(records, sort_keys=True), encoding="utf-8")

    def _load_accepted_state(self) -> None:
        for target, record in self._load_state_records().items():
            if isinstance(record, dict) and isinstance(record.get("state"), dict):
                self._state[target] = dict(record["state"])

    def _load_state_records(self) -> Dict[str, Any]:
        if self._accepted_state_path is None or not self._accepted_state_path.exists():
            return {}
        return json.loads(self._accepted_state_path.read_text(encoding="utf-8"))

    def replay_accepted_state(self, target: str) -> Optional[Dict[str, Any]]:
        if self._accepted_state_path is None:
            return None
        record = self._load_state_records().get(target)
        if not isinstance(record, dict) or not isinstance(record.get("state"), dict):
            return None
        return dict(record["state"])

    def _result(self, intent: Intent, context: Context, decision: AuthorizationDecision,
                plan: Optional[ConnectorPlan], receipt: Optional[ExecutionReceipt],
                verification: Optional[VerificationResult], acceptance: Optional[AcceptanceDecision],
                status: str, cycle_id: str, observation: Optional[Observation] = None) -> CycleResult:
        evidence = {
            "evidence_id": f"evidence-{cycle_id}", "cycle_id": cycle_id, "intent_id": intent.intent_id,
            "normalized_intent": {"action": intent.action, "target": intent.target, "desired_state": intent.desired_state},
            "context": context.values, "context_provenance": context.provenance,
            "authorization": {"allowed": decision.allowed, "reason": decision.reason, "policy_id": decision.policy_id, "rule_id": decision.rule_id, "scope": decision.scope},
            "connector_plan": None if plan is None else {"connector_id": plan.connector_id, "capability": plan.capability, "protocol": plan.protocol, "path": plan.path},
            "execution": None if receipt is None else {"connector_id": receipt.connector_id, "action": receipt.action, "result": receipt.result},
            "observation": None if observation is None else {"state": observation.state, "source": observation.source, "provenance": observation.provenance},
            "verification": None if verification is None else {"verified": verification.verified, "reason": verification.reason},
            "acceptance": None if acceptance is None else {"accepted": acceptance.accepted, "reason": acceptance.reason},
            "accepted_state": self._state.get(intent.target), "status": status,
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

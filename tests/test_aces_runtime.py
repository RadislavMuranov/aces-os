from src.aces_runtime import ACESRuntime, Context, Intent


def test_minimum_cycle_accepts_verified_state():
    runtime = ACESRuntime()
    intent = Intent("I-1E-001", "set_state", "demo", {"value": 1})
    context = runtime.resolve_context(intent, {})
    result = runtime.run(intent, context)

    assert result.status == "ACCEPTED"
    assert result.evidence["verification"]["verified"] is True
    assert result.evidence["accepted_state"] == {"value": 1}
    assert result.evidence["authorization"]["policy_id"] == runtime.POLICY_ID
    assert result.evidence["authorization"]["rule_id"] == runtime.ALLOW_RULE_ID
    assert result.evidence["authorization"]["scope"] == "target:demo"


def test_policy_denial_is_fail_closed():
    runtime = ACESRuntime()
    intent = Intent("I-1E-002", "set_state", "demo", {"value": 1})
    context = runtime.resolve_context(intent, {"deny": True})
    result = runtime.run(intent, context)

    assert result.status == "REJECTED"
    assert result.evidence["execution"] is None
    assert result.evidence["accepted_state"] is None
    assert result.evidence["authorization"]["policy_id"] == runtime.POLICY_ID
    assert result.evidence["authorization"]["rule_id"] == runtime.DENY_RULE_ID
    assert result.evidence["authorization"]["scope"] == "target:demo"


def test_unverified_result_is_not_canonical():
    runtime = ACESRuntime(executor=lambda intent, context: {"value": 0})
    intent = Intent("I-1E-003", "set_state", "demo", {"value": 1})
    context = runtime.resolve_context(intent, {})
    result = runtime.run(intent, context)

    assert result.status == "UNVERIFIED"
    assert result.evidence["verification"]["verified"] is False
    assert result.evidence["accepted_state"] is None


def test_authority_decision_is_explicit_and_separate_from_connector():
    runtime = ACESRuntime()
    intent = Intent("I-3-001", "set_state", "demo", {"value": 2})
    context = runtime.resolve_context(intent, {})
    decision = runtime.authorize(intent, context)

    assert decision.allowed is True
    assert decision.policy_id == runtime.POLICY_ID
    assert decision.rule_id == runtime.ALLOW_RULE_ID
    assert decision.scope == "target:demo"
    result = runtime.run(intent, context)
    assert result.evidence["authorization"]["policy_id"] != result.evidence["connector"]

import unittest

from transition_contract import TransitionContract, validate_transition_contract


class TransitionContractValidatorTests(unittest.TestCase):
    def valid_contract(self):
        return TransitionContract(
            PredecessorState="STATE_A",
            CandidateAction="ACTION_A",
            ExpectedResultingState="STATE_B",
            Evidence="EVIDENCE_REF",
            VerificationRequirement="VERIFY_PASS",
            AuthorizationRequirement="AUTH_REQUIRED",
        )

    def test_complete_contract_is_accepted(self):
        result = validate_transition_contract(self.valid_contract())
        self.assertTrue(result.accepted)
        self.assertEqual(result.errors, ())

    def test_non_contract_input_is_rejected(self):
        result = validate_transition_contract({})
        self.assertFalse(result.accepted)
        self.assertEqual(result.errors, ("contract must be a TransitionContract",))

    def test_empty_required_field_is_rejected(self):
        contract = self.valid_contract()
        contract = TransitionContract(
            PredecessorState=contract.PredecessorState,
            CandidateAction="   ",
            ExpectedResultingState=contract.ExpectedResultingState,
            Evidence=contract.Evidence,
            VerificationRequirement=contract.VerificationRequirement,
            AuthorizationRequirement=contract.AuthorizationRequirement,
        )
        result = validate_transition_contract(contract)
        self.assertFalse(result.accepted)
        self.assertEqual(result.errors, ("CandidateAction: must be non-empty",))

    def test_multiple_invalid_fields_are_reported_in_fixed_order(self):
        contract = TransitionContract(
            PredecessorState=" ",
            CandidateAction="ACTION_A",
            ExpectedResultingState="",
            Evidence="EVIDENCE_REF",
            VerificationRequirement="VERIFY_PASS",
            AuthorizationRequirement=" ",
        )
        result = validate_transition_contract(contract)
        self.assertFalse(result.accepted)
        self.assertEqual(
            result.errors,
            (
                "PredecessorState: must be non-empty",
                "ExpectedResultingState: must be non-empty",
                "AuthorizationRequirement: must be non-empty",
            ),
        )

    def test_wrong_runtime_type_is_rejected_without_coercion(self):
        contract = TransitionContract(
            PredecessorState="STATE_A",
            CandidateAction="ACTION_A",
            ExpectedResultingState="STATE_B",
            Evidence=123,  # type: ignore[arg-type]
            VerificationRequirement="VERIFY_PASS",
            AuthorizationRequirement="AUTH_REQUIRED",
        )
        result = validate_transition_contract(contract)
        self.assertFalse(result.accepted)
        self.assertEqual(result.errors, ("Evidence: expected string",))

    def test_missing_constructor_argument_fails_closed_at_type_boundary(self):
        with self.assertRaises(TypeError):
            TransitionContract(
                PredecessorState="STATE_A",
                CandidateAction="ACTION_A",
                ExpectedResultingState="STATE_B",
                Evidence="EVIDENCE_REF",
                VerificationRequirement="VERIFY_PASS",
            )


if __name__ == "__main__":
    unittest.main()

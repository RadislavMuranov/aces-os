import unittest

from transition_contract import TransitionContract, validate_transition_contract


class TransitionContractValidationMatrixTests(unittest.TestCase):
    FIELDS = (
        "PredecessorState",
        "CandidateAction",
        "ExpectedResultingState",
        "Evidence",
        "VerificationRequirement",
        "AuthorizationRequirement",
    )

    INVALID_RUNTIME_VALUES = (
        None,
        False,
        0,
        0.0,
        b"bytes",
        [],
        {},
        object(),
    )

    def make_valid(self):
        return TransitionContract(
            PredecessorState="STATE_A",
            CandidateAction="ACTION_A",
            ExpectedResultingState="STATE_B",
            Evidence="EVIDENCE_REF",
            VerificationRequirement="VERIFY_PASS",
            AuthorizationRequirement="AUTH_REQUIRED",
        )

    def replace(self, contract, **changes):
        values = {field: getattr(contract, field) for field in self.FIELDS}
        values.update(changes)
        return TransitionContract(**values)

    def test_each_required_field_rejects_whitespace(self):
        for field in self.FIELDS:
            with self.subTest(field=field):
                contract = self.replace(self.make_valid(), **{field: "   "})
                result = validate_transition_contract(contract)
                self.assertFalse(result.accepted)
                self.assertEqual(result.errors, (f"{field}: must be non-empty",))

    def test_each_required_field_rejects_representative_non_string_runtime_values(self):
        for field in self.FIELDS:
            for invalid_value in self.INVALID_RUNTIME_VALUES:
                with self.subTest(field=field, invalid_value=repr(invalid_value)):
                    contract = self.replace(self.make_valid(), **{field: invalid_value})
                    result = validate_transition_contract(contract)
                    self.assertFalse(result.accepted)
                    self.assertEqual(result.errors, (f"{field}: expected string",))

    def test_multiple_invalid_fields_keep_fixed_field_order(self):
        contract = self.replace(
            self.make_valid(),
            PredecessorState=" ",
            Evidence=0,
            AuthorizationRequirement=" ",
        )
        result = validate_transition_contract(contract)
        self.assertFalse(result.accepted)
        self.assertEqual(
            result.errors,
            (
                "PredecessorState: must be non-empty",
                "Evidence: expected string",
                "AuthorizationRequirement: must be non-empty",
            ),
        )


if __name__ == "__main__":
    unittest.main()

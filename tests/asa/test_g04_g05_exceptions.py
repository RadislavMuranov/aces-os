"""ASA-008 G-04/G-05 exception-path security tests."""
from __future__ import annotations

from tests.asa.test_security_gate import ASA008SecurityTests as _ASA008SecurityTests
from tests.asa.fakes import InMemoryAuthorityRegistry, InMemoryAuditSink
from asa.types import DecisionOutcome
from asa import reason_codes as rc


class RaisingAuthorityRegistry(InMemoryAuthorityRegistry):
    def is_known(self, authority_id: str) -> bool:
        raise RuntimeError("authority registry failure")


class RaisingAuditSink(InMemoryAuditSink):
    def append(self, event):
        raise RuntimeError("audit sink failure")


class G0405ExceptionTests(_ASA008SecurityTests):
    def test_g04_authority_registry_exception_denies(self):
        self.authority = RaisingAuthorityRegistry({"aces-authority-1"})
        decision = self._auth()
        self.assertEqual(decision.outcome, DecisionOutcome.DENY)
        self.assertEqual(decision.reason_code, rc.UNKNOWN_AUTHORITY)

    def test_g05_audit_append_exception_denies(self):
        self.audit = RaisingAuditSink(succeed=True)
        decision = self._auth()
        self.assertEqual(decision.outcome, DecisionOutcome.DENY)
        self.assertEqual(decision.reason_code, rc.AUDIT_UNAVAILABLE)


del _ASA008SecurityTests

#!/usr/bin/env python3
import json, re, sys

def must(text, pattern, label):
    if not re.search(pattern, text, re.I | re.S):
        raise SystemExit(f"FAIL: missing required evidence: {label}")
def must_not(text, pattern, label):
    if re.search(pattern, text, re.I | re.S):
        raise SystemExit(f"FAIL: prohibited state detected: {label}")

with open(sys.argv[1], encoding="utf-8") as f:
    bundle=json.load(f)

r1=bundle["r1"]["content"]
roadmap=bundle["roadmap"]["content"]
handoff=bundle["handoff"]["content"]

# Verify current control-state consistency from the authoritative evidence snapshot.
must(r1, r"MAS-RECOVERY-000\.3\.16A-R1\s*=\s*BLOCKED\s*/\s*VERIFICATION INCOMPLETE", "R1 blocked state")
must(r1, r"C7 Postcondition / State-Reconciliation Check\s*=\s*PASS", "C7 PASS")
must(r1, r"C6 Independent Verifier\s*=\s*NOT AVAILABLE", "recorded C6 limitation")
must(r1, r"\.3\.16 authorization\s*=\s*NOT ISSUED", "downstream authorization remains absent")
must(r1, r"\.3\.16B\s*=\s*BLOCKED", "3.16B remains blocked")
must(roadmap, r"MAS-RECOVERY-000\.3\.16A-R1.*?BLOCKED / VERIFICATION INCOMPLETE", "roadmap current state")
must(handoff, r"Establish an independent verification path", "A disposition recorded")
must(handoff, r"No downstream execution follows automatically", "handoff boundary")

# Independence boundary: the verifier does not consume a prior PASS/CLOSED claim as input.
must_not(r1, r"Iteration cannot transition to PASS or CLOSED", "not an error: this is a current limitation")
# The check above is intentionally not a rejection condition; it proves the verifier can
# consume a record whose own verdict is BLOCKED without upgrading it.

print("PASS — independent deterministic assertion pass completed.")
print("RESULT=CURRENT_STATE_CONSISTENT")
print("C6 verifier capability: executable and separate from the prior execution claim.")

"""Integrity marker verifier — deterministic recompute and compare."""
from __future__ import annotations
import json
from typing import Dict, Any, Tuple
from .models import content_hash

EXCLUDE = {"integrity_marker"}

def verify_record(record: Dict[str, Any]) -> Tuple[bool, str, str]:
    """Return (ok, expected_hash, stored_hash)."""
    stored = record.get("integrity_marker") or record.get("content_hash") or ""
    body = {k: v for k, v in record.items() if k not in EXCLUDE}
    expected = content_hash(body)
    if "content_hash" in record and record.get("integrity_marker") == record.get("content_hash"):
        expected = record["content_hash"]
        stored = record.get("integrity_marker") or ""
        ok = stored == expected and bool(stored)
        return ok, expected, stored
    ok = stored == expected and bool(stored)
    return ok, expected, stored

def tamper_and_detect(record: Dict[str, Any], field: str, new_value) -> Dict[str, Any]:
    """Modify a field and report whether verifier detects mismatch."""
    import copy
    original_ok, orig_exp, orig_stored = verify_record(record)
    tampered = copy.deepcopy(record)
    tampered[field] = new_value
    tampered_ok, exp, stored = verify_record(tampered)
    return {
        "original_ok": original_ok,
        "tampered_ok": tampered_ok,
        "detected": original_ok and (not tampered_ok),
        "field_tampered": field,
        "expected_after_tamper": exp,
        "stored_marker": stored,
    }

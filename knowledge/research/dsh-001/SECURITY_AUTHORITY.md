# Security / Sandbox / Authority

**DSH provides:** sandbox seam (Landlock/bwrap/Seatbelt backends reported); approval policy; tool pipeline hooks; env scrub patterns (secondary sources); permission modes (read-only / workspace-write / danger-full-access).

**Critical limits (external + design):**
- Developer preview; safety notices mandatory.
- Plugins run **in-process** — not guest VMs; plugin install ≈ code execution trust.
- Tencent Zhuque A.I.G (arXiv 2608.16393): measurable indirect prompt injection success on multiple channels (skills/file/text); tool-result and skill channels matter.
- Community reports of ecosystem plugin risks; sandbox escape claims (treat as **external**, verify before policy).

**ACES must own:** Architectural Authority, Decision (ALLOW/DENY), protected-resource model (ASA-class), non-self-authorization, evidence for promotion — **above** DSH tool policy.

Confidence: High that DSH security ≠ ACES Authority Boundary.

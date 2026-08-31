# R18 — DSH-Based ACES Engine Decision

## Decision

**C. DSH ENGINE — CONDITIONALLY ACCEPTABLE / SPECIFIC BLOCKERS**  
(Aligned with prior **CONDITIONAL**; under engine-first framing this is **B-leaning C**: acceptable as experimental engine only after **significant hardening**, with explicit blockers before production ACES use.)

Not A (minimal hardening only) — in-process plugin trust, IPI evidence, preview maturity, authority gap are not “minimal.”  
Not D (unsuitable) — capability coverage and session reconstructability are strong enough to **prefer adapting DSH over greenfield harness**.

---

## Smallest safe ACES control surface around DSH

```text
ACES OS
  Semantic Reality | Intent | Decision | Authority | Verification | Evidence | Evolution
            ↓
     ACES HARNESS CONTRACT  (authorize / deny / bind decision-id)
            ↓
     DSH ADAPTER / HARDENING  (allowlist plugins, taint MCP, map approval→Decision)
            ↓
     HARDENED DSH ENGINE (Cordis + agent-loop + tools + session log + sandbox)
            ↓
     Agents / Tools / MCP → Digital World → Result
            ↓
     ACES Verification → Evidence → AcceptedState
```

**Never delegated to DSH:** canonical truth, canonical policy, authorization, final security decision, AcceptedState, canonical provenance, verification authority, evolution authority.

**DSH may:** execute **authorized** work; emit engine logs/traces; mediate tools under contract.

---

## Specific blockers (must clear for production-grade ACES engine use)

1. Plugin load **allowlist** + no default marketplace trust  
2. Protected side effects require **ACES Decision id** (adapter)  
3. Untrusted tool/MCP/skill content **taint + gate**  
4. Skills/foreign hooks **off** until necessity proven  
5. Self-modification **disabled**  
6. DSH **version pin** + regression suite  
7. Session log integrity; explicit **non-identity** with Canon Evidence  
8. Sandbox fail-closed for shell/fs in ACES profiles  

---

## Anti-duplication rule

Do **not** reimplement DSH loop/tools/session inside ACES unless evidence shows: (1) DSH cannot safely provide it, (2) cannot adapt it, (3) capability is constitutionally ACES (authority/evidence/verification/evolution).

---

## Confidence

**Medium–High** that DSH can serve as **experimental** ACES Harness Engine under the control surface above.  
**Low–Medium** for production until blockers cleared and security hardening verified.

**Not Canon. Not implemented.**

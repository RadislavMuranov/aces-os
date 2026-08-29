# ACES OS — P0 PRODUCT VERIFICATION PROTOCOL

**Status:** RATIFIED / READY FOR EXECUTION  
**Protocol:** MASTER PROTOCOL v1.0 — Research → Product Transition  
**Date:** 2026-08-29  
**Repository:** `RadislavMuranov/aces-os`  
**Mode:** Controlled product verification  
**Mutations:** 0 by default

---

## 1. Transition

The R-series architectural falsification cycle is closed for the currently tested gaps.

ACES is **not** permitted to claim architectural necessity from those results.

The project now enters product verification:

> **Does a zero-friction connective coordinator produce measurable human benefit when the underlying digital mechanisms already exist?**

The burden of proof has moved from **necessity** to **utility**.

---

## 2. Scientific conclusion carried forward

Accepted current conclusion:

> Existing platforms + MCP + LLMs + native agents + structured markers + enforcement mechanisms can close the previously tested gaps without requiring a new ACES storage layer, object model, or competing workspace.

Therefore:

- no feature enters the ACES core merely because it is convenient;
- no feature enters the core if existing mechanisms can provide it adequately;
- any claim of new architectural necessity must restart an R-style necessity/minimality test.

---

## 3. P0 objective

Measure whether one connective coordinator can reduce **human integration work** while leaving existing systems as owners.

Primary outcome dimensions:

1. cognitive load;
2. time to understand current state;
3. time to decide;
4. context reconstruction effort;
5. cross-system errors and omissions;
6. duplicate/manual coordination work;
7. continuity after interruption.

Technical elegance is not a success criterion.

---

## 4. Hard constraints

### Prohibited

- new ACES domain objects;
- new ACES database/storage;
- duplicate task manager;
- duplicate knowledge base;
- mandatory manual tagging;
- mandatory data entry for the experiment;
- ACES-owned documents, tasks, contacts, code, or financial records;
- a new dashboard as the experimental target;
- replacing existing platform owners.

### Permitted

- Google Workspace;
- GitHub;
- Obsidian;
- Kaiten;
- Notion where already appropriate;
- MCP;
- LLMs and existing agent platforms;
- existing metadata and minimal marker protocols already accepted by R-series tests;
- measurement of human effort and outcomes.

---

## 5. Baseline / treatment

### Baseline B

Human + existing platforms + available MCP + LLM/native agents + existing protocols.

The human performs the necessary cross-system coordination.

### Treatment T

The same human + the same platforms + the same underlying mechanisms + **one zero-friction connective coordinator**.

The coordinator may observe, correlate, summarize, route, maintain already-permitted markers, and execute already-authorized actions.

It must not become a new owner.

---

## 6. Zero-friction requirement

The coordinator fails the P0 hypothesis if it requires the human to:

- maintain a second representation of reality;
- manually connect systems for the coordinator;
- duplicate tasks or documents;
- learn a new workflow whose burden exceeds the coordination it removes;
- operate a visible control surface merely to keep continuity alive.

Canonical requirement:

> **The mechanism must absorb coordination rather than expose coordination.**

---

## 7. Measurement

For equivalent controlled situations, record:

- elapsed time to reach usable understanding;
- number of application/context switches;
- number of manual joins between systems;
- number of facts that must be re-found;
- number of duplicate entries;
- number of missed/incorrect dependencies;
- decision latency;
- recovery time after interruption;
- subjective cognitive effort;
- uncertainty preservation;
- owner-boundary violations.

No single metric is sufficient. The result must show a meaningful human outcome, not merely lower API latency.

---

## 8. Pass / fail

### PASS

Treatment demonstrates a repeatable, material reduction in human integration effort or a corresponding improvement in decision speed/quality **without introducing material new user burden or owner-boundary violations**.

### FAIL

Any of the following is sufficient:

- no meaningful human improvement;
- benefit comes only from better underlying tools rather than coordination;
- coordinator requires manual maintenance that offsets the benefit;
- coordinator becomes a competing workspace/owner;
- uncertainty or provenance is degraded;
- authority boundaries are weakened;
- results cannot be reproduced.

### INCONCLUSIVE

The experiment cannot isolate the coordinator effect or lacks sufficient observations. INCONCLUSIVE is not FAIL.

---

## 9. Experimental unit

One complete human situation crossing at least two existing environments and containing a meaningful decision or action.

The unit must be replayable or sufficiently controlled to compare B and T.

The experiment does not require real personal data. Synthetic or controlled data is preferred for early safety and repeatability.

---

## 10. Current state

**P0:** READY / AUTHORIZED  
**Execution:** NOT STARTED by this protocol  
**ACES new objects:** 0  
**ACES new storage:** 0  
**ACES new UI:** 0  
**Production mutation:** prohibited unless separately authorized by the test contract  

---

## 11. Decision gate

If P0 passes, the next question is not "what should ACES build?" It is:

> **Which smallest product mechanism produced the measured benefit, and can that mechanism remain entirely owner-neutral and zero-friction?**

If P0 fails, the connective-agent product hypothesis is rejected or narrowed.

No automatic transition to architecture follows from PASS.

---

## 12. Canonical postulate

> **Minimal mechanisms work only on condition that someone creates them, maintains them, places them correctly, and keeps them coherent across the Digital World.**

P0 exists specifically to test whether a zero-friction coordinator can absorb that maintenance burden without becoming another layer the human must operate.

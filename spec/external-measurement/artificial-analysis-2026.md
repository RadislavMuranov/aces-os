# Artificial Analysis — Fundamental Research Record (2026)

**Status:** Research / Strategic Architecture Input
**Date:** 2026-09-03
**Target branch:** `architecture/priority-realization-roadmap-v2`

## Executive conclusion

Artificial Analysis should be treated by ACES OS as an **External AI Capability Measurement / Evidence Layer**, not as a Decision Authority or Authorization Authority.

The key architectural distinction is:

> **Measurement ≠ Authority**

Artificial Analysis increasingly measures the capability space across **Model × Endpoint/Provider × Agent × Search × Hardware × Workload × Cost × Latency × Throughput**. ACES OS must use such measurements as external evidence and combine them with context, risk, policy, authority and verification before permitting execution.

## 1. Evolution of the platform

Artificial Analysis has evolved from model leaderboard benchmarking toward broader AI measurement infrastructure:

```text
Model benchmarking
    → reasoning / frontier evaluation
    → agentic workloads
    → cost + latency
    → provider / endpoint comparison
    → search-provider benchmarking
    → agent performance
    → load / concurrency
    → hardware efficiency
    → domain-specific evaluation
```

The Intelligence Index is now only one component of the platform.

## 2. Intelligence Index

Current methodology is Intelligence Index v4.1.1 (August 2026).

The major methodological direction is away from saturated academic benchmarks and toward evaluations that better separate frontier systems and reflect real-world/agentic work.

Important current evaluation families include:

- GDPval-AA v2
- Terminal-Bench 2.1
- τ³-Bench Banking
- Humanity's Last Exam
- AA-Omniscience
- SciCode
- GPQA
- AA-LCR
- CritPt

The benchmark composition and weighting are version-dependent and must always be stored with the measurement. Scores from different index versions must not be treated as directly interchangeable without version reconciliation.

## 3. Cost and production economics

Artificial Analysis increasingly reports not merely quality but the economics of achieving quality:

- Cost per task
- Time per task
- Tokens per task
- Input/output/reasoning/cache cost components
- Quality × cost Pareto frontiers
- Quality × latency / speed trade-offs

Therefore the relevant production question is not simply “which model is best?” but “which model/provider configuration is non-dominated for the required workload, SLO and budget?”

## 4. Model ≠ Provider ≠ Endpoint

A model name is not sufficient as a production identity.

The same model can behave differently across inference providers because of serving configuration, quantization, context handling and infrastructure.

Artificial Analysis' Endpoint Accuracy Index further establishes the endpoint as a separately measurable object.

For ACES, evidence should therefore preserve at minimum:

```yaml
model: ...
provider: ...
endpoint: ...
configuration: ...
harness: ...
benchmark: ...
benchmark_version: ...
observed_at: ...
```

## 5. Agentic measurement

Artificial Analysis now separates general intelligence from agentic capability and evaluates agentic knowledge work and customer-interaction workloads.

AA-Briefcase and related agentic evaluations move measurement toward realistic multi-step knowledge-work tasks.

AA-AgentPerf additionally measures agent workloads under concurrency and infrastructure constraints.

This is directly relevant to ACES because:

> **Model intelligence ≠ agent capability ≠ execution authority.**

## 6. Search as an external capability

Artificial Analysis Search Index evaluates Search APIs independently of the underlying LLM, allowing the same agent/harness/model configuration to be compared across search providers.

This is highly relevant to the ACES Connector thesis: external capabilities should be replaceable and measurable without requiring the entire agent architecture to change.

## 7. Load and infrastructure measurement

Artificial Analysis has expanded beyond low-concurrency endpoint tests through System Load Testing and agent performance evaluations.

Current measurement includes concurrency, throughput, TTFT, end-to-end speed and related SLO dimensions.

Therefore the earlier characterization of the platform as testing only up to approximately 10 RPS is obsolete and must not be used as the current state description.

## 8. Endpoint fallback and epistemic identity

Frontier evaluations can involve provider-side fallback behavior. A benchmark result therefore describes a **deployment/configuration**, not necessarily a pure isolated model.

For example, the reported Claude Fable 5.1 result includes server-side fallback behavior. ACES evidence must preserve such qualifiers when known.

## 9. API / data access

Artificial Analysis now provides a public Data API with a limited free tier and deeper paid/commercial data access.

API-derived evidence should record:

- source/API version where available;
- retrieval timestamp;
- model/provider identity;
- benchmark/index version;
- measurement fields actually returned;
- provenance.

## 10. Limitations

Artificial Analysis remains insufficient as a sole decision source for ACES.

Important limitations include:

- universal benchmark ≠ domain-specific task validity;
- benchmark score ≠ human preference;
- capability measurement ≠ security assurance;
- factuality ≠ full epistemic governance;
- agent benchmark ≠ authorization to act;
- external benchmark ≠ organizational memory/continuity;
- proprietary methodology introduces reproducibility limits;
- judge-model dependence can affect evaluations;
- provider coverage and measurement availability can be uneven;
- production behavior must still be verified with workload-specific tests.

## 11. ACES architectural interpretation

Artificial Analysis should enter ACES as **external measurement evidence**.

Conceptual flow:

```text
Artificial Analysis
        ↓
External Measurement Evidence
        ↓
ACES Evidence Layer
        ↓
World Model / Epistemic Engine
        ↓
Context + Task + Risk + Cost + Policy
        ↓
Decision Authority
        ↓
Authorized Execution
        ↓
Verification
```

Artificial Analysis must not become a hidden routing authority or single source of truth.

## 12. Proposed ACES Evidence object

```yaml
Evidence:
  source: artificial-analysis
  source_type: external_measurement
  model: ...
  provider: ...
  endpoint: ...
  harness: ...
  benchmark:
    name: ...
    version: ...
  score: ...
  cost_per_task: ...
  latency: ...
  throughput: ...
  fallback: ...
  observed_at: ...
  provenance: ...
```

The exact schema remains subject to ACES Evidence/Knowledge standard reconciliation.

## 13. Strategic implication for ACES Model & Provider Selection

Artificial Analysis can serve as one external evidence feed for a future ACES Model/Provider Selection Engine:

```text
Task
 ↓
Required capabilities
 ↓
Risk classification
 ↓
Candidate models/providers
 ↓
Artificial Analysis evidence
 ↓
Cost / latency / capability Pareto analysis
 ↓
ACES policy + context + risk
 ↓
Selection decision
 ↓
Authorized execution
 ↓
Verification
```

The selection engine must remain ACES-owned.

## 14. Canonical principle candidate

> **External benchmark measurements are Evidence, not Authority.**

Proposed status: **architecture principle / candidate for formal Canon Gate**, not automatically Canonized by this research record.

## 15. Weekly monitoring

A recurring Artificial Analysis Digest has been activated separately. It should track:

- models and frontier leaderboard changes;
- benchmark and methodology changes;
- agentic evaluations;
- provider/endpoint changes;
- search APIs;
- cost, latency and throughput;
- hardware;
- API/data-access changes;
- new evaluation products;
- implications for ACES OS architecture.

Each digest should distinguish **source facts**, **measurement changes**, **interpretation**, and **ACES implications**.

## Primary source families

- Artificial Analysis Intelligence Index and methodology
- Artificial Analysis Performance methodology
- Artificial Analysis Data API documentation
- Artificial Analysis Search Index
- Artificial Analysis Endpoint Accuracy Index
- Artificial Analysis System Load Test
- Artificial Analysis AgentPerf
- Artificial Analysis Articles / Changelog

---

**Research conclusion:** Artificial Analysis is strategically valuable to ACES OS as an independent external measurement and evidence source. Its increasing coverage of model, endpoint, provider, agent, search, workload, cost, latency, throughput and hardware dimensions makes it substantially more useful than a conventional leaderboard. ACES must preserve the separation between measurement, epistemic judgment, decision authority and execution authority.

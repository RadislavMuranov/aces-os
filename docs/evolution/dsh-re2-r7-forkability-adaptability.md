# DSH-RE2 — R7 Forkability & Adaptability Analysis

Status: COMPLETE
Baseline: deepseek-ai/deepseek-harness @ dd6322d604e00eec1ba5e0c8541159906a21094a
Date: 2026-09-01

## Scope
Assess the depth at which ACES can modify DSH, from configuration-only changes through provider replacement and core/runtime changes.

## Evidence
1. Profiles declare ordered bundle layers in `dsh.profile.bundles`; bundle manifests point to patch files. The loader composes bundle layers, profile patch, home patch, and launcher overlays.
2. A patch targets a row by id and replaces its whole config or inserts rows. Therefore runtime composition can replace configured providers without editing upstream package source.
3. DSH explicitly documents that model adapter, tool registry, session log, and agent loop are plugins and replaceable from configuration.
4. Capability seams separate Service Definition, Service Provider, and Consumer. Examples include LLM, tools, filesystem, subprocess, sandbox, agents and sessions.
5. Scoped registrations are owned by Cordis Context effects and unwind with plugin/scope disposal.
6. The concrete agent loop is a separate package from the agent registry/interface. This permits replacing the default loop provider at the composition layer if the replacement satisfies the interface/consumer contract.
7. `sdk-minimal` demonstrates a repository-owned alternative complete runtime tree rather than only patching the shared base bundle.
8. The repository is MIT licensed, permitting a private/public derivative subject to license conditions.

## Adaptability ladder

| Level | Mechanism | Upstream source modification | Result |
|---|---|---:|---|
| A | Profile selection | No | alternate shipped composition |
| B | Bundle ordering | No | layer composition |
| C | Patch/overlay | No | row replacement/insertion |
| D | External plugin | No | new/replaced capability |
| E | Provider/seam replacement | No | subsystem implementation swap |
| F | Alternate runtime tree | No | independent composition |
| G | Fork package/core | Yes | arbitrary source modification |
| H | Fork Cordis/runtime substrate | Yes, upstream substrate | fundamental runtime modification |

## Escape-velocity assessment

No single architectural ceiling was found before source modification. The composition system reaches provider and subsystem replacement without changing DSH source. The repository also contains an explicit alternate complete runtime tree (`sdk-minimal`). Once the required change crosses an interface or Cordis semantic invariant, a source fork is required.

Therefore the practical boundary is not "can DSH be adapted?" but "at which semantic boundary does adaptation stop being a composition change and become a source/runtime fork?".

## Hidden coupling risks

- shared Cordis instance/module identity is deliberately managed by profile module fallback;
- lifecycle semantics constrain live replacement of one-shot/stdio profiles;
- consumers depend on interface/event contracts;
- changing event or session semantics can require coordinated changes across producers and consumers;
- changing Cordis lifecycle/event semantics crosses the DSH substrate boundary.

## R7 verdict

PASS.

Confirmed: DSH is forkable and has multiple non-source adaptation layers. No finite number of adaptation iterations is imposed by the architecture. However, "infinite evolution" is not a formal property; every future change remains constrained by interface compatibility, lifecycle invariants, dependencies, tests, and the cost of maintaining a fork.

## ACES decision input

DSH qualifies as an evolutionary execution substrate candidate. ACES may preserve, replace, or fork DSH components progressively. No claim is made that DSH must remain the permanent lowest-level runtime.

Next: R8 — Controlled Ablation Experiments.

# DSH-RE2 — R4 Context Compiler / Profiles / Bundles / Patches

Status: COMPLETE
Baseline: deepseek-ai/deepseek-harness @ dd6322d604e00eec1ba5e0c8541159906a21094a
Date: 2026-09-01

## Facts

1. A profile is a directory under `$DSH_HOME/profiles/<name>` containing package.json, ordered `dsh.profile.bundles`, and user `cordis.patch.yml`.
2. A bundle is an npm package declaring `dsh.bundle.patch`; its patch file exports a layer of Cordis entry patches.
3. Profile initialization creates an empty root `cordis.yml`; the effective tree is produced by patching this empty list.
4. `composeEntries()` flattens all patch layers and calls `applyEntryPatches()` once. This is the actual composition function used by boot.
5. Application order is: bundle patches in declared order -> profile patches -> home patch -> invocation overlays. Telemetry may append a final launcher-generated disable patch.
6. A patch targets an entry by id. A targeted patch replaces the targeted row's whole config; insert adds entries. Later layers therefore override earlier rows by id.
7. Patch objects are cloned before application/recomposition because inserted rows can retain object references and later id-targeted patches can mutate those objects.
8. Live reload is implemented by re-reading user patch layers and updating the root Include entry. Custom profiles default to live reload; shipped profiles choose live/startup according to lifecycle constraints.
9. Profile package dependencies are installed out-of-tree. Module fallback/healing is used so external plugins can share the installation's Cordis instance.
10. `sdk-minimal` is a separate standalone composition: it does not layer over `dsh-base`; its bundle inserts the complete required tree, after which user/home/invocation patches still apply.

## Effective model

Profile compilation is:

`empty root + ordered bundle layers + profile layer + home layer + invocation overlays -> composed EntryOptions[] -> Cordis Loader tree`

This is a runtime composition compiler, but not a general-purpose compiler: input is structured patch data and output is an ordered Cordis entry list.

## Verified properties

- Deterministic layer ordering: PASS.
- Overlay precedence by entry id: PASS.
- Bundle/profile separation: PASS.
- Standalone minimal profile: PASS.
- Runtime re-composition: PASS.
- Live patch reload mechanism: PASS.
- External plugin dependency injection: PASS.

## Limits / open items

- Full patch algebra semantics are not yet exhaustively reconstructed.
- Complete validation/error semantics of `applyEntryPatches` remain for source-level inspection if needed.
- Security/authority of `!!js` expressions is deferred to R6.
- Whether this composition mechanism is sufficient as an ACES Context Compiler is an architecture decision, not a DSH fact.

## R4 verdict

PASS — DSH has a concrete, source-backed runtime composition compiler based on ordered patch layers over an empty root. Proceed to R5.

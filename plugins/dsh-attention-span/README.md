# DSH ACES Attention Span Pilot

A conservative, deterministic pilot plugin for DeepSeek Harness.

## Purpose

The plugin operationalizes four communication principles:

- Simplicity — reduce unnecessary decoding complexity.
- Brevity — remove redundant or filler material.
- Clarity — preserve explicit meaning rather than relying on implication.
- Humanity — avoid bureaucratic phrasing where a safe deterministic reduction is possible.

The pilot exposes an explicit tool: attention_span_optimize.

## Safety boundary

This is intentionally a tool-first deployment:

1. The model/user explicitly invokes optimization.
2. The plugin performs deterministic local transformations only.
3. The plugin uses a reduction cap of 35% by default.
4. If the cap is exceeded, the original text is returned unchanged.
5. Code fences and URLs are protected from transformation.
6. Token counts are coarse estimates (ceil(chars / 4)), not provider tokenizer measurements.
7. No session state is mutated.

This makes the pilot suitable for local verification before any automatic agent/request or agent/pre-step integration is considered.

## Install

From the ACES OS checkout:

    dsh plugin --profile web add ./plugins/dsh-attention-span

Then verify composition:

    dsh --profile web --dump-config

The bundle should appear as dsh-aces-attention-span.

## Local deterministic verification

The core has no DSH runtime dependency and can be tested directly:

    node plugins/dsh-attention-span/test-core.mjs

## Deployment status

PILOT / LOCAL-VERIFICATION ONLY

No production activation, automatic prompt rewriting, or durable-session mutation is part of this pilot.

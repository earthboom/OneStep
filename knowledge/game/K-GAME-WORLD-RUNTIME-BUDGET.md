---
id: "K-GAME-WORLD-RUNTIME-BUDGET"
title: "Preserve world outcomes when reducing offscreen and streaming costs"
summary: "Profile a representative route, then decide which offscreen objects draw, stay resident, keep state and continue simulating. Check costs alongside world outcomes on return."
kind: "method"
scope: "Rendering, streaming, spawning and NPC simulation budgets for real-time games"
keywords: ["streaming","offscreen AI","culling","pooling","LOD","frame budget","resident memory","화면 밖 NPC","스트리밍","오브젝트 풀","프레임 예산"]
status: "active"
checked_at: "2026-11-26"
---

# Preserve world outcomes when reducing offscreen and streaming costs

## Guidance

Reproduce a long frame on a supported build and device with fixed resolution and quality. Separate first entry, warm-up and repeat entry. Read the CPU and GPU timeline, then isolate the dominant workload. Check pixel cost through resolution, CPU submission through draw and state changes, and first-entry stalls through I/O, decompression, upload and pipeline warm-up. Record median and tail frame times, long frames and memory against the project's budget.

Decide separately whether a world object is rendered, its assets are resident, its logical state is retained and its simulation advances. Give relevant offscreen quest or combat outcomes an owner. Choose full simulation, reduced ticks, scheduled state updates or reconstruction on entry according to the observable requirement. Put limits on spawns and asynchronous activation. Pool when churn warrants it, and reset state, timers, subscriptions and outstanding work before reuse.

## Applicability and exceptions

Culling, batching, distance detail and pooling have CPU, GPU, memory or visual tradeoffs. An AI update can be cheap enough to leave alone. A persistent merchant or quest target may need to advance even while its visual representation is unloaded. Measure on the intended device and representative density.

## Checks

Repeat an entry → encounter → exit → reentry route and verify that the same NPC ID retains the required survival and quest state. Use a populated route and a near-worst case. Compare first-load and repeat-entry time, frame tails, resident memory on return and required visual cues. Test cancellation and a pooled object's second lifetime. [Performance measurement](../code/K-CODE-PERFORMANCE-MEASUREMENT.md) · [World lifecycle verification](../../skills/vegabond-code/references/world-lifecycle-verification.md)

## Evidence

The practices survey records Unity and Unreal profiling references and production examples for rendering, spawning, AI and offscreen objects. Its example route is a proposed project check. [Game development practices](../../docs/research/2026-11-22-game-development-practices.md)

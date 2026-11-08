# Technique Lab Implementation Plan

> **For agentic workers:** Use superpowers:executing-plans inline; this authorized experimental spike does not introduce production features. Do not spawn workers merely to satisfy the plan.

**Goal:** Run three representative techniques in Unity and record reproducible behavior/performance evidence with applicability limits.

**Architecture:** Separate camera, native-physics shooting and graph kernels from independent checks and a shared scene consumer. The editor compiles/checks/builds; a runtime MonoBehaviour exercises actual Update/physics and emits measurements.

**Tech Stack:** Installed Unity 6000.0.77f1, C#, built-in renderer/physics, Windows Mono player, no registry dependencies.

**Spec:** [Prototype design and acceptance](../../../prototypes/TechniqueLab/README.md).

## Global constraints

- Work only in the new OneStep prototype and its evidence/docs/knowledge updates; preserve existing work.
- Keep English guidance canonical and regenerate Korean companions without reading them.
- Keep frame pacing, operation CPU timing, rendering and whole-game performance distinct.
- Record observed hardware/build settings and raw samples; no production or other-platform guarantees.

## Review focus

- Inside-collider ray origins and animated muzzles must not bypass cover.
- Zero-cost links and asymmetric costs must not cycle or reverse the wrong weight.
- Changed navigation topology must invalidate cached successors before movement consumes them.
- FPS caps may not be achieved; record actual Update timing and exact integration interval.
- Initialization/JIT, allocations, asset creation and logging must not masquerade as operation timing.

## Tasks

1. Confirm a real engine invocation produces a probe record; if blocked, resolve the capability before claiming execution.
2. Write independent engine assertions and minimal kernel contracts; run the intentionally incomplete state and retain the failing assertions.
3. Implement the three kernels, repeat the original assertions, and preserve broken comparison modes as sensitivity controls.
4. Create a camera/light scene and a runtime visual/benchmark consumer. Run editor PlayMode, build a standalone Windows player, and run its automated path in repeated sessions.
5. Inspect captures and distributions. Fix confirmed defects, repeat affected checks, and update only the knowledge claims supported by the observed conditions.

No commit, push, deployment, production integration or paid asset/service is part of this request. Retain source and evidence for reproducibility.

## Execution outcome

All five tasks executed. Final Editor PlayMode and three sequential Windows Mono players each passed 27 checks and three actual elapsed-time trials. Build succeeded with zero errors; current C# hashes match player manifests. Native controls were inspected separately from world-only captures. Independent final review found no remaining correctness blocker within the prototype scope.

Red/green evidence retains incomplete kernels, graph identity versus revision-only validity, and early errors erased by assertion-count assignment. Batches now target 3 ms rather than guaranteeing every sample meets it. Public graph mutation, in-flight door reconciliation, network authority, GPU cost and player experience remain explicit limits. [Results](../../../prototypes/TechniqueLab/RESULTS.md) and existing knowledge carry findings; no production integration or commit occurred.

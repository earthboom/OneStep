---
id: K-CODE-GC-LIFETIMES
title: Separate garbage collection, resource cleanup, and memory diagnosis
summary: Garbage collection reclaims eligible unreachable managed objects, while useful lifetime and prompt resource cleanup still need explicit design. Diagnose growing memory with reachability, allocation, and fragmentation evidence before choosing a fix.
kind: reference
scope: .NET managed-memory diagnosis and Unreal UObject references; source-specific mechanisms rather than guarantees for every garbage collector
keywords: [garbage collection, GC, reachability, retention, memory leak, fragmentation, allocation churn, IDisposable, UObject, TObjectPtr, 메모리 관리, 가비지 컬렉션, 메모리 누수, 객체 보존]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: 'Microsoft Learn and Epic primary documentation inspected on 2026-11-07; Epic served Unreal Engine 5.8'
  application_status: 'Reference synthesis; no target process, heap dump, profiler session, or resource-cleanup test executed'
---

# Separate garbage collection, resource cleanup, and memory diagnosis

## Guidance

Distinguish three questions: whether an object remains reachable, whether the application still needs it, and whether an external resource must close now. In .NET, GC discovers unreachable managed objects from roots and reclaims eligible memory during collections. It cannot infer that a reachable cache entry is useless, and it does not release every kind of memory or native handle.

Use the documented disposal contract for owned disposable resources. Microsoft distinguishes `Dispose` cleanup from reclaiming the managed object's storage. An object can be disposed yet remain reachable; ownership determines whether a containing object should cascade disposal. Prompt file or socket closure needs an explicit resource protocol rather than reliance on collection timing.

For Unreal, examine the actual `UObject` reference kind. Epic's current table distinguishes strong, weak, and soft references; `TObjectPtr` is GC-safe only when marked `UPROPERTY`. `TStrongObjectPtr` also affects GC outside reflected fields. A pointer-shaped value alone does not establish engine-tracked reachability.

## Applicability and exceptions

Apply the .NET statements to CLR-managed objects and the Epic statements to the documented engine version. Native allocations, GPU resources, allocator caches, and engine subsystems require their own accounting. GC eligibility is not a promise of immediate reclamation or immediate reduction in process memory. Collection policies differ across runtimes; do not translate the exact .NET algorithm into an Unreal guarantee.

## Checks

Proposed diagnostic sequence:

- Reproduce a fixed workload and compare settled baselines. Separate outstanding allocations with lost ownership, reachable-but-unwanted retention, fragmented free space, and rapid temporary allocation churn; growth alone does not identify which occurred.
- Compare managed heap size, allocation rate, collection behavior, and process/native memory. Inspect dominant types and root paths; Microsoft's tutorial uses counters, dumps, `dumpheap`, and `gcroot`.
- For suspected retention, inspect cache limits, subscriptions, and task captures. For resource exhaustion, count live handles and verify disposal separately. For Unreal, inspect reflected reference tracking and unintended strong references.

## Evidence

Source observations checked on 2026-11-07:

- [Microsoft: GC fundamentals](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/fundamentals): Memory release, Unmanaged resources, and fragmentation discussion.
- [Microsoft: implement Dispose](https://learn.microsoft.com/en-us/dotnet/standard/garbage-collection/implementing-dispose): introduction, Cascade dispose calls, and Dispose() versus managed-storage release.
- [Microsoft: diagnose a leak](https://learn.microsoft.com/en-us/dotnet/core/diagnostics/debug-memory-leak): Examine managed memory usage and Analyze the core dump; tutorial applies to .NET Core 3.1 onward, tool output varies.
- [Epic: object pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine): pointer table footnotes, TObjectPtr, and TStrongObjectPtr; UE 5.8.

Microsoft pages displayed authorization notices but exposed the cited body text. No local measurements were taken; proposed checks establish no diagnosis or verified safeguard here.

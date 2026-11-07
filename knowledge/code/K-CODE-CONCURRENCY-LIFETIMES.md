---
id: K-CODE-CONCURRENCY-LIFETIMES
title: Review asynchronous lifetime, synchronization, and shutdown as separate contracts
summary: Keeping an object alive does not synchronize its mutable state or prove that background work finishes. Review ownership across suspension, publication ordering, cancellation, completion, and cleanup independently using the actual language and runtime contracts.
kind: reference
scope: Concurrent and asynchronous API review informed by C++ shared_ptr, Rust Send/Sync and destructors, and the Go memory model
keywords: [concurrency, lifetime, cancellation, synchronization, safe publication, shared_ptr, Send, Sync, Drop, Go memory model, 동시성, 비동기 수명, 취소, 동기화, 안전한 공개]
status: active
checked_at: '2026-11-07'
relations:
  requires: [K-CODE-RESOURCE-OWNERSHIP, K-CODE-API-CONTRACTS]
context:
  evidence_check: 'Primary language documentation inspected on 2026-11-07; current C++ working draft rendering, live Rust documents, Go memory model version 2022-06-06'
  application_status: 'Reference synthesis and proposed review protocol; no scheduler, race detector, cancellation, or shutdown scenario executed'
---

# Review asynchronous lifetime, synchronization, and shutdown as separate contracts

## Guidance

Review three obligations independently: valid data access, coordination of conflicting access, and shutdown with unfinished work. A local RAII wrapper does not prove that a callback or worker has stopped using its resource. Treat task ownership and cleanup order as part of the interface.

The C++ draft separates `shared_ptr` bookkeeping from pointed-to state for data races. Reference counting does not protect mutable fields; review the pointer variable separately from distinct owners. With aliasing constructors, shared ownership does not extend an unrelated stored target's lifetime; dereferencing it requires a valid target. A reference count is not a synchronization protocol.

Rust's `Send` permits ownership transfer between threads and `Sync` permits shared reference access under their trait contracts. `Rc` does not supply these concurrency guarantees; manually implementing the traits requires unsafe reasoning. The Reference also permits intentionally suppressed destruction and process termination without unwinding. Compile-time safety does not establish leak freedom, deadlock freedom, or eventual task completion.

Go's memory model specifies publication and visibility through synchronization. It explicitly says goroutine exit alone is not synchronized before another event. Use the applicable channel, lock, or atomic contract when another participant must observe an effect.

## Applicability and exceptions

These are comparisons of specific language contracts, not interchangeable guarantees. Framework task cancellation may request cooperation, discard a result, drop a future, or interrupt work; inspect the actual API. Holding an object alive does not establish thread affinity, engine validity, or permission to call every method. Unsafe code and foreign interfaces add obligations outside ordinary safe-reference reasoning.

## Checks

Proposed implementation checks:

- Trace captured references and owners across queueing, suspension, callbacks, retries, and owner destruction. Name the completion event that permits cleanup.
- Draw the publication and conflicting-access ordering; identify its channel, mutex, atomic, or documented executor guarantee. Review lock ordering and waits separately.
- Exercise cancellation before start, during work, and during teardown. Verify whether completion is awaited, who releases resources, and whether callbacks can arrive afterward.
- Reproduce shutdown under contention with available race diagnostics and bounded completion assertions. A passing run samples schedules; it is not a proof of every interleaving.

## Evidence

Source observations checked on 2026-11-07:

- [C++ working draft: shared_ptr](https://eel.is/c++draft/util.smartptr.shared): [util.smartptr.shared.general] paragraphs 1 and 5, aliasing-constructor note 1, and use_count observer notes; mutable draft rendering, not a pinned published standard.
- [Rust Book: Send and Sync](https://doc.rust-lang.org/book/ch16-04-extensible-concurrency-sync-and-send.html): transfer, shared access, and manual implementation sections.
- [Rust Reference: destructors](https://doc.rust-lang.org/reference/destructors.html): Drop scopes and Not running destructors; live Reference.
- [Go memory model](https://go.dev/ref/mem): June 6, 2022 version; Advice, Goroutine destruction, and Channel communication.

All cited text was readable. No runtime safety or liveness check was executed; the review protocol remains proposed.

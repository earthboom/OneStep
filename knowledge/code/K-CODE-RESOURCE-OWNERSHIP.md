---
id: K-CODE-RESOURCE-OWNERSHIP
title: Make resource ownership and borrowing explicit at module boundaries
summary: Give each resource an identifiable cleanup owner, express transfers and borrowing in interfaces, and introduce shared ownership only when independent lifetimes require it. C++ RAII, Rust ownership, and Unreal UObject management impose different contracts.
kind: reference
scope: Resource and interface design in C++, Rust, and Unreal Engine; source-based comparison rather than a universal language guarantee
keywords: [ownership, borrowing, RAII, unique_ptr, shared_ptr, weak_ptr, Rust, Drop, Unreal Engine, UObject, 소유권, 빌림, 자원 수명, 순환 참조]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: 'Primary documentation inspected on 2026-11-07; mutable online editions, including Unreal Engine 5.8 documentation'
  application_status: 'Reference synthesis; proposed review checks, with no local implementation or runtime verification'
---

# Make resource ownership and borrowing explicit at module boundaries

## Guidance

Start an interface review by asking who releases each resource, who may temporarily use it, and what event ends that permission. Include files, sockets, locks, and native handles alongside heap memory. Prefer a lifetime contract that a maintainer can understand without tracing every caller.

In C++, the Core Guidelines recommend RAII wrappers for paired acquisition/release and unique ownership unless sharing is needed. Ordinary scope exit and exception unwinding release correctly constructed automatic wrappers; this does not establish asynchronous completion. Strong `shared_ptr` cycles can prevent reclamation. Choose a weak back-reference only when it matches the ownership model.

Rust makes ownership moves and borrowing visible in types. The Book's `String` example releases its allocation through `drop` at the owner's scope boundary. References borrow rather than own; safe reference rules constrain validity and simultaneous mutable access. These mechanisms help local reasoning, but do not make every resource protocol automatic.

Unreal's `TSharedPtr`/`TUniquePtr` family manages ordinary C++ objects. Epic explicitly separates this library from `UObject` management. Select the engine's object-reference mechanism for `UObject` lifetimes instead of transferring deletion to an ordinary smart pointer.

## Applicability and exceptions

Use this comparison when reviewing ownership-heavy APIs or moving between these ecosystems. A borrowed view can still become invalid if its contract is violated. Legacy raw pointers may encode ownership despite a recommended convention; inspect their actual contract. Custom allocators, arenas, foreign interfaces, and framework-managed lifetimes need their own release rules. RAII does not promise cleanup after abrupt termination, or prove thread safety.

## Checks

Proposed review checks:

- Trace one acquisition through success, early return, failure, and transfer; identify exactly one cleanup responsibility for each owning path.
- Inspect returned views, callbacks, and stored references against their backing owner's lifetime. Explain each shared owner and inspect strong cycles.
- Confirm whether each Unreal target is a `UObject` before selecting its pointer family. Test cleanup behavior in the actual project before claiming prevention.

## Evidence

Source observations checked on 2026-11-07:

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines): R.1, R.21, R.24; recommendations, not a compiler-enforced ownership system.
- [Rust Book: ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html): Ownership Rules and Memory and Allocation; live Book edition.
- [Rust Book: references](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html): Mutable References and Dangling References; safe-reference examples.
- [Epic: smart pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-pointers-in-unreal-engine): introduction and Tips and Limitations; served as UE 5.8.

Pages were readable. No project cleanup scenario or sanitizer run was executed; checks above remain proposed.

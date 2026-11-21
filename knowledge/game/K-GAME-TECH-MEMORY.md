---
id: K-GAME-TECH-MEMORY
title: Check buffer bounds and object lifetimes in game data handling
summary: Validate both byte ranges before copying and keep original weak object identity
  across delayed work.
kind: reference
scope: Game development. For native C++ builds with supported instrumentation, Clang
  AddressSanitizer (ASan) detects many executed out-of-bounds accesses and use-after-free
  errors.
keywords:
- memory
- safety
- ACE
- bounds
- lifetime
- 임의코드실행
- 임의 코드 실행
- CWE-787
- out-of-bounds write
- AddressSanitizer
- ASan
- use-after-free
- dangling pointer
- C++
- 버퍼 경계
- state preservation
- weak object pointer
- delayed callback
- 상태 보존
- 지연 콜백
- 객체 교체
- 객체 수명
status: active
checked_at: '2026-11-21'
context:
  application_status: Scoped local Unreal Win64 evidence for synthetic record bounds
    and weak target lifetime.
---
# Check buffer bounds and object lifetimes in game data handling

## Guidance

MITRE classifies a write before or after the allocated buffer as `CWE-787` (Out-of-bounds Write). It can corrupt neighboring data or crash a program. When loading save files, assets or network messages in C++, verify each length and offset before forming a pointer or writing. After checking offset ≤ capacity, compare count against capacity minus offset, taking element size and signed-to-unsigned conversions into account.

## Applicability and exceptions

For native C++ builds with supported instrumentation, Clang AddressSanitizer (ASan) detects many executed out-of-bounds accesses and use-after-free errors. A dangling pointer refers to an object whose lifetime has ended. Even an in-range index is unsafe if the owner has released or reallocated storage. A clean run covers only executed paths. Arbitrary code execution (ACE) is a possible consequence of some failures and does not identify their underlying weakness.

## Checks

Exercise empty, truncated, exact-fit and oversized records in a supported instrumented build. Verify that rejection leaves the destination state valid. Check callback and view lifetimes across scene unload and buffer reallocation. Attribute a diagnostic to the first invalid access and its allocation lifetime.

## Evidence

MITRE defines the weakness and Clang documents ASan coverage and instrumentation. A public historical game replay demonstrates an observed outcome, without establishing a particular buffer bug. No sanitizer run or particular game defect was verified in this review.

- [MITRE — CWE-787: Out-of-bounds Write](https://cwe.mitre.org/data/definitions/787.html)
- [Clang — AddressSanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)

## Applying Unreal buffer and lifetime checks

Validate the record header and the source and destination ranges before forming copy pointers or mutating state. Check each offset before comparing the requested length with the capacity remaining after that offset. Define whether a zero-length operation at a valid endpoint is allowed. Leave the destination unchanged when a record is rejected.

Capture the original target as a `TWeakObjectPtr` when scheduling a game-thread callback. Resolve it when the callback runs and apply the update only if the original object is still valid. Looking up the target again in a mutable slot can deliver a stale update to a replacement object.

Use AddressSanitizer diagnostics for the instrumented build and the code paths that actually ran. Record the build and paths alongside the diagnostic result.

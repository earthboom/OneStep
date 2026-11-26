---
id: K-GAME-TECH-SAVE
title: Design versioned durable saves and compact password states
summary: Persist stable-ID progress with a versioned container or a compact progress code.
  Unreal checks cover staged A/B restart recovery and a 14-symbol V54 code that restores
  a fixed world state in a separate process.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["save", "serialization", "checksum", "password", "bitflags", "저장", "세이브", "백업", "저장손상", "USaveGame", "UGameplayStatics::AsyncSaveGameToSlot", "save generation", "game state", "stable ID", "SaveGame", "CRC32", "previous generation", "file truncation", "both invalid", "게임 상태", "상태 복원", "이전 세대", "파일 잘림", "양쪽 무효"]
status: active
checked_at: "2026-11-21"
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: UE5.8.3 V20 staged A/B process termination and real NTFS exhaustion,
    V54 versioned 14-symbol code with four restart pairs, eight rejections, and three matched cost runs.
    Physical power loss remains unverified.
---
# Design versioned durable saves and compact password states

## Guidance

Serialize persistent state, stable object identifiers and schema version rather than raw runtime pointers. Pack independent flags into bits when useful. Password saves encode a small reconstructible state into a restricted alphabet with error detection. Proposed durability design: validate a new save before replacing the known-good slot and retain a recoverable generation.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

Emerald's public reconstruction writes sector groups using a save counter to select a slot and tracks the last known good write state; loading validates sector data and selects a valid generation. This is a historical reconstruction, not Nintendo-authored source or a tested local save system. For a new implementation, use generation IDs, payload validation and a documented commit/recovery order; do not assume two files alone are atomic. The original Simon's Quest reverse-engineering FAQ describes seven state bytes, a two-byte additive check and a scrambling byte, encoded into a 16-character password. Item/experience/day state is reconstructed, not an exact paused-world snapshot.

## Applicability and exceptions

A checksum detects some corruption; it is not tamper-proof authentication. Eight bits store eight independent yes/no flags, not hundreds of millions of independent events. Two slots alone do not prove atomic filesystem behavior.

For Unreal saves, `USaveGame` represents game-defined persistent data. `UGameplayStatics::AsyncSaveGameToSlot` serializes the object on the game thread, writes the platform data on a worker thread and reports success or failure via a completion delegate on the game thread. A scheduled operation still needs a completion check. Inject a failed write and verify the previous valid generation remains readable on the target platform. [Epic — UGameplayStatics::AsyncSaveGameToSlot](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UGameplayStatics/AsyncSaveGameToSlot?application_version=5.8)

## Checks

Record the candidate, publication boundary and expected generation before running a fault test. Kill the writer from a separate process at named write boundaries and restart against the same directory. Compare published bytes and the complete restored world, including an invalid-data or missing-binding case whose live state must remain unchanged. Treat process termination, a capacity-limited write, and physical power loss as distinct tests.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Epic — Saving and Loading Your Game](https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine) — Official documentation; custom SaveGame and asynchronous saving. Checked 2026-11-07, except items explicitly marked further reading.
- [pret/pokered — save.asm](https://github.com/pret/pokered/blob/master/engine/menus/save.asm) — Community disassembly artifact, not Nintendo-authored source; inspected as historical implementation evidence, no ROM built. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V20, V54 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

### Follow-up evidence

- [pret/pokeemerald — save.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/save.c) — HandleWriteSector, save generation selection and validation text inspected; community reconstruction; no ROM build or fault injection. Checked 2026-11-07.
- [kingshriek — Simon's Quest Password System FAQ](https://gamefaqs.gamespot.com/nes/587179-castlevania-ii-simons-quest/faqs/38582) — Original reverse-engineering account, generation/decoding sections; exact ROM behavior not independently executed; do not copy apparent transcription errors as a tested decoder. Checked 2026-11-07.

## Native Unreal validation — 2026-11-14

The historical Unreal run and its archived measurements.

One synchronous game-thread owner captures health/checkpoint,32 item flags and8 switch flags with stable sorted IDs. Canonical state is348bytes,stored in one UPROPERTY(SaveGame) byte array inside a USaveGame object. Packaged serialized payload is2393bytes;the40byte envelope makes each file2433bytes in all six cost runs. Basic uses slotA;recovery uses A/B with the same validation and per-file bytes. Recovery retains two files,so total disk footprint differs. This is a gameplay-state restoration prototype;the earlier asynchronous diagnostic-log pipeline is a different technique/use case.

Check magic,version,schema,exact bounded length,headerCRC32 and payloadCRC32 before engine deserialization. Then validate canonical counts,IDs,values and schema. Load selects the highest valid generation;one valid plus one invalid reports Recovered. All missing is Missing;no valid regular file is Invalid;equal valid generations are Conflict. Failed load preserves live state. Load never rewrites/repairs files. Save chooses the invalid/older slot,advances generation and reads back/validates bytes before success. Both-invalid,conflict and uint64 generation exhaustion refuse overwrite. A complete valid newer container can be selected even if its producer never acknowledged success. This defines valid-container selection,not transactional acknowledgment or physical durability.

Restoration validates the complete stable-ID binding before any mutation. Forty actual props display item collection by mesh visibility and switch state by yaw;avatar transform and game fields reflect health/checkpoint. Newly restarted processes spawn props in reversed order. Independent Python checks actual IDs,visibility,rotation,avatar transforms and canonical bytes. It finds/validates the single canonical byte-array inside the opaque UE payload;it is not a complete independent UE serializer. No raw runtime pointers are persisted.

89native policy checks and23real USaveGame/store checks pass. Actual PIE and packaged players each run12cases per mode:missing,A roundtrip,newestB,truncation,byte corruption,unsupported envelope schema,both invalid,save refusal preserving both invalid files,blocked-destination write failure,checksummed but semantically invalid state,missing world binding with atomic refusal,and duplicate saved ID. Total48native behavior cases. Six separate packaged restart consumers verify normalB,basic truncation failure,recovery truncation/corruption fallbackA,and both-invalid preserving mutated liveD. Producer files are copied only into owned consumer sessions;pre-copy hashes,unchanged producer files,distinct PIDs and execution chronology are independently checked. The blocked destination is a controlled directory/write failure,not an injected partial-write failure;truncation is tested separately. CRC golden vector,ties and max-generation refusal have actual native unit-store files.

Six sequential packaged players in basic/recovery,recovery/basic,basic/recovery order. Same alternating state sequence,40props,camera,1280x720,DX11,Development,cap0,noVsync,no audio/capture. Each run has32warmup and256measured save+mutate+load+restore cycles,one per frame. GT blocking is capture+save+load+world restore;contiguous operation also includes scripted live mutation and surrounding overhead. Save includes prior-generation scan,UE serialization,file write and validation readback. Load includes file reads,validation and UE deserialization. Whole OnBeginFrame-to-OnEndFrame wall and cadence include engine/HUD/constant observations/result-row creation. Startup,result JSON,exit and media capture are outside the measured window. Detailed capture/restore/median/GPU timings remain in summary.json. These are OS-buffered local-file measurements,not isolated physical device latency. Retain the slower first basic run;host load and caches are uncontrolled,so do not claim recovery is faster.

Two real native processes produce6seconds of A/B state and8seconds of freshD/loadB/truncated-newest recoveryA/both-invalid preservingD.420actual PNG frames,14seconds,30simulation/30playback,normal1x;startup/tail trimmed only,chronological clips concatenated without retiming. All native and decoded serial/phase markers and16800state cells each are checked against independently validated world/state. Six final native screenshots were directly inspected. This establishes visible native state transitions and real restart provenance;it is not a recording of real-time save stalls or proof of actual30FPS throughput.

Use A/B recovery when reverting to a previous valid generation is preferable to losing all progress. Keep stable IDs,validate completely before applying,and present explicit failure when both generations are invalid. Retain evidence rather than silently replacing invalid saves with defaults. CRC detects accidental corruption and is not authentication;only trusted locally produced UE class/format was tested. Fixed schema1 and fixed32/8IDs have no migration or cross-engine-version guarantee. Graceful process restart and controlled truncation/corruption do not establish forced-crash,power-loss,fsync,full-disk or device-failure safety. Synchronous stalls remain;no asynchronous optimization,password,V54 decoder,autosave tool,cloud,renderer or verification-framework expansion. Previous unrelated actual-FPS gaps remain unverified.

Corpus coverage at that stage was 25 limited sheets and 18 without dedicated prototypes. V54 is covered in the later section below.

## Staged publication and schema migration in Unreal — 2026-11-21

Keep the active generation and inactive slot addressable while writing a candidate to a sibling pending file. Flush and close the candidate, read it back and validate its bytes and state, then replace the inactive slot. On load, consider published slots only. Publication determines what a restart may select. A process can be terminated after publication and before the caller receives a success result. This implementation uses same-directory Windows replacement and a single game-thread writer. [Microsoft — MoveFileExW](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-movefileexw)

In the Win64 Development prototype, the staged candidate remains private if the process stops after serialization, staging open, prefix write, payload write, flush/close, or readback validation. The published generation is selectable after the replacement returns. Use the known-good generation to check both on-disk contents and restored state after restart. A deliberately limited writer produced a real 128-byte pending file before reporting a simulated disk-full error. The subsequent isolated NTFS trial exercises the operating system's capacity limit separately.

Migrate recognized legacy data into a new current-schema value before touching the live world. The exercise's synthetic v0 preserves health, checkpoint and item flags. The eight switch flags added in v1 default to off. Invalid legacy values cause fallback to another valid slot or explicit failure. Preflight all current world bindings before applying a candidate. When either decoding or binding fails, compare the full before/after world and leave the stored files unchanged.

UE 5.8.3 Win64 Development passed 36 writer/restart pairs on one package, three per condition. The 21 external terminations covered seven boundaries. The other cases covered the capacity limit, valid v0, invalid v0 with and without a valid alternative, and a missing world binding. A/B files and pending bytes were tracked independently across the restarts.

Apply this result to a single writer using this file layout and tested fault boundaries. Process termination leaves the operating system running. Power loss, interruption inside a filesystem call, competing writers, and migration from shipped formats each require separate validation. The earlier save timings describe the old direct-write path. Recheck frame stalls before driving the flushed staged path from gameplay.

## Actual NTFS exhaustion on Win64 — 2026-11-21

Capture the operating-system error immediately on a failed call, before cleanup or logging. Keep the operation, error code, requested bytes and completed bytes together. A free-space estimate can inform the UI. The write result determines whether the candidate can advance to validation and publication. [Microsoft — WriteFile](https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-writefile) · [Microsoft — Windows system error codes](https://learn.microsoft.com/en-us/windows/win32/debug/system-error-codes--0-499-)

The UE 5.8.3 Win64 Development comparison used a 64 MiB fixed-size VHDX formatted as NTFS, with 4,096-byte clusters and reports on the host volume. Three normal saves each published a 2,433-byte generation 3 and loaded it after restart. With zero available bytes, the 64-byte prefix remained in the private pending file, and the payload call to WriteFile returned ERROR_DISK_FULL (112) in all three trials. Both published slot hashes and the writer's live world remained unchanged. Restarting while full loaded generation 2. Freeing the test filler allowed each retry to publish generation 3, which a further restart loaded.

Keep the test filler on a separate mounted volume and measure free space after closing it, because a file close can release unused preallocation. Under write, flush, or replace failure, preserve the published slots and present explicit failure to the caller. Once space is restored, run the normal staged save again and verify the resulting slot bytes and complete world on restart. This evidence covers an existing save directory, one writer and the file layout above. Repeat on the production storage and filesystem if that deployment differs.

## V54 compact progress code in Unreal — 2026-11-21

Use a fixed, documented field order and a version for reconstructible game progress. This prototype packs version (4 bits), health 0–100 (7), checkpoint 0–3 (2), 32 item flags and eight switch flags into 53 bits. A CRC-16 with polynomial 0x1021 and initial value 0xffff covers seven little-endian payload bytes, including three zero high bits. The code carries those 53 bits, the 16-bit checksum and one reserved zero bit as fourteen five-bit symbols, low group first. Its alphabet omits I, O, 0 and 1. The independent checker generates the same code with a separate packing implementation and Python's CRC routine. [Python binascii.crc_hqx](https://docs.python.org/3/library/binascii.html#binascii.crc_hqx)

Validate length, alphabet, reserved bit, checksum, version and field range before assigning a decoded candidate. Use stable object IDs and validate the complete bindings before applying that candidate to the world. Keep the previously published version's ID order fixed if the content layout changes. A code is readable, copyable game progress with accidental input error detection. The checksum does not authenticate the progress.

Four native create/restart pairs use only a code supplied as a launch argument. They reproduce the same code across processes and restore normal, minimum and maximum states with all 40 bindings. Eight native invalid inputs preserve the full live world, including a correct-checksum unsupported version and a correct-checksum out-of-range health. Each producer rejected all 434 single-symbol substitutions of its own code without changing the decoder output. This prototype uses a fixed local state schema and launch-argument input.

Three Win64 Development runs used the same four valid states and order at 1280×720. Each stage ran 8,192 timed operations after 1,024 warmup operations. The p95 of per-batch average operation cost across the three runs was 0.291–0.375 µs for encoding, 0.609–0.728 µs for decoding, and 4.178–6.972 µs for applying the world state. These timings describe valid inputs and 40 fixed bindings. Recheck costs and code length when the reconstructible state grows.

---
id: R-CODE-UE-MUSIC-STOP
title: Duplicate stop prolonged an audio fade and delayed restart
summary: A duplicate stop reinitialized a ten-millisecond fade,so restart waited for
  an unnecessarily later endpoint. Keep already-stopped handling idempotent while
  still allowing cancellation of a pending restart.
kind: error
scope: OneStep UE5.8.3 bounded sample-owned adaptive music prototype;fixed calibration
  fixtures
keywords:
- music
- audio
- duplicate stop
- idempotent
- fade
- restart
- deadline
- 중복 중단
- 페이드
- 재시작
status: resolved
checked_at: '2026-11-14'
trigger: Repeated stop while a stop fade is unfinished,followed by restart
symptom: Native314policy checks had2failures:duplicate stop shifted fade completion
  and delayed restart
cause_status: confirmed
prevention: Verify a passing baseline;duplicate stopped-state requests preserve original
  fade endpoint and do not add a new stop transition
prevention_status: verified
---

# Duplicate stop prolonged an audio fade and delayed restart

## Expected and observed

Stopping at sample2000 with480sample fade should end at2480. Duplicate stop2100 must not move that endpoint;restart2500 should start immediately. Native policy checks instead delayed it to2580 and reported a second stop.314checks/2failures are preserved. This is a native policy reproduction,not a claim that the earlier50-input pilot audio contained duplicate stops.

## Cause and resolution

Unconditionally calling Apply(stop) reset gain.From/Begin even when transport was already stopped. Now clear pending changes/restart as requested,but only begin a stop fade when transitioning from playing. An already-stopped duplicate preserves the original ramp;canceling a pending restart remains possible. Restart waits only for the original silence endpoint.

## Recheck and prevention

314native checks pass after repair. The final51-input trace includes stop249600,duplicate249624,restart249648;restart commits250080,not250104. Actual20second mixedPCM matches independently derived waveform in all11finalplayers. These scoped checks demonstrate this bounded player's behavior,not general audio concurrency or production music quality.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- Historical Unreal lab run and archived measurements, checked 2026-11-14.
- Local retained RED:Results/Music/model-stop-red/model.json;GREEN:Results/Music/model-final-v2/model.json. Native implementation/evidence remain local prototype materials.

---
id: K-GAME-TECH-MUSIC
title: Schedule adaptive music at musical boundaries
summary: Keep layers phase-aligned and schedule compatible section changes on beat/bar
  boundaries with explicit late-request,cancellation and idempotency rules. UE5.8.3
  native sample-owned fixed-fixture output/cost evidence exists;not Quartz,musical
  quality or live-ingress certification.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["adaptive", "music", "stems", "transition", "vertical", "horizontal", "음악", "vertical layering", "horizontal resequencing", "tempo map", "beat-synchronous transition", "sample clock", "beat", "bar", "safe lead", "duplicate stop", "restart", "reversal", "actual PCM", "layer add remove", "음악 레이어", "박자", "마디", "예약", "중복 중단"]
status: active
checked_at: "2026-11-19"
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V25 UE5.8.3:314policy/4actualworlds51inputs/6matchedcosts/20s1xWITHactualaudio;fixed120BPM4/4
    native sample owner,notQuartz/composition/liveingress
---
# Schedule adaptive music at musical boundaries

## Guidance

Use synchronized stems for vertical layering and compatible sections for horizontal resequencing. Map gameplay state to musical intensity, then schedule transitions on beats/bars or authored cues. Track tempo, meter, entry/exit points, transition segments and crossfade policy.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Randomly concatenating clips does not guarantee musical continuity. Composer terminology varies; describe the actual scheduling operation. A brief combat toggle should not cause constant musical restarting.

In **vertical layering**, synchronized stems share a musical timeline and the mix changes by adding or removing layers. In **horizontal resequencing**, the score moves to another compatible section at a musical boundary. A tempo map converts beat or bar positions into playback time as tempo changes. Request a transition immediately before and after a tempo change and verify the audible handoff, including any pickup or decay tail. [Kent Carter / Guy Jones — Composer interview on adaptive music](https://www.gamedeveloper.com/audio/composer-guy-jones-talks-adaptive-music-for-games)

## Checks

Native fixed-fixture subset below checks sample boundary offsets,rapid reversals,duplicates,late lead,stop/restart and actual mixed/encoded audio. Arbitrary loading stalls,live ingress and subjective listening/music quality remain unverified.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Kent Carter / Guy Jones — Composer interview on adaptive music](https://www.gamedeveloper.com/audio/composer-guy-jones-talks-adaptive-music-for-games) — 2021 direct composer interview text; stems, sections and tempo maps. Embedded podcast not played. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V25 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

## Native Unreal validation — 2026-11-14

The the historical Unreal run and its archived measurements.

One native USoundWaveProcedural source mixes three fixed calibration fixtures: section A440Hz, section B660Hz and added layer990Hz. These are fixed one-second PCM lookup tables, not composed/generative music. All use48kHz,120BPM,4/4; beat=24000frames(.5s),bar=96000frames(2s). The source sample counter owns phase and changes. This is a scoped native sample-owned implementation, NOT a local Quartz validation. Quartz PlayQuantized is a production alternative for playback scheduling, but no atomic quantized stop/layer-removal/reversal extension was added here. No new content assets, dependencies, engine or shared tool changes.

For section/layer request at frame f,quantum Q and phase origin O,scheduled target is O+ceil((f-O+4800)/Q)*Q. A full100ms lead is required,inclusive;one sample later than the threshold skips to the following safe boundary. Immediate mode applies at f. Section and layer have independent pending slots. Identical pending requests keep the original target;requesting the active value cancels the pending reversal. Last target wins before commitment. Applying section crossfades A/B;layer adds/removes its own gain without restarting transport. Gains ramp linearly for480frames(10ms);oscillator/fixture phase continues through changes. Stop cancels pending changes and ramps to silence. Duplicate stop does not restart the ramp. Restart means start after stop;it waits for an unfinished stop ramp,then starts A/no layer at a new phase origin. Restart while already playing is an idempotent duplicate,not a force-rewind operation.

314native policy checks pass. Four actual worlds (PIE/package × immediate/scheduled) each consume the same51authored sample-domain requests over20seconds. The trace covers beat/bar lead thresholds,one-sample before/at/after,rapid reversal,identical requests,independent pending states,insufficient lead,stop cancellation,duplicate stop,restart during a stop ramp and normal restart. The trace is submitted ahead of playback;it does not validate arbitrary live game-thread/network ingress latency. Scheduled mode applies27changes versus immediate45 by design;coalescing is distinct from losing an accepted queued transition. Independent Python derives sparse event/commit times and full fixture waveforms without calling native policy functions. All11final players,including six cost players and media,compare960000actual mixed samples each against that reference. One constant master gain per run is fitted;relative layer gains,phase,timing and silence are checked across the full trace,not fitted separately per segment. This is not absolute output-volume or hardware/DAC calibration.

Six sequential packaged players,immediate/scheduled,scheduled/immediate,immediate/scheduled order. Same three lookup fixtures,51requests,20second trace,1280×720,DX11,Development,cap0,noVsync and one source. Each measures the source interval2..18s:767488stereo source frames in identical512-frame callbacks. Actual masterPCM recording stays ON in every arm;reported costs include this shared experiment path. Source callback CPU includes procedural allocation/lock/mixing/state processing/instrumentation through its timer,not the entire audio-engine render thread. Per-input policy CPU covers all51requests,including those outside the callback window. GT upfront enqueue time is recorded separately and excluded from steady-state frames;GT audit timing is in summary. Whole OnBeginFrame→OnEndFrame wall/cadence include engine/HUD/audit/row creation. Result JSON,startup,exit,PNG/video encoding are excluded. Tiny sub-microsecond policy values approach timer granularity;three short uncontrolled runs do not establish superiority or hardware-general budgets. Matching offered inputs does not force matching committed changes;27/45is the declared policy difference.

Initial native stub:48checks/42failures,then48GREEN. Added duplicate-stop checks reproduced314checks/2failures:repeating stop restarted its fade and delayed restart. Idempotent already-stopped handling fixed314/314;the final trace contains the duplicate and actual output matches the corrected policy. First hidden PIE correctly failed because EditorEngine overwrote app volume0 without background audio. Reused SoundLab temporary bAllowBackgroundAudio and restored it without SaveConfig;failed output is preserved. Final fresh review found negative evidence tests reading the preserved failed PIE fixture,so assertRaises could pass before testing mutations. An unconditional unmodified-baseline acceptance check reproduced RED(error1/0tests);retargeting the accepted v2 fixture yielded8GREEN. The full746suite was rerun after correction. Preserve prereview logs as invalidated prevention evidence,not final proof.

Reuse the phase-owning clock and independent pending slots when adding/removing synchronized layers or changing compatible sections. Validate actual mixed output;game-thread notifications/HUD state alone do not establish audible timing. Use a documented late-request policy instead of pretending a missed boundary can be met. This prototype has a fixed tempo/meter,three calibration tables,one source,256ordered requests and a bounded one-hour request domain;the player stops after20.5seconds. No arbitrary streamed/compressed assets,tempo maps,indefinite clocks,live input-jitter contract,general music quality/listener comfort or production multi-voice scaling is certified. Missing/hot-swapped audio devices,forced termination and early recording interruption/recovery were not exercised. Musical scheduling wait is intentional and separate from CPU execution. No composition/generative music/rhythm-game/external plugin/renderer/shared-tool expansion;prior unrelated actual-FPS gaps remain unverified.

Latest26limited sheets/17without dedicated prototypes.

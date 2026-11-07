---
id: K-GAME-RHYTHM
title: Separate rhythmic challenge from chart readability and device delay
summary: Establish timing reliability and a readable chart language before judging execution difficulty. Test musical interpretation, visual reading, and calibration as separate causes of misses.
kind: reference
scope: Rhythm-game charting and timing feedback; Rock Band calibration and osu! mapping examples
keywords: [rhythm game, chart design, beatmap, timing, calibration, audio latency, readability, playtest, 리듬 게임, 채보, 박자, 판정, 보정, 오디오 지연, 기획]
status: active
checked_at: '2026-11-07'
context:
  evidence_check: Harmonix developer history and official guide plus osu official wiki page read
  application_status: Proposed genre transfer; no chart or hardware timing tested
---
# Separate rhythmic challenge from chart readability and device delay

## Guidance

**Source claims.** Harmonix developer James Fleming describes separately addressing audio/video alignment and the delay through the display/controller loop for scoring. Its calibration guide offers automatic and manual routes followed by a song test. The official osu! wiki presents proportional time/spacing as a readability technique, especially for easier charts, while acknowledging deliberate spacing variation at higher difficulty. The wiki is community-maintained official documentation, not a controlled study.

**Transferable synthesis.** Define listen/read cue → predict beat → execute input → receive judgment → recover as the repeated loop. Decide which musical layer the chart represents and make repeated motifs recognizable. Increase difficulty by choosing the intended burden: rhythmic inference, reading density, movement, coordination, or endurance. Raising all of them together makes a failed attempt harder to diagnose.

Treat chart timing, visual travel, input capture, sound output, and judgment feedback as a chain. Widening a hit window can hide device offset while weakening the intended scoring distinction. Conversely, perfect authored note times do not guarantee that the player sees and hears aligned cues. Provide a calibration path and a simple reference passage before interpreting difficult-chart failures.

Use consistent chart relationships as a teaching vocabulary, then vary them deliberately for musical emphasis or advanced reading. This is a proposed transfer across games, not a requirement that lane games or one-button games copy osu!'s spatial technique. Link difficulty selection and practice tools to the skill being trained rather than only a single aggregate label.

## Applicability and exceptions

Useful for authored music games and rhythm-driven actions. Free-tempo music, improvisation, expressive timing, and deliberately deceptive cues need explicit timing models and different consistency expectations. Calibration values depend on the hardware path; historical Rock Band timings and example display settings are not defaults for new systems. This entry does not establish accessible play without visual or audio channels.

## Checks

**Proposed checks, not executed:** Compare a sparse reference pattern and a demanding chart on the same setup. Record early/late distributions separately from wrong-input errors. Change audio route and display mode, then recalibrate and repeat. Ask players which musical element and cue they followed. Test repeated motifs for accidental notation changes, and check whether a miss allows recovery before the next phrase.

## Evidence

- [Fleming, Rock Band Calibration](https://www.harmonixmusic.com/blog/rock-band-10th-anniversary-blogs-james-fleming), “Part 1, the Fight” and “Part 2, the Makening”; official developer text opened 2026-11-07. Historical engineering account, no hardware reproduction.
- [Harmonix Calibration Guide](https://www.harmonixmusic.com/how-to-calibration/), “Auto Calibration” and “Manual Calibration”; official text opened 2026-11-07. Product-specific instructions; example numbers not reused.
- [osu!, Time-distance equality](https://osu.ppy.sh/wiki/en/Beatmapping/Mapping_techniques/Time-distance_equality), “Usage” and “Benefits”; official wiki text opened 2026-11-07. Technique guidance, not universal chart law.

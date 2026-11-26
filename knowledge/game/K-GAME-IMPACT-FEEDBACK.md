---
id: "K-GAME-IMPACT-FEEDBACK"
title: "Design impact feedback around the resolved outcome and next action"
summary: "Trace an attack from input through resolution and recovery. Make misses, blocks and hits distinguishable while preserving controls and the information needed for the next action."
kind: "method"
scope: "Action combat feedback using animation, visual effects, camera, sound and haptics"
keywords: ["game feel","impact feedback","hitstop","hit confirmation","combat readability","haptics","타격감","조작감","히트스톱","명중 연출"]
status: "active"
checked_at: "2026-11-26"
---

# Design impact feedback around the resolved outcome and next action

## Guidance

Trace input or buffering → wind-up → authoritative resolution → contact feedback → recovery. Use wind-up and reach to explain the threat. Distinguish miss, block, hit and other rule outcomes using resolved position, direction and reaction. Publish one appropriately keyed feedback event for each accepted result. Give the next threat, aim and movement room to remain readable through recovery.

Set hitstop scope, a limit or merge rule, and what happens to buffered input, physics, combo windows, cooldowns and audiovisual clocks. Specify hitstun separately as a rule that restricts action. Tune camera direction and decay with the actual combat framing. Compare the initial transient, material/body and tail of contact sound at matched volume. Check output latency and masking during repeated attacks.

## Applicability and exceptions

Let players reduce cosmetic shake, motion and vibration while preserving rule outcomes and essential cues. Redundant visuals and sound can carry information when the device lacks haptics or a player disables effects. Preserve meaningful recoil or aim behavior under its gameplay contract. Time-critical rhythm feedback needs explicit audio and input clocks.

## Checks

Play one attack as a miss, block and body hit, then repeat as a multi-hit sequence and after restart. Assert resolution, event direction/count and input recovery. Play on representative screens and input/audio devices with effects reduced. Ask whether players can recognize the outcome and next action, then change one feedback layer at a time. [Hitbox contracts](K-GAME-TECH-HITBOX.md) · [Timestep](K-GAME-TECH-TIMESTEP.md) · [Regression scope](K-GAME-REGRESSION-SCOPE.md#reproduction-visual-quality-and-performance)

## Evidence

The impact-feedback report compares production accounts and experiments. Its candidate cue timings and settings depend on camera, genre and device, and require target-game playtesting. [Game feel and impact feedback](../../docs/research/2026-11-23-game-feel-and-impact-feedback.md)

---
id: K-GAME-TECH-LEVEL
title: Validate perceived scale against traversal and camera constraints
summary: Set playable openings from character dimensions, movement and camera clearance
  separately. Unreal V12 measures traversal, shoulder-camera pull-in and waypoint
  occlusion across five door sizes.
kind: reference
scope: Game development; engine-independent mechanisms with version-dependent engine
  examples
keywords:
- level
- design
- scale
- landmark
- door
- routes
- 레벨
- blockout
- graybox
- level design metrics
- doorway clearance
- door width
- door height
- camera pull-in
- Spring Arm
- waypoint occlusion
- 문틀 폭
- 문틀 높이
- 3인칭 카메라
- 카메라 당김
- 표식 가림
status: active
checked_at: '2026-11-20'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V12 UE 5.8.3 rectangular doorway on flat ground, standing CharacterMovement
    and Spring Arm. Three input paths at five sizes, native camera/marker and three
    frame-cost runs per size. Perceived scale and route choice remain reference research.
---
# Validate perceived scale against traversal and camera constraints

## Guidance

Start with character dimensions, camera envelope, turning radius and encounter sightlines. Block out doors/corridors at usable scale, then tune occlusion, landmarks and route lengths to produce the intended exploration rhythm. Use branching and reconnection where production scope benefits, while preserving meaningful alternative choices.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

This is transferable synthesis, not proof that every game's doors are a fixed multiple of reality. Physical area, travel time, content density and perceived scale differ. See existing exploration and platformer references.

A **blockout** or **graybox** is playable geometry built from simple shapes to test layout before detailed art. Level design metrics express repeatable dimensions such as character clearance, step height and jump reach. Test turns, landings and passages with the actual controller and camera, then vary the metric where the encounter needs a different challenge. [The Level Design Book — Metrics](https://book.leveldesignbook.com/process/blockout/metrics)

## Checks

Proposed: test traversal with production camera and all supported bodies; ask unfamiliar players to find goals without route explanations.

## Evidence

- Related design references: [exploration](K-GAME-EXPLORATION.md), [platformer movement](K-GAME-PLATFORMER.md) and [prototype/playtest](K-GAME-PROTOTYPE-PLAYTEST.md). Scale and route recommendations are synthesis to test in the target game.

- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers) — 2015 creator-authored article; camera-window, framing and smoothing. Checked 2026-11-07, except items explicitly marked further reading.
- [Shaker et al. — Constructive Generation Methods for Dungeons and Levels](https://www.pcgbook.com/chapter03.pdf) — 2016 author chapter; representation, BSP, agents and platform levels. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V11, V12, V24 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

## Unreal doorway and shoulder-camera clearance — 2026-11-20

The local V12 experiment varied width at a fixed height and height at a fixed width. Use the same controller, capsule, camera, wall depth and input when determining the cause of a doorway failure. A 68×176 cm capsule tried five openings on a flat floor. It clears the 136×260 cm control without touch on all three paths. The Spring Arm still withdrew by up to 158.5 cm on the oblique approach and 112.3 cm on the turn. At 136×260 cm, body clearance preceded final camera restoration by 0.92 s in the oblique case.

Measure body clearance, camera recovery, marker occlusion and off-screen time as separate results. Check rendered visibility at unmasking as well as the geometric ray. Two low-door samples differed from the ray and the marker appeared one rendered frame later. Whole-frame p95 across the fifteen runs ranged from 10.424–11.256 ms. Test angled movement and turn inputs as well as straight entry. Preserve width and height controls and vary wall depth and shoulder offset when applying the result to another game. The fixture measures geometry and camera behavior. Perceived scale and wayfinding require a separate player check.

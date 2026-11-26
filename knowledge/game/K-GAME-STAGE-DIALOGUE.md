---
id: "K-GAME-STAGE-DIALOGUE"
title: "Keep stage dialogue state and 2D presentation reusable"
summary: "Use stable line and clip keys, give the stage explicit rules for starting and stopping a conversation, and verify its visual anchors, localized playback and gameplay effects together."
kind: "method"
scope: "2D stages using multiple speakers, portraits, sprite clips or branching dialogue"
keywords: ["LineId","stage dialogue","dialogue runner","sprite animation","atlas","localization","스테이지 대사","대화 분기","스프라이트","자막"]
status: "active"
checked_at: "2026-11-26"
---

# Keep stage dialogue state and 2D presentation reusable

## Guidance

Use stable line IDs with speaker, source text, translation context and portrait, expression or voice keys. Use tables for flat incidental lines, graphs or scripts for branching choice sequences, and condition plus priority for repeat visits. A stage owns eligibility, repeatability and interruption policy. A runner owns temporary conversation state. Quest, reward and progression owners validate and commit commands at the agreed checkpoint.

Choose blocking dialogue, in-world cues or optional interaction according to what the player must still perceive and control. Set the trigger, lower-priority interruptions, end condition and whether to resume, restart or abandon after death, cancel, exit or reload. A skipped presentation still follows the agreed gameplay commitment policy.

## Applicability and exceptions

Use frame-by-frame sprites when bespoke shapes and silhouettes matter, rigs when reusable motion and variants matter, and renders from 3D when consistent orientations justify the pipeline. Keep editable sources, export versions and stable clip names. Atlas coordinates are derived. Preserve pose durations, trim offsets and ground or speech anchors across reimport. If a clip event drives a rule, define its owner, timing, cancellation and repeat semantics.

## Checks

Reimport and compare loop duration, mirroring of asymmetric parts, pivots, texture bleed and actual scale. Enter the stage and exercise the first line, choice, cancellation, restart and reentry. Verify preview and interrupted branches cannot duplicate a reward. Check longer translations, missing voice or glyphs, subtitle duration, input focus and readable cues in the actual scene. [Stage identity](K-GAME-STAGE-COMPATIBILITY.md) · [Regression scope](K-GAME-REGRESSION-SCOPE.md)

## Evidence

The sprite and dialogue survey records production cases and engine/import options, including Aseprite frame metadata, Unity atlas and localization tooling, Unreal Flipbooks and dialogue scripts. Its stage and conditions are examples for a target project. [Sprite animation and stage dialogue](../../docs/research/2026-11-23-2d-sprites-animation-and-stage-dialogue.md)

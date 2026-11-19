---
id: K-GAME-TECH-BILLBOARD
title: Orient image impostors for their intended viewing conditions
summary: Choose how an image plane faces the viewer, then test the silhouette, texture orientation,
  transparency and shadow under the intended camera.
kind: reference
scope: Game development. For image impostors and vegetation, a masked material clips texels at a threshold.
keywords:
- billboard
- impostor
- 빌보드
- screen aligned
- camera facing
- world Z
- axis constrained
- camera roll
- UV mirroring
- vertical pole
- cutout shadow
- alpha sorting
- 화면 정렬
- 카메라 바라보기
- 축 고정
- 극점
- 반투명 정렬
- 마스크 그림자
- masked
- translucent
- overdraw
status: active
checked_at: '2026-11-11'
---
# Orient image impostors for their intended viewing conditions

## Guidance

A screen-aligned billboard copies the camera's right/up axes. A viewpoint-facing billboard points toward each eye or camera position, projecting an up vector into the plane. An axis-constrained billboard rotates around a fixed axis, often world up for vegetation. When the view lies on that axis there is no unique yaw. Reuse the last valid direction or define an initial fallback.

## Applicability and exceptions

For image impostors and vegetation, a masked material clips texels at a threshold. Translucent blending preserves fractional coverage and can expose ordering problems where planes overlap. Overdraw depends on projected pixel coverage. Shadow behavior depends on the material and render pass.

## Checks

Orbit above and below the plane, roll the camera and mark asymmetric UV corners to catch flips. Compare overlapping layers, solid and cutout shadow samples, stereo views, and GPU time at similar projected coverage.

## Evidence

Godot documents material orientation options, GPU Gems illustrates crossed vegetation cards, and Epic documents blend modes. Earlier Unreal observations covered selected orientations, cutouts and overlaps at achieved frame rates. Requested frame-rate coverage was incomplete. Stereo, general sorting and GPU overdraw remain unmeasured.

- [Godot — Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html)
- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass)
- [Epic blend modes](https://dev.epicgames.com/documentation/unreal-engine/material-blend-modes-in-unreal-engine?lang=en-US)
- [material properties](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-material-properties)

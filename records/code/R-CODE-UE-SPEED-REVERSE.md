---
id: R-CODE-UE-SPEED-REVERSE
title: Reverse speed offset crossed the owner in a fixed-forward camera rig
summary: Offset opposite velocity plus camera lag can put a fixed-forward camera ahead
  of its owner when reversing. Scale by speed magnitude but anchor offset direction
  to the intended rig;verify actual framing across reversal.
kind: error
scope: OneStep UE5.8.3 speed-effects prototype;straight lane and fixed+X camera rig
keywords:
- speed
- camera
- reverse
- framing
- lag
- offset
- fixed forward rig
- owner
- 역방향
- 카메라
- 오프셋
status: resolved
checked_at: '2026-11-14'
trigger: Reverse movement while a fixed-forward camera applies opposite-velocity offset
  and delayed following
symptom: Actual pilot at10.918s placed cameraX-191.57 ahead of capsuleX-204.37;two
  native policy checks failed
cause_status: confirmed
prevention: Use the intended rig direction for speed offset and verify actual camera
  remains behind owner across reversal and abrupt speed changes
prevention_status: verified
---
# Reverse speed offset crossed the owner

## Expected and observed

The fixed+X view should remain behind its capsule during reverse. Actual pilot at10.918s showed cameraX-191.57 ahead of bodyX-204.37. A dedicated revised policy expectation produced274checks/2failures. This is observed native framing,not a physics collision defect.

## Cause and resolution

Offset opposite velocity changes side when velocity reverses,while camera lag can retain a position further along the lane. That direction rule conflicted with the fixed-forward rig. Keep the offset backward along the rig and scale its magnitude from actual post-sweep speed. Do not change movement,collision,ray or trigger rules.

## Recheck and prevention

Final274native checks pass. All20normal final players compare1200original movement/collision/judgment rows and trigger entry order exactly within PIE/package separately. Every actual main-view camera remains behind its owner;cuts/disable/reactivation and independently projected views pass. These are bounded straight-lane checks,not general3D camera collision or camera-relative aim guarantees.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- Historical Unreal lab run and archived measurements, checked 2026-11-14.
- Local retained Results/Speed/reverse-framing-red.json,model-reverse-red/model.json and model-final/model.json;native source archive Results/Sources/speed.

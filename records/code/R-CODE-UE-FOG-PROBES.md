---
id: R-CODE-UE-FOG-PROBES
title: Near fog calibration targets hid the intended far samples
summary: Slanted depth-pair placement let nearer cubes cover far probe centers. Check
  actual first-hit geometry and OFF rendered target pixels before interpreting depth
  contrast; native settings alone did not prove the measured appearance.
kind: error
scope: UE5.8.3 single volumetric-fog fixture;opaque calibration cubes and fixed/moving
  camera
keywords:
- volumetric fog
- depth probe
- occluded calibration
- first hit
- pixel contrast
- 밀도
- 거리 표식
- 가림
- 안개
status: resolved
checked_at: '2026-11-17'
trigger: Depth targets placed on nearly overlapping projected rays
symptom: Several intended far probe centers sampled nearer cubes;independent ray/AABB
  visibility test failed
cause_status: confirmed
prevention: Use independently clear rays and actual native OFF target-color/projection
  checks;then compare fog density on the same pixels and retain failed fixture versions
prevention_status: verified
relations:
  prevention:
  - K-GAME-TECH-VOLUME
---
# Fog depth probes sampled nearer boxes

## Expected and observed

The oldx=±(180+120i),y=-300+500i layout converged in perspective:nearer35x6x35halfextent cubes hid intended far probe centers. Native property/state success alone could therefore support a misleading depth comparison. The independent first-hit test was observed RED. Constantx±400 passes and matches recorded native scene centers/extents. Every OFF movie frame checks actual visible target colors at independently projected first-hit positions,including camera movement/cut;occluded/offscreen targets are skipped explicitly.

## Cause and resolution

The same preliminary fixture also had a weak.6043/255base-density response at extinction1;the final scene uses extinction10. Both fixture changes precede final source freeze andallmatchedruns,so do not attribute combined pixel differences solely to extinction or call this an engine/renderer defect. The intentionally hidden-fog TDDstub was independently rejected at.1046/255despite native flags passing. Preliminary players/source snapshots remain local and are excluded from final costs.

## Recheck and prevention

Final54policy/8evidence/full778Python,6actualworlds,9matchedcosts and bound72snormal1x+24sno-history media pass. Reference/API checks,actual image evidence and performance scopes remain distinct. No shared verification framework changes.

## Evidence

The original measurements and recordings are held with the historical experiment records.

The the historical Unreal run and its archived measurements,checked2026-11-17.

---
id: K-GAME-TECH-DESTRUCTION
title: Choose authored fracture or runtime topology from gameplay needs
summary: Choose pre-authored pieces and explicit damage/lifetime/reset rules for bounded
  prop destruction. UE5.8.3 mesh replacement+Chaos rigidbody12/96-piece evidence exists;CCD
  alone did not satisfy contact bounds. Not GeometryCollection clustering or runtime
  cutting.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["fracture", "chaos", "destruction", "decal", "파괴", "Geometry Collection", "Chaos Destruction", "clustering", "prefractured", "debris", "damage threshold", "duplicate break", "TTL", "reset", "substep", "collision bounds", "사전 분할", "임계값", "중복 파괴", "잔해 제거", "리셋", "서브스텝"]
status: active
checked_at: '2026-11-17'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V14 UE5.8.3:27policy/6PIE+packageworlds/9costs/60snormal1x;precreated12/96pieces,CCD32/8/4,maxstep1/240;notGeometryCollectionclustering/runtimefracture
---
# Choose authored fracture or runtime topology from gameplay needs

## Guidance

For cosmetic damage, authored mesh swaps and debris may be sufficient. For gameplay-relevant fracture, author Geometry Collections, clustering, collision and damage thresholds. Decide separately whether to simulate precomputed pieces or generate new cuts at runtime; use decals for surface marks.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### Geometry Collection

In Chaos Destruction, a Geometry Collection represents fracture pieces and their hierarchy. Clustering groups pieces so a group can move together before it breaks. When damage affects traversal, check both the break transition and the resulting collision on the target platform.

## Applicability and exceptions

Pre-fractured does not mean pre-animated. Physics, navigation, replicated state and persistent damage must agree with visual destruction.

## Checks

Bounded native repeated impacts,obstructed pieces,TTL/pool cleanup and active/inactive resets are checked below. Save/load,multiplayer authority and production persistent debris remain unverified.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Epic, Destruction Overview](https://dev.epicgames.com/documentation/unreal-engine/destruction-overview) — terminology and applicability of Geometry Collection, Chaos Destruction, clustering. This is source evidence. The suggested target checks remain to be run.

- [Epic — Geometry Collections User Guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/geometry-collections-user-guide) — Official documentation; Geometry Collection authoring. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V14 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

## Native Unreal validation — 2026-11-17

The historical Unreal run,[contact incident](../../records/code/R-CODE-UE-DESTRUCTION-CONTACT.md),archived measurements.

UE5.8.3 Win64 Development/DX11. A480x24x240cm intact wall switches to12(4x3)or96(12x8)pre-authored regular cube pieces with0.4cm seams. Native Chaos rigidbodies simulate the pieces;this is mesh replacement,NOT GeometryCollection clustering/runtime cutting. Components/materials are prepared before the trace;activation creates/enables physics and applies impulses inside the break timer. Piece UObjects remain in a reuse pool after cleanup. Total fragment mass12kg;the same physical-space velocity field(550+.1x,-120+.05z,110+.05z)cm/s has the same mean kick across tiers. CCD and per-body32position/8velocity/4projection iterations. Final maximum physics step1/240s,max16substeps;this is a configured maximum,not a fixed240Hz or renderingFPS claim. Typed previous physics settings are restored without SaveConfig,and actual PIE restoration is checked. Physics settings are process-wide: this dedicated one-fixture/one-owner test does not certify simultaneous differently configured worlds. Existing62assets/dependencies/Config/project/renderer/shared tools are unchanged.

Damage100inclusive,positive request IDs,finite nonnegative damage;dedup within generation. Broken state never reactivates from subsequent hits. Reset clears damage/IDs/broken/removed and advances generation while retaining audit totals. Same18authored requests in every arm cover99,duplicate99,+1,postbreak repeats,101fresh overshoot,50+49+1,invalidID/negative damage,ID reuse and exact100. Five logical breaks/four TTL expiries/one active reset per player. Three-second TTL disables simulation/collision,clears velocities,hides and reattaches/restores pieces to pool poses. Four resets include active and post-expiry cases. OFF is an intact static visual/physical baseline with identical audited logical requests;its wall remains collidable,so this is not passability equivalence across arms.

27native policy checks pass;initial24/16RED and kick27/3RED are retained. Six actual PIE/package worlds plus9cost/3media players all independently check original request outcomes,native postphysics positions/quaternions/velocities/mass/iteration settings,world-query cleanup and reset poses. Native positive-impulse floor/wall/piece callbacks corroborate contact;callback counts include repeated/substep notifications,not unique impacts. The detailed contact journal caps4096records per player;all callback counters continue. Detailed pose audit20Hz in realtime andeverymovieframe;per-frame native bounds/status checks remain active. Visual and physics bounds are compared;the strict guard is floor minimum>=-3cm and wall maximum<=383cm(inner face380). Cleanup queries return0,and inactive pooled poses/velocities/orientation are independently checked.

Initial30sim pilot failed:floor minimum-4.672cm/wall383.886. Increasing iterations and normalizing kick/mass still failed at-4.273cm. Same diagnostic binary/source/mass/kick/iterations with only substepping OFF/ON compared33ms inputs:OFFfailed-4.273,ONmax1/120passed-1.297;physics bounds matched visual bounds,so this was not a rendering-only proxy. But the frozen1/120v1 repeated matrix later failed perf-high-2 at7.393s,-3.879cm. Allv1source/identity/partialruns including failure are retained under Results/Destruction/v1;none are final costs. Finalmax1/240s was independently piloted and all18finalplayers rerun from scratch with a new identity. Do not cherry-pick repeated identical runs or callCCD/iteration flags proof of contact safety. The controlled study is historical diagnostic evidence,not finalperformance evidence or a universal Chaos guarantee.

Nine sequential packaged players rotate off/low/high,low/high/off,high/off/low. Same20s authored requests,wall/floor/stopwall/camera,12kg total enabled-fragment mass,kick field,physics settings,1280x720,DX11,Development,cap0/noVSync. Steady costs cover[2,18)s. All five breaks,including the first1.2s event outside that window,have activation CPU,paired activation-frame wall and the maximum across activation+next3native frames to include deferred simulation. First-movement delay runs from activation API completion to GT postphysics observation of>0.5cm displacement,with actual piece position/time and neighboring view/frame bindings. It is not input-to-photon latency. Whole wall/cadence/GPU include engine,callbacks,physics,HUD,20Hzpose audit and JSON instrumentation;actor CPU excludes physics that ran before TG_PostPhysics. Contact logging follows the same4096cap policy;its saturation time differs by tier. Whole GPU is delayed,not isolated physics/render GPU cost. Precreation/pool memory,startup/finalserialization/exit and PNG/video work are excluded. No readback/capture in performance runs. Three short uncontrolled runs do not establish a hardware-general winner.

Use this for bounded reusable destructible props when topology is authored in advance. Keep damage/idempotency,generation,body activation,lifetime/reset and visible response separate. Validate actual contacts/poses and removal queries;CCD alone is insufficient. Preserve typed runtime settings and test both active and inactive reset. Budget precreation/pool memory separately;cleanup returns components to the pool rather than freeing their UObjects. Ordinary rigidbodies and synthetic cube seams do not certify artist-quality cracks,structural connectivity,GeometryCollection clusters,load-bearing collapse,navigation,skinning or conservation of fracture energy. Fixed20s/12or96pieces/one wall/known planes/one machine;physics trajectories need not be bit-identical across runs or frame schedules. Long indefinite/hitch/device/production scaling remains unverified. No runtime cutting/building collapse/network/save/renderer/framework expansion. Subjective visual quality and user acceptance remain pending.

[Epic physics sub-stepping](https://dev.epicgames.com/documentation/en-us/unreal-engine/physics-sub-stepping-in-unreal-engine),checked2026-11-17:collision callbacks can repeat across substeps;do not interpret totals as unique impacts. Installed5.8.3PhysLevel/ChaosScene runtime step path governs local tests. Original GeometryCollection source check remains2026-11-07 and does not prove this different native rigidbody implementation. Latest29limited sheets/14without dedicated prototypes.

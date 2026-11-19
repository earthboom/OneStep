---
id: K-GAME-TECH-SPEED
title: Use speed effects without hiding actionable information
summary: Scale FOV,backward rig offset/lag and native blur from actual post-collision
  speed;keep cosmetic state separate from movement/world judgments and reset history
  on cuts. UE5.8.3 bounded off/reduced/full native evidence exists;not actual30/60/144FPS
  or subjective comfort certification.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["FOV", "motion", "blur", "speed", "camera", "속도감", "field of view", "camera motion blur", "velocity buffer", "view-projection matrix", "actual velocity", "camera lag", "camera cut", "disable", "reactivate", "reverse framing", "fixed forward rig", "속도 기반 FOV", "카메라 지연", "역방향", "모션 블러"]
status: active
checked_at: "2026-11-19"
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: V06 UE5.8.3:274policy/22native sessions/20players1200steps/9matchedcosts/60snormal1x;fixedforward
    rig,notvehicle/cameraaim/comfort/FPS certification
---
# Use speed effects without hiding actionable information

## Guidance

Coordinate FOV changes, camera offset/lag and velocity-based blur with acceleration events. Separate base framing from effects so changing visual intensity does not alter aiming or movement rules. Depth-based camera-motion blur reconstructs pixel motion from view transforms; moving objects need additional motion information.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

## Applicability and exceptions

Motion blur does not restore lost input responsiveness or actual frames. Large FOV shifts and forced camera motion may impair comfort and target reading.

The camera's **field of view (FOV)** is its angular coverage. Changing it alters perceived motion and framing. For camera motion blur, reconstruct a world position from screen depth and the inverse current view-projection matrix, then project it with the previous matrix to estimate screen displacement. Independently moving objects need their own motion vectors or a velocity buffer. Compare a moving camera with a stationary scene against a stationary camera and moving character. [Gilberto Rosado — Motion Blur as a Post-Processing Effect](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-27-motion-blur-post-processing-effect)

## Checks

Native bounded traversal subset below compares off/reduced/full with actual movement/world judgments. Subjective comfort/accessibility and general vehicle/camera-aim tasks still require game-specific review.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Gilberto Rosado — Motion Blur as a Post-Processing Effect](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-27-motion-blur-post-processing-effect) — GPU Gems 3 ch.27; depth reconstruction and velocity sampling. Checked 2026-11-07, except items explicitly marked further reading.
- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers) — 2015 creator-authored article; camera-window, framing and smoothing. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V06 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

## Native Unreal validation — 2026-11-14

The the historical Unreal run and its archived measurements,[reverse framing incident](../../records/code/R-CODE-UE-SPEED-REVERSE.md).

A fixed-forward(+X) camera rig follows a native swept kinematic capsule. Actual post-sweep speed magnitude/2200cm/s is clamped to[0,1]; desired speed is not a substitute when blocked. Off/reduced/full use FOV90+0/7.5/15degrees,backward rig offset0/55/130cm and built-in motion-blur amount0/.2/.5. Base offset is(-360,0,140)cm. Reduced position/FOV exponential rates14/s;full position8/s,FOV10/s. Disable immediately restores base/FOV90/blur0 and signals a native history cut;reactivation follows from that base. Camera cuts14/16s reset both owned cosmetic state and native PlayerCameraManager history. No renderer algorithm,assets,configuration,project dependencies,vehicle physics or shared verification tools were added.

274native policy checks cover zero/max/overspeed/reverse,stop/acceleration,disable/reactivation/cuts,finite bounded inputs,atomic invalid rejection and30/60/144/irregular time partitions. These are synthetic time inputs,not measured FPS. The actual20second scene has1200fixed60Hz swept capsule steps per player,wall collision,world-forward Visibility rays and native capsule overlap/enter judgments. All20normal final players preserve every original movement/hit/ray/overlap row and entry order exactly within each consumer (PIE and package independently). An independent reference derives the sweep pullback,geometry,queries,camera filtering and projection. Actual FSceneView origin,FOV,final postprocess,cuts and signed clip depth are checked;WorldToPixel success alone does not mean in front of the camera. Every normal view keeps the camera behind the capsule,including reverse.

Nine sequential packaged cost players rotate off/reduced/full,reduced/full/off,full/off/reduced. Same20s inputs,scene,1280x720,DX11,Development,cap0,noVSync;only[2,18)s is sampled. No PNG/readback/video encoding occurs in these runs. Camera CPU measures render-time substep evaluation plus native setters/publication;fixed-camera updates are instead included in simulation CPU alongside movement sweeps,queries and JSON row creation. Whole frame wall is OnBeginFrame to OnEndFrame;cadence is consecutive frame starts. Both include engine/HUD/main-view observation/experiment bookkeeping. GPU is delayed whole-frame RHI timing,not isolated blur GPU cost. Startup/result saving/exit are excluded. Different FOV naturally changes visible geometry. Three short uncontrolled host runs do not establish hardware-general budgets or a statistically significant performance winner.

Initial native stub274checks/270failures;final274pass. Reverse-framing actual pilot exposed cameraX-191.57 ahead of bodyX-204.37 at10.918s:offset opposite velocity plus lag crossed the owner in a fixed-forward view. Two focused policy failures reproduced it;offset now remains backward along the view rig while magnitude scales strength. Native disable initially snapped to base without a view-history cut;the actual-consumer checker rejected it and the cut was added. Native wall stopping5948.963336cm versus geometric5950cm is intentional PrimitiveComponent PullBackHit,not an engine bug:Clamp(.1,.1/Dist,1/Dist)+.001 of the step. Independent path error is about2.82e-6cm. WorldToPixel usesabsW and can project behind-camera points;projected/front/signedclipW are now separate. Narrow/fast blur pilots failed a guessed LDR peak-drop threshold. Blur need not reduce a finite bar's tonemapped peak by10%;the invalid peak condition was removed with a recorded ruling,not silently relaxed. Strict spatial spread plus matched camera/native flags/cut reset remain,with an off-as-on negative control. Final wide5cm calibration card is diagnostic-only. First screenshot green mask incorrectly excluded actual tonemapped RGB(240,162) in G/B;corrected segmentation from1.5to1.25 retains the4px projection tolerance. First blur mutation selected a stationary already-zero frame and therefore failed to mutate;the retained RED now selects a confirmed moving positive-blur frame. Every negative fixture is accepted unchanged before mutation.

Apply this separation to traversal cameras where cosmetic strength must not feed movement or world queries. Use actual velocity,offer off/reduced settings,keep reverse offset relative to the intended rig,and clear temporal history on discontinuities. This is one straight lane/fixed-forward swept kinematic capsule,not general3D camera collision,vehicle physics,camera-relative aiming/crosshair accuracy,networking or a full controller. World-forward aim preservation is the tested contract. Native blur has actual pixel evidence on a controlled panning card;general disocclusion/animated mesh velocity/artifact quality and subjective comfort/readability need game-specific review. Only8bounded behavior worlds were observed;no stable30/60/144actualFPS certification. No renderer/Present/shared-tool optimization was attempted.

Latest27limited sheets/16without dedicated prototypes.

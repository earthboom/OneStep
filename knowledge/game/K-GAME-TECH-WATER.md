---
id: K-GAME-TECH-WATER
title: Use summed waves for water surfaces with explicit limits
summary: Use summed sine or full parametric Gerstner displacement with analytic normals
  and a conservative steepness budget. UE5.8.3 CPU procedural geometry has native/time/boundary
  and matched-cost evidence;not fluid simulation or GPU WPO performance.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["Gerstner", "sine", "waves", "water", "물", "파도", "Gerstner waves", "horizontal displacement", "buoyancy", "procedural mesh", "parametric", "Lagrangian", "analytic normal", "steepness budget", "UE_DOUBLE_PI", "time partition", "물 표면", "가파름", "시간 입력"]
status: active
checked_at: '2026-11-14'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: UE5.8.3 CPU:222policy/20PIE+20packagecases/9matchedcosts/native20s1xmedia;65x65vertices/4waves;public
    CPU section,not GPU WPO/readback
---
# Use summed waves for water surfaces with explicit limits

## Guidance

Represent height as a sum of waves with amplitude, wavelength, direction and phase. Gerstner waves also move surface points horizontally, producing sharper crests. Compute normals from the same displacement field and share a compatible surface query with buoyancy gameplay.

Implementation selection and checks below are engineering synthesis, not a promise of a source game's exact implementation.

### Gerstner waves

Gerstner waves include horizontal displacement, so a displaced vertex's original horizontal coordinates may differ from its rendered location. For buoyancy, compare the gameplay query and visible water height at the same world-space position and simulation time, especially near steep crests.

## Applicability and exceptions

Steepness must be bounded to avoid folding. Wave sums are not full fluid simulation and do not automatically handle breaking waves, shore interaction or flow around obstacles.

## Checks

Native subset below checks parametric geometry/normals,scripted time partitions and matched CPU costs. Coastlines,floating objects/physics and full water rendering remain unverified.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Mark Finch — Effective Water Simulation from Physical Models](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-1-effective-water-simulation-physical-models) — GPU Gems ch.1; sum of sines and Gerstner waves. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V32 in [the coverage guide](K-GAME-TECH-GUIDE.md). The originating short is a discovery lead, not independent proof.

## Native Unreal validation — 2026-11-14

The historical Unreal run and archived measurements.

For rest coordinate u=(x,y),theta_i=k_i(D_i dot u-c_i*t)+phase_i,k_i=2pi/L_i. Sine P=(x,y,sum A_i*sin theta_i). Gerstner adds horizontal sum q*A_i*D_i*cos theta_i. Differentiate the full parametric position:Tx/Ty include the horizontal derivatives,then N=normalize(Tx cross Ty). A sine-only height-gradient normal is wrong for horizontally displaced Gerstner geometry. Rest coordinates are material/Lagrangian labels,not the displaced world XY;this implementation is not a direct world-height query. Analytic smooth normals intentionally differ from normals of finite planar triangles.

Four fixed waves:directions(1,0),(.6,.8),(-.8,.6),(0,-1);amplitudes24/12/8/4cm;wavelengths640/420/280/200cm;speeds90/65/45/30cm/s;phases0/.7/1.4/2.1radians. Directions normalize during preparation. Default shared q=.9 gives sum(q*k*A)=0.648290 approximately. Gerstner preparation accepts S=sum(q*k*A)<=.99,a conservative margin below the theoretical singular/folding threshold1,and rejects larger values atomically rather than clamping. Actual near-cap fixture S=.989999999;single-wave exact.99 worst crest retains Jacobian.01. q0 equals sine;all zero amplitudes give no horizontal drift and normalUp. Supported finite domain:coordinates/time absolute<=1e6,1..4waves,amplitude0..1000cm,wavelength1..1e6cm,speedabs<=10000cm/s,phaseabs<=1e6,q0..10. No silent large-world/indefinite-clock guarantee;different domain or rebasing needs validation.

One native UProceduralMeshComponent,65x65vertices/64x64cells/8192triangles,25cmspacing,rest domain[-800,800]cm each axis. CPU arrays are reused;create one section then UpdateMeshSection each tick,collision/shadows off,identity component transform,same opaque diffuse blue material with specular0/metallic0/roughness1 and no material WPO/normal override. Built-in ProceduralMeshComponent plugin/module enablement and one owned material are the only dependency/content additions. Installed API marks this component experimental;version changes need revalidation. No engine,renderer,shared verification-framework or external-plugin change. CPU component section values are actual publication-state observations,not GPU vertex-buffer readback. Native screenshots/video establish visible rendered geometry;do not promote CPU equality into a bit-level GPU claim.

Policy222checks:finite repeat,negative coordinates/time,central-difference full normals (h=.001cm,error<1e-6),unit/orthogonal tangents,one-wave exact values,double wavenumber,zero amplitude/q0,nonunit-direction normalization,exact.99/above-limit rejection,worst-crest Jacobian,invalid atomic settings/time/coordinate rejection. Same endpoints reached by30/60/144Hz and irregular time partitions agree;these are scripted time inputs,not proof of actual rendering at requested FPS. Actual PIE and packaged players each exercise20fixtures:flat,sine/Gerstner times0/1.25,replay,negative time,zero amplitude,q0,near-cap,partitioned t8,NaN/high-q/zero-direction/zero-wavelength rejection preserving prior geometry,and +/-1e6seconds. Every fixture reads all4225native positions/normals/tangents,indices,section bounds,material/collision flags and same component identity. Independent Python math checks169000native vertex observations across both players (position<1e-4cm,normal/tangent<1e-6);actual maximum errors appear below. First public CPU publication drift is also checked separately. Winding uses Unreal's upward face convention cross(C-A,B-A).

Nine sequential packaged players in rotated flat/sine/Gerstner,sine/Gerstner/flat,Gerstner/flat/sine order. Same65x65grid/four configured waves/material/camera/light/1280x720/DX11/Development/cap0/noVsync/no audio/capture.128warmup+512measured ticks,one4225vertex publication each measured frame (2163200vertex updates/run). Identical evaluation schedule t=serial/60 across arms/repeats,not elapsed-realtime animation speed. Flat is deliberately a flat-update baseline through the same publication path,not a dormant static-mesh baseline. Five actual CPU-section probes per measured frame plus full pre/post section audits are independently checked;full pre/post audits and save/exit are outside the measured window. No GPU capture/readback during cost. Evaluation timer covers preparation and CPU samples;publication timer covers UpdateMeshSection/enqueue,not GPU completion. Whole OnBeginFrame→OnEndFrame wall/cadence include engine/HUD/constant-size observation/JSON-row creation;GPU samples are delayed whole-frame timings,not isolated water GPU cost. Host load uncontrolled;three short repeats do not establish universal speed or budgets. CPU results do not predict GPU WPO/compute performance.

Actual independent maximum position/normal errors:7.10383289844e-12cm/9.29859380646e-14;222policy,20actualPIE+20packagecases,9costplayers,600frames/20.000snormal1x. Initial float PI and finite-difference normalization-observer failures are documented in the results and R-CODE-UE-EVIDENCE-PROXY;independent double expectations and scaled derivatives preserve the original tolerance. Choose the technique by required shape/coordinate semantics before this CPU-path cost. No buoyancy,fluid/coast/foam/reflection/refraction/streaming/renderer/framework expansion;prior actualFPSgaps remain unverified. Latest24limited sheets/19without dedicated prototypes.

### Retrieval application check

A new standalone Korean homonym keyword incorrectly routed a menu-label-only edit to wave physics (193/194checks,one forbidden hit). Replaced it with a specific water-surface phrase without changing the search engine or weakening the negative case. All194checks then pass. Adopt WATER for geometric wave/normal/time decisions;an interface-label edit alone is not evidence that a wave implementation is needed.

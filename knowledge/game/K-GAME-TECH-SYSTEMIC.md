---
id: K-GAME-TECH-SYSTEMIC
title: Model elemental interactions as explicit state rules
summary: Stage explicit elemental state transitions with water/fire precedence, stable
  event IDs and finite electric propagation. Scoped UE5.8.3 native contacts/state/event/timer
  evidence supports bounded wood/metal rules;Nintendo source details remain unknown.
kind: reference
scope: "Game development; engine-independent mechanisms with version-dependent engine examples"
keywords: ["systemic", "chemistry", "engine", "elements", "material", "emergent", "화학엔진", "chemistry engine", "material state transition", "interaction matrix", "water fire precedence", "wet wood", "metal conductivity", "electric cycle", "stable event id", "event deduplication", "charred fuel", "atomic state transition", "원소 상호작용", "젖은 나무", "전기 순환", "동시 소화"]
status: active
checked_at: '2026-11-12'
context:
  evidence_check: External source text checked; source-specific limits appear in Evidence
  application_status: Scoped UE5.8.3 V51:31policy/960native steps/5760body observations/37evidence
    tests/3costplayers/1xmedia;bounded100ms rules,notNintendo source/fluid/network/largeworld
---
# Model elemental interactions as explicit state rules

## Guidance

Implementation pattern: represent material properties and elemental effects as data, specify transition conditions and precedence, and send resulting events to physics, audio and rendering. Prototype a small interaction matrix before expanding combinations. The original conceptual model is confirmed by the follow-up below; the proposed data architecture is not Nintendo source code.

Implementation selection and checks are engineering synthesis, not a promise of a source game's exact implementation.

### Implementation follow-up — 2026-11-07

The original Nintendo/GDC slides distinguish movement simulation from state transitions. At 40:23 the model separates elemental effects from material objects; at 40:53 effects may alter material state, at 41:08 effects may alter other effects, and at 41:23 material-to-material contact alone does not cause a chemical state transition. This restriction belongs to that game's model, not physical chemistry. Implementation synthesis: collect contacts/exposures, evaluate a directed effect-to-state rule table, resolve simultaneous changes with explicit precedence, commit state, then emit physics/VFX/audio events. For burning wood, a material can emit an elemental fire effect; this preserves the separation instead of declaring that every material directly transforms another.

## Applicability and exceptions

The three conceptual rules have historical original-slide evidence;the native follow-up validates its own bounded authored data/scheduling/propagation rules. Exact Nintendo source code, update order and simulation coefficients are not public evidence here.

In Nintendo's **chemistry engine** presentation, an element can change a material state or affect another element. Material contact alone has no chemical transition in that model. An **interaction matrix** is a transferable representation: list influencing effect, receiving state, preconditions and resulting state for each directed interaction. Check simultaneous exposures in more than one processing order before choosing a precedence policy. [Nintendo/GDC — original technical presentation](https://www.youtube.com/watch?v=QyMsF31NdNc&t=2423s)

## Checks

Native bounded fire/water/electric precedence,event order/dedup,cycles,timer/clock boundaries,actual contacts andcosts are checked below. Save/load,replicatedauthority andunboundedworldremainunverified.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- [Nintendo — Breath of the Wild: Breaking Conventions](https://www.youtube.com/watch?v=niIVdlavc7I) — Earlier pass: excerpt description only. The original full talk slides were subsequently checked at the timestamps below. Checked 2026-11-07, except items explicitly marked further reading.
- Originating channel shorts: V51 in [the coverage guide](K-GAME-TECH-GUIDE.md). Originating shorts are discovery leads, not independent proof.

### Follow-up evidence

- [Nintendo/GDC — original technical presentation](https://www.youtube.com/watch?v=QyMsF31NdNc&t=2423s) — Original slides visually inspected at 40:23, 40:53, 41:08 and 41:23; transcript export unavailable; not a full-video viewing or source-code inspection. Checked 2026-11-07.

## Native elemental-rule evidence — 2026-11-12

The historical Unreal run adds scoped UE5.8.3 Win64 Development/DX11:31policy/clock checks,12cases×20steps×4actual PIE/package consumers=960state snapshots/5760body observations,37independent evidence tests,3matched packaged costs andnormal1xmedia. Latest17limited local technique sheets/26withoutdirect prototypes;not complete subject certification.

Adopt a staged material/effect matrix for small deterministic environmental puzzles oraction interactions. Actual QueryOnlyboxes supply contacts;normalize undirected edges,validate whole batch,compute nextstates,commit once,then publish transitions. Gameplay Wood/Metal tags are separate from Unreal render/physical materials. Contact alone never changes state. Do not wire mutually recursive hit callbacks as unbounded propagation.

Authored100ms contract:wood10fuel,water15wet ticks,electric3charge ticks. Decay timers andconsume previously burningfuel first;fuel0 becomespermanentchar. Applywater beforefire;it extinguishes andblocks outgoingemission immediately. Existingburning sources withremainingfuel expose currentneighbors,newignition emits nextstep. Onlydry/noncharredwood withfuel ignites. Electricity usespost-water/timer conductivity:metal orwetnoncharredwood. Unionexternalconductiveseeds,sorted iterativeBFS,onevisit/body evenincycles. Existingcharge isstatus,notautomaticnewsource. Refresh doesnotrepeatChargeOn;wet1→0 permits same-stepfire. State-changeevents canonicalbybodyID/eventkind,onlyonbooleanchanges;burnout emitsExtinguished+Charred once.

StablepositiveIDs deduplicate withinbatch andworldhistory;sameID/differentpayload rejects entirestepatomically,includingoutput;replay doesnotrefresh. Bounds1..1024bodies,256offeredinputs/step,65536rawcontacts,16384seenIDs untilreset,step0..999999. Noeviction/lifecycle/indefiniteworld claim. Clockaccumulator acceptsfinite0..0.5s,retains100msremainder,max5steps/call;invaliddelta rejects,no silenttime dropping. Scripted30/60/144Hz andirregular2s eachproduce20steps;actualnativeFPS ismeasuredseparately. Requestedcap missesremainunverified,asreported.

Native6bodycases exercisewood/metal,fire-waterpermutations,duplicate/replayedIDs,dry/wetconductivity,cycle/refresh,one-edge-per-tickfirechain,charredreignite,timerboundaries,atomicinvalidbatch,waterstoppingemission andduplicate/selfcontactnormalization. Allcolliders shareoneactor,soignoreonlyselfCOMPONENT.40cmhalfextent queryboxes at70cmcontactspacing surround60cmrendercubes;no movement/fullphysics. ActualUWorldoverlaps retained evenifAPIboolisfalse(touchresults). IndependentPython derivesexpectedgraph fromactualnativepositions/extents,thenindependentlyreplays everystate/timer/input/event/visit/counter/Seen/stateandeventFNV64digest. Actualmesh/collision/materialparent/Tint checked;colourpriority charge>fire>wet>char>base ispresentation. Injectedself/duplicate records areexplicitlyauthored normalizationinputs. Fourmalformednativebatches leaveworld/outputunchanged. Permutation/duplicatecontactcasesequalsexactly. FNVdigest isdeterministiccomparison,notauthentication.

37evidence tests reject missing/reorderedrows,tamperedinput/state/timer/event/contact/graph/pose/extent/collision/material/Tint/hash/visit/delivery/clock/launch/world/capture/costsetup/GPU/activeframes. Onefreshreview foundeventhash/auditwithintimedPublish andanunusedcostgraphcopy;bothmovedoutside(namedhash/dup-audit afterQ3,presentationgraph onlybehavior). Activetail truncationdetector failedfirst,thenbinds exactsamples toactualframeSerial/allWallMs. FinalEditor/package/model/behavior/3costs/media reran oncorrected frozenSource/binaries. Initial30policystubfailed21then30passed;irregularclockadds31. InheritedBlend34/coreactualPIE73/package73 pass.22oldarchives/53existingassets unchanged,no newassets.

|Player|Queryp95ms|Rulesp95ms|Publishp95ms|Wholewallp95ms|Activewallp95ms|Activemaxms|
|---|---:|---:|---:|---:|---:|---:|
|perf-1|1.493|0.537|0.178|2.068|4.635|4.786|
|perf-2|1.542|0.558|0.207|2.153|4.666|4.896|
|perf-3|1.507|0.581|0.188|2.129|4.705|4.761|

Cost:3sequentialpackaged1280×720players,512cubes/QueryOnlyboxes32×16grid70cm,512actualqueries/tick,10Hz,128offeredinputs=64unique+64duplicates.2s/20tickswarmup+8s/80measuredticks. All100orderedstate/eventdigestsandcounters matchacrossrepeats;finalSeen6400. Beforewarmup512actualcomponentpose/collider/material/Tintaudited. No capture/perbodyrawsnapshot/debug incost. Query includesnativeoverlapwork;Rules includesvalidation/normalization/graph/state/BFS;Publish includesallTintsets/readbacks anddeliveryhandler. Inputgeneration/canonicalhash/dup-audit/costrowcreation remaininwholeframe outside subsets. Setup/finalserialization/write/exit excluded. Fullwall/cadence ANDactive-step tails neededbecause10Hz spikes canhideinallframep95. Delayed RHI wholeGPU isnotisolatedruleGPUcost orsameCPUframepairing;zerounavailable,nonfinite/negativefail;valuesmayrepeat. Hostload/scheduling uncontrolled;nooptimization/baseline/speedup claim. Boundhistoryvalidation/hash growswithSeen;donotgeneralize6400IDs toindefiniteplay.

Useforboundedrule-drivensystems aftermatchingtheactualgame'sprecedence,budgets,IDs andlifecycle. Movingcontacts,continuousheat/exposure/diffusion,fluids,physics/VFX/audio,saveload,replicatedauthority/rollback andlargeworldremainunverified. Sourcegameimplementation/updateorder/coefficients remainunknown;thisprototype'snumbersandBFS areauthored. 100ms quantization may addone tickofreactionlatency;fastercombatneedsadifferentstepandrevalidation/costmeasurement. No renderer/profiler/frameworkimprovement orpublication.

Sources:[GDCVault originaltalk](https://gdcvault.com/play/1024562/Change-and-Constant-Breaking-Conventions),metadata checked2026-11-12,confirms talkidentity only;the2026-11-07visualslidetimestamps above remainhistorical,notnewfullwatch. [EpicUWorld API](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/UWorld),installed5.8World.h andactualruns supportOverlapMultiByObjectType;[Epiccollisionoverview](https://dev.epicgames.com/documentation/en-us/unreal-engine/collision-in-unreal-engine---overview) supportsqueryconcepts. No Nintendo source/coefficientclaim.

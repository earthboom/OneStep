---
id: R-CODE-UE-DESTRUCTION-CONTACT
title: Coarse physics steps let dense debris exceed the contact guard
summary: CCD and additional constraint iterations did not keep96debris boxes within
  the declared3cm floor/wall guard. Check actual physics/render bounds under fixed
  movie inputs and repeated realtime runs;retain failed revisions and rerun matched
  arms after changing maximum step.
kind: error
scope: OneStep UE5.8.3 single pre-fractured wall;12/96CCD boxes and known floor/stopwall
keywords:
- destruction
- debris
- contact
- penetration
- CCD
- substep
- maximum delta
- solver iterations
- 바닥 침투
- 파괴
- 잔해
- 서브스텝
status: resolved
checked_at: '2026-11-17'
trigger: Dense precreated debris with coarse/variable physics steps despite CCD and
  iteration settings
symptom: 30sim floor minimum-4.672/-4.273cm;1/120revision later repeated-run singleframe-3.879
  exceeded unchanged3cmguard
cause_status: confirmed
prevention: Measure actual body/visual bounds and collision/query cleanup;declare
  maximum physics step,retain failed runs,and repeat every matched arm on the final
  configuration
prevention_status: verified
relations:
  prevention:
  - K-GAME-TECH-DESTRUCTION
---
# Dense debris exceeded the declared contact guard

## Expected and observed

Native contact guard:floor minimum>=-3cm,stopwall innerface380cm with maximumX<=383. Initial30sim minimum-4.672;iterations32/8/4 and normalized kick/mass still-4.273. A1/120maximumstep pilot passed but later frozenv1perf-high-2 had one-3.879frame. All failures remain local;no failed run is final performance evidence.

## Cause and resolution

Visual bounds and GetBodyBounds matched at the failure,so this was actual contact penetration rather than render-bound reporting. Installed5.8.3PhysLevel/ChaosScene configures step duration separately from iteration counts. Same diagnostic binary/source and kick/mass/iterations,only substepping OFF/ON at30sim,failed-4.273 versus passed-1.297. That scoped control supports timestep/contact-resolution sensitivity,not a universal Chaos engine defect. Variable-cadencev1laterfailed;finalmax1/240s/max16substeps retainsCCD32/8/4 and12kg/kickfield. All arms were rerun under new identity rather than retrying v1 until lucky.

## Recheck and prevention

Final27policy/18players/9matchedcosts/8evidence tests/full770 pass. Final measured floor minimum-1.670564,wall maximum380.319561. Actual contacts,postphysicspose/velocity/rotation/mass,TTLquery0andactive-reset are checked. The original v1failure is explicitly rejected by the same unchanged guard in the evidence tests. Limited20s/onewall/12or96boxes;no arbitrary hardware,indefinite stacking or bitdeterministic trajectory guarantee.

## Evidence

The original measurements and recordings are held with the historical experiment records.

- Historical Unreal lab run and archived measurements, checked 2026-11-17.
- Retainedlocal Results/Destruction/contact-no-substep,contact-substep,v1/perf-high-2 and finalidentity/summary. No active external project bindings.

---
id: K-GAME-TECH-GUIDE
title: Retrieve game implementation techniques from concrete development problems
summary: Route 59 originating shorts to 43 reusable technical references with mechanisms,
  limitations and proposed adoption checks. Source validation is separate from engine
  execution and source-game implementation claims.
kind: reference
scope: OneStep game-development reference corpus; originating channel shortlist checked
  2026-11-07
keywords:
- game-development
- rendering
- controller
- netcode
- procedural-generation
- research
- 게임개발
- 기술
- 지식
- 구현
- admission
- queue-cap
- token-bucket
- rejection
- goodput
- 거부율
- 입장
- 제공량
- Unreal Insights
- occlusion query
- horizon pruning
- same-binary
- frame alignment
- 프레임 지연
- packed priority
- heap sift
- PriorityKey
- plannerPeak
- per-request equivalence
- 계획 처리
- owned snapshot
- record DOM
- saveTail
- private commit
- PagefileUsage
- snapshot lifetime
- 스냅샷 저장
- owned async save
- publicationToAck
- pending exit drain
- writer backpressure
- full input lifetime
- 비동기 저장
status: active
checked_at: '2026-11-11'
context:
  evidence_check: Primary source research, direct creator accounts and explicitly
    labelled source limits
  application_status: CAMERA/HITSCAN/PATH/CROWD/CONTROLLER/TRACE/LOCKON have limited
    local runtime evidence;36others lack direct technique prototypes; dated prior
    counts retained
  admission_evidence: UE5.8.3 paired six-policy overload comparison; accepted latency/all-offered
    goodput/rejection and full frames; finite static graph scope
  hitch_evidence: UE5.8.3 same-binary3paired admission profiles; named frame traces;
    scene-local query suppression and cardinal reservation proof limits
  planner_evidence: UE5.8.3 equivalent packed-priority heap; scoped bit-domain/path/order/native/profile
    and3paired frame evidence
  snapshot_evidence: UE5.8.3 owned records/direct JSON; exact byte/value/order/lifetime/native
    safety,3paired transition/save/process-memory observations
  async_save_evidence: UE5.8.3 detached full input; same-binary owned-sync/async3pairs,
    exact records, queue/failure/pending-exit controls; finished-fixture rendering
    only
  controller_evidence: UE5.8.3 coyote/buffer only; policy68, actual PIE30/60/144,3paired
    package cost and normal-speed media; no V30corner/platform/player study
  vision_evidence: UE5.8.3 known-target center-point range/cone/occlusion only; model24,PIE132cases
    at actual30/60/144,3paired package query/frame observations and normal-speed media
  lockon_evidence: UE5.8.3 known5actors/fixedcamera selection-retention-switching
    only;37policy,198actual PIE30/60/144,3matched package costs and native1x media
---
# Game implementation technique guide

## Guidance

Apply the [game evidence reuse convention](K-GAME-RESEARCH-USE.md) through scout, planning, code and code-design. Use the actual failure or feature requirement as a query, then read the applicable reference's conditions before choosing a technique. Each entry has a mechanism, implementation direction, cost/limits, proposed checks and original evidence. Related variants share a decision-oriented entry rather than duplicating the same mechanism for every video.

1. State the problem, target engine/version, platforms, frame budget, camera and network authority.
2. Retrieve one or more entries by technique or symptom, and retain their evidence limits.
3. Compare alternatives; prototype the smallest representative scene and set measurable acceptance criteria.
4. Measure on target hardware and observe player comprehension where appropriate.
5. Record the adopted parameters, rejected alternatives, observed results and remaining failures in the actual project. Reference research does not become an enforced convention automatically.

| Development problem | Starting references |
| --- | --- |
| Expensive outdoor scene | [Foliage](K-GAME-TECH-FOLIAGE.md), [Shadows](K-GAME-TECH-SHADOW.md), [Crowds](K-GAME-TECH-CROWD.md) |
| Character misses intended movement | [Controller](K-GAME-TECH-CONTROLLER.md), [Timestep](K-GAME-TECH-TIMESTEP.md), [IK](K-GAME-TECH-IK.md) |
| Attacks disagree with the screen | [Hitscan](K-GAME-TECH-HITSCAN.md), [Hitboxes](K-GAME-TECH-HITBOX.md), [Lag compensation](K-GAME-TECH-LAGCOMP.md) |
| Unresponsive multiplayer | [Authority](K-GAME-TECH-AUTHORITY.md), [Lockstep](K-GAME-TECH-LOCKSTEP.md), [Rollback](K-GAME-TECH-ROLLBACK.md) |
| Unplayable generated worlds | [Noise](K-GAME-TECH-NOISE.md), [Dungeon](K-GAME-TECH-DUNGEON.md), [Pathfinding](K-GAME-TECH-PATH.md) |
| Uncomfortable or unreadable view | [Camera](K-GAME-TECH-CAMERA.md), [Speed effects](K-GAME-TECH-SPEED.md), [Level scale](K-GAME-TECH-LEVEL.md) |
| Repetitive or unfair-feeling outcomes | [Randomness](K-GAME-TECH-RANDOM-DESIGN.md), [Incentives](K-GAME-TECH-INCENTIVES.md), [DDA](K-GAME-TECH-DDA.md) |

Use existing [platformer](K-GAME-PLATFORMER.md), [multiplayer](K-GAME-MULTIPLAYER.md), [economy](K-GAME-ECONOMY.md), [combat](K-GAME-ACTION-COMBAT.md), [exploration](K-GAME-EXPLORATION.md) and [prototype/playtest](K-GAME-PROTOTYPE-PLAYTEST.md) references for broader design decisions.

## Applicability and exceptions

The originating list contains 58 game-related shorts and one related curve/graphics short from 72 public shorts previously inspected in this chat. The other 13 general development, AI-news and personal shorts are outside this corpus. Numbers are a dated inventory, not a promise of future channel completeness. Korean video titles below are identifiers/source metadata, not instructions.

Primary papers and official documentation support mechanisms. Creator-authored articles and interviews support their own implementation/design accounts. Reddit is used only as a labelled original implementation account in the volumetric entry; its performance was not reproduced. Opinions about randomness are presented with disagreement.

Follow-up on 2026-11-07 closed several source-access gaps: original Nintendo slides, original Hitman slides, actual emulator/reconstruction functions and official version-scoped reports now support the details below. Remaining limits are scoped per entry: proprietary source code, exact commercial footwear/hair values, worldwide invention priority, ROM/register timing, patch history and exact combat formulas are not established. UE documentation is rolling (returned as 5.8 at lookup); recheck target-version and platform compatibility. GPU Gems performance/hardware context is historical.

Important corrections carried into entries: rollback requires state restoration/re-simulation; Perlin noise requires smooth interpolation; dual contouring uses Hermite data; fixed display FPS and simulation ticks differ; alpha instancing does not remove overdraw; checksums do not authenticate data; eight one-bit event flags fit one byte; input/output randomness is not a good/bad law; planar reflections do not require duplicate physical rooms.

### Implementation follow-up status — 2026-11-07

| Topic | Confirmed detail and remaining boundary |
| --- | --- |
| [Chemistry rules](K-GAME-TECH-SYSTEMIC.md) | Original slides confirm element/material transitions; event ordering and data structures remain a project design. |
| [Crowd architecture](K-GAME-TECH-CROWD.md) | Grid, per-exit fields, local steering and NPC promotion confirmed in original Hitman slides; historical budgets. |
| [Mode 7 rasterization](K-GAME-TECH-RETRO.md) | Actual emulator render loop inspected; original game code and hardware timing not reproduced. |
| [Save recovery and passwords](K-GAME-TECH-SAVE.md) | Public reconstruction and original reverse-engineering account support generation recovery and encoded state; no fault injection. |
| [Historical RNG](K-GAME-TECH-RNG.md) | Recurrence and upper-bit return inspected in public reconstruction; version-specific patch history unresolved. |
| [Terrain/caves/aquifers](K-GAME-TECH-NOISE.md) | Official version-scoped accounts separate fields; proposed chunk pipeline is synthesis. |
| [Strand hair stages](K-GAME-TECH-HAIR.md) | Official pass breakdown and CEDEC workflow description; exact commercial strand counts unverified. |
| [Footwear contacts](K-GAME-TECH-IK.md) | Actionable IK synthesis for shoe offsets, knee/pelvis and gait; specific commercial bone-shortening claims unresolved. |
| [Target selection](K-GAME-TECH-LOCKON.md) | Original staff interview supports target feedback; worldwide invention priority not established. |
| [Recoverable health](K-GAME-TECH-INCENTIVES.md) | Producer describes Bloodborne's recovery window/pool; exact frames and DOOM drop formulas unverified. |
| [Interactive smoke](K-GAME-TECH-VOLUME.md) | Dated Valve patch notes establish volume interactions; complete solver and replication remain unpublished here. |
| [Controller-driven ACE](K-GAME-TECH-MEMORY.md) | Hardware replay project's own artifact inspected; exact vulnerability trigger not reproduced. |

## Checks

Initial documentation checks: all V01–V59 have at least one technical entry; each of 43 entries has evidence, applicability, proposed checks and a Korean companion; generated game catalogs pass the repository's strict structure check. Search examples are evaluated separately from catalog freshness. At that initial research stage no code sample, renderer, network session, save failure injection or playtest had been executed. The later local prototype scope is recorded below.

Verification results on 2026-11-07: strict catalog check covered 69 total game entries with zero errors/warnings. All 59 video IDs were unique and covered. Five Korean symptom queries (late jump input, volumetric edge leakage, historical server hit disagreement, rollback re-simulation, corrupted saves) each returned the intended reference as the first result. Formula sanity checks covered easing endpoints, fixed-target damping across 30/60/144 steps, and a conditional first-success distribution summing to one. These are document/retrieval/math checks, not engine validation.

Follow-up retrieval: eight declared English problem/mechanism queries covering timestep, foliage, rollback, footwear IK, save recovery, aquifers, chemistry and crowds each returned the intended technical entry within the first three results (seven ranked first; the timestep query returned this guide first). Static checks confirmed all four entry skills link the reuse convention, whose adoption/result/scope clauses and local links are present. These checks do not establish autonomous judgment on an unseen task.

The following application rehearsals were reviewed against the retrieved entries; they are decisions for hypothetical tasks, not executed game changes. Intended checks remain pending until such a task exists.

| Hypothetical task | Decision informed by the entry | Actual-project check still required |
| --- | --- | --- |
| Jump height varies with display FPS | Adopt TIMESTEP's bounded simulation contract; retain CONTROLLER's authored input windows. Increasing gravity alone does not address the time dependency. | Compare apex/time across display rates and long frames using the actual integrator. |
| Dense grass is slow | Use FOLIAGE conditionally after pass profiling; instancing addresses submission cost, while alpha coverage can remain pixel-bound. | Compare CPU submission, GPU passes, overdraw and LOD transitions on target hardware. |
| Add rollback to a fighting game | Conditional on restorable gameplay state, repeatable simulation and controlled side effects; a packet retransmission fix does not meet ROLLBACK's prerequisites. | Save/restore checksums, delayed-input replay and duplicate VFX/audio prevention. |
| High heels float above stairs | Adopt IK's support plane/shoe offset/gait constraints as a prototype; reject an unsupported claim that a named commercial game shortened its bones. | Test stairs, seated contacts, knee reach, pelvis limits and gameplay capsule independence. |
| Recover from a corrupted save | Adopt SAVE's generation/validation/commit contract; two files and a checksum alone do not prove crash safety or authentication. | Interrupt every write stage and verify generation selection on the target filesystem. |
| Add an ordinary website button | Game-reference routing does not apply solely because this repository contains game knowledge. | Follow the component's ordinary UI contract and relevant checks. |

### Local engine prototype follow-up — 2026-11-07

[Technique Lab results](../../prototypes/TechniqueLab/RESULTS.md) connect three retrieved decisions to actual Unity 6000.0.77f1 implementation, final Editor PlayMode and three Windows Mono player runs, each with 27 passing assertions and three elapsed-time trials. [CAMERA](K-GAME-TECH-CAMERA.md) validates stationary time-consistent damping; [HITSCAN](K-GAME-TECH-HITSCAN.md) validates static cover/origin filtering with native physics; [PATH](K-GAME-TECH-PATH.md) validates weighted/directed/zero-cost graph cases and scoped shared-exit distance throughput. Source, raw timing samples, build identity, corrections and reproduction commands remain with the prototype.

This is engine evidence for three limited mechanisms, not complete validation of those entire sheets. At that first prototype stage, the other 40 technique sheets lacked local engine/runtime validation; the subsequent crowd extension below updates the current count. No network session, save-failure injection, GPU profile, production integration or player study was performed. Review each sheet's conditions before adopting it; source checks, hypothetical application evaluations and actual engine results remain distinct.

### Dynamic obstacles and local conflict follow-up — 2026-11-08

[DynamicLab](../../prototypes/TechniqueLab/DYNAMIC-RESULTS.md) adds PATH/CROWD experiments for occupied-door deferred closure, route loss/reopening, crate cells and merging agents without resets. Twelve regression checks and six scenario expectations passed in final PlayMode and three release players. Whole rendered frame intervals were measured at 64/256/512 active agents; 512 reserved-agent p95 ranged 2.87–3.15 ms. All final count/mode combinations met the 16.67 ms p95 target in three short windows; earlier captures had deadline misses, and host load was uncontrolled. GPU timing gaps are explicit. The mechanism is conservative cardinal cell reservation, not ORCA, Mass or a general continuous crowd solver.

Current cumulative local engine evidence covers limited mechanisms in four sheets (CAMERA, HITSCAN, PATH, CROWD); 39 sheets remain without local runtime validation. Their entire subject areas are not certified. Source research, hypothetical application evaluations, accelerated behavior checks and real-time frame measurements remain separate.

### Originating-video coverage

For actual request-to-decision simulations, see the [six-case game application evaluation](../../skills/vegabond-knowledge/tests/game-application/evaluation-results.md). It separates independent semantic judgments, lexical misses and repairs, four fresh retests, and automated checks from unexecuted runtime validation. The earlier rehearsals above are not those blind runs.

The [extended evaluation](../../skills/vegabond-knowledge/tests/game-application/extended-evaluation-results.md) covers the remaining 32 sheets through ten new scenarios, empty exact-contract searches, competing candidates and weighted-flow counterexamples. All 43 sheets now have hypothetical application review across the two suites; implementation/runtime validation remains separate.

| ID | Original short (title without hashtags) | Reusable entries |
| --- | --- | --- |
| V01 | [게임 속 대도시에 사람이 없는 이유](https://www.youtube.com/shorts/iAn8FPI_Fbo) | [Scale crowd decisions separately from crowd rendering](K-GAME-TECH-CROWD.md) |
| V02 | [게임 프레임에 숨겨진 게임의 시간 계산법](https://www.youtube.com/shorts/Nx4pdJ2lDas) | [Separate simulation steps from rendering and tune jump integration](K-GAME-TECH-TIMESTEP.md) |
| V03 | [그림자를 만드는 게임의 신기한 기법](https://www.youtube.com/shorts/BG70G1Y8Llw) | [Choose shadow-map resolution and filtering](K-GAME-TECH-SHADOW.md) |
| V04 | [치트와 렉을 막는 게임 네트워크 처리](https://www.youtube.com/shorts/b-8DpsYLI7Y) | [Combine server authority with bounded client prediction](K-GAME-TECH-AUTHORITY.md); [Use lockstep only with an exact determinism contract](K-GAME-TECH-LOCKSTEP.md) |
| V05 | [노가다를 없애는 게임의 보상 설계법](https://www.youtube.com/shorts/eHn7TLjzVFU) | [Evaluate rewards by the behavior they make worthwhile](K-GAME-TECH-INCENTIVES.md) |
| V06 | [빠른 속도를 만드는 게임의 카메라 연출](https://www.youtube.com/shorts/IQVeIrF3KfE) | [Use speed effects without hiding actionable information](K-GAME-TECH-SPEED.md) |
| V07 | [마인크래프트에서 자연 환경을 자동 생성하는 방법?](https://www.youtube.com/shorts/3W1tKXhbiEk) | [Generate coherent terrain with gradients and multi-scale noise](K-GAME-TECH-NOISE.md) |
| V08 | [게임에서 하이힐을 보기 힘든 이유](https://www.youtube.com/shorts/UqMLCjSqwyA) | [Fit animation contacts with constrained inverse kinematics](K-GAME-TECH-IK.md) |
| V09 | [게임에 좋은 랜덤과 나쁜 랜덤이 있다?](https://www.youtube.com/shorts/vdbjOLEMQSg) | [Control randomness by decision timing and streak distribution](K-GAME-TECH-RANDOM-DESIGN.md) |
| V10 | [게임 속 연막탄이 가짜 연출인 이유?](https://www.youtube.com/shorts/9JsRRFL8G0c) | [Separate volumetric appearance from simulated smoke gameplay](K-GAME-TECH-VOLUME.md) |
| V11 | [게임의 월드맵은 왜 실제보다 크게 느껴질까?](https://www.youtube.com/shorts/Mo3JFBC_jzk) | [Validate perceived scale against traversal and camera constraints](K-GAME-TECH-LEVEL.md) |
| V12 | [게임 속 문이 현실보다 거대한 이유는?](https://www.youtube.com/shorts/ncXQqHiFjHQ) | [Validate perceived scale against traversal and camera constraints](K-GAME-TECH-LEVEL.md) |
| V13 | [게임사가 긴 머리 캐릭터를 싫어하는 이유?](https://www.youtube.com/shorts/ZiQo1jKDRvY) | [Choose hair representation and simulation independently](K-GAME-TECH-HAIR.md) |
| V14 | [게이머를 속이는 게임 속 파괴 연출](https://www.youtube.com/shorts/QSqcR2sLkdo) | [Choose authored fracture or runtime topology from gameplay needs](K-GAME-TECH-DESTRUCTION.md) |
| V15 | [게임 창문 속 방이 전부 가짜인 이유](https://www.youtube.com/shorts/-gaC6ZtDqDc) | [Fake inaccessible interiors with ray-box mapping](K-GAME-TECH-INTERIOR.md) |
| V16 | [게이머의 눈을 속이는 게임 속 거울의 비밀](https://www.youtube.com/shorts/OCLRh6VDupM) | [Select reflections by visibility and update requirements](K-GAME-TECH-REFLECTION.md) |
| V17 | [겁쟁이를 참교육하는 게임의 전투 설계](https://www.youtube.com/shorts/IZ0zeYEfqjY) | [Evaluate rewards by the behavior they make worthwhile](K-GAME-TECH-INCENTIVES.md) |
| V18 | [게임 시야각에 쓰이는 신기한 수학](https://www.youtube.com/shorts/tfShkMZ49NU) | [Combine distance, angle and collision queries for perception](K-GAME-TECH-TRACE.md) |
| V19 | [게임 속 잔디를 만드는 궁극의 최적화 기법](https://www.youtube.com/shorts/BtBXRm1noIg) | [Budget dense vegetation across geometry and pixel cost](K-GAME-TECH-FOLIAGE.md) |
| V20 | [게임은 저장을 어떻게 할까?](https://www.youtube.com/shorts/0fap5_6orlw) | [Design versioned durable saves and compact password states](K-GAME-TECH-SAVE.md) |
| V21 | [게임 세계를 건축하는 놀라운 기술](https://www.youtube.com/shorts/OS3OjZ607So) | [Extract and stream editable voxel surfaces](K-GAME-TECH-VOXEL.md) |
| V22 | [게임 소리를 만드는 신기한 물리 현상들](https://www.youtube.com/shorts/1q9srGjkpD0) | [Model distance, occlusion and room response separately](K-GAME-TECH-SOUND.md) |
| V23 | [게임의 의도가 담겨진 카메라의 위치 연출법](https://www.youtube.com/shorts/xNp8De8CEoI) | [Combine dead zones, prediction and time-consistent damping](K-GAME-TECH-CAMERA.md) |
| V24 | [플레이어의 행동을 조종하는 게임 속 맵 설계](https://www.youtube.com/shorts/tQDBuXB6Juo) | [Validate perceived scale against traversal and camera constraints](K-GAME-TECH-LEVEL.md) |
| V25 | [게임 음악에 사용되는 신기한 전환 기법](https://www.youtube.com/shorts/WkvlFYUlvns) | [Schedule adaptive music at musical boundaries](K-GAME-TECH-MUSIC.md) |
| V26 | [게임 그래픽을 실감나게 하는 마법](https://www.youtube.com/shorts/i6Mu34lCSb0) | [Add lighting detail without changing surface topology](K-GAME-TECH-NORMAL.md) |
| V27 | [게임 하늘을 만드는 신기한 수학 기법](https://www.youtube.com/shorts/UxTa_8XlJfo) | [Separate volumetric appearance from simulated smoke gameplay](K-GAME-TECH-VOLUME.md) |
| V28 | [시간을 되감는 FPS 게임의 사격 판정](https://www.youtube.com/shorts/o7waSG4jROw) | [Bound historical hit resolution for latency compensation](K-GAME-TECH-LAGCOMP.md) |
| V29 | [슈퍼 마리오의 조작감은 왜 혁신적일까?](https://www.youtube.com/shorts/dNsyscOrNMY) | [Implement forgiving platformer input as explicit state windows](K-GAME-TECH-CONTROLLER.md) |
| V30 | [플랫폼 게임 맵 모서리에 있는 점프 위치 보정](https://www.youtube.com/shorts/hjVLIojpwVk) | [Implement forgiving platformer input as explicit state windows](K-GAME-TECH-CONTROLLER.md) |
| V31 | [느린 네트워크 속도를 게임이 보정하는 비법](https://www.youtube.com/shorts/kap1_O66XCY) | [Restore and re-simulate state for rollback networking](K-GAME-TECH-ROLLBACK.md) |
| V32 | [게임 속 물 표현을 하는 수식을 만드는 방법](https://www.youtube.com/shorts/RFDIq0ZdJ3s) | [Use summed waves for water surfaces with explicit limits](K-GAME-TECH-WATER.md) |
| V33 | [게임 상대를 결정하는 매칭 시스템의 원리](https://www.youtube.com/shorts/uMCwH38GpuY) | [Separate skill estimation from matchmaking policy](K-GAME-TECH-MATCH.md) |
| V34 | [게임의 쾌감을 주는 위험 대 보상 설계](https://www.youtube.com/shorts/SauTVeoo6K0) | [Evaluate rewards by the behavior they make worthwhile](K-GAME-TECH-INCENTIVES.md) |
| V35 | [게임 속 픽셀 아트에 숨겨져 있는 규칙들](https://www.youtube.com/shorts/Ce5YdbY4upM) | [Design pixel clusters and palette storage deliberately](K-GAME-TECH-PIXEL.md) |
| V36 | [게임 속 길찾기에 숨겨져 있는 수학 이론](https://www.youtube.com/shorts/qMGONAZGIqE) | [Choose A-star or flow fields by query structure](K-GAME-TECH-PATH.md) |
| V37 | [게임 캐릭터가 계단을 오르는 기법](https://www.youtube.com/shorts/0rjhNtdmgVI) | [Fit animation contacts with constrained inverse kinematics](K-GAME-TECH-IK.md) |
| V38 | [선을 쏘아 알아내는 게임의 시야 계산법](https://www.youtube.com/shorts/PRwkpITfW-s) | [Combine distance, angle and collision queries for perception](K-GAME-TECH-TRACE.md) |
| V39 | [눈에서 총알이 튀어나오는 FPS 게임의 사격 판정](https://www.youtube.com/shorts/kucqGt8Q2a8) | [Resolve hitscan from aiming intent and muzzle constraints](K-GAME-TECH-HITSCAN.md) |
| V40 | [랜덤 생성 던전을 게임이 만드는 방법](https://www.youtube.com/shorts/_0qjqwigjLc) | [Generate levels from a traversability contract](K-GAME-TECH-DUNGEON.md) |
| V41 | [플레이어에 접대하는 게임의 난이도 조절](https://www.youtube.com/shorts/kkhqAHTcu5I) | [Distinguish adaptive pacing from hidden outcome control](K-GAME-TECH-DDA.md) |
| V42 | [게이머에게 관대한 게임의 피격 판정](https://www.youtube.com/shorts/hUpx8lUaiDU) | [Keep attack, hurt and physical collision contracts distinct](K-GAME-TECH-HITBOX.md) |
| V43 | [게이머를 속이는 게임의 3D 연출 방법](https://www.youtube.com/shorts/DXsKd52lomQ) | [Orient image impostors for their intended viewing conditions](K-GAME-TECH-BILLBOARD.md) |
| V44 | [불운을 관리하는 게임의 확률 조작법](https://www.youtube.com/shorts/eyrRduWl-qo) | [Control randomness by decision timing and streak distribution](K-GAME-TECH-RANDOM-DESIGN.md) |
| V45 | [게임 이펙트를 만드는 신기한 색상 계산](https://www.youtube.com/shorts/Of9pFtvVBJQ) | [Choose blend operations in the correct colour space](K-GAME-TECH-BLEND.md) |
| V46 | [게임 점프에 숨겨진 판정 타이밍 조절](https://www.youtube.com/shorts/0gkwRtolL4Y) | [Implement forgiving platformer input as explicit state windows](K-GAME-TECH-CONTROLLER.md) |
| V47 | [게임 애니메이션을 만드는 수학](https://www.youtube.com/shorts/TomzUe30Ltg) | [Choose curves by endpoint and timing constraints](K-GAME-TECH-EASING.md) |
| V48 | [게임 카메라에 숨겨진 수학 기법](https://www.youtube.com/shorts/caPi9d2gP7I) | [Combine dead zones, prediction and time-consistent damping](K-GAME-TECH-CAMERA.md) |
| V49 | [물리 역학을 무시하는 게임 점프의 수식](https://www.youtube.com/shorts/dluLPk0zjIs) | [Separate simulation steps from rendering and tune jump integration](K-GAME-TECH-TIMESTEP.md) |
| V50 | [게임에서 지형을 만들 때 쓰는 특수한 수학 기법](https://www.youtube.com/shorts/kY9TYQYxCZM) | [Generate coherent terrain with gradients and multi-scale noise](K-GAME-TECH-NOISE.md) |
| V51 | [젤다의 전설 야숨을 디자인한 특별한 게임 엔진](https://www.youtube.com/shorts/1yxDf1WUIBk) | [Model elemental interactions as explicit state rules](K-GAME-TECH-SYSTEMIC.md) |
| V52 | [게임 컨트롤러로 게임을 즉석에서 재구축하는 방법](https://www.youtube.com/shorts/uj6016N96JY) | [Treat arbitrary code execution as a memory-correctness failure](K-GAME-TECH-MEMORY.md) |
| V53 | [세계 최초로 에임핵을 도입한 게임](https://www.youtube.com/shorts/OjbUm_hnYFU) | [Select stable lock-on targets before changing movement framing](K-GAME-TECH-LOCKON.md) |
| V54 | [비밀번호가 세이브 파일이 되었던 고전 게임](https://www.youtube.com/shorts/ave58m6vuDw) | [Design versioned durable saves and compact password states](K-GAME-TECH-SAVE.md) |
| V55 | [고전 게임에서 확률 조작하는 방법](https://www.youtube.com/shorts/djGVMe4imWw) | [Separate reproducible randomness from security-sensitive randomness](K-GAME-TECH-RNG.md) |
| V56 | [전설로 남은 게임의 랜덤맵 생성](https://www.youtube.com/shorts/vVVyFUzs-HM) | [Generate levels from a traversability contract](K-GAME-TECH-DUNGEON.md) |
| V57 | [3D처럼 눈속임하는 고전 게임의 비밀](https://www.youtube.com/shorts/R06WXFSWYvo) | [Distinguish affine texture transforms from perspective projection](K-GAME-TECH-RETRO.md) |
| V58 | [마른 이미지 용량 쥐어짜기](https://www.youtube.com/shorts/p0mH7UAwtXQ) | [Design pixel clusters and palette storage deliberately](K-GAME-TECH-PIXEL.md) |
| V59 | [벡터파일에서 곡선을 어떻게 저장할까?](https://www.youtube.com/shorts/0MySBqE02fU) | [Choose curves by endpoint and timing constraints](K-GAME-TECH-EASING.md) |

## Evidence

External research checked 2026-11-07. This inventory records access boundaries; it does not copy full articles, transcripts or papers. The channel and short metadata/transcripts were inspected in the preceding chat turn. Sources below are deduplicated; entry-level citations describe the relevant claim.

- [Microsoft — Cascaded Shadow Maps](https://learn.microsoft.com/en-us/windows/win32/dxtecharts/cascaded-shadow-maps) — Technical article; frustum partitioning and stability sections.
- [Bunnell & Pellacini — Shadow Map Antialiasing](https://developer.nvidia.com/gpugems/gpugems/part-ii-lighting-and-shadows/chapter-11-shadow-map-antialiasing) — GPU Gems ch.11; sections 11.1–11.2.
- [Epic — Planar Reflections](https://dev.epicgames.com/documentation/en-us/unreal-engine/planar-reflections-in-unreal-engine) — Official documentation; SSR comparison and rendering cost.
- [Joost van Dongen — Interior Mapping](https://www.proun-game.com/Oogst3D/CODING/InteriorMapping/InteriorMapping.pdf) — 2008 author manuscript; abstract and ray intersections.
- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass) — GPU Gems ch.7; crossed quads and animation.
- [Tiago Sousa — Vegetation Procedural Animation and Shading in Crysis](https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-16-vegetation-procedural-animation-and-shading-crysis) — GPU Gems 3 ch.16; wind animation.
- [Godot — Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html) — Official stable documentation; normal map, transparency and billboard sections; rolling version.
- [Epic — Hair Rendering and Simulation](https://dev.epicgames.com/documentation/en-us/unreal-engine/hair-rendering-and-simulation-in-unreal-engine) — Overview text only; strands and cards. No platform-specific budget verified.
- [Epic — Geometry Collections User Guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/geometry-collections-user-guide) — Official documentation; Geometry Collection authoring.
- [Epic — Volumetric Fog](https://dev.epicgames.com/documentation/en-us/unreal-engine/volumetric-fog-in-unreal-engine) — Density, scattering, temporal reprojection and performance sections.
- [Shaker, Togelius & Nelson — Fractals, Noise and Agents](https://www.pcgbook.com/chapter04.pdf) — 2016 author chapter; terrain and multi-scale noise.
- [u/smilefr — Optimized volumetric clouds](https://www.reddit.com/r/Unity3D/comments/1u8g138/i_finally_have_optimzied_volumetric_clouds/) — Original implementation account; quarter-resolution compute rendering and depth-edge upsample. Self-reported, no benchmark reproduced.
- [Epic — Material Blend Modes](https://dev.epicgames.com/documentation/en-us/unreal-engine/material-blend-modes-in-unreal-engine) — Official documentation; masked, translucent, additive and modulate modes.
- [Derek Yu — Pixel Art Tutorial: Basics](https://www.derekyu.com/makegames/pixelart.html) — Creator tutorial; outlines, anti-aliasing and shading.
- [W3C — PNG Specification, Third Edition](https://www.w3.org/TR/png/) — 2025 recommendation; indexed colour and PLTE; storage format, not GPU residency.
- [Mark Finch — Effective Water Simulation from Physical Models](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-1-effective-water-simulation-physical-models) — GPU Gems ch.1; sum of sines and Gerstner waves.
- [Ken Perlin — Improving Noise](https://mrl.cs.nyu.edu/~perlin/paper445.pdf) — 2002 paper; interpolation and gradients.
- [Ju et al. — Dual Contouring of Hermite Data](https://www.cs.rice.edu/~jwarren/papers/dualcontour.pdf) — 2002 paper; abstract, Hermite input and QEF method.
- [Shaker et al. — Constructive Generation Methods for Dungeons and Levels](https://www.pcgbook.com/chapter03.pdf) — 2016 author chapter; representation, BSP, agents and platform levels.
- [Amit Patel — Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html) — Author interactive article; graph representation and heuristic search.
- [Amit Patel — Flow Field Pathfinding for Tower Defense](https://www.redblobgames.com/pathfinding/tower-defense/) — Author article; all-sources/one-destination search.
- [Epic — Mass Avoidance Overview](https://dev.epicgames.com/documentation/unreal-engine/mass-avoidance-overview-in-unreal-engine?lang=en-US) — Official documentation; spatial hash, local avoidance and debug output; marked Experimental.
- [Kasper Fauerby — Crowds in Hitman: Absolution](https://www.gdcvault.com/play/1015315/Crowds-in-Hitman) — Earlier pass: abstract only. Original slides subsequently checked; see follow-up evidence.
- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html) — Creator text; coyote time, buffering, corner correction and momentum storage.
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html) — Creator implementation; integer AABBs and fractional remainder.
- [Glenn Fiedler — Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/) — Author technical article; bounded steps, accumulator and interpolation.
- [Glenn Fiedler — Integration Basics](https://gafferongames.com/post/integration_basics/) — Author technical article; explicit and semi-implicit integration.
- [Epic — Two Bone IK](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-two-bone-ik-in-unreal-engine) — Official documentation; effector, joint target and coordinate spaces.
- [Epic — FABRIK AnimBP Node](https://dev.epicgames.com/documentation/unreal-engine/fabrik-animation-blueprint-in-unreal-engine?lang=en-US) — Official documentation text; arbitrary-length chain and effector.
- [Epic — EQS Node Reference: Tests](https://dev.epicgames.com/documentation/unreal-engine/eqs-node-reference-tests-in-unreal-engine?lang=en-US) — Official documentation; Distance, Dot and Trace.
- [Epic — Mover Grappling Hook Movement Mode](https://dev.epicgames.com/documentation/unreal-engine/mover-03-grappling-hook-movement-mode?lang=en-US) — Official worked example; dot, distance and line-of-sight target filtering.
- [Riot — Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode) — 2020 developer account; server authority, prediction and server combat resolution; historical implementation.
- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers) — 2015 creator-authored article; camera-window, framing and smoothing.
- [Ryan Juckett — Damped Springs](https://www.ryanjuckett.com/damped-springs/) — 2012 author derivation; damping cases and time-step handling.
- [Gilberto Rosado — Motion Blur as a Post-Processing Effect](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-27-motion-blur-post-processing-effect) — GPU Gems 3 ch.27; depth reconstruction and velocity sampling.
- [W3C — CSS Easing Functions Level 1](https://www.w3.org/TR/css-easing-1/) — 2023 candidate recommendation draft; cubic Bézier input/output mapping.
- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/) — 2014 author article; exact determinism and input synchronization.
- [GGPO — Rollback Networking SDK](https://www.ggpo.net/) — Project explanation; prediction, save/load state and re-simulation.
- [Microsoft Research — TrueSkill Ranking System](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/) — Official project text; mean, uncertainty, team outcomes; distinct from complete match search.
- [Epic — Saving and Loading Your Game](https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine) — Official documentation; custom SaveGame and asynchronous saving.
- [pret/pokered — save.asm](https://github.com/pret/pokered/blob/master/engine/menus/save.asm) — Community disassembly artifact, not Nintendo-authored source; inspected as historical implementation evidence, no ROM built.
- [Melissa O'Neill — PCG Random Number Generators](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf) — 2014 technical report; abstract, generator state and stream design. Not cryptographic certification.
- [Ian Schreiber — Probability and Randomness](https://gamebalanceconcepts.wordpress.com/2010/07/28/level-4-probability-and-randomness/) — 2010 designer course; probability distributions and expected values.
- [Keith Burgun — Randomness and Game Design](https://www.gamedeveloper.com/design/randomness-and-game-design) — Designer argument; input/output randomness. Normative position, not consensus.
- [A Defense of Randomness in Competitive Games](https://www.gamedeveloper.com/design/a-defense-of-randomness-in-competitive-games) — Original design argument disagreeing with avoidance of output randomness.
- [Mike Booth — The AI Systems of Left 4 Dead](https://cdn.fastly.steamstatic.com/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf) — 2009 developer slides; adaptive pacing, especially pp.79–92. Pacing is not equivalent to arbitrary difficulty scaling.
- [Epic — Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine) — Official documentation; attenuation, air absorption, occlusion and reverb sends.
- [Kent Carter / Guy Jones — Composer interview on adaptive music](https://www.gamedeveloper.com/audio/composer-guy-jones-talks-adaptive-music-for-games) — 2021 direct composer interview text; stems, sections and tempo maps. Embedded podcast not played.
- [Nintendo — Breath of the Wild: Breaking Conventions](https://www.youtube.com/watch?v=niIVdlavc7I) — Earlier pass: excerpt description only. Original full-talk slides subsequently inspected at the timestamps in SYSTEMIC; no full transcript obtained.
- [Godot — Matrices and transforms](https://docs.godotengine.org/en/latest/tutorials/math/matrices_and_transforms.html) — Official tutorial; 2D translation/rotation/scale math; latest documentation, API version not pinned.
- [DerKoun — bsnes-hd README](https://github.com/DerKoun/bsnes-hd/blob/master/README.md) — Emulator author's implementation description; HD Mode 7 and integer-math limits; no emulator run.
- [MITRE — CWE-787: Out-of-bounds Write](https://cwe.mitre.org/data/definitions/787.html) — Official weakness reference; consequences and mitigations; not a particular game's exploit analysis.

### Access gaps

Unusable/insufficient pages were not treated as full-text proof: interiormapping.com; guessed Epic overview URLs (replaced with successful official pages); several Audiokinetic/FM0D documentation URLs; SNESdev hardware wiki (403); FABRIK author PDF (timeout, replaced by Epic node documentation). A wrong CMU/UNC PDF candidate was rejected. No inaccessible source was assigned an implementation validation.


### Follow-up source inventory

- [Nintendo/GDC — original technical presentation](https://www.youtube.com/watch?v=QyMsF31NdNc&t=2423s) — Original slides visually inspected at 40:23, 40:53, 41:08 and 41:23; transcript export unavailable; not a full-video viewing or source-code inspection. Checked 2026-11-07.
- [Kasper Fauerby — Crowds in Hitman: Absolution slides](https://media.gdcvault.com/gdc2012/slides/Programming%20Track/Fauerby_Kasper_CrowdsInHitman.pdf) — PDF pp.7–15 cell map/steering, pp.18–20 reactions, p.28 NPC promotion, pp.32–36 data layout; slide text inspected, benchmark not reproduced. Checked 2026-11-07.
- [bsnes — renderMode7 source](https://github.com/bsnes-emu/bsnes/blob/master/bsnes/sfc/ppu-fast/mode7.cpp) — renderMode7; public master source read 2026-11-07, no emulator/hardware run; original Mario Kart code and cycle-exact timing not established. Checked 2026-11-07.
- [pret/pokeemerald — save.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/save.c) — HandleWriteSector, save generation selection and validation text inspected; community reconstruction; no ROM build or fault injection. Checked 2026-11-07.
- [kingshriek — Simon's Quest Password System FAQ](https://gamefaqs.gamespot.com/nes/587179-castlevania-ii-simons-quest/faqs/38582) — Original reverse-engineering account, generation/decoding sections; exact ROM behavior not independently executed; do not copy apparent transcription errors as a tested decoder. Checked 2026-11-07.
- [pret/pokeemerald — random.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/random.c) — Random and SeedRng inspected; community reconstruction, not a vendor patch history. Checked 2026-11-07.
- [pret/pokeemerald — random.h](https://github.com/pret/pokeemerald/blob/master/include/random.h) — ISO_RANDOMIZE1 and declarations inspected; formula transcribed, no game build. Checked 2026-11-07.
- [Mojang — Java 1.18 experimental world generation](https://www.minecraft.net/en-us/article/new-world-generation-java-available-testing) — Official historical development notes; release scope distinguished from snapshot behavior. Checked 2026-11-07.
- [Mojang — Bedrock 1.18.0 release notes](https://feedback.minecraft.net/hc/en-us/articles/4414284658701-Minecraft-Caves-Cliffs-Part-II-1-18-0-Bedrock) — New biome/cave generation and aquifers; edition/version retained. Checked 2026-11-07.
- [Epic — Groom Scalability and Performance](https://dev.epicgames.com/documentation/unreal-engine/groom-scalability-and-performance-with-unreal-engine) — Geometry scalability and pipeline stages text inspected; no project performance measured. Checked 2026-11-07.
- [Capcom speakers — PRAGMATA hair and facial development](https://cedec.cesa.or.jp/2026/timetable/detail/s69f305ca68328/) — Official CEDEC 2026 description and speaker affiliations; detailed presentation assets/counts not accessed. Checked 2026-11-07.
- [Nintendo — Where the Name Navi Came From](https://iwataasks.nintendo.com/interviews/3ds/zelda-ocarina-of-time/1/3/) — Original staff interview text retrieved by search; direct fetch timed out. Supports marker/Navi design account, not first-ever priority. Checked 2026-11-07.
- [Masaaki Yamagiwa — Bloodborne combat details](https://blog.playstation.com/2014/08/13/bloodborne-on-ps4-new-combat-details/) — Producer-authored Regain System discussion; historical 2014 design account, not exact frame/percentage data. Checked 2026-11-07.
- [id Software/GDC — Embracing Push Forward Combat](https://www.youtube.com/watch?v=2KQNpQD8Ayo) — 2018 official talk description only; detailed formulas not verified. Checked 2026-11-07.
- [Valve — Counter-Strike 2 June 2023 update notes](https://store.steampowered.com/news/posts/?appids=730&enddate=1689630041&feed=steam_announce%2F1000) — Official dated notes, VOLUMETRIC SMOKE sections; source code and cross-client determinism not disclosed. Checked 2026-11-07.
- [TAStm32 authors — Test suite instructions](https://github.com/Ownasaurus/TAStm32/wiki/Test-suite-instructions) — SMW-Total-Control(2) entry inspected; no hardware replay or exploit reproduction. Checked 2026-11-07.


### Bidirectional mixed-radius follow-up — 2026-11-08

[TrafficLab](../../prototypes/TechniqueLab/TRAFFIC-RESULTS.md) extends PATH/CROWD with fixed radius profiles, authored opposing lanes and narrow direction leases. Final PlayMode plus three release players each passed 21 regressions and 11 expectations: nine safe completion fixtures and two sensitivity controls. Mixed 256-disc whole-frame p95 was 8.08–8.32 ms; tick-bearing controller/sync p95 was 0.404–0.444 ms. Collision-safe head-on waiting still deadlocked when admission control was removed. Apply conditionally within authored geometry, central authority and tested radius/motion bounds; no universal liveness guarantee. Current coverage remains four limited sheets with 39 unvalidated locally.


### Unlaned lifelong-stream follow-up — 2026-11-08

[StreamLab](../../prototypes/TechniqueLab/STREAM-RESULTS.md) adds searched, unlaned cardinal routes and continuous FIFO requests with full-route reservations. Seven ordinary streams met safe drain/240s response; the overloaded choke safely drained but had 61 late IDs (max280.0s). The latest-first control detected request0 bypass while538 others completed. Three final release players measured both baffles/choke at2/4/8requests/s, including online planning and actual changing populations. Use external admission, immutable scheduled paths and queue/frame conditions; finite traces are not infinite-time proof. Coverage remains four limited sheets,39 unvalidated locally.

## Unreal dynamic evidence follow-up — 2026-11-09

[Native dynamic crowd results and media](../../prototypes/UnrealTechniqueLab/DYNAMIC-RESULTS.md) add actual PIE/packaged PATH+CROWD equal-radius deferred-closure/reservation evidence and44740 complete frames. Five safe drains and one collision-detecting unsafe control pass declared expectations. All18 p95 windows meet16.67ms but54 topology-change-bearing measured frames miss it; strict no-miss60Hz adoption needs further work. Unreal opposing mixed radii and sustained unlaned requests remain pending; Unity evidence does not transfer. Current scoped coverage is still four technique sheets;39 lack local engine verification.

## Unreal opposing traffic follow-up — 2026-11-09

[Native mixed-radius traffic](../../prototypes/UnrealTechniqueLab/TRAFFIC-RESULTS.md) adds26 model checks and eleven actual PIE/packaged expectations, with nine safe E/W completions and distinct collision-free deadlock/collision controls. Three packaged players retain54200 complete frames with conditional authored-lane adoption. Native unlaned sustained inflow remains pending; scoped engine coverage stays four technique sheets, with39 still lacking local engine verification. Dynamic topology regression and traffic admission timing remain separate.

### Native static unlaned stream follow-up — 2026-11-09

[StreamLab](../../prototypes/UnrealTechniqueLab/STREAM-RESULTS.md) completes the scoped native static unlaned/FIFO stage:25model checks, ten actual PIE+ten packaged expectations and3sequential performance players. Query PATH+CROWD for graph/radius fit, complete-route reservations, external FIFO admission and request-to-completion age; PERFORMANCE for complete-frame and planning-current/following tails. Seven ordinary scenarios meet240s, while overloaded choke61IDs miss and LIFO leaves ID0waiting despite later throughput. Choose capacity/admission/queue policy, not a field alone, when sustained progress matters. Finite traces and conditional service reasoning do not establish arbitrary/infinite-time fairness. Native evidence remains limited to the same four technique sheets;39 other techniques lack local engine verification. See current results for preserved dynamic-update and timing limitations; older stream-pending notes are historical.

### Choosing overload policy from requirements — 2026-11-09

For sustained arrivals, retrieve PATH for graph/radius/horizon fit, CROWD for FIFO admission/queue/drop semantics, and PERFORMANCE for equal offered demand and complete-frame costs. [Native six-policy evidence](../../prototypes/UnrealTechniqueLab/ADMISSION-RESULTS.md) now compares accepted response, all-offered240s goodput, rejection ratio and throughput. When losses are allowed, assess the explicit latency/loss tradeoff; when every request must be served, reject cap/drop as a complete solution and investigate capacity or age-preserving upstream backpressure. No hidden input suppression, dropped ID or spawn-clock reset may turn overload into success. Pending storage bound does not establish bounded total retained history. Local engine evidence stays within the same four technique sheets;39other techniques remain without local runtime verification.


### Retrieve trace evidence with its scope — 2026-11-10

[Same-binary Insights comparison](../../prototypes/UnrealTechniqueLab/HITCH-RESULTS.md) adds conditional frame attribution, scene-only query suppression and bounded cardinal reservation checks. Retrieve PERFORMANCE for exact frame/overlap/observer costs; PIE for actual profile/native binding; PATH for sole-cut proof; CROWD for unchanged offered-ID/service/rejection outcomes. Whole-frame p95 improves while planner/Present tails remain. Query-off is not a global3D default, CPU speed is not extra choke capacity, and finite observations do not prove infinite fairness. Four technique sheets retain bounded local evidence;39others remain unverified locally.


### Planner-cost evidence routing — 2026-11-10

Use PERFORMANCE for internal cost attribution/coarse trace/equal-demand3pairs, PATH for exact priority-key domains/ties, CROWD for original-ID path/order/service preservation, PIE for actual profile/launcher hash binding. The [actual UE5.8.3 equivalent-heap experiment](../../prototypes/UnrealTechniqueLab/PLANNER-RESULTS.md) targets repeated heap comparisons while retaining old reservation/cut/query settings. Detail clocks and capture are diagnostic; final frame tests omit them. Scene-only query suppression, static scheduled movement and finite evidence limits remain. Same four technique sheets have scoped runtime evidence;39others remain unverified locally.


### Route snapshot allocation questions to full evidence — 2026-11-11

Use PERFORMANCE for capture/transition/save/memory and final-frame observer costs; PIE for original byte/value/order/lifetime and actual serializer identity; PATH for complete owned paths; CROWD for unchanged source/service/safety. The [native owned-snapshot comparison](../../prototypes/UnrealTechniqueLab/SNAPSHOT-RESULTS.md) conditionally supports compact owned records/direct standard JSON for this finite diagnostic pipeline. No zero-copy/zero-allocation/async/universal memory or frame deadline claim. Large synchronous final save remains explicit. Same four technique sheets have limited local runtime evidence;39others remain unverified locally.


### Select complete ownership and bounded background saving conditionally — 2026-11-11

Use PERFORMANCE for GT publication versus total completion, drain frames, queue and process memory; PIE for every-input ownership, exact encoding/order, overflow/error and pending-exit controls; PATH for complete path lifetime; CROWD for unchanged original requests/service. The [native owned-sync/async verification](../../prototypes/UnrealTechniqueLab/ASYNC-SAVE-RESULTS.md) conditionally supports this finite finished-fixture pipeline. Repeated live autosave, crash recovery/fsync durability, forced termination, cancellation, universal deadlines and globally bounded history are unverified. Do not infer those from low publication time or queue bounds. Same four technique sheets retain limited local evidence;39others remain locally unverified.


## Controller follow-up — 2026-11-11

[Coyote/buffer native results](../../prototypes/UnrealTechniqueLab/JUMP-RESULTS.md) add two specific CONTROLLER mechanisms (V29,V46),68policy checks,108actual PIE cases at observed30/60/144,3matched standalone performance pairs and native normal-speed media. A failed packaged30request/23.42observed is preserved; consumer/rate scopes stay distinct. No save/renderer/Present/framework optimization. Latest corpus coverage is5sheets with limited runtime evidence and38without a direct technique prototype. This does not certify all controller rules; V30corner correction and moving-platform behavior remain untested. Earlier four/39counts are historical.

## Vision follow-up — 2026-11-11

[Native distance/FOV/occlusion](../../prototypes/UnrealTechniqueLab/VISION-RESULTS.md) adds scoped TRACE/V18,V38 evidence:24geometry checks,132actual PIE case checks at observed30/60/144,3matched packaged query/frame comparisons, normal-speed original screenshots/video. Conditions are one known center point,3D cone, simple Visibility first-hit target, observer ignored. No patrol,pursuit,combat,AI framework or tool/renderer/save optimization. Latest coverage is6partially implemented sheets/37without direct local prototypes; earlier dated counts are historical. Broader perception and Lambert shading remain untested.

## Lock-on follow-up — 2026-11-11

[Native LOCKON selection/retention/switching](../../prototypes/UnrealTechniqueLab/LOCKON-RESULTS.md) adds scoped V53 evidence:37policy checks,198actual PIE cases at observed30/60/144,3matched packaged query/selection/full-frame observations and native1x media. Retrieve LOCKON for stable selected identity/score/entry-exit bands/explicit input/loss/replacement; TRACE for binary center-point visibility. Do not expand a visibility task into combat/movement AI or camera choreography. Latest coverage7partially implemented sheets/36without direct local technique prototypes; earlier dated counts are history. Physical input feel and broader targeting/AI remain untested.

# NPC 의사결정 방식을 고르고 화면 밖 상태 보존하기

K-GAME-NPC-SIMULATION · 방법 · 적용 중 · 근거 확인 2026-11-22

플레이어가 관찰해야 하는 동작을 정한 뒤 AI·충돌·애니메이션·렌더링·복제 갱신 수준을 각각 선택한다. 정밀도를 바꿀 때는 상태 쓰기 권한을 한 번만 넘긴다.

적용 범위 — 게임 NPC 행동, 조우 조정, 다중 관찰자를 포함한 시뮬레이션 정밀도.

## 적용 방법

감지→기억한 관찰(시각·만료)→판단→실행→결과를 추적한다. 단계가 명확하면 상태 기계에 진입·이탈·중단 규칙을 둔다. 우선순위가 있는 재사용 경로에는 행동 트리를 쓰고 실행 중·성공·실패 결과, 블랙보드 작성자, 중단 정리를 정한다. 효용 AI는 점수 단위, 동점 처리, 현재 행동을 유지할 기준이 있어야 잦은 전환을 막는다. GOAP·HTN은 계획 시간·탐색 노드·재계획 수를 제한하고 실제 실행 실패 시 대안을 둔다.

집단 제어가 공격 슬롯·스폰·좌석 같은 희소 자원을 소유한다. 내비게이션은 통과 가능한 경로를 찾고 지역 회피는 이웃에 대응하며 좁은 길은 진입·양보 규칙으로 조율한다. 후보 점수, 계획 실패, 슬롯 거부 이유를 남기면 플레이어가 본 행동을 설명할 수 있다.

위협, 목표 중요도, 최근 상호작용과 모든 관찰자를 고려해 전체 갱신·저빈도 갱신·요약 시뮬레이션·정지를 선택한다. 렌더링, AI, 충돌, 그림자, 소리, 애니메이션, 네트워크 관련성, 상주 여부를 독립적으로 조절한다. 승격·강등 문턱을 다르게 하거나 최소 체류 시간을 둔다. 이벤트·타이머 소유권은 한 번만 넘기고 밀린 일의 프레임당 처리량을 제한한다. 필요한 경우 고정 ID, 구역, 목표, 도착 예정 시각, 체력, 처치·퀘스트 상태를 유지한다.

## 적용 조건과 예외

화면 밖 추격자도 충돌하거나 소리를 내고 전투에 영향을 준다. 보이지 않는 문도 이동 경로를 막을 수 있다. 장식 군중은 밀도만 유지해도 되지만 이름 있는 동료는 개별 상태가 이어져야 한다. Mass LOD와 Unity CullingGroup은 이를 위한 정보와 수단을 제공하고, 보장할 결과는 게임이 정한다.

## 확인 방법

공격 중단, 소리 기억 만료, 길 차단, 같은 슬롯 경쟁을 시험한다. 전투 중 떠났다가 한참 후 돌아오고, 두 번째 관찰자만 남긴 경우도 반복한다. 전체·요약 실행을 비교해 퀘스트·처치 결과, 반응 지연, 유효한 복귀 위치, 중복 공격·스폰과 밀린 갱신에 의한 끊김을 확인한다.

## 근거

11월 22일 개발 관행 조사는 Halo 2, F.E.A.R., Left 4 Dead, S.T.A.L.K.E.R. 개발진 사례와 계획·시뮬레이션 연구, 엔진 문서를 살폈다. 팀마다 상태를 유지할 필요가 달랐다. 당시 로컬 AI·화면 밖 복귀 실험을 수행하지 않았다.

[군중 진입과 회피](K-GAME-TECH-CROWD.md) · [협동 조우 연출](K-GAME-COOP-DIRECTOR.md)

- [Halo 2 behavior design](https://www.gamedeveloper.com/programming/gdc-2005-proceeding-handling-complexity-in-the-i-halo-2-i-ai) · [Analysis of planning in games](https://cdn.aaai.org/ojs/12728/12728-52-16245-1-2-20201228.pdf) · [Unreal StateTree](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-state-tree-in-unreal-engine) · [Iovino et al. literature review](https://arxiv.org/abs/2005.05842) · [Unreal BT](https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---overview)
- [Unity Behavior graphs](https://docs.unity.cn/Packages/com.unity.behavior%401.0/manual/behavior-graph.html) · [Dave Mark and Kevin Dill, GDC 2010](https://media.gdcvault.com/gdc10/slides/MarkDill_ImprovingAIUtilityTheory.pdf) · [Orkin talk](https://gdcvault.com/play/1013459/Three-States-and-a-Plan) · [Valve talk video](https://www.gdcvault.com/play/1422/) · [Group control and encounter direction — Original presentation](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ReplayableCooperativeGameDesign_Left4Dead.pdf)
- [Recast and Detour source](https://github.com/recastnavigation/recastnavigation) · [ORCA paper and code](https://gamma-web.iacs.umd.edu/ORCA/) · [Unity AI Navigation](https://docs.unity.com/en-us/engine/6000.3/manual/packages-list/packages-all/pack-safe/com-unity-ai-navigation) · [Unreal AI Perception](https://dev.epicgames.com/documentation/en-us/unreal-engine/ai-perception-in-unreal-engine)
- [Carlson and Hodgins, 1997](https://graphicsinterface.org/proceedings/gi1997/gi1997-1/) · [Unreal Mass Gameplay](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-gameplay-in-unreal-engine) · [Chenney, GDC 2001](https://pages.cs.wisc.edu/~schenney/research/culling/chenney-gdc2001.pdf) · [Epic Significance Manager](https://dev.epicgames.com/documentation/unreal-engine/significance-manager-in-unreal-engine) · [S.T.A.L.K.E.R. developer interview](https://www.gamedeveloper.com/game-platforms/interview-inside-the-ai-of-i-s-t-a-l-k-e-r-i-)
- [O’Sullivan et al., 2002 — Paper](https://secom.ru.is/publications/CGF2002.pdf) · [Assassin’s Creed Unity — GDC session](https://www.gdcvault.com/play/1022411/massive-crowd-on-assassin-s) · [Assassin’s Creed Unity — Video](https://www.youtube.com/watch?v=Rz2cNWVLncI) · [Animation Budget Allocator](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-budget-allocator-in-unreal-engine) · [Unity CullingGroup](https://docs.unity.com/en-us/engine/6000.5/manual/cameras/occlusion-culling/culling-group-api/api)
- [AnimatorCullingMode](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/animatorcullingmode)

# 군중 의사결정·경로·렌더링을 나누어 확장

기준 K-GAME-TECH-CROWD · 활성 참고 지식 · 확인일 2026-11-08. Unity 셀 예약·동적 셀 장애물 실험은 실행했으며 Mass·ORCA 구현은 아니다.

## 지침

공간 분할로 이웃 검색을 줄이고 국소 회피로 가까운 충돌, 공유 경로로 장거리 이동을 처리한다. 행동 갱신·애니메이션·표현 비용은 별도 예산으로 관리한다. 먼 개체의 상세도를 낮춰도 중요한 사건/행위자를 보존한다. 구현 종합안은 원작의 정확한 코드 보증이 아니다.

### 원본 구현 추가 조사 — 2026-11-07

Fauerby의 2012 슬라이드는 2.5D 내비게이션의 규칙 셀 격자·점유/주석, 국소 조향/상태기계, 출구별 사전 계산 방향/비용장을 설명한다. 출구 채널을 바꿀 수 있고 좁은 곳에는 작성한 안내가 필요하다. 작은 풀에서 정식 NPC로 승격하며 자주 쓰는 데이터를 분리하고 셀 속성은 배열별로 나눈다. 과거 PS3 수치·개수는 현재 성능 보장이 아니다. 현대 ECS/Mass로 옮기는 것은 새 구현이며 Mass도 버전·플랫폼 조건을 확인한다.

### 로컬 군중 실험 — 2026-11-08

[DynamicLab](../../prototypes/TechniqueLab/DYNAMIC-RESULTS.kr.md)은 공유 거리장·현재/목적 칸 예약·양보를 결합했다. 단일 권한이 그래프·예약·물리 상태를 소유한다. 폐쇄 요청은 새 경로를 바로 막고 재계산하며 이미 통과 중인 개체가 나간 뒤 물리적으로 닫는다. 열기·상자 칸 변경은 ID/위치 초기화 없이 갱신한다. 일시정지 제어의 네이티브 콜라이더와 실제 Windows UI도 검사했다.

반경0.20·속도3의 같은 원판이 상하좌우 격자에서 한 출구 영역으로 이동한다. 안전 시험 최소 간격은 0.999908단위로 보수적인 셀 간격이며 물리적 밀착/밀기 군중이 아니다. 64/256개는 31.27/101.47 시뮬레이션 초에 모두 도착했다. 매 틱 기하 감사·화면 프레임별 네이티브 장애물 검사를 했고 회피 없음 비교군에서는 겹침을 감지했다. PlayMode·독립 실행3회 각각 회귀12개·시나리오6개를 통과했다. 동작 재생은 프레임당8틱 가속이며 성능은 별도 실시간60Hz다.

양보·폐쇄 지연을 허용하는 단일 목표 격자에 적합하다. 교행·일반 기아 방지·가변 반경·연속 이동 장애물·속도 공간 솔버는 검증하지 않았다. [ORCA 원저 자료](https://gamma-web.iacs.umd.edu/ORCA/)의 상호 속도 제약/최적화 조건을 이 셀 예약에 가져오지 않는다. ORCA·Mass·Hitman 원본 구현을 재현한 것은 아니다.

512개에서 제어/동기화 p95는 0.130–0.144ms지만 전체 p95는 2.87–3.15ms였다. 최종 모든 조합은 세 실행의 짧은 구간에서 16.67ms p95를 충족했지만 이전 측정에는 미달이 있었고 부하는 통제하지 않았다. GPU 누락을 0비용으로 계산하지 않으며 GPU 꼬리 성능은 미검증이다. 실제 전체 프레임과 장면을 확인하는 조건부 채택이며 개수·거리 조회 미세 측정만으로 판단하지 않는다. 빠른 위험 비교군은 안전한 대체가 아니다.

## 적용 조건과 예외

과거 원작의 셀·출구·승격 구조는 확인했으나 과거 하드웨어의 비용은 전이하지 않는다. 로컬 실험은 같은 원판·한 권한·상하좌우·한 출구 영역·정지/양보·폐쇄 지연 조건이다. 상용 애니메이션·LOD·임의 강체 상호작용은 미검증이다.

## 검사

병목·좁은 출구·정지 군중·LOD 전환을 프로파일하고 겹침·정체를 기록한다. 이번 실행은 문 내부 폐쇄·모든 경로 차단/재개·셀 장애물 변경·합류·위험 비교군·반복 상자·일시정지 네이티브 동기화·도착 구간 감사 검출까지다. 실제 프로젝트의 입력·권한·형상·행동·표현·전체 프레임으로 재검사한다.

## 근거

- [Epic Mass Avoidance](https://dev.epicgames.com/documentation/unreal-engine/mass-avoidance-overview-in-unreal-engine?lang=en-US): 공식 공간 해시·국소 회피·디버깅, Experimental 표시. 2026-11-07 확인.
- [Crowds in Hitman 세션](https://www.gdcvault.com/play/1015315/Crowds-in-Hitman): 초기는 개요만 확인. 이후 [원본 슬라이드](https://media.gdcvault.com/gdc2012/slides/Programming%20Track/Fauerby_Kasper_CrowdsInHitman.pdf)의 pp.7–15·18–20·28·32–36을 확인했다. 전체 발표·벤치마크 재현은 아니다. 2026-11-07 확인. [V01 대응](K-GAME-TECH-GUIDE.kr.md).
- [로컬 전체 결과](../../prototypes/TechniqueLab/DYNAMIC-RESULTS.kr.md), [월드](../../prototypes/TechniqueLab/Assets/TechniqueLab/CrowdWorld.cs), [검사](../../prototypes/TechniqueLab/Assets/TechniqueLab/CrowdChecks.cs), [최종 실행](../../prototypes/TechniqueLab/Results/Dynamic/dynamic-run-1.json.gz), [원본 분석](../../prototypes/TechniqueLab/Results/Dynamic/summary.json).
- [ORCA 원저](https://gamma-web.iacs.umd.edu/ORCA/)는 원리 대조에 사용했으며 로컬 구현은 아니다. [Unity Frame Timing Manager](https://docs.unity.com/en-us/engine/6000.0/manual/analysis/graphics-performance-profiling/profile-rendering/frame-timing-manager/manager)의 지연·GPU 누락 가능성을 확인했다. 두 자료는 2026-11-08 확인.

## 양방향·서로 다른 반경 확장 — 2026-11-08

[TrafficLab](../../prototypes/TechniqueLab/TRAFFIC-RESULTS.kr.md)은 반경 .20/.35/.60별 양쪽 출구 장·작성한 상하좌우 차선·방향 임대 제어를 추가했다. 거친 네 노드 비용은 통로 선호도이며 실제 최단 거리가 아니다. 여유 .04로 큰 개체의 좁은 통로를 거부하고 반경 합으로 쓸린 이동·독립 감사를 수행했다. 이전 DynamicLab의 한 목표/동일 반경 제한은 그 과거 장면에 해당한다.

PlayMode·release3회 각각 회귀21개·기대11개(안전9개·정책을 끈 비교2개)를 통과했다. 혼합64/128/256개 양쪽 모두 도착했고256개는114.7500시뮬레이션 초였다. 최소 안전 표면 간격0.0476715단위, 벽/쌍 침투·순간이동·임대 오류·전역 교착 없음. 역순·90틱 지연·넓은 동시 교행·진입 중단/배출/재개·도착 선분을 검사했다. 진입 제어만 끄면 충돌 없이 교착, 방어도 끄면 겹침이 생겼다. 충돌 안전과 진전은 다른 조건이다.

혼합256개 전체 프레임 p95 8.08–8.32ms, 틱 포함 제어/동기화 p95 0.404–0.444ms. 18개 실행/조합 구간 모두16.67ms p95목표를 충족했다. 실제 창·활성/표시 수·전체 분포·드문 초과·GPU 누락을 보존했다. 부하 미통제로 반경 모드의 인과 성능 차이는 판단하지 않는다. 임대 중단은 물리적 문 폐쇄가 아니며 이전 동적 장애물 실험과 별개다.

대기 공간·차선·한 이동 권한·고정 원판·정지/교대를 허용할 때 조건부 채택한다. 방향별 FIFO이며 방향 사이 전역 FIFO는 아니다. 무한 유입 공정성·임의 내비메시·곡선·가속·밀기·실시간 반경 변경·분산 권한은 미검증이다. 공간 해시는 반경≤.60·속도3·dt≤1/30에 의존한다. 원저 [통로 대칭](https://mapf.info/index.php/Main.SKoen20k)·[C-space](https://lavalle.pl/planning/node161.html)·[고정 경로 협조](https://lavalle.pl/planning/node325.html)는2026-11-08확인한 설계 참고이며 CBS/완전 플래너를 구현한 것은 아니다. [최종 검사](../../prototypes/TechniqueLab/Results/Traffic/editor-final.json)·[전체 분포](../../prototypes/TechniqueLab/Results/Traffic/summary.json).

## 무차선·지속 유입·개별 진전 확장 — 2026-11-08

[StreamLab 결과](../../prototypes/TechniqueLab/STREAM-RESULTS.kr.md)는 무방향 상하좌우 지형에서 각 요청의 경로를 계산하고 반경별 쓸린 시간 예약·불변 완전 경로·외부 FIFO 진입을 결합했다. 차선 태그나 미리 정한 경유점은 없다. 생성 전 대기도 ID별 응답에 포함한다. 일반7개는 무충돌 배출·240초 응답을 통과했지만 과부하480개 중61ID는 이를 초과했고 최대280.0초였다. 최신 우선은 다른538개 도착 중 요청0을310초 미생성 상태로 남겼다. 전체 처리량으로 특정 개체의 기아를 판단하면 안 된다.

FIFO 머리가 막히면 젊은 진입을 막고 기존 유한 경로가 빠진 뒤 정적 경로를 찾는 조건부 논증이다. 유한 실행이 무한 시간의 증명은 아니며 과부하에서는 일정한 지연 상한을 주지 않는다. 생성 통제·정적 지형·고정 반경·계획대로 이동·도착 후 제거가 필요하다. 기존 임의 개체·점유 입구 강제 생성·갑작스런 정지·동적 벽/반경·가속·분산 권한은 범위 밖이다.

병목 초당8요청 전체 프레임 p953.52–6.10ms, 탐색 다음 전체 프레임 p9520.23–20.52ms. 실제 활성/표시 인원·대기열·온라인 탐색/생성/소멸·프레임 초과·GPU 누락을 기록했다. 목표 수요와 고정 개체 수를 혼동하지 않는다. [PlayMode23검사/10기대](../../prototypes/TechniqueLab/Results/Stream/editor-final.json)·[분포](../../prototypes/TechniqueLab/Results/Stream/summary.json). 원저 [RHCR](https://arxiv.org/abs/2005.07371)·[PIBT](https://arxiv.org/abs/1901.11282)·[온라인 작업](https://arxiv.org/abs/1705.10868)은2026-11-08초록만 확인했으며 그 알고리즘/정리를 구현한 것은 아니다.

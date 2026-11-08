# 양방향·혼합 반경 TrafficLab 결과 — 2026-11-08

## 결과와 채택 판단

최종 Unity PlayMode와 순차 Windows release 3회에서 각각 **회귀 검사 21개·시나리오 기대 11개**를 통과했다. 안전 상황 9개와 의도적으로 정책을 끈 비교군 2개다. 반경 .20/.35/.60의 256개까지 양쪽 모두 도착했고 쌍 충돌·벽 침투·순간이동·잘못된 임대·금지된 좁은 통로 사용·전역 교착은 검출되지 않았다. 안전 상황의 최소 표면 간격은 0.0476715단위다. 중심 간 거리가 아니다. 작성한 차선·반경 프로필·중앙 진입 제어를 허용하는 게임에서 조건부로 활용한다.

18개 실행/조합 구간 모두 16.67ms p95 목표를 충족했다. 혼합 256개 전체 프레임 p95는 **8.08–8.32ms**, 틱 포함 제어/Transform 동기화 p95는 **0.404–0.444ms**였다. 한 PC의 짧은 3회 측정이며 부하는 통제하지 않았다. 반경 혼합이 빠르거나 느리다는 인과·상용 성능 보장은 아니다. [전체 분포](Results/Traffic/summary.json).

## 실제 구현

기존 [DynamicLab](DYNAMIC-RESULTS.kr.md)과 별도인 TrafficLab.unity/TrafficBuild를 만들었고 원래·동적 C#을 보존했다. [설계](TRAFFIC.kr.md), [월드](Assets/TechniqueLab/TrafficWorld.cs), [기하/진입 제어](Assets/TechniqueLab/TrafficGeometry.cs), [독립 감사](Assets/TechniqueLab/TrafficAudit.cs), [검사](Assets/TechniqueLab/TrafficChecks.cs), [네이티브 표시](Assets/TechniqueLab/TrafficView.cs), [실행기](Assets/TechniqueLab/TrafficRunner.cs).

128×40 정적 월드에 폭1의 좁은 구멍과 중심 간격2인 넓은 차선4개가 있다. 반경마다 양쪽 출구용 역방향 장을 만든다. 네 노드의 허브/통로 그래프 비용1/2는 좁은/넓은 통로 선호도이며 실제 기하 최단 거리가 아니다. 선택 뒤 작성한 상하좌우 경유점을 속도3, 고정1/60초로 이동한다. 반경은 생성 시 고정하며 여유 .04를 포함해 좁은 통로에 .46은 허용, .47은 거부, .60은 넓은 곳으로 돌린다. 다른 체격에 부적합한 장을 공유하지 않는다.

좁은 통로는 방향별 FIFO 대기표·방향 독점 임대·전신 이탈 후 반환을 사용한다. 반대편 대기 중에는 한 단계의 같은 방향 신규 진입을4개로 제한하고 기존 개체가 모두 나간 후 교대한다. 방향 간 전역 FIFO는 아니다. 입구 대기 줄과 출구 동선을 분리한다. 이동 제안은 각 반경의 합으로 선분 간 최단 거리를 검사하고 위험하면 양보한다. 공간 해시 폭2와 인접 칸 검사는 반경≤.60·속도3·dt≤1/30 조건에 의존한다. 64개240틱에서 모든 이웃 검사 방식과 궤적이 같았다. 공개 반경 직접 변경·임의 dt·속도 변경은 보장 범위 밖이다.

독립 감사는 매 틱 double 기반 반경 합·이동 중 거리·벽 거리를 계산하고 도착 마지막 선분도 검사한다. 이동기의 쌍 거리 함수를 호출하지 않는다. 표시 프레임마다 실제 반경으로 Unity 벽 Sphere 겹침도 검사한다. 개체는 반경에 맞춰 키운 원기둥이며 애니메이션·물리적 밀기는 없다. 측정 중 활성/보이는 개체 수가 동일함을 기록했다.

## 동작 결과

| 상황 | 동/서 도착 | 시뮬레이션 초 | 넓은 통로 동시 교행 틱 |
| --- | --- | --- | --- |
| narrow-headon | 1 / 1 | 28.6500 | 0 |
| wide-opposing | 1 / 1 | 21.5167 | 88 |
| large-redirect | 1 / 1 | 23.5167 | 0 |
| mixed-64 | 32 / 32 | 42.7333 | 370 |
| mixed-128 | 64 / 64 | 66.6833 | 670 |
| mixed-256 | 128 / 128 | 114.7500 | 1270 |
| reverse-128 | 64 / 64 | 66.6833 | 670 |
| late-west-64 | 32 / 32 | 42.7333 | 370 |
| admission-pause | 32 / 32 | 44.3500 | 370 |

밀집 상황은 동/서 인원을 반씩, 좁은 통로1/4·넓은 통로3/4로 나누며 세 반경을 모두 사용했다. 역순은 실제 첫 진입 방향이 서쪽이고 지연 상황은 동쪽 첫 요청1틱·서쪽90틱이다. 반대 대기 시 신규 진입은 최대4개였다. 진입 중단은 새 허가를 막고 기존 임대가 빠져나가며 대기표·위치를 보존한다. 재개 후 모두 도착했다. 물리적인 새 문 폐쇄 시험은 아니며 이전 DynamicLab의 문 실험은 별도로 남겼다.

진입 제어만 끈 비교군은 충돌 없이도 0/2 도착·5초 전역 정지를 보였다. 충돌 방어까지 끈 비교군은 이동 중 겹침을 검출했다. 충돌 안전만으로 진전을 보장하지 않는다. 안전 상황의 최대 연속 개별 정지는 의도적 진입 중단 포함12.3333초, 혼합256개는10.9667초였다. 개별 대기는 허용하며 전역 정지 검사가 개별 대기 상한·무한 유입의 공정성을 증명하지 않는다. 완주 한도는 쌍120초,64/128개180초,256개300초다. 동작은 화면당8틱의 가속 시뮬레이션이며 아래 실시간 성능과 구분한다.

실패→통과 원본: [초기 커널](Results/Traffic/red-contracts.json), [통과](Results/Traffic/green-contracts.json), [월드 실패](Results/Traffic/red-world.json), [수정](Results/Traffic/green-world.json), [독립 감사 변조 검출](Results/Traffic/red-audit-sensitivity.json), [최종 PlayMode](Results/Traffic/editor-final.json). 여유·반경 합·쓸린 선분·교대·중단, 대기 시간 이중 합산, Dense(8) 슬롯 누락, 실제 대기표 역순을 보완했다. 감사를 고정 지름으로 바꾸고 도착 구간을 건너뛰자 두 직접 검사가 실패했으며 최종 빌드 전에 복구했다. 독립 코드 검토의 역순/지연/감사 회귀 보강도 반영했다.

## 전체 프레임

Unity6000.0.77f1·Windows x64 Mono release·i7-12700KF·RTX3080·Windows11·D3D11·1280×720·MSAA2·vSync0. 실제 창을 보이게 실행했다. 비교 순서는 혼합/균일,균일/혼합,혼합/균일이다. 균일 반경은 모두.35이며 초기 중심·통로·카메라·표현·속도는 같다. 초기화·반경별 장 생성·독립 감사·캡처·파일 저장은 측정 밖이고 실제 이동 충돌 방어·진입 제어·네이티브 동기화는 포함한다. 이 측정은 TrafficLab의 위상 재계산을 포함하지 않는다.

1초 준비 후6초를 기록했다. 60Hz 실시간 누적기에서 프레임당 최대8틱을 처리하고 미처리 시간을 버리지 않는다. 이 짧은 구간에는 도착·재생성이 없고 모든 개체가 활성·표시 상태다. 전체 벽시계 프레임·제어·CPU/main/render/present/GPU·GC를 보존했다. 측정1.5초에 진입 중단,3초에 재개한다. 이벤트의 제어 비용과 그 **다음** 벽시계 프레임을 연결한다.

| 활성 개체 | 반경 | 전체 프레임 p95 ms | 틱 포함 제어/동기화 p95 ms | 최악 프레임 ms | 16.67ms 초과율 % (1/2/3회) |
| --- | --- | --- | --- | --- | --- |
| 64 | 균일 .35 | 2.89–4.21 | 0.132–0.140 | 10.82 | 0.000 / 0.000 / 0.000 |
| 64 | 혼합 .20/.35/.60 | 2.80–3.53 | 0.135–0.140 | 9.91 | 0.000 / 0.000 / 0.000 |
| 128 | 균일 .35 | 3.57–3.89 | 0.253–0.271 | 10.54 | 0.000 / 0.000 / 0.000 |
| 128 | 혼합 .20/.35/.60 | 3.59–7.62 | 0.250–0.272 | 10.05 | 0.000 / 0.000 / 0.000 |
| 256 | 균일 .35 | 8.13–8.28 | 0.402–0.485 | 10.16 | 0.000 / 0.000 / 0.000 |
| 256 | 혼합 .20/.35/.60 | 8.08–8.32 | 0.404–0.444 | 10.53 | 0.000 / 0.000 / 0.000 |

범위는 실행별 백분위 최솟값/최댓값이며 합친 신뢰구간이 아니다. 전체 131,052프레임 중16.67ms 초과0개, 최악10.817ms다. 드문 초과도 지우거나 0으로 반올림하지 않는다. 무제한 렌더링은 틱 없는 프레임이 많아 표의 제어 열은 틱 포함 집합이다. 전체 제어 분포·틱 다음 전체 프레임·p99/max·적체·GC·이벤트는 summary에 있다. 작은 제어 타이머가 전체 예산은 아니다.

Unity 엔진 시간은 비동기이며 타임스탬프로 중복을 제거했다. 벽시계 행과 일대일 대응하지 않는다. 엔진131,052관측 중 GPU23,429개가 누락됐다. 0은 누락이며 유효 값만의 통계로 GPU 꼬리 지연을 보장하지 않는다. CPU+GPU를 합하지 않는다. [Unity 공식 문서](https://docs.unity.com/en-us/engine/6000.0/manual/analysis/graphics-performance-profiling/profile-rendering/frame-timing-manager/manager)의 지연·자료 부재 조건을 따른다. [빌드](Results/Traffic/build.json)는 오류0이며 소스·관리 어셈블리 해시/GUID를3회와 대조했다.

## 실제 창·재현

Computer Use로 정지→정지 중64개 재시작→진입 중단→이동 재개→진입 재개→종료를 확인했다. 다른 크기와 양방향 색이 보였고 넓은 차선은 이동하며 좁은 곳은 기다렸다가 허가 후 재개했다. 이후 양쪽24개씩 도착·좁은 개체16개 활성·임대3개·교대1회를 관찰했다. 정성 UI 확인과 자동 감사·완주는 구분한다. [관찰](Results/Traffic/ui-observation.json)·[정상 종료](Results/Traffic/traffic-ui-process.json). 카메라 PNG는 OnGUI 없는 월드만 담는다. [혼합256 이동](Results/Traffic/traffic-run-3-mixed-256-active.png), [넓은 동시 교행](Results/Traffic/traffic-run-3-wide-opposing-active.png), [성능 장면](Results/Traffic/traffic-run-3-agents-256-mixed.png).

실험실 폴더에서 Run-Editor.ps1의 TrafficBatch.Checks,TrafficBatch.Play(-Graphics),TrafficBatch.Build 순으로 실행한다. Run-Traffic.ps1의 -Interactive로 제어하고 측정은 -Visible과 -Session traffic-run-1/2/3, -Order0/1/0으로 순차 실행한다. 정확한 명령은 [영문 기준](TRAFFIC-RESULTS.md)에 있다. Batch PlayMode는 연속 Game view 렌더링이 없어 성능을 생략한다. [analyze_traffic.py](analyze_traffic.py)는21검사·11기대·메타데이터·인원/표시·프레임 연속성·이벤트·엔진 자료·해시·실행 순서를 검증한다.

원본 [1회](Results/Traffic/traffic-run-1.json.gz)·[2회](Results/Traffic/traffic-run-2.json.gz)·[3회](Results/Traffic/traffic-run-3.json.gz), [무손실 압축 명세](Results/Traffic/compression.json). 해제 바이트 수·SHA-256이 원본과 같으며 분석기는 JSON/gzip 모두 지원한다. 프로세스 신원은 해당 traffic-run-N-process.json에 있다.

## 활용 연결·남은 조건

문제→[PATH](../../knowledge/game/K-GAME-TECH-PATH.kr.md)의 목표/반경 호환 장+[CROWD](../../knowledge/game/K-GAME-TECH-CROWD.kr.md)의 이웃 검사·협조→차선/임대 조건부 채택→체격별 통로·쓸린 이동 검사·교대 구현→안전9개·민감도 비교2개→실측과 한계를 지식에 반영했다. 순수 공유 장은 교행 진전을 해결하지 않으며 거리 조회의 작은 비용으로 렌더링 예산을 판단하지 않는다. 기존 동일 반경/한 출구 결과는 이전 장면의 범위로 유지한다.

신규 검색3개 중 처음 한국어2개는 결과가 없었다. 기존 항목에 검증한 교행/반경/통로 조건과 검색어를 추가한 뒤3/3을 통과했고 기존57개도 통과해 **60/60**이다. [전](Results/Traffic/retrieval-before.json)·[후](Results/Traffic/retrieval-traffic.json)·[목록69개 엄격 검사](Results/Traffic/catalog-check.json)·[문서/압축/짝 검사](Results/Traffic/document-checks.json)·[독립 검토](Results/Traffic/review.json). 사람용 번역은 읽지 않고 작성 원본에서 갱신했다. 선언한 질문의 검색성을 확인한 것이며 미지의 상황의 자율 판단 증명은 아니다. 누적 엔진 근거는 제한된4개 항목이며39개는 여전히 미검증이다.

작성한 차선·대기 공간·중앙 권한·고정 원판·대기/교대를 허용하고 대상 게임의 안전·완주·전체 예산을 확인할 때 채택한다. 임의 내비메시·곡선·가속·물리적 밀기·실시간 반경 변경·무한 유입·분산/네트워크·예고 없는 이동 장애물은 새 설계/검사가 필요하다. 보편적인 무충돌/교착 해법으로 확대하지 않는다.

2026-11-08 원저 조사: [Li 등 ICAPS2020](https://mapf.info/index.php/Main.SKoen20k)의 통로 대칭은 협조 필요성 참고이며 CBS를 구현한 것은 아니다. [LaValle C-space](https://lavalle.pl/planning/node156.html)·[평행이동/Minkowski](https://lavalle.pl/planning/node161.html)는 반경 여유 참고이며 AABB 팽창은 원판 모서리의 보수적 근사다. [고정 경로 협조](https://lavalle.pl/planning/node325.html)는 경로와 스케줄 분리 참고다. 이 임대 제어는 자체 구현이며 원저의 완전성 보장을 가져오지 않는다.

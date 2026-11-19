# 대표 부하에서 최적화의 효과 측정하기

항목 `K-CODE-PERFORMANCE-MEASUREMENT` · 상태 활성 · 확인일 2026-11-11

검색어 profiling,benchmark,latency,throughput,goodput,tail latency,p95,frame pacing,fixed timestep,token bucket,FIFO,backpressure,Unreal Insights,Timing Insights,occlusion query,Render Hardware Interface,Present,binary heap,snapshot lifetime,working set,private commit,benchmark::DoNotOptimize,성능,프로파일링,프레임 시간,비동기 저장

## 지침

먼저 사용자가 수행하는 작업, 같은 부하에서 유지할 동작, 허용 시간을 정한다. 개별 요청 지연, 단위시간당 처리량, 할당률, 남아 있는 메모리와 프로세스 최고 사용량을 나누어 본다. 벤치마크 실행 중 병목을 확인한다. 작은 벤치마크에서 결과를 소비하고 필요하면 생성된 코드를 본다. `benchmark::DoNotOptimize`를 써도 인수 표현식 자체는 최적화될 수 있다.

**프레임 시간.** Unreal Insights의 Timing Insights에서 전체 프레임을 선택하고 게임·렌더·RHI(Render Hardware Interface) 스레드 및 수집된 GPU 트랙을 확인한다. 콜백 소요 시간은 콜백 범위만, 연속 시작점 간격은 콜백 사이의 비용까지 포함한다. 작업이 발생한 프레임과 다음 시작점 간격을 연결하고 시작, 워밍업, 정상 상태, 계측 비용, 마지막 저장과 종료 경계를 남긴다. 중첩·동시 구간은 잘라 합집합으로 계산한다. `Present` 대기는 해당 CPU 스레드가 막힌 위치를 알려 준다. GPU, 디스플레이 동기화, 드라이버 원인은 별도 증거가 필요하다. 오클루전 쿼리를 끄는 비교는 같은 장면에서 수행하고 가시성과 GPU 비용도 확인한다.

**같은 작업량.** 같은 실행 파일, 뷰포트, 렌더 설정, 데이터와 입력 일정으로 기준과 변경 실험을 번갈아 실행한다. 조건별 프레임 수, 백분위수, 최댓값과 마감 초과 횟수를 보존한다. p95가 예산 안이어도 개별 프레임은 마감에 늦을 수 있다. 고정 스텝 h에 대해 매 행의 새 잔여 시간 = 이전 잔여 시간 + 실제 경과 − 스텝 수 × h를 확인하고, 버린 시간이 있으면 별도 차감한다. 도착 기록과 큐 깊이, 가장 오래 기다린 요청, 각 소비자의 생존 구간을 대조한다. 토큰 버킷은 모은 크레디트만큼 순간 처리를 허용하며 장기 입장률을 제한한다. FIFO는 자격이 있는 오래된 항목을 먼저 처리한다. 같은 제공 부하에서 승인된 요청의 지연과 함께 거절 수, 단위시간당 기한 내 완료한 원래 요청 수(goodput)를 보고한다. 생성 시점부터 재면 입장 대기 시간이 빠진다.

**알고리즘과 저장.** 이진 힙의 우선순위 키를 미리 패킹하면 비교 연산이 줄 수 있다. 비트 범위와 동점 순서, 요청별 경로와 확장 수를 확인하고 플래너당 추가 메모리를 잰다. 짧은 호출은 상세 계측 자체의 영향을 받으므로 거친 추적과 추적 없는 측정을 반복한다. 저장은 스냅샷 생성, 직렬화, 쓰기, 정리, 제출 후 확인, 프로세스 시작부터 종료까지를 나누어 잰다. 원본을 바꾸거나 폐기한 뒤에도 전체 출력과 소유권을 비교한다. 역압(backpressure)은 작성기가 밀릴 때 수락할 입력을 제한한다. 실행 중인 입력과 대기 입력을 모두 계상하고 생산자, 인코딩 버퍼, 축적한 이력은 별도로 잰다. Windows의 private commit은 프로세스 전용 커밋 메모리, working set은 현재 메모리에 상주하는 페이지다. 주기적인 샘플 사이의 정점은 놓칠 수 있다.

## 적용 범위와 예외

입력과 결과 및 추적 경계가 비교 가능할 때 적용한다. 합성 장면, 정적 경로 그래프, 고정 카메라, 가속 캡처, Debug 또는 에디터 측정으로 패키징 게임의 마감을 보장할 수 없다. 큐 밖의 메모리, 용량, 지연, 공정성, 동적 지형, 실시간 자동 저장과 드라이버 원인은 대상 작업에서 각각 검증한다.

## 점검

- 기준과 후보 순서를 바꾸어 반복한다. 조건별 표본 수, 모든 마감 초과와 콜백 밖의 구간을 보존한다. 원래 요청 ID와 같은 시뮬레이션 시점으로 누락·재정렬을 확인한다.
- 샘플 삭제, 중간 카운터 변조, 다른 실행 파일, 출력의 값·순서 변경을 검증기가 잡는지 본다. 실제 실행한 산출물과 빌드 식별자를 대조한다.
- 비동기 저장은 게임 스레드의 제출과 결과 수신, 워커, 비우기, 종료를 나누어 측정한다. 큐 가득 참, 쓰기 실패, 수락된 작업을 남긴 종료를 시험한다. 파일 닫기와 이름 변경만으로 충돌 후 내구성을 보장할 수 없다.

## 근거

방법론 조사는 2026-11-07에 수행했다. 2026-11-09~11에 기록한 UE 5.8.3 Windows/D3D11 비교에서는 p95가 통과해도 발생하는 마감 초과, 플래너 외부의 렌더 대기, 캡처 비용과 최종 저장 비용의 차이를 관찰했다. 저장 비교 대상은 이미 종료된 시뮬레이션이었다. 아래 등록 ID는 과거 관찰을 가리킨다. 이번 검토에서는 Epic의 프로파일러 설명을 확인했으며 해당 실험을 재실행하지 않았다.

- [Brendan Gregg, Performance Analysis Methodology](https://www.brendangregg.com/methodology.html) · [Active Benchmarking](https://www.brendangregg.com/activebenchmarking.html)
- [Google Benchmark User Guide](https://google.github.io/benchmark/user_guide.html) · [Epic, Timing Insights](https://dev.epicgames.com/documentation/unreal-engine/timing-insights-in-unreal-engine?application_version=5.8)
- [Frame and world checks](../sources.md#src-ue-lab-editor-gate-results-md) · [Variable frame workloads](../sources.md#src-ue-lab-dynamic-results-md) · [Per-consumer checks](../sources.md#src-ue-lab-traffic-results-md)
- [Sustained load](../sources.md#src-ue-lab-stream-results-md) · [Admission](../sources.md#src-ue-lab-admission-results-md) · [Frame attribution](../sources.md#src-ue-lab-hitch-results-md) · [Planner comparison](../sources.md#src-ue-lab-planner-results-md)
- [Snapshot ownership](../sources.md#src-ue-lab-snapshot-results-md) · [Asynchronous publication](../sources.md#src-ue-lab-async-save-results-md)

## 풀링과 캐싱의 비용

객체 풀링(메모리 풀링)은 할당된 저장 공간이나 인스턴스를 다시 쓴다. 같은 활성 개체 수에서 생성·초기화 비용, 할당률, 보유 용량, 캐시 지역성과 긴 프레임을 비교한다. 풀 워밍업·반납·재획득을 포함한다. 할당 횟수가 줄어도 상태가 남거나 메모리가 더 오래 유지될 수 있다. 캐싱·배치·동시 처리에도 무효화·지연·경합 비용이 있으므로 변경 뒤 전체 작업을 다시 측정한다.

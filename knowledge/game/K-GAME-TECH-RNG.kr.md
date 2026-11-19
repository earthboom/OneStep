# 의사난수·시드·스트림

기준 항목: K-GAME-TECH-RNG · 확인일: 2026-11-07 · 참고 지식. 엔진 실행·성능·실제 플레이 검증은 별도다.

## 원리와 구현 요점

결정론적 의사난수기는 내부 상태에서 재현 가능한 수열을 만든다. 리플레이·생성·전리품의 상태를 저장하거나 독립 스트림을 쓰고 장식용 난수 소비가 게임 결과를 바꾸지 않게 한다. 주기·통계 품질·속도·재현 요구로 생성기를 고른다.

### 추가 조사로 보완한 구현

pret의 에메랄드 재구성에서 Random은 32비트 상태를 곱셈·덧셈으로 갱신하고 상위 16비트를 반환하며 SeedRng는 상태를 지정한다. 헤더의 점화식은 s'=(1103515245*s+24691) mod 2^32이다. 재현 조건은 같은 시드와 같은 호출 횟수·순서이며 단순히 실제 경과 시간만 같다고 충분하지 않다. 버전별 난수 문제를 진단할 때 초기화와 모든 호출자를 먼저 추적한다. 새 게임은 게임플레이와 장식용 스트림을 분리한다.

## 적용 조건과 한계

예측 가능성은 구현에 달려 있고 현대 게임이 모두 난수 조작을 막는 것은 아니다. 일반 목적 PCG를 비밀성이 필요한 암호학적 난수기 대신 쓰지 않는다.

## 적용 전 점검

적용 전 점검: 상태 복원·장식 활동 변경·분포 검사를 수행하고 실제 사용에서 스트림 분리가 유지되는지 확인한다.

## 근거

로컬 시험의 원시 측정과 매체는 해당 실험 기록에 보관돼 있다.

- [Melissa O'Neill — PCG Random Number Generators](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf)
- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

### 추가 조사 출처

- [pret/pokeemerald — random.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/random.c) — Random and SeedRng inspected; community reconstruction, not a vendor patch history.
- [pret/pokeemerald — random.h](https://github.com/pret/pokeemerald/blob/master/include/random.h) — ISO_RANDOMIZE1 and declarations inspected; formula transcribed, no game build.

추가 조사 출처의 영문 주석은 정확한 절·함수·접근 범위를 보존한다. 원본 슬라이드·문서·공개 코드의 확인과 실제 엔진·하드웨어 실행은 구분한다. 영상 설명·세션 개요만 확인한 자료를 전체 발표 확인으로 간주하지 않는다.

출발 영상: V55. [영상별 대응표](K-GAME-TECH-GUIDE.kr.md).

### linear congruential generator

**선형 합동 생성기(LCG)**는 상태에 곱셈·덧셈을 한 뒤 모듈러 연산으로 다음 상태를 만든다. PCG(Permuted Congruential Generator) 계열은 합동 상태 생성기에 출력 변환을 적용한다. 재현 가능한 게임 시뮬레이션이라면 같은 알고리즘과 스트림 매개변수에서 전체 추출 순서를 비교한다. 시각 효과용 스트림을 분리했다면 장식 효과가 난수를 더 써도 게임 판정 난수는 바뀌지 않아야 한다. [O'Neill — The PCG Paper](https://www.pcg-random.org/paper.html)

## 실제 언리얼 검증

명시적 시드와 상태를 가진 PRNG는 같은 호출순서에서 같은 값을 재생한다. 게임·장식 스트림을 용도별로 소유하고 메모리복원은 전체상태와 게임진행을 포함한다. 시드·생성기·호출순서가 달라지면 결과도 달라진다.

### 지침

기존 pret Emerald 재구성은32비트 곱셈·덧셈 후 상위16비트를 반환하며 s'=(1103515245s+24691)mod2^32이다. SeedRng는 상태를 설정한다. 같은 경과시간만으로 같은 난수는 보장되지 않는다. 원작의 정확한 버전·패치 이력은 확인하지 않았다.

### 적용과 예외

예측 가능성은 구현에 달려 있다. PCG 같은 범용 난수는 암호학적 비밀을 대신하지 않는다. 서로 다른 시드의 스트림 소유 분리는 통계적 독립 증명이 아니다.

### 확인

UE5.8.3 실제PIE·패키지에서 각8상황,정책57·근거38검사,공유/분리 각3비용·정상영상으로 보완했다. 게임시드12345·장식67890을 사용하며 게임결과는 상위8비트다. 분리 방식은 장식호출량·프레임처리묶음·리셋·메모리복원을 바꿔도48게임이벤트의 값·순서·점수가 유지된다. 공유는 장식호출 증가에 결과가 달라지는 대조군이다.

전체값 복사는 초기·현재시드/두스트림/호출수/이벤트커서/점수/누적값을 보존한다. 현재시드만 Initialize하면 Reset의 원래시드가 달라진다. 정수포함범위 폭1..2^23은 int64로 검사하며 역전·초과는 무소비 거부,단일값도 한 번 소비한다. 실수[0,1) 양끝·음수/int32극단시드를 확인했다. 낮은 비트 나머지연산은 피한다.

매 실행512준비+4096측정틱,매틱 게임/장식65536회씩,정확히536,870,912측정호출이다. 난수구간/전체프레임/시작간격/지연전체GPU를 구분한다. 전체프레임은HUD·관찰을 포함하고최종저장·캡처는 제외한다. 빠른 전체프레임을 가정하지 말고 결과격리를 위해 선택한다. 같은순서의 게임호출을 전제로 하며 임의 재정렬·게임물리 전체·통계품질·버전간동일성·멀티스레드를 보장하지 않는다.

### 근거

- 과거 Unreal 실험 결과,보관된 측정 기록.
- [Epic Random Streams](https://dev.epicgames.com/documentation/unreal-engine/random-streams-in-unreal-engine):시드반복개념. 구체점화식·구간은설치5.8헤더/오늘실행으로확인했다.
- [PCG 기술보고서](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf),[Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/):2026-11-07의문헌근거이며오늘암호/네트워크실험은없다.
- [pret random.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/random.c),[random.h](https://github.com/pret/pokeemerald/blob/master/include/random.h):커뮤니티재구성·2026-11-07소스확인,게임빌드는수행하지않았다.
- 원래V55는탐색단서다. 생성알고리즘은NOISE/DUNGEON,영속복구는SAVE로별도조회한다. 파일저장·롤백·암호·렌더러/도구개선은제외했다.

### 측정값과 선택 조건

동일 호출량의 난수 구간 p95는 분리 0.1532/0.1423/0.1439ms, 공유 0.1938/0.1919/0.1941ms였다. 전체 프레임 p95는 분리 7.345/7.226/7.272ms, 공유 7.496/7.354/7.267ms였다. 난수 구간은 분리가 세 번 모두 빨랐지만 전체 프레임의 일관된 개선은 확인되지 않았다. 이 값은 위 raw 호출·카운터·체크섬·관찰 비용의 조건에 한정한다. 독립 스트림은 장식 호출이 게임 결과를 바꾸지 않도록 격리하기 위해 선택한다.

### 결과 정책 경계 — 2026-11-13

[RANDOM-DESIGN](K-GAME-TECH-RANDOM-DESIGN.kr.md)은시드스트림위에고정25%/백4/천장8을구현했다.성공률·연속실패·보장은이항목을조회한다.유한시드분포관측은난수통계독립이나보안을증명하지않는다.

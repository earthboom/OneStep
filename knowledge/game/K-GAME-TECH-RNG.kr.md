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

- [Melissa O'Neill — PCG Random Number Generators](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf)
- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

### 추가 조사 출처

- [pret/pokeemerald — random.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/random.c) — Random and SeedRng inspected; community reconstruction, not a vendor patch history.
- [pret/pokeemerald — random.h](https://github.com/pret/pokeemerald/blob/master/include/random.h) — ISO_RANDOMIZE1 and declarations inspected; formula transcribed, no game build.

추가 조사 출처의 영문 주석은 정확한 절·함수·접근 범위를 보존한다. 원본 슬라이드·문서·공개 코드의 확인과 실제 엔진·하드웨어 실행은 구분한다. 영상 설명·세션 개요만 확인한 자료를 전체 발표 확인으로 간주하지 않는다.

출발 영상: V55. [영상별 대응표](K-GAME-TECH-GUIDE.kr.md).

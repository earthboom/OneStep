# 헤어 카드·스트랜드와 시뮬레이션

기준 항목: K-GAME-TECH-HAIR · 확인일: 2026-11-07 · 참고 지식. 엔진 실행·성능·실제 플레이 검증은 별도다.

## 원리와 구현 요점

카드는 제작된 실루엣과 낮은 표현 예산에, 스트랜드는 근접 고품질 캐릭터에 검토한다. 렌더 표현·시뮬레이션 가이드·충돌·LOD를 분리하고 그룸 파이프라인을 고르기 전에 플랫폼 지원을 확인한다.

### 추가 조사로 보완한 구현

에픽은 가이드 시뮬레이션→렌더 가닥 보간→밀도 복셀화→가시성→조명→합성 단계를 구분한다. 렌더 곡선 수와 가이드 수 감소는 서로 다른 비용을 줄이며 화면 밖 헤어도 그림자를 위해 갱신될 수 있다. 카드·스트랜드·감소량 선택 전에 패스별로 측정한다. 캡콤 CEDEC 2026 세션 설명에서 PRAGMATA 장발·스트랜드의 Maya·RE ENGINE 제작 경로는 확인했지만 정확한 가닥·포인트 수는 확인하지 못했다.

## 적용 조건과 한계

렌더링되는 모든 가닥을 독립적으로 시뮬레이션할 필요는 없다. 장발 난도는 표현·충돌·동작 요구에 달려 있으며 단발이 보편적인 필수 조건은 아니다.

## 적용 전 점검

적용 전 점검: 어깨 접촉·급회전·모자·LOD 전환과 다수 캐릭터 동시 비용을 확인한다.

## 근거

- [Epic — Hair Rendering and Simulation](https://dev.epicgames.com/documentation/en-us/unreal-engine/hair-rendering-and-simulation-in-unreal-engine)

### 추가 조사 출처

- [Epic — Groom Scalability and Performance](https://dev.epicgames.com/documentation/unreal-engine/groom-scalability-and-performance-with-unreal-engine) — Geometry scalability and pipeline stages text inspected; no project performance measured.
- [Capcom speakers — PRAGMATA hair and facial development](https://cedec.cesa.or.jp/2026/timetable/detail/s69f305ca68328/) — Official CEDEC 2026 description and speaker affiliations; detailed presentation assets/counts not accessed.

추가 조사 출처의 영문 주석은 정확한 절·함수·접근 범위를 보존한다. 원본 슬라이드·문서·공개 코드의 확인과 실제 엔진·하드웨어 실행은 구분한다. 영상 설명·세션 개요만 확인한 자료를 전체 발표 확인으로 간주하지 않는다.

출발 영상: V13. [영상별 대응표](K-GAME-TECH-GUIDE.kr.md).

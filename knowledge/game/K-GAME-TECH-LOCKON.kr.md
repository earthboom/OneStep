# 락온·타겟 전환·카메라

기준 항목: K-GAME-TECH-LOCKON · 확인일: 2026-11-07 · 참고 지식. 엔진 실행·성능·실제 플레이 검증은 별도다.

## 원리와 구현 요점

거리·화면 방향·각도·시야로 후보를 평가한다. 비슷한 후보 간 깜빡임을 막는 이력과 명확한 전환·해제 규칙을 둔다. 카메라·캐릭터 회전을 분리하고 필요하면 선택 적 기준으로 횡이동을 정의한다.

### 추가 조사로 보완한 구현

닌텐도 원개발자 인터뷰는 Z 타게팅의 선택 적 식별 문제와 프로토타입 마커를 나비로 바꾼 과정을 설명한다. 표적 선택 피드백의 근거이지 세계 최초라는 근거는 아니다. 실무 구현은 해제 조건 전까지 현재 표적을 유지하고 신규 후보 평가는 획득·전환 때 수행하며 캐릭터 회전·선회 이동·카메라 구도를 분리한다. 일시 차폐 유예는 게임의 시야 정책이 허용할 때만 적용한다.

## 적용 조건과 한계

원개발자 설명은 Z 타게팅의 마커·나비 피드백 설계를 뒷받침하지만 세계 최초나 정확한 평가 수식의 근거는 아니다.

## 적용 전 점검

적용 전 점검: 적 중첩·차폐·카메라 뒤 이동·패드 타겟 전환을 확인한다.

## 근거

- [Epic — Mover Grappling Hook Movement Mode](https://dev.epicgames.com/documentation/unreal-engine/mover-03-grappling-hook-movement-mode?lang=en-US)
- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers)

### 추가 조사 출처

- [Nintendo — Where the Name Navi Came From](https://iwataasks.nintendo.com/interviews/3ds/zelda-ocarina-of-time/1/3/) — Original staff interview text retrieved by search; direct fetch timed out. Supports marker/Navi design account, not first-ever priority.

추가 조사 출처의 영문 주석은 정확한 절·함수·접근 범위를 보존한다. 원본 슬라이드·문서·공개 코드의 확인과 실제 엔진·하드웨어 실행은 구분한다. 영상 설명·세션 개요만 확인한 자료를 전체 발표 확인으로 간주하지 않는다.

출발 영상: V53. [영상별 대응표](K-GAME-TECH-GUIDE.kr.md).

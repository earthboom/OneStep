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

## 언리얼 락온 검증 — 2026-11-11

[실제 결과](../../prototypes/UnrealTechniqueLab/LOCKON-RESULTS.kr.md)는 고정 카메라·알려진5대상의 선택·유지·전환 검증이다. 거리·시야·중심점 Visibility 판정을 재사용한다. 획득1000cm/45도, 유지1100cm/50도 반각과 점수는 실험 설계값이며 상용 게임의 수치가 아니다. 유효한 현재 대상을 유지하고 명시적 좌우 입력으로 수평 각도/고정ID 순서를 순환한다. 전환 후보가 없어도 유지 조건을 만족하는 현재 대상은 남는다.

입력 상승 에지로만 처리하고 양쪽 방향이 함께 눌리면 순서가 엇갈려도 취소한다. 가림·이탈·삭제 시 즉시 해제하며 누름 유지로 재획득하지 않는다. 고정ID와 Actor 수명은 다르므로 이전 약한 참조를 확인해 같은ID의 교체 객체가 선택을 상속하지 않도록 한다. no-hit은 감지가 아니다.

정책37·실제PIE6실행/198상황·관측30/60/144FPS와 동일 패키지 성능3쌍, 정상 속도 실제 캡처를 확인했다. 독립 검토의 양방향 누름 문제는 실패→수정→성공으로 검증했다. 성능 장면에서5회→3회/평가로40% 쿼리가 줄어도 전체 프레임 개선·다수NPC 확장성을 보장하지 않는다. 전체 프레임과 판정 비용을 함께 기록한다. 물리 입력·사용감·카메라 이동·전투AI·이동·네트워크는 미검증이다. 도구/저장/렌더 최적화는 추가하지 않았다.

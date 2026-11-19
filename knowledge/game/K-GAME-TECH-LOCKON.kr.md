# 선택한 대상의 생존과 락온 전환 조건 확인하기

**K-GAME-TECH-LOCKON** · 명시한 가시성과 점수 규칙으로 대상을 획득한다. 해제 조건이 발생하거나 플레이어가 전환할 때까지 유효한 대상을 유지한다.

## 지침

거리·시야각·가시선으로 후보를 거르고 남은 후보의 점수를 계산한다. 히스테리시스는 획득 범위보다 넓은 이탈 범위를 두어 경계 떨림을 줄인다. 현재 대상을 유지하면 두 점수가 엇갈릴 때마다 선택이 바뀌는 일을 막는다. 동점·전환 순서와 가림 유예를 정하고, 각도 기준 중앙과 화면 픽셀 거리를 구분한다.

## 적용 조건과 예외

언리얼의 `TWeakObjectPtr`은 객체를 소유하지 않는 약한 참조다. 사용 전 유효성을 검사해 파괴된 액터의 선택이 같은 게임 ID를 재사용한 새 액터로 넘어가지 않게 한다. 버튼 누름 순간과 계속 누르는 상태는 구분한다. 캐릭터 방향, 카메라 궤도, 공격 결정은 선택 결과를 각각 사용할 수 있다.

## 확인 방법

화면 중앙에서 두 표적을 교차시키고 획득·이탈 경계를 오간다. 선택한 액터의 파괴·교체·가림과 양쪽 전환 버튼을 동시에 누르는 상황을 검사한다. 변화 전후 대상을 비교하고 실제 입력과 카메라 체감은 플레이로 평가한다.

## 근거

Nintendo 개발진 인터뷰는 Z 타기팅의 피드백과 Navi를, Epic 예제는 후보 필터링을 설명한다. 기존 언리얼 스크립트 검사는 고정 시점의 선택 유지·전환·액터 교체를 다뤘다. 카메라 체감과 Nintendo 내부 구현은 검증 범위 밖이다.

- [Nintendo — Where the Name Navi Came From](https://iwataasks.nintendo.com/interviews/3ds/zelda-ocarina-of-time/1/3/)
- [Epic — Mover Grappling Hook Movement Mode](https://dev.epicgames.com/documentation/unreal-engine/mover-03-grappling-hook-movement-mode?lang=en-US)
- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers)
- [Epic — Object Pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine)

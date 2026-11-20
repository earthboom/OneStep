# C++ 구현 가이드

> 사람이 읽는 한국어 번역본이다. 코딩 에이전트는 영문 구현 가이드를 사용한다.

구현 방식을 결정해야 하는 변경에서는 해당 항목을 참고한다. 현재 작업 중인 프로젝트의 지침과 관례를 우선한다.

## 문법 기능, 타입, 소유권

- 대상의 툴체인이 지원하는 문법 기능과 라이브러리 타입을 선택한다. 타입 추론과 오류 처리는 주변 코드의 관례를 따른다. 선언이 더 읽기 쉬워질 때 `auto`를 쓰고, 의도한 복사·참조·포인터 여부를 드러낸다.
- 복사 비용이 낮은 입력은 값으로, 복사 비용이 큰 읽기 전용 입력은 상황에 맞게 `const&`로 받는다. 자원은 RAII로 관리한다. 뷰나 참조를 보관할 때는 원본 객체가 더 오래 살아 있는지 확인한다.
- **순수 C++ 예시** — 프로젝트에서 타입 추론을 허용한다면 루프에서 아이템을 조회할 때 `const auto& item`을 쓴다. `std::string_view`의 원본보다 텍스트를 오래 보관해야 하면 소유하는 문자열로 복사한다.
- **Unreal C++ 예시** — 모듈의 `auto` 사용 관례를 따른다. 컴포넌트가 GC로 해제되지 않도록 유지해야 하는 지속 참조는 `UPROPERTY()`가 붙은 `TObjectPtr<UInventoryComponent>`로 표현한다. 비소유 캐시는 `TWeakObjectPtr`로 두고 사용할 때 유효성을 확인한다.

참고 자료 — [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) · [Abseil 매개변수 전달 가이드](https://abseil.io/tips/234) · [Epic C++ 코딩 표준](https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine) · [Unreal 객체 포인터](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine)

## 이름과 호출부 가독성

- 프로젝트의 도메인 용어와 명명 관례를 따른다. 사용처에서 역할을 이해할 수 있도록 이름을 짓는다. 타입만으로 단위를 알 수 없을 때는 이름에 단위를 표시하고, 불리언은 참·거짓을 묻는 형태로 짓는다.
- 불리언 리터럴 하나나 여러 개를 넘겨 호출부의 선택을 알아보기 어렵다면, 선택을 드러내는 이름 있는 모드나 옵션 타입을 사용한다.
- **순수 C++ 예시** — `remainingSlots`나 `retryDelayMs`처럼 짓는다. `Save(path, SaveMode::Overwrite)`는 호출부에서 저장 방식을 드러낸다.
- **Unreal C++ 예시** — 한도는 `MaxStackCount`, 불리언 필드는 `bHasPendingReward`, 조회 함수는 `IsInventoryFull()`처럼 짓는다.

참고 자료 — [식별자와 코드 이해 연구](https://www.se.cs.uni-saarland.de/publications/docs/HoSeHo17.pdf) · [Abseil 호출부 가독성 가이드](https://abseil.io/tips/94) · [Epic 명명 관례](https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine#naming-conventions)

## 디자인 패턴

어떤 동작이 바뀌는지, 어느 경계에서 변환이 필요한지 먼저 설명한다. 요구사항을 충족하는 가장 작은 구현을 선택하고, 프로젝트에 이미 맞는 방식이 있으면 재사용한다.

| 필요한 동작 | 순수 C++ 예시 | Unreal C++ 예시 |
| --- | --- | --- |
| **Strategy**로 동작을 교체한다. | 이벤트별 보상 공식을 함수나 람다로 전달한다. | 보상 정책을 전달하고 컴포넌트가 그 결과를 적용한다. |
| **Adapter**로 맞지 않는 API를 연결한다. | SDK 결과를 프로젝트의 기존 값·오류 타입으로 변환한다. | 온라인 서비스의 결과를 게임플레이 코드가 사용하는 결과 타입으로 변환한다. |
| **Observer**로 독립적인 기능에 알린다. | UI와 텔레메트리 콜백이 인벤토리 변경을 구독하고, 구독을 언제 해제할지 정한다. | HUD를 인벤토리 컴포넌트의 변경 델리게이트에 연결하고 HUD를 정리할 때 연결을 해제한다. |
| **상태 머신**으로 허용 전이를 표현한다. | `Idle`, `Charging`, `Released`를 `enum class`와 명시적 전이로 표현한다. | 능력의 상태 전이는 그 상태를 소유한 컴포넌트에 둔다. |

참고 자료 — [디자인 패턴 유지보수 실험](https://ps.ipd.kit.edu/downloads/zeitschriftenartikel_PatmainTSE2001.pdf) · [C++ Software Design](https://www.oreilly.com/library/view/c-software-design/9781098113155/ch05.html) · [Unreal 델리게이트](https://dev.epicgames.com/documentation/en-us/unreal-engine/delegates-and-lambda-functions-in-unreal-engine)

## 성능 개선

- 측정 지표와 대표 작업 부하를 정한다. 관련 호출 경로를 프로파일링하고, 반복 작업·복사·할당·낮은 데이터 지역성 등 실제로 측정된 비용을 개선한다.
- 영향을 받는 동작을 확인하고, 같은 입력과 실행 조건으로 수정 전후를 측정한다. 결과와 함께 추가 메모리나 준비 시간 등 관련 비용도 보고한다. 측정할 수 없다면 기대 효과를 가설로 설명한다.
- **순수 C++ 예시** — 반복 선형 탐색을 인덱스로 바꾸기 전에 대표 데이터 크기에서 조회 시간, 인덱스 생성 시간, 메모리 사용량을 비교한다.
- **Unreal C++ 예시** — 프로파일링에서 `TArray` 재할당 비용이 드러나고 예상 요소 수를 안다면 `Reserve()`를 검토한다. 같은 게임플레이 시나리오에서 Unreal Insights로 할당과 프레임 시간을 비교한다.

참고 자료 — [Google 성능 튜닝 사례](https://abseil.io/fast/hints) · [코딩 에이전트 PR의 성능 검증 연구](https://arxiv.org/abs/2610.03969) · [Unreal 배열 컨테이너](https://dev.epicgames.com/documentation/en-us/unreal-engine/array-containers-in-unreal-engine) · [Unreal Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine)

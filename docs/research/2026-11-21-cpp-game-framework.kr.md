# C++ 게임플레이 프레임워크 자료 조사

2026-11-21 · 독립 C++와 Unreal Engine 5의 게임플레이 코드

**변경이 어디까지 퍼지는지로 프레임워크를 평가한다.** 인벤토리의 내부 자료구조를 바꾸면 인벤토리 안에서 수정이 끝나는지, 새 능력을 추가하면 그 능력의 구현과 등록 지점으로 변경이 모이는지, 맵이 바뀌면 월드의 상태와 구독이 함께 정리되는지 확인한다. 이 세 가지는 모듈화·확장성·수명 관리를 실제 변경으로 평가하는 출발점이다.

여기서 프레임워크는 게임 규칙, 상태 소유권, 기능 조립, 엔진과의 연결을 담당하는 코드다. 렌더러·물리 엔진의 구현은 의존성이 게임플레이 구조에 영향을 주는 경우에 참고한다. 최종 장르, 멀티플레이 요구, 배포 대상, 성능 예산이 정해지면 아래의 조건부 제안을 다시 판단한다.

## 설계 판단에 바로 쓸 자료

| 자료 | 원문에서 확인할 내용 | 우리 코드에 적용할 질문 |
| --- | --- | --- |
| Parnas, 1972 · 논문 | 같은 시스템을 처리 단계와 정보 은닉으로 각각 분해한다. 원문의 `Improvement in Circular Shift Module`은 인터페이스가 실제로 필요하지 않은 순서까지 약속했을 때 구현 선택이 제한된다는 사례다. [ACM](https://doi.org/10.1145/361598.361623) · [논문 본문](https://ckrybus.com/static/papers/decomposing_systems_into_modules_1972.pdf) | 인벤토리 호출자가 슬롯 배열, 정렬 순서, 저장 포맷 중 무엇을 알아야 하는가? 배열을 바꿔도 지급·조회 계약을 유지할 수 있는가? |
| Liskov·Wing, 1994 · 논문 | 상위 타입으로 알 수 있는 불변식과 상태 변화의 성질이 하위 타입에서도 성립해야 한다. §4.3과 §5.1. [저자 공개본](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf) | 같은 능력 인터페이스를 쓰는 구현이 실패·취소 시 비용과 쿨다운에 관해 동일한 약속을 지키는가? |
| Daly 외, 1996 및 Unger·Prechelt, 1998 · 원실험과 재현 연구 | 상속 깊이와 유지보수 시간의 관계가 실험 조건과 과제에 따라 달랐다. 재현 연구는 이해를 위해 추적한 메서드 수와 작업 시간의 상관도 보고했다. 두 연구는 실험 과제를 비교한 자료다. [Daly 원문](https://strathprints.strath.ac.uk/2676/1/strathprints002676.pdf) · [재현 연구](https://page.mi.fu-berlin.de/prechelt/Biblio/inheritTR.pdf) | 계층 깊이 상한을 정하기 전에, 한 요청에서 실제 구현과 상태 변경을 찾는 데 거치는 오버라이드와 간접 호출을 세어볼 수 있는가? |
| Ullmann 외, 2025 · SyDRA 논문 | C++ 엔진 10개의 `#include` 관계를 서브시스템으로 묶었다. Godot을 대상으로 한 16명 실험에서 해당 지도가 코드 이해와 변경 영향 분석을 도왔다. 표본과 실험 범위는 §5–6을 참고한다. [논문](https://espace2.etsmtl.ca/id/eprint/29117/1/Petrillo-F-2024-29117.pdf) | 소스·빌드 의존성, 에셋 참조, 런타임의 호출·수명 관계를 각각 조사하면 어느 경로를 통해 변경이 퍼지는지 설명할 수 있는가? |
| Redmond 외, 2025 · Core ECS 논문 | ECS 시스템의 쿼리와 상태 변경이 실행 순서에 따라 언제 관찰되는지 모델링하고, 결정성을 보존하는 조건을 실제 프레임워크 5개와 비교한다. §4–5. [논문](https://arxiv.org/abs/2508.15264) · [OOPSLA 발표](https://www.youtube.com/watch?v=z2vqiVtmsuY) | 시스템별 읽기·쓰기 대상과 구조 변경 반영 시점을 명시할 수 있는가? 같은 입력에서 순서가 달라지면 결과가 달라지는가? |
| C++ Core Guidelines 및 WG21 P3019R14 · 지침과 표준 제안 | Core Guidelines의 C.120·C.129·C.133은 계층의 용도, 인터페이스 상속과 구현 상속, `protected` 데이터의 비용을 설명한다. P3019R14는 동적 할당을 이용하는 값 의미론의 조합 타입 `indirect`와 `polymorphic`을 제시한다. 해당 타입의 툴체인 지원은 별도로 확인한다. [Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c-hier-class-hierarchies-oop) · [WG21 제안서](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3019r14.pdf) | 변경 가능한 정책을 값·함수·컴포넌트·런타임 다형성 중 어디에 두면 소유권과 호출 계약이 가장 명확해지는가? |

## 게임 개발자 발표와 실제 코드

| 자료 | 확인할 지점과 적용 범위 |
| --- | --- |
| **Dungeon Siege · Scott Bilas, GDC 2002** | 행동을 바꿀 때마다 C++ 계층을 재편하던 경험에서 출발한다. `Solution: Component System` 슬라이드는 코드로 작성한 동작을 데이터로 조립하고 외부 스키마로 검사하는 해법을 보여준다. 디자이너가 자주 조합을 바꾸는 기능에 특히 관련 있다. [발표 슬라이드와 발표자 노트](https://this.scottbilas.com/files/pubs/2002/gdc-san-jose/GameObjects.pdf) · [개발자 회고](https://this.scottbilas.com/) |
| **Overwatch · Timothy Ford, GDC 2017** | 여러 영웅의 기능 조합과 네트워크 시뮬레이션에 ECS를 사용한 출시작 사례다. 개발자가 어떤 문제에 ECS를 택했는지와 결정성을 네트워크 동작에 어떻게 활용했는지를 보는 자료다. [GDC Vault](https://gdcvault.com/play/1024001/-Overwatch-Gameplay-Architecture-and) · [GDC 공식 영상](https://www.youtube.com/watch?v=W3aieHjyNvw) |
| **Lyra · Epic Games** | Experience를 바꾸면 로드하는 Game Feature와 Pawn 설정이 달라진다. `ULyraPawnExtensionComponent`와 `ULyraHeroComponent`는 데이터 준비와 기능 초기화를 조율한다. Epic은 Init State 도입 전 Lyra 5.0의 경쟁 조건도 설명한다. 초기화 상태와 일회성 확장 이벤트가 각각 언제 쓰이는지 비교할 수 있다. [Tech Talk](https://dev.epicgames.com/community/learning/talks-and-demos/yrrn/lyra-starter-game-overview) · [샘플](https://dev.epicgames.com/documentation/unreal-engine/lyra-sample-game-in-unreal-engine) · [Init State 구현 설명](https://dev.epicgames.com/documentation/unreal-engine/game-framework-component-manager-in-unreal-engine?lang=en-US) |
| **Action Roguelike · Tom Looman, Inside Unreal 및 소스** | `URogueActionComponent`가 기본 액션을 권한 측에서 추가하고 `EndPlay`에서 중지시키는 경로를 볼 수 있다. `URogueAction`의 시작·정지 훅, 복제 상태, 표시용 훅을 함께 읽으면 작은 샘플이 조합과 상속을 함께 쓰는 방식을 추적할 수 있다. 영상과 현재 `master`는 시점이 다르다. [Inside Unreal 영상](https://www.youtube.com/watch?v=YKhcN8NkIYY) · [액션 컴포넌트 구현](https://github.com/tomlooman/ActionRoguelike/blob/master/Source/ActionRoguelike/ActionSystem/RogueActionComponent.cpp) · [액션 헤더](https://github.com/tomlooman/ActionRoguelike/blob/master/Source/ActionRoguelike/ActionSystem/RogueAction.h) |
| **Game Programming Patterns · Robert Nystrom** | `Component` 장은 입력·물리·표현을 나눌 때 생기는 조립과 간접 참조 비용을 다룬다. `Event Queue` 장은 발신과 소비 시점을 분리할 때의 이점과 전역 큐의 결합 문제를 설명한다. [Component 원문](https://raw.githubusercontent.com/munificent/game-programming-patterns/master/book/component.markdown) · [Event Queue 원문](https://raw.githubusercontent.com/munificent/game-programming-patterns/master/book/event-queue.markdown) |
| **Sean Parent 및 Mike Acton · C++ 발표** | Parent는 비침투 런타임 다형성과 값 의미론을 구현하는 예를 다룬다. Acton은 콘솔 게임의 성능 민감 경로를 데이터와 연산 중심으로 보는 관점을 제시한다. [Parent, GoingNative 2013](https://learn.microsoft.com/en-us/shows/goingnative-2013/inheritance-base-class-of-evil) · [Acton, CppCon 2014](https://www.youtube.com/watch?v=rX0ItVEVjHc) |
| **Godot과 O3DE · 다른 C++ 엔진 사례** | Godot `Node`는 SceneTree 진입·종료와 처리 훅을 제공한다. O3DE는 컴포넌트의 제공·필수·비호환 서비스를 선언할 수 있고, 의존 순서대로 활성화한 뒤 역순으로 비활성화한다. 프레임워크가 조합과 수명 순서를 보장하는 서로 다른 사례다. [Godot Node 문서](https://docs.godotengine.org/en/stable/classes/class_node.html) · [Node C++ 구현](https://github.com/godotengine/godot/blob/master/scene/main/node.cpp) · [O3DE 컴포넌트 계약](https://docs.o3de.org/docs/user-guide/programming/components/create-component/) |

## 모듈화와 확장 방식 선택

아래는 자료를 바탕으로 정리한 설계 제안이다. 같은 게임 안에서도 해결할 문제에 따라 여러 방식을 조합할 수 있다.

| 해결할 문제 | 먼저 검토할 방식 | 확인할 비용과 계약 |
| --- | --- | --- |
| 아이템 용량, 보상 승인, 쿨다운처럼 호출자가 공유하는 규칙 | 상태와 변경 연산을 같은 C++ 타입 또는 모듈에 둔다. 구현에 엔진 상태가 필요 없는 규칙은 엔진 없이 검사할 수 있다. | 실패 후 상태, 취소·재시도, 입력과 결과. 규칙을 떼어낼 때 변환 코드와 중복 상태가 늘어나는지도 본다. |
| 여러 Actor가 상호작용·인벤토리 같은 기능을 서로 다른 조합으로 사용 | 독립 C++의 멤버 조합 또는 Unreal의 `UActorComponent`를 검토한다. 콘텐츠마다 달라지는 값과 조합은 검증 가능한 에셋이나 설정으로 표현한다. | 필수 동료 컴포넌트, Actor 수명, 중복 등록, 구성 오류의 발견 시점. 성능 민감한 경로라면 호출과 메모리 비용도 측정한다. |
| 한 계약을 만족하는 구현을 런타임에 교체하거나 엔진 훅을 재정의 | 좁은 인터페이스 또는 기존 엔진 기반 클래스의 훅을 사용한다. 독립적으로 달라지는 정책은 타입·함수·컴포넌트로 조합한다. | 대체 구현이 사전조건·사후조건·불변식을 지키는지, 실패와 정리를 같은 방식으로 처리하는지 공통 테스트로 확인한다. |
| 빌드 의존성이나 편집기 기능을 격리 | Unreal에서는 `Build.cs`의 공개·비공개 의존성과 `Public`·`Private` 헤더를, 독립 C++에서 CMake를 쓰면 프로젝트의 타깃 의존성을 검사한다. | 어떤 공개 헤더가 의존성을 전파하는지와 변경 후 실제 재빌드 범위를 확인한다. 에셋 의존성은 Unreal Reference Viewer에서 따로 추적한다. [Unreal Modules](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-modules) · [CMake 타깃 링크 계약](https://cmake.org/cmake/help/latest/command/target_link_libraries.html) · [Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine) |
| 모드별 콘텐츠를 묶거나 선택 기능을 독립적으로 활성화 | 일반 모듈로 빌드 경계를 만들 수 있다. 런타임 활성화가 요구되면 Unreal Game Feature와 활성화·비활성화 훅을 검토한다. | 액션·입력·구독·비동기 요청의 정리, 재활성화, 에셋 참조, 사용 환경의 쿠킹과 패키징. `Deactivate`와 `Unload`는 별도 단계다. [Game Features](https://dev.epicgames.com/documentation/en-us/unreal-engine/game-features-and-modular-gameplay-in-unreal-engine) · [Game Feature Action 수명주기](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/GameFeatures/UGameFeatureAction) |
| 많은 개체의 같은 데이터를 반복 갱신 | 먼저 타깃 작업 부하를 재고, 아키타입 기반 Flecs·MassEntity나 EnTT의 sparse-set 기반 저장소를 비교한다. 단순한 연속 배열을 포함해 같은 시나리오로 비교할 수 있다. | 매 프레임 읽기·쓰기, 생성·삭제와 조합 변경 빈도, 스케줄, 저장 비용, 디버깅, 데이터와 Actor 사이의 동기화. [Flecs Quickstart](https://www.flecs.dev/flecs/Quickstart.html) · [EnTT 개발자 발표 자료](https://skypjack.github.io/pdf/the_cpp_of_entt.pdf) · [MassEntity 문서](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-entity-in-unreal-engine?lang=en-US) |

### 캡슐화의 구체적인 기준

인벤토리는 보유량과 용량의 불변식을 소유한다. `TryAdd` 같은 변경 연산에서 성공·실패와 상태 반영 규칙을 정의하고, UI에는 표시에 필요한 값과 변경 알림을 제공한다. 내부 컨테이너의 변경 가능한 참조를 반환하면 `private` 필드의 보호를 우회할 수 있다. 복사를 피하려고 읽기 전용 뷰를 제공해야 한다면 유효 기간과 무효화 조건도 인터페이스에 포함한다. 저장 데이터는 읽기 경계에서 검증한 뒤 소유 모듈을 통해 반영한다. [정보 은닉](../../knowledge/code/K-CODE-INFORMATION-HIDING.kr.md) · [데이터 불변식](../../knowledge/code/K-CODE-DATA-INVARIANTS.kr.md)

### Unreal에서 특히 중요한 경계

- **권한과 화면 표시.** 멀티플레이에서 `GameMode`는 서버에만 있고 `GameState`는 서버와 클라이언트에 있다. 매치 규칙과 클라이언트가 관측할 매치 상태를 배치할 때 이 차이를 이용한다. 재스폰 전후 유지해야 할 플레이어 상태는 Pawn과 `PlayerState` 중 어느 수명에 속하는지 결정한다. Lyra의 Pawn Extension은 Pawn 때문에 부여된 능력을 추적해 Pawn 파괴 또는 빙의 해제 시 제거한다. [Gameplay Framework Quick Reference](https://dev.epicgames.com/documentation/unreal-engine/gameplay-framework-quick-reference-in-unreal-engine?lang=en-US) · [Lyra 능력 초기화](https://dev.epicgames.com/documentation/unreal-engine/abilities-in-lyra-in-unreal-engine?lang=en-US#how-are-lyra-characters-initialized)
- **수명과 참조.** 월드별 상태는 월드 수명, Game Instance 전반의 상태는 해당 인스턴스 수명에 맞춘다. 지속되는 `UObject` 강한 참조를 GC가 추적해야 하면 `UPROPERTY`가 붙은 `TObjectPtr`, 파괴될 수 있는 객체의 비소유 참조에는 `TWeakObjectPtr`, 필요 시 로드할 에셋에는 `TSoftObjectPtr`를 검토한다. Actor 정리는 파괴뿐 아니라 맵 이동·스트리밍 언로드·PIE 종료로도 호출되는 `EndPlay` 경로에서 확인한다. [Subsystems](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-subsystems-in-unreal-engine?lang=en-US) · [Object Pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine?lang=en-US) · [Actor Lifecycle](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-actor-lifecycle)
- **요청과 알림.** 버튼의 사용 요청은 결과를 반환할 수 있는 연산으로 상태 소유자에게 전달한다. 성공 후 UI나 사운드에는 확정 결과를 알린다. 지연 소비가 필요한 이벤트는 발행 시점의 데이터, 소비 순서, 종료 후 남은 항목의 처리 조건을 정한다. 이미 초기화된 객체에 뒤늦게 붙는 구독자가 있다면 현재 상태 조회와 변경 알림을 함께 설계한다. [Event Queue 원문](https://raw.githubusercontent.com/munificent/game-programming-patterns/master/book/event-queue.markdown) · [Unreal Component Manager의 확장 이벤트와 Init State](https://dev.epicgames.com/documentation/unreal-engine/game-framework-component-manager-in-unreal-engine?lang=en-US)

## 설계안을 검증할 첫 기능

**재사용 대기시간이 있는 능력 하나**를 예시로 삼는다. 입력으로 사용을 요청하고, 조건을 검사한 뒤 비용과 쿨다운을 반영하고, 결과를 UI에 표시한다. 두 번째 능력을 추가하며 재사용된 규칙과 새 구현의 변경 위치를 기록한다. 대상 게임에서 능력이 핵심이 아니라면 인벤토리 지급·소모처럼 상태 변경, 실패, 표현을 함께 검증할 수 있는 대표 기능도 적합하다.

| 시나리오 | 관찰할 결과 |
| --- | --- |
| 두 번째 능력 추가 | 새 능력의 정책과 등록 지점이 어디인지 찾을 수 있다. 기존 능력과 공유하는 계약을 같은 테스트로 확인한다. |
| 실패·취소·중복 입력 | 요청 결과와 비용·쿨다운의 변화를 확인한다. 중복 요청이 비용을 다시 적용하는지, 취소가 허용되는 각 단계에서 어떤 상태가 남는지 검사한다. |
| UI 교체 또는 HUD 없는 실행 | 같은 게임플레이 입력에서 권한 측 결과가 일치한다. 멀티플레이가 요구된다면 실제 클라이언트와 함께 검사한다. |
| 늦은 초기화·재스폰·맵 전환 | 판단에 필요한 데이터가 늦게 도착해도 준비 완료 후에만 기능이 실행된다. 이전 Pawn·월드의 이벤트, 입력 바인딩, 타이머, 비동기 완료 처리가 정리된다. |
| 기능 활성화·비활성화·재활성화 | 런타임 선택 기능을 도입한 경우에 검사한다. 등록과 정리가 대칭이고 재활성화 뒤 핸들러 수가 증가하지 않는다. 대상 패키지에서도 기능을 끈 상태로 기본 플레이 경로에 진입할 수 있다. |
| 저장·갱신·복구 | 지속성이 요구되면 이전 버전 데이터를 읽어 유효한 상태로 복원한다. 로드 실패나 취소 시 기존 상태에 일부만 반영되는지 확인한다. |
| 대량 처리 비교 | 병목이 있는 경우 같은 입력, 개체 수, 생성·삭제 패턴에서 프레임 시간 분포와 최대 메모리를 비교한다. 프레임 간 처리 순서가 달라지더라도 보존해야 할 결과가 일치하는지 검사한다. |

독립적인 규칙은 해당 C++ 테스트에서 확인하고, 엔진의 소유권·복제·에셋 문제는 기능 테스트와 대상 빌드에서 확인한다. 유지보수성 비교에는 변경한 모듈과 파일, 추가한 공개 인터페이스, 정상·실패 흐름을 찾기 위해 추적한 경로, 기존 동작의 회귀 여부를 기록한다. 위 시나리오는 설계안에 적용할 검증 항목이다. [Unreal Automation Test Framework](https://dev.epicgames.com/documentation/unreal-engine/automation-test-framework-in-unreal-engine?lang=en-US) · [네트워크 게임 테스트](https://dev.epicgames.com/documentation/en-us/unreal-engine/testing-and-debugging-networked-games-in-unreal-engine)

## OneStep에서 이어 읽을 자료와 확인 범위

- **실행 예시.** 독립 C++ 턴제 전술과 언리얼 C++ 실시간 액션에서 선택 콘텐츠를 추가하고, 기본·단독·조합 구성을 실제 실행으로 비교했다. [C++ 게임플레이 작업 예시](../examples/cpp-gameplay-workflow/README.md)
- **기존 판단 기준.** C++ 작업 지침과 구현 가이드의 호출 경로·소유권·의존성 판단을 출발점으로 삼았다. [C++ 작업 지침](../../skills/vegabond-code/references/cpp-project-guidelines.kr.md) · [구현 가이드](../../skills/vegabond-code/references/cpp-implementation.kr.md) · [정보 은닉](../../knowledge/code/K-CODE-INFORMATION-HIDING.kr.md) · [의존 방향](../../knowledge/code/K-CODE-DEPENDENCY-DIRECTION.kr.md) · [추상화 비용](../../knowledge/code/K-CODE-ABSTRACTION-COST.kr.md) · [유지보수성 평가](../../knowledge/code/K-CODE-MAINTAINABILITY-EVIDENCE.kr.md)
- **자료의 범위.** 논문은 관련 절, 공식 문서는 명시된 계약, 공개 코드는 해당 심볼을 확인했다. 영상 링크는 공식 소개와 발표 페이지를 기준으로 수집했다. Lyra는 Epic의 배포·구현 설명을 참고했으며 적용 대상에서는 설치된 UE 버전의 샘플과 소스로 다시 확인해야 한다. 이번 조사에 이어 만든 Pulse Arena 예시의 `EngineAssociation`은 `5.8`이다. [Pulse Arena 프로젝트 설정](../examples/cpp-gameplay-workflow/unreal-action/PulseArena.uproject)
- **남은 판단.** 실제 프로젝트에 필요한 멀티플레이 형태, 맵 이동·재스폰 정책, 콘텐츠 조립의 변경 빈도, 배포 단위, 기대 개체 수와 프레임 예산에 따라 적합한 조합이 달라진다. 위 사례에서 프레임워크 전체의 성능이나 유지보수 결과를 추정하려면 해당 프로젝트의 대표 변경과 실행 측정이 필요하다.

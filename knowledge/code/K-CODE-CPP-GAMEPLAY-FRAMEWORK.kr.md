# C++ 게임플레이의 소유권과 변경 범위로 구성 방식 선택하기

K-CODE-CPP-GAMEPLAY-FRAMEWORK · 방법 · 적용 중 · 근거 확인 2026-11-21

게임플레이 요청에서 상태 소유자, 빌드 의존성, 등록점, 수명을 추적한다. 두 번째 능력을 추가하고 선택 기능을 제거해 경계를 확인한다.

적용 범위 — 독립 C++ 및 Unreal 게임플레이. 엔진 계약은 설치 버전, 권한, 실행 구성에 따라 달라진다.

## 적용 방법

불변조건을 책임지는 상태와 연산을 한곳에 둔다. 인벤토리는 아이템 지급·조회 결과를 공개하고 슬롯 배치, 정렬, 용량, 저장 방식은 내부에서 관리한다. 능력 사용 요청은 소유자가 승인·거절하고 공개 계약에 따라 비용과 재사용 대기시간을 적용한다. UI에는 판정 후 결과를 알린다.

독립적으로 바뀌는 동작에는 값, 정책 객체, 멤버 컴포넌트를 쓴다. 호출자가 초기화·실패·취소 보장을 공유할 때 가상 디스패치나 엔진 훅을 고려한다. 한 요청을 이해하려고 거치는 메서드와 오버라이드를 추적한다. 컴파일·링크 의존성, 에셋 참조, 런타임 활성화를 따로 본다. 빌드 경계는 일반 Unreal 모듈로도 만들 수 있다. 독립 활성화용 Game Features를 도입하면 등록·준비·비활성화 책임도 생긴다.

대량 갱신에 ECS를 검토할 때는 읽기·쓰기 집합, 구조 변경이 보이는 시점, 처리 순서를 정하고 대상 작업량에서 현재 배치와 비교한다. Unreal에서 서버의 GameMode와 복제되는 GameState는 접근 주체가 다르다. 상태를 Pawn·월드·Game Instance 수명에 맞추고 소유 경계에서 타이머·구독·입력을 해제한다. 선행 조건이 늦게 도착하면 준비된 뒤 활성화한다.

## 적용 조건과 예외

Dungeon Siege와 Overwatch의 조합·네트워크 요구는 해당 게임의 사례다. Lyra와 Action Roguelike는 특정 엔진과 초기화 절차를 전제한다. 상속 실험의 결과는 과제마다 달랐고, SyDRA는 엔진 10개의 헤더 관계를 분석하고 참여자 16명으로 이해도를 조사했다. Core ECS의 결정성은 형식 모델의 성질이다. 상속 깊이 제한, 전면 ECS 전환, 실제 플랫폼 간 결정성을 이 사례들만으로 정할 수 없다. WG21 제안은 컴파일러 지원 여부도 확인한다.

## 확인 방법

능력 하나에서 승인·실패·취소·중복 입력, 지연 초기화, 리스폰, 맵 이동을 확인한다. 호출부를 고치지 않고 두 번째 정책을 추가한다. HUD를 빼도 권한 주체의 결과가 같은지 본다. 선택 기능은 기본·A·B·동시 실행, 비활성화와 재활성화, A를 뺀 빌드를 확인한다. 저장 기능은 구버전 파일과 쓰기 중단을, 복제는 실제 서버·클라이언트 역할을 검사한다. 성능은 동일 입력·엔티티 수·빌드에서 프레임 시간 분포로 비교한다.

## 근거

11월 21일 검토는 논문의 해당 절, 문서의 계약, 공개 코드의 식별자를 확인했다. 영상 관련 자료에는 공식 소개와 슬라이드가 포함된다. C++와 Unreal 실행 사례의 근거 범위는 실제로 검사한 선택 콘텐츠 경로다. Unreal 예제의 EngineAssociation은 5.8이다.

[게임플레이 실행 사례](../../docs/examples/cpp-gameplay-workflow/README.md) · [정보 은닉](K-CODE-INFORMATION-HIDING.md) · [의존 방향](K-CODE-DEPENDENCY-DIRECTION.md) · [추상화 비용](K-CODE-ABSTRACTION-COST.md)

- [ACM](https://doi.org/10.1145/361598.361623) · [Full paper](https://ckrybus.com/static/papers/decomposing_systems_into_modules_1972.pdf) · [Liskov and Wing, 1994 — Authors' copy](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf) · [Daly paper](https://strathprints.strath.ac.uk/2676/1/strathprints002676.pdf) · [Replication](https://page.mi.fu-berlin.de/prechelt/Biblio/inheritTR.pdf)
- [Ullmann et al., 2025 — Paper](https://espace2.etsmtl.ca/id/eprint/29117/1/Petrillo-F-2024-29117.pdf) · [Redmond et al., 2025 — Paper](https://arxiv.org/abs/2508.15264) · [OOPSLA talk](https://www.youtube.com/watch?v=z2vqiVtmsuY) · [Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#c-hier-class-hierarchies-oop) · [WG21 proposal](https://www.open-std.org/jtc1/sc22/wg21/docs/papers/2025/p3019r14.pdf)
- [Dungeon Siege — Slides and speaker notes](https://this.scottbilas.com/files/pubs/2002/gdc-san-jose/GameObjects.pdf) · [Developer retrospective](https://this.scottbilas.com/) · [GDC Vault](https://gdcvault.com/play/1024001/-Overwatch-Gameplay-Architecture-and) · [Official GDC video](https://www.youtube.com/watch?v=W3aieHjyNvw) · [Tech Talk](https://dev.epicgames.com/community/learning/talks-and-demos/yrrn/lyra-starter-game-overview)
- [Sample](https://dev.epicgames.com/documentation/unreal-engine/lyra-sample-game-in-unreal-engine) · [Init State implementation](https://dev.epicgames.com/documentation/unreal-engine/game-framework-component-manager-in-unreal-engine?lang=en-US) · [Inside Unreal video](https://www.youtube.com/watch?v=YKhcN8NkIYY) · [Action component implementation](https://github.com/tomlooman/ActionRoguelike/blob/master/Source/ActionRoguelike/ActionSystem/RogueActionComponent.cpp) · [Action header](https://github.com/tomlooman/ActionRoguelike/blob/master/Source/ActionRoguelike/ActionSystem/RogueAction.h)
- [Component chapter](https://raw.githubusercontent.com/munificent/game-programming-patterns/master/book/component.markdown) · [Event Queue chapter](https://raw.githubusercontent.com/munificent/game-programming-patterns/master/book/event-queue.markdown) · [Parent, GoingNative 2013](https://learn.microsoft.com/en-us/shows/goingnative-2013/inheritance-base-class-of-evil) · [Acton, CppCon 2014](https://www.youtube.com/watch?v=rX0ItVEVjHc) · [Godot Node documentation](https://docs.godotengine.org/en/stable/classes/class_node.html)
- [Node C++ implementation](https://github.com/godotengine/godot/blob/master/scene/main/node.cpp) · [O3DE component contract](https://docs.o3de.org/docs/user-guide/programming/components/create-component/)
- [Unreal Modules](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-modules) · [CMake target linking contract](https://cmake.org/cmake/help/latest/command/target_link_libraries.html) · [Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine) · [Game Features](https://dev.epicgames.com/documentation/en-us/unreal-engine/game-features-and-modular-gameplay-in-unreal-engine) · [Game Feature Action lifecycle](https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/GameFeatures/UGameFeatureAction)
- [Flecs Quickstart](https://www.flecs.dev/flecs/Quickstart.html) · [EnTT developer talk](https://skypjack.github.io/pdf/the_cpp_of_entt.pdf) · [MassEntity documentation](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-entity-in-unreal-engine?lang=en-US) · [Gameplay Framework Quick Reference](https://dev.epicgames.com/documentation/unreal-engine/gameplay-framework-quick-reference-in-unreal-engine?lang=en-US) · [Lyra ability initialization](https://dev.epicgames.com/documentation/unreal-engine/abilities-in-lyra-in-unreal-engine?lang=en-US#how-are-lyra-characters-initialized)
- [Subsystems](https://dev.epicgames.com/documentation/en-us/unreal-engine/programming-subsystems-in-unreal-engine?lang=en-US) · [Object Pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine?lang=en-US) · [Actor Lifecycle](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-actor-lifecycle)
- [Unreal Automation Test Framework](https://dev.epicgames.com/documentation/unreal-engine/automation-test-framework-in-unreal-engine?lang=en-US) · [Testing networked games](https://dev.epicgames.com/documentation/en-us/unreal-engine/testing-and-debugging-networked-games-in-unreal-engine)

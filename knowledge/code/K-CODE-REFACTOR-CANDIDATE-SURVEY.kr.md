---
id: K-CODE-REFACTOR-CANDIDATE-SURVEY
title: 큰 게임 코드베이스에서 작고 효과 큰 리팩터링 후보를 찾는 방법
summary: 소스 트리를 영역별로 나누고, 영역마다 정해 둔 구체적 신호(갈라진 복사본, 핫패스의 쓰지 않는 복사, 큰 구조체 값 전달, 디버그 전용 틱, 세션 상태를 쥔 프로세스 수명 static, 우회된 헬퍼)를 찾은 뒤, 모든 결과를 코드에서 확인하고 노력 대비 효과로 순위를 매긴다. 스타일만 고치는 일괄 작업과 길이만 근거인 지적은 낮게 둔다.
kind: method
scope: 큰 C++ 게임 프로젝트, 특히 Unreal Engine에서 리팩터링 후보를 읽기 전용으로 찾는 일. 신호는 질문을 찾아 줄 뿐이며, 선택한 변경의 동작 테스트를 대신하지 않는다
keywords: [refactoring candidates, code survey, duplication, copy divergence, dead code, hot path, pass by value, TFunctionRef, FGameplayEventData, bAllowTickOnDedicatedServer, bCanEverTick, AActor::Tick, RegisterTickFunction, NM_DedicatedServer, empty tick, function-local static, static storage duration, PIE, 리팩터링 후보, 중복 코드, 복사본 불일치, 핫패스]
status: active
checked_at: "2026-11-27"
context:
  engine: Unreal Engine 5.8
  language: C++20
relations:
  requires: [K-CODE-ABSTRACTION-COST, K-CODE-MAINTAINABILITY-EVIDENCE]
---

# 큰 게임 코드베이스에서 작고 효과 큰 리팩터링 후보를 찾는 방법

## 지침

소스 트리를 서로 독립된 몇 개 영역(예: 능력 시스템, AI와 스폰, UI와 데이터, 아이템과 서비스)으로 나누고 병렬로 조사한다. 각 조사에 프로젝트 코딩 규약과 같은 신호 목록을 준다. 주장마다 파일과 줄을 요구하고, 확인한 뒤 버린 항목 목록도 요구한다.

작은 변경으로 구체적 효과를 가장 자주 낸 신호:

- **갈라진 복사본.** 같은 블록이 여러 곳에 있으면 복사본을 줄 단위로 비교한다. 엉뚱한 설정 변수를 읽거나, 0 검사를 빠뜨리거나, 다른 빌드 가드를 쓰는 복사본은 중복이면서 잠재 결함이므로 단순 중복보다 위에 둔다.
- **핫패스의 쓰지 않는 복사.** 큰 구조체(효과 스펙, 사용자 레코드, 퀘스트 배열)를 복사하고 읽지 않는 지역 변수, 또는 타격마다나 프레임마다 도는 함수의 큰 구조체 값 전달 매개변수. Unreal에서 `FGameplayEventData`와 `FGameplayTagContainer`를 값으로 넘기면 복사 때 메모리를 할당한다. 동기 콜백 매개변수는 값 전달 `TFunction` 대신 `TFunctionRef`로 둘 수 있다.
- **디버그 전용 틱.** 콘솔 변수가 켜졌을 때 디버그 오버레이를 그리려고만 `bCanEverTick`을 켠 컴포넌트는, 틱이 허용된 곳에서 인스턴스마다 틱 하나씩 비용을 낸다. 틱을 디버그 빌드 플래그로 감싸고, 클라이언트 전용 작업이면 `bAllowTickOnDedicatedServer`를 false로 둔다. `PrimaryComponentTick` 설정은 클래스 계층의 모든 생성자가 쓰므로, 어느 머신이 틱하는지 주장하기 전에 기반 클래스 생성자를 읽는다. 프로젝트 기반 컴포넌트가 이미 `bAllowTickOnDedicatedServer`를 false로 두었을 수 있고, 그러면 서버 쪽 효과는 사라진다. 엔진은 틱 함수를 등록할 때 월드의 넷 모드를 검사해 `bAllowTickOnDedicatedServer`를 적용하므로, 에디터 플레이의 데디케이티드 서버 월드도 이 설정을 따른다.
- **빈 액터 틱.** 네이티브 C++ 액터 클래스에서 `AActor::Tick`은 Blueprint로 만든 클래스나 네이티브가 아닌 클래스일 때만 Blueprint `ReceiveTick`과 잠복 액션을 실행한다. 따라서 `Super::Tick`만 부르는 오버라이드는 네이티브 클래스에서 아무 일도 하지 않지만, `bCanEverTick`이 true면 틱 함수는 여전히 등록된다. 스폰되는 Blueprint 하위 클래스가 없고 틱을 켜는 곳이 없음을 확인했다면 오버라이드와 틱 플래그를 지워도 안전하다.
- **프로세스 수명 상태.** 함수 안 `static`은 정적 저장 기간을 가지므로 프로세스가 끝날 때까지 산다. 한 프로세스에서 플레이 세션을 여러 번 돌리는 에디터에서는, 세션마다 생기는 객체 안의 `static bool bEnded` 때문에 두 번째 세션이 종료 경로를 건너뛴다. 소유 인스턴스의 멤버로 바꾸면 고쳐진다.
- **우회된 헬퍼와 반복 선형 탐색.** 기존 헬퍼 본문을 되풀이하는 호출처, 또는 같은 컨테이너를 도는 루프 안에서 항목마다 하는 선형 탐색.

노력 대비 효과와 위험으로 순위를 매긴다. 길이만, 표 모양 함수, 프로젝트 전체 스타일 일괄 작업은 낮게 둔다. 공용 위젯의 갱신 시점을 바꾸는 변경은 작아도 위험이 높은 쪽에 둔다.

## 적용 범위와 예외

리플렉션이나 비주얼 스크립팅이 함수를 부를 수 있으면 참조 수 0은 죽은 코드의 증거가 아니다. 그런 함수는 미확인으로 보고한다. 엔진 생성 코드나 프로토콜 생성 코드, 전송 형식, 안티치트 경로는 좋지 않은 후보다. 갈라진 복사본은 의도일 수 있으니 합치기 전에 담당자에게 확인한다. 프로세스 수명 static은 프로세스 하나에 세션 하나를 돌리는 데디케이티드 서버에서는 해가 없으므로, 효과는 에디터와 자동화 실행에 있다.

## 점검

- 보고 전에 인용한 줄을 다시 읽는다. 이 작업의 한 조사는 쓰지 않는 함수 검사를 중간에 멈췄고 그 사실을 밝혀서, 불완전한 주장이 순위에 들어가지 않았다.
- 핫패스 주장에는 그 경로를 뜨겁게 만드는 호출처를 적는다.
- 갈라진 복사본에는 어느 쪽이 의도한 규칙인지 적는다.
- 후보마다 변경 뒤 테스트할 동작을 적는다.
- 틱 주장에는 모든 기반 클래스 생성자를 따라 `PrimaryComponentTick`(또는 `PrimaryActorTick`) 대입을 추적하고, 아직 그 틱에 기대는 곳을 확인한다: 하위 클래스, Event Tick이 있는 Blueprint 하위 클래스, `SetComponentTickEnabled` 호출, 틱 선행 조건.
- 빌드 플래그로 감쌀 때는 그 플래그가 타깃별, 빌드 파이프라인별로 어떻게 정해지는지 읽는다. 에디터 밖에서 기본값이 꺼진 플래그도 빌드 서버가 내부 빌드에서 켤 수 있고, 그것이 디버그 기능이 남는 곳을 정한다.

## 근거

- 작업 확인 2026-11-26: 약 100만 줄 규모 Unreal Engine 5 게임 소스 트리를 읽기 전용 조사 네 개로 병렬 조사해 후보 32개를 얻었다. 그중 12개를 인용 줄에 대고 직접 다시 확인했다(갈라진 물 탈출 설정 변수, 두 주문 시전 클래스의 서로 다른 빌드 가드, 체력 변화마다 생기는 쓰지 않는 효과 스펙 복사, 디버그 전용 장비 틱, 빈 풀 매니저 틱, 프로세스 수명 게임 종료 플래그, 피해 이벤트마다 생기는 퀘스트 배열 복사, 항목마다 하는 선형 슬롯 탐색, 참조 없는 유틸리티 함수, 커서 재중앙 블록 복사본 7개). 변경을 구현하거나 측정하지는 않았다.
- 작업 확인 2026-11-26(디버그 전용 장비 틱의 후속 구현): 조사는 그 틱이 데디케이티드 서버에서도 돈다고 주장했다. 프로젝트 기반 컴포넌트 생성자가 이미 `bAllowTickOnDedicatedServer`를 false로 두었으므로, 지울 것은 클라이언트 틱뿐이었다. 감싼 변경은 에디터 타깃(플래그 켬)과 게임 Development 타깃(플래그 끔)에서 빌드되었다. 조사가 파생 클래스 생성자만 읽어서 이를 놓쳤다.
- 작업 확인 2026-11-27(두 번째 후속, 빈 풀 매니저 액터 틱과 디버그 전용 루팅 컴포넌트 틱): 컴포넌트에서 같은 조사 누락이 다시 나왔다. 기반 생성자가 데디케이티드 서버 틱을 이미 껐으므로, 변경 전에 서버 쪽 효과 주장을 뺐다. 게임 모드가 모든 던전 서버에서 스폰하는 풀 매니저 액터는 서버에서 실제로 틱했다. 두 변경 모두 에디터 타깃(플래그 켬)과 게임 Development 타깃(플래그 끔)에서 빌드되었고, 기존 루팅 자동화 테스트(네트워크 에디터 플레이 8건, 기본과 높은 지연)가 통과했다. 콘텐츠 전체 이름 검색과 Blueprint 텍스트 렌더로 두 클래스의 Blueprint 하위 클래스나 틱 오버라이드가 없음을 확인했다. 프레임 비용은 측정하지 않았다.
- 등록 확인: Unreal Engine 5.8 `Engine/Source/Runtime/Engine/Private/TickTaskManager.cpp` 2412줄, `FTickFunction::RegisterTickFunction`은 `bAllowTickOnDedicatedServer || !(World && World->IsNetMode(NM_DedicatedServer))`를 검사한다.
- 네이티브 액터 틱: Unreal Engine 5.8 `Engine/Source/Runtime/Engine/Private/Actor.cpp` 2006-2028줄, `AActor::Tick`은 클래스가 Blueprint에서 컴파일되었거나 네이티브가 아닐 때만 `ReceiveTick`을 부르고 잠복 액션을 처리한다.
- `TFunctionRef` 선언: Unreal Engine 5.8 `Engine/Source/Runtime/Core/Public/Templates/Function.h` 556줄.
- `bAllowTickOnDedicatedServer` 선언: Unreal Engine 5.8 `Engine/Source/Runtime/Engine/Classes/Engine/EngineBaseTypes.h` 221줄(`FTickFunction`).
- 블록 범위 `static` 변수의 정적 저장 기간: C++ 표준 초안 [basic.stc.static], [stmt.dcl], https://eel.is/c++draft/basic.stc.static.

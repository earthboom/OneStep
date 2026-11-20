---
id: K-CODE-UE-GAS-CUE-EXECUTE-VS-ADD
title: Unreal GAS 에서 한 번 일어나는 사건은 ExecuteGameplayCue, 지속되는 상태는 AddGameplayCue 로 고른다
summary: ExecuteGameplayCue 는 Executed 이벤트 하나를 신뢰성 없는 멀티캐스트로 보내고 아무것도 저장하지 않으므로, 늦게 들어오거나 관련성 밖에 있던 클라이언트는 보지 못한다. AddGameplayCue 는 큐를 복제되는 컨테이너에 저장하고 큐 태그도 부여하므로 관련성 변화에도 살아남지만 반드시 제거해야 하며, RemoveGameplayCue 한 번은 그 태그의 항목을 모두 지운다.
kind: reference
scope: 네트워크 게임에서 어빌리티나 액터가 호출하는 Unreal Engine 5 GameplayAbilities 플러그인의 UAbilitySystemComponent 큐 API
keywords: [GameplayCue, ExecuteGameplayCue, AddGameplayCue, RemoveGameplayCue, AddGameplayCue_MinimalReplication, FActiveGameplayCueContainer, NetMulticast, prediction key, IsLocalClientKey, WhileActive, OnActive, Executed, Removed, late join, relevancy]
status: active
checked_at: "2026-11-20"
context:
  engine: Unreal Engine 5.8 (release/5.8.0p5 소스)
---

## Guidance

연출이 얼마나 오래 보이는지가 아니라 무엇을 나타내는지로 API 를 고른다.

- **한 번 일어나는 사건**(피격 스파크, 충돌음, 카메라 흔들림, 시전 섬광): `ExecuteGameplayCue`. 권한 측이 `UGameplayCueManager` 에 큐를 쌓고, `FlushPendingCues` 가 신뢰성 없는 멀티캐스트 `NetMulticast_InvokeGameplayCueExecuted_WithParams` 로 보낸다. 저장되는 것도, 부여되는 태그도 없다. 그 순간 관련성이 없거나, 나중에 들어오거나, 패킷을 잃은 클라이언트는 보지 못하며, 사건이라면 이것이 맞는 결과다.
- **지속되는 상태**(버프 오라, 채널링 루프, 클라이언트가 관련성을 얻었을 때도 보여야 하는 부착 효과): `AddGameplayCue` 와 짝이 되는 `RemoveGameplayCue`. 권한 측은 `ActiveGameplayCues`(fast array)에 항목을 추가하고, 소유자 태그 맵에서 큐 태그 수를 올리고, `OnActive` 용 신뢰성 없는 멀티캐스트 `NetMulticast_InvokeGameplayCueAdded_WithParams` 를 보내고, 자기 쪽에서 `WhileActive` 를 실행한다. 클라이언트는 `PostReplicatedAdd` 에서 `WhileActive` 를, `PreReplicatedRemove` 에서 `Removed` 를 받으므로, 나중에 관련성을 얻은 클라이언트도 큐를 시작한다(`OnActive` 가 아니라 `WhileActive` 를 받는다).

예측은 둘이 같다. 권한이 없는 머신에서 각 호출은 범위 안의 예측 키가 `IsLocalClientKey()` 일 때만 로컬 작업을 한다. Execute 는 `Executed` 를 로컬에서 실행하고, Add 는 `PredictiveAdd` 와 로컬 `OnActive`, `WhileActive` 를 실행한다. 서버가 보낸 사본은 같은 키를 가지고 있어 받는 클라이언트가 건너뛰므로 두 번 재생되지 않는다. 로컬 키가 없으면 클라이언트 호출은 아무것도 하지 않는다.

## Applicability and exceptions

- `AddGameplayCue` 는 중복을 없애지 않는다. 같은 태그를 두 번 추가하면 항목이 두 개 생기고, 권한 측에서 두 번째 추가는 `WhileActive` 를 다시 실행하지 않으며, `RemoveGameplayCue` 한 번이 그 태그의 항목을 모두 지운다. 두 주체가 한 큐 태그를 공유할 수 있으면 게임 코드에서 참조 수를 센다.
- 추가된 큐 태그는 ASC 의 소유 게임플레이 태그로 집계되므로 태그 질의나 어빌리티 차단 규칙이 그것을 본다. 실행된 큐는 태그를 남기지 않는다.
- 추가된 큐의 파라미터는 항목과 함께 복제되며, 바꾸려면 제거 후 다시 추가해야 한다. 실행된 큐의 파라미터는 한 번만 보내진다.
- `AddGameplayCue_MinimalReplication` 은 `Mixed` 모드에서 시뮬레이티드 프록시에만 복제되는 컨테이너에 큐를 저장한다. 소유 클라이언트는 복제된 게임플레이 이펙트에서 큐를 받는다고 가정한다.
- `Mixed` 복제 모드에서 엔진은 자율 프록시의 두 번 재생을 막으려고 `AddGameplayCue_Internal` 에서 RPC 예측 키를 바꾼다. 복제 프록시를 재정의하는 프로젝트는 이 규칙을 유지해야 한다.
- 게임플레이 이펙트의 `GameplayCues` 목록에서 나오는 큐는 이펙트를 따른다. 즉시 이펙트는 실행하고, 지속시간 이펙트와 무한 이펙트는 추가하고 제거한다. 직접 호출은 어떤 이펙트도 소유하지 않는 연출에만 쓴다.
- 프로젝트가 `UGameplayCueManager::HandleGameplayCue` 를 직접 부르는 로컬 전용 헬퍼를 둘 수 있다. 이것은 ASC 컨테이너를 완전히 건너뛴다. 태그도, 복제도, 서버가 나중에 보내는 `Removed` 도 없으므로, 로컬 측이 추가한 것은 로컬 측이 제거해야 한다.

## Checks

- 큐마다 묻는다. 1초 뒤에 관련성을 얻은 클라이언트가 이것을 봐야 하는가? 그렇다면 Add/Remove, 아니라면 Execute 다.
- `AddGameplayCue` 마다 모든 종료 경로(어빌리티 종료, 취소, 소유자 사망, 액터 파괴)에서 `RemoveGameplayCue` 를 찾는다.
- 클라이언트가 어느 API 든 부를 때 로컬 예측 키가 범위 안에 있는지(활성 예측 창) 확인한다. 아니면 그 클라이언트에서 호출이 조용히 버려진다.
- 제거 한 번에 기대기 전에 같은 큐 태그를 둘 이상의 주체가 추가하는지 검색한다.

## Evidence

2026-11-20 에 UE 5.8 릴리스 소스의 `Engine/Plugins/Runtime/GameplayAbilities/Source/GameplayAbilities` 플러그인에서 읽었다.

- `Private/AbilitySystemComponent.cpp`: `ExecuteGameplayCue` 는 `ScopedPredictionKey` 와 함께 큐 매니저로 넘긴다. `AddGameplayCue_Internal` 의 권한 분기(`AddCue`, Mixed 모드 키 교체, `Call_InvokeGameplayCueAdded_WithParams`, 태그가 목록에 없었을 때만 로컬 `WhileActive`)와 `IsLocalClientKey` 분기(`PredictiveAdd`, 로컬 `OnActive` 와 `WhileActive`). `RemoveGameplayCue_Internal`. 로컬 클라이언트 키를 건너뛰는 멀티캐스트 구현.
- `Public/AbilitySystemComponent.h`: `NetMulticast_InvokeGameplayCueExecuted_WithParams` 와 `NetMulticast_InvokeGameplayCueAdded_WithParams` 는 `NetMulticast, unreliable` 로 선언된다.
- `Private/GameplayCueManager.cpp`: `InvokeGameplayCueExecuted_WithParams`, `AddPendingCueExecuteInternal`, `FlushPendingCues`(권한 측은 멀티캐스트를 보내고, 로컬 키가 있는 클라이언트는 `Executed` 를 로컬에서 실행한다).
- `Private/GameplayCueInterface.cpp`: `FActiveGameplayCueContainer::AddCue`(새 항목, `UpdateTagMap` +1), `RemoveCue`(태그의 항목을 모두 지우고 항목마다 `Removed`), `PredictiveAdd`, `PredictiveRemove`, `FActiveGameplayCue::PostReplicatedAdd` 와 `PreReplicatedRemove`.

복제 큐 헬퍼와 로컬 전용 큐 헬퍼를 나눠 둔 한 스튜디오 프로젝트에 적용했다. 프로젝트 고유 규칙은 그 프로젝트의 문서에 남긴다.

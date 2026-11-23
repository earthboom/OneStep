# 언리얼 FTimerManager: 돌고 있는 핸들을 다시 설정하면 생기는 일, SetTimerForNextTick 과의 차이, 소유자보다 오래 사는 타이머

> 이 문서는 `K-CODE-UE-TIMER-MANAGER.md` 의 사람용 번역이다. 정본은 영어 원문이다.

- **요약:** 아직 살아 있는 타이머를 가리키는 핸들로 `SetTimer` 를 부르면 그 타이머를 지우고 새 핸들 값으로 새 타이머를 만든다. 주기가 0 이하이면 지우기만 한다. `SetTimerForNextTick` 은 핸들을 받지 않고 다음 타이머 매니저 틱에 돌며, 그 틱이 같은 프레임 뒤쪽일 수 있다. 엔진 코드는 액터의 EndPlay 나 파괴 때 타이머를 지우지 않으므로 정리 여부는 델리게이트 종류에 달려 있다.
- **종류:** reference
- **범위:** 게임 스레드에서 `UWorld::GetTimerManager` 나 `AActor::GetWorldTimerManager` 로 쓰는 Unreal Engine 5 FTimerManager, 네이티브 C++ 타이머와 블루프린트 이벤트·함수 타이머 노드
- **상태:** active, 확인일 2026-11-20
- **조건:** Unreal Engine 5.8 (release/5.8.0p5 소스)

## 지침

**이미 돌고 있는 핸들을 다시 설정할 때.** `SetTimer(Handle, ...)` 은 먼저 핸들을 찾는다. 아직 살아 있는 타이머를 가리키면 그 타이머를 지운 뒤 새 타이머를 더하고, 핸들을 새 인덱스와 일련번호로 덮어쓴다. 남는 것은 없다. 카운트다운은 새 주기로 처음부터 다시 시작하고, 옛 델리게이트와 그 페이로드는 버려지며, 옛 핸들 값의 복사본은 더는 아무 타이머와도 맞지 않는다. 그래서 "같은 멤버 핸들로 SetTimer 를 다시 부르기"가 재시작이나 디바운스의 표준 방법이다. 주기가 0 이하이면 핸들을 지우고 무효로 만들기만 하며 델리게이트는 부르지 않는다. 다른 핸들 변수로 건 타이머는 서로 독립이므로, 버린 지역 `FTimerHandle` 의 타이머는 취소할 수 없고 반복 호출은 쌓인다.

타이머 자신의 콜백 안에서 다시 거는 것은 안전하다. 실행 중인 타이머는 제거되고 그 타이머의 반복 실행 루프는 멈추며, 새 타이머는 평소대로 예약된다.

**지운 타이머.** 활성 타이머에 `ClearTimer` 를 부르면 `ActivePendingRemoval` 표시만 하고 항목은 틱 안에서 나중에 제거된다. 조회 함수는 이미 없는 것으로 다루므로 `IsTimerActive` 는 바로 거짓이 된다.

**SetTimerForNextTick.** 부를 때마다 새 핸들을 돌려주고 핸들 인자가 없으므로 앞선 요청을 대체하지 않는다. 호출하는 쪽이 저장해 둔 이전 핸들을 지우지 않으면 두 번 부른 만큼 두 번 돈다. 기본값 `TimerManager.GuaranteeEngineTickDelay=0` 에서는 현재 타이머 시계로 활성 상태가 되고, 시간을 앞으로 보내는 다음 `FTimerManager::Tick` 에서 발동한다. `UWorld::Tick` 은 타이머 틱을 `TG_PostPhysics` 뒤, `TG_PostUpdateWork` 앞에서 돌린다. 그래서 한 프레임에서 그 지점보다 앞서 낸 요청(네트워크 수신, post physics 까지의 틱 그룹)은 같은 프레임 뒤쪽에서 돌고, 타이머 콜백 안이나 타이머 틱 뒤에서 낸 요청은 다음 프레임에 돈다. 이 CVar 를 1 로 두면 타이머 틱 전에 낸 요청도 엔진 프레임 경계를 반드시 넘는다. 타이머 틱 전에 건 일반 `SetTimer` 는 대기 상태로 들어가 건 프레임에는 절대 발동하지 않는다.

**소유자 파괴.** 이 엔진 버전에서 `AActor::EndPlay` 와 액터 파괴는 `ClearAllTimersForObject` 를 부르지 않는다. 결과는 델리게이트에 따라 다르다.

| 델리게이트 | 실행 전 약한 참조 검사 | `ClearAllTimersForObject(Object)` 의 키 |
| --- | --- | --- |
| UObject 의 메서드 (`SetTimer(Handle, this, &Method)`, `CreateUObject`, `BindUObject`) | 있다. 파괴되었거나 garbage 인 객체면 아무 일도 하지 않고, 반복 타이머는 다음 발동 때 제거된다. | 있다, 그 객체로 |
| 다이내믹 델리게이트 (블루프린트 타이머, `CreateUFunction`) | 있다 | 있다, 그 객체로 |
| `CreateWeakLambda(Context, ...)` | 컨텍스트 객체만 검사한다 | 있다, 타이머를 건 클래스가 아니라 컨텍스트 객체로 |
| `CreateLambda`, 원시 `TFunction` 람다, `CreateRaw` | 없다. 만료되면 무조건 돈다. | 없다. `ClearAllTimersForObject` 가 보지 못한다. |

엔진 소유자 두 곳은 타이머를 지운다. `UGameplayAbility::EndAbility` 는 `AbilitySystem.ClearAbilityTimers` 가 1(기본값)인 동안 `ClearAllTimersForObject(this)` 를 부르고, `UUserWidget::CancelLatentActions` 는 불렸을 때 그렇게 한다. `UWorld::GetTimerManager` 는 게임 인스턴스가 있으면 게임 인스턴스의 타이머 매니저를 돌려주므로, 지우지 않은 타이머는 그것을 건 월드보다 오래 살아 레벨 전환 뒤에 발동할 수 있다.

## 적용 범위와 예외

- 기본 타이머 경로에서 확인했다. AutoRTFM 트랜잭션 타이머가 켜져 있으면 닫힌 트랜잭션 안의 설정과 지우기는 커밋이나 중단까지 미뤄진다.
- 약한 참조 검사는 바인딩된 객체만 확인한다. 페이로드나 람다 캡처에 복사된 다른 UObject 는 보호받지 않는다. `this` 에 바인딩한 약한 람다 안에서 `[this]` 나 지역 변수를 참조로 캡처하는 것은 캡처된 모든 객체가 `this` 이상 살아 있을 때만 안전하다.
- 소유자가 죽은 약한 바인딩 단발 타이머는 일찍 제거되지 않는다. 만료될 때까지 남아 있다가 아무 일도 하지 않고 끝난다.
- `SetTimerForNextTick` 은 네트워크 전송 경계가 아니다. 같은 프레임에 요청한 RPC 와 파괴가 여전히 같은 전송으로 나갈 수 있다.
- 엔진의 대기 어빌리티 태스크는 지속시간이 0 이하이면 `SetTimerForNextTick` 으로 바꾼다. 그런 지속시간을 `SetTimer` 에 그대로 넘기는 래퍼는 끝나지 않는다.

## 점검

- 각 `SetTimer` 마다 두 번째 호출이 재시작해야 하는지, 무시해야 하는지(`IsTimerActive` 로 막기), 나란히 돌아야 하는지(핸들 분리) 정한다. 서로 다른 용도에 같은 멤버 핸들을 넘기면 두 번째 호출이 첫 번째를 조용히 취소한다.
- 데이터나 콘솔 변수에서 오는 주기마다, 0 이하인 경우에도 콜백을 부르거나 명시적으로 건너뛰는지 확인한다.
- 각 `SetTimerForNextTick` 마다 호출하는 쪽에 필요한 것이 "이 프레임 틱 그룹 뒤"(타이머 틱 전에 낸 요청이면 성립)인지 "프레임 경계 뒤"(CVar, 타이머 틱 뒤에 만든 타이머, 다른 수단이 필요)인지 따진다. 요청이 반복될 수 있으면 돌려받은 핸들을 저장하고 지운다.
- 람다나 원시 델리게이트마다 캡처한 포인터를 나열하고, 모든 종료 경로에서 그 타이머를 지우는 코드를 찾는다. `ClearAllTimersForObject` 와 어빌리티 종료는 지우지 않는다.
- 핸들을 버린 반복 타이머마다 소유자가 파괴될 때까지 도는 것이 의도인지 확인한다.

## 근거

2026-11-20 UE 5.8 릴리스 소스에서 읽었다.

- `Engine/Source/Runtime/Engine/Private/TimerManager.cpp`: `InternalSetTimer`(조회, 지우기, 주기 검사, `HasBeenTickedThisFrame` 에 따른 대기·활성), `InternalSetTimerForNextTick`(`GuaranteeEngineTickDelay`, `ExpireTime = InternalTime`), `InternalClearTimer`(`Executing` 을 포함한 상태별 처리), `InternalClearAllTimers`(`ObjectToTimers` 사용), `AddTimer`(`GetBoundObject` 로 만든 키), `Tick`(엄격한 `InternalTime > ExpireTime`, `!bRequiresDelegate || IsBound()` 일 때만 반복 재예약, 끝에서 대기 타이머 승격), `FTimerUnifiedDelegate::IsBound`, `GetBoundObject`, `Execute`.
- `Engine/Source/Runtime/Engine/Public/TimerManager.h`: `ClearTimer`, `ClearAllTimersForObject`, `FTimerData::bRequiresDelegate`.
- `Engine/Source/Runtime/Core/Public/Delegates/DelegateInstancesImpl.h`: 함수 객체(람다) 인스턴스의 `GetObjectForTimerManager` 는 null, 약한 함수 객체 인스턴스는 컨텍스트 객체를 돌려준다. UObject, 약한 람다, 원시 인스턴스의 `IsSafeToExecute`.
- `Engine/Source/Runtime/Engine/Private/LevelTick.cpp`: `GetTimerManager().Tick` 앞뒤 틱 그룹 순서.
- `Engine/Source/Runtime/Engine/Private/Actor.cpp`: `AActor::EndPlay` 에 타이머 정리가 없다. `Engine/Source/Runtime/Engine/Private/World.cpp`: `UWorld::GetTimerManager`.
- `Engine/Plugins/Runtime/GameplayAbilities/Source/GameplayAbilities/Private/Abilities/GameplayAbility.cpp`: `FAbilitySystemTweaks::ClearAbilityTimers` 와 `EndAbility` 의 호출. `Private/Abilities/Tasks/AbilityTask_WaitDelay.cpp`: 지속시간 0 분기. `Engine/Source/Runtime/UMG/Private/UserWidget.cpp`: `CancelLatentActions`.

소스 읽기만 했고 런타임 시험은 하지 않았다. 한 스튜디오 프로젝트의 읽기 전용 리뷰에 적용했고, 거기서 공유 핸들 취소와 0 분기가 없는 대기 래퍼를 설명했다. 프로젝트 발견 사항은 그 프로젝트에 남긴다.

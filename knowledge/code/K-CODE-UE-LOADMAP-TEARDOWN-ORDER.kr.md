---
id: K-CODE-UE-LOADMAP-TEARDOWN-ORDER
title: 언리얼 맵 로드 중 액터 EndPlay가 실행될 때 아직 남아 있는 것, 그리고 그때 UUserWidget::GetOwningPlayer가 null인 이유
summary: UEngine::LoadMap은 이전 월드를 해체 중으로 표시한 뒤 각 로컬 PlayerController와 그 폰을 파괴하고 LocalPlayer->PlayerController를 비우며, 그다음에야 UWorld::EndPlay를 호출한다. 그래서 액터 EndPlay에서 도달하는 코드(위젯에 브로드캐스트하는 델리게이트 포함)는 GetOwningPlayer()가 nullptr를 반환하는 상황을 만나지만, 위젯 자체와 UUserWidget::GetWorld()는 여전히 유효하다.
kind: reference
scope: UEngine::LoadMap을 거치는 언리얼 엔진 5 클라이언트 맵 로드(비심리스 이동과 새 맵으로의 이동); 액터 EndPlay에서 브로드캐스트되는 매니저 이벤트에 반응하는 UMG 위젯; 심리스 트래블과 PIE 종료는 확인하지 않음
keywords: [UEngine::LoadMap, UWorld::EndPlay, EEndPlayReason::LevelTransition, UWorld::BeginTearingDown, bIsTearingDown, ULocalPlayer::PlayerController, FLocalPlayerContext::IsValid, UUserWidget::GetOwningPlayer, UUserWidget::GetWorld, AActor::EndPlay, map travel, level transition, teardown order, null PlayerController, null dereference crash, loading screen crash]
status: active
checked_at: "2026-11-23"
context:
  engine: Unreal Engine 5.8 (custom fork source checkout)
  verification: engine source reading and one client crash matched by code reading; not reproduced at runtime
---

## Guidance

**떠나는 월드에 대한 `UEngine::LoadMap` 내부 순서.**

1. `UWorld::BeginTearingDown()`이 이전 월드에 `bIsTearingDown`을 설정한다.
2. `PlayerController`가 그 월드에 속한 모든 로컬 플레이어에 대해, 엔진은 컨트롤러의 폰을 파괴하고, 컨트롤러를 파괴하고, `LocalPlayer->PlayerController = nullptr`로 설정한다.
3. `UWorld::EndPlay(EEndPlayReason::LevelTransition)`이 실행되어 남아 있는 액터(게임 스테이트, 매니저, 아직 살아 있는 HUD 소유 액터)에 `AActor::EndPlay`를 호출한다.
4. 이어서 `UWorld::CleanupWorld()`가 실행된다.

**UMG에 미치는 결과.** `UUserWidget::GetOwningPlayer()`는 `PlayerContext.IsValid() ? PlayerContext.GetPlayerController() : nullptr`을 반환하고, `FLocalPlayerContext::IsValid()`는 `LocalPlayer->GetPlayerController(World)`가 null이 아니어야 참이 된다. 2단계 이후에는 이것이 거짓이므로, 해체가 끝날 때까지 모든 위젯의 `GetOwningPlayer()`는 `nullptr`이다. 위젯 객체 자체는 아직 살아 있고 `UUserWidget::GetWorld()`도 이전 월드를 계속 반환한다. 목록(플레이어, 파티원, 인벤토리)을 비우면서 항목별 제거 이벤트를 브로드캐스트하는 액터 `EndPlay`는 따라서 소유 플레이어가 없는 상태로 위젯 갱신 코드를 구동하게 된다.

**여기서 나오는 규칙.**

- 매니저 이벤트로 실행될 수 있는 위젯 코드에서는 `GetOwningPlayer()->...`를 연달아 쓰지 않는다. null 포인터에 `GetWorld()` 같은 virtual 함수를 호출하면 크래시가 난다. 월드만 필요하면 위젯 자신의 `GetWorld()`를 쓰고, 컨트롤러가 필요하면 null 검사를 한다.
- 전환 중 연출 작업을 건너뛰려면 `World->bIsTearingDown`을 검사한다. 이 값은 컨트롤러가 파괴되기 전, 어떤 `EndPlay`가 실행되기 전에 이미 참이다.
- 말단 위젯에 확인되지 않은 역참조가 몇 년 동안 숨어 있다가, 새 호출자가 해체 시점 이벤트로 그 위젯을 갱신하기 시작할 때에야 도달 가능해질 수 있다. 그런 호출자를 추가할 때는 기존 호출자들의 방어(예: 컨트롤러가 없으면 갱신을 건너뛰는 형제 위젯)와 비교한다.

## Applicability and exceptions

- 언리얼 엔진 5.8 소스에서 읽었다. 이전 UE5 버전도 같은 구조를 쓰지만, 줄 위치를 인용하기 전에 확인한다.
- 클라이언트 `LoadMap`에서 떠나는 월드를 다룬다. 심리스 트래블은 전환 동안 컨트롤러를 유지하며 확인하지 않았다. PIE 종료는 다른 경로를 따르며 확인하지 않았다.
- 데디케이티드 서버에는 로컬 플레이어가 없으므로 2단계가 적용되지 않는다.
- 엔진 포크에서는 순서가 바뀔 수 있다. 엔진 버전이 바뀌면 `UEngine::LoadMap`을 다시 읽는다.

## Checks

- 위젯이 이벤트를 구독할 때, 액터 `EndPlay`의 목록 비우기를 포함해 그 이벤트를 브로드캐스트하는 모든 위치를 나열하고 "소유 플레이어가 없는 맵 로드"를 한 가지 경우로 취급한다.
- 변경된 위젯 코드에서 null 검사 없이 쓰인 `GetOwningPlayer()->`와 `GetOwningPlayer<...>()->`를 검색한다.
- 목록 기반 위젯(멤버당 한 행)은, 제거 순서 때문에 남은 멤버가 다른 행으로 옮겨 가는 맵 전환을 실행해 본다. 새 유효 식별자를 받은 행만 전체 갱신을 하기 때문이다.

## Evidence

- 소스 확인(2026-11-23, Unreal Engine 5.8 포크 체크아웃): `Engine/Source/Runtime/Engine/Private/UnrealEngine.cpp` 16183행(`BeginTearingDown`), 16243-16250행(폰과 컨트롤러 파괴, `Player->PlayerController = nullptr`), 16259행(`EndPlay(EEndPlayReason::LevelTransition)`), 16262행(`CleanupWorld`); `Engine/Source/Runtime/Engine/Private/LocalPlayer.cpp` 98-106행(`FLocalPlayerContext::IsValid`)과 147-151행(`GetPlayerController`); `Engine/Source/Runtime/UMG/Private/UserWidget.cpp` 1487-1490행(`GetOwningPlayer`).
- 작업 확인(2026-11-23): 출시된 클라이언트가 파티원 세 명이 던전 맵을 로드하는 동안 크래시 리포트 없이 종료되었다. 콜스택이 없어 원인은 코드 읽기로 맞춰 보았다. 게임 스테이트 `EndPlay`의 파티 목록 비우기가 한 멤버를 다른 행으로 옮겼고, 새로 추가된 행 위젯이 상태 셀을 갱신했으며, 말단 셀이 `GetOwningPlayer()->GetWorld()`를 호출했다. 수정은 그 셀이 자신의 `GetWorld()`를 쓰게 바꾼 것이다. 런타임 재현은 이번 확인에서 수행하지 않았다.

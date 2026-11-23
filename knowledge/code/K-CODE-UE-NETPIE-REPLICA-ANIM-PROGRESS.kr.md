# 헤드리스 네트워크 PIE 테스트에서 시뮬레이트 프록시의 몽타주 위치가 멈춘 것처럼 보이는 이유

> 영어 원문 [K-CODE-UE-NETPIE-REPLICA-ANIM-PROGRESS.md](K-CODE-UE-NETPIE-REPLICA-ANIM-PROGRESS.md)의 번역이다. 헤더 정보: 종류 reference, 상태 active, 확인일 2026-11-23, 엔진 Unreal Engine 5.8 소스.

**요약:** 메시가 그려지지 않는 시뮬레이트 프록시는 애니메이션 갱신 빈도 최적화(URO)가 여러 프레임 동안 애니메이션 갱신을 건너뛸 수 있다. 그래서 갱신 사이에 `Montage_GetPosition`이 그대로이고, 테스트 프레임률이 낮으면 그 간격이 고정된 벽시계 정지 기준을 넘는다. 몽타주를 멈췄다고 하기 전에 `FAnimUpdateRateParameters::ShouldSkipUpdate()`가 거짓인 프레임만 센다.

**범위:** 네트워크 PIE에서 시뮬레이트 프록시의 애니메이션 진행(몽타주 위치, 구간, 노티파이)을 관찰하는 Unreal Engine 5 자동화 테스트. 특히 헤드리스나 오프스크린 실행.

## 지침

- `bEnableUpdateRateOptimizations`가 켜지면 스킨드 메시의 갱신 빈도 추적기가 프레임마다 애니메이션 갱신을 건너뛸지 정한다. 사람이 조종하지 않고 그려지지 않는 메시는 `BaseNonRenderedUpdateRate`를 써서 그 프레임 수마다 한 번 갱신한다. 건너뛴 프레임에는 애님 인스턴스가 몽타주를 진행하지 않아 `Montage_GetPosition`이 같은 값을 돌려준다.
- 헤드리스 실행(`-RenderOffscreen`)에서는 다른 플레이어의 캐릭터가 대개 그려지지 않아 모든 시뮬레이트 프록시가 그려지지 않은 빈도로 돈다. 프로젝트는 흔히 시뮬레이트 프록시의 이 빈도를 올린다. 테스트 프레임률이 느리면(높은 지연 네트워크 에뮬레이션, 한 프로세스의 여러 PIE 월드) 몇 프레임만 건너뛰어도 벽시계로 수백 밀리초를 넘는다.
- 그래서 경과 시간만 보는 정지 점검은 정상 프록시에서도 실패한다. 마지막 위치 변화 뒤 실제로 애니메이션을 갱신한 프레임(`AnimUpdateRateParams->ShouldSkipUpdate()`가 거짓이거나 URO가 꺼짐) 수를 세고, 갱신 수 2 이상과 시간 기준을 모두 넘을 때만 정지로 보고한다. 재생 속도가 0이 아니면 실제 갱신 한 번에도 위치가 바뀐다.
- 속도와 구간 단언은 그대로 둔다. 진행 점검에만 갱신을 아는 조건이 필요하다.

## 적용 범위와 예외

- 사람이 조종하는(로컬 조종) 캐릭터는 갱신 빈도 1이라 영향이 없다.
- 테스트가 프록시의 모든 프레임을 필요로 하면 시간 기준을 늘리지 말고 프로젝트의 URO 덮어쓰기나 `VisibilityBasedAnimTickOption`으로 강제한 뒤 설정을 되돌린다.
- 데디케이티드 서버는 플레이어 몽타주를 아예 진행하지 않을 수 있다. 서버 상태는 위치 대신 재생 속도 같은 복제 값으로 본다.

## 점검

- 진행 점검이 느린 프로필에서만, (갱신 빈도) x (프레임 시간)에 가까운 차이로 실패하면 게임플레이를 의심하기 전에 프록시 메시의 `bEnableUpdateRateOptimizations`와 `AnimUpdateRateParams->BaseNonRenderedUpdateRate`를 읽는다.
- 판별력을 확인한다. 재생 속도를 0으로 강제하면 갱신을 아는 점검도 실제 갱신 두 번 뒤에 실패해야 한다.

## 근거

2026-11-23에 UE 5.8 소스 `Engine/Source/Runtime/Engine`에서 읽었다.

- `Private/Components/SkinnedMeshComponent.cpp`: 갱신 빈도 추적기는 사람이 조종하면 1을, 아니면 그려지지 않을 때 `BaseNonRenderedUpdateRate`를 쓴다(295행 부근). `bSkipUpdate = ((Counter % UpdateRate) > 0)`이 6081행 부근에 있다.
- `Classes/Engine/EngineTypes.h`: `FAnimUpdateRateParameters::ShouldSkipUpdate()`가 `bSkipUpdate`를 돌려준다(2858행 부근). `BaseNonRenderedUpdateRate`는 2768행 부근에 선언되어 있다.

런타임, 한 스튜디오 프로젝트, 2026-11-23: 헤드리스 네트워크 PIE 테스트가 관전자 쪽 사본의 루프 몽타주 진행을 확인했다. 0.25초 벽시계 정지 기준이 높은 지연 프로필에서만 실패했다("위치가 0.26초 그대로"). 프로젝트는 시뮬레이트 프록시에 `BaseNonRenderedUpdateRate = 8`을 둔다. 점검이 갱신된 프레임만 세게 바꾼 뒤 같은 묶음이 기본 프로필과 높은 지연 프로필 모두에서 통과했다. 속도 0 판별력은 코드로 추적했고 실행하지 않았다.

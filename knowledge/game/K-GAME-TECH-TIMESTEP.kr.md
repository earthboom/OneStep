# 시뮬레이션 고정 스텝과 화면 보간 분리하기

**K-GAME-TECH-TIMESTEP** · 경과 시간을 누적하고 고정 간격으로 시뮬레이션을 진행한다. 밀린 스텝의 처리 예산을 정하고 권위 상태와 화면 보간을 분리한다.

## 지침

누산기(accumulator)는 아직 시뮬레이션하지 않은 경과 시간을 보관한다. 고정 간격 h가 쌓일 때마다 상태를 갱신하고 h를 뺀다. 프레임당 처리 한도에 닿았을 때 남은 시간을 어떻게 처리할지 정한다. 반암시적 오일러는 속도를 먼저 갱신한 뒤 위치에 사용하고 명시적 오일러는 이전 속도를 사용한다. 위치의 소수부를 보존하면 정수 픽셀 화면에서도 서브픽셀 이동을 누적할 수 있다.

## 적용 조건과 예외

고정 스텝 모델에서 잔여 시간이 h보다 작으면 alpha=잔여 시간/h로 직전과 현재 트랜스폼을 보간한다. 화면은 경과 시간 기준 궤적보다 약 한 시뮬레이션 틱 늦다. 충돌과 입력은 시뮬레이션 시계를 사용한다. 과부하가 지속되면 시간 폐기, 느린 진행 또는 처리 용량 확보 정책을 정해야 한다.

## 확인 방법

같은 시각의 명령을 다른 렌더 주기와 긴 프레임에서 재생한다. 유입 시간과 시뮬레이션 시간·잔여 시간·폐기 시간을 대조한다. 점프별 정점과 착지 시각을 비교한다. 바닥 허용 오차를 적용할 때는 작은 상승을 착지로 오인하지 않도록 하강 여부도 본다.

## 근거

Fiedler는 누산기 스케줄과 적분 방법을 설명한다. Thorson은 정수 충돌 모델의 소수 이동량을 기록했다. 과거 스크립트 이동 검사에서는 유한 지연 후의 밀린 스텝 처리와 화면 보간을 확인했다. 엔진 전체 물리 결정성, 실제 표시 완료까지의 복구 시간, 네트워크 재생은 검증하지 않았다.

- [Glenn Fiedler — Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)
- [Glenn Fiedler — Integration Basics](https://gafferongames.com/post/integration_basics/)
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html)

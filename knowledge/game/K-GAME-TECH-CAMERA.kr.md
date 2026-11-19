# 데드존과 시간에 따른 감쇠로 추적 카메라 구성하기

**K-GAME-TECH-CAMERA** · 화면 구도에 맞는 추적점을 정하고, 고정 표적에 대한 수렴 속도를 유지하려면 경과 시간으로 감쇠를 계산한다.

## 지침

데드존은 피사체가 화면의 정해진 영역을 벗어날 때 추적을 시작한다. 룩어헤드는 예상 이동 방향으로 목표점을 옮긴다. 한 구간 동안 목표가 고정되면 현재 위치에 `(target - position) * (1 - exp(-lambda * dt))`를 더한다. `lambda`는 초당 감쇠율이다. 같은 구간을 나누어도 반올림 오차를 제외하면 같은 위치에 도달한다. 속도나 오버슈트를 표현하려면 감쇠 스프링을 고려한다.

## 적용 조건과 예외

피사체가 움직이면 목표점 샘플링 오차가 생긴다. 언리얼 엔진의 `UCameraComponent`는 시점과 투영 설정을 제공한다. 카메라 트랜스폼을 부드럽게 이동할 때도 충돌, 순간 이동, 구도 전환 규칙이 필요하다.

## 확인 방법

고정 목표에 불규칙한 시간 간격과 0초 간격을 적용하고 같은 경과 시간에서 변위를 비교한다. 움직이는 피사체의 급반전, 가림, 순간 이동, 화면비 변화는 실제 표시 주기와 함께 확인한다.

## 근거

Keren은 화면 구도를, Juckett은 감쇠 스프링 응답을 설명한다. 과거 Unity와 Unreal 검사는 고정 목표에 대한 수렴을 확인했다. 이동 중의 체감과 카메라 충돌은 별도 확인이 필요하다.

- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers)
- [Ryan Juckett — Damped Springs](https://www.ryanjuckett.com/damped-springs/)
- [Epic — UCameraComponent](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/Camera/UCameraComponent?application_version=5.5)

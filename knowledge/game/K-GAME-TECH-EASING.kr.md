# 시간 곡선의 끝점·중단·역재생 정책 정하기

**K-GAME-TECH-EASING** · 정규화한 경과 시간으로 유한 전환을 계산하고, 중단될 때 위치·속도·완료 이벤트가 어떻게 변하는지 정한다.

## 지침

기간이 양수이면 경과 시간/기간을 [0,1]로 제한하고 곡선을 평가해 양 끝값을 보간한다. 선형 보간은 속도가 일정하다. `smoothstep`은 3t²−2t³으로 양 끝 기울기가 0이다. Perlin의 5차 `smootherstep`은 끝점의 이계도함수도 0이다. CSS 방식 3차 베지에 시간 함수는 x(u)=t를 먼저 풀고 y(u)를 사용한다. 비대칭 제어점으로 검사하면 선형 곡선에서 가려진 오류를 찾기 쉽다.

## 적용 조건과 예외

유한 전환(tween)에서 일시정지는 진행 지점을 유지하고, 재시작은 현재 표시값을 새 시작점으로 삼을 수 있다. 역재생은 같은 곡선을 거슬러 올라갈 수 있다. 재시작 때 속도가 달라지고 역재생 때 속도 방향이 바뀔 수 있다. 언리얼의 `SetWorldLocation`은 월드 좌표의 위치를 적용한다. 루트 스윕을 사용하면 장애물 때문에 목표점 전에 멈출 수 있다.

## 확인 방법

끝점과 오버슈트, 0 기간, 일시정지·재개, 중간과 완료 후 재시작·역재생을 검사한다. 완료 이벤트가 한 번씩 발생하는지 보고 실제 컴포넌트 위치를 곡선 계산값과 별도로 측정한다. 실제 경과 시간과 합성 샘플은 구분한다.

## 근거

W3C는 베지에 시간 함수를, Perlin은 5차 다항식을 설명한다. 과거 비충돌 컴포넌트 검사에서 위치가 이어지는 재시작, 곡선 역재생, 작은 위치 오차가 관찰됐다. 일부 목표 표시율은 달성하지 못했다. 충돌, 속도 연속성, 플레이어 체감은 별도 확인이 필요하다.

- [W3C — CSS Easing Functions Level 1](https://www.w3.org/TR/css-easing-1/)
- [Ken Perlin — Improving Noise](https://mrl.cs.nyu.edu/~perlin/paper445.pdf)
- [Epic — Set World Location](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/USceneComponent/K2_SetWorldLocation?application_version=5.8)

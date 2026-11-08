# 고정 시간 간격·점프 적분·서브픽셀

기준 항목: K-GAME-TECH-TIMESTEP · 확인일: 2026-11-07 · 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

안정적인 물리·리플레이가 필요하면 누적기로 고정 시뮬레이션 간격을 유지하고 화면을 보간한다. 밀린 계산량은 제한한다. 반암시적 오일러는 v+=a*dt 뒤 x+=v*dt를 계산하며 명시적 오일러는 이전 속도를 쓴다. 점프의 상승·하강 가속도는 다르게 설계할 수 있다. 정수 픽셀로 표시해도 소수 위치나 잔여량은 보존한다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

델타 타임을 곱하는 것만으로 모든 물리가 안정적·결정론적으로 바뀌지 않는다. 화면 FPS·시뮬레이션 틱·네트워크 틱은 별개다.

## 적용 전 점검

적용 전 점검: 동일 입력을 30·60·144 렌더 FPS와 순간 멈춤 조건에서 재생해 최고점·착지·이벤트 순서를 비교한다.

## 근거

- [Glenn Fiedler — Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/) — 출처의 확인 범위는 아래 원칙을 따른다.
- [Glenn Fiedler — Integration Basics](https://gafferongames.com/post/integration_basics/) — 출처의 확인 범위는 아래 원칙을 따른다.
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html) — 출처의 확인 범위는 아래 원칙을 따른다.
- 공식 문서·논문·저자 글은 확인한 본문 범위에 한정한다. 초록·영상 설명만 확인한 경우와 미열람 자료는 영문 정본 Evidence에 명시했다. 예제 코드·영상·제품 성능은 실행 검증하지 않았다.
- 출발 영상: V02, V49. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).


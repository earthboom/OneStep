# 군중의 경로·국소 회피·입장 제어·표시 비용 분리하기

**K-GAME-TECH-CROWD** · 공유 경로로 진행 방향을 정하고 주변 움직임에는 국소 회피를 사용한다. 안전하게 움직여도 요청이 끝없이 밀릴 수 있다면 입장 정책을 설계한다.

## 지침

공간 해시는 주변 개체를 셀로 묶어 이웃 질의 후보를 줄인다. 공유 플로 필드는 장거리 방향을 제공하고 국소 회피는 이웃 몸체를 고려해 가까운 미래의 이동을 고른다. ORCA(Optimal Reciprocal Collision Avoidance)는 상호 회피를 가정해 속도 제약을 구한다. 중앙 예약은 공간과 시간을 미리 배정한다. 좁은 통로에는 몸체가 출구를 완전히 지날 때까지 한 방향 통행을 허용할 수 있다. Hitman: Absolution 개발자 발표는 2.5D 셀 지도, 출구별 대피 필드, 국소 조향, 일부 군중의 NPC 승격을 설명한다.

## 적용 조건과 예외

지속 유입에서 선입선출(FIFO)은 입장 순서를 보존하지만 맨 앞 요청이 막히면 뒤도 멈춘다. 토큰 버킷은 보충률과 허용 버스트 크기로 입장량을 제한한다. 역압력은 상류에 대기를 전달한다. 손실을 허용하면 거부·폐기로 진입 부하를 줄일 수 있다. 큐 상한은 해당 큐만 제한한다. 충돌이 없어도 교착이나 특정 개체의 기아가 생길 수 있다. 표시 LOD, 행동 갱신 주기, 물리 안전 예산을 나누어 측정한다.

## 확인 방법

같은 요청 유입에서 최초 도착 시각을 보존한다. 유입·승인·거부·가장 오래된 요청의 나이·완료·전체 유입 대비 기한 내 완료 비율을 기록한다. 실제 반경, 마지막 이동, 의도적 충돌 대조 사례로 스윕 중 간격을 검사한다. 대상 장치에서 지형 변경, 동기화, 애니메이션, 렌더링을 포함한 긴 프레임도 측정한다.

프레임 예산을 평가할 때 CPU와 GPU 시간을 각각 기록하고 누락된 GPU 표본을 표시한다.

## 근거

Fauerby의 발표는 해당 게임의 과거 구조를, ORCA 저자들은 알고리즘 가정을, Epic은 Mass Avoidance의 공간·조향 모델을 설명한다. 기존 격자 예시에서 충돌 없는 교착과 유한 큐 소진이 각각 관찰됐다. 유한 소진은 무한 시간 진행이나 실제 Mass 동작의 증명이 아니다.

- [Kasper Fauerby — Crowds in Hitman: Absolution slides](https://media.gdcvault.com/gdc2012/slides/Programming%20Track/Fauerby_Kasper_CrowdsInHitman.pdf)
- [Epic — Mass Avoidance Overview](https://dev.epicgames.com/documentation/unreal-engine/mass-avoidance-overview-in-unreal-engine?lang=en-US)
- [ORCA authors](https://gamma-web.iacs.umd.edu/ORCA/)
- [Li et al., corridor symmetry](https://mapf.info/index.php/Main.SKoen20k)
- [LaValle footprint/C-space](https://lavalle.pl/planning/node161.html)
- [fixed-path coordination](https://lavalle.pl/planning/node325.html)
- [RHCR](https://arxiv.org/abs/2005.07371)
- [PIBT](https://arxiv.org/abs/1901.11282)
- [online pickup/delivery](https://arxiv.org/abs/1705.10868)

### admission control

모든 요청 처리와 거부 불가가 요구되면 대기열에서 요청을 버리는 정책은 요구를 충족하지 않는다. 유입량이 처리 용량을 계속 초과하는 과부하에서는 유한 대기열과 함께 상류 역압력, 용량 증대 또는 합의된 유입량 변경이 필요하다. 역압력 전후에도 원래 요청 ID와 도착 시각을 유지한다. 가장 오래 기다린 요청과 전체 완료 건수를 같이 봐서 총처리량에 가려진 기아를 찾는다. 요청이 계속 들어오고 각 완료에 처리 용량이 든다는 조건의 판단이다. [Reactive Streams — asynchronous backpressure](https://www.reactive-streams.org/)

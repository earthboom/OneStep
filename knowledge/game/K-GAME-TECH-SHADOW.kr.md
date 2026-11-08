# 섀도 맵·CSM·필터링 선택

기준 항목: K-GAME-TECH-SHADOW · 확인일: 2026-11-07 · 상태: 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

움직이는 광원·물체에 사용한다. 광원 시점의 깊이를 저장하고 수신 표면 깊이와 비교한다. CSM은 카메라 시야를 거리별로 나눠 해상도를 배분하고, PCF는 깊이 자체가 아닌 비교 결과를 평균한다. 분할 거리·바이어스·필터 크기·안정화를 따로 조정한다. 정적 조명 베이크는 광원과 물체의 변화 조건부터 확인한다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

표면 줄무늬, 그림자 들뜸, 캐스케이드 경계, 이동 시 떨림은 원인이 다르다. 과거 Direct3D 예제가 현재 UE 렌더러의 최적 설정을 뜻하지 않는다.

## 적용 전 점검

적용 전 점검: 비스듬한 표면·얇은 물체·느린 카메라 이동에서 확인하고 품질 단계별 그림자 GPU 시간과 메모리를 측정한다.

## 근거

- [Microsoft — Cascaded Shadow Maps](https://learn.microsoft.com/en-us/windows/win32/dxtecharts/cascaded-shadow-maps) — 확인 범위는 영문 정본의 Evidence에 기록. 추가 읽기로 표시된 자료는 본문 전체를 확인하지 않았다.
- [Bunnell & Pellacini — Shadow Map Antialiasing](https://developer.nvidia.com/gpugems/gpugems/part-ii-lighting-and-shadows/chapter-11-shadow-map-antialiasing) — 확인 범위는 영문 정본의 Evidence에 기록. 추가 읽기로 표시된 자료는 본문 전체를 확인하지 않았다.
- 출발 영상: V03. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).


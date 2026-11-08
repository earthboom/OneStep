# 잔디·식생의 LOD와 렌더링 예산

기준 항목: K-GAME-TECH-FOLIAGE · 확인일: 2026-11-07 · 상태: 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

실루엣 중요도에 따라 교차 카드나 메시를 선택한다. 보이지 않는 영역은 컬링하고 먼 곳은 단순화하며 호환 인스턴스를 묶는다. 공간적으로 이어지는 바람으로 정점을 변형한다. 드로 호출·정점·오버드로·그림자 비용을 나눠 측정한다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

인스턴싱이 줄이는 것은 주로 제출 비용이며 모든 셰이딩 비용이 사라지지는 않는다. 카드는 불투명 메시보다 픽셀 비용이 클 수 있다. 현재 Nanite 식생 동작은 별도 확인한다.

## 적용 전 점검

적용 전 점검: 낮은 시점·상공에서 밀집 식생을 보고 바람·그림자·알파 레이어를 각각 꺼 병목을 찾는다.

## 근거

- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass) — 확인 범위는 영문 정본의 Evidence에 기록. 추가 읽기로 표시된 자료는 본문 전체를 확인하지 않았다.
- [Tiago Sousa — Vegetation Procedural Animation and Shading in Crysis](https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-16-vegetation-procedural-animation-and-shading-crysis) — 확인 범위는 영문 정본의 Evidence에 기록. 추가 읽기로 표시된 자료는 본문 전체를 확인하지 않았다.
- 출발 영상: V19. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).


# 평면 반사·환경맵·SSR 선택

기준 항목: K-GAME-TECH-REFLECTION · 확인일: 2026-11-07 · 상태: 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

정확한 평면 거울은 반사 카메라와 클리핑으로 장면을 다시 그린다. 대략적인 주변 반사는 환경맵·프로브를 쓰고 갱신 정책을 정한다. SSR은 화면 깊이 안에서만 추적하므로 화면 밖 정보에 대한 대체 수단이 필요하다. 거칠기·거리·중요도로 방식을 조합한다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

거울 뒤 복제 공간은 과거의 구현 방법 중 하나다. 큐브맵도 동적 갱신이 가능하다. SSR은 보이지 않는 지오메트리를 복구할 수 없다.

## 적용 전 점검

적용 전 점검: 반사 대상을 화면 밖으로 이동하고 시점을 바꾸며 정적·동적 캡처의 차이와 GPU 비용을 비교한다.

## 근거

- [Epic — Planar Reflections](https://dev.epicgames.com/documentation/en-us/unreal-engine/planar-reflections-in-unreal-engine) — 확인 범위는 영문 정본의 Evidence에 기록. 추가 읽기로 표시된 자료는 본문 전체를 확인하지 않았다.
- 출발 영상: V16. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).


## Screen Space Reflections의 적용과 확인

Screen Space Reflections는 현재 화면에 있는 정보로 반사를 계산하므로 화면 가장자리에서 결과가 사라질 수 있다. Planar Reflections는 평면에 대해 반사된 시점에서 장면을 렌더링한다. 반사 대상이 본 화면 밖으로 나갈 때의 완전성과 선택한 품질에서의 GPU 시간을 비교한다.

검색어 · Screen Space Reflections, Planar Reflections

[Epic, Planar Reflections](https://dev.epicgames.com/documentation/unreal-engine/planar-reflections-in-unreal-engine?lang=en-US)은 용어와 적용 조건의 근거다. 제안한 검사는 대상 환경에서 수행한다.

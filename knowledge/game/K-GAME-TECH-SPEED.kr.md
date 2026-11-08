# 속도감·FOV·모션 블러

기준 항목: K-GAME-TECH-SPEED · 확인일: 2026-11-07 · 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

가속 이벤트에 FOV 변화·카메라 오프셋·지연·속도 기반 블러를 연결한다. 기본 구도와 연출을 분리해 강도 설정이 조준·이동 규칙을 바꾸지 않게 한다. 깊이 기반 카메라 블러는 시점 변환으로 픽셀 이동을 복원하지만 움직이는 물체는 추가 운동 정보가 필요하다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

블러가 잃어버린 입력 반응이나 실제 프레임을 복구하지는 않는다. 큰 FOV 변화·강제 카메라 이동은 편안함과 표적 판독을 해칠 수 있다.

## 적용 전 점검

적용 전 점검: 실제 주행·이동 과제에서 효과 끔·약함·기본을 비교하고 접근성 설정을 제공한다.

## 근거

- [Gilberto Rosado — Motion Blur as a Post-Processing Effect](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-27-motion-blur-post-processing-effect) — 출처의 확인 범위는 아래 원칙을 따른다.
- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers) — 출처의 확인 범위는 아래 원칙을 따른다.
- 공식 문서·논문·저자 글은 확인한 본문 범위에 한정한다. 초록·영상 설명만 확인한 경우와 미열람 자료는 영문 정본 Evidence에 명시했다. 예제 코드·영상·제품 성능은 실행 검증하지 않았다.
- 출발 영상: V06. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).


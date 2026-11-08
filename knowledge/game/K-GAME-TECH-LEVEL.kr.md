# 월드 규모·문 크기·랜드마크·경로

기준 항목: K-GAME-TECH-LEVEL · 확인일: 2026-11-07 · 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

캐릭터 크기·카메라 범위·회전 반경·전투 시야에서 시작한다. 통과 가능한 문·복도를 블록아웃하고 차폐·랜드마크·경로 길이로 탐험 리듬을 만든다. 제작 범위에 유리하면 분기와 합류를 쓰되 의미 있는 대안은 남긴다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

모든 게임의 문이 현실의 일정 배수라는 주장은 아니다. 면적·이동 시간·콘텐츠 밀도·체감 규모는 다르다. 기존 탐험·플랫포머 지식과 함께 사용한다.

## 적용 전 점검

적용 전 점검: 실제 카메라·지원 체형으로 통과시키고 경로 설명 없이 목표를 찾는지 관찰한다.

## 근거

- 기존 [탐험](K-GAME-EXPLORATION.kr.md), [플랫포머](K-GAME-PLATFORMER.kr.md), [프로토타입·플레이테스트](K-GAME-PROTOTYPE-PLAYTEST.kr.md)를 함께 사용한다. 크기·경로 제안은 대상 게임에서 검증할 설계 종합이다.

- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers) — 출처의 확인 범위는 아래 원칙을 따른다.
- [Shaker et al. — Constructive Generation Methods for Dungeons and Levels](https://www.pcgbook.com/chapter03.pdf) — 출처의 확인 범위는 아래 원칙을 따른다.
- 공식 문서·논문·저자 글은 확인한 본문 범위에 한정한다. 초록·영상 설명만 확인한 경우와 미열람 자료는 영문 정본 Evidence에 명시했다. 예제 코드·영상·제품 성능은 실행 검증하지 않았다.
- 출발 영상: V11, V12, V24. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).


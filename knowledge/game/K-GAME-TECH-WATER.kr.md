# 사인파·거스너파 수면

기준 항목: K-GAME-TECH-WATER · 확인일: 2026-11-07 · 상태: 참고 지식. 실제 엔진 구현·성능·플레이테스트는 수행하지 않았다.

## 원리와 구현 요점

진폭·파장·방향·위상을 가진 파동들을 합해 수면을 만든다. 거스너파는 표면점을 수평으로도 움직여 더 뾰족한 마루를 표현한다. 같은 변위장에서 노멀을 계산하고 부력 판정에도 호환되는 수면 질의를 제공한다.

구현 선택과 점검은 출처를 바탕으로 한 실무적 종합이며 특정 게임의 정확한 구현을 보증하지 않는다.

## 적용 조건과 한계

접힘을 피하도록 가파름을 제한한다. 파동 합은 완전한 유체 시뮬레이션이 아니며 쇄파·해안·장애물 유동을 자동 처리하지 않는다.

## 적용 전 점검

적용 전 점검: 상공 반복 무늬·얕은 해안·부유 물체·시뮬레이션 주기별 차이를 확인한다.

## 근거

- [Mark Finch — Effective Water Simulation from Physical Models](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-1-effective-water-simulation-physical-models) — 확인 범위는 영문 정본의 Evidence에 기록. 추가 읽기로 표시된 자료는 본문 전체를 확인하지 않았다.
- 출발 영상: V32. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).


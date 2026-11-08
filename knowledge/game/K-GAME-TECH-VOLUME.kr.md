# 볼류메트릭 연기·구름과 게임 판정 분리

기준 항목: K-GAME-TECH-VOLUME · 확인일: 2026-11-07 · 참고 지식. 엔진 실행·성능·실제 플레이 검증은 별도다.

## 원리와 구현 요점

밀도장과 산란·소광으로 연기·구름을 표현하고 노이즈로 형상을 만든다. 저해상도 계산과 시간축 복원은 품질·성능 절충이다. 경쟁 게임의 연막은 클라이언트 최종 이미지에 맡기지 말고 권한 있는 밀도·가시성 규칙을 공유한다.

### 추가 조사로 보완한 구현

밸브의 2023년 CS2 패치 노트는 벽 근처 연기 부피 확장, AMD에서의 스텝 함수 조정, 산탄총이 만드는 구멍을 명시한다. 공간 부피 연막 동작은 확인되지만 전체 솔버가 공개된 것은 아니다. 구현 종합안은 권한 있는 연막 점유·일시적 총탄/수류탄 변형과 시점별 조명을 분리하고 공유 상태를 플랫폼에 맞게 샘플링하는 방식이다. 지오메트리 교차·복원 품질이 게임 가시성을 바꾸지 않도록 확인한다.

## 적용 조건과 한계

밸브의 해당 패치에서 부피 연막 동작을 확인했지만 전체 밀도 솔버·동기화·레이마칭 코드는 공개되지 않았다. 부피 표현과 유체 시뮬레이션은 다르며 경쟁 가시성은 대상 게임에서 검증한다.

## 적용 전 점검

적용 전 점검: 움직이는 조명·카메라 컷·연기 내부·깊이 경계와 품질별 가시성 일치를 확인한다.

## 근거

- [Epic — Volumetric Fog](https://dev.epicgames.com/documentation/en-us/unreal-engine/volumetric-fog-in-unreal-engine)
- [Shaker, Togelius & Nelson — Fractals, Noise and Agents](https://www.pcgbook.com/chapter04.pdf)
- [u/smilefr — Optimized volumetric clouds](https://www.reddit.com/r/Unity3D/comments/1u8g138/i_finally_have_optimzied_volumetric_clouds/)

### 추가 조사 출처

- [Valve — Counter-Strike 2 June 2023 update notes](https://store.steampowered.com/news/posts/?appids=730&enddate=1689630041&feed=steam_announce%2F1000) — Official dated notes, VOLUMETRIC SMOKE sections; source code and cross-client determinism not disclosed.

추가 조사 출처의 영문 주석은 정확한 절·함수·접근 범위를 보존한다. 원본 슬라이드·문서·공개 코드의 확인과 실제 엔진·하드웨어 실행은 구분한다. 영상 설명·세션 개요만 확인한 자료를 전체 발표 확인으로 간주하지 않는다.

출발 영상: V10, V27. [영상별 대응표](K-GAME-TECH-GUIDE.kr.md).

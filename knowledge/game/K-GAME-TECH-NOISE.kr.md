# 펄린 노이즈·프랙탈 지형

기준 항목: K-GAME-TECH-NOISE · 확인일: 2026-11-07 · 참고 지식. 엔진 실행·성능·실제 플레이 검증은 별도다.

## 원리와 구현 요점

공간적으로 이어지는 변형에 사용한다. 펄린 노이즈는 주변 격자점의 기울기 내적을 부드럽게 보간한다. 내적값을 그대로 더하는 것만으로는 부족하다. 주파수·진폭을 조절한 옥타브를 합쳐 다중 규모 디테일을 만들고 바이옴 필드는 메시 생성과 분리한다.

### 추가 조사로 보완한 구현

모장 1.18 개발 노트는 지형 형상·바이옴 분포·노이즈 동굴·대수층을 구분한다. 대수층은 지하 영역에 지역 수위를 주며 기존 동굴 파기와 노이즈장을 함께 쓸 수 있다. 새 생성기는 밀도 d(x,y,z)·기후/바이옴장·유체 점유를 별도 입력으로 취급하고 청크 메시 전 이웃 여백까지 평가해 경계를 맞춘다. 이는 구현 종합안이며 모장의 정확한 밀도 함수는 아니다.

## 적용 조건과 한계

높이맵은 돌출 천장을 표현할 수 없지만 밀도장은 가능하다. 마인크래프트의 정확한 알고리즘은 에디션·버전별로 별도 확인해야 한다.

## 적용 전 점검

적용 전 점검: 시드를 고정하고 청크 경계·미분 연속성·바이옴 전환·이동 가능한 지형을 확인한다.

## 근거

- [Ken Perlin — Improving Noise](https://mrl.cs.nyu.edu/~perlin/paper445.pdf)
- [Shaker, Togelius & Nelson — Fractals, Noise and Agents](https://www.pcgbook.com/chapter04.pdf)

### 추가 조사 출처

- [Mojang — Java 1.18 experimental world generation](https://www.minecraft.net/en-us/article/new-world-generation-java-available-testing) — Official historical development notes; release scope distinguished from snapshot behavior.
- [Mojang — Bedrock 1.18.0 release notes](https://feedback.minecraft.net/hc/en-us/articles/4414284658701-Minecraft-Caves-Cliffs-Part-II-1-18-0-Bedrock) — New biome/cave generation and aquifers; edition/version retained.

추가 조사 출처의 영문 주석은 정확한 절·함수·접근 범위를 보존한다. 원본 슬라이드·문서·공개 코드의 확인과 실제 엔진·하드웨어 실행은 구분한다. 영상 설명·세션 개요만 확인한 자료를 전체 발표 확인으로 간주하지 않는다.

출발 영상: V07, V50. [영상별 대응표](K-GAME-TECH-GUIDE.kr.md).

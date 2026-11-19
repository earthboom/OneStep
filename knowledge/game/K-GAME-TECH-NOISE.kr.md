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

로컬 시험의 원시 측정과 매체는 해당 실험 기록에 보관돼 있다.

- [Ken Perlin — Improving Noise](https://mrl.cs.nyu.edu/~perlin/paper445.pdf)
- [Shaker, Togelius & Nelson — Fractals, Noise and Agents](https://www.pcgbook.com/chapter04.pdf)

### 추가 조사 출처

- [Mojang — Java 1.18 experimental world generation](https://www.minecraft.net/en-us/article/new-world-generation-java-available-testing) — Official historical development notes; release scope distinguished from snapshot behavior.
- [Mojang — Bedrock 1.18.0 release notes](https://feedback.minecraft.net/hc/en-us/articles/4414284658701-Minecraft-Caves-Cliffs-Part-II-1-18-0-Bedrock) — New biome/cave generation and aquifers; edition/version retained.

추가 조사 출처의 영문 주석은 정확한 절·함수·접근 범위를 보존한다. 원본 슬라이드·문서·공개 코드의 확인과 실제 엔진·하드웨어 실행은 구분한다. 영상 설명·세션 개요만 확인한 자료를 전체 발표 확인으로 간주하지 않는다.

출발 영상: V07, V50. [영상별 대응표](K-GAME-TECH-GUIDE.kr.md).

### fractional Brownian motion

절차 지형의 **옥타브(octave)**는 특정 주파수·진폭의 노이즈 층이다. 흔히 fBm(fractional Brownian motion)이라 부르는 프랙털 노이즈 합성은 여러 층을 더한다. **Lacunarity**는 옥타브 사이의 주파수 배율, **persistence**는 진폭 배율이다. 청크 경계에서 샘플링하는 월드 좌표를 일치시킨다. 인접 청크를 각각 생성해 경계를 비교하고 먼 LOD에서 고주파 앨리어싱도 검사한다. [libnoise — Perlin module parameters](https://libnoise.sourceforge.net/docs/classnoise_1_1module_1_1Perlin.html)

## 실제 언리얼 높이장 — 2026-11-12

과거 Unreal 실험 결과:시드Perlin/fBm4·인접4청크·57모델검사·실제PIE/패키지12상황·2352표본/3120경계쌍·각3회비용·정상1배속영상이다. 최신14부분구현/29직접구현없음이다.

전역 정수 표본좌표와 시드/설정을 공유하고 음수격자는floor로 계산한다. 법선은 주파수체인룰을 포함한 전역분석미분이다. 차분은 이웃여유영역이 필요하며 청크끝 한쪽차분은 높이가 같아도 법선이 어긋날 수 있다. 정상경계 높이/법선차이0,잘못된로컬높이96.235647cm,잘못된법선.10062494벡터로 실패를 검출했다.

동일빌드내 역순생성·3회시드0..63결과는 재현됐다. Editor와패키지의 소스double해시는 서로달랐고 법선오차차이는약1.6e-17이었다. 빌드간 소스비트동일성은 주장하지 않는다. 실제게시된 메시해시·표본·경계·인덱스는정확히같다. 실제float위치5e-5cm/16비트법선1e-4벡터의 표현오차와 정책재현성을 구분한다.

삼각형방향을 거꾸로 해석해 수치검사가 통과했지만 지형이보이지 않는 실패를 수정했다. 실제엔진평면·역순평면·모든네이티브삼각형과 캡처로 확인했으며 양면재질/컬링변경으로 우회하지 않았다. 실패기록과29개결과변형 검사를 보존했다.

1280×720·4청크전체재생성·64시드·각3회에서 생성p95는Perlin약.65~.68ms/fBm약1.44~1.50ms,메시반영약36ms,전체wall약39~40ms다. 이조건의매프레임동기재생성은60FPS예산을 넘는다. 정적1회생성·중요프레임밖 적용은별도수명/예산확인이 필요하다. GPU완료·메모리상한·엔진GC종료·스트리밍성능은검증하지 않았다.

단일높이연속지형에만 조건부적용한다. 개별삼각형기울기·충돌부드러움·바이옴·LOD·대형월드·내비게이션·동굴·유체·복셀·스트리밍은별도다. 렌더러/검증도구개선은하지 않았다. 세부원자료는로컬증거이며 이전지식커밋에구현이포함됐다는뜻이아니다. 이번작업은커밋/푸시하지않았다.

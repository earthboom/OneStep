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

로컬 시험의 원시 측정과 매체는 해당 실험 기록에 보관돼 있다.

- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass) — 확인 범위는 영문 정본의 Evidence에 기록. 추가 읽기로 표시된 자료는 본문 전체를 확인하지 않았다.
- [Tiago Sousa — Vegetation Procedural Animation and Shading in Crysis](https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-16-vegetation-procedural-animation-and-shading-crysis) — 확인 범위는 영문 정본의 Evidence에 기록. 추가 읽기로 표시된 자료는 본문 전체를 확인하지 않았다.
- 출발 영상: V19. [전체 대응표](K-GAME-TECH-GUIDE.kr.md).

## Static Mesh Foliage의 적용과 확인

언리얼 Static Mesh Foliage는 하드웨어 인스턴싱으로 반복 메시를 묶어 제출한다. 오버드로는 겹친 잎 카드가 같은 화면 영역을 여러 번 셰이딩할 때 드는 별도 비용이다. 인스턴스 수를 고정하고 카드의 화면 점유율을 바꿔 GPU 시간과 드로 제출 수를 따로 본다.

검색어 · Static Mesh Foliage, hardware instancing, overdraw

[Epic, Foliage Mode](https://dev.epicgames.com/documentation/unreal-engine/foliage-mode-in-unreal-engine?lang=en-US)은 용어와 적용 조건의 근거다. 제안한 검사는 대상 환경에서 수행한다.

## 실제 언리얼 검증

### 지침

여러 잔디 덩어리에 같은 교차 카드 메시와 알파 마스크 재질을 공유하고,개별 컴포넌트와 ISM의 비용을 실제 장면에서 비교한다. 인스턴싱은 반복 제출·오브젝트 비용을 줄이는 수단이며 모든 마스킹 픽셀 작업을 없애지는 않는다. 화면 점유율·겹침·시점과 GPU 비용을 따로 확인한다.

### 적용 조건과 예외

작은 정적 패치의 제한된 UE5.8.3 구현 근거다. 실제 잔디 아트·조명·그림자·바람·LOD·Nanite·대규모 숲/스트리밍·충돌/상호작용은 별도 검증한다. 과거 GPU Gems 아이디어를 현재 하드웨어 성능 보장으로 옮기지 않는다.

### 실제 검사 — 2026-11-13

과거 Unreal 실험 결과:정책37/증거47,실제PIE4회+패키지4회에서각8상황,4조건각3회비용과정상1배속영상이다. 최신20개부분구현/23개직접구현없음이며이전FPS미확인은유지한다.

공유 메시의수직교차카드2면은8정점/4삼각형,1LOD·비Nanite,충돌/그림자없음이다. 행동16개/비용1024개이며실제개별·인스턴스변환과공유바인딩을대조한다. 선형64×64BGRA8최근접/클램프/밉없음마스크와Masked/Unlit/양면·ISM지원재질을사용한다. 실제4096텍셀과불투명1344텍셀을독립계산했다.

같은숫자의컬링거리가같은가시범위는아니다. 설치엔진의개별메시는경계구표면,ISM은중심을기준으로한다. 기본설정을유지하고개별최대거리를1000−실제반경,ISM을1000cm로설정했다. 반경57.6888204cm는카드정점의구이며AABB모서리길이가아니다. 경계/크기/엔진이달라지면다시유도한다. 중심1000cm는보이고1001/1300cm는사라지며같은살아있는개체가999cm로재진입한다. 하드컬링팝/부드러운페이드는구분한다.

실제카메라/투영/메시/UV/재질/배치/컬링/캡처목록과픽셀을대조한다. 1/256픽셀정점스냅·원근UV·최근접마스크로깊이/색을독립계산했다. 정면/뒷면의두앞면방향관측과단일개체구멍표본이있다. 최대RGB오차0.000484452로.008한계이내다. 숫자선형HDR과톤매핑스크린샷은별개다. 예상거리생존끔1024/켬182는GPU실제가시개체수가아니다. 가림/프러스텀이추가된다.

1280×720·같은1024배치/자산/설정/카메라/실행물,준비2초+측정8초,4조건각3회다. 개별1024컴포넌트대ISM1개는의도한차이다. 구성/등록/검사/읽기/최종저장은측정밖이고HUD/숫자배열은전체에포함한다. 측정중배치·카메라·컬링변경과관측읽기는없다. individual-off: whole wall p95 9.984–10.222 ms; whole-RHI draw medians [865, 865, 865]. ism-off: whole wall p95 9.390–9.666 ms; whole-RHI draw medians [27, 27, 27]. individual-on: whole wall p95 9.546–9.942 ms; whole-RHI draw medians [149, 149, 149]. ism-on: whole wall p95 9.621–9.737 ms; whole-RHI draw medians [27, 27, 27]. 전체wall/간격·지연된전체GPU·전체RHI드로콜을단독잔디패스나같은CPU/GPU프레임으로보지않는다. 자동배칭을끄지않았고호스트부하는미통제다. 초기등록/메모리/변경비용과알파오버드로단독비용은분리하지않았다.

독립검토1회에서비교cvar·실행환경검증누락을발견해5실패를재현후보완했다. 실제에디터/패키지빌드도확인했으며에디터전용Nanite설정은조건부대입,런타임은실제데이터검사를사용한다. 렌더러/검증프레임워크개선이나커밋/푸시는없다.

### 근거

- 과거 Unreal 실험 결과.
- [GPU Gems 잔디 교차카드](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass),[Crysis 식생](https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-16-vegetation-procedural-animation-and-shading-crysis):기존2026-11-07문헌확인과오늘실제검증을구분한다. 바람/조명검증은수행하지않았다.
- [Epic ISM 설명](https://dev.epicgames.com/documentation/en-us/unreal-engine/instanced-static-mesh-component-in-unreal-engine):반복묶기개념이며현재웹5.9를설치5.8의LOD보장으로옮기지않는다. 거리규칙은설치5.8소스와실제출력으로확인했다.
- 원래쇼츠V19는[기술가이드](K-GAME-TECH-GUIDE.kr.md)의탐색출발점이다.

실측 적용 판단: 전체RHI 드로콜 중앙값은 개별/끔865·개별/켬149에서 ISM두조건27로 줄었다. 전체프레임 개선은 작았고,이 작은 정적 장면에서 ISM에 컬링을 더한 추가 이득은 일관되게 확인되지 않았다. 예상 생존 개체수만으로 판단하지 말고 실제프레임/GPU 결과를 함께 사용한다.

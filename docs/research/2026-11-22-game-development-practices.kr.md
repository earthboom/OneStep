# 게임 개발 실무 연구

2026-11-22 · 데이터 변경, 렌더링, 생성과 캐시, 몬스터·NPC AI, 화면 밖 시뮬레이션

**게임의 사실을 담는 상태와 그 상태를 표현하는 객체의 수명을 분리한다.** 멀어진 몬스터는 화면에서 사라지고 애니메이션 갱신이 줄어도, 처치 여부와 퀘스트 상태는 이어질 수 있다. 반대로 구경꾼 한 명의 개별 경로가 게임에 영향을 주지 않으면, 플레이어 가까이에서만 실제 객체를 만들 수 있다. 무엇을 남길지는 카메라 거리와 함께 **플레이어가 관찰하거나 규칙이 의존하는 결과**로 결정한다. [Simulation Level-of-Detail](https://pages.cs.wisc.edu/~schenney/research/culling/chenney-gdc2001.pdf) · [Unreal Mass Gameplay](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-gameplay-in-unreal-engine)

이 문서는 [C++·Unreal 프레임워크 조사](2026-11-21-cpp-game-framework.kr.md), [Unity·C# 프레임워크 조사](2026-11-22-unity-csharp-game-framework.kr.md), [AI 코드 변경의 품질 보존 조사](2026-11-21-ai-codebase-quality.kr.md)를 제작·운영 판단으로 이어간다. 사례의 수치나 엔진 API는 당시 장르, 하드웨어, 엔진·패키지 버전의 조건에서 읽는다. 아래 표의 구현·검증 제안은 게임에 맞춰 실험할 후보다.

| 결정 | 첫 질문 | 확보할 증거 |
| --- | --- | --- |
| 데이터 추가·수정·삭제 | 이전 저장이나 모드가 그 ID와 값을 쓰는가? | 에셋 의존 그래프, 예전 파일의 로드와 마이그레이션, 릴리스 데이터 검증 결과 |
| 렌더링 비용 절감 | 실제 긴 프레임은 CPU, GPU, I/O 중 어디에서 기다리는가? | 타깃 빌드 캡처, 재현 루트, 프레임 시간 분포, 픽셀·동작 품질 비교 |
| 로드·생성·해제·캐시 | 요청부터 사용 준비까지 얼마나 걸리고, 얼마나 자주 다시 쓰는가? | 콜드·웜 지연, 상주·피크 메모리, 캐시에서 쫓겨난 뒤 재요청, 생성 지연 |
| 몬스터·NPC AI | 관찰, 결정, 이동, 애니메이션, 월드 연출이 어디에서 만나는가? | 결정 근거와 취소 로그, 경로 실패·재계획, 예산 안의 응답 지연 |
| 화면 밖 NPC와 객체 | 사라진 동안 어떤 결과가 반드시 이어져야 하는가? | 전이 왕복, 재진입, 퀘스트·전투·사운드·복제의 연속성 |

## 1. 데이터의 수명과 변경 계약

### 데이터마다 쓰는 주체와 배포 시점을 정한다

- **저작 원본**에는 NPC 정의, 대사·지역화 키, 전투 수치, 씬 연결 등 디자이너가 편집하는 값을 둔다. 소스 관리, 검증, 변경 이력이 필요하다. 사용 중인 엔진의 에셋 GUID나 경로가 바뀔 수 있다면, 저장과 네트워크가 의존할 게임 ID를 명시적으로 고정한다.
- **생성된 배포 데이터**에는 검증된 카탈로그·번들, NavMesh, 라이트맵, 사전 계산 표가 들어간다. 입력 데이터, 변환 도구, 대상 플랫폼으로 재생성 가능해야 한다. 입력·도구·플랫폼 변경이 빌드 캐시를 무효화하도록 하고, 같은 결과가 필요한 경우 빌드 산출물을 비교한다. AI가 생성 결과를 직접 수정할 수 있는 구조에서는 다음 빌드가 변경을 덮어쓰는지 확인한다.
- **플레이 세션의 상태**에는 현재 HP, 위치, 행동, 점유 중인 자리, 이미 수집한 물건이 들어간다. 소유권은 월드·세션·서버 등 실제로 쓰는 쪽에 둔다. 세이브에는 지속되어야 하는 부분과 `schemaVersion`, 필요한 콘텐츠 버전·ID를 기록한다. 외형·NavMesh 포인터·로드 핸들은 다시 얻을 수 있는 값이다.
- **라이브 설정**은 밸런스나 콘텐츠 가용성처럼 배포 사이에 바꿀 필요가 있을 때 둔다. 게임 규칙에 닿는 설정은 경기·세이브의 버전을 고정하거나 안전한 경계에서 검증된 스냅샷을 교체한다. 로딩 중 태스크가 이전 데이터와 새 데이터를 섞는지, 서버와 클라이언트가 같은 버전을 쓰는지 확인한다. [Bungie의 에셋 파이프라인](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s) · [Factorio 데이터 수명](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html) · [Unity 번들 재현성](https://docs.unity.com/en-us/engine/6000.3/manual/building-and-publishing/build-deterministic-builds/assetbundles-addressables)

| 작업 | 계약과 처리 | 실패를 드러낼 예 |
| --- | --- | --- |
| **추가** | 고유 ID를 발급하고 기본값·단위·범위·자원 참조·패키지 경계를 검사한다. Beta 몬스터의 독립 팩이 기존 선택 팩을 암묵적으로 끌어오지 않는지 실제 빌드에서 본다. | 중복 ID, 잘못된 음수 값, 누락된 애니메이션 키, 특정 선택 팩이 없는 빌드 |
| **수정** | 표시 이름과 호환성이 걸린 ID를 분리한다. 공격력 같은 수치 변경, 필드 이름 변경, 의미·단위 변경의 영향은 각각 다르다. 예전 저장에서 기존 개체의 값을 유지할지 새 정의를 적용할지 먼저 정한다. | 이전 저장의 동일 몬스터, 옛 단위로 기록된 값, 구·신 버전이 공존하는 경로 |
| **삭제** | 새 생성과 드롭 목록에서 먼저 빼고 사용 중인 이전 참조를 조사한다. 지원 기간에는 교체 ID, 폐기 표식, 안전한 대체 표현, 또는 명시적 로드 실패 중 계약에 맞는 것을 둔다. 이전 데이터 소비가 끝나면 정의와 관련 에셋을 제거한다. 폐기 ID는 구데이터가 남아 있는 동안 재사용하지 않는다. | 삭제한 아이템을 장착한 저장, 그 ID를 쓰는 퀘스트·모드, 에셋이 없는 Player, 마이그레이션 재실행 |

예를 들어 `ForestWolf`의 표시 이름 수정은 ID에 손댈 이유가 없다. `ForestWolf`를 삭제한다면 기존 개체를 대체 몬스터로 옮길지, 기존 개체만 보존할지, 저장 지원 정책에 따라 종료할지 먼저 정한다. 출시용 필수 참조를 누락하면 빌드 검증에서 실패시키고, 개발 중 placeholder를 허용한다면 어떤 입력이 왜 대체됐는지 진단에 남긴다. 저장을 변환하다 실패할 수 있는 환경에서는 성공한 결과를 다시 읽을 수 있을 때 원본 교체를 완료하고, 강제 종료 후 복구도 플랫폼에서 검증한다. [Factorio 마이그레이션](https://lua-api.factorio.com/latest/auxiliary/migrations.html) · [Protocol Buffers 스키마 진화](https://protobuf.dev/best-practices/dos-donts/) · [OneStep 저장 기술](../../knowledge/game/K-GAME-TECH-SAVE.kr.md)

| 찾아볼 자료 | 적용할 지점 |
| --- | --- |
| **Brandon Moro · Destiny 2, GDC 2018** | 작업 수준과 에셋 수준 의존성의 비용을 비교한다. 발표의 `Combined Dependencies`와 오래된 AO 사례에서 캐시 단위, 무효화 범위, 아티스트의 반복 작업이 연결된다. [GDC 발표](https://www.gdcvault.com/play/1025285/Tools-Tutorial-Day-Bungie-s) · [슬라이드](https://media.gdcvault.com/gdc2018/presentations/Moro_Brandon_Bungies_Asset_Pipeline.pdf) |
| **Andreas Fredriksson · Loading From Imperfect Data, GDC 2013** | 작업 중 에셋이 불완전할 때 로더가 어떻게 동작할 수 있는지 다룬다. 편집 중 계속 작업할 수 있는 정책과 출시 빌드에서 오류를 검출하는 정책을 설계할 때 읽을 만하다. [발표 슬라이드](https://media.gdcvault.com/gdc2013/slides/822192Fredriksson_Andreas_Loading_Imperfect_Data.pdf) |
| **Mokhov·Mitchell·Peyton Jones · Build Systems à la Carte, 2018** | 빌드 시스템의 작업 순서와 재빌드 판단을 분리해 비교한다. 에셋 변경 시 어떤 산출물만 다시 만들어야 하는지 설계할 때 참고할 논문이다. [논문](https://simon.peytonjones.org/assets/pdfs/build-systems-original.pdf) |
| **Factorio · 모드 및 저장 호환성 문서** | 정의를 구성하는 단계와 저장된 게임을 실행하는 단계가 구분된다. 공식 마이그레이션은 프로토타입 이름·타입 교체와 저장 상태 변경, 변경 적용 이력을 보여준다. [데이터 단계](https://lua-api.factorio.com/latest/auxiliary/data-lifecycle.html) · [마이그레이션](https://lua-api.factorio.com/latest/auxiliary/migrations.html) |
| **Insomniac · Marvel’s Spider-Man, SIGGRAPH 2019** | 오픈월드 콘텐츠 저작에서 절차적 처리를 사용하고 아티스트가 결과를 제어할 수 있게 했다. 같은 기반 입력에서 도시 콘텐츠를 반복 생성할 때, 어느 값이 저작 원본이고 어느 값이 다시 생성될 결과인지 판단하는 제작 사례다. [저자 발표 논문](https://history.siggraph.org/wp-content/uploads/2022/09/2019-Talks-Santiago_Procedural-System-Assisted-Authoring.pdf) |
| **Unreal·Unity의 도구** | Unreal은 Asset Manager와 Data Registries로 탐색·로딩·조회 경계를 나누고 Data Validation으로 규칙을 검사할 수 있다. Unity는 정의 에셋과 Addressables 카탈로그를 사용하고 별도 검증으로 중복 ID·깨진 참조를 찾을 수 있다. 초기에는 엔진 기본 기능과 실제 병목을 기준으로 선택한다. [Epic Asset Manager](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-management-in-unreal-engine) · [Data Registries](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-registries-in-unreal-engine) · [Data Validation](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-validation-in-unreal-engine) · [Unity ScriptableObject](https://unity.com/how-to/separate-game-data-logic-scriptable-objects) · [Addressables 출시작 사례](https://unity.com/resources/marvel-snap) |

## 2. 렌더링 최적화의 순서

1. **긴 프레임을 재현한다.** 타깃 기기·해상도·빌드·품질 옵션을 고정한다. 대표 경로와 최악에 가까운 경로에서 워밍업 구간을 구별하고, 프레임 시간의 중앙값·p95·p99, 예산을 초과한 프레임의 빈도와 길이를 본다. 60 FPS의 프레임 간격은 약 16.67 ms다. CPU·GPU가 겹쳐 실행되므로 단계 시간과 대기 구간을 타임라인에서 읽는다. [Unity 프로파일링](https://unity.com/how-to/best-practices-for-profiling-game-performance) · [Unreal 프로파일링](https://dev.epicgames.com/documentation/en-us/unreal-engine/introduction-to-performance-profiling-and-configuration-in-unreal-engine) · [Unreal Fest 프레임 타이밍 영상](https://www.youtube.com/watch?v=dKSHw_8vz3I)
2. **의심하는 원인을 한 번에 하나씩 바꾼다.** 해상도를 내렸을 때 GPU 패스가 짧아지면 픽셀 비용을 확인한다. CPU 렌더 제출이 길면 상태 전환·그리기 호출·배칭이 후보이고, 그림자·스키닝·파티클이 지배하면 패스별로 확인한다. 첫 진입만 늦으면 I/O·압축 해제·GPU 업로드·PSO 컴파일을 구별한다. 동적 해상도를 쓰면 품질과 GPU 비용의 관계를 그 플랫폼에서 다시 잰다. [Unity 렌더링 캡처](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/graphics-performance-profiling/profile-rendering) · [Unreal 동적 해상도](https://dev.epicgames.com/documentation/en-us/unreal-engine/dynamic-resolution-in-unreal-engine) · [Unreal PSO Precaching](https://dev.epicgames.com/documentation/unreal-engine/pso-precaching-for-unreal-engine) · [Unity PSO 워밍업](https://docs.unity.com/en-us/engine/6000.3/manual/materials-and-shaders/shaders/shader-troubleshooting/shader-reduce-stalling/shader-prevent-stutter/shader-pso-trace-warming/shader-pso-introduction)
3. **절감한 시간과 새 비용을 같이 잰다.** 인스턴싱·배칭은 제출을 줄일 수 있고, 선택한 배칭 방식에 따라 메모리·컬링 단위·셰이더 요구가 달라진다. 프러스텀·가림 컬링은 제출을 줄이되 대규모 가리는 물체가 적은 씬에서는 검사 비용의 가치가 작을 수 있다. 거리 LOD·HLOD는 실루엣과 전환, 그림자, 빠른 시점 이동을 확인한다. 패스 자체를 줄였으면 반사, 투명도, 포스트프로세스 등 빠진 효과가 허용되는지 본다. [Unity 그리기 호출 최적화](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/graphics-performance-profiling/reduce-draw-calls/optimizing-draw-calls-choose-method) · [Unity URP GPU 컬링](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/graphics-performance-profiling/in-urp/gpu-culling) · [Unreal 가시성·가림](https://dev.epicgames.com/documentation/en-us/unreal-engine/visibility-and-occlusion-culling-in-unreal-engine)

| 자료 | 무엇을 배우는가 |
| --- | --- |
| **Hoppe, SIGGRAPH 1996 · Progressive Meshes** | 메시를 단계적으로 단순화해 필요한 정밀도를 선택하는 방법의 기초다. 게임에서는 화면 크기와 형태 오차, 전환 안정성을 판단 기준으로 옮긴다. [논문](https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Hoppe96.pdf) |
| **Bittner 외, 2004 · Coherent Hierarchical Culling** | 순진한 하드웨어 가림 질의가 응답 대기 때문에 오히려 느려질 수 있음을 설명한다. 계층적 공간 구조와 이전 프레임의 시간적 일관성을 이용한다. 가리는 구조가 다른 레벨에서 전후 비용을 따로 확인할 이유다. [논문](https://www.cg.tuwien.ac.at/research/publications/2004/Bittner-2004-CHC/Bittner-2004-CHC-Paper.pdf) |
| **Haar·Aaltonen, SIGGRAPH 2015 · GPU-Driven Rendering Pipelines** | 렌더 제출과 가시성 처리 일부를 GPU로 옮기는 사례다. CPU 제출을 줄여 얻은 이득과 GPU 쪽 작업·데이터 비용의 이동을 비교해 읽는다. [발표 슬라이드](https://advances.realtimerendering.com/s2015/aaltonenhaar_siggraph2015_combined_final_footer_220dpi.pdf) |
| **Karis 외, SIGGRAPH 2021 · Nanite** | 계층적 클러스터, 가시성, 스트리밍, 래스터 경로를 함께 다루는 실무 자료다. 실제 적용은 프로젝트의 재질과 가려진 미세 형상, 그림자, 플랫폼의 비용을 확인한다. [발표 영상](https://www.youtube.com/watch?v=eviSykqSUUw) · [SIGGRAPH 자료](https://advances.realtimerendering.com/s2021/Karis_Nanite_SIGGRAPH_Advances_2021_final.pdf) · [Epic 기술 문서](https://dev.epicgames.com/documentation/en-us/unreal-engine/nanite-technical-details) |
| **O’Donnell · Frostbite FrameGraph, GDC 2017** | 패스의 읽기·쓰기와 리소스 수명을 명시해 기능 모듈화와 렌더 리소스 관리가 어떻게 연결되는지 보여준다. 엔진을 직접 개발하는 경우와 이미 엔진의 그래프에 패스를 추가하는 경우 작업 범위가 다르다. [GDC 발표](https://www.gdcvault.com/play/1024612/) |
| **Joshua Simmons · Snowdrop, GDC 2024** | Avatar에서 절차적으로 배치한 밀도 높은 월드와 협동 플레이를 지원하기 위해 엔진을 변경한 사례다. 렌더링 최적화의 범위를 정할 때 콘텐츠 밀도와 시뮬레이션·호스팅 비용도 함께 고려하게 한다. [GDC 발표](https://www.gdcvault.com/play/1034412/Upgrading-the-Snowdrop-Engine-for) · [개발팀 기술 소개](https://www.massive.se/article/crafting-pandoras-breathtaking-landscape-with-snowdrop/) |

## 3. 실시간 생성, 풀, 캐시, 스트리밍을 고르는 기준

| 선택 | 선택 조건 | 비용과 실패를 확인할 방법 |
| --- | --- | --- |
| **그때 생성하고 해제** | 호출이 드물고 지연이 예산 안이거나, 초기화할 상태가 복잡해 재사용 위험이 크다. | 대량 동시 생성이 있는 대표 장면에서 p99와 메모리를 확인한다. GC나 네이티브 해제 시점이 예상과 맞는지 본다. |
| **풀로 재사용** | 투사체·일시 효과처럼 비슷한 형태가 자주 반복되고 생성·해제가 실제로 비싸다. | 상한과 고갈 정책, 리셋할 HP·타이머·콜백·물리 상태를 정한다. 재사용 전 세대의 지연 콜백이 새 객체를 건드리는 경우를 시험한다. 상주 메모리와 활성화 비용도 잰다. |
| **파생 결과를 캐시** | 같은 입력으로 다시 읽는 비용이 크고 재사용 가능성이 높다. Nav 경로의 일부, 빌드 결과, 선택한 리소스가 후보가 된다. | 키에 입력·버전·필요한 공간 범위를 넣는다. 변경 시 무효화하고 상주 메모리 예산, 캐시 적중으로 절감한 시간, 오래된 값 사용을 측정한다. 이동 경로가 한 번만 훑는 지역이 자주 쓰는 결과를 밀어내는지도 확인한다. |
| **미리 굽기** | NavMesh·라이트맵·정적 배치처럼 상태 변화가 적고 오프라인 비용으로 런타임을 줄일 수 있다. | 원본 변경 이후 새 결과를 배포하는지, 업데이트 비용과 산출물 크기가 수용 가능한지 확인한다. 파괴·문 열림처럼 바뀌는 조건은 별도 갱신 전략을 둔다. |
| **비동기 프리페치·스트리밍** | 공간이나 진행 상태로 다음 필요 자원을 예측할 수 있고 전체 상주가 비싸다. | I/O → 압축 해제 → 활성화·업로드를 별도 예산으로 본다. 즉시 필요한 요청을 우선하고, 경로가 바뀌면 오래된 요청의 결과를 안전하게 해제한다. 왕복 이동·텔레포트·느린 저장장치·메모리 압박에서 측정한다. |
| **런타임 절차 생성** | 입력 조합이 많고 고정된 산출물을 모두 저장하기 어렵거나 생성 자체가 플레이의 일부다. | 시드·생성기 버전·플레이 변경분의 소유자를 정한다. 재로딩과 버전 변경에서 동일 상태가 필요한 경우를 테스트한다. 비용 큰 결과는 재사용이 측정되는 경우에만 캐시한다. |

풀은 **재사용할 객체를 보관**하고 캐시는 **다시 얻기 비싼 결과를 보관**한다. 성능 문제가 있는 시점이 생성인지 최초 로드·셰이더 컴파일인지 구별해야 효과적인 수단을 고를 수 있다. 선로딩 범위의 초기 추정은 `예상 이동 속도 × 자원 준비 시간 + 여유 거리`로 잡을 수 있다. 이후 고속 이동, 진입·이탈 범위 차이, 같은 리소스의 로드·언로드 반복을 측정한다. 로드가 끝났어도 한 프레임에 대량 활성화하면 끊길 수 있어 활성화 예산을 별도로 둔다. [Nystrom Object Pool](https://gameprogrammingpatterns.com/object-pool.html) · [Dirty Flag](https://gameprogrammingpatterns.com/dirty-flag.html) · [Unity 풀링 지침](https://docs.unity.com/en-us/engine/6000.3/manual/analysis/performance-memory/managed-memory/optimizing-code-managed-memory/reusable-code)

| 자료 | 적용할 지점 |
| --- | --- |
| **Elan Ruskin · Sunset Overdrive, GDC 2015** | 오픈월드 이동과 레벨 제작 방식이 스트리밍 기술에 주는 제약을 살펴본다. 맵 데이터와 로드 순서를 함께 설계해야 할 때 참고한다. [GDC 발표](https://www.gdcvault.com/play/1022268/Streaming-in-Sunset-Overdrive) · [슬라이드](https://media.gdcvault.com/gdc2015/presentations/Ruskin_Elan_SunsetOverdriveStreaming.pdf) |
| **Chad Barb · Titanfall 2, GDC 2017** | 텍스처를 미리 선택하는 데이터와 런타임 GPU 피드백을 다룬다. 여러 하드웨어에서 메모리와 화질을 함께 관리한 사례다. [영상](https://www.youtube.com/watch?v=4BuvKotqpWo) · [슬라이드](https://media.gdcvault.com/gdc2017/Presentations/Barb_Chad_EfficientTextureStreaming.pdf) |
| **Innes McKendrick · No Man’s Sky, GDC 2017** | 연속적인 월드 생성과 작업 분배를 설명한다. 절차 생성도 준비 지연과 스케줄링을 관리해야 한다는 점을 살핀다. [GDC 발표](https://www.gdcvault.com/play/1024265/Continuous-World-Generation-in-Noby) |
| **Megiddo·Modha, FAST 2003 · ARC** | 빈도·최근성을 조정하고 순차 스캔에 덜 흔들리는 캐시 교체 방식의 저장 시스템 논문이다. 게임에서는 한 번 훑는 스트리밍 루트와 반복 방문에서 캐시 교체 정책이 어떻게 달라지는지 비교하는 가설로 쓸 수 있다. [논문](https://www.usenix.org/legacy/publications/library/proceedings/fast03/tech/full_papers/megiddo/megiddo.pdf) |
| **엔진 스트리밍과 플랫폼 I/O** | Unreal World Partition은 스트리밍 소스와 셀, Unity Addressables는 핸들과 번들의 참조 카운트를 확인한다. 다운로드 파일이 디스크에 캐시된 상태와 GPU에서 사용할 수 있는 상태를 구별한다. Xbox의 DirectStorage는 I/O 예산이 실제 압축·전송 경로와 묶이는 플랫폼 사례다. [World Partition](https://dev.epicgames.com/documentation/en-us/unreal-engine/world-partition-in-unreal-engine) · [Addressables 메모리 2.7](https://docs.unity3d.com/Packages/com.unity.addressables@2.7/manual/MemoryManagement.html) · [DirectStorage](https://learn.microsoft.com/en-us/xbox/gdk/docs/features/console/storage/directstorage/directstorage-overview?view=gdk-2604) |

## 4. 몬스터·NPC AI 설계

**게임에서 보이고 전달되어야 할 행동을 먼저 적는다.** 경비가 소리를 들으면 확인하러 가는지, 공격 중 피격되면 취소되는지, 적이 길을 잃었을 때 플레이어가 어떤 신호를 보는지가 설계의 출발점이다. 이를 `감지 → 관찰 기억 → 결정 → 행동 실행 → 결과`로 따라가며 근거·시각·유효기간을 기록한다. 이동 계획, 지역 회피, 애니메이션, 피해 계산은 분리해 각각 실패할 수 있게 한다. 역할과 행동이 늘어날 때 목표·전제 조건·실패 처리·취소를 테스트한다. [Halo 2의 행동 설계](https://www.gamedeveloper.com/programming/gdc-2005-proceeding-handling-complexity-in-the-i-halo-2-i-ai) · [게임 플래닝 분석 논문](https://cdn.aaai.org/ojs/12728/12728-52-16245-1-2-20201228.pdf)

| 선택 | 잘 맞는 상황 | 주의할 실패와 참고 자료 |
| --- | --- | --- |
| **FSM·계층 상태 머신** | 보스 단계, 공격 예고 → 발동 → 회복, 경비가 순찰·경계·귀환하는 비교적 명확한 모드 | 전이가 많아지면 공통 취소 정책과 하위 상태의 책임을 정한다. 진입·종료 부작용을 확인한다. [Unreal StateTree](https://dev.epicgames.com/documentation/en-us/unreal-engine/overview-of-state-tree-in-unreal-engine) |
| **Behavior Tree** | 조건과 우선순위가 명확한 몬스터, 재사용할 서브트리, 디자이너가 경로를 시각적으로 편집하는 상황 | 실행 중 우선순위가 바뀌면 행동을 중단·정리하는지 확인한다. 노드의 `running/success/failure` 의미를 고정하고 Blackboard의 쓰기 주체를 추적한다. Unreal BT는 이벤트 중심 동작을 문서화한다. [Iovino 외 문헌 조사](https://arxiv.org/abs/2005.05842) · [Unreal BT](https://dev.epicgames.com/documentation/en-us/unreal-engine/behavior-tree-in-unreal-engine---overview) · [Unity Behavior 그래프](https://docs.unity.cn/Packages/com.unity.behavior%401.0/manual/behavior-graph.html) |
| **Utility AI** | 체력·거리·자원·동료 상황을 점수화해 여러 유효 행동 중 고르는 NPC | 점수의 단위와 응답 곡선, 동점·기존 행동 유지 기준을 조정한다. 선택 이유와 후보 점수를 로그에 남기고 작은 값 차이로 행동을 반복 전환하는지 본다. [Dave Mark·Kevin Dill, GDC 2010](https://media.gdcvault.com/gdc10/slides/MarkDill_ImprovingAIUtilityTheory.pdf) |
| **GOAP·HTN** | 장애물이 생기거나 수단이 여러 개여서 목표를 달성하는 행동 순서가 바뀌는 NPC | 계획 탐색 시간·확장 노드·재계획 수에 한도를 둔다. 무계획·실패 시 대체 행동을 두고 계획 데이터와 실행 상태가 달라지는 경우를 검증한다. F.E.A.R.의 GOAP, Killzone 3 등의 HTN 사례는 계획 성공률과 플레이에서 적절했는지의 차이를 함께 보여준다. [Orkin 발표](https://gdcvault.com/play/1013459/Three-States-and-a-Plan) · [세 FPS의 플래닝 분석](https://cdn.aaai.org/ojs/12728/12728-52-16245-1-2-20201228.pdf) |
| **그룹·연출 제어** | 무리의 공격 순서, 도로 진입 순번, 조우의 긴장과 휴식을 조절할 때 | 개별 NPC의 결정과 별도로 스폰·좌석·공격 슬롯 등의 공유 자원을 소유한다. 그룹이 예산을 넘기거나 개별 NPC가 자원을 동시에 점유하는지 본다. Left 4 Dead는 감독이 조우 흐름을 조절한 사례다. [Valve 발표 영상](https://www.gdcvault.com/play/1422/) · [원 발표 자료](https://cdn.fastly.steamstatic.com/apps/valve/2009/GDC2009_ReplayableCooperativeGameDesign_Left4Dead.pdf) |

경로 선택과 회피도 분리한다. NavMesh·공유 경로는 통과 가능한 길을 찾고, 지역 회피는 주변 이동에 반응하며, 점유·진입 제한은 좁은 문과 병목의 순서를 관리한다. 지역 회피에 출구나 양보 규칙이 없으면 멈춤이 지속될 수 있다. 실제 배치에서 경로 실패, 예산 초과, 대기 시간, 교착 후 복구를 본다. Unity AI Navigation과 Unreal AI Perception은 경로·감지 도구의 출발점이며 행동 결정의 계약은 게임에서 정한다. [Recast·Detour 원 코드](https://github.com/recastnavigation/recastnavigation) · [ORCA 논문과 코드](https://gamma-web.iacs.umd.edu/ORCA/) · [Unity AI Navigation](https://docs.unity.com/en-us/engine/6000.3/manual/packages-list/packages-all/pack-safe/com-unity-ai-navigation) · [Unreal AI Perception](https://dev.epicgames.com/documentation/en-us/unreal-engine/ai-perception-in-unreal-engine) · [OneStep 군중 자료](../../knowledge/game/K-GAME-TECH-CROWD.kr.md)

## 5. 보이지 않는 오브젝트와 NPC

게임에는 가시성 외에도 소리, 그림자·반사, 충돌, 전투 효과, 퀘스트, 다른 카메라·네트워크 관찰자가 있다. **렌더 가시성, 애니메이션, 물리·충돌, AI, 네트워크 복제, 메모리 상주를 각각 판단한다.** 예를 들어 화면 밖의 추격자가 가까이 있으면 소리·충돌·위험한 행동은 필요할 수 있다. 반대로 저 멀리 같은 출근 경로를 걷는 시민은 일정과 다음 도착 시각만 기록해도 충분한 게임이 있다. [Carlson·Hodgins, 1997](https://graphicsinterface.org/proceedings/gi1997/gi1997-1/) · [Unreal Mass Gameplay](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-gameplay-in-unreal-engine)

| 상태 | 할 일 | 넘어가기 전에 확인할 것 |
| --- | --- | --- |
| **전체 갱신** | 근접 전투, 중요 NPC, 카메라에 크게 보이는 객체의 감지·이동·애니메이션·충돌을 필요한 정밀도로 유지한다. | 긴 프레임에서 무엇이 비용을 올리는지와 게임 규칙의 최소 갱신 조건 |
| **부분 갱신** | AI·감지·애니메이션 빈도를 각각 줄이고 여러 개체의 갱신을 프레임에 나눈다. 중요한 이벤트는 즉시 깨울 수 있게 한다. | 최대 반응 지연, 충돌·메시지 순서, 정지한 것이 갑자기 움직이는 시각적 부작용 |
| **요약 시뮬레이션** | 안정적인 ID, 지역·목표·도착 예정·HP·퀘스트 상태를 유지하고 사건 기반 또는 낮은 빈도로 진행한다. 필요하면 집단 단위 결과를 계산한다. | 정상 승격 전에 결과를 한 번만 반영하고, 유효한 위치에서 복원하며, 보장한 전투·퀘스트 규칙을 지키는지 |
| **정지·언로드** | 게임에서 활동을 멈춰도 되는 객체의 다음 시간 또는 지속 상태를 저장하고 무거운 표현·리소스를 푼다. 지운 객체는 저장된 처치·폐기 기록으로 구분한다. | 재진입 시 중복 스폰, 처치된 대상의 부활, 자원 누수, 장기간 미접속 후 일괄 재생성으로 인한 끊김 |

전이를 결정할 때 거리와 화면 여부 외에 **전투 관여, 야기할 피해, 목표의 중요도, 최근 상호작용, 가장 가까운 관련 플레이어**를 입력으로 고려한다. 경계 왕복은 승격·강등의 서로 다른 임곗값이나 최소 체류 시간으로 완화한다. 전환 중에는 타이머·이벤트·지역 점유의 권한을 넘겨 한쪽만 쓰게 한다. 장기간의 진행은 필요한 결과만 계산하고 한 프레임에 밀린 모든 갱신을 몰아서 수행하지 않도록 제한한다. 카메라의 일부만 보이는 분할 화면과 멀티플레이는 모든 관련 관찰자를 기준으로 검증한다. [Chenney, GDC 2001](https://pages.cs.wisc.edu/~schenney/research/culling/chenney-gdc2001.pdf) · [Epic Significance Manager](https://dev.epicgames.com/documentation/unreal-engine/significance-manager-in-unreal-engine)

가령 카메라 밖의 닫힌 문은 그리기를 생략해도 NPC의 경로와 충돌에는 남아야 할 수 있다. 퀘스트 동료의 전환에서는 대사·목표·사망 상태와 서버 권한을 보존하고, 애니메이션과 사소한 발 위치는 재진입 때 구성할 수 있다. 장식용 군중은 지속되는 개별 신원이 요구되지 않을 때 지역의 밀도와 흐름만 유지할 수 있다. 이러한 보존 항목을 먼저 정하면 전체 갱신과 요약 모드를 동일한 장기 입력으로 실행해 어떤 결과 차이를 허용할지 판단할 수 있다. [Simulation Level-of-Detail](https://pages.cs.wisc.edu/~schenney/research/culling/chenney-gdc2001.pdf) · [S.T.A.L.K.E.R. 개발자 인터뷰](https://www.gamedeveloper.com/game-platforms/interview-inside-the-ai-of-i-s-t-a-l-k-e-r-i-)

| 자료 | 확인할 내용 |
| --- | --- |
| **Carlson·Hodgins, 1997 · Simulation Levels of Detail** | 시뮬레이션에서 중요한 대상과 덜 중요한 대상에 다른 정확도를 쓴 원 연구다. 단순화한 행동도 관찰 가능한 부분에서 충분한지 평가하는 출발점이다. [논문 안내 및 원문](https://graphicsinterface.org/proceedings/gi1997/gi1997-1/) |
| **O’Sullivan 외, 2002 · Levels of Detail for Crowds and Groups** | 군중의 표현, 애니메이션, 시뮬레이션에 LOD를 적용하는 연구다. 집단 단위의 단순화와 중요한 개체 보존의 차이를 읽는다. [논문](https://secom.ru.is/publications/CGF2002.pdf) |
| **S.T.A.L.K.E.R. · Dmitriy Iassenev 인터뷰** | 개발자는 근접 캐릭터의 자세한 행동과 원거리 캐릭터의 요약 행동을 구별했다고 설명한다. 원거리에서도 이동과 전투 등의 결과가 생기며 근접 모드 진입 때 이어진다. 지속적인 생태계가 실제로 필요한 게임의 사례다. [개발자 인터뷰](https://www.gamedeveloper.com/game-platforms/interview-inside-the-ai-of-i-s-t-a-l-k-e-r-i-) |
| **Assassin’s Creed Unity · GDC 2015** | 대규모 군중에 AI 재활용을 적용한 사례다. 주변 인구 밀도와 활동을 유지할 때 필요한 개체 정밀도와 재활용 비용을 살펴본다. [GDC 세션](https://www.gdcvault.com/play/1022411/massive-crowd-on-assassin-s) · [영상](https://www.youtube.com/watch?v=Rz2cNWVLncI) |
| **Epic Mass 및 Unity CullingGroup** | Mass는 표현·시뮬레이션·복제 LOD를 각각 제공한다. Unity CullingGroup은 카메라에 대한 가시성과 거리 구간을 제공하고 Animator의 컬링은 스켈레톤 갱신에 영향을 준다. 어느 경우든 프로젝트의 퀘스트·충돌·AI가 요구하는 조건은 별도로 구현·검증한다. [Epic Mass](https://dev.epicgames.com/documentation/unreal-engine/overview-of-mass-gameplay-in-unreal-engine) · [Animation Budget Allocator](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-budget-allocator-in-unreal-engine) · [Unity CullingGroup](https://docs.unity.com/en-us/engine/6000.5/manual/cameras/occlusion-culling/culling-group-api/api) · [AnimatorCullingMode](https://docs.unity.com/en-us/engine/6000.0/script-reference/unityengine/animatorcullingmode) |

## 6. 한 장면에서 함께 검증하는 방법

작은 **마을 → 숲 입구 → 교전 → 마을 복귀** 루트를 기준으로 삼는다. 마을에는 퀘스트 NPC와 장식용 시민이 있고 숲에는 전투 몬스터와 선택 가능한 콘텐츠 팩을 둔다. 목표 기기와 프레임 간격을 정하고, 화면 밖 전투·이동·저장 중 현재 게임이 약속하는 동작을 각 사례에 고정한다. 되돌아올 때 이전 상태를 포함해 새 엔진 실행에서 재현할 수 있어야 한다.

| 실험 | 방법 | 기록할 판정 |
| --- | --- | --- |
| 데이터 추가·수정·삭제 | 몬스터 팩을 추가한 뒤 수치와 표시 이름을 변경하고, 저장이 참조하는 정의 하나를 교체한다. 구버전 저장을 로드한다. 중복·누락 참조를 넣은 후보도 사용한다. | 지원하는 저장은 전투·퀘스트를 이어가고, 잘못된 데이터는 어느 ID와 참조가 문제인지 보고한다. |
| 렌더링 | 같은 이동·카메라·기기에서 기준판과 후보판을 비교한다. 좁은 골목과 넓은 숲, 야간 조명과 군중 장면을 나눠 캡처한다. | CPU·GPU별 프레임 시간, p95/p99, 예산 초과 횟수, 그림자·시각 전환·가시성 오류 |
| 생성·풀·스트리밍 | 캐시가 비어 있는 첫 진입과 반복 방문을 구별한다. 예상 경로 이탈과 순간이동을 실행하고 스폰 요청을 한꺼번에 몰아 넣는다. | 활성화의 프레임 비용, 로드 준비 지연, 피크 메모리, 오래된 요청 취소, 객체 재사용 후 중복 콜백이 없는지 |
| AI와 화면 밖 | 장애물·소리·실패한 경로·지원 단절을 넣고, 전투 중 시야 밖으로 갔다가 돌아온다. 두 관찰자가 있는 게임이면 한 명만 이탈시킨다. | 행동과 취소 이유, 반응 지연, 중복 공격·복제·스폰, 퀘스트·처치 기록이 요구대로 이어지는지 |

OneStep에서 AI가 이 작업을 맡으면 초기 브리프에 **데이터 및 상태 소유자, 관찰 가능한 게임 규칙, 플랫폼별 예산, 실행할 루트**를 적는다. 기능을 추가하는 B 팩과 기존 A 팩의 참조를 실제 빌드에서 분리해 보는 방식은 앞선 [C++·Unreal 작업 사례](../examples/cpp-gameplay-workflow/README.md)와 이어진다. 최적화 후보는 같은 입력에서 성능과 게임 결과를 함께 기록하고, 결과가 부족한 지점은 코드·에셋·시뮬레이션 어느 상태가 원인인지 추적한다. [OneStep 코드 검증](../../skills/vegabond-code/references/verification.kr.md) · [성능 측정 지식](../../knowledge/code/K-CODE-PERFORMANCE-MEASUREMENT.kr.md)

### 자료를 보는 순서

1. **데이터와 제작**은 Bungie의 에셋 파이프라인과 Factorio의 마이그레이션부터 읽는다. 에셋 변경 비용과 이전 저장 호환성이라는 두 종류의 문제를 비교할 수 있다.
2. **프레임과 메모리**는 Unity 또는 Unreal의 프로파일러 문서로 한 프레임을 읽은 뒤 Titanfall 2와 Nanite 발표로 넘어간다. 실제로 시간을 먹는 단계에 맞춰 자료를 고를 수 있다.
3. **NPC와 세계**는 Halo 2와 F.E.A.R.에서 행동 결정의 경계를 보고, S.T.A.L.K.E.R.와 Assassin’s Creed Unity에서 화면 밖 세계를 얼마나 유지했는지를 비교한다.

영상은 공개 세션 설명·발표 슬라이드와 함께 안내했다. 출시작 사례는 각 개발팀의 문제와 해결 비용을 보여주며, 논문의 모델은 특정 조건에서의 근거를 제공한다. 이 문서는 적용 기준과 검증 방법을 정리한 조사이며 위 테스트 장면의 실행 결과를 포함하지 않는다.

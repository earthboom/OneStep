# C# 어셈블리·에셋·Player에서 Unity 게임플레이 경계 검증하기

K-CODE-UNITY-GAMEPLAY-FRAMEWORK · 방법 · 적용 중 · 근거 확인 2026-11-22

정의 에셋, 가변 세션, 표현의 소유자를 정한다. 어셈블리 의존 방향, 직렬화 참조, 실제 로드·정리 동작을 지원 대상 Player에서 검증한다.

적용 범위 — Unity C# 프로젝트의 버전별 직렬화·Addressables·수명·백엔드·선택 콘텐츠.

## 적용 방법

대표 플레이에서 시작한다. 전술·카드는 명령 검증, 해결 순서, 재현 가능한 상태가 중요하다. 액션은 입력을 의도로 바꾸는 지점, 비용·쿨다운 소유자, 결과를 받는 표현이 필요하다. 네트워크 게임은 권한 결과와 보정, 콘텐츠 게임은 고정 정의와 세션별 상태를 정한다. 대량 시뮬레이션은 실제 접근 패턴을 측정한 뒤 Entities를 검토한다.

Unity 진입점에서 규칙 소유자를 호출하도록 둔다. 엔진과 분리할 이유가 있는 단위엔 .asmdef와 No Engine References를 쓸 수 있다. 초기에는 폴더와 작은 공개 API만으로 충분할 수 있다. 초기화·실패·취소 계약을 공유할 때 공통 기반 타입을 쓴다. Inspector 입력은 직렬화 필드로 노출한다. ScriptableObject는 공유 정의를 공급하고 세션 객체는 체력·진행을 소유한다. 의도적으로 가변 에셋을 공유하면 작성자와 초기화 규칙을 정한다. 대상이 정해진 명령은 직접 요청하고 Event Channel은 알림에 쓴다.

직렬화 참조, 번들 의존성, 동적 키를 따로 추적한다. 에셋과 .meta GUID를 함께 관리하고 필드 이름이나 타입·어셈블리를 옮긴 뒤 Prefab 오버라이드를 확인한다. FormerlySerializedAs는 필드 이름 변경을 돕고 SerializeReference는 다형·공유 참조용이다. 실제 이전 에셋과 별도 세이브 파일을 읽어 본다. Addressables 핸들마다 소유자와 실패·취소·재진입 시 해제 경로를 정한다.

## 적용 조건과 예외

활성 기간 구독은 비활성화 때 해제한다. 파괴 토큰은 작업이 관찰해야 하며 풀 재사용·씬 전환의 모든 경우를 처리하지 않는다. Domain Reload를 끄면 연속 Play에서 정적 구독이 남을 수 있다. 리플렉션·제네릭·스트리핑은 에디터 컴파일만으로 릴리스 Player의 동작을 확인할 수 없다. 인용한 Unity 6.3 언어 문서와 Addressables 1.21·2.7 자료의 버전이 다르므로 설치된 패키지·백엔드를 확인한다.

## 확인 방법

에디터·패키지·플랫폼·백엔드·진입 씬을 기록한다. .cs, .asmdef, 씬, Prefab, ScriptableObject, .meta, 설정과 번들 변경을 함께 본다. Edit Mode에서 규칙, Play Mode에서 시작·정리, 대상 Player에서 실제 팩 포함 여부를 검사한다. 기본·A·B·동시 구성을 실행하고 A의 프리팹을 실제로 제외한 B를 연다. 금지한 참조를 일부러 넣어 검출되는지 확인한다. 풀 재사용, 로드 중 씬 이탈, 연속 Play, 이전 에셋 재로드를 반복한다. 다음 한두 번의 콘텐츠 변경에서 손댄 파일·등록점·작업량을 기록한다.

## 근거

11월 22일 조사는 Unity 문서, Chop Chop, Boss Room, 출시작 사례와 연구를 비교했다. 아키텍처 리뷰는 논문 36편, 코드 스멜 연구는 설문 68명과 Unity 프로젝트 100개, UnityBench-Mini3D는 단기 과제 77개에 검사 1,178개를 사용했다. Core ECS는 형식 모델이고 타워 디펜스 비교는 해당 작업량의 결과다. Unity A/B 실험은 C++ 예제를 포팅해 실행한 결과가 아닌 제안이다.

[C++ 게임플레이 실험](K-CODE-CPP-GAMEPLAY-FRAMEWORK.md) · [자원 소유권](K-CODE-RESOURCE-OWNERSHIP.md) · [게임플레이 회귀](../game/K-GAME-GAMEPLAY-REGRESSION.md)

- [Unity assemblies](https://docs.unity.com/en-us/engine/6000.3/manual/programming-environment/script-compilation/assembly-definition-files/class-assembly-definition-importer) · [UnityBench-Mini3D](https://arxiv.org/abs/2610.35980) · [Unity release policy](https://unity.com/releases/unity-6/support) · [Project manifest](https://docs.unity.com/en-us/engine/6000.3/manual/packages-list/managing-packages-manifest/upm-manifest-prj) · [CoreCLR progress update](https://discussions.unity.com/t/coreclr-scripting-and-net-update-october-2026/1738338)
- [Mizutani, Daros, and Kon, 2021 — Authors' copy](https://users.ime.usp.br/~kon/papers/SoftwareArchitectureForDigitalGameMechanics2021.pdf) · [Borrelli et al., MSR 2020 — Conference paper and materials](https://2020.msrconf.org/details/msr-2020-papers/15/Detecting-Video-Game-Specific-Bad-Smells-in-Unity-Projects) · [Borrelli et al., MSR 2020 — Follow-up UnityLint tool paper](https://mdipenta.github.io/files/icpc2023-unitylinter.pdf) · [Redmond et al., OOPSLA 2025 — Paper](https://arxiv.org/abs/2508.15264) · [Tasnim and Zhao, SAC 2026 — Paper](https://arxiv.org/abs/2606.14919)
- [Official Unity video](https://www.youtube.com/watch?v=raQ3iHhE_Kk) · [Speaker's code](https://github.com/roboryantron/Unite2017) · [Official Unity video](https://www.youtube.com/watch?v=VBA1QCoEAX4) · [Unity's current ScriptableObject design resources](https://unity.com/how-to/architect-game-code-scriptable-objects) · [Public source and architecture wiki](https://github.com/UnityTechnologies/open-project-1/wiki/Game-architecture-overview)
- [Official development video](https://www.youtube.com/watch?v=WLDgtRNK2VE) · [Sample source](https://github.com/Unity-Technologies/com.unity.multiplayer.samples.coop) · [Architecture documentation](https://mp-docs.dl.it.unity3d.com/netcode/1.8.1/learn/bossroom/bossroom-architecture/) · [Development team's account](https://blog.stunlock.com/v-rising-dev-update-4-v-rising-engine-and-cutting-edge-technology/) · [Unity case study and developer interview](https://unity.com/resources/stunlock-studios-v-rising)
- [Unity case study with developer interview](https://unity.com/resources/marvel-snap) · [GCAP video](https://www.youtube.com/watch?v=2j7AJj1oRSQ) · [Unpacking — Talk details](https://confpad.io/conferences/gcap-2023-empower/empowering-design-the-tools-and-pipelines-of-unpacking) · [Xbox Wire developer interview](https://news.xbox.com/en-us/2023/04/13/vampire-survivors-dlc-2-launch/) · [Unity 6 pattern resources](https://unity.com/blog/game-programming-patterns-update-ebook)
- [Sample repository](https://github.com/Unity-Technologies/game-programming-patterns-demo) · [Unity pattern examples and Robert Nystrom's book — Author's edition](https://gameprogrammingpatterns.com/contents.html)
- [Unity Network Simulator](https://mp-docs.dl.it.unity3d.com/tools/current/tools-network-simulator/) · [Entities system order 1.4](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/systems-update-order.html) · [Baking 1.4](https://docs.unity3d.com/Packages/com.unity.entities@1.4/manual/baking-overview.html) · [Official ECS samples](https://github.com/Unity-Technologies/EntityComponentSystemSamples)
- [Unity packages](https://docs.unity.com/en-us/engine/6000.3/manual/packages-list/packages/upm-overview) · [Serialization rules](https://docs.unity.com/en-us/engine/6000.3/manual/programming-environment/code-reload-serialization/script-serialization/rules) · [Separating data and logic](https://unity.com/how-to/separate-game-data-logic-scriptable-objects) · [GetDependencies](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/AssetDatabase.GetDependencies.html) · [Analyze 1.21](https://docs.unity3d.com/Packages/com.unity.addressables@1.21/manual/AnalyzeTool.html)
- [Build Layout 2.7](https://docs.unity3d.com/Packages/com.unity.addressables@2.7/manual/BuildLayoutReport.html) · [Asset metadata](https://docs.unity.com/en-us/engine/6000.3/manual/assets-and-media/import-assets/asset-metadata) · [FormerlySerializedAs](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Serialization.FormerlySerializedAsAttribute.html) · [SerializeReference](https://docs.unity.com/en-us/engine/6000.3/script-reference/unityengine/serializereference) · [Event execution order](https://docs.unity.com/en-us/engine/6000.3/manual/scripting/managing-update-order/event-functions)
- [Domain Reload](https://docs.unity3d.com/6000.3/Documentation/Manual/domain-reloading.html) · [Awaitable and threads](https://docs.unity.com/en-us/engine/6000.3/manual/scripting/programming-distribute-work-threads/async-await-support/async-awaitable-continuations) · [Destruction cancellation token](https://docs.unity3d.com/6000.3/Documentation/ScriptReference/MonoBehaviour-destroyCancellationToken.html) · [.NET cancellation model](https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads) · [C# version](https://docs.unity3d.com/6000.3/Documentation/Manual/csharp-compiler.html)
- [IL2CPP restrictions](https://docs.unity3d.com/6000.3/Documentation/Manual/scripting-restrictions.html) · [Code stripping](https://docs.unity3d.com/6000.3/Documentation/Manual/managed-code-stripping.html) · [Profiler documentation](https://docs.unity3d.com/6000.3/Documentation/Manual/profiler-profiling-applications.html) · [Official Unity Profiler video](https://www.youtube.com/watch?v=xjsqv8nj0cw) · [Addressables memory 2.7](https://docs.unity3d.com/Packages/com.unity.addressables@2.7/manual/MemoryManagement.html)
- [Content updates 2.7](https://docs.unity3d.com/Packages/com.unity.addressables@2.7/manual/content-update-builds-overview.html)
- [Unity Test Framework modes 1.4](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/edit-mode-vs-play-mode-tests.html) · [Command line 1.4](https://docs.unity3d.com/Packages/com.unity.test-framework@1.4/manual/reference-command-line.html) · [Prefab YAML](https://docs.unity.com/en-us/engine/6000.3/manual/working-with-scenes/text-scene-format/yaml-prefab-serialization) · [Smart Merge](https://docs.unity.com/en-us/engine/6000.3/manual/get-started/project-configuration/version-control/smart-merge)

# 스테이지 대사의 선택·중단·결과 확정은 누가 맡고 현지화와 저장은 어떻게 연결할까?

식별자 `K-GAME-STAGE-DIALOGUE` · 참고 자료 · 사용 중 · 근거 확인일 2026-11-23

**요약** 안정적인 대사 ID로 번역·음성·초상화를 연결한다. 스테이지 배치는 대화 후보를 고르고 세션은 임시 입력·연출을 관리하며 영속 게임 상태가 퀘스트 결과를 한 번만 적용한다.

**적용 범위** 반응 대사·상호작용 대화·연출 장면을 갖춘 게임의 스테이지 통합 설계와 회귀 점검

**검색어** stage dialogue, conversation, dialogue session, LineId, storylet, interruption, resume, localization, voice-over, Yarn Spinner, ink, FText, String Table, SignalEmitter, Sequencer Event Track, 스테이지 대사, 대화 세션, 대사 ID, 대화 중단, 재개, 재방문, 보상 중복, 현지화, 자막

## 활용 방법

작가가 흔히 하는 수정에 맞춰 형식을 고른다. 개별 인사말은 표에 적고, 선택지와 재합류 분기를 따라가야 하면 스크립트나 그래프를 쓴다. 재방문 때 조건별로 고르는 이야기 조각에는 선행 조건, 우선순위, 반복 제한과 대체 경로가 필요하다. 대화 중심 게임은 장면·음성·전환을 한 스크립트로 표현할 수 있다. [Unreal data-driven gameplay](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine) · [Yarn Spinner localization](https://docs.yarnspinner.dev/3.1/yarn-spinner-for-unity/assets-and-localization/inbuilt-localisation) · [Writing with ink](https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md) · [Yarn Dialogue Runner](https://docs.yarnspinner.dev/components/dialogue-runner) · [Emily Short on Storylets](https://emshort.blog/2019/11/29/storylets-you-want-them/) · [Valve talk on dynamic dialogue](https://www.gdcvault.com/play/1015528/Do-Say-The-Right-Thing) · [Ren’Py dialogue and narration](https://www.renpy.org/doc/html/dialogue.html) · [Ren’Py voice](https://www.renpy.org/doc/html/voice.html)

각 대사에 안정적인 `LineId`, 화자, 원문, 소유 노드, 번역 맥락을 둔다. 초상화·표정 키, 자막 구간과 녹음을 같은 ID에 연결한다. 원문 수정 시 번역·재녹음 검토 표시를 남긴다. 대사를 나누거나 뜻을 바꾸면 기존 번역·음성·저장 위치를 어떻게 처리할지 정한다. Yarn 태그, Unity Localization String Tables, Unreal의 `FText`와 String Tables는 이 연결의 일부를 지원한다. 목표 빌드에서 현지화 자산과 음성 패키징을 확인한다. [Yarn Spinner tags and metadata](https://docs.yarnspinner.dev/write-yarn-scripts/advanced-scripting/tags-metadata) · [Unity Localization String Tables](https://docs.unity3d.com/Packages/com.unity.localization%401.5/manual/StringTables.html) · [Unreal text localization](https://dev.epicgames.com/documentation/en-us/unreal-engine/text-localization-in-unreal-engine) · [Yarn Spinner voice-over and localization sample](https://docs.yarnspinner.dev/yarn-spinner-for-unity/samples/sample-guide-voice-over-and-localisation) · [Yarn Spinner and Unity](https://docs.yarnspinner.dev/3.1/yarn-spinner-for-unity/yarn-spinner-in-unity-scenes) · [Asset localization](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-localization-in-unreal-engine) · [Dialogue Wave API](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UDialogueWave?application_version=5.8)

| 담당 | 결정할 사항 |
| --- | --- |
| 대화 정의 | 대사, 선택, 분기, 이야기가 요청할 명령 |
| 스테이지 배치 | 안정적인 등장인물 역할에 연결할 대화와 접근·상호작용·목표 달성 등 발동 조건 |
| 대화 세션 | 현재 대사·선택지, 입력 포커스, 카메라·음성 수명, 우선순위, 대기열, 건너뛰기·중단·재개 정책 |
| 월드 상태와 저장 | 퀘스트 조건, 일회성 결과, 대사를 보거나 들은 것으로 기록할 때, 버전 간 지원하는 재개 지점 |
| 표시와 연출 | 선택된 대사·화자·표정·제스처·음성·자막을 보여 주고 즉시 표시·건너뛰기·선택을 세션에 알림 |

짧은 반응은 이동 중에도 들려주고 명시적 선택에는 입력권을 준다. 시점이 정해진 장면에는 타임라인을 쓴다. 읽는 속도와 분기를 플레이어가 정하면 세션의 대사·선택 이벤트에 맞춰 연출한다. 진행 상태 변경은 소유자에게 요청하고 확정 후 결과를 보여 준다. Unity Timeline의 `SignalEmitter`와 Unreal Sequencer Event Track은 연출 시점에 명령을 연결할 수 있다. 건너뛰기·스크러빙·반복 중 해당 명령의 처리를 정한다. [Running ink, state, and external functions](https://github.com/inkle/ink/blob/master/Documentation/RunningYourInk.md) · [Unity Timeline Signal Emitter](https://docs.unity3d.com/Packages/com.unity.timeline%401.8/api/UnityEngine.Timeline.SignalEmitter.html) · [Unreal Sequencer Event Track](https://dev.epicgames.com/documentation/en-us/unreal-engine/cinematic-event-track-in-unreal-engine)

## 적용 조건과 예외

화면 밖의 짧은 반응은 긴급 신호에 양보할 수 있고, 필수 안내는 재생을 미루거나 기록으로 남겨야 할 수 있다. 위치가 중요한 짧은 말에는 말풍선, 긴 번역과 선택에는 초상화가 있는 고정 대화창을 고려한다. 서로 다른 선택의 결과를 예상할 수 있는지는 플레이어에게 확인한다. 텍스트 어드벤처의 88명 실험은 해당 조건에서 이 질문의 근거가 된다. 개별 게임 제작 사례는 도구와 중단 처리의 비용을 설명하며 아래 통합 점검은 제안 단계다. [Ren’Py side images](https://www.renpy.org/doc/html/side_image.html) · [Authors' paper](https://users.soe.ucsc.edu/~michaelm/publications/mateas-aiide2005.pdf) · [Research paper](https://cdn.aaai.org/ojs/12716/12716-52-16233-1-2-20201228.pdf) · [Greg Kasavin and Darren Korb talk](https://gdcvault.com/play/1027149/Breathing-Life-into-Greek-Myth) · [Developer talk](https://www.gdcvault.com/play/1024415/Do-You-Copy-Dialog-System) · [Sean Krankel talk](https://www.gdcvault.com/play/1024270/Building-Game-Mechanics-to-Elevate) · [Itay Keren's GDC talk on side-scrolling cameras](https://www.gdcvault.com/play/1022244/Scroll-Back-The-Theory-and) · [GDC talk on Celeste level layout and story](https://www.gdcvault.com/play/1024307/The-Gamer-s-Brain-How)

## 검증 방법

1. 접근 → 인사 → 상호작용 → 선택 → 결과 연출 → 조작 복귀를 재생한다. 다른 이벤트를 겹치고 선택 중에 떠나거나 화자를 제거하거나 발화 중 건너뛴다. 이전 저장으로 재진입한다. 선택 조건·우선순위·종료 사유를 기록하고 모든 종료 경로에서 입력·카메라·자막·음성이 정리되는지 본다. 미리보기, 재시도, 재생에서 영속 보상이 의도한 횟수만큼 적용돼야 한다.
2. 공통 대사를 고친 뒤 ID 중복, 끊긴 분기, 음성·초상화·번역 누락, 과거 플래그를 점검하고 기존 스테이지 두 곳을 재방문한다. 실제 읽기·녹음 길이에서 대사 교체, 무음 대사 진행, 입 모양과 카메라 복귀를 확인한다.
3. 초기에는 의사 현지화를 쓰고 실제 현지화 빌드에서는 글리프, 한중일 줄바꿈, 지원하는 우횡서, 변수 치환, 대비, 겹친 자막 순서를 검사한다. 화면 가장자리 말풍선, 가까이 있는 두 화자, 사라진 화자에서 긴 문장을 시험한다. [Xbox subtitle and caption guidelines](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/104) · [Unicode line breaking algorithm](https://www.unicode.org/reports/tr14/)

## 근거

Firewatch 제작 발표는 대화 중단과 재개, Hades는 대규모 녹음 제작, ink는 이야기 상태 저장과 외부 함수를 설명한다. 이를 소유권 분리와 점검 설계에 활용했다. 두 스테이지 플레이, 현지화 빌드, 저장 마이그레이션을 실행한 결과는 없다. 애니메이션 원본과 재임포트는 [캐릭터 스프라이트 제작](K-GAME-SPRITE-PRODUCTION.md), 선택 설계는 [내러티브 어드벤처](K-GAME-NARRATIVE-ADVENTURE.md)를 참고한다. [Running ink, state, and external functions](https://github.com/inkle/ink/blob/master/Documentation/RunningYourInk.md) · [Greg Kasavin and Darren Korb talk](https://gdcvault.com/play/1027149/Breathing-Life-into-Greek-Myth) · [Developer talk](https://www.gdcvault.com/play/1024415/Do-You-Copy-Dialog-System)

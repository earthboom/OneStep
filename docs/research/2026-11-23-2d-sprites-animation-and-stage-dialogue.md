# 2D 게임의 스프라이트·애니메이션과 스테이지 대사 제작 연구

2026-11-23 · 이미지 원본, 애니메이션 저작, 대사와 현지화, 스테이지 연출 · Unity와 Unreal

**그림을 수정하는 경로, 캐릭터가 움직이는 규칙, 대사가 선택되는 조건, 장면을 보여주는 연출을 각각 명시한다.** 예를 들어 경비의 표정을 다시 그리면 해당 그림에서 에셋을 생성하고, 대사를 번역하면 문장 ID에 연결된 텍스트를 교체한다. 경비가 어느 시점에 무슨 말을 하는지는 스테이지와 퀘스트의 상태로 정한다. 이 경계를 잡으면 새 스테이지에서 기존 캐릭터와 동작을 재사용하면서 대사와 구도를 그 스테이지에 맞게 만들 수 있다. [스테이지 제작 프레임워크](2026-11-22-stage-content-framework.md) · [게임 데이터 관리 방법론](2026-11-22-game-data-management-methods.md)

이 문서는 논문, 공식 문서, 개발팀 발표와 제작 기록에서 도출한 선택 기준과 검증 설계다. 프로젝트 착수와 콘텐츠 추가에 적용할 저작 경로, 상태 소유권, 플레이 확인 조건을 정리한다.

## 1. 이미지가 움직이는 방법을 저작 비용으로 고른다

| 방식 | 어울리는 콘텐츠와 저작 원본 | 검토할 비용과 표현 차이 |
| --- | --- | --- |
| **손으로 그린 프레임 애니메이션** | 픽셀 아트, 격투·플랫포머의 강한 포즈와 실루엣 변화. Aseprite 또는 레이어가 있는 그림 및 타임라인이 원본이다. | 자유롭게 형태를 바꿀 수 있다. 방향·의상·캐릭터가 늘면 다시 그릴 범위가 커진다. 프레임을 추가하는 것과 특정 포즈를 오래 보여 주는 것을 구별한다. [Aseprite 스프라이트 시트](https://aseprite.org/docs/sprite-sheet/) · [Cuphead 제작 발표](https://www.gdcvault.com/play/1024315/Animation-Bootcamp-Cuphead-Process-and) |
| **부품과 2D 스켈레탈 애니메이션** | 말하기, 대기, 걷기와 다양한 의상·장비를 공유하는 캐릭터. 레이어 이미지, 본·웨이트·슬롯·키프레임이 원본이다. | 공통 동작과 스킨을 재사용할 수 있다. 실루엣이 크게 변하거나 손과 무기가 교차할 때 변형, 앞뒤 순서, 가려질 부위를 저작해야 한다. 대각선으로 회전한 픽셀 아트는 의도한 픽셀 형태를 유지하는지 확인한다. [Spine 키와 타임라인](https://us.esotericsoftware.com/spine-keys) · [Unity PSD Importer](https://docs.unity3d.com/Packages/com.unity.2d.psdimporter%4010.0/manual/index.html) |
| **3D에서 저작하고 2D로 굽기** | 본과 애니메이션을 여러 적·무기에 공유하되 게임에서는 고정 화각의 2D 프레임을 쓰고 싶을 때. 3D 모델, 리그, 조명·카메라, 렌더 출력 규격이 원본이다. | 포즈 수정과 여러 동작의 재생성에 이점이 있다. 출력 해상도, 외곽선, 픽셀 정렬, 방향·장비별 프레임 수가 제작량과 텍스처 비용을 결정한다. [Thomas Vasseur의 Dead Cells 제작기](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-) |
| **혼합** | 평상시 동작은 공용 리그로, 실루엣이 중요한 공격·표정·이펙트는 별도 프레임으로 저작한다. 대화 초상화는 표정이나 입 모양만 교체할 수도 있다. | 여러 출력 방식의 피벗과 연결점, 시작과 종료의 포즈, 에셋 사용 여부를 맞춘다. 어떤 분량부터 어느 쪽을 반복 저작할지 대표 캐릭터에서 정한다. [Skullgirls 애니메이션 발표](https://gdcvault.com/play/1020575/) · [Ren’Py 캐릭터 옆 이미지](https://www.renpy.org/doc/html/side_image.html) |

Lasseter의 SIGGRAPH 논문은 누르고 늘리기, 예비 동작, 타이밍, 스테이징 같은 전통 2D 원리를 컴퓨터 애니메이션에 옮겨 설명한다. 여기서 가져올 판단은 포즈의 의미가 짧은 프레임에서도 읽히는지, 무엇을 강조할지, 행동의 다음 시점을 예측할 수 있는지다. 《Skullgirls》는 프레임 제한 속에서 강하고 유려한 모션을 만드는 사례이며, 《Cuphead》와 《Dead Cells》는 원하는 미술 스타일과 팀의 반복 수정 비용에 따라 다른 저작 경로가 성립함을 보여준다. [Lasseter 논문](https://www.cs.utexas.edu/~fussell/courses/cs384g-fall2011/projects/animator/lasseter.pdf) · [Skullgirls 발표](https://gdcvault.com/play/1020575/) · [Cuphead 발표](https://www.gdcvault.com/play/1024315/Animation-Bootcamp-Cuphead-Process-and) · [Dead Cells 제작기](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-)

### 프레임과 게임 상태를 연결하는 계약

- **클립 이름은 행동의 의미를 나타낸다.** 예를 들어 `guard.idle`, `guard.talk`, `guard.turn`과 방향·스킨 조합을 정한다. 클립의 반복 여부, 끝난 뒤 상태, 전환 우선순위와 재시작 방식을 소유자가 결정한다. 모든 방향을 그릴지 좌우 반전으로 해결할지 선택한다. 무기 손잡이, 글자, 비대칭 흉터가 있다면 반전한 결과를 따로 확인한다.
- **재생 시간과 프레임 번호를 구분한다.** Aseprite 원본에 프레임 지속 시간과 태그가 있으면 내보내기·엔진 가져오기에서 그 포즈가 실제로 얼마 동안 보이는지 확인한다. Unreal Flipbook은 FPS와 각 키의 프레임 지속 시간을 사용한다. 도구 교체나 리임포트 때 같은 태그와 클립이 재생되더라도 홀드 시간과 루프 경계가 달라질 수 있다. [Aseprite 파일 규격](https://github.com/aseprite/aseprite/blob/main/docs/ase-file-specs.md) · [Unity Aseprite Importer 기능](https://docs.unity3d.com/Packages/com.unity.2d.aseprite%403.0/manual/ImporterFeatures.html) · [Unreal Flipbooks](https://dev.epicgames.com/documentation/en-us/unreal-engine/paper-2d-flipbooks-in-unreal-engine)
- **의미가 다른 신호를 누가 소유할지 정한다.** 클립에서 재생하는 발자국, 눈 깜빡임, 입 모양과 게임이 판정하는 공격·입력·진행을 구분한다. 특정 포즈가 실제 판정의 기준이라면 그 연결, 도중 취소, 루프나 속도 변경에서 판정이 몇 번 일어나는지 명시한다. 접촉 결과가 확정됐을 때만 그 결과에 해당하는 타격 연출을 보낸다. [Spine의 Events 타임라인](https://us.esotericsoftware.com/spine-events) · [공격·피격·물리 판정 계약](../../knowledge/game/K-GAME-TECH-HITBOX.md) · [타격감과 손맛 연구](2026-11-23-game-feel-and-impact-feedback.md)

## 2. 이미지 원본, 가져오기, 아틀라스, 배포를 관리한다

| 작업 단위 | 유지할 정보와 기준 |
| --- | --- |
| **저작 원본** | 아트가 실제로 편집하는 `.aseprite`, `.psb`, 리그 프로젝트, 3D 자산과 필요한 팔레트·파일 링크를 기록한다. 원본 소유자와 수정 권한, 에셋 출처·사용 범위는 제작 시점에 확인한다. 큰 바이너리는 작업 환경과 저장소에 맞춰 LFS나 체크아웃을 검토한다. [Aseprite CLI](https://aseprite.org/docs/cli/) · [Git LFS 설정](https://docs.github.com/en/repositories/working-with-files/managing-large-files/configuring-git-large-file-storage) · [Unreal Perforce 안내](https://dev.epicgames.com/documentation/en-us/unreal-engine/using-perforce-as-source-control-for-unreal-engine) |
| **가져오기 계약** | 이미지의 크기·알파·필터·압축, 월드 단위당 픽셀, 피벗, 트림 전 원본 경계와 오프셋, 지면·손·말풍선 기준점을 정한다. 픽셀 아트의 필터·카메라 스케일은 실제 출력 해상도와 이동에서 확인한다. [Unity Sprite Atlas 설정](https://docs.unity3d.com/6000.0/Documentation/Manual/class-SpriteAtlas.html) · [Paper 2D Sprite Editor](https://dev.epicgames.com/documentation/unreal-engine/paper-2d-sprite-editor-in-unreal-engine) · [픽셀 아트 렌더링 지식](../../knowledge/game/K-GAME-TECH-PIXEL.md) |
| **생성물** | PNG 프레임, 아틀라스, 프레임 좌표·지속 시간 메타데이터, 엔진 클립을 원본으로부터 다시 만든다. 가져오기에서 생성한 파일에 손으로 편집할 값이 생기면 그 값을 별도 원본에 둘지 결정한다. 원본 위치, 내보내기 설정·도구 버전, 타깃 포맷을 기록한다. [Aseprite CLI](https://aseprite.org/docs/cli/) · [TexturePacker 메타데이터 내보내기](https://www.codeandweb.com/texturepacker/documentation/custom-exporter) · [Unity Aseprite Importer 생성 에셋](https://docs.unity3d.com/Packages/com.unity.2d.aseprite%403.0/manual/ImporterFeatures.html) |
| **아틀라스와 로드 수명** | 자주 함께 그리거나 로드하는 이미지와 실제 배칭 조건을 확인한다. UI 공용, 현재 지역, 긴 대화에서 쓰는 초상화, 선택 팩은 필요한 수명이 다를 수 있다. 아틀라스 공간을 잘 채우는 것과 동시에 상주하는 텍스처 비용을 줄이는 것을 함께 고려한다. [Unity Sprite Atlas 설정](https://docs.unity3d.com/6000.0/Documentation/Manual/class-SpriteAtlas.html) · [Spine Texture Packer](https://us.esotericsoftware.com/spine-texture-packer) |

파생 시트를 다시 패킹하면 사각형 위치가 바뀔 수 있다. **게임과 대사에서는 의미가 유지되는 에셋 키로 조회**하고, 시트 좌표와 순서는 가져오기에서 관리한다. 투명 영역을 트림할 때 원본 기준점과 오프셋을 보존하면 대기에서 말하기로 바뀔 때 발이 튀는 문제를 줄일 수 있다. 필터링·밉맵·타깃 압축을 쓰는 경우 인접 그림이 새는지 대표 확대율에서 본다. 패딩이나 경계 픽셀 확장을 조정할 때 좌우 반전·회전 패킹과 UI 마스크도 같이 확인한다. [Aseprite 내보내기 옵션](https://aseprite.org/docs/cli/) · [TexturePacker 아틀라스 설정](https://www.codeandweb.com/texturepacker/documentation/texture-settings)

아틀라스는 실제로 공유되는 머티리얼, 그리기 순서, 텍스처 바인딩 조건에 맞을 때 배칭에 도움을 준다. 사각형 패킹 알고리즘은 한 장의 공간을 채우는 데 쓰고, 어떤 것을 같은 장에 넣을지는 씬과 UI의 실제 사용으로 결정한다. 새 지역에 들어갈 때 한 초상화 때문에 큰 시트 전체를 상주시켜야 한다면 패킹 분리를 비교한다. 원본 PNG 용량과 별도로 패키지 용량, 실제 기기의 텍스처 메모리, 첫 로드와 지역 이동 뒤 해제를 본다. 지역마다 같은 공용 그림이 중복 패킹되는지도 비교한다. [Jylänki의 사각형 패킹 기술 문서](https://github.com/juj/RectangleBinPack/blob/master/RectangleBinPack.pdf) · [Unity Sprite Atlas 그룹 설계](https://docs.unity.com/en-us/engine/6000.0/manual/unity2d/sprite/atlas/atlas-introduction) · [게임 개발 성능·스트리밍 연구](2026-11-22-game-development-practices.md)

## 3. 대사의 저작 형식과 문장 수명을 정한다

| 저작 방식 | 언제 선택하는가 | 잘못 고르면 늘어나는 작업 |
| --- | --- | --- |
| **시트·타입이 있는 엔진 에셋** | 인사, 전투·환경에서 짧게 나오는 말, 고정 튜토리얼과 간단한 대화. 한 줄씩 검색·일괄 수정하거나 엔진 안에서 음성·초상화를 연결한다. | 조건과 분기가 많아지면 행만 읽고 실제 대화 흐름을 복원하기 어렵다. 선택 순서와 조건을 확인하는 미리보기나 탐색 도구가 필요해진다. [Unreal 데이터 기반 게임플레이](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine) · [Yarn Spinner 현지화](https://docs.yarnspinner.dev/3.1/yarn-spinner-for-unity/assets-and-localization/inbuilt-localisation) |
| **대화 스크립트·그래프** | 선택지, 흐름 합류, 화자·감정 전환을 작가가 주로 편집한다. Yarn Spinner나 ink가 예다. | 프로젝트의 플래그·명령을 대화가 어떤 인터페이스로 사용할지 정한다. 그래프 크기가 커지면 편집기에서 탐색하는 방법과 사람이 읽을 수 있는 변경 비교가 중요하다. [Writing with ink](https://github.com/inkle/ink/blob/master/Documentation/WritingWithInk.md) · [Yarn Dialogue Runner](https://docs.yarnspinner.dev/components/dialogue-runner) |
| **조건과 우선순위로 대사 선택** | 여러 스테이지를 자주 왕복하거나 세계의 변화에 따라 NPC가 짧은 말을 고른다. 조건, 우선순위, 반복 여부와 듣지 못한 대사를 다시 보낼지를 저작한다. | 여러 조건이 동시에 맞거나 모두 어긋날 때, 선택 이유가 추적 가능해야 한다. 이야기의 순서가 중요한 장면은 필수 선행 조건과 대체 경로를 정한다. [Emily Short의 Storylets](https://emshort.blog/2019/11/29/storylets-you-want-them/) · [Valve 동적 대사 발표](https://www.gdcvault.com/play/1015528/Do-Say-The-Right-Thing) |
| **대사·연출이 중심인 대본 언어** | 비주얼 노벨처럼 말하기, 배경·표정, 음성, 전환이 대표 플레이인 게임. Ren’Py는 해당 작업을 한 대본으로 표현하는 엔진 사례다. | 세계 탐색·전투·스트리밍까지 결합하면 스테이지 상태와 대화 명령을 연결할 범위를 정해야 한다. [Ren’Py 대사와 내레이션](https://www.renpy.org/doc/html/dialogue.html) · [Ren’Py 음성](https://www.renpy.org/doc/html/voice.html) |

**문장에 안정적인 ID를 부여한다.** 시작할 때 `LineId`, 화자, 원문, 번역용 맥락, 대화 순서 또는 소속 노드를 둔다. 사용한다면 초상화·표정 키, 음성 테이크, 자막 분할, 전후 맥락을 연결한다. 문장을 고쳐도 번역·녹음과 이어질 ID는 유지하고 재번역·재녹음이 필요한 원문 개정을 표시한다. 한 문장을 둘로 나누거나 뜻을 바꿀 때 기존 녹음과 저장된 대화 진행을 어떻게 처리할지 정한다. [Yarn Spinner 태그와 메타데이터](https://docs.yarnspinner.dev/write-yarn-scripts/advanced-scripting/tags-metadata) · [Unity Localization String Tables](https://docs.unity3d.com/Packages/com.unity.localization%401.5/manual/StringTables.html) · [Unreal 텍스트 현지화](https://dev.epicgames.com/documentation/en-us/unreal-engine/text-localization-in-unreal-engine)

**선택지, 상태, 표시 자산의 책임을 명시한다.** 같은 문장을 여러 스테이지에서 말할 수 있어도 발화 가능 조건과 재생 이력은 스테이지·캠페인 정책이 정한다. 퀘스트 수락·보상·해금처럼 플레이에 영향을 주는 대화 명령은 해당 상태 소유자가 검증하고 반영한다. 대사 스크립트의 변수와 월드 플래그에 같은 사실을 중복해 쓰게 될 때 한쪽의 읽기 계약을 정한다. 미리보기에서 대사를 읽다가 아이템이 실제로 지급되지 않는지, 재시도나 반복 실행에서 결과가 중복되지 않는지도 확인한다. [ink 실행과 상태·외부 함수](https://github.com/inkle/ink/blob/master/Documentation/RunningYourInk.md) · [Yarn Spinner Dialogue Runner](https://docs.yarnspinner.dev/components/dialogue-runner)

| 연구와 제작 사례 | 프로젝트에 적용해 볼 판단 |
| --- | --- |
| **Mateas·Stern, Façade, AIIDE 2005** | 지역적인 행동과 더 큰 극적 진행을 여러 저작 수준으로 구성한 연구 사례다. 일상 반응과 이야기의 필수 전환을 함께 구현할 때 각 수준의 책임을 생각할 근거다. [저자 논문](https://users.soe.ucsc.edu/~michaelm/publications/mateas-aiide2005.pdf) |
| **Cardona-Rivera 외, 의미 있는 선택지와 에이전시, AIIDE 2014** | 88명이 참여한 텍스트 어드벤처 실험에서 선택의 결과가 의미 있게 달라질 것으로 예상할 수 있을 때 에이전시 평가가 높았다. 버튼 개수보다 플레이어가 선택의 의미를 이해하는지 확인할 이유다. 다른 장르의 성과로 직접 일반화하려면 별도 플레이테스트가 필요하다. [연구 논문](https://cdn.aaai.org/ojs/12716/12716-52-16233-1-2-20201228.pdf) |
| **Supergiant, Hades, GDC** | 2만 2천 줄이 넘는 음성 대사를 제작한 팀이 캐릭터 목소리, 녹음, 처리, 게임 연결의 협업 과정을 설명한다. 줄마다 맥락·테이크·갱신 여부를 추적하는 규모가 어떤 것인지 볼 수 있다. [Greg Kasavin·Darren Korb 발표](https://gdcvault.com/play/1027149/Breathing-Life-into-Greek-Myth) |
| **Campo Santo, Firewatch, GDC** | 중단이 잦은 짧은 말 중심 시스템이 길고 다시 이어지는 대화를 다루도록 바뀌었다. 대사 선택 방식뿐 아니라 재개와 저작 도구의 비용이 전개 방식을 제약한 사례다. [개발팀 발표](https://www.gdcvault.com/play/1024415/Do-You-Copy-Dialog-System) |
| **Night School, Oxenfree, GDC** | 탐색과 의사소통을 함께 플레이하게 하는 목표를 두고 대화와 메커닉을 설계했다. 대화 도중 이동, 응답할 기회, 끼어들기가 핵심인지 판단할 때 볼 수 있다. [Sean Krankel 발표](https://www.gdcvault.com/play/1024270/Building-Game-Mechanics-to-Elevate) |

## 4. 스테이지에서 어떤 대사가 시작되고 중단되는지 정한다

| 역할 | 가질 데이터와 책임 |
| --- | --- |
| **대화 정의** | 대사·선택·분기, 화자, 표시할 줄 ID와 필요한 조건·명령. 여러 스테이지에서 재사용할 대화는 스테이지와 연출 자산을 얼마나 알아야 하는지 최소화한다. |
| **스테이지의 대화 배치** | `StageId`, 스폰 또는 오브젝트의 안정적인 역할 ID, 연결할 대화와 진입 조건. 접근, 상호작용, 지역 진입, 특정 목표 완료 같은 실제 트리거를 배치한다. 스테이지에서만 필요한 카메라 위치와 말풍선 기준점도 이 조립 단계에 연결할 수 있다. |
| **대화 세션** | 현재 재생하는 줄·선택·화자와 임시 입력·카메라 제어를 소유한다. 트리거 경쟁 시 우선순위, 중단·대체·큐잉, 자막·음성의 수명을 결정한다. 씬을 나가거나 화자가 사라질 때 실행 중인 작업과 임시 제어를 정리한다. |
| **게임 상태 및 저장** | 퀘스트, 보상, 반복 제한, 배운 정보 등 지속해야 할 결과를 소유한다. 언제 `봤다`나 `들었다`로 기록할지 정한다. 줄 단위 재개를 지원할 때는 지원 버전을 두고 줄·분기 수정의 영향을 확인한다. |
| **대사 표시와 연출** | 현재 줄과 화자·감정 키를 받아 텍스트, 음성, 초상화·스프라이트 상태, 카메라와 제스처를 재생한다. 선택 가능·자동 진행·스킵·중단 상태를 세션에 전달한다. |

### 장면에 맞춰 대화 모드를 고른다

- **짧은 반응 대사.** 이동과 기본 조작을 계속하게 하고, 쿨다운과 같은 화자의 중복 발화를 제한한다. 화면 밖에서 들릴 수 있는 짧은 말에 거리·위치와 자막의 노출 기준을 둔다. 중요한 전투 경고나 필수 진행 안내에 먼저 자리를 준다. [Valve 동적 대화 발표](https://www.gdcvault.com/play/1015528/Do-Say-The-Right-Thing) · [Firewatch 중단·재개 개발 경험](https://www.gdcvault.com/play/1024415/Do-You-Copy-Dialog-System)
- **플레이어가 시작하는 대화.** 상호작용 제안을 보여주고 선택지·대화창에 입력 초점을 준다. 멀어짐, 전투 발생, 여러 NPC와의 동시 상호작용에서 어느 시점에 줄·선택을 취소하거나 보존할지 정한다. 결과를 알리는 선택 화면은 플레이어가 선택의 차이를 예상할 정보를 준다. [Oxenfree 제작 발표](https://www.gdcvault.com/play/1024270/Building-Game-Mechanics-to-Elevate) · [의미 있는 선택지 연구](https://cdn.aaai.org/ojs/12716/12716-52-16233-1-2-20201228.pdf)
- **스크립트된 장면.** 카메라와 캐릭터 위치·입력 전환을 장면이 맡아야 하는 순간에 사용한다. 건너뛰기·사망·씬 전환·다시 보기에서 최종 위치와 플래그, 카메라·입력 복원을 각각 정한다. 연출 길이가 언어별 음성이나 이용자의 읽기 속도에 따라 달라질 수 있음을 저작 단계에서 고려한다. [Unity Timeline Signal Emitter](https://docs.unity3d.com/Packages/com.unity.timeline%401.8/api/UnityEngine.Timeline.SignalEmitter.html) · [Unreal Sequencer Event Track](https://dev.epicgames.com/documentation/en-us/unreal-engine/cinematic-event-track-in-unreal-engine)

우선순위는 장르에 맞게 선정한다. 예를 들어 플레이 중 생존 신호가 대사 중간에 발생하면 짧은 반응은 중단하고, 완료에 꼭 필요한 안내는 위험이 사라진 뒤 재생하거나 읽을 기록을 남길 수 있다. 같은 이벤트가 겹치면 `현재 스테이지와 화자가 유효한가 → 아직 필요한 대사인가 → 다른 대화의 입력·음성을 빼앗을 수 있는가`를 확인한다. 같은 대사가 반복될 때는 우선순위, 유효 조건, 호출 이유, 완료·중단 이유를 개발자가 볼 수 있게 한다. [Firewatch 대사 도구](https://www.gdcvault.com/play/1024415/Do-You-Copy-Dialog-System) · [스토리렛의 조건·단위 설계](https://emshort.blog/2019/11/29/storylets-you-want-them/)

## 5. 2D 화면에서 대사를 연출한다

| 수단 | 선택 기준과 실제 확인 지점 |
| --- | --- |
| **캐릭터 위 말풍선** | 누가 말하는지 위치가 즉시 보여야 하는 탐색·짧은 반응에 알맞다. 카메라 가장자리, 서로 가까운 두 화자, 화면 밖·스트리밍으로 사라진 화자, 긴 번역에서 위치·화자 표시를 확인한다. |
| **고정 대화창과 초상화** | 긴 대화, 선택지, 작은 캐릭터에서 표정이 중요한 때 사용한다. 화자 이름과 초상화를 유지하고 등장·감정 전환·시선 방향의 기준을 정한다. UI가 가능한 조작을 가리거나 입력 초점을 놓치지 않는지 살핀다. [Ren’Py 대사](https://www.renpy.org/doc/html/dialogue.html) · [Ren’Py 옆 이미지](https://www.renpy.org/doc/html/side_image.html) |
| **스테이지 내 카메라와 제스처** | 중요한 대상이나 공간을 볼 때 카메라의 프레이밍·제한 구역, NPC·플레이어 위치, 앞뒤 레이어, 제스처 타이밍으로 주의를 안내한다. 횡스크롤에서 카메라 이동 뒤 출구나 위협을 알아볼 수 있고 입력이 돌아왔는지 확인한다. [Itay Keren의 횡스크롤 카메라 GDC](https://www.gdcvault.com/play/1022244/Scroll-Back-The-Theory-and) · [Celeste 레벨 배치와 이야기 GDC](https://www.gdcvault.com/play/1024307/The-Gamer-s-Brain-How) |
| **텍스트·음성·입 모양** | 대화가 멈춰 있을지, 사용자 입력으로 넘어갈지, 음성 종료로 진행할지 모드마다 정한다. 텍스트 즉시 보기, 음성 스킵, 다음 줄 전환, 음성 누락에서 초상화와 입 모양이 다음 줄로 넘어가는지 확인한다. 내레이션·화면 밖 화자도 식별할 수 있게 한다. [Yarn Spinner 음성과 현지화 샘플](https://docs.yarnspinner.dev/yarn-spinner-for-unity/samples/sample-guide-voice-over-and-localisation) · [Xbox 자막과 캡션 지침](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/104) |

### 번역과 접근성도 같은 장면에서 검토한다

긴 문장, 한글·일본어·중국어의 줄바꿈과 글꼴 누락, 화면과 장치 크기별 글자 크기, 우좌 방향 언어를 지원한다면 해당 표시를 실제 장면에서 확인한다. 변수 치환이나 복수형, 이름 발음은 번역자가 맥락을 볼 수 있게 전달한다. 화자 이름, 효과음 캡션과 텍스트 대비, 말이 겹칠 때 표시 순서와 지난 대사의 확인 경로를 필요한 게임에 맞춰 정한다. 가짜 현지화는 레이아웃을 일찍 발견하는 도구로 쓰고, 실제 번역의 줄바꿈·폰트·녹음 길이는 각 언어 빌드에서 본다. [Unicode 줄바꿈 알고리즘](https://www.unicode.org/reports/tr14/) · [Unity String Tables](https://docs.unity3d.com/Packages/com.unity.localization%401.5/manual/StringTables.html) · [Xbox 자막·캡션 지침](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/104) · [OneStep 접근성·온보딩 지식](../../knowledge/game/K-GAME-ACCESSIBILITY-ONBOARDING.md)

## 6. Unity와 Unreal의 선택지

| 경로 | Unity | Unreal Engine |
| --- | --- | --- |
| **이미지·프레임** | Sprite Importer와 Sprite Atlas를 사용한다. Aseprite 직접 가져오기에서는 태그가 클립으로 생성되는지 확인한다. 레이어 직결과 2D 리그가 필요하면 `.psb` 가져오기를 검토한다. 가져오기에서 생성되는 클립과 직접 고치는 클립의 원본을 정한다. [Aseprite Importer](https://docs.unity3d.com/Packages/com.unity.2d.aseprite%403.0/manual/ImporterFeatures.html) · [PSD Importer](https://docs.unity3d.com/Packages/com.unity.2d.psdimporter%4010.0/manual/index.html) | Paper 2D Sprite에서 텍스처 영역, 피벗, 단위를 정하고 Flipbook으로 키와 프레임 지속 시간을 편집한다. 외부 시트의 설명 파일을 가져오는 경우 출력 포맷과 임포트 옵션을 맞춘다. [Import Sprites](https://dev.epicgames.com/documentation/unreal-engine/import-sprites-in-unreal-engine) · [Paper 2D Flipbooks](https://dev.epicgames.com/documentation/en-us/unreal-engine/paper-2d-flipbooks-in-unreal-engine) |
| **부품과 모션 전환** | `Animator`와 2D Animation 또는 팀이 사용하는 리그 런타임을 고른다. 의상·무기·표정 교체에서 스프라이트 순서와 기준점을 맞춘다. [Unity 2D Animation](https://docs.unity3d.com/Packages/com.unity.2d.animation%4010.0/manual/index.html) · [Spine 런타임](https://en.esotericsoftware.com/spine-using-runtimes/) | 프로젝트의 Pawn·Actor 상태에서 Flipbook을 선택한다. 혼합·이벤트·본이 필요한 규모는 별도 리그 런타임과 가져오기, 목표 플랫폼·지원 버전을 검토한다. [Unreal의 2D 개발 개요](https://dev.epicgames.com/documentation/en-us/unreal-engine/2d-in-unreal-engine) · [Spine 런타임](https://en.esotericsoftware.com/spine-using-runtimes/) |
| **대사와 번역** | 규모에 맞춰 타입이 있는 에셋, Yarn Spinner, ink를 선택한다. 줄 ID에 문자열과 지역화된 음성·초상화를 연결하고 기존 화면 구성에 출력한다. [Unity String Tables](https://docs.unity3d.com/Packages/com.unity.localization%401.5/manual/StringTables.html) · [Yarn Spinner와 Unity](https://docs.yarnspinner.dev/3.1/yarn-spinner-for-unity/yarn-spinner-in-unity-scenes) · [ink 런타임](https://github.com/inkle/ink/blob/master/Documentation/RunningYourInk.md) | Data Asset·Data Table과 게임의 대화 세션을 한 출발점으로 삼는다. 표시 텍스트는 지역화 키를 지닌 `FText`·String Table로, 녹음이 필요하면 대화 음성 자산을 연결한다. 외부 대화 도구의 Unreal 통합은 프로젝트 버전에서 기능과 배포 경로를 확인한다. [Unreal Text Localization](https://dev.epicgames.com/documentation/en-us/unreal-engine/text-localization-in-unreal-engine) · [에셋 현지화](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-localization-in-unreal-engine) · [Dialogue Wave API](https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/UDialogueWave?application_version=5.8) |
| **장면 연출** | Timeline에서 카메라·오브젝트·애니메이션을 함께 배치하고 필요한 Signal을 대화·게임의 공개 명령에 연결한다. 중간 진입·스킵·반복 재생에서 재생 신호가 다시 오는 조건을 확인한다. [Unity Timeline Signal Emitter](https://docs.unity3d.com/Packages/com.unity.timeline%401.8/api/UnityEngine.Timeline.SignalEmitter.html) | Sequencer의 Event Track을 연출 시점과 대화에 연결한다. 스킵, 강제 종료, 스크러빙 같은 재생 조건에서 중요한 게임 결과가 몇 번 반영되는지 확인한다. [Unreal Sequencer Event Track](https://dev.epicgames.com/documentation/en-us/unreal-engine/cinematic-event-track-in-unreal-engine) |

정해진 길이의 컷신에는 타임라인이 어울린다. 플레이어가 기다리거나 선택하는 대화는 세션이 줄과 응답을 진행하고 장면은 해당 상태에 맞춰 재생하는 구성이 편하다. 타임라인에 연결된 보상·진행 명령은 스킵과 반복에서의 결과를 게임 상태 소유자가 정한다. 프로젝트가 여러 플랫폼에서 배포된다면 가져오기와 현지화 자산이 실제 타깃에 포장되는 경로도 확인한다. [Unity Timeline Signal Emitter](https://docs.unity3d.com/Packages/com.unity.timeline%401.8/api/UnityEngine.Timeline.SignalEmitter.html) · [Unreal Sequencer Event Track](https://dev.epicgames.com/documentation/en-us/unreal-engine/cinematic-event-track-in-unreal-engine) · [Unreal 에셋 현지화](https://dev.epicgames.com/documentation/en-us/unreal-engine/asset-localization-in-unreal-engine)

## 7. 스테이지 하나를 추가하는 설계 예시

횡스크롤 어드벤처에 `mill-yard`를 추가한다. 공용 경비 캐릭터의 대기·걷기·말하기 클립과 초상화 키를 재사용한다. 경비의 인사는 처음 근처에 왔을 때 짧게 나오고, 플레이어가 상호작용하면 방앗간을 여는 선택지가 나온다. 퀘스트를 수락한 뒤 다시 오면 다음 목표를 알려주고, 목표를 완료한 뒤에는 완료 대사를 고른다.

| 저작 작업 | 어디를 바꾸고 어떤 결과를 볼 것인가 |
| --- | --- |
| **이미지와 동작** | 경비의 새 표정이 필요하면 원본 그림에 추가하고 가져오기에서 같은 발·얼굴 기준점을 확인한다. 방앗간 전용 제스처가 있으면 클립을 추가하고 말하기 종료 뒤 대기로 이어지는지 본다. |
| **문장과 번역·음성** | `mill.guard.first-greeting`, `mill.guard.open-question`처럼 맥락을 담은 문장 키를 만들고 화자, 번역 메모와 음성을 연결한다. 주 텍스트나 음성을 고쳐도 스테이지 배치의 키와 순서가 올바른지 확인한다. |
| **스테이지 배치·조건** | 경비 역할과 위치, 접근·호출 트리거, 이전 진행에 따른 대화를 지정한다. 접근 반응은 선택 유도 대화와 겹치지 않게 하고, 재방문과 이전 저장에서 올바른 줄을 선택한다. |
| **연출과 상태 확정** | 짧은 모션과 초상화 전환은 대사 세션의 줄과 연결한다. 방앗간이 실제로 열리는 조건은 선택 또는 게임 상태에서 판정하고, 카메라 이동은 확정 상태에 맞춰 시작한다. 플레이어의 스킵이나 퇴장 후 어떤 대사와 제어가 이어질지는 사전에 정한 정책을 따른다. |

장면을 연출할 때는 **접근 → 인사 → 대화 선택 → 결과를 보여주기 → 조작 복귀**의 다섯 순간을 따로 저작한다. 접근 인사는 이동 중 말풍선으로 보이고, 말을 걸었을 때만 경비와 플레이어가 화면에 같이 들어오도록 잡는다. 경비가 방앗간을 가리키는 제스처는 해당 줄이 시작될 때 재생한다. 문이 열리는 선택이 확정되면 움직임을 보여주고, 장면이 끝나거나 건너뛰면 원래 카메라와 입력으로 돌아간다. 번역이나 녹음 길이가 바뀌어도 각 행동은 정한 대화 사건에 맞춰 일어나야 한다. [Itay Keren의 횡스크롤 카메라 발표](https://www.gdcvault.com/play/1022244/Scroll-Back-The-Theory-and) · [Firewatch 대화 프로그램](https://www.gdcvault.com/play/1024415/Do-You-Copy-Dialog-System)

## 8. 가져오기와 대사 연출의 회귀 검증

1. **가져오기와 배포.** 새 태그나 레이어, 리임포트, 방향 반전과 트림 뒤의 피벗·홀드 시간·클립 참조를 확인한다. 대표 해상도와 타깃에서 텍스처 색·알파·필터링·패킹 문제를 본다. 두 스테이지를 왕복하면서 이미지·초상화가 로드되고 정리되는지 확인한다.
2. **대사와 현지화.** 문장 ID 중복, 끊긴 선택과 분기, 없는 화자·초상화·음성, 현지화 키 누락·긴 문자열을 검사한다. 플레이 중 음성이 없는 줄의 표시, 화자 교대, 선택 진입과 스킵, 이전 플래그로 시작한 재방문의 대사를 실제 목록·트리거 경로에서 확인한다.
3. **연출과 중단.** 접근 직후 다른 트리거를 밟거나, 재생 중 장면을 나가거나, 선택 화면에서 취소하는 경우에 음성·효과·카메라와 입력 초점이 정리되는지 본다. 공유 정의나 공용 플레이어를 바꿨다면 기존 스테이지에서 같은 동작과 반응을 확인한다.
4. **유지할 결과.** 대사의 말투나 표정을 바꾸는 작업과 퀘스트에 영향을 주는 작업을 구분해 기대값을 정한다. 텍스트 노출 시점, 보상이 몇 번 반영되는지, 현재 상태를 이어갈 수 있는지 등 영향 범위를 기존 작업 브리프에 적는다. 새 스테이지를 등록하고 기존 주요 경로에서 실제 플레이를 확인한다. [스테이지 검증 연구](2026-11-22-stage-content-framework.md#6-자동-검증과-제작-검토) · [게임플레이 회귀 검증](2026-11-22-gameplay-regression-verification.md) · [콘텐츠 확장 설계 지침](../../skills/vegabond-code-design/references/gameplay-framework.md#give-content-an-extension-path)

처음 정할 기준은 **어디서 이미지를 고치는가, 무엇이 한 클립의 시간을 정하는가, 문장 ID로 텍스트와 음성을 어떻게 찾는가, 스테이지에서 누가 대사를 시작·중단하고 상태를 확정하는가**다. 대표 캐릭터와 스테이지를 각각 두 가지 변형으로 대입해, 새 저작에 필요한 작업과 공용 규칙이 달라지는 지점을 확인한다.

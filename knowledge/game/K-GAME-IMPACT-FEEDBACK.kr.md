# 입력·접촉·판정·회복을 구분해 타격감 설계하기

K-GAME-IMPACT-FEEDBACK · 방법 · 적용 중 · 근거 확인 2026-11-23

입력 승인에는 즉시 반응하고 접촉 연출은 확정된 판정에 연결한다. 흔들림·소리·진동을 각각 조절하며 헛침·막힘·명중을 구별할 수 있는지 비교한다.

적용 범위 — 근접·원거리 액션, 이동, 리듬, 턴제 게임의 기기·시점별 조작감과 타격감.

## 적용 방법

입력 승인, 예비 동작, 접촉, 판정, 회복까지 공격 하나를 따라간다. 휘두른 궤적과 접촉 위치·재질을 구별한다. 헛침은 휘두름, 막힘은 고유 신호와 반동, 명중은 확정 피격 반응으로 읽히게 한다. 규칙이 접촉·피해·히트스턴을 결정하고 표현은 결과·표면·위치·방향·강도로 신호를 선택한다. 멀티플레이는 발사에 곧바로 반응한 뒤 예측과 확인을 맞추되 같은 타격을 두 번 재생하지 않는다. 다단 공격의 각 접촉은 구분한다.

히트스톱의 범위와 시간을 정의한다. 공격자·대상·월드·물리·입력 버퍼·콤보·무적·쿨다운·카메라·오디오·UI가 어떻게 진행하는지 정한다. 히트스턴은 규칙상 다음 행동을 제한한다. 연타 정지는 누적 상한을 두고 입력이 보존되는지 본다. Unity에서 전역 timeScale=0은 FixedUpdate와 WaitForSeconds 대기를 멈춘다. Unreal에서 준비된 휘두름은 Animation Notify, 확정 접촉은 Niagara나 장식용 Gameplay Cue로 표현할 수 있다. 손실 가능한 큐가 권한 피해를 결정해서는 안 된다.

흔들림의 진폭·방향·주파수·거리 감쇠·중첩·잔향을 조절한다. 장식 흔들림을 줄여도 조준점·탄도·다음 위협을 읽을 수 있어야 한다. 스윙음, 접촉 첫 음·재질, 여운, 플레이어 확인음을 분리한다. 같은 음량에서 앞부분 무음·출력 지연·동시 발음 제한·마스킹을 확인한다. 미리 아는 리듬 신호는 오디오 시계로 예약한다. 진동은 펄스 간격과 채널로 결과를 구별한다. 중요 신호는 다른 감각 채널로도 제공하고 흔들림·헤드 보빙·블러·진동을 따로 조절한다.

## 적용 조건과 예외

Unity는 Cinemachine Impulse·Audio Mixer·Input System, Unreal은 Camera Shakes·Sound Concurrency·Force Feedback 등으로 구현할 수 있다. 근접은 유효 판정 구간, 슈터는 반동 중 조준, 플랫폼·레이싱은 접촉·접지, 리듬은 빠름·늦음과 보정, 턴제는 짧고 분명한 판정 전달이 중요하다. 강도 하나나 시청각 허용 오차 하나를 모든 과제·기기에 적용할 수 없다.

## 확인 방법

무기·대상·표면·거리를 맞춘 뒤 헛침·막힘·약타·강타를 비교한다. 한 채널씩 바꾸고 순서를 교차한다. 입력 인지, 판정 식별, 다음 입력 성공, 놓친 전조와 불편함을 측정한다. 엔진 이벤트 시각과 실제 입력에서 화면·소리 출력까지의 지연을 구분한다. 저효과·음소거·진동 끔·낮은 프레임률·패킷 손실에서 확인한다. 빠른 재시도와 동시 타격에서 중복 신호, 경고음 마스킹, 섬광 중첩, 피해·히트스턴·콤보 변화가 있는지 본다.

회복 중 조준과 이동을 유지할 수 있는지, 다음 위협을 알아볼 수 있는지 확인한다. 확정 판정마다 식별 가능한 피드백 이벤트를 발행하고, 공격과 재시작, 효과를 낮춘 상태는 [회귀 검증 범위](K-GAME-REGRESSION-SCOPE.kr.md)에 맞춰 확인한다.

## 근거

11월 23일 검토는 동작 튜닝, 입력 보조, 피드백 강조를 구분했다. Lin 등은 상·하위 게임 각 8개의 특징 19개를 비교했다. Kao의 액션 RPG 실험은 3,018명이 네 조건에 참여했고 여러 요소가 함께 달라졌다. 오디오 메타분석은 검토한 14편 중 6편을 포함했고 진동 실험은 휴대폰에서 수행했다. 이 근거와 출시작 발표는 비교 항목을 제시하나 대상 게임의 타이밍·편안함을 확정하지 않는다. 당시 로컬 기기 플레이테스트는 보고되지 않았다.

[전투 가독성](K-GAME-ACTION-COMBAT.md) · [히트박스 계약](K-GAME-TECH-HITBOX.md) · [접근성](K-GAME-ACCESSIBILITY-ONBOARDING.md) · [Gameplay Cue 수명](../code/K-CODE-UE-GAS-CUE-EXECUTE-VS-ADD.md)

- [Pichlmair and Johansen's game feel survey](https://researcher.itu.dk/p/en/research-outputs/designing-game-feel-a-survey) · [Swink's Game Feel](https://www.routledge.com/Game-Feel/Swink/p/book/9780123743282) · [Research on impact feedback in action games](https://faculty.washington.edu/zkwen/articles/lin22features.pdf)
- [Pichlmair and Johansen, Designing Game Feel — Authors' version](https://researcher.itu.dk/ws/portalfiles/portal/91131028/TG3072241.pdf) · [Kao, The Effects of Juiciness in an Action RPG, 2020 — Abstract and bibliographic record](https://experts.illinois.edu/en/publications/the-effects-of-juiciness-in-an-action-rpg/) · [Hicks et al., Good Game Feel, DiGRA 2018 — Paper](https://dl.digra.org/index.php/dl/article/download/936/936/933) · [Nacke, Grimshaw, and Lindley, FPS sound experiment, 2010 — Paper record at the authors' institution](https://vbn.aau.dk/en/publications/more-than-a-feeling-measurement-of-sonic-user-experience-and-psyc/) · [PLOS ONE paper](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0361519)
- [Singhal and Schneider, Juicy Haptic Design, CHI 2021 — Authors' paper](https://uwspace.uwaterloo.ca/bitstream/handle/10012/16894/Juicy_Haptic_Design_SIGCHI_2021__UWSpace_.pdf) · [Synchrony review](https://research.tilburguniversity.edu/en/publications/perception-of-intersensory-synchrony-a-tutorial-review/) · [FPS aiming experiment](https://research.nvidia.com/publication/2021-05_case-study-first-person-aiming-low-latency-esports)
- [Jiesang Song on making Kingdom Under Fire](https://www.gamedeveloper.com/audio/improving-the-combat-impact-of-action-games) · [Riot on combat clarity](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/) · [Xbox on attack cues in Grounded](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/103)
- [Skullgirls animation at GDC](https://gdcvault.com/play/1020575/) · [VFX as a Game Design Language at GDC](https://www.gdcvault.com/play/1027899/Visual-Effects-Summit-VFX-as) · [Riot VFX production training](https://www.riotgames.com/en/artedu/visual-effects) · [Sakurai's hitstop video](https://www.youtube.com/watch?v=OdVkEOzdCPw) · [Unity time scale](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Time-timeScale.html)
- [Juicing Your Cameras With Math at GDC](https://www.gdcvault.com/play/1023557/Math-for-Game-Programmers-Juicing) · [Eiserloh's slides](https://media.gdcvault.com/gdc2016/Presentations/Eiserloh_Squirrel_JuicingYourCameras.pdf) · [Vlambeer talk](https://www.youtube.com/watch?v=AJdEqssNZ-U) · [God of War combat and camera at GDC](https://www.gdcvault.com/play/1026423/Evolving-Combat-in-God-of)
- [UNDERDOGS sound at GDC](https://gdcvault.com/play/1035486/Visceral-Sound-on-Tiny-Speakers) · [Unreal sound concurrency rules](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-concurrency-reference-guide) · [Hi-Fi RUSH director at GDC](https://gdcvault.com/play/1034256/Developing-Hi-Fi-RUSH-Backwards) · [Unity PlayScheduled](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/AudioSource.PlayScheduled.html)
- [Housemarque and PlayStation sound team's production account](https://blog.playstation.com/?p=349009) · [Unreal device-specific Force Feedback](https://dev.epicgames.com/documentation/en-us/unreal-engine/force-feedback-in-unreal-engine) · [XAG 110 haptics](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/110) · [XAG 117 motion](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/117) · [XAG 118 flash review](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/118)
- [Cinemachine Impulse](https://docs.unity3d.com/Packages/com.unity.cinemachine%403.1/manual/CinemachineImpulse.html) · [Camera Shakes](https://dev.epicgames.com/documentation/en-us/unreal-engine/camera-shakes-in-unreal-engine) · [Visual Effect Graph](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph%4017.0/manual/index.html) · [Animation Notifies](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-notifies-in-unreal-engine) · [Niagara overview](https://dev.epicgames.com/documentation/unreal-engine/overview-of-niagara-effects-for-unreal-engine)
- [Audio Mixer](https://docs.unity3d.com/6000.0/Documentation/Manual/AudioMixer.html) · [AudioSource priority](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/AudioSource-priority.html) · [Input System Gamepad](https://docs.unity3d.com/Packages/com.unity.inputsystem%401.11/manual/Gamepad.html) · [MetaSounds](https://dev.epicgames.com/documentation/en-us/unreal-engine/metasounds-the-next-generation-sound-sources-in-unreal-engine) · [Unity client anticipation](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects%402.13/manual/advanced-topics/client-anticipation.html)
- [Unreal GAS cosmetic effects](https://dev.epicgames.com/documentation/en-us/unreal-engine/understanding-the-unreal-engine-gameplay-ability-system#handling-cosmetic-effects)
- [Juice It or Lose It demonstration](https://www.gdcvault.com/play/1016789/Juice-It-or-Lose)

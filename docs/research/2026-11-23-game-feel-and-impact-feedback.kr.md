# 게임의 타격감과 손맛 설계 연구

2026-11-23 · 입력 반응, 애니메이션, 카메라, 이펙트, 사운드, 햅틱

**카메라·이펙트·사운드는 같은 판정의 서로 다른 정보를 전달할 때 타격감을 만든다.** 무기가 닿는 순간 볼 수 있어야 하고, 맞은 재질과 결과를 소리로 구분할 수 있어야 하며, 큰 충격 뒤에도 다음 행동에 필요한 시야와 조작이 이어져야 한다. 이 문서에서 **타격감**은 접촉과 그 결과가 느껴지는 정도, **손맛**은 입력이 받아들여지고 다음 선택으로 이어지는 전체 조작의 느낌을 가리킨다. 실제 개발에서는 입력·움직임의 조정, 사건의 피드백, 플레이어가 의도를 실행하도록 돕는 설계를 함께 본다. [Pichlmair·Johansen의 Game Feel 조사](https://researcher.itu.dk/p/en/research-outputs/designing-game-feel-a-survey) · [Swink의 Game Feel](https://www.routledge.com/Game-Feel/Swink/p/book/9780123743282) · [액션 게임의 타격 피드백 연구](https://faculty.washington.edu/zkwen/articles/lin22features.pdf)

이 문서는 [게임 개발 기본 전략](../designs/game-development-strategy.md)과 [게임플레이 회귀 검증 기본 규칙](2026-11-22-gameplay-regression-verification.kr.md)을 타격감·조작감에 적용한 조사다. 사례의 값은 해당 게임의 카메라, 장르, 입력 장치와 함께 읽는다. 아래 예시는 실제 프로젝트에서 검증할 설계안이다.

## 1. 연구에서 판단할 수 있는 범위

| 출처 | 결과와 사용할 수 있는 범위 |
| --- | --- |
| **Pichlmair·Johansen, Designing Game Feel** | 피드백으로 사건을 강조하는 *juicing*, 움직임과 물리를 조정하는 *tuning*, 플레이어의 의도를 도와주는 *streamlining*을 구분한다. 입력이 늦게 받아들여지는 문제, 무기의 무게가 약하게 느껴지는 문제, 명중 여부가 안 보이는 문제를 각각 진단할 근거다. [저자본](https://researcher.itu.dk/ws/portalfiles/portal/91131028/TG3072241.pdf) |
| **Lin 외, Impact Feedback in Action Games, 2022** | Steam 리뷰를 바탕으로 게임 순위를 추정하고, 상위 8개와 하위 8개를 19개 특성으로 비교했다. 히트스톱, 사운드와 화면의 일관성, 카메라 제어가 구별되는 후보로 나왔다. 게임 간 비교이므로 요소 하나의 인과 효과나 모든 장르에 통하는 설정값은 이 연구에서 정할 수 없다. [논문](https://faculty.washington.edu/zkwen/articles/lin22features.pdf) |
| **Kao, The Effects of Juiciness in an Action RPG, 2020** | 3,018명이 참여한 한 액션 RPG의 네 조건에서, 피드백이 없는 조건과 극단적으로 과한 조건은 중간·높은 조건보다 플레이 시간, 경험, 내재적 동기, 성과가 낮았다. 여러 피드백이 함께 달라진 실험이다. 프로그램에 효과를 더할 때 개선 지표와 가독성 비용을 함께 확인할 이유다. [논문 초록과 서지](https://experts.illinois.edu/en/publications/the-effects-of-juiciness-in-an-action-rpg/) |
| **Hicks 외, Good Game Feel, DiGRA 2018** | 개발자 관점에서 과도해 보일 수 있는 장식이 어떻게 의미 있는 반응으로 쓰이는지 분석했다. 효과의 양을 정하기 전에 의미와 맥락을 먼저 정할 근거다. [논문](https://dl.digra.org/index.php/dl/article/download/936/936/933) |
| **Nacke·Grimshaw·Lindley, FPS 사운드 실험, 2010** | FPS 개조판에서 효과음과 음악의 켜기·끄기를 조합했다. 효과음은 경험 설문의 여러 항목에 영향을 주고, 음악과 효과음의 조합은 긴장과 몰입 흐름 평가에 영향을 줬다. 같은 전투 효과를 솔로 재생과 게임 믹스에서 모두 들어볼 근거다. [저자 소속기관의 논문 기록](https://vbn.aau.dk/en/publications/more-than-a-feeling-measurement-of-sonic-user-experience-and-psyc/) |
| **Heikkilä·Danso·Luck, 게임 오디오 메타분석, 2026** | 문헌 14편 중 6편을 메타분석했다. 게임 오디오가 포함된 조건에서 즐거움 등 긍정 경험이 높았으며, 일부 조건을 제외하면 추정 효과는 작아졌다. 게임 사운드에 음악을 더하는 효과에는 불확실성이 컸다. 이 결과는 여러 게임에서의 오디오 경험에 관한 것으로, 타격음 단독 효과는 대표 타격으로 검증한다. [PLOS ONE 논문](https://journals.plos.org/plosone/article?id=10.1371%2Fjournal.pone.0361519) |
| **Singhal·Schneider, Juicy Haptic Design, CHI 2021** | 휴대폰을 사용한 두 연구에서 시각과 함께 제시한 진동의 선호와 게임 경험을 조사하고, 설계된 진동이 즐거움과 경험을 높일 수 있다고 보고했다. 콘솔 패드나 장시간 플레이에는 장치와 사용 시간을 맞춰 다시 평가한다. [저자 논문](https://uwspace.uwaterloo.ca/bitstream/handle/10012/16894/Juicy_Haptic_Design_SIGCHI_2021__UWSpace_.pdf) |
| **Vroomen·Keetels, 감각 사이 동시성 검토 · Spjut 외, FPS 입력 지연 사례 연구** | 시청각 동시성 판단은 자극과 과제 조건에 영향을 받는다. FPS 조준은 실제 입력·표시 지연을 다루는 별도 측정 대상이다. 그래서 타격 소리의 상대 시점과 입력 반응 시간은 각자 기록하고, 다른 환경의 수치를 범용 허용값으로 사용하지 않는다. [감각 동시성 검토](https://research.tilburguniversity.edu/en/publications/perception-of-intersensory-synchrony-a-tutorial-review/) · [FPS 조준 실험](https://research.nvidia.com/publication/2021-05_case-study-first-person-aiming-low-latency-esports) |

## 2. 한 번의 타격을 입력부터 회복까지 설계한다

| 시점 | 플레이어가 알아야 할 것 | 설계 수단 |
| --- | --- | --- |
| **입력 접수** | 버튼이 받아들여졌는지, 다음 공격이 예약됐는지 | 공격이 실제로 시작되면 손·무기 자세나 시동음을 보여준다. 콤보나 버퍼를 지원할 경우 입력 시점, 소비할 수 있는 구간, 취소나 모드 전환에서 만료되는 조건을 정한다. |
| **공격 준비와 이동** | 어느 방향·거리·리듬으로 공격이 오는지 | 실루엣, 체중 이동, 무기 궤적, 예고음으로 힘과 방향을 전달한다. 상대가 피하거나 막을 시간이 필요한 공격은 준비 동작을 적절한 카메라 거리에서 읽을 수 있어야 한다. |
| **접촉과 판정** | 빗나갔는지, 막혔는지, 무엇을 맞혔는지 | 실제 판정과 같은 접촉 위치·방향의 이펙트, 결과별 음색, 피격 포즈를 조합한다. 손맛을 위한 작은 충격과 전황을 바꾸는 큰 충격의 표현 차이를 둔다. |
| **여파와 회복** | 피해·경직이 얼마나 중요한지, 어느 순간부터 다음 행동을 할 수 있는지 | 짧은 멈춤·반동·잔향으로 여운을 만들고, 몸·카메라·믹스가 다음 위협을 읽을 상태로 돌아오게 한다. 공격 취소나 행동 허용 시점은 규칙과 동작에서 일치해야 한다. |

**같은 무기로 결과만 바꿔 비교한다.** 허공에서는 휘두르는 소리와 궤적, 방패에 막히면 금속음과 방패에서 튕기는 반응, 몸에 맞으면 접촉 이펙트와 피격 방향을 사용한다. 패링이나 가드 붕괴가 전투의 주도권을 바꾼다면 고유한 음색·실루엣 등으로 구별한다. 슈퍼아머가 경직을 막는 게임에서는 체력 피해와 경직 여부를 서로 다른 신호로 표현할 수 있다. [Jiesang Song의 Kingdom Under Fire 제작 경험](https://www.gamedeveloper.com/audio/improving-the-combat-impact-of-action-games) · [Riot의 전투 가독성](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/) · [Xbox의 Grounded 공격 신호 사례](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/103)

## 3. 애니메이션, 이펙트, 히트스톱

- **준비·접촉·회복에 서로 알아볼 수 있는 포즈를 둔다.** 무게는 준비에서의 체중 이동, 접촉에서의 속도 변화, 여파에서의 제동을 통해 느낄 수 있다. 큰 공격과 빠른 공격은 준비와 회복의 시간 대비를 활용한다. 맞은 몸이 어느 방향으로 밀리는지, 공격이 유효한 구간과 화면에서 읽히는 궤적이 맞는지 확인한다. [Skullgirls 애니메이션 GDC](https://gdcvault.com/play/1020575/) · [근접 타격 연출 제작 경험](https://www.gamedeveloper.com/audio/improving-the-combat-impact-of-action-games) · [공격·피격·물리 충돌 계약](../../knowledge/game/K-GAME-TECH-HITBOX.kr.md)
- **이펙트에는 의미를 담는다.** 접촉점 스파크는 위치, 날아가는 파편은 방향·재질, 큰 섬광이나 깨어지는 형태는 상황 변화에 대응할 수 있다. 휘두름 궤적은 공격자, 피격 이펙트는 접촉점을 표현한다. 범위 예고와 실제 판정이 다르거나 다른 사람의 효과가 다음 위협을 가리면 우선순위와 크기·명도·지속 시간을 조정한다. 입자 수를 줄인 품질 설정에서도 필수 경계와 결과 신호가 남게 한다. [VFX as a Game Design Language GDC](https://www.gdcvault.com/play/1027899/Visual-Effects-Summit-VFX-as) · [Riot VFX 제작 교육](https://www.riotgames.com/en/artedu/visual-effects)
- **히트스톱의 범위를 정한다.** 타격 순간 강조를 위한 짧은 정지·감속을 공격자와 피격자, 애니메이션, 월드 전체 중 어디에 적용할지 적는다. 입력 수집, 콤보·무적·쿨다운 타이머, 이동 판정, 카메라·UI·소리의 시계가 각각 어떻게 진행되는지도 정한다. 경직은 다음 행동을 제한하는 게임 규칙이므로 연출용 멈춤과 따로 명시한다. Unity에서 전역 `timeScale`을 0으로 두면 `FixedUpdate`와 `WaitForSeconds`로 대기하는 코루틴이 진행되지 않으므로 물리 판정과 회복을 함께 점검해야 한다. 연속 타격에서 정지가 누적돼 입력이 사라지거나 월드가 늘어지는 경우에는 한도나 병합 기준을 둔다. 약타·가드·강타의 길이는 프로젝트의 조작 리듬으로 비교한다. [Sakurai의 히트스톱 영상](https://www.youtube.com/watch?v=OdVkEOzdCPw) · [Lin 외 비교 연구](https://faculty.washington.edu/zkwen/articles/lin22features.pdf) · [Unity 시간 배율](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/Time-timeScale.html) · [시뮬레이션 스텝 지식](../../knowledge/game/K-GAME-TECH-TIMESTEP.kr.md)

## 4. 카메라는 충격과 전투 정보를 함께 다룬다

| 수단 | 쓰기 좋은 조건 | 점검할 부작용 |
| --- | --- | --- |
| **짧은 방향성 흔들림** | 근접 타격, 착지, 폭발처럼 충격이 온 방향이나 세기를 강조한다. 발생 위치·플레이어와의 거리·공격 종류에 따라 감쇠를 정한다. | 고빈도 공격과 여러 폭발이 겹치면 지속 흔들림이 되므로 우선순위·합성 한도를 둔다. 진폭·주파수·방향·감쇠를 각각 조정한다. |
| **프레이밍·줌·시선 변화** | 강한 공격의 준비, 투사체의 도착, 보스의 주요 행동처럼 주목할 대상이 이동한다. | 조준, 다음 적, 피할 공간, 카메라와 벽의 충돌을 확인한다. 3인칭에서 근접 적을 잘 보이게 한 프레이밍이 화면 밖 위험을 늘릴 수 있다. |
| **카메라 반동과 무기 반동** | FPS·TPS에서 발사한 순간의 방향과 무게를 전달한다. | 조준점과 탄도의 관계가 실제로 바뀌는 반동은 게임 규칙에 속한다. 표현용 흔들림을 줄이는 옵션에 따라 명중 판정이나 조준 보정이 달라지지 않게 한다. |
| **컷·큰 줌·연출 카메라** | 스킬 마무리나 보스 페이즈 전환처럼 플레이가 바뀌는 순간에 제한적으로 쓰기 좋다. | 입력 권한이 돌아오는 시점과 적의 재개를 맞추고, 플레이어가 조작할 공간을 다시 보게 한다. 분할 화면·관전자·멀티플레이에 적용되는 카메라를 별도로 정한다. |

Eiserloh는 충격량을 제한된 값에 누적·감쇠시키고 비선형 곡선으로 흔들림에 연결하는 예를 보여준다. 평타에는 작은 변화, 큰 충격에는 선명한 변화를 두고 싶을 때 비교할 수 있다. Vlambeer의 데모는 여러 반응을 하나씩 더해 차이를 보는 방법을, *God of War* 팀은 가까운 플레이어 제어 카메라로 바뀌면서 전투 자체를 다시 설계한 경험을 보여준다. 기본 구도에서 공격자, 접촉 위치, 다음 위협이 보이는지부터 확인한다. [Juicing Your Cameras With Math GDC](https://www.gdcvault.com/play/1023557/Math-for-Game-Programmers-Juicing) · [Eiserloh 발표 자료](https://media.gdcvault.com/gdc2016/Presentations/Eiserloh_Squirrel_JuicingYourCameras.pdf) · [Vlambeer 발표](https://www.youtube.com/watch?v=AJdEqssNZ-U) · [God of War 전투·시점 GDC](https://www.gdcvault.com/play/1026423/Evolving-Combat-in-God-of) · [카메라 추적과 감쇠 지식](../../knowledge/game/K-GAME-TECH-CAMERA.kr.md)

## 5. 소리의 공격·접촉·여파를 따로 조정한다

| 소리 층 | 전달할 것 | 저작과 믹스 판단 |
| --- | --- | --- |
| **휘두름·발사 준비** | 속도, 방향, 무기의 크기, 공격 시점 | 허공을 가르는 소리와 공격자의 기합은 접촉 전에도 발생할 수 있다. 적의 중요한 예고음이 내 연타와 음악에 묻히지 않도록 우선순위를 둔다. |
| **접촉음** | 명중·가드·튕김, 맞은 재질과 충격 시작 | 소리의 첫 타격이 영상의 접촉과 묶여 들리는지 확인한다. 짧은 어택으로 접촉을 느끼게 하고 바디와 재질음을 더해 무게와 재질을 구분한다. 사운드 파일 앞부분의 무음과 실제 출력 장치의 지연도 차이를 만든다. |
| **여파** | 중량, 규모, 공간, 피격자의 상태 | 무기 공명·파편·피격음·잔향의 길이를 고른다. 연타와 다수 NPC에서 꼬리가 쌓이면 동시 재생 한도, 우선순위, 짧은 감쇠나 다른 소리의 일시적 감쇠를 검토한다. |
| **플레이어용 확인음** | 멀거나 화면 밖이라도 중요한 결과가 확정됐음을 전달 | 공간에서 들리는 소리와 로컬 확인음을 쓰는 이유를 나눈다. 같은 결과가 두 번 발생한 것처럼 들리는지, 상대의 방향 정보나 팀 신호가 가려지는지 확인한다. |

**강한 소리와 큰 소리에는 다른 조정 방법이 있다.** 같은 볼륨에서 짧은 시작음, 재질층, 여파를 바꿔 비교한다. 기본 타격에는 변주를 두되 가드·패링·피해가 다른 종류로 들리는 특징을 유지한다. 저음이 약한 소형 스피커, 헤드폰, 음악·대사가 겹치는 조건에서 테스트한다. *UNDERDOGS* 발표는 작은 VR 스피커에서 강한 전투 오디오를 전달하는 실제 제작 사례이고, *Kingdom Under Fire* 글은 휘두름·피격·재질음을 어떻게 나눠 생각하는지 보여준다. [UNDERDOGS 사운드 GDC](https://gdcvault.com/play/1035486/Visceral-Sound-on-Tiny-Speakers) · [Kingdom Under Fire 제작 글](https://www.gamedeveloper.com/audio/improving-the-combat-impact-of-action-games) · [Unreal 동시 재생 규칙](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-concurrency-reference-guide)

리듬 액션은 입력 허용 구간과 음악 재생 시계, 화면과 소리의 보정 범위를 처음에 정한다. 예정되어 있는 박자·전환은 오디오 시계로 스케줄할 수 있고, 명중 후에야 알 수 있는 접촉음은 확정 시점과 출력 지연을 관찰한다. 일반 액션에서도 연출의 시작을 무엇에 맞출지 명시하면 애니메이션의 모양을 고친 뒤 사운드가 뒤따라 늦어지는 문제를 찾기 쉽다. [Hi-Fi RUSH 디렉터 GDC](https://gdcvault.com/play/1034256/Developing-Hi-Fi-RUSH-Backwards) · [Unity PlayScheduled](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/AudioSource.PlayScheduled.html) · [게임 음악 타이밍 지식](../../knowledge/game/K-GAME-TECH-MUSIC.kr.md)

## 6. 햅틱과 접근성

진동은 짧은 펄스의 길이·강도·채널과 반복 간격을 설계해 충격이나 방향을 보강할 수 있다. *Returnal* 팀은 비를 작은 펄스로, 대시 방향을 손의 좌우로, 강한 착지를 그에 맞는 충격으로 표현했다. 지속 진동이 큰 충격을 가리면 배경은 낮게, 타격은 짧게, 중요한 상태는 고유한 패턴으로 구분한다. 패드마다 모터와 가능한 패턴이 다르므로 지원 장치와 키보드·마우스에서 각각 플레이한다. [Housemarque·PlayStation 사운드팀 제작 글](https://blog.playstation.com/?p=349009) · [햅틱 비교 연구](https://uwspace.uwaterloo.ca/bitstream/handle/10012/16894/Juicy_Haptic_Design_SIGCHI_2021__UWSpace_.pdf) · [Unreal 기기별 Force Feedback](https://dev.epicgames.com/documentation/en-us/unreal-engine/force-feedback-in-unreal-engine)

중요한 경고와 결과는 두 감각 경로 이상에서 전달할 방법을 정한다. 예를 들어 패링 성공은 짧은 소리와 독특한 형태를, 화면 밖 위협은 공간음과 방향 표시를 사용할 수 있다. 흔들림·헤드밥·모션 블러·진동 강도는 별도로 조절할 수 있게 하고, 섬광 효과는 빠르게 겹치는 전투 전체에서 검사한다. 효과를 줄이는 설정에서도 판정과 플레이에 필요한 정보가 유지되는지 직접 확인한다. [Xbox XAG 103 감각 경로](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/103) · [XAG 110 햅틱](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/110) · [XAG 117 움직임](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/117) · [XAG 118 섬광 검토](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/118) · [OneStep 접근성·온보딩](../../knowledge/game/K-GAME-ACCESSIBILITY-ONBOARDING.kr.md)

## 7. 장르별로 다른 손맛

| 장르 | 핵심 조건 | 먼저 비교할 표현 |
| --- | --- | --- |
| **격투·근접 액션** | 상대의 위협과 공격의 유효 구간, 확정 명중·가드·패링·회복의 차이 | 접촉 포즈와 짧은 정지, 상대의 반응 방향, 결과별 소리부터 비교한다. 군중전에서 이펙트가 가리는 정도도 확인한다. |
| **FPS·TPS·협동 액션** | 조준을 유지하면서 발사를 즉시 느끼고, 서버가 확정한 결과를 구별 | 발사 애니메이션과 발사음, 정확한 판정에 연결된 확인음, 피해 방향을 고른다. 카메라 반동과 탄도, 지연·보정에서의 중복 연출을 검사한다. |
| **플랫포머·레이싱** | 입력의 연속성과 물리 상태의 전환을 느낄 수 있음 | 착지·벽 접촉·그립 상실·충돌을 서로 다르게 표현한다. 같은 접근 속도에서 변화를 인식하고 다음 점프나 조향을 조절할 수 있는지 확인한다. |
| **리듬 액션** | 오디오·시각·입력의 기준 시간과 오차 피드백 | 성공·빠름·늦음의 신호, 오디오와 디스플레이 지연 보정, 장치 변경 뒤 판정 감각을 비교한다. |
| **퍼즐·턴제** | 입력 접수, 규칙 결과, 진행 단계가 짧고 확실하게 보임 | 상자가 움직일 때와 막힐 때, 카드 효과와 턴 종료를 분명히 구분한다. 반복 행동에서 컷·긴 여파가 다음 입력을 늦추는지 살핀다. |

## 8. Unity와 Unreal에서 판정과 연출을 연결한다

**공통 설계.** 입력에서 공격이 시작된 사건과 접촉 판정이 확정된 사건을 분리한다. 전투 규칙이 결과·대상·접촉 위치·방향과 필요한 경우 피해·경직을 소유한다. 표현을 담당하는 쪽은 같은 결과에 해당하는 애니메이션·이펙트·소리·카메라·햅틱을 선택한다. 예를 들어 두 무기가 같은 가드 판정을 쓰면 재질·세기별 표현을 공유하고 각 공격의 궤적과 회복 시간을 따로 저작할 수 있다. 실제로 필요한 사건과 데이터만 두고 기존 게임의 소유권과 진입점을 사용한다. [게임플레이 프레임워크와 콘텐츠 설계](../../skills/vegabond-code-design/references/gameplay-framework.kr.md) · [공격·피격·물리 충돌 계약](../../knowledge/game/K-GAME-TECH-HITBOX.kr.md)

| 분야 | Unity | Unreal Engine |
| --- | --- | --- |
| **카메라** | Cinemachine을 쓰는 프로젝트에서 Impulse Source·Listener와 필터링으로 발생 위치·채널·응답 곡선을 관리할 수 있다. 조준과 추적 카메라의 기본 동작을 함께 확인한다. [Cinemachine Impulse](https://docs.unity3d.com/Packages/com.unity.cinemachine%403.1/manual/CinemachineImpulse.html) | Camera Shake 자산과 소스를 사용해 단발 패턴과 공간 감쇠를 고를 수 있다. 플레이어 카메라의 정보와 시야가 유지되는지 확인한다. [Camera Shakes](https://dev.epicgames.com/documentation/en-us/unreal-engine/camera-shakes-in-unreal-engine) |
| **이펙트·애니메이션** | Animator와 Particle System 또는 VFX Graph를 프로젝트에 맞게 사용한다. 접촉 위치·표면·결과를 표현 입력으로 전달한다. [Visual Effect Graph](https://docs.unity3d.com/Packages/com.unity.visualeffectgraph%4017.0/manual/index.html) | Animation Notifies를 동작의 예정 연출에 쓰고, 명중이나 가드 연출은 게임 결과에 맞춰 연결한다. Niagara의 파라미터로 접촉 위치와 방향을 전달할 수 있다. [Animation Notifies](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-notifies-in-unreal-engine) · [Niagara 개요](https://dev.epicgames.com/documentation/unreal-engine/overview-of-niagara-effects-for-unreal-engine) |
| **사운드·진동** | Audio Mixer에서 전투·음악·대사·환경을 그룹별로 믹싱하고, 필요한 소리에는 `AudioSource.priority`를 정한다. Input System을 쓰는 게임에서 지원 패드의 진동을 연결한다. [Audio Mixer](https://docs.unity3d.com/6000.0/Documentation/Manual/AudioMixer.html) · [AudioSource 우선순위](https://docs.unity3d.com/6000.0/Documentation/ScriptReference/AudioSource-priority.html) · [Input System Gamepad](https://docs.unity3d.com/Packages/com.unity.inputsystem%401.11/manual/Gamepad.html) | Sound Concurrency 등으로 중요한 소리가 중첩 시 살아남게 하고, 필요에 따라 MetaSounds와 Force Feedback을 사용한다. [Sound Concurrency](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-concurrency-reference-guide) · [MetaSounds](https://dev.epicgames.com/documentation/en-us/unreal-engine/metasounds-the-next-generation-sound-sources-in-unreal-engine) · [Force Feedback](https://dev.epicgames.com/documentation/en-us/unreal-engine/force-feedback-in-unreal-engine) |

**멀티플레이.** 발사·공격 시작의 즉각적인 표현과 피해 확정의 표현을 구분한다. 예측 연출이 있는 프로젝트에서는 확정과 취소에 대응하고, 같은 공격의 같은 대상·타격이 확인 과정에서 두 번 재생되지 않게 한다. 지연, 손실, 다단 공격, 동시 피격에서 확인한다. Unreal에서 이미 GAS를 쓰는 경우 Gameplay Cues는 누락될 수 있는 장식 피드백에 적합하다. 피해·경직과 같이 반드시 일치해야 하는 상태는 권한 있는 게임플레이 경로가 처리한다. [Unity 클라이언트 선행 표현](https://docs.unity3d.com/Packages/com.unity.netcode.gameobjects%402.13/manual/advanced-topics/client-anticipation.html) · [Unreal GAS의 Cosmetic Effects](https://dev.epicgames.com/documentation/en-us/unreal-engine/understanding-the-unreal-engine-gameplay-ability-system#handling-cosmetic-effects)

## 9. 플레이테스트와 회귀 검증을 설계한다

1. **한 장면에서 여러 판정을 반복한다.** 같은 무기, 적, 재질, 거리에서 허공·가드·명중·강타가 나오는 경로를 정한다. 공격자의 조작 영상과 피격자·관전자 관점이 필요한 경우 각각 본다. `입력이 응답했는지`, `결과를 알아맞힐 수 있는지`, `충격이 얼마나 느껴지는지`, `다음 행동이 보이는지`를 별도 질문으로 둔다. [타격 피드백 연구](https://faculty.washington.edu/zkwen/articles/lin22features.pdf) · [플레이테스트 방식 선택](../../knowledge/game/K-GAME-PROTOTYPE-PLAYTEST.kr.md)
2. **같은 규칙에서 표현의 차이를 비교한다.** 카메라 강도, 접촉음, 히트스톱 중 의심되는 요소 하나씩 비교하고, 필요한 경우 두 요소를 조합한 조건도 포함한다. 순서를 교차해 먼저 본 효과에 익숙해지는 영향을 줄인다. 선호도 외에도 가드·명중 구분 정확도, 다음 입력 성공, 적의 예고를 놓친 횟수, 피로·불편을 함께 본다. [Kao의 피드백 강도 비교](https://experts.illinois.edu/en/publications/the-effects-of-juiciness-in-an-action-rpg/) · [Juice It or Lose It 시연](https://www.gdcvault.com/play/1016789/Juice-It-or-Lose)
3. **지연과 시간 순서를 확인한다.** 입력 접수, 규칙 판정, 애니메이션·이펙트·사운드 요청 시점을 기록한다. 실제 사용자 지연이 문제라면 입력부터 화면·소리까지 출력된 시점을 대표 장치에서 측정한다. 빠른 연타, 낮은 프레임률, 무선 오디오, 목표 네트워크 조건에서 첫 반응과 이후 판정이 어떻게 보이는지 확인한다. [FPS 입력 지연 측정 연구](https://research.nvidia.com/publication/2021-05_case-study-first-person-aiming-low-latency-esports) · [시청각 동시성 검토](https://research.tilburguniversity.edu/en/publications/perception-of-intersensory-synchrony-a-tutorial-review/)
4. **기존 품질을 확인할 경로를 남긴다.** 카메라 흔들림과 진동을 줄여도 피해·경직·콤보 판정이 유지되는지, 명중이 없을 때 명중 효과가 뜨지 않는지, 다단 공격과 반복 재시도에서 연출이 중복되거나 남지 않는지 본다. 자동 검증으로 사건 방향·횟수와 규칙 결과를 확인하고, 실제 장치에서 소리와 조작감의 차이를 플레이 리뷰한다. [회귀 검증과 시각·성능 품질](2026-11-22-gameplay-regression-verification.kr.md#5-재현-시각과-성능-품질)

첫 설계의 판단 기준은 **입력을 받았음을 느낄 수 있는가, 무엇을 맞혔는지 구별되는가, 큰 결과를 강조해도 다음 위협을 볼 수 있는가**다. 하나의 대표 공격에서 이 세 가지를 확인한 뒤 다른 무기, 적, 시점, 플랫폼에서 유지할 기준을 정한다.

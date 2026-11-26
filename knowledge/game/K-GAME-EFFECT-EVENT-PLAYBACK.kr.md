# 2D 이펙트가 실제 사건의 시점과 위치를 정확히 보여 주는가?

식별자 `K-GAME-EFFECT-EVENT-PLAYBACK` · 방법 · 사용 중 · 근거 확인일 2026-11-23

**요약** 일회성 효과는 확정된 사건에 연결하고 부착점 또는 월드 위치를 정한다. 내보낸 캐릭터·효과 트랙을 따로 보고 합성해 누락된 단서의 원인을 찾는다.

**적용 범위** 캐릭터에 부착하거나 월드에 발생시키는 2D 셀·파티클 텍스처 시트·플립북

**검색어** 2D effects, landing dust, event timing, one-shot, world space, local coordinates, exposure, draw order, SpriteFrames, GPUParticles2D, Texture Sheet Animation, 착지 먼지, 이펙트, 월드 좌표, 노출 시간, 그리기 순서, 가림, 플립북

## 활용 방법

효과별 발동 조건, 기준점, 수명, 그리기 순서를 정한다. 충전광은 손을 따라가고, 발사체는 놓는 순간 위치를 한 번 가져가며, 도착 신호는 실제 수신 뒤에 켜진다. 착지 먼지는 캐릭터가 떠나도 확정된 접촉점에 남는다. 캐릭터와 효과를 같은 시간표에 적되 셀 노출은 독립시킨다. 캐릭터가 웅크린 자세를 유지하는 사이 먼지는 두 셀을 쓸 수 있다. Godot SpriteFrames는 상대 지속 시간을 사용해 정상 속도 10FPS에서 1.2가 120ms다. Unity Texture Sheet Animation은 수명·속도·FPS를 사용할 수 있어 수명 비율에 묶인 셀은 파티클 수명을 바꾸면 때가 달라진다. [Godot SpriteFrames duration](https://docs.godotengine.org/en/stable/classes/class_spriteframes.html#class-spriteframes-method-get-frame-duration) · [Godot GPUParticles2D coordinates and one-shot restart](https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html) · [Unity Texture Sheet Animation time modes](https://docs.unity3d.com/6000.0/Documentation/Manual/PartSysTexSheetAnimModule.html)

시작과 끝의 핵심 형태를 그리고 손이 소품 뒤로 지나가거나 물막이 물방울로 갈라지는 구간을 직접 보충한다. 게임 동작에 주어진 시간 안에서 예비 동작과 회복을 읽히게 한다. 지속되는 불꽃은 각 불길의 발생과 소멸을 엇갈리게 하며, 힘의 방향과 빈 공간 변화로 물성을 표현한다. 경고 효과는 눈에 보이는 경계와 실제 영향 범위, 다른 행동에 대한 시각적 우선순위를 견준다. [Paper, Figure 1 and §4](https://studios.disneyresearch.com/wp-content/uploads/2019/03/BetweenIT-An-Interactive-Tool-for-Tight-Inbetweening-Paper.pdf) · [Authors’ abstract, paper and demonstration](https://www.cse.iitb.ac.in/~paragc/publication/2016-icvgip-01/) · [Paper](https://arxiv.org/abs/2405.17933) · [Authors’ demonstration](https://doubiiu.github.io/projects/ToonCrafter/) · [Official GDC video](https://www.youtube.com/watch?v=Mw0h9WmBlsw) · [Slides on anticipation, timing and gameplay](https://media.gdcvault.com/GDC2014/Presentations/Cartwright_Muriel_Animation_Bootcamp_Fluid.pdf) · [Keyser and Graf interview](https://www.toonboom.com/jason-keyser-and-chris-graf-on-the-secrets-behind-the-magic-of-2d-fx) · [Timing and rough motion studies](https://www.vfxapprentice.com/blog/the-soul-of-effects-what-is-timing-in-vfx) · [Riot development examples](https://www.leagueoflegends.com/en-us/news/dev/clarity-in-league/) · [Riot art education videos and materials](https://www.riotgames.com/en/artedu/visual-effects) · [GDC VFX slides](https://media.gdcvault.com/gdc2017/Presentations/Chamberlin_Keyser_ArtisticPrinciplesVFX.pdf)

## 적용 조건과 예외

제작한 미리보기에서는 고정된 접촉 시각을 사용할 수 있다. 점프 높이, 취소, 접촉 실패가 달라지는 게임에서는 해당 상태 사건이 필요하다. 벡터·영상 보간 연구는 중간 자세를 어디에 그릴지 판단하는 근거이며 엔진 지연, 픽셀 알파 품질, 플레이어 인지를 측정하지 않았다.

## 검증 방법

- 실제로 내보낸 캐릭터 단독, 효과 단독, 합성 결과를 밝고 어두운 바닥에서 목표 속도로 재생한다. 접촉과 소멸 전후를 한 프레임씩 확인하고 캐릭터와 카메라를 따로 움직인다. 사건 미발생, 중간 취소, 재발동, 끝난 뒤 잔상을 검사한다. 반복 경계의 중복 노출도 확인한다.
- 효과만 볼 때 보이면 시간을 바꾸기 전에 가림을 확인한다. 필요하면 가까운 덩어리와 먼 덩어리를 나눠 캐릭터 앞뒤에 놓는다. 흰 테두리는 경계 RGB와 직선·선곱 알파 일치를 보고, 이웃 셀 색은 패딩과 샘플링을 본다. 밝은 바닥에서 가산광이 사라지면 알파 혼합 중심부를 시험한다. [Godot CanvasItem blend modes](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html) · [Aseprite CLI](https://www.aseprite.org/docs/cli/)
- 요청을 모르는 관찰자에게 정상 속도에서 무엇이 어디서 어느 방향으로 일어났는지 묻는다. 효과가 겹친 상황에서 경고 가시성, 반복 섬광, 목표 기기 프레임 시간을 확인한다. 강도를 낮춰야 한다면 사건을 알아볼 단서를 유지한다. [Xbox Accessibility Guideline 118](https://learn.microsoft.com/en-us/gaming/accessibility/xbox-accessibility-guidelines/118)

## 근거

디코딩한 부두 착지 미리보기는 타이밍이 맞았지만 신발에 가려 첫 먼지가 거의 보이지 않았다. 가까운 덩어리만 앞으로 옮기자 불투명 픽셀 71개 중 보이는 수가 23개에서 46개가 됐다. 이 클립은 120ms에 닿고 420ms에 먼지가 사라졌다. 이는 두 배경에서 여섯 상태의 마스크 노출과 제작 시각을 확인한 값이다. 사람의 감지율, 동작의 부드러움, 엔진 입력 지연, 목표 기기 성능은 측정하지 않았다. [작화·내보내기 기록](../../output/2d-character-test/landing-effects-01/example.md) · [피벗·셀 시간·레이어](../../output/2d-character-test/landing-effects-01/timing.json) · [제작 지침](../../skills/vegabond-image/references/2d-effects-and-motion.md)

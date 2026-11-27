# 축소와 상태 변경을 견디는 게임 UI 이미지 제작

플레이어가 어떤 행동을 식별해야 하는지, 무엇과 혼동할 수 있는지, 화면에 표시될 최소 크기가 얼마인지부터 정한다. 화면 콘셉트는 배치를 보여준다. 구현용 HUD·인벤토리·메뉴라면 입력, 값, 레이아웃에 따라 바뀌는 부분을 개별 에셋으로 전달한다.

## 부품별 설계

- **아이콘·지도 핀.** 기능을 드러내는 실루엣과 내부 표식을 정한다. 회복은 넓은 플라스크와 십자, 해독은 다른 병 모양과 해독을 뜻하는 표식을 시도한다. 수량·등급·쿨다운·선택은 독립 레이어로 둔다. 화풍 레퍼런스에는 카메라·광원·선 굵기·시각적 무게를, 스케치에는 형태를 맡긴다. 핀은 밀집 상태에서도 끝점이 위치를 가리키는지 확인한다.
- **버튼·포커스.** 기본판을 승인한 뒤 눌림 음각·포커스 링·지속 선택·비활성 처리를 파생한다. 캔버스·피벗·레이블 영역을 겹쳐 맞춘다. 선택한 아이템에 포커스가 있을 때와 다른 아이템으로 옮겼을 때를 모두 합성한다. Godot TextureButton은 포커스 이미지를 기본판 위에 그린다. 실제 입력 영역과 탐색은 컨트롤에서 확인한다.
- **프레임·대화창.** 고정 장식은 나인슬라이스의 모서리 안에 두고 늘어나면 찌그러지는 문장은 별도 레이어로 낸다. 64×48 원본의 절단 여백이 사방 8 px, 내용 안쪽 여백이 12 px라면 1배율의 192×72 창에서도 모서리는 8×8이다. 폭 32에서는 글에 8 px만 남는다. 최소·보통·최대 폭에 가장 긴 실제 문구를 넣는다. 반복 무늬는 늘이기와 타일링을 비교한다.
- **게이지·쿨다운.** 빈 트랙, 가득 찬 채움이나 마스크, 프레임을 같은 좌표에 둔다. 폭 96 px가 왼쪽부터 차면 별도 캡과 반올림 전의 25%는 24 px다. 0%, 한 줄, 절반, 100%에서 빈 프레임의 장식이 잔량처럼 보이는지 확인한다. 방사형은 중심·시작각·방향을 정한다.
- **레이블·입력 안내.** 수치, 이름, 현지화 문자열과 재할당 가능한 버튼은 런타임에서 그린다. 긴 번역과 한글 글리프, 지원하는 RTL 조판, 입력기 변경을 시험한다. 뒤로 가기 화살표와 동쪽을 가리키는 나침반의 반전 규칙을 구별한다. Steam Input에서 현재 바인딩의 기호를 받을 수 있다.

## 생성 요청 예시

1. “32 px 회복 아이콘. 바다 테마 세트의 광원과 외곽선을 따르고 스케치의 넓은 배와 짧은 목을 지킨다. 가운데 큰 상아색 십자와 투명 여백을 둔다.” 해독병은 검수 합성본에만 나란히 둔다.
2. “승인된 황동 슬롯의 안쪽 베벨만 눌린 상태로 바꾼다. 네 모서리, 라벨 영역, 광원과 알파 캔버스를 정렬해 유지한다. 포커스 링은 별도다.”
3. “64×48 격자에 빈 대화창을 그린다. 황동 고정구는 8 px 모서리 밴드 안에 둔다. 곧은 측면 밴드와 조용한 중앙, 분리된 문장 장식과 빈 글 영역을 제공한다.” 실제 수치는 내보낸 파일에서 재고 정확한 마스크는 필요하면 다시 구성한다.

## 근거와 실측

McDougall·Isherwood의 아이콘 식별 연구는 초기에는 그림과 기능의 연관성, 이후에는 익숙함의 역할을 구분했다. 초견 사용자에게 예상 동작을 묻는 시험과 숙련자가 이웃 아이콘 사이에서 찾는 시험을 분리한다. IconDM은 추상 기능의 시각화와 세트 화풍 일치를 나눠 다뤘다. Scenario의 제작 과정은 스케치와 스타일 참조의 분업 사례이고, Riot은 상점의 축소 화면에서 배경 복잡도와 전경 분리를 다뤘다. 월드 공간 UI는 Dead Space 제작 사례처럼 카메라와 움직이는 밝고 어두운 배경에서 본다.

2026-11-24 회복병·해독병 두 칸을 생성한 1774×887 RGBA 시트를 등분하고 Lanczos 필터로 32×32와 24×24로 줄였다. 네 출력의 왼쪽 위는 투명이었다. 폭 4 px 원본 거터에는 알파가 1/255인 픽셀이 23개 있어 0보다 큰 알파에 맞춘 자동 트림 대신 지정 셀을 사용했다. 24 px에서 알파 ≥128인 경계는 둥근 병 18×22, 좁은 병 12×22였다. 밝고 어두운 슬롯에서 십자와 띠가 남고 회색조에서 외곽을 구별할 수 있었다. 띠만으로 ‘해독’을 연상하는지는 알 수 없다. 표식이나 현지화 이름을 바꿔 초견 판독을 시험하는 것이 다음 검증이다.

## 전달·검수

슬롯·크기·알파·여백·피벗·변형과 런타임 값을 명시한다. 출시 필터로 패킹한 뒤 실제 배경에서 대비를 확인한다. Xbox XAG 102의 일반 크기 중요 요소 권고는 4.5:1이며 큰 요소, 비활성 텍스트, 고대비 모드에는 다른 기준이 있다. 이번 시트는 픽셀 수준의 구별을 관찰했다. 사람의 의미 식별률, 기준선 대비 개선, 엔진 임포트와 접근성 적합성은 별도 검증 대상이다.

## 출처

[IconDM](https://www.microsoft.com/en-us/research/publication/icondm-text-guided-icon-set-expansion-using-diffusion-models/) · [Riot](https://www.leagueoflegends.com/en-au/news/dev/quick-gameplay-thoughts-nov-20/) · [Godot TextureButton](https://docs.godotengine.org/en/stable/classes/class_texturebutton.html) · [Xbox focus guidance](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/113) · [Unity nine-slicing](https://docs.unity3d.com/6000.0/Documentation/Manual/sprite/9-slice/9-slicing.html) · [Godot NinePatchRect](https://docs.godotengine.org/en/stable/classes/class_ninepatchrect.html) · [Godot TextureProgressBar](https://docs.godotengine.org/en/4.5/classes/class_textureprogressbar.html) · [Xbox additional cue guidance](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/103) · [Godot localization](https://docs.godotengine.org/en/4.5/tutorials/i18n/internationalizing_games.html) · [Steam Input origin and glyph API](https://partner.steamgames.com/doc/api/isteaminput) · [Xbox contrast criteria and examples](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/102) · [Xbox focus examples](https://learn.microsoft.com/en-us/xbox/accessibility/xbox-accessibility-guidelines/113) · [Paper](https://link.springer.com/content/pdf/10.3758/BRM.41.2.325.pdf) · [Microsoft Research](https://www.microsoft.com/en-us/research/publication/icondm-text-guided-icon-set-expansion-using-diffusion-models/) · [Creator workflow](https://help.scenario.com/articles/4516993982-designing-icons-for-a-match-3-game) · [Development notes](https://www.leagueoflegends.com/en-au/news/dev/quick-gameplay-thoughts-nov-20/) · [Developer presentation](https://www.youtube.com/watch?v=pXGWJRV1Zoc)

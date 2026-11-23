# 등대 정비사 2D 캐릭터 가이드 테스트

OneStep `8b98bd2`의 [2D 캐릭터 제작 지침](../../../skills/vegabond-image/references/2d-game-characters.md)을 적용했다. 이전 기준 일러스트 (`../lighthouse-mechanic/portrait.png`)를 두 생성의 공통 디자인 참조로 사용했다. 두 자산은 내장 imagegen으로 새로 생성했다.

| 자산 | 확인 방법과 결과 |
| --- | --- |
| 대화 일러스트 (`portrait.png`) | 1254×1254 원본. 360×360 모의 대화 슬롯에 넣고 아래쪽 82픽셀을 대사창으로 덮었다. 오른쪽을 향한 눈, 살짝 열린 입, 귀 근처에 든 장갑과 스카프가 보인다. |
| 인게임 대기 자세 (`idle-64.png`) | 투명 생성 원본 (`idle-source.png`)을 축소하고 팔레트를 정리했다. 64×64 RGBA, 인물 24×60, 가시색 14개, 알파 0과 255. 밝고 어두운 모의 부두에서 각각 1배로 보았다. 오른쪽을 향한 얼굴과 밝은 앞머리, 주황 스카프가 남는다. 열쇠는 확대하면 보이지만 1배에서는 금색 장식으로도 읽힌다. |

배치 미리보기 (`review.png`). 게임 엔진 임포트와 애니메이션 재생은 이 정지 자산 테스트의 범위 밖이다.

## 사용한 프롬프트

### 대화 일러스트

Use the supplied painting as character design only. Paint a fresh, square cropped dialogue portrait for this 2D narrative adventure. Same adult woman lighthouse mechanic, freckles, ink-black bob with one broad ivory forelock, orange triangular scarf, cropped petrol-blue jacket, ochre tool belt. New acting beat: she has heard a second foghorn in the mist. She pauses in mid-task, one gloved hand lightly cupped behind her near ear, eyes alert and looking screen-right out to sea, mouth just parted. Keep her whole head including hair and raised hand within the upper three quarters, leave lower quarter for a dialogue overlay, textured gouache and clean ink masses, muted harbor sky at dawn. No text, interface, border or panel divisions.

### 인게임 스프라이트

Use supplied painting for the identity and costume of a single protagonist in a side-scrolling 2D game. Make a new transparent pixel art gameplay sprite. Right-facing full body, relaxed alert standing idle, forward boot slightly ahead, profile nose, separated feet. Black bob with one generously sized ivory forelock, orange triangular scarf solid block, petrol-blue jacket, ochre belt and pouch, work trousers and boots. Her brass tide key hangs from the belt outside the hip silhouette as a bold simple gold ring joined to a short toothed stem, visibly separate from the pouch and hands. Strong deliberate pixel clusters, sturdy low-res proportions and chunky key proportions, approx 60 logical pixels character height, square canvas with breathing room around soles and head, simple restrained palette. One figure only, true transparent surrounding area, no stage or floor shadow or text.

# 등대 정비사의 착지와 먼지

재생 미리보기 (`playback.png`)는 같은 착지를 두 가지 바닥색에서 두 배로 확대해 보여 준다. 정지 프레임 (`timeline.png`)으로 발바닥과 먼지의 겹침을 따로 볼 수 있다. 미리보기는 비교를 위해 900ms마다 다시 시작한다. 게임에서 착지 먼지는 한 번만 발생한다.

## 원본 셀과 재생 방법

- 캐릭터 시트 (`actor.png`)는 64×72 셀 세 장이다. 왼쪽부터 하강, 첫 접지, 회복 순서이며 클립의 0, 120, 240ms에 각각 표시한다.
- 먼지 시트 (`dust.png`)는 64×24 셀 세 장이다. 착지 이벤트가 일어난 바닥 위치에서 시작하고, 이벤트로부터 0, 60, 180ms에 다음 그림을 표시한 뒤 300ms에 지운다. 착지가 발생하지 않으면 생성하지 않는다.
- [재생 데이터](timing.json)에 좌상단 기준 피벗, 레이어, 픽셀 필터와 합성 방법을 기록했다. 이 예시에서는 먼지의 왼쪽 절반이 가까운 덩어리다. 다른 방향으로 그린 먼지에는 해당 그림의 앞뒤 관계에 맞는 마스크를 써야 한다.

## 생성에 사용한 요청

캐릭터는 기존 정비사 (`../lighthouse-guide-8b98bd2/idle-64.png`)를 참조했다. 두 시트는 별도로 생성하고, 트랙별로 공통 배율과 기준선을 적용해 내보냈다. 다음은 생성기에 전달한 두 요청이다.

**캐릭터**

The supplied sprite is the identity, palette, scale and right-facing gameplay camera reference. A single transparent landscape 3:1 horizontal sprite strip, exactly three equally spaced separate full-body drawings in equal square cells, each centered horizontally with clear padding. One short landing sequence for the same adult lighthouse mechanic. Cell 1 descends, knees slightly tucked and boots clear. Cell 2 touches down and compresses compactly, bent knees, hips low, both shoes load. Cell 3 straightens to a balanced upright standing idle. Use same head size in all three. Retain ink bob, large ivory hair streak, orange scarf, blue work jacket, brass tool pouch and boots. True transparent background, no platform, shadow, dust, labels, dividing lines or scenery. 2D limited-palette chunky pixel art; distinct leg and upper body silhouettes.

**먼지**

Draw an animation asset, one horizontal wide sprite strip, three equal cells separated by ample TRANSPARENT empty gutters. Three consecutive hand-drawn pixel-art cels of the same small tan landing dust puff spreading out from a single point on a flat dusty dock. Cel one compact pair of tiny outward spurts. Cel two wider asymmetric rolling low lobes and a couple of grit flecks surrounding the same center with a hole opening. Cel three still wider broken thin fragments curling away with long transparent gaps and little remaining mass. Exactly three distinct stages, fixed ground line, position and scale, one simple continuous causal motion. Opaque warm ochre and desaturated umber pixel clusters with light sandy accents, no soft glow. True transparent background. No character, ground, shadow, labels, frame lines or scenery.

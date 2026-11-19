# 시야에 맞는 빌보드 방향과 알파 처리 선택하기

**K-GAME-TECH-BILLBOARD** · 이미지 평면이 카메라를 향하는 방식을 고른 뒤 사용할 시점에서 실루엣, 텍스처 방향, 투명도와 그림자를 확인한다.

## 지침

화면 정렬 빌보드는 카메라의 오른쪽·위쪽 축을 따른다. 시점 지향 빌보드는 개별 눈 또는 카메라 위치를 바라보고 위쪽 벡터를 평면에 투영한다. 축 고정 빌보드는 정해진 축을 중심으로 회전한다. 식생에서는 흔히 월드 위쪽 축을 쓴다. 시선이 축과 일치하면 방위각을 정할 수 없으므로 마지막 유효 방향 또는 초기 대체 방향을 사용한다.

## 적용 조건과 예외

이미지 임포스터와 식생에서 마스크 머티리얼은 임계값을 기준으로 텍셀을 버린다. 반투명 블렌딩은 부분 투과를 보존하지만 평면이 겹치면 정렬 문제가 드러난다. 오버드로는 화면상 픽셀 점유율에, 그림자는 머티리얼과 렌더 패스에 좌우된다.

## 확인 방법

평면 위아래로 카메라를 돌리고 롤을 바꾼다. UV의 서로 다른 모서리에 표식을 넣어 뒤집힘을 찾는다. 겹친 층, 그림자의 불투명 부분과 구멍, 스테레오 시점, 비슷한 픽셀 점유율에서의 GPU 시간을 비교한다.

## 근거

Godot 문서는 방향 옵션을, GPU Gems는 교차 식생 카드 사용을, Epic 문서는 블렌드 모드를 설명한다. 기존 언리얼 관찰은 실제 달성한 프레임률에서 일부 방향·컷아웃·겹침을 확인했다. 목표 프레임률 일부에 도달하지 못했고 스테레오, 일반 정렬, GPU 오버드로는 측정하지 않았다.

- [Godot — Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html)
- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass)
- [Epic blend modes](https://dev.epicgames.com/documentation/unreal-engine/material-blend-modes-in-unreal-engine?lang=en-US)
- [material properties](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-material-properties)

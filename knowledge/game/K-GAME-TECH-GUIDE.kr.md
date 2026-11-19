# 개발 문제에서 필요한 게임 구현 기법 찾기

**K-GAME-TECH-GUIDE** · 관찰한 증상이나 필요한 동작으로 관련 기법을 찾고 실제 게임에서 전제 조건을 확인한 뒤 선택한다.

## 지침

관찰 가능한 실패와 관련 시계·형상·플랫폼·판정 권한을 기록한다. 표시 주기에 따라 점프 높이가 달라지면 [고정 스텝](K-GAME-TECH-TIMESTEP.kr.md)과 [입력 유예](K-GAME-TECH-CONTROLLER.kr.md)를, 발이 미끄러지면 [IK](K-GAME-TECH-IK.kr.md)를 본다. 게임의 적중 판정이 어긋나면 [공격 볼륨](K-GAME-TECH-HITBOX.kr.md), [히트스캔](K-GAME-TECH-HITSCAN.kr.md), [과거 시점 판정](K-GAME-TECH-LAGCOMP.kr.md)을 구분한다. 경로가 충돌하면 [길찾기](K-GAME-TECH-PATH.kr.md)와 [군중 조정](K-GAME-TECH-CROWD.kr.md)을, 표시 비용이 크면 [식생](K-GAME-TECH-FOLIAGE.kr.md)·[빌보드](K-GAME-TECH-BILLBOARD.kr.md)·[그림자](K-GAME-TECH-SHADOW.kr.md)를 비교한다. 아래 표에서 전체 주제를 찾을 수 있다.

## 적용 조건과 예외

게임 설계·개발·디버깅에서 공개 영상은 질문을 찾는 출발점이다. 논문이나 개발자의 직접 설명은 해당 기법을, 엔진 API 문서는 해당 버전의 계약을 뒷받침한다. 다른 엔진·플랫폼·부하에 적용할 때는 [근거 재사용 지침](K-GAME-RESEARCH-USE.kr.md)을 참고한다.

## 확인 방법

항목의 적용 조건과 원 출처를 읽는다. 대표 장면, 반례, 관찰할 합격 조건을 정한다. 문제에 맞춰 실제 갱신률, 프레임 비용, 플레이 결과를 측정한다. 게임별 설정값·원시 실행 결과·도입 결정은 해당 프로젝트에 기록한다.

## 근거

아래 표는 주제를 발견하는 데 사용한 공개 영상과 관련 항목을 연결한다. 버전별 API 문서, 개발진의 직접 설명, 알고리즘 출처는 개별 항목에 있다. 다음은 대표적인 원 저자의 구현 설명과 유도 과정이다.

- [Glenn Fiedler — Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)
- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html)
- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass)
- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)

### 주제를 찾는 데 사용한 공개 영상

| ID | 원본 영상 | 관련 기법 |
| --- | --- | --- |
| V01 | [게임 속 대도시에 사람이 없는 이유](https://www.youtube.com/shorts/iAn8FPI_Fbo) | [CROWD](K-GAME-TECH-CROWD.kr.md) |
| V02 | [게임 프레임에 숨겨진 게임의 시간 계산법](https://www.youtube.com/shorts/Nx4pdJ2lDas) | [TIMESTEP](K-GAME-TECH-TIMESTEP.kr.md) |
| V03 | [그림자를 만드는 게임의 신기한 기법](https://www.youtube.com/shorts/BG70G1Y8Llw) | [SHADOW](K-GAME-TECH-SHADOW.kr.md) |
| V04 | [치트와 렉을 막는 게임 네트워크 처리](https://www.youtube.com/shorts/b-8DpsYLI7Y) | [AUTHORITY](K-GAME-TECH-AUTHORITY.kr.md); [LOCKSTEP](K-GAME-TECH-LOCKSTEP.kr.md) |
| V05 | [노가다를 없애는 게임의 보상 설계법](https://www.youtube.com/shorts/eHn7TLjzVFU) | [INCENTIVES](K-GAME-TECH-INCENTIVES.kr.md) |
| V06 | [빠른 속도를 만드는 게임의 카메라 연출](https://www.youtube.com/shorts/IQVeIrF3KfE) | [SPEED](K-GAME-TECH-SPEED.kr.md) |
| V07 | [마인크래프트에서 자연 환경을 자동 생성하는 방법?](https://www.youtube.com/shorts/3W1tKXhbiEk) | [NOISE](K-GAME-TECH-NOISE.kr.md) |
| V08 | [게임에서 하이힐을 보기 힘든 이유](https://www.youtube.com/shorts/UqMLCjSqwyA) | [IK](K-GAME-TECH-IK.kr.md) |
| V09 | [게임에 좋은 랜덤과 나쁜 랜덤이 있다?](https://www.youtube.com/shorts/vdbjOLEMQSg) | [RANDOM-DESIGN](K-GAME-TECH-RANDOM-DESIGN.kr.md) |
| V10 | [게임 속 연막탄이 가짜 연출인 이유?](https://www.youtube.com/shorts/9JsRRFL8G0c) | [VOLUME](K-GAME-TECH-VOLUME.kr.md) |
| V11 | [게임의 월드맵은 왜 실제보다 크게 느껴질까?](https://www.youtube.com/shorts/Mo3JFBC_jzk) | [LEVEL](K-GAME-TECH-LEVEL.kr.md) |
| V12 | [게임 속 문이 현실보다 거대한 이유는?](https://www.youtube.com/shorts/ncXQqHiFjHQ) | [LEVEL](K-GAME-TECH-LEVEL.kr.md) |
| V13 | [게임사가 긴 머리 캐릭터를 싫어하는 이유?](https://www.youtube.com/shorts/ZiQo1jKDRvY) | [HAIR](K-GAME-TECH-HAIR.kr.md) |
| V14 | [게이머를 속이는 게임 속 파괴 연출](https://www.youtube.com/shorts/QSqcR2sLkdo) | [DESTRUCTION](K-GAME-TECH-DESTRUCTION.kr.md) |
| V15 | [게임 창문 속 방이 전부 가짜인 이유](https://www.youtube.com/shorts/-gaC6ZtDqDc) | [INTERIOR](K-GAME-TECH-INTERIOR.kr.md) |
| V16 | [게이머의 눈을 속이는 게임 속 거울의 비밀](https://www.youtube.com/shorts/OCLRh6VDupM) | [REFLECTION](K-GAME-TECH-REFLECTION.kr.md) |
| V17 | [겁쟁이를 참교육하는 게임의 전투 설계](https://www.youtube.com/shorts/IZ0zeYEfqjY) | [INCENTIVES](K-GAME-TECH-INCENTIVES.kr.md) |
| V18 | [게임 시야각에 쓰이는 신기한 수학](https://www.youtube.com/shorts/tfShkMZ49NU) | [TRACE](K-GAME-TECH-TRACE.kr.md) |
| V19 | [게임 속 잔디를 만드는 궁극의 최적화 기법](https://www.youtube.com/shorts/BtBXRm1noIg) | [FOLIAGE](K-GAME-TECH-FOLIAGE.kr.md) |
| V20 | [게임은 저장을 어떻게 할까?](https://www.youtube.com/shorts/0fap5_6orlw) | [SAVE](K-GAME-TECH-SAVE.kr.md) |
| V21 | [게임 세계를 건축하는 놀라운 기술](https://www.youtube.com/shorts/OS3OjZ607So) | [VOXEL](K-GAME-TECH-VOXEL.kr.md) |
| V22 | [게임 소리를 만드는 신기한 물리 현상들](https://www.youtube.com/shorts/1q9srGjkpD0) | [SOUND](K-GAME-TECH-SOUND.kr.md) |
| V23 | [게임의 의도가 담겨진 카메라의 위치 연출법](https://www.youtube.com/shorts/xNp8De8CEoI) | [CAMERA](K-GAME-TECH-CAMERA.kr.md) |
| V24 | [플레이어의 행동을 조종하는 게임 속 맵 설계](https://www.youtube.com/shorts/tQDBuXB6Juo) | [LEVEL](K-GAME-TECH-LEVEL.kr.md) |
| V25 | [게임 음악에 사용되는 신기한 전환 기법](https://www.youtube.com/shorts/WkvlFYUlvns) | [MUSIC](K-GAME-TECH-MUSIC.kr.md) |
| V26 | [게임 그래픽을 실감나게 하는 마법](https://www.youtube.com/shorts/i6Mu34lCSb0) | [NORMAL](K-GAME-TECH-NORMAL.kr.md) |
| V27 | [게임 하늘을 만드는 신기한 수학 기법](https://www.youtube.com/shorts/UxTa_8XlJfo) | [VOLUME](K-GAME-TECH-VOLUME.kr.md) |
| V28 | [시간을 되감는 FPS 게임의 사격 판정](https://www.youtube.com/shorts/o7waSG4jROw) | [LAGCOMP](K-GAME-TECH-LAGCOMP.kr.md) |
| V29 | [슈퍼 마리오의 조작감은 왜 혁신적일까?](https://www.youtube.com/shorts/dNsyscOrNMY) | [CONTROLLER](K-GAME-TECH-CONTROLLER.kr.md) |
| V30 | [플랫폼 게임 맵 모서리에 있는 점프 위치 보정](https://www.youtube.com/shorts/hjVLIojpwVk) | [CONTROLLER](K-GAME-TECH-CONTROLLER.kr.md) |
| V31 | [느린 네트워크 속도를 게임이 보정하는 비법](https://www.youtube.com/shorts/kap1_O66XCY) | [ROLLBACK](K-GAME-TECH-ROLLBACK.kr.md) |
| V32 | [게임 속 물 표현을 하는 수식을 만드는 방법](https://www.youtube.com/shorts/RFDIq0ZdJ3s) | [WATER](K-GAME-TECH-WATER.kr.md) |
| V33 | [게임 상대를 결정하는 매칭 시스템의 원리](https://www.youtube.com/shorts/uMCwH38GpuY) | [MATCH](K-GAME-TECH-MATCH.kr.md) |
| V34 | [게임의 쾌감을 주는 위험 대 보상 설계](https://www.youtube.com/shorts/SauTVeoo6K0) | [INCENTIVES](K-GAME-TECH-INCENTIVES.kr.md) |
| V35 | [게임 속 픽셀 아트에 숨겨져 있는 규칙들](https://www.youtube.com/shorts/Ce5YdbY4upM) | [PIXEL](K-GAME-TECH-PIXEL.kr.md) |
| V36 | [게임 속 길찾기에 숨겨져 있는 수학 이론](https://www.youtube.com/shorts/qMGONAZGIqE) | [PATH](K-GAME-TECH-PATH.kr.md) |
| V37 | [게임 캐릭터가 계단을 오르는 기법](https://www.youtube.com/shorts/0rjhNtdmgVI) | [IK](K-GAME-TECH-IK.kr.md) |
| V38 | [선을 쏘아 알아내는 게임의 시야 계산법](https://www.youtube.com/shorts/PRwkpITfW-s) | [TRACE](K-GAME-TECH-TRACE.kr.md) |
| V39 | [눈에서 총알이 튀어나오는 FPS 게임의 사격 판정](https://www.youtube.com/shorts/kucqGt8Q2a8) | [HITSCAN](K-GAME-TECH-HITSCAN.kr.md) |
| V40 | [랜덤 생성 던전을 게임이 만드는 방법](https://www.youtube.com/shorts/_0qjqwigjLc) | [DUNGEON](K-GAME-TECH-DUNGEON.kr.md) |
| V41 | [플레이어에 접대하는 게임의 난이도 조절](https://www.youtube.com/shorts/kkhqAHTcu5I) | [DDA](K-GAME-TECH-DDA.kr.md) |
| V42 | [게이머에게 관대한 게임의 피격 판정](https://www.youtube.com/shorts/hUpx8lUaiDU) | [HITBOX](K-GAME-TECH-HITBOX.kr.md) |
| V43 | [게이머를 속이는 게임의 3D 연출 방법](https://www.youtube.com/shorts/DXsKd52lomQ) | [BILLBOARD](K-GAME-TECH-BILLBOARD.kr.md) |
| V44 | [불운을 관리하는 게임의 확률 조작법](https://www.youtube.com/shorts/eyrRduWl-qo) | [RANDOM-DESIGN](K-GAME-TECH-RANDOM-DESIGN.kr.md) |
| V45 | [게임 이펙트를 만드는 신기한 색상 계산](https://www.youtube.com/shorts/Of9pFtvVBJQ) | [BLEND](K-GAME-TECH-BLEND.kr.md) |
| V46 | [게임 점프에 숨겨진 판정 타이밍 조절](https://www.youtube.com/shorts/0gkwRtolL4Y) | [CONTROLLER](K-GAME-TECH-CONTROLLER.kr.md) |
| V47 | [게임 애니메이션을 만드는 수학](https://www.youtube.com/shorts/TomzUe30Ltg) | [EASING](K-GAME-TECH-EASING.kr.md) |
| V48 | [게임 카메라에 숨겨진 수학 기법](https://www.youtube.com/shorts/caPi9d2gP7I) | [CAMERA](K-GAME-TECH-CAMERA.kr.md) |
| V49 | [물리 역학을 무시하는 게임 점프의 수식](https://www.youtube.com/shorts/dluLPk0zjIs) | [TIMESTEP](K-GAME-TECH-TIMESTEP.kr.md) |
| V50 | [게임에서 지형을 만들 때 쓰는 특수한 수학 기법](https://www.youtube.com/shorts/kY9TYQYxCZM) | [NOISE](K-GAME-TECH-NOISE.kr.md) |
| V51 | [젤다의 전설 야숨을 디자인한 특별한 게임 엔진](https://www.youtube.com/shorts/1yxDf1WUIBk) | [SYSTEMIC](K-GAME-TECH-SYSTEMIC.kr.md) |
| V52 | [게임 컨트롤러로 게임을 즉석에서 재구축하는 방법](https://www.youtube.com/shorts/uj6016N96JY) | [MEMORY](K-GAME-TECH-MEMORY.kr.md) |
| V53 | [세계 최초로 에임핵을 도입한 게임](https://www.youtube.com/shorts/OjbUm_hnYFU) | [LOCKON](K-GAME-TECH-LOCKON.kr.md) |
| V54 | [비밀번호가 세이브 파일이 되었던 고전 게임](https://www.youtube.com/shorts/ave58m6vuDw) | [SAVE](K-GAME-TECH-SAVE.kr.md) |
| V55 | [고전 게임에서 확률 조작하는 방법](https://www.youtube.com/shorts/djGVMe4imWw) | [RNG](K-GAME-TECH-RNG.kr.md) |
| V56 | [전설로 남은 게임의 랜덤맵 생성](https://www.youtube.com/shorts/vVVyFUzs-HM) | [DUNGEON](K-GAME-TECH-DUNGEON.kr.md) |
| V57 | [3D처럼 눈속임하는 고전 게임의 비밀](https://www.youtube.com/shorts/R06WXFSWYvo) | [RETRO](K-GAME-TECH-RETRO.kr.md) |
| V58 | [마른 이미지 용량 쥐어짜기](https://www.youtube.com/shorts/p0mH7UAwtXQ) | [PIXEL](K-GAME-TECH-PIXEL.kr.md) |
| V59 | [벡터파일에서 곡선을 어떻게 저장할까?](https://www.youtube.com/shorts/0MySBqE02fU) | [EASING](K-GAME-TECH-EASING.kr.md) |

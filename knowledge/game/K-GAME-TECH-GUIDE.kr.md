# 게임 개발 기술 안내서

기준 항목: K-GAME-TECH-GUIDE · 확인일: 2026-11-07. 관련 쇼츠 59편을 원리 중심 기술 43개로 연결한다. 출처 확인과 실제 엔진·성능 검증은 구분한다.

## 상황에 맞게 활용

[게임 근거 활용 규칙](K-GAME-RESEARCH-USE.kr.md)을 Scout·기획·코드·코드 설계 진입 지침에 연결했다. 실제 문제·기능으로 조회하고 적용 조건을 읽은 뒤 채택·조건부·기각을 판단한다. 문제·제약 → 항목 ID·출처 위치 → 결정·이유 → 변경 → 검사·관찰 결과를 기존 작업 브리프에 남긴다.

1. 엔진·버전, 플랫폼, 프레임 예산, 카메라, 네트워크·상태 권한을 확인한다.
2. 증상·원리로 후보를 찾고 근거 한계를 보존한다. 검색이 빗나가면 아래 대응표를 쓴다.
3. 대안을 비교하고 대표 장면의 작은 실험과 측정 기준을 정한다.
4. 대상 기기에서 측정하고 필요하면 플레이어 이해도를 관찰한다.
5. 실제 적용 값·기각 이유·관찰·남은 실패를 프로젝트에 기록하고 지식으로 반환한다.

| 개발 상황 | 출발 항목 |
| --- | --- |
| 야외 장면이 느림 | FOLIAGE 잔디·수목, SHADOW 그림자, CROWD 군중 |
| 의도한 이동·점프가 안 됨 | CONTROLLER 입력 유예, TIMESTEP 시간 간격, IK 접지 |
| 화면과 공격 판정이 다름 | HITSCAN 조준·총구, HITBOX 판정, LAGCOMP 지연 보정 |
| 멀티플레이 반응이 둔함 | AUTHORITY 권한, LOCKSTEP 입력 동기화, ROLLBACK 복원·재실행 |
| 생성한 세계를 플레이할 수 없음 | NOISE 지형, DUNGEON 경로 보장, PATH 길찾기 |
| 시점이 불편하거나 정보를 못 읽음 | CAMERA 카메라, SPEED 속도 효과, LEVEL 공간 규모 |
| 결과가 반복적이거나 불공정하게 느껴짐 | RANDOM-DESIGN 무작위성, INCENTIVES 보상, DDA 페이싱 |

넓은 설계 결정은 기존 플랫폼·멀티플레이·경제·전투·탐험·프로토타입/플레이테스트 항목도 활용한다.

## 추가 조사로 보완한 범위

| 기술 | 확인한 세부와 남은 한계 |
| --- | --- |
| [화학 상호작용](K-GAME-TECH-SYSTEMIC.kr.md) | 원본 슬라이드의 세 규칙 확인. 이벤트 순서·자료구조는 프로젝트별 설계. |
| [군중](K-GAME-TECH-CROWD.kr.md) | 히트맨 원본 슬라이드에서 격자·출구별 흐름장·지역 회피·NPC 승격 확인. 예산은 당시 기준. |
| [Mode 7](K-GAME-TECH-RETRO.kr.md) | 에뮬레이터 렌더 루프 확인. 원작 게임 코드·하드웨어 타이밍 재현은 별도. |
| [저장·암호](K-GAME-TECH-SAVE.kr.md) | 공개 재구성 코드의 세대 복구, 역공학 원저자의 암호 상태 구조 보완. 장애 주입은 미실행. |
| [난수](K-GAME-TECH-RNG.kr.md) | 공개 재구성 코드의 점화식·상위 비트 반환 확인. 버전별 패치 이력은 미확인. |
| [지형·동굴·대수층](K-GAME-TECH-NOISE.kr.md) | 버전이 명시된 공식 설명의 역할 구분 확인. 청크 처리 절차는 종합안. |
| [헤어](K-GAME-TECH-HAIR.kr.md) | 공식 패스 구분·CEDEC 작업 흐름 개요 확인. 상용 게임 가닥 수는 미확인. |
| [신발·발 IK](K-GAME-TECH-IK.kr.md) | 신발 오프셋·무릎·골반·보행 적용안 보완. 특정 상용 게임의 뼈 단축 주장은 미확인. |
| [락온](K-GAME-TECH-LOCKON.kr.md) | 원작 개발진 인터뷰로 대상 피드백 근거 보완. 세계 최초 주장은 미확인. |
| [전투 보상](K-GAME-TECH-INCENTIVES.kr.md) | 제작자의 회복 창·회복 가능 체력 설명 확인. 정확한 프레임·DOOM 드롭 식은 미확인. |
| [반응형 연막](K-GAME-TECH-VOLUME.kr.md) | 날짜 있는 Valve 패치로 공간 상호작용 확인. 전체 해법·복제 코드는 확인 불가. |
| [컨트롤러 ACE](K-GAME-TECH-MEMORY.kr.md) | 하드웨어 재생 프로젝트의 구현 자료 확인. 정확한 취약점 유발 과정은 미재현. |

## 적용 조건과 한계

앞서 확인한 공개 쇼츠 72편 중 게임 관련 58편과 곡선·그래픽 관련 1편을 포함하고 일반 개발·AI 소식·개인 영상 13편은 제외했다. 이 수는 조사일 기준이며 채널의 미래 전체성을 보장하지 않는다. 제목은 출처 식별 정보다.

논문·공식 문서는 원리를, 개발자 원저 글·인터뷰는 자신의 구현·설계 관찰을 뒷받침한다. Reddit은 볼류메트릭 항목의 원저 구현 경험으로 한정하며 성능을 재현하지 않았다. 무작위성의 설계 의견은 반대 견해도 구분했다.

이번에는 닌텐도 원본 발표의 해당 슬라이드, 히트맨 원본 슬라이드, 에뮬레이터·재구성 코드의 실제 함수, 버전이 명시된 공식 자료를 확인했다. 공개하지 않은 상용 코드, 신발·헤어의 특정 수치, 세계 최초 주장, ROM·레지스터 타이밍, 패치 이력, 전투 보상식은 확인 범위를 넘는다. UE 문서는 조회 시 5.8로 표시된 이동 문서이므로 실제 프로젝트 버전을 재확인한다. GPU Gems의 하드웨어·성능 맥락은 과거 기준이다.

롤백은 상태 복원·재시뮬레이션을 요구한다. Perlin은 부드러운 보간, 듀얼 컨투어링은 Hermite 데이터를 사용한다. 화면 FPS와 시뮬레이션 틱은 다르며 인스턴싱은 알파 오버드로를 제거하지 않는다. 체크섬은 인증이 아니고 1비트 플래그 8개는 1바이트다. 입력·출력 무작위성이 선악 법칙은 아니며 평면 반사는 물리적 방 복제를 요구하지 않는다.

## 검증 범위

59개 영상의 대응 관계, 기술 43개의 필수 절·근거·번역 존재, 게임 목록의 엄격한 구조 검사를 확인한다. 검색 사례와 수식 검사는 따로 평가한다. 최초 문서 연구에서는 코드·렌더러·네트워크·저장 장애·플레이를 실행하지 않았다. 이후 세 기술의 실제 엔진 실험을 아래에 추가했다. 검색 적중과 지침 연결은 실제 게임에서 자동으로 적절한 결정을 내렸다는 증거가 아니다.

## 영상별 대응표

| ID | 출발 쇼츠 | 기술 항목 |
| --- | --- | --- |
| V01 | [게임 속 대도시에 사람이 없는 이유](https://www.youtube.com/shorts/iAn8FPI_Fbo) | [군중 AI·회피·거리별 연산](K-GAME-TECH-CROWD.kr.md) |
| V02 | [게임 프레임에 숨겨진 게임의 시간 계산법](https://www.youtube.com/shorts/Nx4pdJ2lDas) | [고정 시간 간격·점프 적분·서브픽셀](K-GAME-TECH-TIMESTEP.kr.md) |
| V03 | [그림자를 만드는 게임의 신기한 기법](https://www.youtube.com/shorts/BG70G1Y8Llw) | [섀도 맵·CSM·필터링 선택](K-GAME-TECH-SHADOW.kr.md) |
| V04 | [치트와 렉을 막는 게임 네트워크 처리](https://www.youtube.com/shorts/b-8DpsYLI7Y) | [서버 권한·클라이언트 예측·보정](K-GAME-TECH-AUTHORITY.kr.md); [결정론적 록스텝](K-GAME-TECH-LOCKSTEP.kr.md) |
| V05 | [노가다를 없애는 게임의 보상 설계법](https://www.youtube.com/shorts/eHn7TLjzVFU) | [반복 보상·공격 유도·리스크와 리워드](K-GAME-TECH-INCENTIVES.kr.md) |
| V06 | [빠른 속도를 만드는 게임의 카메라 연출](https://www.youtube.com/shorts/IQVeIrF3KfE) | [속도감·FOV·모션 블러](K-GAME-TECH-SPEED.kr.md) |
| V07 | [마인크래프트에서 자연 환경을 자동 생성하는 방법?](https://www.youtube.com/shorts/3W1tKXhbiEk) | [펄린 노이즈·프랙탈 지형](K-GAME-TECH-NOISE.kr.md) |
| V08 | [게임에서 하이힐을 보기 힘든 이유](https://www.youtube.com/shorts/UqMLCjSqwyA) | [발 IK·FABRIK·신체 비율 보정](K-GAME-TECH-IK.kr.md) |
| V09 | [게임에 좋은 랜덤과 나쁜 랜덤이 있다?](https://www.youtube.com/shorts/vdbjOLEMQSg) | [입력·출력 무작위성과 천장·셔플백](K-GAME-TECH-RANDOM-DESIGN.kr.md) |
| V10 | [게임 속 연막탄이 가짜 연출인 이유?](https://www.youtube.com/shorts/9JsRRFL8G0c) | [볼류메트릭 연기·구름과 게임 판정 분리](K-GAME-TECH-VOLUME.kr.md) |
| V11 | [게임의 월드맵은 왜 실제보다 크게 느껴질까?](https://www.youtube.com/shorts/Mo3JFBC_jzk) | [월드 규모·문 크기·랜드마크·경로](K-GAME-TECH-LEVEL.kr.md) |
| V12 | [게임 속 문이 현실보다 거대한 이유는?](https://www.youtube.com/shorts/ncXQqHiFjHQ) | [월드 규모·문 크기·랜드마크·경로](K-GAME-TECH-LEVEL.kr.md) |
| V13 | [게임사가 긴 머리 캐릭터를 싫어하는 이유?](https://www.youtube.com/shorts/ZiQo1jKDRvY) | [헤어 카드·스트랜드와 시뮬레이션](K-GAME-TECH-HAIR.kr.md) |
| V14 | [게이머를 속이는 게임 속 파괴 연출](https://www.youtube.com/shorts/QSqcR2sLkdo) | [사전 파쇄·런타임 파괴 선택](K-GAME-TECH-DESTRUCTION.kr.md) |
| V15 | [게임 창문 속 방이 전부 가짜인 이유](https://www.youtube.com/shorts/-gaC6ZtDqDc) | [접근 불가능한 실내의 인테리어 매핑](K-GAME-TECH-INTERIOR.kr.md) |
| V16 | [게이머의 눈을 속이는 게임 속 거울의 비밀](https://www.youtube.com/shorts/OCLRh6VDupM) | [평면 반사·환경맵·SSR 선택](K-GAME-TECH-REFLECTION.kr.md) |
| V17 | [겁쟁이를 참교육하는 게임의 전투 설계](https://www.youtube.com/shorts/IZ0zeYEfqjY) | [반복 보상·공격 유도·리스크와 리워드](K-GAME-TECH-INCENTIVES.kr.md) |
| V18 | [게임 시야각에 쓰이는 신기한 수학](https://www.youtube.com/shorts/tfShkMZ49NU) | [내적·시야각·레이캐스팅](K-GAME-TECH-TRACE.kr.md) |
| V19 | [게임 속 잔디를 만드는 궁극의 최적화 기법](https://www.youtube.com/shorts/BtBXRm1noIg) | [잔디·식생의 LOD와 렌더링 예산](K-GAME-TECH-FOLIAGE.kr.md) |
| V20 | [게임은 저장을 어떻게 할까?](https://www.youtube.com/shorts/0fap5_6orlw) | [저장·백업·비트 플래그·패스워드](K-GAME-TECH-SAVE.kr.md) |
| V21 | [게임 세계를 건축하는 놀라운 기술](https://www.youtube.com/shorts/OS3OjZ607So) | [복셀·듀얼 컨투어링·청크](K-GAME-TECH-VOXEL.kr.md) |
| V22 | [게임 소리를 만드는 신기한 물리 현상들](https://www.youtube.com/shorts/1q9srGjkpD0) | [거리 음향·차폐·도플러·리버브](K-GAME-TECH-SOUND.kr.md) |
| V23 | [게임의 의도가 담겨진 카메라의 위치 연출법](https://www.youtube.com/shorts/xNp8De8CEoI) | [데드존·룩어헤드·카메라 감쇠](K-GAME-TECH-CAMERA.kr.md) |
| V24 | [플레이어의 행동을 조종하는 게임 속 맵 설계](https://www.youtube.com/shorts/tQDBuXB6Juo) | [월드 규모·문 크기·랜드마크·경로](K-GAME-TECH-LEVEL.kr.md) |
| V25 | [게임 음악에 사용되는 신기한 전환 기법](https://www.youtube.com/shorts/WkvlFYUlvns) | [어댑티브 뮤직·스템·전환 구간](K-GAME-TECH-MUSIC.kr.md) |
| V26 | [게임 그래픽을 실감나게 하는 마법](https://www.youtube.com/shorts/i6Mu34lCSb0) | [노멀 매핑으로 조명 디테일 추가](K-GAME-TECH-NORMAL.kr.md) |
| V27 | [게임 하늘을 만드는 신기한 수학 기법](https://www.youtube.com/shorts/UxTa_8XlJfo) | [볼류메트릭 연기·구름과 게임 판정 분리](K-GAME-TECH-VOLUME.kr.md) |
| V28 | [시간을 되감는 FPS 게임의 사격 판정](https://www.youtube.com/shorts/o7waSG4jROw) | [서버 되감기·지연 보상](K-GAME-TECH-LAGCOMP.kr.md) |
| V29 | [슈퍼 마리오의 조작감은 왜 혁신적일까?](https://www.youtube.com/shorts/dNsyscOrNMY) | [코요테 타임·버퍼·코너 보정](K-GAME-TECH-CONTROLLER.kr.md) |
| V30 | [플랫폼 게임 맵 모서리에 있는 점프 위치 보정](https://www.youtube.com/shorts/hjVLIojpwVk) | [코요테 타임·버퍼·코너 보정](K-GAME-TECH-CONTROLLER.kr.md) |
| V31 | [느린 네트워크 속도를 게임이 보정하는 비법](https://www.youtube.com/shorts/kap1_O66XCY) | [롤백·입력 지연 넷코드](K-GAME-TECH-ROLLBACK.kr.md) |
| V32 | [게임 속 물 표현을 하는 수식을 만드는 방법](https://www.youtube.com/shorts/RFDIq0ZdJ3s) | [사인파·거스너파 수면](K-GAME-TECH-WATER.kr.md) |
| V33 | [게임 상대를 결정하는 매칭 시스템의 원리](https://www.youtube.com/shorts/uMCwH38GpuY) | [Elo·TrueSkill·매치메이킹](K-GAME-TECH-MATCH.kr.md) |
| V34 | [게임의 쾌감을 주는 위험 대 보상 설계](https://www.youtube.com/shorts/SauTVeoo6K0) | [반복 보상·공격 유도·리스크와 리워드](K-GAME-TECH-INCENTIVES.kr.md) |
| V35 | [게임 속 픽셀 아트에 숨겨져 있는 규칙들](https://www.youtube.com/shorts/Ce5YdbY4upM) | [픽셀 아트와 팔레트 저장](K-GAME-TECH-PIXEL.kr.md) |
| V36 | [게임 속 길찾기에 숨겨져 있는 수학 이론](https://www.youtube.com/shorts/qMGONAZGIqE) | [A*·다익스트라·플로 필드 길찾기](K-GAME-TECH-PATH.kr.md) |
| V37 | [게임 캐릭터가 계단을 오르는 기법](https://www.youtube.com/shorts/0rjhNtdmgVI) | [발 IK·FABRIK·신체 비율 보정](K-GAME-TECH-IK.kr.md) |
| V38 | [선을 쏘아 알아내는 게임의 시야 계산법](https://www.youtube.com/shorts/PRwkpITfW-s) | [내적·시야각·레이캐스팅](K-GAME-TECH-TRACE.kr.md) |
| V39 | [눈에서 총알이 튀어나오는 FPS 게임의 사격 판정](https://www.youtube.com/shorts/kucqGt8Q2a8) | [히트스캔·총구 차폐 판정](K-GAME-TECH-HITSCAN.kr.md) |
| V40 | [랜덤 생성 던전을 게임이 만드는 방법](https://www.youtube.com/shorts/_0qjqwigjLc) | [던전 생성과 통과 가능성 보장](K-GAME-TECH-DUNGEON.kr.md) |
| V41 | [플레이어에 접대하는 게임의 난이도 조절](https://www.youtube.com/shorts/kkhqAHTcu5I) | [동적 난이도·러버밴딩·페이싱](K-GAME-TECH-DDA.kr.md) |
| V42 | [게이머에게 관대한 게임의 피격 판정](https://www.youtube.com/shorts/hUpx8lUaiDU) | [공격·피격 판정과 히트스톱](K-GAME-TECH-HITBOX.kr.md) |
| V43 | [게이머를 속이는 게임의 3D 연출 방법](https://www.youtube.com/shorts/DXsKd52lomQ) | [빌보드·이미지 대체물의 방향 설정](K-GAME-TECH-BILLBOARD.kr.md) |
| V44 | [불운을 관리하는 게임의 확률 조작법](https://www.youtube.com/shorts/eyrRduWl-qo) | [입력·출력 무작위성과 천장·셔플백](K-GAME-TECH-RANDOM-DESIGN.kr.md) |
| V45 | [게임 이펙트를 만드는 신기한 색상 계산](https://www.youtube.com/shorts/Of9pFtvVBJQ) | [알파·가산·곱하기 블렌딩](K-GAME-TECH-BLEND.kr.md) |
| V46 | [게임 점프에 숨겨진 판정 타이밍 조절](https://www.youtube.com/shorts/0gkwRtolL4Y) | [코요테 타임·버퍼·코너 보정](K-GAME-TECH-CONTROLLER.kr.md) |
| V47 | [게임 애니메이션을 만드는 수학](https://www.youtube.com/shorts/TomzUe30Ltg) | [이징·스무드스텝·베지에 곡선](K-GAME-TECH-EASING.kr.md) |
| V48 | [게임 카메라에 숨겨진 수학 기법](https://www.youtube.com/shorts/caPi9d2gP7I) | [데드존·룩어헤드·카메라 감쇠](K-GAME-TECH-CAMERA.kr.md) |
| V49 | [물리 역학을 무시하는 게임 점프의 수식](https://www.youtube.com/shorts/dluLPk0zjIs) | [고정 시간 간격·점프 적분·서브픽셀](K-GAME-TECH-TIMESTEP.kr.md) |
| V50 | [게임에서 지형을 만들 때 쓰는 특수한 수학 기법](https://www.youtube.com/shorts/kY9TYQYxCZM) | [펄린 노이즈·프랙탈 지형](K-GAME-TECH-NOISE.kr.md) |
| V51 | [젤다의 전설 야숨을 디자인한 특별한 게임 엔진](https://www.youtube.com/shorts/1yxDf1WUIBk) | [화학 엔진·시스템 상호작용](K-GAME-TECH-SYSTEMIC.kr.md) |
| V52 | [게임 컨트롤러로 게임을 즉석에서 재구축하는 방법](https://www.youtube.com/shorts/uj6016N96JY) | [메모리 오류·임의 코드 실행](K-GAME-TECH-MEMORY.kr.md) |
| V53 | [세계 최초로 에임핵을 도입한 게임](https://www.youtube.com/shorts/OjbUm_hnYFU) | [락온·타겟 전환·카메라](K-GAME-TECH-LOCKON.kr.md) |
| V54 | [비밀번호가 세이브 파일이 되었던 고전 게임](https://www.youtube.com/shorts/ave58m6vuDw) | [저장·백업·비트 플래그·패스워드](K-GAME-TECH-SAVE.kr.md) |
| V55 | [고전 게임에서 확률 조작하는 방법](https://www.youtube.com/shorts/djGVMe4imWw) | [의사난수·시드·스트림](K-GAME-TECH-RNG.kr.md) |
| V56 | [전설로 남은 게임의 랜덤맵 생성](https://www.youtube.com/shorts/vVVyFUzs-HM) | [던전 생성과 통과 가능성 보장](K-GAME-TECH-DUNGEON.kr.md) |
| V57 | [3D처럼 눈속임하는 고전 게임의 비밀](https://www.youtube.com/shorts/R06WXFSWYvo) | [아핀 변환·주사선별 의사 원근](K-GAME-TECH-RETRO.kr.md) |
| V58 | [마른 이미지 용량 쥐어짜기](https://www.youtube.com/shorts/p0mH7UAwtXQ) | [픽셀 아트와 팔레트 저장](K-GAME-TECH-PIXEL.kr.md) |
| V59 | [벡터파일에서 곡선을 어떻게 저장할까?](https://www.youtube.com/shorts/0MySBqE02fU) | [이징·스무드스텝·베지에 곡선](K-GAME-TECH-EASING.kr.md) |

## 출처

- [Microsoft — Cascaded Shadow Maps](https://learn.microsoft.com/en-us/windows/win32/dxtecharts/cascaded-shadow-maps)
- [Bunnell & Pellacini — Shadow Map Antialiasing](https://developer.nvidia.com/gpugems/gpugems/part-ii-lighting-and-shadows/chapter-11-shadow-map-antialiasing)
- [Epic — Planar Reflections](https://dev.epicgames.com/documentation/en-us/unreal-engine/planar-reflections-in-unreal-engine)
- [Joost van Dongen — Interior Mapping](https://www.proun-game.com/Oogst3D/CODING/InteriorMapping/InteriorMapping.pdf)
- [Kurt Pelzer — Rendering Countless Blades of Waving Grass](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-7-rendering-countless-blades-waving-grass)
- [Tiago Sousa — Vegetation Procedural Animation and Shading in Crysis](https://developer.nvidia.com/gpugems/gpugems3/part-iii-rendering/chapter-16-vegetation-procedural-animation-and-shading-crysis)
- [Godot — Standard Material 3D](https://docs.godotengine.org/en/stable/tutorials/3d/standard_material_3d.html)
- [Epic — Hair Rendering and Simulation](https://dev.epicgames.com/documentation/en-us/unreal-engine/hair-rendering-and-simulation-in-unreal-engine)
- [Epic — Geometry Collections User Guide](https://dev.epicgames.com/documentation/en-us/unreal-engine/geometry-collections-user-guide)
- [Epic — Volumetric Fog](https://dev.epicgames.com/documentation/en-us/unreal-engine/volumetric-fog-in-unreal-engine)
- [Shaker, Togelius & Nelson — Fractals, Noise and Agents](https://www.pcgbook.com/chapter04.pdf)
- [u/smilefr — Optimized volumetric clouds](https://www.reddit.com/r/Unity3D/comments/1u8g138/i_finally_have_optimzied_volumetric_clouds/)
- [Epic — Material Blend Modes](https://dev.epicgames.com/documentation/en-us/unreal-engine/material-blend-modes-in-unreal-engine)
- [Derek Yu — Pixel Art Tutorial: Basics](https://www.derekyu.com/makegames/pixelart.html)
- [W3C — PNG Specification, Third Edition](https://www.w3.org/TR/png/)
- [Mark Finch — Effective Water Simulation from Physical Models](https://developer.nvidia.com/gpugems/gpugems/part-i-natural-effects/chapter-1-effective-water-simulation-physical-models)
- [Ken Perlin — Improving Noise](https://mrl.cs.nyu.edu/~perlin/paper445.pdf)
- [Ju et al. — Dual Contouring of Hermite Data](https://www.cs.rice.edu/~jwarren/papers/dualcontour.pdf)
- [Shaker et al. — Constructive Generation Methods for Dungeons and Levels](https://www.pcgbook.com/chapter03.pdf)
- [Amit Patel — Introduction to A*](https://www.redblobgames.com/pathfinding/a-star/introduction.html)
- [Amit Patel — Flow Field Pathfinding for Tower Defense](https://www.redblobgames.com/pathfinding/tower-defense/)
- [Epic — Mass Avoidance Overview](https://dev.epicgames.com/documentation/unreal-engine/mass-avoidance-overview-in-unreal-engine?lang=en-US)
- [Kasper Fauerby — Crowds in Hitman: Absolution](https://www.gdcvault.com/play/1015315/Crowds-in-Hitman)
- [Maddy Thorson — Celeste & Forgiveness](https://maddymakesgames.com/articles/celeste_and_forgiveness/index.html)
- [Maddy Thorson — Celeste & TowerFall Physics](https://www.mattmakesgames.com/articles/celeste_and_towerfall_physics/index.html)
- [Glenn Fiedler — Fix Your Timestep!](https://gafferongames.com/post/fix_your_timestep/)
- [Glenn Fiedler — Integration Basics](https://gafferongames.com/post/integration_basics/)
- [Epic — Two Bone IK](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-two-bone-ik-in-unreal-engine)
- [Epic — FABRIK AnimBP Node](https://dev.epicgames.com/documentation/unreal-engine/fabrik-animation-blueprint-in-unreal-engine?lang=en-US)
- [Epic — EQS Node Reference: Tests](https://dev.epicgames.com/documentation/unreal-engine/eqs-node-reference-tests-in-unreal-engine?lang=en-US)
- [Epic — Mover Grappling Hook Movement Mode](https://dev.epicgames.com/documentation/unreal-engine/mover-03-grappling-hook-movement-mode?lang=en-US)
- [Riot — Peeking into VALORANT's Netcode](https://www.riotgames.com/en/news/peeking-valorants-netcode)
- [Itay Keren — Scroll Back](https://www.gamedeveloper.com/design/scroll-back-the-theory-and-practice-of-cameras-in-side-scrollers)
- [Ryan Juckett — Damped Springs](https://www.ryanjuckett.com/damped-springs/)
- [Gilberto Rosado — Motion Blur as a Post-Processing Effect](https://developer.nvidia.com/gpugems/gpugems3/part-iv-image-effects/chapter-27-motion-blur-post-processing-effect)
- [W3C — CSS Easing Functions Level 1](https://www.w3.org/TR/css-easing-1/)
- [Glenn Fiedler — Deterministic Lockstep](https://gafferongames.com/post/deterministic_lockstep/)
- [GGPO — Rollback Networking SDK](https://www.ggpo.net/)
- [Microsoft Research — TrueSkill Ranking System](https://www.microsoft.com/en-us/research/project/trueskill-ranking-system/)
- [Epic — Saving and Loading Your Game](https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine)
- [pret/pokered — save.asm](https://github.com/pret/pokered/blob/master/engine/menus/save.asm)
- [Melissa O'Neill — PCG Random Number Generators](https://www.pcg-random.org/pdf/hmc-cs-2014-0905.pdf)
- [Ian Schreiber — Probability and Randomness](https://gamebalanceconcepts.wordpress.com/2010/07/28/level-4-probability-and-randomness/)
- [Keith Burgun — Randomness and Game Design](https://www.gamedeveloper.com/design/randomness-and-game-design)
- [A Defense of Randomness in Competitive Games](https://www.gamedeveloper.com/design/a-defense-of-randomness-in-competitive-games)
- [Mike Booth — The AI Systems of Left 4 Dead](https://cdn.fastly.steamstatic.com/apps/valve/2009/ai_systems_of_l4d_mike_booth.pdf)
- [Epic — Sound Attenuation](https://dev.epicgames.com/documentation/en-us/unreal-engine/sound-attenuation-in-unreal-engine)
- [Kent Carter / Guy Jones — Composer interview on adaptive music](https://www.gamedeveloper.com/audio/composer-guy-jones-talks-adaptive-music-for-games)
- [Nintendo — Breath of the Wild: Breaking Conventions](https://www.youtube.com/watch?v=niIVdlavc7I)
- [Godot — Matrices and transforms](https://docs.godotengine.org/en/latest/tutorials/math/matrices_and_transforms.html)
- [DerKoun — bsnes-hd README](https://github.com/DerKoun/bsnes-hd/blob/master/README.md)
- [MITRE — CWE-787: Out-of-bounds Write](https://cwe.mitre.org/data/definitions/787.html)
- [Nintendo/GDC — original technical presentation](https://www.youtube.com/watch?v=QyMsF31NdNc&t=2423s)
- [Kasper Fauerby — Crowds in Hitman: Absolution slides](https://media.gdcvault.com/gdc2012/slides/Programming%20Track/Fauerby_Kasper_CrowdsInHitman.pdf)
- [bsnes — renderMode7 source](https://github.com/bsnes-emu/bsnes/blob/master/bsnes/sfc/ppu-fast/mode7.cpp)
- [pret/pokeemerald — save.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/save.c)
- [kingshriek — Simon's Quest Password System FAQ](https://gamefaqs.gamespot.com/nes/587179-castlevania-ii-simons-quest/faqs/38582)
- [pret/pokeemerald — random.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/random.c)
- [pret/pokeemerald — random.h](https://github.com/pret/pokeemerald/blob/master/include/random.h)
- [Mojang — Java 1.18 experimental world generation](https://www.minecraft.net/en-us/article/new-world-generation-java-available-testing)
- [Mojang — Bedrock 1.18.0 release notes](https://feedback.minecraft.net/hc/en-us/articles/4414284658701-Minecraft-Caves-Cliffs-Part-II-1-18-0-Bedrock)
- [Epic — Groom Scalability and Performance](https://dev.epicgames.com/documentation/unreal-engine/groom-scalability-and-performance-with-unreal-engine)
- [Capcom speakers — PRAGMATA hair and facial development](https://cedec.cesa.or.jp/2026/timetable/detail/s69f305ca68328/)
- [Nintendo — Where the Name Navi Came From](https://iwataasks.nintendo.com/interviews/3ds/zelda-ocarina-of-time/1/3/)
- [Masaaki Yamagiwa — Bloodborne combat details](https://blog.playstation.com/2014/08/13/bloodborne-on-ps4-new-combat-details/)
- [id Software/GDC — Embracing Push Forward Combat](https://www.youtube.com/watch?v=2KQNpQD8Ayo)
- [Valve — Counter-Strike 2 June 2023 update notes](https://store.steampowered.com/news/posts/?appids=730&enddate=1689630041&feed=steam_announce%2F1000)
- [TAStm32 authors — Test suite instructions](https://github.com/Ownasaurus/TAStm32/wiki/Test-suite-instructions)

각 기술 항목이 실제 절·함수·타임스탬프와 접근 한계를 보존한다. 세션 개요만 확인한 출처를 전체 발표 확인으로 취급하지 않는다. 접근 불가·불충분 자료는 interiormapping.com, 일부 Audiokinetic/FMOD 문서, SNESdev 하드웨어 위키, FABRIK 원논문 등이며 다른 공식 자료로 보완하거나 공백으로 남겼다. 잘못된 PDF 후보는 제외했다.

## 가상 평가와 후속 엔진 실험

[6개 상황 평가](../../skills/vegabond-knowledge/tests/game-application/evaluation-results.kr.md)와 [추가 평가](../../skills/vegabond-knowledge/tests/game-application/extended-evaluation-results.kr.md)는 독립 가상 판단·검색 누락·보완·새 재검사를 구별한다. 두 평가에서 43개 기술의 가상 적용 검토를 마쳤으나 실제 실행을 뜻하지 않는다. 시간 간격·잔디·롤백·신발 IK·저장 복구·대수층·화학·군중의 영문 검색 8개에서도 의도 항목이 상위 3개에 들었고 7개는 1위였다. 지침 4개의 연결과 수식 검사는 별도다. 미지의 요청에 대한 자율 판단 보장은 아니다.

[Technique Lab 실제 결과](../../prototypes/TechniqueLab/RESULTS.kr.md)는 조회한 세 결정을 구현·최종 PlayMode·Windows Mono 독립 실행 3회로 연결한다. 매 실행 검사 27개와 실제 시간 응답 3개를 통과했다. CAMERA는 정지 목표 감쇠, HITSCAN은 정적 엄폐/내부 원점과 네이티브 물리, PATH는 가중·방향·0비용 그래프 및 같은 출구 거리 처리량을 확인했다. 코드·원본 표본·빌드 식별·수정·재현 명령은 실험에 보관했다.

세 항목 전체의 완전 검증이 아닌 제한된 원리의 엔진 근거다. 첫 단계에는40개 기술이 로컬 미검증이었다. 후속 실험으로 현재 누적4개 제한 근거·39개 미검증이다. 네트워크·저장 장애·GPU 프로파일·상용 통합·플레이어 연구는 수행하지 않았다. 출처 확인·가상 판단·실제 실행을 구별하고 각 조건을 읽어 적용한다.

## 동적 확장과 누적 범위

[DynamicLab](../../prototypes/TechniqueLab/DYNAMIC-RESULTS.kr.md)은 초기화 없는 문/상자·동일 반경 합류를 검증했다. 폐쇄는 기존 개체 배출을 기다린다. 최종 프레임 통과와 이전 미달·GPU 누락을 함께 기록했다. 누적 CAMERA/HITSCAN/PATH/CROWD4개는 제한된 원리의 근거이며39개는 로컬 미검증이다.

## 양방향·서로 다른 반경 확장 — 2026-11-08

[TrafficLab](../../prototypes/TechniqueLab/TRAFFIC-RESULTS.kr.md)은 반경 .20/.35/.60별 양쪽 출구 장·작성한 상하좌우 차선·방향 임대 제어를 추가했다. 거친 네 노드 비용은 통로 선호도이며 실제 최단 거리가 아니다. 여유 .04로 큰 개체의 좁은 통로를 거부하고 반경 합으로 쓸린 이동·독립 감사를 수행했다. 이전 DynamicLab의 한 목표/동일 반경 제한은 그 과거 장면에 해당한다.

PlayMode·release3회 각각 회귀21개·기대11개(안전9개·정책을 끈 비교2개)를 통과했다. 혼합64/128/256개 양쪽 모두 도착했고256개는114.7500시뮬레이션 초였다. 최소 안전 표면 간격0.0476715단위, 벽/쌍 침투·순간이동·임대 오류·전역 교착 없음. 역순·90틱 지연·넓은 동시 교행·진입 중단/배출/재개·도착 선분을 검사했다. 진입 제어만 끄면 충돌 없이 교착, 방어도 끄면 겹침이 생겼다. 충돌 안전과 진전은 다른 조건이다.

혼합256개 전체 프레임 p95 8.08–8.32ms, 틱 포함 제어/동기화 p95 0.404–0.444ms. 18개 실행/조합 구간 모두16.67ms p95목표를 충족했다. 실제 창·활성/표시 수·전체 분포·드문 초과·GPU 누락을 보존했다. 부하 미통제로 반경 모드의 인과 성능 차이는 판단하지 않는다. 임대 중단은 물리적 문 폐쇄가 아니며 이전 동적 장애물 실험과 별개다.

대기 공간·차선·한 이동 권한·고정 원판·정지/교대를 허용할 때 조건부 채택한다. 방향별 FIFO이며 방향 사이 전역 FIFO는 아니다. 무한 유입 공정성·임의 내비메시·곡선·가속·밀기·실시간 반경 변경·분산 권한은 미검증이다. 공간 해시는 반경≤.60·속도3·dt≤1/30에 의존한다. 원저 [통로 대칭](https://mapf.info/index.php/Main.SKoen20k)·[C-space](https://lavalle.pl/planning/node161.html)·[고정 경로 협조](https://lavalle.pl/planning/node325.html)는2026-11-08확인한 설계 참고이며 CBS/완전 플래너를 구현한 것은 아니다. [최종 검사](../../prototypes/TechniqueLab/Results/Traffic/editor-final.json)·[전체 분포](../../prototypes/TechniqueLab/Results/Traffic/summary.json).

## 무차선·지속 유입·개별 진전 확장 — 2026-11-08

[StreamLab 결과](../../prototypes/TechniqueLab/STREAM-RESULTS.kr.md)는 무방향 상하좌우 지형에서 각 요청의 경로를 계산하고 반경별 쓸린 시간 예약·불변 완전 경로·외부 FIFO 진입을 결합했다. 차선 태그나 미리 정한 경유점은 없다. 생성 전 대기도 ID별 응답에 포함한다. 일반7개는 무충돌 배출·240초 응답을 통과했지만 과부하480개 중61ID는 이를 초과했고 최대280.0초였다. 최신 우선은 다른538개 도착 중 요청0을310초 미생성 상태로 남겼다. 전체 처리량으로 특정 개체의 기아를 판단하면 안 된다.

FIFO 머리가 막히면 젊은 진입을 막고 기존 유한 경로가 빠진 뒤 정적 경로를 찾는 조건부 논증이다. 유한 실행이 무한 시간의 증명은 아니며 과부하에서는 일정한 지연 상한을 주지 않는다. 생성 통제·정적 지형·고정 반경·계획대로 이동·도착 후 제거가 필요하다. 기존 임의 개체·점유 입구 강제 생성·갑작스런 정지·동적 벽/반경·가속·분산 권한은 범위 밖이다.

병목 초당8요청 전체 프레임 p953.52–6.10ms, 탐색 다음 전체 프레임 p9520.23–20.52ms. 실제 활성/표시 인원·대기열·온라인 탐색/생성/소멸·프레임 초과·GPU 누락을 기록했다. 목표 수요와 고정 개체 수를 혼동하지 않는다. [PlayMode23검사/10기대](../../prototypes/TechniqueLab/Results/Stream/editor-final.json)·[분포](../../prototypes/TechniqueLab/Results/Stream/summary.json). 원저 [RHCR](https://arxiv.org/abs/2005.07371)·[PIBT](https://arxiv.org/abs/1901.11282)·[온라인 작업](https://arxiv.org/abs/1705.10868)은2026-11-08초록만 확인했으며 그 알고리즘/정리를 구현한 것은 아니다.

## 언리얼 동적 군중 후속 — 2026-11-09

[실제 결과·영상](../../prototypes/UnrealTechniqueLab/DYNAMIC-RESULTS.kr.md)에서 경로장·군중의 동일 반경 예약·점유 문 지연 닫기를 실제 PIE·패키지로 확인했다. 안전 완료5개와 충돌 검출 대조군1개가 기대 조건을 통과했다.44,740개 전체 프레임을 보존했다.18개 구간 p95는16.67ms 이내지만 장애물 변경 작업과 겹친 초과54회가 있어 엄격한 무초과60Hz 채택은 추가 검증이 필요하다. 혼합 반경 양방향·무차선 지속 유입은 언리얼 후속 단계다. 제한된 엔진 근거4개 항목·미검증39개라는 범위는 같다.

## 언리얼 양방향 교행 후속 — 2026-11-09

[혼합 반경 실제 교행](../../prototypes/UnrealTechniqueLab/TRAFFIC-RESULTS.kr.md)에 모델26개·실제 PIE/패키지11개 기대 조건, 안전한 양쪽 완료9개·충돌 없는 교착/충돌 대조군을 추가했다. 패키지3개·전체54200프레임과 사전 차선의 조건부 채택을 기록했다. 무차선 지속 유입은 언리얼 후속 단계다. 제한된 엔진 근거4개 항목·미검증39개라는 범위는 같다. 동적 토폴로지 회귀와 정적 교행의 입장 조정 비용은 분리한다.

## 언리얼 무차선 지속 유입 — 2026-11-09

[UE5.8.3 실제 결과](../../prototypes/UnrealTechniqueLab/STREAM-RESULTS.kr.md): 모델25개·실제 PIE10개·전체 쿠킹 패키지10개 기대 조건과 ID/동작 기록이 일치했다. FIFO8상황의 유효3120요청 완료·도달 불가1거부, 일반7상황240초 기준 통과다. 과부하 통로는 충돌 없이 배출됐지만61ID가240초 초과·최대280초라 **지연 실패**다. LIFO는310초에 나중538ID가 도착해도 ID0가 미입장 상태다. 유한 대기 관측이며 무한 시간 증명이 아니다. 예약 해제는 실제 충돌을 검출했다. 첫/중간/도착을5분율로 ID별 대조하고 캡슐·시각 메시의 실제 위치/크기·벽 쿼리 오염도 검출한다.

정적32×24 무방향 직교 격자·150cm간격·사전 포털·차선 없음·고정20/35/60cm·여유4cm·속도300cm/s·0.5초 동작·96동작 이내 완전 불변 경로·단일 권한·FIFO 외부 입장·출구 소멸에 조건부 사용한다. 대기 나이는 생성 전 요청부터 센다. 유한한 이전 ID와 완전 경로 서비스의 조건부 논리만 가능하며 임의 NavMesh/물리 밀기/가속/동적 형상·지형/예정 외 간섭·영구 유입의 일정 지연/메모리 상한은 검증하지 않았다. 과부하는 유입·경로 용량과 대기열 제한/거부 정책으로 다루고 오래된 ID를 처리량과 함께 감시한다. 이전 동적 갱신 지연도 남는다. 과거의 언리얼 지속 유입 미검증 표기는 이 제한된 정적 격자 범위에서만 갱신한다.

순차 패키지3개·전체19559프레임, 전체 wall p9510.013–11.108ms·측정 초과101회·시작 간격 초과104회·계획 현재 최대24.671ms·다음 간격 최대24.746ms다. p95가 좋아도 엄격한60Hz 무초과는 실패다. 초과 중 계획 포함14회·계획 없는87회라 모두 탐색 탓으로 단정하지 않는다. End시각 기록 뒤 관측 행 생성 비용은 시작 간격에 포함한다. 실제 출생·온라인 예약/탐색·입장·도착과 변하는 활성/대기 수를 포함한다. 초기 콜백 전 사전 채움·최종 저장, 메모리/할당률·새 목표 캐시·프레임 정렬 GPU 꼬리·계획 없는 지연 원인은 제외/미검증이다. GPU0은 결측, 잔상이 보이는 영상15배속·5분율 감사는 실시간 성능과 분리하고 픽셀 잔상을 실제 충돌 반경으로 사용하지 않는다.

PATH에서 격자/반경/경로 길이, CROWD에서 입장·충돌/교착/개별 대기, PERFORMANCE에서 전체 프레임과 계획 발생 꼬리를 찾는다. 검토에서 드러난 메시 실제 위치·요청 시각/가장 오래된 ID 대조 누락을 실패 재현 후 고쳤고96개 회귀를 통과했다.1e-9초 누적 시간과 프레임별 생명주기를 대조한다. 사용자의 독립 검토·승인과 AI 검증은 구분한다.

## 언리얼 과부하 정책 비교 — 2026-11-09

[실제 비교](../../prototypes/UnrealTechniqueLab/ADMISSION-RESULTS.kr.md)는 모든 정책에 초당8요청을 제공하고 FIFO 입장 무제한/초당1개·버스트2와 대기열 무제한/32/64의6조합을 비교했다.60초480요청·120초960요청을 각각 같은 ID/seed 안에서 실제 PIE12개·패키지12개로 대조했다. 새 요청만 명시적으로 거부하고 원래 ID·요청 시각·기존 수락 FIFO를 보존한다.

수락 요청의 완료 지연과 전체 제공 요청 기준240초 내 완료율·완료율·거부율·처리량을 함께 본다. 거부0초를 완료 지연에 섞지 않는다. 작은 대기열이 지연을 줄여도 통로 용량을 늘리는 것은 아니며, 모든 요청 처리 요구에는 거부 정책만으로 해결할 수 없다. 상류 제어를 도입하더라도 원래 수요의 대기 나이를 유지해야 한다. 대기열 상한은 활성 개체·장기 요청/감사 이력·전체 메모리 상한과 다르다.

패키지3개·전체22389프레임에서 wall16.667ms초과103회·시작 간격 초과97회를 보존했다. 실제 생성/거부/계획/입장/완료·변하는 개체 수를 포함하며 준비/정책 전환·계획 현재/다음 꼬리·관측 스냅샷 비용을 구분한다. 최초 콜백 전 사전 채움·최종 저장·메모리/할당률·정렬 GPU 꼬리는 미측정이다. 이번 진단 카메라는 일관되게 모션 블러를 껐고 이전 다른 화면 설정과 속도 향상을 비교하지 않는다.

정적 직교 격자·고정20/35/60cm·완전 불변 시간 예약·외부 FIFO·예정 이동·출구 소멸 조건이다. 임의 NavMesh/물리/동적 지형/일반 공정성이나 최적 입장률은 검증하지 않았다. 모델18·네이티브 오염/정책 연결8그룹·회귀127, 독립 토큰/대기열/원래 ID/거부/도착 검사가 근거다. 실제15배속 영상은 성능과 분리한다. PATH/CROWD/PERFORMANCE에서 요구 조건에 맞게 조회하며 기존4개 기술 근거·39개 미검증 범위도 유지한다.

## Insights 병목 개선의 적용 조건 — 2026-11-10

[실제 추적·전후3회 비교](../../prototypes/UnrealTechniqueLab/HITCH-RESULTS.kr.md)에서 같은 실행 파일·1280×720·초당8요청·6정책을 유지했다. 기준 wall/간격 초과88/80, 개선29/20이며 계획/Present 꼬리와 준비·관측 비용을 남긴다. 프레임 이름을 정확히 대조하고 중첩 포괄 시간을 합산하지 않는다. CPU 대기로 드라이버·화면·전력 원인을 단정하지 않는다.

가림 없는 평면 진단 뷰포트에만 쿼리를 끈다. 가림 있는3D 전체 설정으로 일반화하지 않는다. 제곱거리 경계의 원래 판정·시작점 단일 색인·유일 통로의 완료 불가능 하한은150cm 직교 한 칸·반경20~60cm·여유4cm·정적96동작 경로 조건이다. 다른 구멍·큰/가변 반경·대각 이동·동적 지형은 재검증한다. 우선순위·동점·예약 안전 판정은 유지한다.

패키지12상황·실제 PIE2상황, 전후3쌍의 공통 시뮬레이션 경계에서 원래 ID/경로/수락/거부/토큰/완료·안전 기록을 대조했다. 새 모델18·기존 회귀·Python148검사를 포함한다. 해상도/프로파일 오표시 실패 검사도 추가했다. 서비스 용량·응답/거부율은 그대로이며 무한 공정성·전체 이력 메모리·기존 동적 재계산·일반60Hz는 보장하지 않는다. 실제15배속 영상은 성능 입력에서 제외한다.

## 계획기 힙 비용 개선 — 2026-11-10

[실제 비교](../../prototypes/UnrealTechniqueLab/PLANNER-RESULTS.kr.md)는 같은 패키지·1280×720·초당8요청·6정책의 기준/개선3쌍을 비교했다. 기준 wall/간격 초과27/19, 개선11/2이며 상세 시계·녹화는 성능에서 제외한다. 초기 진단에서 힙55~56%, 충돌17~18%였고 정수 키로 반복 비교 계산을 줄였다.74496상태17비트·거리0~767의10비트 범위에서 원래 동점/부모/경로/입장 순서를 유지한다. 더 큰/가중/실수/음수 우선순위는 새 증명이 필요하다. 추가 힙595968바이트는 명시된 메모리 교환이다.

실제 패키지12·PIE2·전후3쌍의 원래 ID/경로/입장·완료·거부/토큰/5표본 안전과 같은 탐색 확장·충돌·힙 호출 수를 확인했다. 계획 프레임의 wall최대가 스냅샷일 수 있어 실제 계획최대 창을 따로 남긴다. 추적 실행기의 실제 해시도 고정한다. 새 모델11·기존 회귀·Python161을 포함한다. 처리량·거부율·과부하 응답 실패·입구 공정성·이력 메모리 한계는 그대로이며 Present/동적 재계산은 별도다. PATH/CROWD/PERFORMANCE/PIE의 조건을 조회하고 무한 공정성·일반60Hz로 확대하지 않는다.

## 소유형 스냅샷·저장·메모리 — 2026-11-11

[실제 검증](../../prototypes/UnrealTechniqueLab/SNAPSHOT-RESULTS.kr.md)은 같은 패키지·1280×720·초당8요청·6정책3쌍에서 원래 기록 값/키·배열 순서/누락 여부를 대조했다. 기준 wall/간격 초과10/1, 개선0/0이다. 최초 준비·전환·경계·저장 구성/변환/쓰기/로컬 정리와 프로세스 종료까지 모두 남긴다. 경계만 낮추고 비용을 밖으로 옮겨 개선이라고 부르지 않는다. 최종 saveTail 전체 추적도 포함한다.

원래 시점에 중첩 배열/문자열/경로를 소유하는 기록을 복사하고 표준 JSON작성기로 직접 출력한다. 바이트 동등·문자/소수값·빈 배열·나쁜 커버리지·원본 변경/파괴를 모델12와 실제 패키지12/PIE2·3쌍·Python177로 확인했다. 기록 DOM값0은 전체 할당0이 아니고 원시 바이트는 순 메모리 증가와 다르다. Windows개인 커밋/작업 집합/수명 최고치·경계 증가·저장시점을 함께 보며 정확한 전체 할당률은 미측정이다.

이 스냅샷은 데이터를 소유하지만 현재 전체 저장 함수는 라이브 월드/메타데이터/프레임 DOM도 읽어 게임 스레드에서 실행한다. 그대로 작업자 스레드로 옮기지 않는다. 비동기는 모든 입력 소유권·제한된 대기 메모리·순서·오류·배압 검증이 별도로 필요하다. 동기 저장/Present·동적 재계산·전체 이력 메모리·무한 공정성 한계는 남으며 이동·처리량·거부 결과는 그대로다.

## 전체 입력 소유형 비동기 저장 — 2026-11-11

[실제 결과](../../prototypes/UnrealTechniqueLab/ASYNC-SAVE-RESULTS.kr.md)는 같은 소유형 입력·표준 직렬화기를 사용하는 동기/비동기3쌍을 비교한다. 작업자는 메타데이터·현재/과거 경로·원장·커버리지·형식화된 프레임까지 독립적으로 소유하며 Actor/월드/공유 JSON을 읽지 않는다. 이전 단계의 동기 저장 설명은 역사적 결과이고 새 경로만 별도 검증했다. 게임 스레드 제출·완료 처리, 작업자 변환/쓰기/해제, 전체 완료 시간, 추가 프레임·종료 대기, 대기열·OS메모리 최고치를 구분한다. 비용을 측정 창 밖으로 옮긴 것만으로 전체 개선이라 하지 않는다.

모델14는 원본 파괴 뒤 전체 바이트 일치·실제39필드 프레임·큐 포화/재제출/FIFO/오류/용량/종료를 검사한다. 실제3쌍·패키지12·PIE2의 원래 값·타입·키/배열 순서·누락·이동·처리량·거부를 대조했다. 종료 제어는 미완료1건에서 시작해 저장 뒤0건이다. 일반 폴링은 기다리지 않지만 종료 시 drain은 정지할 수 있다. 상한2건/64MiB는 수락 입력 용량이며 출력 버퍼·할당자·생산자·엔진·전체 이력 메모리는 포함하지 않는다. 파일 닫기/이름 변경은 전원 장애 내구성이 아니다.

저장 중에는 검증이 끝난 고정 장면을 렌더링한다. 진행 중 시뮬레이션 자동 저장·강제 종료·복구/취소·영구 공정성·임의 NavMesh/물리는 별도 검증이 필요하다. 비동기 제출이 빨라도 전체 완료·CPU·메모리까지 줄었다고 추정하지 않는다. 게임 요청 거부와 저장 작업 제출 거부를 혼동하지 않는다.

## 조작 보정 후속 검증

정책68·실제PIE 네 프로필×관측30/60/144FPS의108상황·같은 패키지의 성능3쌍·정상 속도 실제 영상을 기록했다. 첫 패키지30요청은23.42FPS여서 탈락으로 보존하고 실제PIE에서 목표별 동작을 검사했다. 렌더/Present를 개선하지 않았다. 요청ID·실제 점프/착지·속도·프레임과 만료/중복/재착지를 대조했다. 작은 타이머 비용은 전체 이동 물리 비용이 아니며 FPS향상이나 사람의 조작감 검증을 주장하지 않는다. 코너보정V30·이동발판·벽점프·애니메이션·네트워크·가변 점프 적분은 범위 밖이다.

최신 범위는 제한된 구현5항목/미검증38항목이다. CONTROLLER중 코요테·버퍼V29·V46만 추가했으며 V30과 나머지 조작 기능은 미검증이다. 이전4/39는 역사적 집계다.

## 시야 판정 후속 근거

정책24·실제PIE 두 프로필×관측30/60/144의132상황에서 경계·벽/모서리·얇은벽·대상 뒤 벽·채널·자기 제외와 제외하지 않는 대조군을 확인했다. 정확한 모서리 접촉은 이 백엔드·수치 범위의 관찰이다. 같은 패키지 성능3쌍은 판정을 유지하며 이 실험의 약25% 유효 후보만 쿼리한다. 쿼리/평가/단계 수와 전체 프레임을 함께 보고 FPS향상이나 다수NPC 확장성을 주장하지 않는다. 정상 속도 실제 영상은 측정과 분리한다.

중심점 가림과 전신 노출은 다르며 단순/복잡 충돌·채널·원점·동기화·권한·후보 스케줄링은 실제 프로젝트에서 다시 확인한다. 순찰·추적·전투·기억·EQS·Lambert조명은 구현하지 않았다. 저장·렌더·Present·공용 도구로 확대하지 않았다. 외부 공식 문서는 현재5.9로 표시되어 개념 참고로 사용하고 로컬 API는 설치된5.8.3과 실제 실행으로 검증했다.

최신 집계는 제한된 구현6항목/미검증37항목이다. TRACE중 거리·시야·중심점가림만 추가했고 더 넓은 AI/조명 기능은 미검증이다.

## 언리얼 락온 검증 — 2026-11-11

[실제 결과](../../prototypes/UnrealTechniqueLab/LOCKON-RESULTS.kr.md)는 고정 카메라·알려진5대상의 선택·유지·전환 검증이다. 거리·시야·중심점 Visibility 판정을 재사용한다. 획득1000cm/45도, 유지1100cm/50도 반각과 점수는 실험 설계값이며 상용 게임의 수치가 아니다. 유효한 현재 대상을 유지하고 명시적 좌우 입력으로 수평 각도/고정ID 순서를 순환한다. 전환 후보가 없어도 유지 조건을 만족하는 현재 대상은 남는다.

입력 상승 에지로만 처리하고 양쪽 방향이 함께 눌리면 순서가 엇갈려도 취소한다. 가림·이탈·삭제 시 즉시 해제하며 누름 유지로 재획득하지 않는다. 고정ID와 Actor 수명은 다르므로 이전 약한 참조를 확인해 같은ID의 교체 객체가 선택을 상속하지 않도록 한다. no-hit은 감지가 아니다.

정책37·실제PIE6실행/198상황·관측30/60/144FPS와 동일 패키지 성능3쌍, 정상 속도 실제 캡처를 확인했다. 독립 검토의 양방향 누름 문제는 실패→수정→성공으로 검증했다. 성능 장면에서5회→3회/평가로40% 쿼리가 줄어도 전체 프레임 개선·다수NPC 확장성을 보장하지 않는다. 전체 프레임과 판정 비용을 함께 기록한다. 물리 입력·사용감·카메라 이동·전투AI·이동·네트워크는 미검증이다. 도구/저장/렌더 최적화는 추가하지 않았다.

최신 집계는 제한된 구현7항목/직접 구현 없는36항목이다. 단순 시야 질문은TRACE, 선택 유지/전환/수명 질문은LOCKON으로 찾는다.

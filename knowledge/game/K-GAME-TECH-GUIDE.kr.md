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

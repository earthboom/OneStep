# 발 IK·FABRIK·신체 비율 보정

기준 항목: K-GAME-TECH-IK · 확인일: 2026-11-07 · 참고 지식. 엔진 실행·성능·실제 플레이 검증은 별도다.

## 원리와 구현 요점

발 접촉 지점을 질의하고 이펙터를 놓은 뒤 폴·관절 목표로 무릎 방향을 제한한다. 입력 좌표계를 맞추고 필요하면 골반을 보정하며 보행 단계에 따라 IK를 혼합한다. 팔다리는 2본 해석 해법, 긴 체인은 FABRIK 등을 검토한다.

### 추가 조사로 보완한 구현

Two Bone IK 기반 구현 종합안: 지지면 질의→밑창·굽 오프셋을 포함한 발 목표 변환→안정적인 무릎 목표로 다리 해결→허용 범위의 골반·루트 보정 순서다. 보행 상태에 따라 접촉 제약을 혼합해 공중의 발이 고정되지 않게 한다. 키를 유지하려고 뼈 길이를 바꾸는 미술 해법을 선택했다면 손 도달·앉기 접촉·게임 캡슐을 따로 검증한다. 시각적 뼈 변경이 경쟁 판정을 조용히 바꾸면 안 된다.

## 적용 조건과 한계

IK만으로 완전한 보행이 생기거나 도달 불가능 목표가 해결되지는 않는다. 굽 높이·골격 비율·상호작용 소켓·게임 충돌의 계약이 필요하다. 특정 게임이 정강이를 줄였다는 주장은 별도 미확인이다.

## 적용 전 점검

적용 전 점검: 계단·경사·이동 표면·앉기·손 접촉·극단적 신발에서 발 미끄러짐과 무릎 뒤집힘을 확인한다.

## 근거

- [Epic — Two Bone IK](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-two-bone-ik-in-unreal-engine)
- [Epic — FABRIK AnimBP Node](https://dev.epicgames.com/documentation/unreal-engine/fabrik-animation-blueprint-in-unreal-engine?lang=en-US)

### 추가 조사 출처

- [Epic — Two Bone IK](https://dev.epicgames.com/documentation/en-us/unreal-engine/animation-blueprint-two-bone-ik-in-unreal-engine) — Effector, joint-target and coordinate-space contract; high-heel procedure is proposed transfer, not confirmation of specific commercial games.

추가 조사 출처의 영문 주석은 정확한 절·함수·접근 범위를 보존한다. 원본 슬라이드·문서·공개 코드의 확인과 실제 엔진·하드웨어 실행은 구분한다. 영상 설명·세션 개요만 확인한 자료를 전체 발표 확인으로 간주하지 않는다.

출발 영상: V08, V37. [영상별 대응표](K-GAME-TECH-GUIDE.kr.md).

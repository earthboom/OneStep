# 저장·백업·비트 플래그·패스워드

기준 항목: K-GAME-TECH-SAVE · 확인일: 2026-11-07 · 참고 지식. 엔진 실행·성능·실제 플레이 검증은 별도다.

## 원리와 구현 요점

런타임 포인터 대신 영속 상태·안정적인 객체 ID·스키마 버전을 저장한다. 필요하면 독립 플래그를 비트로 압축한다. 패스워드는 작은 복원 상태를 제한된 문자 집합과 오류 검출 정보로 인코딩한다. 내구성 설계안: 새 저장본을 검증한 뒤 정상 슬롯을 교체하고 복구 세대를 남긴다.

### 추가 조사로 보완한 구현

에메랄드 공개 재구성 코드는 저장 카운터로 슬롯을 선택하고 정상 쓰기 상태를 보존하며 섹터를 기록한다. 읽을 때 데이터 유효성과 세대를 판정한다. 닌텐도 원본 코드나 이번 작업에서 시험한 저장 시스템은 아니다. 새 구현은 세대 ID·데이터 검증·확정 및 복구 순서를 설계하고 파일 두 개만으로 원자성을 가정하지 않는다. 악마성 II의 직접 역공학 FAQ는 상태 7바이트·가산 검사 2바이트·스크램블 1바이트를 16문자로 인코딩한다고 설명한다. 전체 정지 화면 대신 아이템·경험·일수 등 선택 상태를 복원한다.

## 적용 조건과 한계

체크섬은 일부 손상을 검출하지만 위변조 방지 인증은 아니다. 8비트는 독립된 예/아니오 플래그 8개를 저장한다. 두 슬롯만으로 파일시스템 원자성이 보장되지는 않는다.

## 적용 전 점검

적용 전 점검: 쓰기 단계별 중단·데이터 손상·구버전 저장본·객체 참조를 시험하고 대상 플랫폼에서 복구를 확인한다.

## 근거

- [Epic — Saving and Loading Your Game](https://dev.epicgames.com/documentation/en-us/unreal-engine/saving-and-loading-your-game-in-unreal-engine)
- [pret/pokered — save.asm](https://github.com/pret/pokered/blob/master/engine/menus/save.asm)

### 추가 조사 출처

- [pret/pokeemerald — save.c](https://raw.githubusercontent.com/pret/pokeemerald/refs/heads/master/src/save.c) — HandleWriteSector, save generation selection and validation text inspected; community reconstruction; no ROM build or fault injection.
- [kingshriek — Simon's Quest Password System FAQ](https://gamefaqs.gamespot.com/nes/587179-castlevania-ii-simons-quest/faqs/38582) — Original reverse-engineering account, generation/decoding sections; exact ROM behavior not independently executed; do not copy apparent transcription errors as a tested decoder.

추가 조사 출처의 영문 주석은 정확한 절·함수·접근 범위를 보존한다. 원본 슬라이드·문서·공개 코드의 확인과 실제 엔진·하드웨어 실행은 구분한다. 영상 설명·세션 개요만 확인한 자료를 전체 발표 확인으로 간주하지 않는다.

출발 영상: V20, V54. [영상별 대응표](K-GAME-TECH-GUIDE.kr.md).

# 코드 지식

구현·시스템·런타임·검증 지식을 실제 변경 조건에 맞게 조회한다. 설계 질문은 [원칙 재사용](K-CODE-PRINCIPLE-REUSE.kr.md), 실제 언리얼 플레이는 [PIE 검증](K-CODE-UE-PIE-VERIFICATION.kr.md)에서 시작한다. 영문 정본에서 생성한 사람용 목록이며 원문을 직접 확인한다.

|ID|주제|상세|확인일|
|---|---|---|---|
|K-CODE-ABSTRACTION-COST|전체 추론 비용을 줄일 때 추상화를 도입하기|[읽기](K-CODE-ABSTRACTION-COST.kr.md)|2026-11-07|
|K-CODE-API-CONTRACTS|의존성 교체 전에 인터페이스 의무와 보장을 명시하기|[읽기](K-CODE-API-CONTRACTS.kr.md)|2026-11-07|
|K-CODE-CHANGE-TESTS|안정적인 동작 경계에서 변경을 검증하기|[읽기](K-CODE-CHANGE-TESTS.kr.md)|2026-11-07|
|K-CODE-CONCURRENCY-LIFETIMES|비동기 수명·동기화·종료 계약을 따로 검토하기|[읽기](K-CODE-CONCURRENCY-LIFETIMES.kr.md)|2026-11-07|
|K-CODE-CONFIGURATION-POLICY|불변 상수·조정 정책·배포 설정·비밀을 구분하기|[읽기](K-CODE-CONFIGURATION-POLICY.kr.md)|2026-11-07|
|K-CODE-DATA-INVARIANTS|유효한 데이터 상태와 전이를 명시적으로 검증하기|[읽기](K-CODE-DATA-INVARIANTS.kr.md)|2026-11-07|
|K-CODE-DEPENDENCY-DIRECTION|정책을 보호하는 계약으로 의존 방향 정하기|[읽기](K-CODE-DEPENDENCY-DIRECTION.kr.md)|2026-11-07|
|K-CODE-DEPENDENCY-SELECTION|수명 가치와 소유 비용으로 의존성 선택하기|[읽기](K-CODE-DEPENDENCY-SELECTION.kr.md)|2026-11-07|
|K-CODE-GC-LIFETIMES|가비지 수집·자원 정리·메모리 진단을 구분하기|[읽기](K-CODE-GC-LIFETIMES.kr.md)|2026-11-07|
|K-CODE-GIT-ISOLATED-MERGE|주 작업 사본을 보존하며 희소 연결 작업트리에서 병합하기|[읽기](K-CODE-GIT-ISOLATED-MERGE.kr.md)|2026-11-06|
|K-CODE-INFORMATION-HIDING|숨겨야 할 설계 결정을 중심으로 모듈 나누기|[읽기](K-CODE-INFORMATION-HIDING.kr.md)|2026-11-07|
|K-CODE-MAINTAINABILITY-EVIDENCE|구체적인 변경과 여러 결과로 유지보수성 판단하기|[읽기](K-CODE-MAINTAINABILITY-EVIDENCE.kr.md)|2026-11-07|
|K-CODE-PERFORMANCE-MEASUREMENT|최적화 전에 대표 부하·전체 프레임·계획 발생 꼬리 측정하기|[읽기](K-CODE-PERFORMANCE-MEASUREMENT.kr.md)|2026-11-11|
|K-CODE-PRINCIPLE-REUSE|구체적인 계약과 변경 위험으로 코딩 원칙 적용하기|[읽기](K-CODE-PRINCIPLE-REUSE.kr.md)|2026-11-07|
|K-CODE-READABILITY|구체적인 유지보수 질문으로 가독성 검토하기|[읽기](K-CODE-READABILITY.kr.md)|2026-11-07|
|K-CODE-RESOURCE-OWNERSHIP|모듈 경계에서 자원 소유·빌림을 명시하기|[읽기](K-CODE-RESOURCE-OWNERSHIP.kr.md)|2026-11-07|
|K-CODE-UE-ENGINE-CHECKOUT|커스텀 언리얼 엔진을 읽기 전에 현재 소스 사본 확인하기|[읽기](K-CODE-UE-ENGINE-CHECKOUT.kr.md)|2026-11-06|
|K-CODE-UE-LOC-MERGE|언리얼 로컬라이제이션 충돌을 의미적으로 병합하고 locres 일치 검증하기|[읽기](K-CODE-UE-LOC-MERGE.kr.md)|2026-11-06|
|K-CODE-UE-LOCAL-ONLY-WORK|공유 DDC·분산 컴파일 경로를 확인해 에디터 작업을 로컬로 제한하기|[읽기](K-CODE-UE-LOCAL-ONLY-WORK.kr.md)|2026-11-06|
|K-CODE-UE-PIE-VERIFICATION|네이티브 에디터 API로 실제 PIE·메시 위치·요청 ID 검증하기|[읽기](K-CODE-UE-PIE-VERIFICATION.kr.md)|2026-11-11|
|K-CODE-UE-RENDER-ORIENTATION|분석·최적화 전에 언리얼 프로젝트 렌더링 설정 파악하기|[읽기](K-CODE-UE-RENDER-ORIENTATION.kr.md)|2026-11-05|
|K-CODE-UE-RENDERDOC-ATTACH|언리얼 에디터에 RenderDoc을 연결하고 시작 장애 해결하기|[읽기](K-CODE-UE-RENDERDOC-ATTACH.kr.md)|2026-11-06|

## 무차선 지속 유입의 실제 검증

[UE5.8.3 결과](../../prototypes/UnrealTechniqueLab/ADMISSION-RESULTS.kr.md)는 정책 이름과 실제 설정·거부된 원래 요청 ID·제공/수락/완료/거부·토큰/대기열·전체 프레임을 대조한다. 처리량과 개별 대기를 구분하고 계획이 일어난 현재/다음 프레임 꼬리를 포함한다. 영상15배속·감사 비용과 실시간 성능, 비동기 CPU/GPU·결측·초기화 제외 구간을 구분한다.

## 전체 입력 소유형 비동기 저장

[실제 검증](../../prototypes/UnrealTechniqueLab/ASYNC-SAVE-RESULTS.kr.md)은 동기/비동기3쌍, 원래 기록·경로·이동/서비스, 큐/오류/종료/전체 프레임·메모리와 실제 영상을 확인한다. 제출 정지는 줄고 총 완료는 늘었다. 종료 대기와 전체 입력 독립 소유가 필요하며 진행 중 자동 저장·복구/강제 종료·전체 메모리 상한을 보장하지 않는다. 지식6/검색115/적용6 조건을 참고한다.

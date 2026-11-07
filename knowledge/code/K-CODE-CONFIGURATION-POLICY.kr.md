# 불변 상수·조정 정책·배포 설정·비밀정보 구분

사람 전용 번역. AI는 영문 K-CODE-CONFIGURATION-POLICY.md를 사용한다.

ID: K-CODE-CONFIGURATION-POLICY. 유형: 참고 자료. 상태: 사용 가능. 근거 확인일: 2026-11-07.

요약: 값을 외부로 옮기기 전에 의미·관리 주체·변경 주기를 분류한다. 불변에는 이름 있는 상수, 실제 변화에는 검증한 데이터·설정, 자격증명에는 적절한 비밀정보 관리를 사용한다.

범위: 애플리케이션·게임의 설정·데이터 설계. Twelve-Factor 배포 지침과 Unreal 데이터 작업은 각 맥락을 유지한다.

검색어: hardcoding, magic-number, configuration, constant, data-driven, secrets, validation, 하드코딩, 매직넘버, 설정, 상수, 데이터주도, 비밀정보

## 활용 지침

출처 관찰: C++ 지침 ES.45는 의미가 불명확한 리터럴 대신 이름 있는 상수를 권한다 [S1]. Twelve-Factor는 배포별 설정과 내부 애플리케이션 구조를 구별한다 [S2]. Epic은 게임 조정을 위한 외부 작성 테이블·커브를 설명한다 [S3]. OWASP는 비밀정보를 파일 위치뿐 아니라 접근·수명주기 문제로 다룬다 [S4].

응용 방법: 값을 도메인·프로토콜 불변, 제품 정책·조정값, 환경별 설정, 비밀정보, 예제·시험 데이터로 분류한다. 누가 얼마나 자주 바꾸며 빌드·콘텐츠 배포·배포 환경 변경·실시간 다시 읽기 중 무엇이 필요한지 정한다. 그 주기를 지원하는 가장 단순한 표현을 선택한다.

설정에는 형·단위·유효 범위·필수 여부·기본값·우선순위·호환성을 정의한다. 입력 경계에서 검증하고 적용된 비밀 아닌 값을 확인할 수 있게 한다. 다시 읽기는 일관성·실패 동작이 있는 상태 전이로 다루며 변경 가능한 전역 설정 읽기를 업무 로직 전체에 흩뿌리지 않는다.

## 적용 조건과 예외

리터럴 자체가 결함은 아니다. 명확한 작은 값·규격 상수·시험 벡터는 코드에 있는 편이 명료할 수 있다. 모든 숫자를 외부화하면 스키마·전달·호환 비용이 늘어난다. 환경변수가 보편 게임 콘텐츠 형식이나 충분한 비밀 보호는 아니다. 테이블의 값 변경과 실행 정책 변경을 구별하고 기준과 검증을 명시한다.

## 확인 항목

제안 점검: 의도한 담당자가 무관한 로직 수정 없이 정책을 바꿀 수 있는가? 누락·오류·충돌 값을 의도대로 처리하는가? 자격증명 노출 없이 배포의 적용 설정을 재현할 수 있는가? 실제 경계의 버전·검증을 확인하며 상수를 파일로 옮긴 것만으로 유지보수성을 입증하지 않는다.

## 근거

- [S1] [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-magic)의 ES.45 Reason·Example·Enforcement. 이 항목에서는 해당 규칙만 사용했다.
- [S2] [Twelve-Factor: Config](https://www.12factor.net/config)의 배포별 변화와 내부 설정 제외 설명.
- [S3] Epic [데이터 기반 게임플레이](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine)의 테이블·커브·작성 작업 흐름. 확인 당시 UE5.8 문서.
- [S4] OWASP [Secrets Management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)의 도입·일반 관리·수명주기.
- 공식 원문 구획 확인일 2026-11-07. 이번 작업에서 실제 코드·비밀정보에 분류·점검을 적용하지 않았다.

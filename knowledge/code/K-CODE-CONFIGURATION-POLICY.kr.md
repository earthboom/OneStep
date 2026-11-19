# 불변 상수, 조정 가능한 정책, 배포 설정과 비밀 구분하기

항목 `K-CODE-CONFIGURATION-POLICY` · 상태 활성 · 확인일 2026-11-07

검색어 hardcoding, magic-number, configuration, constant, data-driven, secrets, validation, 하드코딩, 매직넘버, 설정, 상수, 데이터주도, 비밀정보, UDataTable, FTableRowBase, UCurveTable, curve interpolation

## 지침

의미를 알 수 없는 리터럴에는 의도를 나타내는 상수를 고려한다(C++ ES.45). 배포에 따라 변하는 환경 설정과 애플리케이션 구조를 가른다. UE의 UDataTable은 FTableRowBase에서 파생된 반영 스키마에 맞는 이름 있는 행을 보관한다. UCurveTable은 입력값으로 평가하는 이름 있는 수치 곡선을 보관한다. 행의 단위·범위·누락 정책을, 곡선에서는 보간과 입력 범위를 확인한다. 비밀은 위치뿐 아니라 접근과 교체 수명주기를 관리한다.

값이 규격의 불변식인지, 튜닝 정책인지, 환경 설정·비밀 또는 예제 데이터인지 분류한다. 변경자·빈도와 빌드, 콘텐츠 릴리스, 배포, 런타임 재로드의 필요성을 보고 표현을 고른다. 타입·단위·범위·기본값·우선순위·호환성을 검증하고 비밀을 제외한 유효값은 확인 가능하게 한다. 재로드의 일관성과 실패 동작도 설계한다.

## 적용 범위와 예외

명백한 값과 테스트 벡터는 코드에서 더 명료할 수 있다. 모든 수치의 외부화에는 스키마·배포 비용이 따른다. 환경 변수는 만능 게임 콘텐츠 포맷이나 충분한 비밀 보호가 아니다. 표는 데이터를 바꾸므로 동작 변경의 권한과 검증을 분명히 한다.

## 점검

의도한 담당자가 관련 없는 로직 수정 없이 정책을 바꿀 수 있는가? 잘못된·누락된·충돌한 값과 예전 데이터를 처리하는가? 자격 증명을 노출하지 않고 릴리스별 유효 설정을 재현할 수 있는가?

## 근거

C++ Core Guidelines ES.45, Twelve-Factor의 Config, UE 5.8 데이터 주도 게임플레이 표·곡선, OWASP 비밀 관리 수명주기를 기준으로 한 문헌 종합이다. 2026-11-07 원래 조사는 로컬 구현이나 실제 비밀을 시험하지 않았다. [C++ ES.45](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines#Res-magic) · [Twelve-Factor Config](https://www.12factor.net/config) · [Epic data-driven gameplay](https://dev.epicgames.com/documentation/en-us/unreal-engine/data-driven-gameplay-elements-in-unreal-engine?application_version=5.8) · [OWASP secrets management](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)

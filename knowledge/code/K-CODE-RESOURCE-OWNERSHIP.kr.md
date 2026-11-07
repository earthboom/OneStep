# 모듈 경계에서 자원 소유권과 빌림을 명시한다

- ID: K-CODE-RESOURCE-OWNERSHIP
- 요약: 각 자원의 정리 책임자를 식별하고 인터페이스에 이전·빌림을 표현합니다. 독립적인 수명에 필요할 때 공유 소유권을 도입하며 C++ RAII·Rust·Unreal UObject의 계약을 구분합니다.
- 종류: 참고 지식 / 상태: 활성 / 근거 확인일: 2026-11-07
- 범위: C++·Rust·Unreal Engine의 자원 및 인터페이스 설계. 모든 언어의 보장이 아닌 출처 비교입니다.
- 검색어: ownership, borrowing, RAII, unique_ptr, shared_ptr, weak_ptr, Rust, Drop, Unreal Engine, UObject, 소유권, 빌림, 자원 수명, 순환 참조
- 확인 및 적용 맥락: 2026-11-07 일차 문서와 UE 5.8 온라인 자료를 확인했습니다. 구현·실행 검증 없는 출처 종합과 제안 점검입니다.

## 지침

누가 자원을 해제하고 누가 잠시 사용하며 어떤 사건이 그 허용을 끝내는지 묻습니다. 힙뿐 아니라 파일·소켓·잠금·네이티브 핸들을 포함합니다. 모든 호출자를 추적하지 않아도 유지보수자가 이해할 수 있는 수명 계약을 선호합니다.

C++ Core Guidelines는 획득·해제 쌍에 RAII 래퍼를, 공유가 필요하지 않으면 고유 소유권을 권장합니다. 정상 범위 종료·예외 스택 풀기는 올바르게 생성한 자동 래퍼를 해제하지만 비동기 완료까지 입증하지는 않습니다. 강한 shared_ptr 순환은 회수를 막을 수 있습니다. 소유 모델에 맞을 때만 약한 역참조를 선택합니다.

Rust는 소유권 이동·빌림을 타입에 드러냅니다. Book의 String 예는 소유자 범위 끝의 drop으로 할당을 해제합니다. 참조는 소유하지 않고 빌리며 안전 참조 규칙은 유효성·동시 가변 접근을 제한합니다. 이는 로컬 추론을 돕지만 모든 자원 프로토콜을 자동화하지는 않습니다.

Unreal의 TSharedPtr·TUniquePtr 계열은 일반 C++ 객체를 관리하며 Epic은 이를 UObject 관리와 구분합니다. UObject 수명에는 엔진 객체 참조 기전을 선택하고 일반 스마트 포인터로 삭제 책임을 옮기지 않습니다.

## 적용 조건과 예외

소유권 중심 API나 생태계 전환 검토에 사용합니다. 계약 위반 시 빌린 뷰도 무효화될 수 있습니다. 기존 raw 포인터는 관례와 달리 소유권을 담을 수 있으므로 실제 계약을 읽습니다. 사용자 할당자·아레나·외부 인터페이스·프레임워크 수명에는 자체 해제 규칙이 필요합니다. RAII는 강제 종료의 정리나 스레드 안전성을 보장하지 않습니다.

## 점검

다음은 제안하는 검토입니다.

- 획득에서 성공·조기 반환·실패·이전을 추적하고 소유 경로마다 정리 책임을 식별합니다.
- 반환 뷰·콜백·저장 참조와 기반 소유자 수명을 비교합니다. 각 공유 소유자와 강한 순환을 검토합니다.
- Unreal 대상이 UObject인지 확인한 뒤 포인터 계열을 선택합니다. 예방을 주장하기 전에 실제 프로젝트 정리를 검사합니다.

## 근거

2026-11-07 관련 본문을 확인했습니다.

- [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines): R.1·R.21·R.24. 권고이며 컴파일러 강제 소유권 시스템이 아닙니다.
- [Rust 소유권](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html): Ownership Rules, Memory and Allocation. 온라인 Book입니다.
- [Rust 참조와 빌림](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html): Mutable References, Dangling References의 안전 참조 예입니다.
- [Epic 스마트 포인터](https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-pointers-in-unreal-engine): 도입과 Tips and Limitations, UE 5.8로 제공됐습니다.

프로젝트 정리 시나리오·sanitizer 실행은 하지 않았으며 위 점검은 제안 상태입니다.

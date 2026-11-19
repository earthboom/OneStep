# 모듈 경계에서 자원 소유권과 빌림 명확히 하기

항목 `K-CODE-RESOURCE-OWNERSHIP` · 상태 활성 · 확인일 2026-11-07

검색어 ownership, borrowing, RAII, unique_ptr, shared_ptr, weak_ptr, Rust, Drop, Unreal Engine, UObject, 소유권, 빌림, 자원 수명, 순환 참조, std::unique_ptr, std::shared_ptr, std::weak_ptr, std::weak_ptr::lock, TSharedPtr, TUniquePtr

## 지침

메모리, 파일, 소켓, 잠금, 네이티브 핸들을 누가 해제하고 누가 언제까지 빌려 쓰는지 명시한다. C++의 RAII는 자원 획득과 해제를 객체 수명에 묶는다. 정상 범위 종료와 예외 되감기 시 이미 생성된 자동 객체가 정리된다. std::unique_ptr은 이동으로 단독 소유권을 넘긴다. std::shared_ptr은 소유권을 공유하고 강한 소유권 순환은 정리를 가로막는다. std::weak_ptr은 생존을 연장하지 않으며 lock()으로 가능한 동안 임시 소유권을 얻는다.

Rust의 소유·이동·빌림은 타입에 드러난다. String은 소유자 범위 종료의 drop으로 할당을 해제하고 참조는 값을 빌린다. 안전 참조는 유효성과 가변 접근을 제한한다. 언리얼 TSharedPtr과 TUniquePtr은 각각 일반 C++ 객체의 공유·단독 소유권을 표현한다. UObject의 수명은 엔진의 객체 참조 체계를 사용한다.

## 적용 범위와 예외

레거시 원시 포인터, 아레나, 커스텀 할당자, 외부 ABI는 실제 계약을 확인한다. RAII는 강제 종료 후 정리, 작업 완료나 스레드 안전을 보장하지 않는다.

## 점검

획득에서 성공·조기 반환·실패·이동까지 정리 책임을 추적한다. 뷰·콜백·보관 참조가 소유자보다 오래 남는지, 강한 순환이 있는지 검사한다. 대상이 UObject인지 확인하고 실제 프로젝트에서 정리를 시험한다.

## 근거

2026-11-07 조사한 C++ 권고, Rust Book의 소유·빌림, UE 5.8 문서에 C++ 표준 초안의 소유 의미를 대조했다. 문서 기반의 제안이며 실제 정리 시나리오나 새니타이저를 실행하지 않았다. [C++ Core Guidelines R.1, R.21, R.24](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) · [C++ working draft, smart pointers](https://eel.is/c++draft/smartptr) · [Rust ownership](https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html) · [Rust borrowing](https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html) · [Epic smart pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-pointers-in-unreal-engine?application_version=5.8)

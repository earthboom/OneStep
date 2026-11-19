# 비동기 수명·동기화·종료의 계약 따로 검토하기

항목 `K-CODE-CONCURRENCY-LIFETIMES` · 상태 활성 · 확인일 2026-11-07

검색어 concurrency, lifetime, cancellation, synchronization, safe publication, shared_ptr, Send, Sync, Drop, Go memory model, 동시성, 비동기 수명, 취소, 동기화, 안전한 공개, std::shared_ptr, std::shared_ptr::use_count, aliasing constructor, RAII

## 지침

큐와 콜백에서 데이터가 살아 있는지, 충돌 접근이 동기화되는지, 작업 종료 후 누가 정리하는지를 따로 확인한다. RAII 래퍼가 범위를 벗어나는 것만으로 워커 종료가 보장되지는 않는다.

C++ std::shared_ptr의 소유권 회계와 대상의 가변 상태를 구분한다. 동일 포인터 변수와 서로 다른 소유자를 따로 본다. 별칭 생성자에서 소유 대상과 무관한 저장 포인터의 수명은 연장되지 않는다. std::shared_ptr::use_count는 소유자 수의 관찰값으로 데이터 접근의 순서나 작업 완료를 보장하지 않는다.

Rust의 Send는 소유권의 스레드 간 전달, Sync는 공유 참조 접근에 대한 계약이다. Rc는 그 보장을 주지 않는다. 수동 구현은 unsafe 조건을 검토한다. 소멸을 억제하거나 되감기 없이 종료할 수 있으므로 누수·교착·작업 완료는 별도 문제다. Go의 고루틴 종료만으로 다른 참여자의 관찰이 동기화되지 않는다. 채널·락·원자 연산의 약속을 확인한다.

## 적용 범위와 예외

언어·런타임별 계약이다. 취소는 협조 요청·결과 폐기·미래값 드롭·작업 중단 등 다양하다. 생존만으로 스레드 소속이나 엔진 API 호출 권한을 보장하지 않는다.

## 점검

대기·중단·재시도·객체 파괴 후 캡처 수명과 완료 이벤트를 추적한다. 채널·뮤텍스·원자 연산으로 정한 순서 및 락 순서를 그린다. 시작 전·실행 중·종료 중 취소와 뒤늦은 콜백, 경합 속 종료를 시험한다. 한 번 통과한 실행은 가능한 스케줄 일부다.

## 근거

2026-11-07 C++ 공개 초안의 shared_ptr 일반·별칭·관찰 항목, Rust의 Send/Sync와 소멸, 2022-06-06 Go 메모리 모델을 조사했다. 실제 스케줄러나 경합 탐지기, 취소·종료 시나리오는 실행하지 않았다. [C++ working draft, shared_ptr](https://eel.is/c++draft/util.smartptr.shared) · [Rust Send and Sync](https://doc.rust-lang.org/book/ch16-04-extensible-concurrency-sync-and-send.html) · [Rust destructors](https://doc.rust-lang.org/reference/destructors.html) · [Go memory model](https://go.dev/ref/mem)

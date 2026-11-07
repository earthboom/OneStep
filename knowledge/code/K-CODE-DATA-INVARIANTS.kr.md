# 유효한 데이터 상태를 명시하고 전이 검증

사람 전용 번역. AI는 영문 K-CODE-DATA-INVARIANTS.md를 사용한다.

ID: K-CODE-DATA-INVARIANTS. 유형: 참고 자료. 상태: 사용 가능. 근거 확인일: 2026-11-07.

요약: 언어가 지원하는 형과 캡슐화한 생성으로 유효한 상태·부재·오류를 구별한다. 외부 경계의 실행 시 검증을 유지하고 표현을 무효화할 변경·전이를 점검한다.

범위: 데이터 모델·불변식 설계. OCaml·Rust 사례는 실제 언어·직렬화·변경 경로에 맞게 적용한다.

검색어: invariant, type, state-machine, enum, validation, encapsulation, immutability, 불변식, 타입, 상태, 유효성검사, 캡슐화, 불변데이터

## 활용 지침

출처 관찰: Minsky의 OCaml 예제는 연결 상태 레코드를 상태별 데이터로 바꾼다 [S1]. Rust 책은 enum·Option으로 선택지·존재를 구분하고 [S2], 비공개 표현과 검증 생성자를 보인다 [S3]. 표현 기법이지 모든 업무 규칙의 증명은 아니다.

응용 방법: 실제 도메인 상태, 각 상태에 필요한 데이터, 허용 전이를 나열한다. 불가능한 조합을 허용하는 무관한 bool·선택 필드를 피한다. 모든 원시값을 감싸기 위해서가 아니라 반복 해석·검증을 줄일 때 집중된 값 형을 도입한다.

생성·파싱·역직렬화·변경이 같은 불변 경계를 지키게 한다. 잘못된 외부 입력의 보고와 복구 위치를 정한다. 혼동 비용이 크면 단위·정체를 구별한다. 호출자가 숨은 setter 순서를 기억하지 않아도 되도록 공개 계약에 전이를 드러낸다.

## 적용 조건과 예외

빠진 규칙·틀린 모델·공개 변경·리플렉션·unsafe·검증 없는 역직렬화는 형만으로 막지 못한다. 부호 없는 형이 업무 범위를 보장하지는 않는다. 트랜잭션·편집기의 중간 상태가 합법이면 작업을 금지하지 말고 모델링한다. 예외·오류 반환·panic·assert는 실제 언어 계약에 따라 고른다.

## 확인 항목

제안 점검: 지원하는 진입점에서 잘못된 조합을 만들 수 있는가? 전이가 필수 데이터를 보존하고 올바른 경계에서 잘못된 입력을 거절하는가? 생성자의 정상 경로뿐 아니라 직렬화 왕복·버전 변경·변경 작업을 확인한다. 정적 보장 주장은 실제 컴파일러·런타임에서 검증해야 하며 이번에는 실행하지 않았다.

## 근거

- [S1] Yaron Minsky, [Effective ML Revisited](https://blog.janestreet.com/effective-ml-revisited/), 2011. Make illegal states unrepresentable 공개 예제를 읽었으며 연결 강연은 미시청.
- [S2] [Rust 책: enum 정의](https://doc.rust-lang.org/book/ch06-01-defining-an-enum.html)의 variant 데이터·Option.
- [S3] [panic 사용 판단](https://doc.rust-lang.org/book/ch09-03-to-panic-or-not-to-panic.html)의 Custom Types for Validation, 가시성·생성.
- 저자·공식 본문 확인일 2026-11-07. 점검은 종합 제안이며 프로젝트의 컴파일·직렬화 시험을 한 것은 아니다.

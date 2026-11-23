---
id: K-CODE-UE-AUTOMATION-EXPECTED-MESSAGES
title: 언리얼 자동화 테스트가 같은 기대 로그 메시지를 두 번 선언하면 어떻게 되는가
summary: FAutomationTestBase는 기대 메시지를 패턴 문자열만 키로 쓰는 집합에 담는다. 그래서 같은 패턴으로 나중에 부른 AddExpectedError나 AddExpectedMessage가 앞 선언을 횟수, 상세도, 비교 방식까지 통째로 바꾼다. 공용 하네스가 환경 메시지를 선언할 때 테스트 본문에서 같은 패턴을 또 선언하면, 본문 선언이 덮이거나 하네스 선언을 덮는다.
kind: reference
scope: 언리얼 엔진 5 자동화 프레임워크(FAutomationTestBase)의 기대 오류, 경고, 메시지 선언. 테스트 도중 선언하는 잠재(latent) 명령 포함
keywords: [FAutomationTestBase, AddExpectedError, AddExpectedMessage, AddExpectedMessagePlain, FAutomationExpectedMessage, ExpectedMessages, EAutomationExpectedErrorFlags, EAutomationExpectedMessageFlags, Occurrences, TSet, MoveByRelocate, expected error, expected occurrences, test harness, local whitelist, 기대 오류, 예상 에러 선언]
status: active
checked_at: "2026-11-23"
context:
  engine: 언리얼 엔진 5.8 소스(Runtime/Core Misc/AutomationTest와 Containers)
---

## 안내

`FAutomationTestBase::AddExpectedMessage`(그리고 이 함수로 넘기는 `AddExpectedError`, `AddExpectedMessagePlain`)는 `FAutomationExpectedMessage`를 `TSet<FAutomationExpectedMessage>`인 `ExpectedMessages`에 더한다. 원소의 같음 비교와 해시는 `MessagePatternString`만 쓴다. 이 집합은 중복 키를 허용하지 않으므로, 이미 있는 패턴과 같은 원소를 더하면 새 원소가 옛 원소 자리로 옮겨져 덮어쓴다. 한 패턴에는 마지막 선언만 남고, 그 선언의 횟수, 상세도, 비교 방식, 정규식 여부가 앞 값을 대신한다. 선언끼리 더해지지 않는다.

결과:

- 환경 메시지(예: 클라이언트마다 나오는 헤드리스 렌더링 메시지)를 선언하는 공용 하네스와 같은 패턴을 선언하는 테스트 본문은 합쳐지지 않는다. 나중에 실행된 호출이 기대 횟수를 정한다. 잠재 명령은 `RunTest`가 반환된 뒤에 돌므로, 잠재 명령 안에서 한 하네스 선언이 테스트 본문의 선언을 덮는다.
- 횟수가 같은 중복 선언은 해가 없어 보이지만 죽은 코드이고, 한쪽이 바뀌면 실제 횟수와 조용히 어긋난다. 환경 잡음은 한 곳에서만 선언하고, 테스트는 그 소유자가 필요로 하는 사실(예: 클라이언트 수)을 넘긴다.
- 한 글자라도 다른 패턴은 별개 항목이며 따로 검사된다.

## 적용 범위와 예외

5.8 엔진 소스로 확인했다. 덮어쓰기 동작은 이 멤버의 `TSet`이 중복 키 없이 기본 키 함수를 쓴다는 데 기댄다. 그 버전에서는 성립한다. 다른 엔진 버전에서는 기대기 전에 같은 두 곳을 확인한다. 이 항목은 선언 저장만 다룬다. 테스트 끝에서 맞은 메시지를 세는 방식은 그대로다.

## 점검

- 테스트에 기대 메시지를 더하기 전에, 그 테스트가 쓰는 공용 하네스와 헬퍼에서 같은 패턴 문자열을 찾는다. 있으면 지역 선언을 지우고 하네스가 필요로 하는 입력을 넘긴다.
- 한 시나리오에서 횟수를 바꿔야 하면 선언을 정확히 한 곳에서 하고, 실행해서 기대 횟수가 충족됐다고 보고되는지 확인한다.

## 근거

- 엔진 소스, UE 5.8: `Runtime/Core/Public/Misc/AutomationTest.h`: `FAutomationExpectedMessage::operator==`와 `GetTypeHash`는 `MessagePatternString`만 비교한다. 멤버 `TSet<FAutomationExpectedMessage> ExpectedMessages`.
- `Runtime/Core/Private/Misc/AutomationTest.cpp`: `FAutomationTestBase::AddExpectedMessage`는 조회 없이 `ExpectedMessages.Add(...)`를 부른다.
- `Runtime/Core/Public/Containers/CompactSet.h.inl`와 `SparseSet.h.inl`: `bAllowDuplicateKeys`가 거짓이고 키가 이미 있으면 새 원소가 `MoveByRelocate`로 기존 원소를 대신한다.
- 작업 확인(2026-11-23): 한 게임 테스트 묶음이 테스트마다 헤드리스 커서 메시지를 선언했고, 공용 네트워크 테스트 하네스가 잠재 명령에서 같은 패턴을 나중에 선언했다. 지역 선언을 지우고 하네스 선언만으로 묶음을 다시 돌렸다.

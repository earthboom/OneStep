# 빈 FGameplayTagQuery와 빈 태그 컨테이너가 Unreal에서 무엇과 일치하는가, 그리고 비어 있는 허용 목록에 따로 검사가 필요한 이유

- **ID:** K-CODE-UE-TAGQUERY-EMPTY-MATCH
- **종류:** reference
- **상태:** active
- **근거 확인일:** 2026-11-24
- **범위:** Unreal Engine 5 GameplayTags 런타임 모듈. 디자이너가 작성한 태그 조건이나 태그 컨테이너로 액터를 거르거나 고르는 코드
- **맥락:** 엔진 Unreal Engine 5.8 (5.8.0 소스 트리)
- **키워드:** FGameplayTagQuery, FGameplayTagContainer, MatchesQuery, Matches, IsEmpty, HasAny, HasAll, empty query, allowlist, optional filter, match-all, gameplay tag, designer-authored condition, unset property
- **요약:** FGameplayTagQuery::Matches는 빈 조건에 false를 돌려주고, 빈 컨테이너에 대해 HasAny는 false, HasAll은 true를 돌려준다. 프로젝트 래퍼는 빈 조건을 전부 일치로 바꾸는 경우가 많다. 조건이 어떤 동작이 건드릴 대상을 고르는 용도라면, 일치 호출에 맡기지 말고 설정 시점에 비어 있는지 검사한다.

## 지침

게임플레이 태그 조건(`FGameplayTagQuery`)은 디자이너가 게임플레이 태그로 작성하는 불 식이다. 태그 컨테이너(`FGameplayTagContainer`)는 태그 집합이다. 조건 쪽이 비어 있을 때 각 호출의 답은 정해져 있고 서로 다르다.

| 호출 | 빈 조건의 결과 | 뜻 |
| --- | --- | --- |
| `FGameplayTagQuery::Matches(Tags)` | false | 설정하지 않은 조건은 아무것과도 일치하지 않는다 |
| `FGameplayTagContainer::MatchesQuery(Query)` | false | `Query.Matches(*this)`로 넘긴다 |
| 빈 `Other`에 대한 `FGameplayTagContainer::HasAny(Other)` | false | 찾을 것이 없다 |
| 빈 `Other`에 대한 `FGameplayTagContainer::HasAll(Other)` | true | 실패한 검사가 없다 |

빈 조건이 무엇을 뜻해야 하는지는 그 조건의 역할로 정하고, 실제 호출 경로가 그 뜻을 내는지 확인한다.

- **선택 필터** (기본으로 허용된 것에 거는 제한. 예: "대상이 이 태그들을 가질 때만 적용"): 비어 있으면 제한이 없다는 뜻이므로 원하는 답은 true다. 엔진의 조건 호출은 그 답을 주지 않는다. 그래서 프로젝트는 흔히 `Query.IsEmpty() ? true : Tags.MatchesQuery(Query)` 형태로 감싼다.
- **허용 목록 또는 선택** (조건이 동작이 건드릴 대상을 지정하고 나머지는 그대로 둔다): 비어 있으면 아무것도 고르지 않는다는 뜻이므로 원하는 답은 false다. 이런 조건을 전부 일치로 읽는 래퍼에 넘기면, 설정하지 않은 속성이 모든 후보를 고른다.

허용 목록에서는 빈 경우를 일치 호출에 맡기지 않는다. 소유자를 설정하거나 활성화할 때 한 번 `IsEmpty()`를 검사하고(조건이 데이터 에셋에 있으면 에셋이 null인지도 함께), 소유자 이름을 넣은 눈에 보이는 에러로 알리고, 그 선택 경로를 끈다. 그러면 후보별 일치 호출은 빈 조건을 볼 일이 없고, 래퍼가 어느 쪽 의미이든 안전하다.

## 적용 범위와 예외

- 표는 엔진 동작이다. 엔진 함수와 이름이 같은 프로젝트 헬퍼는 다를 수 있다. 어느 쪽 의미인지 가정하기 전에 헬퍼를 읽는다.
- 빈 조건은 내용 때문에 아무것과도 일치하지 않는 조건(예: 어떤 객체도 갖지 않은 태그에 대한 조건)과 다르다. 설정 시점 검사는 설정하지 않은 경우만 잡는다. 다른 경우에는 회귀 테스트나 데이터 검사가 필요하다.
- 빈 컨테이너에 대해 `HasAll`이 true를 돌려주는 것은 컨테이너 형태의 같은 위험이다. "이것들을 모두 가져야 한다" 목록을 비워 두면 모든 후보가 통과한다.
- 이 항목은 `FGameplayTagRequirements`나 게임플레이 이펙트 적용 요구 조건을 다루지 않는다. 그쪽의 빈 경우 동작은 읽지 않았다.

## 점검

- 디자이너가 작성하는 태그 조건마다, 제한하는 조건인지 고르는 조건인지와 설정하지 않은 값이 무엇을 해야 하는지를 적는다.
- 코드가 실제로 부르는 함수(엔진 호출이든 프로젝트 래퍼든)를 열어 빈 조건 분기를 읽는다.
- 고르는 조건이라면, 첫 후보를 검사하기 전에 비었거나 없는 조건을 거부하는 곳을 찾고, 소유자 이름과 함께 로그를 남기는지 확인한다.
- 조건을 설정하지 않은 채 소유자를 실행해, 어떤 후보도 선택되지 않고 에러가 보고되는지 확인하는 테스트를 더한다.

## 근거

2026-11-24에 UE 5.8.0 소스 트리의 `Engine/Source/Runtime/GameplayTags` 모듈에서 읽었다.

- `Private/GameplayTagContainer.cpp`: `FGameplayTagQuery::Matches`는 `IsEmpty()`이면 false를 돌려준다. `FGameplayTagQuery::IsEmpty`는 토큰 스트림이 비었는지 본다. `FGameplayTagContainer::MatchesQuery`는 `Query.Matches(*this)`를 돌려준다.
- `Classes/GameplayTagContainer.h`: `HasAny`의 주석과 본문은 빈 `ContainerToCheck`에 false를 돌려준다. `HasAll`의 주석과 본문은 빈 `ContainerToCheck`에 true를 돌려주며, 이유는 "실패한 검사가 없었기 때문"이라고 적혀 있다.

래퍼 형태와 허용 목록 위험은 한 스튜디오 프로젝트의 헬퍼를 설계 검토 중에 읽어서 찾았다. 실행한 것은 없다. 그 프로젝트의 클래스와 데이터는 그 프로젝트 문서에 남는다.

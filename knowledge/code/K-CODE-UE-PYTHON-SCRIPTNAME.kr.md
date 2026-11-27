# K-CODE-UE-PYTHON-SCRIPTNAME: 선언에 ScriptName 메타데이터가 있는 Unreal 클래스가 에디터 Python에서 갖는 이름

- 요약: 에디터 Python은 리플렉션 클래스에 ScriptName 메타데이터가 있으면 C++ 이름이 아니라 그 메타데이터의 이름으로 클래스를 노출한다. UBlueprintGameplayTagLibrary는 unreal.GameplayTagLibrary이고, unreal.BlueprintGameplayTagLibrary는 AttributeError를 낸다. 호출을 쓰기 전에 UCLASS 줄을 읽는다.
- 종류: 참고 자료
- 범위: 스크립트에서 리플렉션 C++ 클래스와 Blueprint 함수 라이브러리를 부르는 Unreal Engine 5 에디터 Python(unreal 모듈). 헤드리스 pythonscript 실행을 포함한다
- 상태: 사용 중
- 확인한 날: 2026-11-25
- 조건: Unreal Engine 5.8 소스와 UnrealEditor-Cmd -run=pythonscript

## 안내

`ScriptName`은 클래스, 프로퍼티, 함수에 붙는 리플렉션 메타데이터다. 엔진은 이것을 그 항목을 스크립트 언어로 내보낼 때 쓸 이름이라고 설명한다. `UCLASS`에 `meta=(ScriptName="X")`가 있으면 에디터 Python은 그 클래스를 `unreal.X`로 노출한다. 이 경우 접두사를 뗀 C++ 이름은 등록되지 않는다.

`UBlueprintGameplayTagLibrary`는 `UCLASS(meta=(ScriptName="GameplayTagLibrary"))`로 선언되어 있다. 그래서 이 클래스의 함수는 `unreal.GameplayTagLibrary.<함수>`로 부른다. `unreal.BlueprintGameplayTagLibrary`로 부르면 `AttributeError: module 'unreal' has no attribute 'BlueprintGameplayTagLibrary'`로 실패한다.

함수 이름은 함수에 자기 `ScriptName`이 없으면 C++ 이름을 평소처럼 스네이크 케이스로 바꾼 것이다. `MakeGameplayTagQuery_MatchAnyTags`는 `make_gameplay_tag_query_match_any_tags`이고, `MakeGameplayTagContainerFromArray`는 `make_gameplay_tag_container_from_array`다.

## 적용 범위와 예외

UE 5.8의 클래스 하나로 확인했다. `ScriptName`은 클래스마다 따로 붙고 대부분의 클래스에는 없으므로, 다른 클래스는 그 선언을 직접 읽어야 한다. 이 메타데이터가 없는 클래스는 접두사를 뗀 C++ 이름을 그대로 쓴다. 같은 실행에서 `unreal.EditorAssetLibrary` 호출은 성공했지만 그 선언은 읽지 않았다.

이 메타데이터는 세미콜론 뒤에 폐기된 이름을 더 적을 수 있다. 그런 추가 이름이 Python에서 풀리는지는 시험하지 않았다.

## 점검

- `unreal.<클래스>`를 쓰기 전에 C++ 선언의 `UCLASS(...)` 줄에서 `ScriptName` 값을 읽는다.
- 긴 헤드리스 스크립트에서는 스크립트가 쓰는 `unreal.<클래스>`를 맨 위에서, 첫 변경 전에 모두 풀어 본다. 그러면 이름이 틀렸을 때 객체를 만들거나 바꾸기 전에 실행이 멈춘다.
- 실패한 실행 뒤에는 스크립트가 무엇을 남겼는지 확인한다. 확인한 실행에서는 에셋을 메모리에 만든 뒤, 저장하기 전에 실패했고 디스크에 파일이 생기지 않았다.

## 근거

- 엔진 소스, UE 5.8: `Engine/Source/Runtime/CoreUObject/Public/UObject/ObjectMacros.h`의 클래스 메타데이터 목록에 있는 `ScriptName` 항목과 그 주석.
- 엔진 소스, UE 5.8: `Engine/Source/Runtime/GameplayTags/Classes/BlueprintGameplayTagLibrary.h`의 `UCLASS(meta=(ScriptName="GameplayTagLibrary"), MinimalAPI)` 줄과 `MakeGameplayTagQuery_MatchAnyTags`, `MakeGameplayTagContainerFromArray` 선언.
- 작업 중 확인(2026-11-25): `unreal.BlueprintGameplayTagLibrary.make_gameplay_tag_query_match_any_tags`를 부른 `-run=pythonscript` 실행이 위 AttributeError로 끝났다. 같은 스크립트를 `unreal.GameplayTagLibrary`로 바꾸자 컨테이너와 쿼리를 만들고, 에셋을 저장하고, 값을 다시 읽었다.

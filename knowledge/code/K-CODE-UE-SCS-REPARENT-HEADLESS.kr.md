---
id: K-CODE-UE-SCS-REPARENT-HEADLESS
title: 헤드리스 에디터 Python에서 블루프린트 컴포넌트를 다른 부모 아래로 옮기는 방법
summary: UE 5.8에서 blueprint_context를 준 SubobjectDataSubsystem.reparent_subobject는 블루프린트 에디터 미리보기 액터가 없으면 실패한다("In a blueprint context there must be an actor preview"). attach_subobject(new_parent, child)는 미리보기 없이 SCS 노드를 옮기지만 자식의 상대 트랜스폼을 그대로 두므로, 옮긴 뒤 의도한 상대 트랜스폼을 직접 넣고 스폰한 인스턴스로 월드 트랜스폼을 확인한다.
kind: method
scope: 블루프린트 에디터를 열지 않은 헤드리스나 스크립트 에디터에서 Unreal Engine 5 에디터 Python으로 블루프린트 컨스트럭션 스크립트(SCS) 컴포넌트를 고칠 때
keywords: [SubobjectDataSubsystem, reparent_subobject, ReparentSubobject, ReparentSubobjectParams, ActorPreviewContext, attach_subobject, AttachSubobject, DetachSubobject, USCS_Node, SimpleConstructionScript, AddChildNode, ParentComponentOrVariableName, add_new_subobject, scene component pivot, non-uniform scale, make_relative, ExecutePythonScript, headless editor, 컴포넌트 부모 변경, 피벗]
status: active
checked_at: "2026-11-24"
context:
  engine: Unreal Engine 5.8 소스와 에디터 Python (UnrealEditor-Cmd -ExecutePythonScript, -nullrhi)
---

## 지침

`USubobjectDataSubsystem::ReparentSubobject`(Python `reparent_subobject`)에 `ReparentSubobjectParams.blueprint_context`를 주면, `actor_preview_context`에 블루프린트 에디터의 미리보기 액터가 없을 때 false를 돌려주고 `Failed to reparent: In a blueprint context there must be an actor preview!`를 로그에 남긴다. 헤드리스 스크립트에는 그런 에디터가 없다.

`AttachSubobject(OwnerHandle, ChildHandle)`(Python `attach_subobject(new_parent, child)`)는 미리보기가 필요 없다. 현재 부모에 `DetachSubobject`를 불러 SCS 노드를 루트 목록이나 부모의 자식 목록에서 빼고, 새 부모 SCS 노드의 자식으로 넣거나 네이티브나 상속 부모를 가리키는 루트 노드로 넣는다. 트랜스폼은 바꾸지 않는다. 자식의 상대 위치, 회전, 스케일은 그대로이고 이제 새 부모 기준이 된다. 옮긴 뒤 의도한 상대 트랜스폼을 직접 넣는다.

흔한 쓰임은 공용 피벗과 비균일 스케일 메시 사이에 스케일 1인 Scene 컴포넌트를 끼워, 형제 컴포넌트가 메시 스케일을 물려받지 않게 하는 것이다. 옮기는 자식과 새 부모가 같은 옛 부모 기준이었다면 새 상대 트랜스폼은 `old_relative.make_relative(new_parent_relative)`로 구한다.

## 적용 범위와 예외

부모가 네이티브 C++ 컴포넌트인 새 SCS Scene 노드 아래로, 블루프린트에서 더한 SCS 노드를 옮기는 경우를 확인했다. 네이티브나 상속 컴포넌트를 옮기는 경우는 다루지 않는다. `CanReparent` 규칙은 그대로 적용된다. 열린 블루프린트 에디터 안에서는 미리보기 액터로 월드 배치까지 유지하는 `reparent_subobject`가 맞는 호출이다.

인스턴스별 트랜스폼 덮어쓰기가 없는 레벨 배치 인스턴스는 에디터에서 레벨을 불러올 때(컨스트럭션 스크립트 재실행) 새 계층을 따른다. 옮긴 컴포넌트의 상대 트랜스폼을 덮어쓴 인스턴스는 옛 숫자를 그대로 두고 그것이 새 부모 기준이 되므로, 저장 전에 살펴본다.

한 번의 실행에서 컴포넌트 템플릿에서 `get_editor_property("RelativeLocation")`로 읽은 구조체가 같은 템플릿에 나중에 한 `set_editor_property`를 반영했다. 옛 값이 계속 필요하면 원본 프로퍼티를 바꾸기 전에 새 구조체로 값을 복사한다.

## 점검

- 고치기 전에 블루프린트 인스턴스를 스폰해 옮길 컴포넌트마다 월드 위치, 회전, 스케일을 기록하고, 고치고 컴파일한 뒤 다시 스폰해 허용 오차로 비교한다.
- 옮긴 노드마다 서브오브젝트 트리와 스폰한 인스턴스(`get_attach_parent`)에서 부모를 확인한다.
- 저장한 에셋의 SCS 노드를 읽는다. 새 부모의 `ChildNodes`에 옮긴 노드가 있고, 옮긴 노드에는 더 이상 `ParentComponentOrVariableName`이 없어야 한다.
- 오류 0으로 컴파일하고, 모든 점검을 통과했을 때만 저장한다.

## 근거

- 엔진 소스, UE 5.8: `Editor/SubobjectDataInterface/Private/SubobjectDataSubsystem.cpp`, `ReparentSubobjects`, `DetachSubobject`, `AttachSubobject`.
- 작업 점검(2026-11-24): `-nullrhi` `-ExecutePythonScript` 실행에서 `blueprint_context`를 준 `reparent_subobject`가 위 로그와 함께 false를 돌려줬다. `attach_subobject`로 SCS 노드 6개를 새 Scene 노드 3개 아래로 옮겼고, 컴파일 오류 0, 점검 161개 통과(월드 트랜스폼 0.01 cm 이내와 쿼터니언 내적 1 - 1e-7 초과, 부모, 프로퍼티 값, SCS 노드 필드), 불러온 레벨의 배치 인스턴스도 새 부모를 보였다.

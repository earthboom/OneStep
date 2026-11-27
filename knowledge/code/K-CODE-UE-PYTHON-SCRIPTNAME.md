---
id: K-CODE-UE-PYTHON-SCRIPTNAME
title: Which name an Unreal class has in editor Python when its declaration carries ScriptName metadata
summary: Editor Python exposes a reflected class under the name given by its ScriptName metadata when that metadata exists, not under its C++ name. UBlueprintGameplayTagLibrary is unreal.GameplayTagLibrary; unreal.BlueprintGameplayTagLibrary raises AttributeError. Read the UCLASS line before writing the call.
kind: reference
scope: Unreal Engine 5 editor Python (unreal module) calling reflected C++ classes and Blueprint function libraries from scripts, including headless pythonscript runs
keywords: [ScriptName, UCLASS meta, unreal module, editor Python, AttributeError, "module 'unreal' has no attribute", BlueprintGameplayTagLibrary, GameplayTagLibrary, UBlueprintGameplayTagLibrary, MakeGameplayTagQuery_MatchAnyTags, make_gameplay_tag_query_match_any_tags, make_gameplay_tag_container_from_array, pythonscript commandlet, headless editor, Python class name]
status: active
checked_at: "2026-11-25"
context:
  engine: Unreal Engine 5.8 source and UnrealEditor-Cmd -run=pythonscript
---

## Guidance

`ScriptName` is reflection metadata for classes, properties and functions. The engine describes it as the name to use when the item is exported to a scripting language. When a `UCLASS` carries `meta=(ScriptName="X")`, editor Python exposes the class as `unreal.X`. The C++ name without its prefix is not registered in that case.

`UBlueprintGameplayTagLibrary` is declared with `UCLASS(meta=(ScriptName="GameplayTagLibrary"))`. Its functions are therefore called as `unreal.GameplayTagLibrary.<function>`. A call through `unreal.BlueprintGameplayTagLibrary` fails with `AttributeError: module 'unreal' has no attribute 'BlueprintGameplayTagLibrary'`.

Function names follow the usual snake case conversion of the C++ name unless the function has its own `ScriptName`. `MakeGameplayTagQuery_MatchAnyTags` is `make_gameplay_tag_query_match_any_tags`, and `MakeGameplayTagContainerFromArray` is `make_gameplay_tag_container_from_array`.

## Applicability and exceptions

Checked for one class in UE 5.8. Other classes need their own declaration read, because `ScriptName` is set per class and most classes do not carry it. A class without the metadata keeps its C++ name without the prefix; the same run called `unreal.EditorAssetLibrary` successfully, but its declaration was not read.

The metadata may list deprecated names after a semicolon. Whether such additional names resolve in Python was not tested.

## Checks

- Before writing `unreal.<Class>`, read the `UCLASS(...)` line of the C++ declaration for a `ScriptName` value.
- In a long headless script, resolve every `unreal.<Class>` the script uses at the top, before the first change. A wrong name then stops the run before any object is created or modified.
- After a failed run, confirm what the script left behind. In the checked run the failure came after an asset was created in memory and before it was saved, and no file appeared on disk.

## Evidence

- Engine source, UE 5.8: `Engine/Source/Runtime/CoreUObject/Public/UObject/ObjectMacros.h`, the `ScriptName` entry in the class metadata list and its comment.
- Engine source, UE 5.8: `Engine/Source/Runtime/GameplayTags/Classes/BlueprintGameplayTagLibrary.h`, the `UCLASS(meta=(ScriptName="GameplayTagLibrary"), MinimalAPI)` line and the declarations of `MakeGameplayTagQuery_MatchAnyTags` and `MakeGameplayTagContainerFromArray`.
- Task check (2026-11-25): a `-run=pythonscript` run calling `unreal.BlueprintGameplayTagLibrary.make_gameplay_tag_query_match_any_tags` ended with the AttributeError above. The same script with `unreal.GameplayTagLibrary` built the container and the query, saved the asset and read the values back.

---
id: K-CODE-UE-SCS-REPARENT-HEADLESS
title: How to move a Blueprint component under another parent from headless editor Python
summary: In UE 5.8 SubobjectDataSubsystem.reparent_subobject with a blueprint_context fails without an open Blueprint editor preview actor ("In a blueprint context there must be an actor preview"). attach_subobject(new_parent, child) moves the SCS node without a preview but keeps the child's relative transform, so set the intended relative transform afterwards and verify world transforms on a spawned instance.
kind: method
scope: Unreal Engine 5 editor Python editing Blueprint construction script (SCS) components in a headless or scripted editor without an open Blueprint editor
keywords: [SubobjectDataSubsystem, reparent_subobject, ReparentSubobject, ReparentSubobjectParams, ActorPreviewContext, attach_subobject, AttachSubobject, DetachSubobject, USCS_Node, SimpleConstructionScript, AddChildNode, ParentComponentOrVariableName, add_new_subobject, scene component pivot, non-uniform scale, make_relative, ExecutePythonScript, headless editor, 컴포넌트 부모 변경, 피벗]
status: active
checked_at: "2026-11-24"
context:
  engine: Unreal Engine 5.8 source and editor Python (UnrealEditor-Cmd -ExecutePythonScript, -nullrhi)
---

## Guidance

`USubobjectDataSubsystem::ReparentSubobject` (Python `reparent_subobject`) with `ReparentSubobjectParams.blueprint_context` set returns false and logs `Failed to reparent: In a blueprint context there must be an actor preview!` unless `actor_preview_context` holds the Blueprint editor's preview actor. A headless script has no such editor.

`AttachSubobject(OwnerHandle, ChildHandle)` (Python `attach_subobject(new_parent, child)`) needs no preview. It calls `DetachSubobject` on the current parent (removing the SCS node from the root set or its parent's child list) and adds the node as a child of the new parent's SCS node, or as a root node pointed at a native or inherited parent. It does not convert transforms: the child's relative location, rotation and scale stay as they were, now relative to the new parent. Set the intended relative transform explicitly after the move.

A common use is inserting a scale-1 Scene component between a shared pivot and a mesh with non-uniform scale, so that sibling components no longer inherit the mesh scale. Compute each moved child's new relative transform with `old_relative.make_relative(new_parent_relative)` when both were relative to the same old parent.

## Applicability and exceptions

Checked on Blueprint-added SCS nodes moved under a newly added SCS Scene node whose parent is a native C++ component. Moving a native or inherited component is not covered; `CanReparent` rules still apply. `reparent_subobject` remains the right call inside an open Blueprint editor, where it also keeps world placement through the preview actor.

Placed level instances without per-instance transform overrides follow the new hierarchy when the level is loaded in the editor (construction script rerun). Instances that override a moved component's relative transform keep the old numbers, now relative to the new parent; inspect them before saving.

In one run, a struct read with `get_editor_property("RelativeLocation")` from a component template reflected a later `set_editor_property` on the same template. Copy values into a new struct before changing the source property when the old value is still needed.

## Checks

- Before editing, spawn an instance of the Blueprint and record world location, rotation and scale of every component that will move; after editing and compiling, spawn again and compare with a tolerance.
- Check each moved node's parent in the subobject tree and the spawned instance (`get_attach_parent`).
- Read the saved asset's SCS nodes: new parent's `ChildNodes` lists the moved nodes, and moved nodes no longer carry `ParentComponentOrVariableName`.
- Compile with zero errors and save only when every check passes.

## Evidence

- Engine source, UE 5.8: `Editor/SubobjectDataInterface/Private/SubobjectDataSubsystem.cpp`, `ReparentSubobjects`, `DetachSubobject` and `AttachSubobject`.
- Task check (2026-11-24): `reparent_subobject` with `blueprint_context` returned false with the log above in a `-nullrhi` `-ExecutePythonScript` run; `attach_subobject` moved six SCS nodes under three new Scene nodes, compile had 0 errors, 161 checks passed (world transforms within 0.01 cm and quaternion dot above 1 - 1e-7, parents, property values, SCS node fields), and a placed instance in a loaded level showed the new parents.

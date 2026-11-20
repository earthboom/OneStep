---
id: K-CODE-UE-GAS-CUE-EXECUTE-VS-ADD
title: Choose ExecuteGameplayCue for a one-shot event and AddGameplayCue for a persistent state in Unreal GAS
summary: ExecuteGameplayCue sends one Executed event through an unreliable multicast and stores nothing, so late or out-of-relevancy clients never see it; AddGameplayCue stores the cue in a replicated container that also grants the cue tag, so it survives relevancy changes but must be removed, and one RemoveGameplayCue removes every entry with that tag.
kind: reference
scope: Unreal Engine 5 GameplayAbilities plugin, UAbilitySystemComponent cue API called from abilities or actors on a networked game
keywords: [GameplayCue, ExecuteGameplayCue, AddGameplayCue, RemoveGameplayCue, AddGameplayCue_MinimalReplication, FActiveGameplayCueContainer, NetMulticast, prediction key, IsLocalClientKey, WhileActive, OnActive, Executed, Removed, late join, relevancy]
status: active
checked_at: "2026-11-20"
context:
  engine: Unreal Engine 5.8 (release/5.8.0p5 source)
---

## Guidance

Pick the API by what the presentation represents, not by how long the effect looks:

- **One-shot event** (hit spark, impact sound, camera shake, cast flash): `ExecuteGameplayCue`. The authority queues the cue in `UGameplayCueManager`, and `FlushPendingCues` sends it through `NetMulticast_InvokeGameplayCueExecuted_WithParams`, an unreliable multicast. Nothing is stored and no tag is granted. A client that is not relevant at that moment, joins later, or drops the packet never sees it, which is the correct result for an event.
- **Persistent state** (buff aura, channel loop, attached effect that must still show when a client gains relevancy): `AddGameplayCue` with a matching `RemoveGameplayCue`. The authority appends an entry to `ActiveGameplayCues` (a fast array), raises the cue tag count on the owner's tag map, sends an unreliable `NetMulticast_InvokeGameplayCueAdded_WithParams` for `OnActive`, and plays `WhileActive` locally. Clients get `WhileActive` from `PostReplicatedAdd` and `Removed` from `PreReplicatedRemove`, so a client that becomes relevant later still starts the cue (it gets `WhileActive`, not `OnActive`).

Prediction is shared by both: on a non-authority machine each call does local work only when the scoped prediction key `IsLocalClientKey()`. Execute then plays `Executed` locally, and Add calls `PredictiveAdd` plus local `OnActive` and `WhileActive`; the server's copy carries the same key, and the receiving client skips it, so there is no double play. Without a local key a client call does nothing.

## Applicability and exceptions

- `AddGameplayCue` does not deduplicate. Two adds of one tag create two entries, the second add on the authority does not replay `WhileActive`, and one `RemoveGameplayCue` removes every entry of that tag. Reference-count in game code if two owners can share one cue tag.
- The added cue tag counts as an owned gameplay tag on the ASC, so a tag query or ability blocking rule can see it. An executed cue has no tag footprint.
- Cue parameters of an added cue replicate with the entry; updating them requires remove and add. An executed cue's parameters are sent once.
- `AddGameplayCue_MinimalReplication` stores the cue in the container that replicates only to simulated proxies in `Mixed` mode; the owning client is expected to get the cue from its replicated gameplay effect instead.
- In `Mixed` replication mode the engine rewrites the RPC prediction key in `AddGameplayCue_Internal` to avoid a double play on the autonomous proxy; projects that override the replication proxy must keep that rule.
- Cues that come from a gameplay effect's `GameplayCues` list follow the effect: instant effects execute, duration and infinite effects add and remove. Use the direct calls only for presentation that no effect owns.
- A project can add local-only helpers that call `UGameplayCueManager::HandleGameplayCue` directly. Those skip the ASC container entirely: no tag, no replication, no later `Removed` from the server, so the local side must remove what it added.

## Checks

- For each cue, ask: should a client that gains relevancy one second later see it? Yes means Add/Remove; no means Execute.
- For each `AddGameplayCue`, find the `RemoveGameplayCue` on every end path (ability end, cancel, owner death, actor destruction).
- When a client calls either API, confirm a local prediction key is in scope (an active prediction window); otherwise the call is silently dropped on that client.
- Search for the same cue tag added by more than one owner before relying on one remove.

## Evidence

Read in the UE 5.8 release source on 2026-11-20, plugin `Engine/Plugins/Runtime/GameplayAbilities/Source/GameplayAbilities`:

- `Private/AbilitySystemComponent.cpp`: `ExecuteGameplayCue` forwards to the cue manager with `ScopedPredictionKey`; `AddGameplayCue_Internal` authority branch (`AddCue`, Mixed mode key rewrite, `Call_InvokeGameplayCueAdded_WithParams`, local `WhileActive` only when the tag was not already in the list) and `IsLocalClientKey` branch (`PredictiveAdd`, local `OnActive` and `WhileActive`); `RemoveGameplayCue_Internal`; multicast implementations that skip a local client key.
- `Public/AbilitySystemComponent.h`: `NetMulticast_InvokeGameplayCueExecuted_WithParams` and `NetMulticast_InvokeGameplayCueAdded_WithParams` are declared `NetMulticast, unreliable`.
- `Private/GameplayCueManager.cpp`: `InvokeGameplayCueExecuted_WithParams`, `AddPendingCueExecuteInternal`, `FlushPendingCues` (authority sends the multicast; a client with a local key invokes `Executed` locally).
- `Private/GameplayCueInterface.cpp`: `FActiveGameplayCueContainer::AddCue` (new entry, `UpdateTagMap` +1), `RemoveCue` (removes all entries of the tag, `Removed` per entry), `PredictiveAdd`, `PredictiveRemove`, `FActiveGameplayCue::PostReplicatedAdd` and `PreReplicatedRemove`.

Applied in one studio project that splits replicated and local-only cue helpers; the project-specific rules stay in that project's documents.

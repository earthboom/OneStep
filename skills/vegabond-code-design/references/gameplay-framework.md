# Gameplay framework and content design

Apply this when choosing or changing the game's runtime structure, the contracts through which content extends gameplay, or dependencies between features. Keep the decisions and checks in the existing brief or design. Use only the parts relevant to the change. For a local correction that preserves the contract, use the existing path and check the affected behavior.

## Plan a new game foundation

Use the [representative play sequences](#derive-the-framework-from-representative-play) and include a failure or interruption that affects the design. Settle the following decisions before choosing the project scaffold, folders, shared base types or optional packages.

| Decision | Record in the existing brief |
| --- | --- |
| Framework | Choose the gameplay entry point, time model and authority. Map them to appropriate Unity or Unreal roles for the chosen engine, target platform and constraints. Identify the parts of the rules that benefit from engine-independent C# or C++, and the parts owned by the engine's world, physics, assets or networking. If the engine is undecided, keep the gameplay contracts explicit and compare the engine choices against those contracts. |
| State ownership | Name who creates, writes, reads and releases each consequential state. Distinguish object, scene or world, session or match, and persisted lifetimes as needed. Specify what survives transitions such as scene exit, respawn or reconnect when the game supports them. Route changes through the owner and give presentation the state or results it reads. |
| Content entry path | Trace the first content item and a plausible second variant from authoring through validation, registration and play. Identify the owning feature, stable ID or contract where needed, assembly point and permitted dependencies. State which changes use definitions and which require a rule change. |

Use the simplest engine facilities and module boundaries that meet those decisions. Record the concrete requirement or budget that would justify a more elaborate framework. For example, a turn-based card adventure can use ordered combat commands and authored card definitions, while exploration retains its own map state. The handoff may be a short section in the existing brief. For a strategy or design-only request, return the design decisions, assumptions and proposed checks. Carry them into implementation when the request includes it.

## Derive the framework from representative play

Start with an existing design or describe a short sequence of player input, rule execution, feedback, and the next meaningful choice. Include a second sequence if a different mode or hybrid activity changes the guarantees. Identify the technical consequences relevant to the chosen sequence, such as turn or real-time scheduling, response deadlines, simulation authority, replication, deterministic replay, persistence, authoring, and expected workload. Tie each consequential choice to a gameplay requirement and observable result. Keep unknown requirements attached to the decisions they affect. [Genre and observable play](../../../knowledge/game/K-GAME-DESIGN-FRAMEWORK.md)

For example, a turn-based tactics game may need a place to validate commands, resolve actions in rule order, and expose the turn's result. A real-time co-op action game may need responsive local feedback, authoritative outcomes, and recovery when replicated state arrives late. Derive these requirements from the actual game. Share a rule across these modes only if its inputs, guarantees, and intended changes really coincide. Place engine-independent rules in ordinary C++ when this serves an actual testing or reuse need. Preserve existing engine ownership and hooks for behavior tied to worlds, actors, assets, or networking.

## Give content an extension path

Choose one current content item and one credible variation, such as a second encounter, weapon, quest, or ruleset. Walk through how an author creates, validates, registers, plays, and updates each. Identify the stable rules and their owners, the authored data that can vary, and behavior changes that need their own implementation. Treat a common rule as shared only where its callers need the same guarantees and the rule should evolve together. Keep feature-specific state and internals with the owning feature. Define the small interface a caller needs, including authority, valid state, failure, and lifetime when relevant. [Information hiding](../../../knowledge/code/K-CODE-INFORMATION-HIDING.md)

Use validated data or assets for values and combinations with an existing meaning. Use a concrete function, type, or component to compose behavior that varies independently. Add an extension point or base type for an identified variation or framework contract, and check substitutability for public inheritance. Identify the place where content is registered and related features are assembled. For data consumed by existing content, saves, or network peers, preserve the relevant IDs, schemas, and contracts or specify a migration. Account for missing or invalid content at the point the project can detect it.

For stage additions and changes to shared gameplay code or rules, [set the regression scope](#set-gameplay-regression-scope) before implementation.

## Make feature dependencies explicit

Give independently optional features no direct sibling dependency. Shared rules or stable contracts may have a common owner, and the code or content that assembles a mode can depend on the features it selects. Put an intentional interaction between optional features in that assembly or in an integration that is enabled when its prerequisites are available. If the product requires one feature for another, document the dependency direction, the required contract, and the unavailable case. Avoid cycles and preserve the target project's legitimate dependency directions. [Dependency direction](../../../knowledge/code/K-CODE-DEPENDENCY-DIRECTION.md)

Trace the affected edges in source and build configuration, authored content, and runtime. Look at public types, includes, modules and plugins; hard or soft asset references and registration data; and object lookup, events, initialization, and cleanup. An event, tag, or soft reference still carries a dependency if a particular feature must provide it for the flow to work. For Unreal, inspect relevant `Build.cs` or plugin declarations, check affected Blueprint and data-asset references with the available asset tools, and verify registration and teardown in the intended world and network role. [Unreal build dependencies](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-modules) · [Unreal Reference Viewer](https://dev.epicgames.com/documentation/en-us/unreal-engine/reference-viewer-in-unreal-engine)

## Set gameplay regression scope

In the existing brief, state the intended change and what players should still see or be able to do. Include the authoritative or persisted result when the behavior depends on it. For each proposed check, identify the starting state, action, expected result, actual gameplay entry point, and required environment. Use the existing game contract or an accepted baseline to define the expectation.

| Change | Select before implementation |
| --- | --- |
| Shared gameplay code or rules | Representative existing callers or stages with different uses of the rule or lifecycle. Include a relevant invalid or interrupted path when it can expose a regression. |
| Stage addition | The new stage's normal registration and play path and representative existing content affected through shared rules, assets, or progression. Include existing saves and target builds when the change reaches those boundaries. |

Use both rows when adding a stage changes shared gameplay code or a shared rule defined in data. Scale the check set to the affected contracts and supported configurations. For design-only work, hand off the proposed checks, expected observations, and any untested assumptions. [Gameplay regression verification](../../vegabond-code/references/verification.md#gameplay-regression-checks)

## Design gameplay feedback

In the existing brief, trace accepted input, action start, outcome, and recovery. State which feedback can begin with the action and which communicates a confirmed outcome. For each relevant outcome, such as hit, guard, or miss, name the resolving gameplay owner and the camera, visual, audio, or haptic cues that express its result. Match contact cues to the resolved location and direction when those details matter. For network anticipation, specify what can play early and how confirmation, rejection, or correction handles duplicate or misleading cues.

Record when the next input can be captured and acted on. If feedback uses hitstop or other time changes, name which actors and clocks pause or continue, including input buffering and rule timers where affected. Treat hit timing, gameplay recoil, and changes to action windows as gameplay decisions. Presentation-only settings preserve those decisions.

Decide what must remain readable after impact and when effects overlap, such as aim, an incoming warning, or the difference between a guard and a hit. Prioritize those cues and give essential information another supported sensory path when shake, effects, sound, or haptics are reduced or unavailable. Hand off representative outcomes, a rapid repeat or interruption if relevant, and the settings and observations needed for [gameplay feedback verification](../../vegabond-code/references/verification.md#gameplay-feedback-checks).

## Review the change through content and play

- **Genre fit.** Exercise the sequence that motivated the design through the real gameplay entry point. Define what the player and authoritative state should observe, including one failure or ordering case when it affects the choice.
- **Extension and maintenance.** Add or trace the second representative variant through the actual authoring and registration path. Record which shared modules, files, public interfaces, and assets need edits and why. Inspect whether the changes stay with the new content and its registration unless an explicit shared contract changes. Recheck existing content affected by that contract.
- **Independence.** For each affected configuration the project supports, exercise core play and the eligible features alone or together as relevant. Check feature absence in the build or package when absence is supported, and disabled behavior when only runtime disabling is supported. If the product supports both, check both. For a supported runtime lifecycle, verify cleanup of registered behavior, subscriptions, or pending work and repeat activation when applicable. Check a likely accidental dependency with an actual build, load, or gameplay observation that could fail if the dependency exists.

A design returns expected observations and how to obtain them. Verify the implementation with the target project's existing build, test, editor, and packaging paths as applicable. Keep evidence from a proposed check or isolated rule test distinct from the integrated play result. [Design review](review.md) · [Software verification](../../vegabond-code/references/verification.md)

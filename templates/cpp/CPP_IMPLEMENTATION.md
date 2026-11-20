# C++ Implementation Guide

Use the relevant section when a change calls for an implementation decision. Follow the working project's instructions and conventions first.

## Language features, types, and ownership

- Choose features and library types supported by the target's toolchain. Follow the surrounding code's conventions for type deduction and error handling. Use `auto` when it makes the declaration easier to read, and make intended copies, references, and pointers explicit.
- Pass inexpensive values by value and expensive read-only inputs by `const&` where appropriate. Use RAII for resource ownership. Confirm that the underlying object outlives any stored view or reference.
- **Plain C++ example** — Use `const auto& item` to inspect item objects in a loop when the project permits type deduction. Copy a `std::string_view` into an owning string when the text must outlive its source.
- **Unreal C++ example** — Follow the module's approach to `auto`. Use a `UPROPERTY()`-marked `TObjectPtr<UInventoryComponent>` for a persistent reference that must keep the component reachable. Use `TWeakObjectPtr` for a non-owning cache and check validity when using it.

References — [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines) · [Abseil parameter passing](https://abseil.io/tips/234) · [Epic C++ coding standard](https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine) · [Unreal object pointers](https://dev.epicgames.com/documentation/en-us/unreal-engine/object-pointers-in-unreal-engine)

## Names and call-site readability

- Use the project's domain terms and naming conventions. Give a name enough context to read correctly at its use site. Include units when the type leaves them implicit. Name booleans as predicates.
- When a literal flag or a sequence of flags obscures a choice at the call site, use a named mode or options type that expresses the choice.
- **Plain C++ example** — Use `remainingSlots` or `retryDelayMs`. A call such as `Save(path, SaveMode::Overwrite)` makes the save mode visible.
- **Unreal C++ example** — Use `MaxStackCount` for a limit, `bHasPendingReward` for a boolean field, and `IsInventoryFull()` for a query.

References — [Identifier comprehension study](https://www.se.cs.uni-saarland.de/publications/docs/HoSeHo17.pdf) · [Abseil call-site readability](https://abseil.io/tips/94) · [Epic naming conventions](https://dev.epicgames.com/documentation/en-us/unreal-engine/epic-cplusplus-coding-standard-for-unreal-engine#naming-conventions)

## Design patterns

Name the behavior that varies or the boundary that needs adapting, then use the smallest implementation that meets the requirement. Reuse the project's existing mechanisms when they fit.

| Need | Plain C++ example | Unreal C++ example |
| --- | --- | --- |
| **Strategy** for interchangeable behavior | Pass an event-specific reward formula as a function or lambda. | Pass a reward policy to a component that applies the result. |
| **Adapter** for an incompatible API | Translate an SDK result into the project's existing value and error types. | Translate the online service's result into the gameplay-facing result type. |
| **Observer** for independent consumers | Subscribe UI and telemetry callbacks to an inventory change and define when they unsubscribe. | Bind the HUD to the inventory component's change delegate and unbind it when the HUD is torn down. |
| **State machine** for constrained transitions | Model `Idle`, `Charging`, and `Released` with an `enum class` and explicit transitions. | Keep ability-state transitions in the component that owns the state. |

References — [Design pattern maintenance experiment](https://ps.ipd.kit.edu/downloads/zeitschriftenartikel_PatmainTSE2001.pdf) · [C++ Software Design](https://www.oreilly.com/library/view/c-software-design/9781098113155/ch05.html) · [Unreal delegates](https://dev.epicgames.com/documentation/en-us/unreal-engine/delegates-and-lambda-functions-in-unreal-engine)

## Performance work

- Define the metric and a representative workload. Profile the relevant path, then target the measured cost, such as repeated work, copies, allocations, or poor locality.
- Verify the affected behavior and measure before and after with the same inputs and execution conditions. Report the result and relevant costs, such as added memory or setup time. If measurement is unavailable, describe the expected effect as a hypothesis.
- **Plain C++ example** — Before replacing repeated linear searches with an index, compare lookup time, index construction time, and memory use at representative sizes.
- **Unreal C++ example** — When profiling shows `TArray` reallocation overhead and the expected element count is known, try `Reserve()`. Compare allocation activity and frame time in Unreal Insights using the same gameplay scenario.

References — [Google performance tuning notes](https://abseil.io/fast/hints) · [Study of performance validation in coding-agent PRs](https://arxiv.org/abs/2610.03969) · [Unreal array containers](https://dev.epicgames.com/documentation/en-us/unreal-engine/array-containers-in-unreal-engine) · [Unreal Insights](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-insights-in-unreal-engine)

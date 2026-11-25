# Scope, design depth and delivery units

Use this with Scout's existing brief when the implementation boundary is a decision. A small change with a settled contract can go straight to its normal check.

## Establish what the change buys

Anchor the scope in one current and desired behavior at a real entry point. Identify the user, player, caller or content author who can observe it. Include the affected path and the adjacent behavior, data or platform guarantee that must survive. Name a tempting extension to defer only when someone might reasonably assume it is included. Use the supplied budget or target if it constrains the choice. Verify assumptions against an actual caller, save, build or play sequence. If two interpretations would change the outcome, apply Scout's ambiguity rule.

## Decide what warrants design

Ask which unsettled decision could force someone to redo work, lose data, change another consumer or build the wrong player experience. Name that consequence and the evidence needed to choose. The design can stop when the implementer can identify who owns the behavior, how the change fits existing contracts and what observation would disprove it.

| Situation | Proportionate action |
| --- | --- |
| The pattern, ownership and acceptance check are established, and the edit is easy to undo. | Carry the preservation check inline and implement. For a label-only correction, inspect the changed resource and rendered label. Exercise the command or shortcut if the changed resource also controls its binding. |
| A choice affects correctness, consumers or a costly commitment. | Resolve the specific tradeoff. Compare the smallest viable options, name the owner and failure behavior, and give the check that distinguishes them. A single persistence write can warrant this. |
| Reading the source cannot settle a material assumption about feasibility or player experience. | State the question, the cheapest representative probe, the observation and what each outcome changes. A paper sketch, compatibility fixture, target-device trace or greybox playtest may suffice. Keep dependent production work conditional until the observation exists. |

## Choose one pass or checked stages

Try describing the intermediate state that a proposed split would produce. **What can we verify or learn there, and what subsequent choice depends on the answer?** If there is no useful intermediate result, keep the contract change and its callers/tests in one coherent, reversible unit. Design depth and file count do not set the number of units.

Split when a usable behavior can be verified independently, a compatibility window must exist, or evidence from the first unit could change or cancel the next. Prefer a thin path through the real entry point to a list of isolated layers. A compatibility reader or disposable experiment can also be a valid first unit if it answers a named dependency. For each necessary boundary, record the result, its check and the downstream decision. If it fails, revise the implicated assumption before extending it. Keep the full requested outcome in scope and verify the integrated user or player path after the units come together.

One unit may touch UI, rules and persistence. Two units can proceed independently only when their interface and shared writes are understood and both can be checked separately. Sequence work that requires another unit's contract or evidence. Staging alone grants no permission for delegation, deployment or production data changes.

## Examples of decisions that change the plan

- **One pass after design.** A local inventory transfer must debit one slot and credit the other atomically. Resolve which existing transaction owns both updates and the notification. Keep the implementation and tests together. From the normal transfer command, verify conservation of quantity and that a rejected transfer leaves both slots intact. Splitting debit and credit would expose an invalid intermediate behavior.
- **Compatibility before rollout.** Old clients still write the existing save representation. Establish which versions must read which writes and what rollback must preserve. First exercise the compatible reader against real old fixtures and representative new data. Enable the new writer only when the supported readers can handle its output or a compatible rollout path exists. Retire legacy support only when the agreed support window closes. A failing older reader changes the format or rollout plan.
- **Gameplay uncertainty before content multiplication.** If players must find a route by following a sound, prototype one junction with placeholder audio. Observe an unprompted player's route choice and reason for it. If cues confuse players, adjust the cue or layout and retest. Once the behavior reads, a representative authored room loaded through the actual game can test the content pipeline before building more rooms. A scripted traversal checks routing and playback; a player observation supports the claim about discoverability.
- **Established game content.** An additional encounter using a proven schema can be authored and played with its existing neighbor in one unit. If the new encounter requires two packs that were promised to work independently, reopen the dependency decision and verify each supported pack configuration.

Hand the chosen boundary and reason back to the caller in the existing brief. For example, “Keep both inventory updates together because they preserve one quantity. Check the rejected transfer through the normal command.” A multi-unit handoff says which result unlocks the next and how the combined behavior will be judged. For a design-only request, leave those checks explicitly proposed.

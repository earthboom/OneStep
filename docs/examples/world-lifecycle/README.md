# Town, forest, combat, return

These examples apply OneStep's [world runtime design](../../../skills/vegabond-code-design/references/world-lifecycle.md) and [game runtime checks](../../../skills/vegabond-code/references/world-lifecycle-verification.md) to the same gameplay contract in Unity and Unreal. They use each engine's own representation and streaming operations. The projects are available under [Unity](unity/README.md) and [Unreal](unreal/README.md).

## Contract and checks

| Step | Observed outcome to check |
| --- | --- |
| Start in town from the [v1 save](fixtures/legacy-v1.json) | The loader resolves `forest-wolf` to `forest-wolf-v2`. HP is 100, quest stage is 0, and patrol steps start at 0. |
| Enter the forest | The engine loads the forest asynchronously and activates its NPC representation. Record request-to-activation latency and transition frame deltas. |
| Fight | A normal attack removes 40 HP and advances the quest to stage 1. HP is now 60. |
| Return to town | The engine unloads the forest and removes the NPC representation. The session retains canonical identity, HP 60 and quest stage 1 while the region and its view are absent. |
| Wait outside and re-enter | The session advances at least one patrol step while no view exists. A newly bound view presents the same NPC at HP 60 and quest stage 1. Record the revisit separately from the first visit. |
| Persist the result | Produce a v2 save and load it through the normal loader. Preserve the canonical ID and the final HP, quest stage and patrol data. Reject unsupported or malformed input with an explicit diagnostic. |

The scene or level owns the NPC view. The active game session owns gameplay state and advances the simple offscreen patrol on game time. Save data stores persistent values and the stable ID. The world transition code owns the load operations. This lets an unloaded representation disappear without changing the simulation's identity or resetting progress. The retired-ID mapping is an explicit compatibility decision for this fixture.

## Observations

Both projects loaded the same v1 fixture and observed HP 100 and quest stage 0 at startup. After the strike, the scene and level were unloaded with HP 60 and quest stage 1 intact. Each session advanced one patrol step while its NPC representation was absent. A different representation showed the preserved state on return. Both wrote and read back v2, rejecting unsupported input without changing the live state. Unreal also reloaded the save in a new process.

| Windows target | Independent process runs | First forest request to ready | Revisit request to ready | Largest sampled transition update gap |
| --- | ---: | ---: | ---: | ---: |
| [Unity 6000.0.77f1 Player](unity/README.md), D3D11 batch mode | 3 | 4.04–4.64 ms | 1.46–9.88 ms | 7.88 ms |
| Unreal 5.8.3 standalone Game, [NullRHI](unreal/Evidence/observed-nullrhi.json) | 3 | 15.21–20.62 ms | 10.01–24.38 ms | 8.41 ms |
| Unreal 5.8.3 standalone Game, [windowed D3D11](unreal/Evidence/observed-d3d11.json) | 3 | 52.85–56.17 ms | 40.78–60.07 ms | 17.34 ms |

The Unity pilot immediately after the build observed a 27.00 ms first load and a 1.45 ms revisit. The initial Unreal D3D11 check observed 93.87 ms and 63.69 ms. “First” means the first request in a new process. The OS and engine caches may already be warm. Each timing uses the engine-specific readiness boundary in its README. The scenes, graphics modes and workloads differ. The sampled gaps are wall-clock intervals between game updates. GPU render time, presented frames and production-scale streaming budgets need separate captures. The examples exercise single-player state, simple timed patrol and one combat action.

# Tactics workflow brief

Create a Windows console game in standalone C++17 for a player using stdin and stdout. Build and play the built-in encounter and Harrier first. Add the second encounter after that checkpoint so the observed edits can answer whether the authoring contract is reusable.

A move, strike, or guard spends one turn. The game validates the command against the current state, resolves the player action, resolves the enemy response, then displays the resulting state and outcome. A defeated enemy forfeits the response and the game reports it. Rejected syntax, illegal positions and unavailable encounter selections keep the current state. The initial human-facing playable path is `start core`, move into range, and strike. Harrier demonstrates guarding and counterattacking. The second pack changes starting orientation and stats.

The console owns command dispatch and catalog composition. The session owns positions, health and turn. A catalog loader validates and translates human-readable encounter files to concrete definitions before any session exists. File discovery enables physical omission and imposes a schema and stable IDs. Compiled pack registration would require an executable change for each addition. An explicit runtime manifest would put a second file between a pack and standalone play, so directory discovery fits this request.

| Question | Decision and acceptance check |
| --- | --- |
| Will a rejected or lethal action break the order? | Compare explicit command sequences, player and enemy event order, and the full state after every transition. The selected inputs cover invalid movement/strike, guard, victory and loss. |
| Can one pack rely on the other? | Verify catalog and play through four separate launches using real staged directories and measured file membership. Build a controlled broken copy with B relying on A and verify that B-only gameplay catches it. |
| Where does the next authored encounter propagate? | Hash source and original content before adding B. Compare the final hashes and file list, and explain the authored and verification changes. |

## Knowledge applied before implementation

- Adopted [K-CODE-DEPENDENCY-DIRECTION](../../../../knowledge/code/K-CODE-DEPENDENCY-DIRECTION.md#guidance) within the standalone app. The stable encounter definition is a concrete shared contract, the catalog composes optional files, and gameplay reads typed values. Check physical absence and verify which files change.
- Adopted [K-CODE-DATA-INVARIANTS](../../../../knowledge/code/K-CODE-DATA-INVARIANTS.md#guidance) as a design principle. Parse untrusted content before session construction and reject actions before mutating state. Check malformed definitions and independently expected state snapshots.
- Adopted [K-GAME-PROTOTYPE-PLAYTEST](../../../../knowledge/game/K-GAME-PROTOTYPE-PLAYTEST.md#guidance) for a small integrated play slice. Playable entry and useful runtime feedback answer the engineering question. Scenario playback covers the mechanism under the chosen commands.
- Rejected [K-GAME-STRATEGY-TURN-4X](../../../../knowledge/game/K-GAME-STRATEGY-TURN-4X.md#applicability-and-exceptions) for the one-unit turn contract because the historical case concerns empire-wide orders and campaigns. The fixture request supplies this game's turn contract.
- Adopted the independent expected-value check and accepted-baseline precondition from [R-CODE-UE-EVIDENCE-PROXY](../../../../records/code/R-CODE-UE-EVIDENCE-PROXY.md#negative-mutation-tests-require-an-accepted-baseline--2026-11-14). The Unreal real-time and media details have different mechanisms. Verify fixture membership, catalog IDs, board positions, health, turn, and relevant ordered output independently before testing a deliberately broken executable.

## Baseline and extension

MSVC built the baseline with `harrier.enc` as the only authored optional file. The harness staged that single file and played Crossing and Harrier through the executable before Bulwark existed. It recorded each expected turn, enemy response and health transition. The [baseline build](evidence/baseline-build.txt), [baseline play](evidence/baseline-play.txt), [baseline manifest](evidence/baseline-manifest.json), and [baseline replay](evidence/baseline-replay.txt) retain those observations. After building from this checkout, use `python -B verify.py --only a` to exercise the same A-only scenario with the current executable.

Bulwark added one authored file, `packs/bulwark.enc`. The existing scan discovered it using its ID and schema. SHA-256 comparison measured zero edits to gameplay source, the build script and Harrier. The verification script gained the B scenarios, configuration checks, content diagnostics and fault. [File comparison](evidence/baseline-vs-extension.json)

## Dependency and state paths

- Source and build. `build.cmd` compiles `main.cpp` as C++17. No pack ID, include, object or library from either optional file participates in the build.
- Content. `main` invokes `LoadCatalog` once, inserts Crossing and validates each present file into an `Encounter`. `Run` handles `list` and `start ID`, and successful selection constructs a `Session` from its own immutable definition. Each entry provides all six authored fields and directly depends on that shared schema.
- Runtime. `Run` validates syntax and dispatches to `Session::TryAction`. The session owns board positions, HP and turn. On success it resolves the player action, increments the turn once, resolves the enemy outcome and prints the resulting state. On rejection it prints the same state. No optional file is read during an action and there is no runtime pack loading or teardown.
- Counterexample. A mistaken lookup requiring `harrier.enc` before registering Bulwark would be invisible when both files are present. A temporary build with that condition passed Bulwark play in the both-files directory. B-only validation rejected the same executable at catalog and selection, after the original executable completed the B-only precondition. [Final run](evidence/final-run.txt)

## Observed play

| Launched optional files | Successful gameplay | End state by encounter |
| --- | --- | --- |
| None | Crossing | Turn 4, player HP 2, enemy HP 0 |
| Harrier only | Crossing and Harrier | Harrier turn 4, player HP 3, enemy HP 0 |
| Bulwark only | Crossing and Bulwark | Bulwark turn 5, player HP 1, enemy HP 0 |
| Both | Crossing, Harrier and Bulwark | Each reached the same end state as in its individual configuration |

Crossing's early out-of-range strike and off-board move left turn 0 and both units untouched. Harrier's guard absorbed 2 damage and countered for 1. In Bulwark, moving left twice put the player in melee with 2 HP. Moving into the enemy cell left that state unchanged, and a subsequent strike led to defeat on turn 3. The next `start bulwark` restored turn 0 and both units to full HP. The eight invalid content cases exited 2 with diagnostics and an empty stdout. [Final MSVC build](evidence/final-build.txt) · [Final runtime checks](evidence/final-run.txt) · [Default launch and direct stdin play](evidence/default-play.txt)

The linked OneStep workflow made the extension and physical absence checks part of the design before construction. It required a baseline play checkpoint, a measured authoring change, a full final launch matrix and an observable dependency failure. The learned application is scoped to this console fixture. The shared procedures provided historical guidance, and the local executable supplies the observations. The game commands and validation ran on Windows x64 with MSVC. AI verification complete. Awaiting vagabond testing or review.
